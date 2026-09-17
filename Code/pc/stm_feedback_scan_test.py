#!/usr/bin/env python3
"""Tests for stm_feedback_scan.py, against a simulated junction.

A control loop that has never been run is exactly the thing that drives a tip
into a sample, so every behaviour below was checked before the loop was pointed
at the instrument on 2026-09-17.

Each test was also shown to FAIL against a deliberately broken loop: the last
test reverses the sign of the gain and requires that the loop runs into a
clamp. The first version of that check only looked at the high clamp and passed
while the fault was present -- a reversed loop runs to the LOW clamp.

Run: py stm_feedback_scan_test.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import stm_feedback_scan as fs

SETPOINT = 3000.0


class FakeScope:
    """Current rises tenfold per COUNTS_PER_DECADE of Z above the surface."""

    def __init__(self, surface):
        self.surface = surface          # x -> the Z that gives SETPOINT
        self.z = 30000
        self.x = fs.MID
        self.zs_seen = []
        self._port = None

    def _write(self, frame):
        s = frame.decode().strip()
        if s.startswith("DACZ"):
            self.z = int(s.split()[1])
            self.zs_seen.append(self.z)
        elif s.startswith("DACX"):
            self.x = int(s.split()[1])

    def read_adc(self, timeout=None):
        decades = (self.z - self.surface(self.x)) / fs.COUNTS_PER_DECADE
        return int(max(-32768, min(32767, SETPOINT * (10 ** decades))))


def run(surface, xs, iters=6, start_offset=0):
    dev = FakeScope(surface)
    loop = fs.Loop(dev, SETPOINT)
    loop.set_z(surface(xs[0]) + start_offset)
    out = []
    for x in xs:
        dev._write(("DACX %d\n" % x).encode())
        for _ in range(max(1, iters // fs.ITERS)):
            z, _ = loop.settle()
        out.append(z)
    return loop, dev, out


def main():
    xs = list(range(fs.MID - 400, fs.MID + 401, 40))
    fails = []

    flat = lambda x: 30000
    loop, dev, zs = run(flat, xs, start_offset=-300)
    err = max(abs(z - 30000) for z in zs)
    print("holds a flat surface: max error %d counts" % err)
    if err > 60:
        fails.append("does not hold a flat surface")

    bump = lambda x: 30000 + (600 if abs(x - fs.MID) < 120 else 0)
    loop, dev, zs = run(bump, xs)
    on = [z for x, z in zip(xs, zs) if abs(x - fs.MID) < 120]
    off = [z for x, z in zip(xs, zs) if abs(x - fs.MID) >= 200]
    got = sum(on) / len(on) - sum(off) / len(off)
    print("follows a 600-count bump: measured %.0f" % got)
    if not 400 < got < 800:
        fails.append("does not follow a 600-count bump")

    far = lambda x: 80000
    loop, dev, zs = run(far, xs, iters=30)
    print("surface out of reach: clamped %d times, Z stayed within %d..%d"
          % (loop.clamped, min(dev.zs_seen), max(dev.zs_seen)))
    if max(dev.zs_seen) > fs.Z_MAX_SAFE or min(dev.zs_seen) < fs.Z_MIN_SAFE:
        fails.append("left the safe Z window")
    if loop.clamped == 0:
        fails.append("did not notice it was clamped")

    hot = lambda x: 12000
    loop, dev, zs = run(hot, xs, iters=12)
    print("hard contact: retreated to Z=%d" % zs[-1])
    if zs[-1] > 30000:
        fails.append("did not retreat from saturation")

    good = fs.GAIN
    fs.GAIN = -good
    loop, dev, zs = run(flat, xs, iters=12, start_offset=-300)
    ran_away = (max(dev.zs_seen) >= fs.Z_MAX_SAFE
                or min(dev.zs_seen) <= fs.Z_MIN_SAFE)
    fs.GAIN = good
    print("injected fault, sign reversed: ran into a clamp = %s" % ran_away)
    if not ran_away:
        fails.append("the sign-reversal test did not fail as it should")

    print("")
    print("FAILURES: %s" % (fails if fails else "none"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
