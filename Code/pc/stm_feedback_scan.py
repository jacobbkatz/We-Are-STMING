#!/usr/bin/env python3
"""Constant-current imaging with the feedback loop running on this computer.

Written 2026-09-17 at the bench, the night the first tip-sample junction was
found. It exists because the gap drifts closed in about ten seconds at a fixed
Z (`sessions/2026-09-17-bench.md` section 3.16), so a constant-height image is
not possible: something has to hold the current steady.

**The firmware's own loop, `CCON`, is barred by `STATUS.md` safety rule 8**,
which is Jacob and Nuh's to lift. This keeps the loop on the PC, where every
step is bounded and counted:

  * Z never leaves [Z_MIN_SAFE, Z_MAX_SAFE].
  * One pixel moves Z by at most MAX_STEP counts.
  * Saturated pixels and pixels stuck against a clamp are counted, and the run
    aborts if either gets out of hand.
  * Z is retracted and X/Y re-centred on every exit path, including Ctrl-C.

The value recorded at each pixel is the Z that holds the setpoint current,
which is the topograph. Every line is scanned forward and then backward:
**trace against retrace is the test of whether a feature is real.** On
2026-09-17 it was near zero for every image, so no structure was claimed.

Tested against a simulated junction by `stm_feedback_scan_test.py`, including
a deliberately reversed sign, which must run the loop into a clamp.

Usage:
    py stm_feedback_scan.py <half_width> <step> <n_lines> <setpoint> <out_csv>

    py stm_feedback_scan.py 400 40 12 3000 scan.csv
"""
import sys
import os
import time
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import serial
from stm_approach import Device, find_teensy

MID = 32768
Z_MIN_SAFE, Z_MAX_SAFE = 12000, 48000
Z_LOCATE_START, Z_LOCATE_END, Z_LOCATE_STEP = 10000, 48000, 200

# MEASURED 2026-09-17: the current changes tenfold per about 250 Z counts, and
# one motor step is also about 250 Z counts. Both in sessions/2026-09-17-bench.md.
COUNTS_PER_DECADE = 250.0
COUNTS_PER_NANOAMP = 320.5     # docs/FACTS.md, dummy junction 2026-09-16

MAX_STEP = 300                 # counts of Z per pixel. Raised from 150 on
                               # 2026-09-17: at 150 the loop could not follow
                               # this surface over a wide scan and saturated.
GAIN = 0.35                    # fraction of the log error corrected per step
ITERS = 5                      # feedback iterations per pixel
SAT = 32760                    # counts; at or past this the ADC is railed
# Noise on the reading the loop steers on: 46 counts (0.14 nA) averaged,
# 188 counts (0.59 nA) single-conversion. MEASURED 2026-09-17.
FLOOR = 60                     # counts; below this the log means nothing


def read_averaged(dev, timeout=0.15):
    """`ADCR` — the firmware's AVERAGED reading, not a single conversion.

    MEASURED 2026-09-17: 0.24 ms per read against 0.23 ms for a single
    conversion, and **46 counts of noise against 188** — four times quieter for
    the same time. Everything before this measurement ran the feedback loop on
    single conversions, at 0.59 nA of noise, which is most of a tunnelling
    current. Use this.
    """
    dev._write(b"ADCR")
    deadline = time.time() + timeout
    buf = b""
    while time.time() < deadline:
        waiting = getattr(dev._port, "in_waiting", 0)
        chunk = dev._port.read(waiting if waiting else 1)
        if chunk:
            buf += chunk
            if b"\n" in buf:
                try:
                    return int(buf.split(b"\n")[0].strip())
                except ValueError:
                    return None
    return None


def read_junction(dev):
    """The reading the loop steers on. Averaged when there is a real port.

    The simulated scope in the test harness has no port, so it falls back to its
    own read_adc and the tests still exercise the loop.
    """
    if getattr(dev, "_port", None) is None:
        return dev.read_adc()
    v = read_averaged(dev)
    if v is not None:
        return v
    return fast_read(dev)


def fast_read(dev):
    """A read that resynchronises instead of waiting out the long timeout.

    MEASURED 2026-09-17: the median read is 0.3 ms, but about 1.5% get no reply
    and those stalls cost up to 3 s each, which made a single image take a
    minute. The firmware takes four characters as soon as one byte arrives
    (see stm_console.py), so a partial command leaves it out of step; newlines
    flush it harmlessly.
    """
    v = dev.read_adc(timeout=0.12)
    if v is not None:
        return v
    dev._port.write(b"\n\n\n\n")
    dev._port.flush()
    time.sleep(0.01)
    dev._port.reset_input_buffer()
    return dev.read_adc(timeout=0.25)


class Loop:
    """One integral step per iteration, in decades of current."""

    def __init__(self, dev, setpoint):
        self.dev = dev
        self.setpoint = float(setpoint)
        self.z = None
        self.clamped = 0
        self.saturated = 0
        self.lost = 0

    def set_z(self, z):
        z = int(max(Z_MIN_SAFE, min(Z_MAX_SAFE, z)))
        if z in (Z_MIN_SAFE, Z_MAX_SAFE):
            self.clamped += 1
        self.dev._write(("DACZ %d\n" % z).encode())
        self.z = z

    def settle(self):
        """Run the loop at the current X, Y. Returns (z, last reading)."""
        last = 0
        for _ in range(ITERS):
            v = read_junction(self.dev)
            if v is None:
                self.lost += 1
                continue
            last = v
            mag = max(abs(v), FLOOR)
            if abs(v) >= SAT:
                self.saturated += 1
            # Too much current -> move Z DOWN, away from the sample. The HIGH
            # end extends toward the sample: MEASURED 2026-09-17.
            error_decades = math.log10(mag / self.setpoint)
            delta = -GAIN * error_decades * COUNTS_PER_DECADE
            delta = max(-MAX_STEP, min(MAX_STEP, delta))
            self.set_z(self.z + delta)
        return self.z, last


def locate(dev, setpoint):
    """Sweep Z up from the retracted end until the current crosses setpoint."""
    for z in range(Z_LOCATE_START, Z_LOCATE_END + 1, Z_LOCATE_STEP):
        dev._write(("DACZ %d\n" % z).encode())
        # Averaged, like the loop. On a single conversion the noise is 188
        # counts, so a setpoint near a real tunnelling current would be found on
        # a noise spike rather than on the surface.
        v = read_junction(dev)
        if v is not None and abs(v) >= setpoint:
            return z
    return None


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if len(argv) < 5:
        print(__doc__)
        return 2
    half, step, nlines = int(argv[0]), int(argv[1]), int(argv[2])
    setpoint, out = float(argv[3]), argv[4]
    # Optional 6th argument: the bias DAC code. 38229 is -0.5 V at the sample,
    # 43691 is -1.0 V. More volts holds the same current at a LARGER gap, which
    # is how a real STM stays out of contact.
    bias_code = int(argv[5]) if len(argv) > 5 else 38229

    xs = list(range(MID - half, MID + half + 1, step))
    ys = [MID - half + round(i * (2.0 * half) / max(nlines - 1, 1))
          for i in range(nlines)]

    portname = find_teensy()
    if not portname:
        print("No Teensy found.")
        return 1

    port = serial.Serial(portname, 115200, timeout=0.2)
    with port:
        time.sleep(1.0)
        dev = Device(port)
        rows = []
        try:
            dev.set_z(Z_LOCATE_START)
            dev._write(("DACX %d\n" % MID).encode())
            dev._write(("DACY %d\n" % MID).encode())
            dev._write(b"BIAS 38229\n")      # -0.5 V at the sample
            time.sleep(0.1)

            onset = locate(dev, setpoint)
            if onset is None:
                print("No junction in the Z range. Approach with the motor "
                      "first: stm_approach.py --z-retracted low "
                      "--motor-toward-sample negative")
                return 1

            loop = Loop(dev, setpoint)
            loop.set_z(onset)
            print("onset Z=%d, setpoint %d counts (%.2f nA), bias code %d, "
                  "%d x %d pixels"
                  % (onset, setpoint, setpoint / COUNTS_PER_NANOAMP, bias_code,
                     len(xs), len(ys)))

            t0 = time.time()
            for yi, y in enumerate(ys):
                dev._write(("DACY %d\n" % y).encode())
                line = {}
                for name, order in (("fwd", xs), ("back", list(reversed(xs)))):
                    zs = []
                    for x in order:
                        dev._write(("DACX %d\n" % x).encode())
                        z, _ = loop.settle()
                        zs.append(z)
                    if name == "back":
                        zs.reverse()
                    line[name] = zs
                rows.append((y, line["fwd"], line["back"]))
                if loop.saturated > 40 * (yi + 1) or loop.clamped > 40 * (yi + 1):
                    print("  ABORT: saturated %d, clamped %d -- the surface is "
                          "moving faster than the loop can follow"
                          % (loop.saturated, loop.clamped))
                    break
            print("  %d lines in %.2f s, saturated %d, clamped %d, lost reads %d"
                  % (len(rows), time.time() - t0, loop.saturated, loop.clamped,
                     loop.lost))
        finally:
            # Runs on success, on failure and on Ctrl-C.
            dev.set_z(Z_LOCATE_START)
            dev._write(("DACX %d\n" % MID).encode())
            dev._write(("DACY %d\n" % MID).encode())
            dev._write(b"BIAS 32768\n")
            time.sleep(0.05)

    with open(out, "w") as f:
        f.write("y,dir," + ",".join(str(x) for x in xs) + "\n")
        for y, fwd, back in rows:
            f.write("%d,fwd,%s\n" % (y, ",".join(str(v) for v in fwd)))
            f.write("%d,back,%s\n" % (y, ",".join(str(v) for v in back)))
    print("  wrote %s" % out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
