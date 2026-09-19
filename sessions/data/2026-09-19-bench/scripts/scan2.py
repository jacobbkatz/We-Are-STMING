"""Constant-current scan with the Z direction as a PARAMETER.

stm_feedback_scan.py hardcodes "the HIGH end of Z extends toward the sample" (measured on the old
tip, 2026-09-17). For the tip fitted on 2026-09-19 that is not established, so this wraps the same
tested Loop with a sign:

    toward = +1   high Z extends toward the sample (the old tip)
    toward = -1   low Z extends toward the sample

Everything else is stm_feedback_scan's: Z clamped to [Z_MIN_SAFE, Z_MAX_SAFE], MAX_STEP per
correction, saturated and clamped pixels counted, the run aborted when either gets out of hand.
locate() sweeps from the RETRACTED end toward the sample. Every exit retracts Z to the retracted end,
recentres X and Y and zeroes the bias.

Usage: py scan2.py <toward +1|-1> <half> <step> <nlines> <setpoint> <cpd> <reps> <out_prefix> [xheld]
  xheld = 1 runs the SAME timing with X never moving: the control.
"""
import sys
import os
import time
import math

sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
import stm_feedback_scan as fs

BIAS = 38229


class SLoop(fs.Loop):
    def __init__(self, dev, setpoint, toward):
        fs.Loop.__init__(self, dev, setpoint)
        self.toward = toward

    def settle(self):
        last = 0
        for _ in range(fs.ITERS):
            v = fs.read_junction(self.dev)
            if v is None:
                self.lost += 1
                continue
            last = v
            mag = max(abs(v), fs.FLOOR)
            if abs(v) >= fs.SAT:
                self.saturated += 1
            error_decades = math.log10(mag / self.setpoint)
            # Too much current -> move AWAY from the sample: -toward.
            delta = -self.toward * fs.GAIN * error_decades * fs.COUNTS_PER_DECADE
            delta = max(-fs.MAX_STEP, min(fs.MAX_STEP, delta))
            self.set_z(self.z + delta)
        return self.z, last


def retracted_end(toward):
    return fs.Z_MIN_SAFE - 2000 if toward > 0 else fs.Z_MAX_SAFE + 2000


def locate(dev, setpoint, toward, step=100):
    """From the retracted end toward the sample until the current reaches setpoint."""
    z = retracted_end(toward)
    end = fs.Z_MAX_SAFE if toward > 0 else fs.Z_MIN_SAFE
    while (z <= end) if toward > 0 else (z >= end):
        dev._write(("DACZ %d\n" % z).encode())
        v = fs.read_junction(dev)
        if v is not None and abs(v) >= setpoint:
            return z
        z += toward * step
    return None


def scan(dev, toward, half, step, nlines, setpoint, xheld=False, log=print):
    xs = list(range(fs.MID - half, fs.MID + half + 1, step))
    ys = [fs.MID - half + round(i * (2.0 * half) / max(nlines - 1, 1)) for i in range(nlines)]
    onset = locate(dev, setpoint, toward)
    if onset is None:
        return None, None
    loop = SLoop(dev, setpoint, toward)
    loop.set_z(onset)
    rows = []
    for yi, y in enumerate(ys):
        dev._write(("DACY %d\n" % y).encode())
        line = {}
        for name, order in (("fwd", xs), ("back", list(reversed(xs)))):
            zs = []
            for x in order:
                if not xheld:
                    dev._write(("DACX %d\n" % x).encode())
                z, _ = loop.settle()
                zs.append(z)
            if name == "back":
                zs.reverse()
            line[name] = zs
        rows.append((y, line["fwd"], line["back"]))
        if loop.saturated > 40 * (yi + 1) or loop.clamped > 40 * (yi + 1):
            log("  ABORT line %d: saturated %d, clamped %d" % (yi, loop.saturated, loop.clamped))
            break
    return rows, loop


def main(argv):
    import serial
    from stm_approach import Device, find_teensy
    toward = int(argv[0])
    half, step, nlines, setpoint = int(argv[1]), int(argv[2]), int(argv[3]), float(argv[4])
    fs.COUNTS_PER_DECADE = float(argv[5])
    reps, prefix = int(argv[6]), argv[7]
    xheld = len(argv) > 8 and argv[8] == "1"
    assert toward in (1, -1)
    port = serial.Serial(find_teensy(), 115200, timeout=0.2)
    ts = lambda: time.strftime("%H:%M:%S", time.gmtime())
    with port:
        dev = Device(port)
        try:
            dev._write(("DACZ %d\n" % retracted_end(toward)).encode())
            dev._write(("DACX %d\n" % fs.MID).encode())
            dev._write(("DACY %d\n" % fs.MID).encode())
            dev._write(("BIAS %d\n" % BIAS).encode())
            time.sleep(0.1)
            for r in range(reps):
                t0 = time.time()
                rows, loop = scan(dev, toward, half, step, nlines, setpoint, xheld)
                if rows is None:
                    print(ts(), "rep %d: no junction in reach" % r, flush=True)
                    continue
                out = "%s_%d.csv" % (prefix, r)
                with open(out, "w") as f:
                    f.write("y,dir," + ",".join(str(x) for x in range(fs.MID - half, fs.MID + half + 1, step)) + "\n")
                    for y, fwd, back in rows:
                        f.write("%d,fwd,%s\n" % (y, ",".join(str(v) for v in fwd)))
                        f.write("%d,back,%s\n" % (y, ",".join(str(v) for v in back)))
                zs = [v for _, f_, b_ in rows for v in f_ + b_]
                print(ts(), "rep %d: %d lines in %.1f s, Z %d..%d, saturated %d, clamped %d, lost %d -> %s" % (
                    r, len(rows), time.time() - t0, min(zs), max(zs), loop.saturated, loop.clamped, loop.lost, out),
                    flush=True)
                dev._write(("DACZ %d\n" % retracted_end(toward)).encode())
                time.sleep(0.2)
        finally:
            dev._write(("DACZ %d\n" % retracted_end(toward)).encode())
            dev._write(("DACX %d\n" % fs.MID).encode())
            dev._write(("DACY %d\n" % fs.MID).encode())
            dev._write(b"BIAS 32768\n")
            time.sleep(0.05)
            print(ts(), "end: Z %d (retracted for toward=%+d), X/Y mid, bias 0 V" % (retracted_end(toward), toward))


if __name__ == "__main__":
    main(sys.argv[1:])
