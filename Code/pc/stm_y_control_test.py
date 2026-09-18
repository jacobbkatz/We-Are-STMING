#!/usr/bin/env python3
"""Tests for stm_y_control.py.

The tool's whole job is to answer one question correctly -- is a reproducible
profile the sample or the scanner -- and on 2026-09-17 that question was
answered WRONGLY by a control whose statistics were unfair. So the tests here
are mostly about the statistics, not the serial protocol.

Three synthetic worlds with a known truth:

    topography   each place carries its own shape  -> must say SURFACE
    bow          every place carries the SAME shape -> must not say SURFACE
    noise        no shape at all                    -> must say there is
                                                       nothing to test

And two faults injected on purpose, each of which must make the tool give the
WRONG answer -- which is what proves the honest version is doing the work
rather than getting lucky:

    fair=False           the 2026-09-17 bug: all-pass averages between places
                         against single passes within one. On a world that
                         really does carry topography, it loses it.
    detrend_passes=False leaving the tip-sample tilt in every pass. On a world
                         with NO profile at all, the bare tilt is worth about
                         1,400 counts RMS over +-15,000 -- five times the
                         wobble floor -- so the tool reports on noise.
                         A shared tilt inflates within and between equally, so
                         it fakes a SIGNAL rather than reversing a real one;
                         the first version of that check asserted the wrong
                         failure and passed while the fault was present.

Finally the analyser is run against the real committed file from that night and
must reproduce the figures the wrap corrected to.

Run: py stm_y_control_test.py
"""
import sys
import os
import math
import random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import stm_y_control as yc

N_X = 21
HALF = 15000
PLACES = (-3000, 0, 3000)


def shape(seed, n=N_X):
    """A smooth, arbitrary profile -- three sine components, fixed by seed."""
    rng = random.Random(seed)
    ph = [rng.uniform(0, 2 * math.pi) for _ in range(3)]
    amp = [1.0, 0.55, 0.3]
    out = []
    for i in range(n):
        t = i / float(n - 1)
        v = sum(a * math.sin(2 * math.pi * k * t + p)
                for k, (a, p) in enumerate(zip(amp, ph), start=1))
        out.append(v)
    m = sum(out) / len(out)
    out = [v - m for v in out]
    s = math.sqrt(sum(v * v for v in out) / len(out))
    return [v / s for v in out]          # unit RMS


def world(kind, n_passes=10, topo=500.0, bow=700.0, noise=1200.0,
          tilt=0.0, seed=7):
    """Build {y_offset: [pass, ...]} for a world with a known truth.

    topo   amplitude of the shape that belongs to the PLACE
    bow    amplitude of the shape shared by every place (the scanner)
    noise  per-point, per-pass noise
    tilt   Z counts per X count, the instrumental tilt, shared by all
    """
    rng = random.Random(seed)
    shared = shape(1)
    places = {}
    for pi, y in enumerate(PLACES):
        own = shape(100 + pi)
        passes = []
        for _ in range(n_passes):
            row = []
            for i in range(N_X):
                x = -HALF + i * (2.0 * HALF / (N_X - 1))
                v = 38000.0
                if kind in ("topography",):
                    v += topo * own[i]
                if kind in ("topography", "bow"):
                    v += bow * shared[i]
                v += tilt * x
                v += rng.gauss(0, noise)
                row.append(v)
            passes.append(row)
        places[y] = passes
    return places


def check(name, got, want, fails):
    ok = got == want
    print("  %-46s %-32s %s" % (name, got, "OK" if ok else "WRONG, wanted " + want))
    if not ok:
        fails.append(name)
    return ok


def main():
    fails = []

    print("THE THREE WORLDS, analysed honestly")
    for kind, want in (("topography", "THE PROFILE IS THE SURFACE"),
                       ("bow", None),
                       ("noise", "NO PROFILE TO TEST")):
        w = world(kind, topo=(0.0 if kind != "topography" else 500.0),
                  bow=(0.0 if kind == "noise" else 700.0),
                  noise=(700.0 if kind == "noise" else 1200.0))
        r = yc.analyse(w)
        v = yc.report(r)
        if want is None:
            # The bow world must NOT be called topography. Either verdict the
            # tool can reach for a shared shape is acceptable.
            ok = v != "THE PROFILE IS THE SURFACE"
            print("  %-46s %-32s %s"
                  % ("bow world is not called topography", v,
                     "OK" if ok else "WRONG"))
            if not ok:
                fails.append("bow world called topography")
        else:
            check(kind + " world", v, want, fails)

    print("")
    print("INJECTED FAULT 1 -- the 2026-09-17 bug, unfair averaging")
    w = world("topography")
    honest = yc.report(yc.analyse(w, fair=True))
    broken = yc.report(yc.analyse(w, fair=False))
    print("  honest: %s" % honest)
    print("  broken: %s" % broken)
    if honest != "THE PROFILE IS THE SURFACE":
        fails.append("honest statistic failed on the topography world")
    if broken == "THE PROFILE IS THE SURFACE":
        fails.append("the unfair statistic did NOT go wrong -- "
                     "this test cannot detect the bug it exists for")

    print("")
    print("INJECTED FAULT 2 -- tilt left in, no detrending")
    # A world with NO profile at all, plus the real -0.17 counts-of-Z-per-
    # count-of-X tilt. Detrended, the tool must say there is nothing to test.
    # Undetrended, the tilt IS the profile: it is worth 1,400 counts RMS over
    # +-15,000, five times the wobble floor, so the gate waves it through and
    # the tool reports on noise.
    #
    # NOTE, because the first version of this check was wrong and passed while
    # the fault was present: a tilt shared by every place inflates within AND
    # between by the same amount, so it does NOT reverse a true positive. It
    # fakes a SIGNAL where there is none. That is the failure to test for.
    w = world("noise", topo=0.0, bow=0.0, noise=700.0, tilt=-0.17)
    honest = yc.report(yc.analyse(w, detrend_passes=True))
    broken = yc.report(yc.analyse(w, detrend_passes=False))
    print("  detrended:     %s" % honest)
    print("  not detrended: %s" % broken)
    if honest != "NO PROFILE TO TEST":
        fails.append("detrended analysis did not see through a bare tilt")
    if broken == "NO PROFILE TO TEST":
        fails.append("the undetrended analysis did NOT go wrong -- "
                     "the detrend step is not being tested")

    print("")
    print("THE REAL FILE FROM 2026-09-17")
    real = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "..", "sessions", "data", "2026-09-17-bench",
                        "line_three_y_positions.csv")
    real = os.path.normpath(real)
    if not os.path.exists(real):
        print("  SKIPPED -- %s not found" % real)
    else:
        _, r = yc.analyse_file(real)
        # The wrap's corrected figures, reproduced independently 2026-09-18.
        for label, got, want in (("within a place", r["within_single"], 0.133),
                                 ("between places", r["between_single"], 0.146)):
            ok = abs(got - want) < 0.005
            print("  %-46s %+0.3f (wrap says %+0.3f)   %s"
                  % (label, got, want, "OK" if ok else "MISMATCH"))
            if not ok:
                fails.append("does not reproduce the wrap's %s figure" % label)

    print("")
    print("THE BENCH HALF STAYS INSIDE THE SAFE Z WINDOW")
    try:
        import stm_feedback_scan as fs
        import stm_feedback_scan_test as fst

        dev = fst.FakeScope(lambda x: 80000)      # surface out of reach
        loop = fs.Loop(dev, fst.SETPOINT)
        loop.set_z(30000)
        xs = list(range(fs.MID - HALF, fs.MID + HALF + 1,
                        2 * HALF // (N_X - 1)))
        yc.reacquire(fs, loop, dev, xs[0], fst.SETPOINT)
        yc.sweep(fs, loop, dev, xs)
        lo, hi = min(dev.zs_seen), max(dev.zs_seen)
        print("  unreachable surface: Z stayed within %d..%d, clamped %d times"
              % (lo, hi, loop.clamped))
        # fs.locate() sweeps from Z_LOCATE_START (10000) with a direct DACZ,
        # below the Loop's own 12000 floor. That is the RETRACTED end, away
        # from the sample, and inside the 10000-50000 window docs/FACTS.md
        # gives for the summing stage. The floor that matters for the tip is
        # the HIGH end.
        if lo < fs.Z_LOCATE_START or hi > fs.Z_MAX_SAFE:
            fails.append("left the safe Z window")
        if loop.clamped == 0:
            fails.append("did not notice it was clamped")

        dev = fst.FakeScope(lambda x: 12000)      # hard contact
        loop = fs.Loop(dev, fst.SETPOINT)
        loop.set_z(30000)
        yc.reacquire(fs, loop, dev, xs[0], fst.SETPOINT)
        zs = yc.sweep(fs, loop, dev, xs)
        print("  hard contact:        retreated to Z=%d" % zs[-1])
        if zs[-1] > 30000:
            fails.append("did not retreat from saturation")
    except ImportError as exc:
        print("  SKIPPED -- %s" % exc)

    print("")
    print("FAILURES: %s" % (fails if fails else "none"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
