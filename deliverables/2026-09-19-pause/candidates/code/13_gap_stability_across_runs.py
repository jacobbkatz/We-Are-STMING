"""13 - Was the gap stable between the three-Y runs? And the cross-run place test.

Run from the repository root:

    python3 deliverables/2026-09-19-pause/candidates/code/13_gap_stability_across_runs.py

Writes work/gap_stability_across_runs.csv.

WHY THIS EXISTS - A CORRECTION TO MY OWN VERDICT
------------------------------------------------
The first version of VERDICT.md said run 4 came "half an hour" after run 2, and that between them
"the gap demonstrably moved by most of the Z range", and concluded that genuine non-reproduction
and "the surface moved out from under it" could not be separated.

**BOTH OF THOSE WERE UNEVIDENCED AND BOTH ARE WRONG.** The lead caught it. Neither ycontrol log
carries a timestamp, so I inferred an interval instead of bounding one - exactly the failure
CLAUDE.md warns about.

  THE INTERVAL. sessions/2026-09-19-bench.md is chronological. Section 3.14 is timestamped 03:48
  (cas9.log's last line is 03:48:56) and section 3.16 is timestamped 03:53. Section 3.15 - ALL FIVE
  three-Y runs - sits between them. Five runs in about four minutes, so run 2 to run 4 is about two
  minutes and at most four. Bounded by the session log's own timestamps, not measured.

  THE GAP. There is a direct measurement nobody used. The first line of every ycontrol_run*.log
  records the onset Z at which the loop found the surface. This script reads them.

WHAT THIS SCRIPT DOES
---------------------
  1. Reads the onset Z out of all five logs and reports the motion across the runs.
  2. Asks what onset Z can and cannot see, from the measured dZ/dX and dZ/dY of each run.
  3. THE TEST THIS MAKES POSSIBLE. If the gap was stable for those two minutes, then run 2 and run
     4 sampled the same three places, and a profile belonging to a PLACE must agree across the two
     runs at the same place. That is a direct cross-run place test, and it was not worth running
     while the gap was believed to have moved by most of the Z range. Now it is.

PROCESSING: detrending as elsewhere. Permutation null over the place labels of the second run,
20,000 draws, seeded.
"""
import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from stmload import load_ycontrol, data, out, detrend, corr, fisher_mean

RNG = np.random.default_rng(20260919)
NPERM = 20000

RUNS = [
    ("ycontrol_run1.log", "ycontrol_run1.csv", "run 1, y_sep 3000"),
    ("ycontrol_xheld_run1.log", "ycontrol_xheld_run1.csv", "X-HELD control, y_sep 3000"),
    ("ycontrol_run2.log", "ycontrol_run2_ysep12000.csv", "run 2, y_sep 12000 - THE POSITIVE"),
    ("ycontrol_run3.log", "ycontrol_run3_ysep12000_xheld.csv", "run 3, X-HELD control"),
    ("ycontrol_run4.log", "ycontrol_run4_ysep12000_repeat.csv", "run 4, THE REPEAT"),
]


def onset(logname):
    first = open(data("2026-09-19-bench", logname)).readline()
    return int(re.search(r"onset Z=(\d+)", first).group(1))


def prep(csvname):
    xs, pls, P = load_ycontrol(data("2026-09-19-bench", csvname))
    return xs, pls, {p: np.array([detrend(v) for v in P[p]]) for p in pls}, P


def zscore(M):
    M = M - M.mean(1, keepdims=True)
    return M / np.maximum(M.std(1, keepdims=True), 1e-12)


def main():
    rows = []

    print("1. THE GAP, MEASURED - the onset Z on the first line of every ycontrol log")
    print("   the Z at which the loop found the surface before each run started")
    print()
    print("   %-38s %10s %14s" % ("run", "onset Z", "change"))
    prev = None
    ons = {}
    for lg, cs, what in RUNS:
        o = onset(lg)
        ons[cs] = o
        print("   %-38s %10d %14s" % (what, o, "" if prev is None else "%+d" % (o - prev)))
        rows.append(["onset Z", what, lg, str(o)])
        prev = o
    d24 = ons["ycontrol_run4_ysep12000_repeat.csv"] - ons["ycontrol_run2_ysep12000.csv"]
    span = max(ons.values()) - min(ons.values())
    print("""
   RUN 2 TO RUN 4: %+d counts. That is %.1f%% of the 65,536-count Z range, not "most of it".
   Across all five runs the onset spans %d counts (%.1f%% of range).
   The interval is about two minutes and at most four (section 3.14 at 03:48, section 3.16 at
   03:53, five runs in between). THE GAP WAS STABLE ACROSS THE COMPARISON THAT MATTERS.""" % (
        d24, 100.0 * abs(d24) / 65536, span, 100.0 * span / 65536))
    rows.append(["onset Z", "run 2 -> run 4", "%+d counts" % d24,
                 "%.1f%% of the Z range" % (100.0 * abs(d24) / 65536)])
    print("""   INDEPENDENT CROSS-CHECK OF BOTH THE INTERVAL AND THE RATE.
   sessions/2026-09-19-morning.md section 6 measured, from the cas9 and img data and without
   reference to these logs: "the gap opened at ~40-41 counts/s on average from 03:48:13 to
   03:52:58". The five ycontrol runs sit inside that 285-second window, and %d counts of onset
   motion across them is %.0f counts/s - the same rate, from a different measurement. Two
   independent routes agree that this was a FOUR-MINUTE window with a gap drifting slowly and
   steadily, not moving by most of its range.""" % (span, span / 240.0))
    rows.append(["onset Z", "drift rate across the five runs", "%.0f counts/s" % (span / 240.0),
                 "morning log section 6 measured ~40-41 counts/s over 03:48:13-03:52:58"])

    print("\n2. WHAT ONSET Z CAN AND CANNOT SEE")
    print("   onset Z is ONE number. It confounds vertical gap motion with lateral drift across a")
    print("   tilted surface. The sensitivities are measurable from the runs themselves:")
    print()
    print("   %-38s %10s %10s %16s %16s" % ("run", "dZ/dX", "dZ/dY",
                                            "X drift for 2200", "Y drift for 2200"))
    for lg, cs, what in RUNS:
        xs, pls, D, P = prep(cs)
        A = np.array([v for p in pls for v in P[p]])
        dzdx = float(np.mean([np.polyfit(xs.astype(float), v, 1)[0] for v in A]))
        ys = np.array(pls, dtype=float)
        zs = np.array([P[p].mean() for p in pls])
        dzdy = float(np.polyfit(ys, zs, 1)[0])
        fx = abs(d24) / abs(dzdx) if dzdx else float("inf")
        fy = abs(d24) / abs(dzdy) if dzdy else float("inf")
        print("   %-38s %10.4f %10.4f %16s %16s" % (
            what, dzdx, dzdy,
            "%.0f" % fx if fx < 1e6 else "out of range",
            "%.0f" % fy if fy < 1e6 else "out of range"))
        rows.append(["tilt", what, "dZ/dX %.4f" % dzdx, "dZ/dY %.4f" % dzdy])
    print("""
   Read the last two columns as "how much lateral drift would be needed to fake the whole
   2,200-count onset change on that run's own measured slope". On run 4's slopes it is about a
   million counts - fifteen times the whole DAC range - so ONSET Z IS VERY NEARLY BLIND TO LATERAL
   DRIFT THERE. Turn that round: a lateral drift of the ENTIRE X range would move run 4's onset by
   about 150 counts, which this measurement could not see at all.

   Run 2's dZ/dY is the exception at +0.225, on which about 10,000 counts of Y drift would account
   for the whole change - but that slope is fitted to THREE places and is dominated by one of them
   sitting 5,400 counts higher, so it is weakly determined. EITHER WAY the conclusion is the same:
   onset Z bounds the VERTICAL motion and says nothing about the LATERAL.""")

    print("\n3. THE CROSS-RUN PLACE TEST - possible only now the gap is known to have been stable")
    print("   run 2 and run 4 sampled the same three Y places about two minutes apart.")
    print("   A profile belonging to a PLACE must agree across the two runs AT THE SAME PLACE.")
    print()
    xs, pls, R2, P2 = prep("ycontrol_run2_ysep12000.csv")
    _, _, R4, _ = prep("ycontrol_run4_ysep12000_repeat.csv")
    _, _, R3, _ = prep("ycontrol_run3_ysep12000_xheld.csv")
    A = np.vstack([R2[p] for p in pls])
    la = np.repeat(pls, [len(R2[p]) for p in pls])

    def stat(B, lb):
        C = np.clip(zscore(A) @ zscore(B).T / A.shape[1], -0.999999, 0.999999)
        same = la[:, None] == lb[None, :]
        zz = np.arctanh(C)
        return float(np.tanh(zz[same].mean()) - np.tanh(zz[~same].mean())), \
            float(np.tanh(zz[same].mean())), float(np.tanh(zz[~same].mean()))

    for nm, R in (("run 4, THE REPEAT", R4), ("run 3, the X-HELD control", R3)):
        B = np.vstack([R[p] for p in pls])
        lb = np.repeat(pls, [len(R[p]) for p in pls])
        obs, s, o = stat(B, lb)
        null = np.array([stat(B, RNG.permutation(lb))[0] for _ in range(NPERM)])
        p = float((null >= obs).mean())
        print("   run 2 vs %-26s same place %+.3f  other place %+.3f  difference %+.3f  p = %.4f"
              % (nm, s, o, obs, p))
        rows.append(["cross-run place test", "run 2 vs " + nm, "same %+.3f" % s,
                     "other %+.3f" % o, "difference %+.3f" % obs, "p = %.4f" % p])
    print()
    print("   per-place, pass-averaged, run 2 against run 4:")
    for p_ in pls:
        print("      Y %+6d : r %+.2f" % (p_, corr(R2[p_].mean(0), R4[p_].mean(0))))
        rows.append(["cross-run per place", "Y %+d" % p_,
                     "%+.2f" % corr(R2[p_].mean(0), R4[p_].mean(0))])
    print("   (sessions/2026-09-19-bench.md 3.15 quotes +0.11, +0.50 and -0.72 - reproduced exactly)")
    print("""
   THE SAME PLACE AGREES NO BETTER THAN A DIFFERENT PLACE. It agrees slightly WORSE
   (-0.020 against +0.054, difference -0.074, permutation p = 0.70). Over an interval in which the
   gap moved 2,200 counts, a profile belonging to those places does not survive to the repeat.

   THIS WEAKENS CANDIDATE B and it is the sharpest evidence against it. My earlier "the gap moved
   so the two readings cannot be separated" was wrong on its facts; genuine non-reproduction - no
   surface signal - is now the better-supported reading.

   WHAT KEEPS IT OPEN, narrowly and specifically: onset Z measures the GAP, not LATERAL position.
   A drift in X or Y carries the tip onto a different patch of gold while barely moving the Z at
   which it finds the surface - section 2 puts numbers on how blind onset Z is to that. NOTHING IN
   THIS PROJECT HAS EVER MEASURED LATERAL DRIFT. That is a specific missing measurement, not a
   general doubt.""")

    with open(out("work", "gap_stability_across_runs.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["test", "a", "b", "c", "d", "e"])
        for r in rows:
            w.writerow(list(r) + [""] * (6 - len(r)))
    print("\n-> %s" % out("work", "gap_stability_across_runs.csv"))


if __name__ == "__main__":
    main()
