#!/usr/bin/env python3
"""
Sample the STM's ADC over time and report statistics.

Reads field 5 of GSTS, which is stm_status.adc, set by update() from
read_adc_raw() every pass of loop(). That is a RAW single conversion.

Do not use ADCR for this. ADCR calls read_adc(), which returns a 5-sample
rolling average, and averaging hides exactly the isolated bit-flips that a
marginal SPI link produces.

Unlike stm_console.py's one-shot mode this holds the port open for the whole
run, so the sample interval is real rather than dominated by port setup.
Release it before uploading firmware.

Usage:
    python adc_stats.py                 # 50 samples as fast as practical
    python adc_stats.py -n 60 -i 2.0    # 60 samples, 2 s apart, for settling
    python adc_stats.py -n 50 --tag 40MHz
"""

import argparse
import sys
import time

import serial
from serial.tools import list_ports


def find_teensy():
    """PJRC vendor ID is 0x16C0."""
    for p in list_ports.comports():
        if p.vid == 0x16C0:
            return p.device
    ports = list_ports.comports()
    return ports[0].device if len(ports) == 1 else None


def read_status(port, timeout=3.0):
    port.reset_input_buffer()
    port.write(b"GSTS")
    port.flush()
    deadline = time.time() + timeout
    buf = b""
    while time.time() < deadline:
        chunk = port.read(256)
        if chunk:
            buf += chunk
            if buf.endswith(b"\n"):
                break
        elif buf:
            break
    return buf.decode("ascii", "replace").strip()


def parse_adc(line):
    parts = line.split(",")
    if len(parts) != 10:
        return None, None
    try:
        return int(parts[4]), int(parts[9])
    except ValueError:
        return None, None


def stats(vals):
    n = len(vals)
    mean = sum(vals) / n
    var = sum((v - mean) ** 2 for v in vals) / (n - 1) if n > 1 else 0.0
    return mean, var ** 0.5, min(vals), max(vals)


def main():
    ap = argparse.ArgumentParser(description="Sample the STM ADC and report statistics")
    ap.add_argument("-n", "--samples", type=int, default=50)
    ap.add_argument("-i", "--interval", type=float, default=0.0,
                    help="seconds between samples (default: as fast as practical)")
    ap.add_argument("-p", "--port")
    ap.add_argument("--tag", default="", help="label for this run, printed in the summary")
    ap.add_argument("-q", "--quiet", action="store_true", help="summary only")
    opts = ap.parse_args()

    portname = opts.port or find_teensy()
    if not portname:
        print("No Teensy found. Ports seen:")
        for p in list_ports.comports():
            print("  %s  %s" % (p.device, p.description))
        return 1

    try:
        port = serial.Serial(portname, 115200, timeout=0.2)
    except serial.SerialException as e:
        print("Could not open %s: %s" % (portname, e))
        print("Something else has the port open.")
        return 1

    vals, bad = [], 0
    with port:
        time.sleep(1.0)
        t0 = time.time()
        if not opts.quiet:
            print("  %8s  %10s  %12s" % ("t (s)", "adc", "uptime (s)"))
        for i in range(opts.samples):
            adc, ms = parse_adc(read_status(port))
            if adc is None:
                bad += 1
            else:
                vals.append(adc)
                if not opts.quiet:
                    print("  %8.1f  %10d  %12.1f" % (time.time() - t0, adc, ms / 1000.0))
            if opts.interval and i + 1 < opts.samples:
                time.sleep(opts.interval)
        span = time.time() - t0

    if not vals:
        print("No valid samples. Is the firmware running?")
        return 1

    mean, sd, lo, hi = stats(vals)
    print("")
    print("  run%s: %d samples over %.1f s%s" %
          (" [" + opts.tag + "]" if opts.tag else "", len(vals), span,
           ", %d malformed" % bad if bad else ""))
    print("  mean   %12.1f counts" % mean)
    print("  stdev  %12.1f counts" % sd)
    print("  min    %12d" % lo)
    print("  max    %12d" % hi)
    print("  range  %12d" % (hi - lo))
    if lo == hi:
        print("")
        print("  Every sample identical. Either the input is railed and the ADC is")
        print("  clipping, which removes the noise too, or the read path is stuck.")
        print("  A railed analog input and a digital fault look the same here.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
