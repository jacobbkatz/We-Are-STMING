#!/usr/bin/env python3
"""Tests for stm_noise_spectrum.py.

The tool's job is one verdict: did the SUSPENSION cause a noise change, or did
something else? A wrong verdict here sends a bench session chasing the wrong
thing, so the tests build worlds where the truth is known and check the tool
says it.

    suspension worked   low bands fall, high bands do not  -> credit the suspension
    gain changed        EVERYTHING falls together          -> do NOT credit it
    platform fouling    low bands rise                     -> check it hangs free

The middle one is the one that matters. A tool that just says "quieter, well
done" would pass a gain change as a success and the coins would get credit
for a loose connection.

Run: py stm_noise_spectrum_test.py
"""
import io
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stm_noise_spectrum as ns

RATE = 3510.0          # reads/s; 4 s gives n ~ 14040, matching the bench run

# The synthetic world is CALIBRATED to reproduce the 2026-09-18 run, so that a
# multiplier of 1.0 really does mean "unchanged". Without that the tests are
# checking the harness, not the tool -- which is how the first version of this
# file failed two of its four cases for no reason.
#
#   white sd 344 over n=14041  ->  line floor sd*sqrt(pi/n) = 5.15 counts,
#                                  and the bench measured 400-1600 Hz at 5.0.
#   the low bands then need mechanical content that reproduces 09-18's 7.4
#   counts once the floor is taken out in quadrature. The analytic value, 7.7,
#   gave 4.8 -- the per-line amplitude and the band MEAN are not the same thing
#   once each line is a vector sum of signal and noise. CALIBRATED NUMERICALLY
#   INSTEAD: 10.0 lands it on 7.5 against the target 7.4.
#
#   An uncalibrated harness tests itself rather than the tool. The first
#   version of this file failed two of four cases for exactly that reason and
#   the numbers, not the code, were what was wrong.
SD_WHITE = 344.0
LOW_EXCESS = 10.0       # counts of broadband mechanical content per line, 2-30 Hz
HIGH_EXCESS = 0.0      # there is none up there, which is why it is the control


def synth(secs=4.0, low=1.0, high=1.0, sd=SD_WHITE, seed=3):
    """Samples reproducing 2026-09-18 when low=high=1.0 and sd is unchanged.

    `low` scales the 2-30 Hz mechanical excess -- the only thing a suspension
    can touch. `high` scales 400-1600 Hz content, which should be nothing.
    `sd` scales the broadband white floor, which sits under every band.
    """
    rng = random.Random(seed)
    n = int(secs * RATE)
    ts = [i / RATE + rng.gauss(0, 0.00002) for i in range(n)]
    # broadband low-frequency content: every integer Hz in 2-30, random phase,
    # so the BAND MEAN responds linearly to `low` instead of a few tones
    lof = [(f, rng.uniform(0, 2 * math.pi)) for f in range(2, 31)]
    hif = [(f, rng.uniform(0, 2 * math.pi)) for f in range(400, 1600, 50)]
    al = low * LOW_EXCESS * math.sqrt(n) / 2.0 * (2.0 / math.sqrt(n))
    vs = []
    for t in ts:
        v = rng.gauss(0, sd)
        for f, ph in lof:
            v += low * LOW_EXCESS * math.sin(2 * math.pi * f * t + ph)
        for f, ph in hif:
            v += high * HIGH_EXCESS * math.sin(2 * math.pi * f * t + ph)
        v += 87.0 * math.sin(2 * math.pi * 60 * t)
        vs.append(v)
    return ts, vs


def verdict(ts, vs):
    buf, old = io.StringIO(), sys.stdout
    sys.stdout = buf
    try:
        ns.report(ts, vs, ns.spectrum(ts, vs))
    finally:
        sys.stdout = old
    return buf.getvalue()


def main():
    fails = []
    cases = [
        ("suspension worked   (low x0.2, floor unchanged)",
         dict(low=0.2), "THE LOW-FREQUENCY CONTENT FELL"),
        ("floor fell 7x -> must REFUSE a cross-night verdict",
         dict(sd=47.0), "THIS COMPARISON IS NOT RELIABLE"),
        ("platform fouling    (low x3)",
         dict(low=3.0), "LOW-FREQUENCY CONTENT ROSE"),
        ("nothing changed at all",
         dict(), "NO CHANGE in the low-frequency"),
    ]
    for name, kw, want in cases:
        out = verdict(*synth(**kw))
        ok = want in out
        print("  %-56s %s" % (name, "OK" if ok else "WRONG"))
        if not ok:
            fails.append(name)
            for line in out.splitlines():
                if "=>" in line or "stands" in line or "control reads" in line:
                    print("      " + line.strip())

    print("")
    print("THE TRAP THE TOOL EXISTS TO AVOID, shown catching it")
    # A run at the 2026-09-17 floor (sd 47) with the SAME mechanical content.
    # Raw band means all collapse by 7x. A tool comparing raw means would call
    # that a triumph for the coins. Dividing by the floor shows nothing moved.
    ts, vs = synth(sd=47.0)
    out = verdict(ts, vs)
    raw_fell = "BETTER than that" in out
    refuses = "THIS COMPARISON IS NOT RELIABLE" in out
    blames_suspension = "LOW-FREQUENCY CONTENT ROSE" in out or "CONTENT FELL" in out
    print("    the raw floor really did fall 7x:                   %s" % raw_fell)
    print("    the tool REFUSES a cross-night verdict:             %s" % refuses)
    print("    and does NOT blame or credit the suspension:        %s" % (not blames_suspension))
    if not refuses:
        fails.append("does not refuse an unreliable cross-night comparison")
    if blames_suspension:
        fails.append("gives a suspension verdict it cannot support")

    print("")
    print("THE WITHIN-NIGHT COMPARISON -- same estimator both sides, no reconstruction")
    import csv as _csv, tempfile
    d = tempfile.mkdtemp()
    paths = {}
    for name, kw in (("still", dict(low=1.0)), ("stamp", dict(low=3.0, seed=11))):
        ts_, vs_ = synth(**kw)
        paths[name] = os.path.join(d, name + ".csv")
        with open(paths[name], "w", newline="") as fh:
            w = _csv.writer(fh); w.writerow(["t_s", "adcr"]); w.writerows(zip(ts_, vs_))
    buf, old = io.StringIO(), sys.stdout
    sys.stdout = buf
    try:
        ns.compare(paths["still"], paths["stamp"])
    finally:
        sys.stdout = old
    out = buf.getvalue()
    saw_more = "MORE" in out and "the building IS getting in" in out
    print("    stamping put 3x more into 2-30 Hz and it says so: %s" % saw_more)
    if not saw_more:
        fails.append("the within-night comparison missed a 3x low-band rise")
        print(out)
    for pth in paths.values():
        os.remove(pth)
    os.rmdir(d)

    print("")
    print("ROUND TRIP THROUGH CSV")
    import csv as _csv
    ts, vs = synth(low=0.25)
    tmp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_nstest.csv")
    with open(tmp, "w", newline="") as fh:
        w = _csv.writer(fh); w.writerow(["t_s", "adcr"]); w.writerows(zip(ts, vs))
    ts2, vs2 = [], []
    with open(tmp) as fh:
        for row in _csv.DictReader(fh):
            ts2.append(float(row["t_s"])); vs2.append(float(row["adcr"]))
    os.remove(tmp)
    same = verdict(ts, vs) == verdict(ts2, vs2)
    print("    re-analysing the CSV gives the identical verdict: %s" % same)
    if not same:
        fails.append("CSV round trip changes the answer")

    print("")
    print("FAILURES: %s" % (fails if fails else "none"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
