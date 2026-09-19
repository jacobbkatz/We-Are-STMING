"""04 - The place test for the 2026-09-17 +-15,000 profile, from data already on disk.

Run from the repository root:

    python3 deliverables/2026-09-19-pause/candidates/code/04_0917_wide_place_test.py

Writes work/0917_wide_place_test.csv.

WHY THIS EXISTS
---------------
sessions/2026-09-17-bench.md section 3.25 closes with:

    "The experiment that would settle it - the same line at three separated Y
     positions AT +-15,000 - has NOT been run. That test is the first thing to
     do next session, and it takes ten minutes."

It was run on 2026-09-19 (script 03). But a version of it was ALREADY IN THE
2026-09-17 FILES and nobody has used it. sessions/data/2026-09-17-bench/
scan_wide_25nm_1.csv and _2.csv are two complete 2D images of the SAME nine Y
positions (17768 to 47768, 3750 apart) over the SAME X grid (17768 to 47768,
1500 apart) as line_repeated_wide.csv. Two images of nine places is a
within-place / between-place test with 9 same-place pairs and 72
different-place pairs, taken the same night, with the same tip and the same
sample, at the width the result is claimed at.

  same place   line at Y_k in image 1  vs  line at Y_k in image 2
  other place  line at Y_j in image 1  vs  line at Y_k in image 2, j != k

If the corrugation belongs to the surface, same-place pairs beat other-place
pairs. If it is one fixed shape the scanner draws wherever it points, or a
function of pixel index alone, they are equal.

Also here:
  - Does the 12-pass line repeat's agreement decay with pass separation?
    A fixed shape gives a flat curve; a slow drift gives a decaying one.
  - How much of the 636-count profile is a simple bow? Fit polynomials.
  - Does the 12-pass profile match the two 2D images' lines at the same width?

PROCESSING: every pass detrended (least-squares straight line in X) and nothing
else. No smoothing, no alignment, no rejection.
"""
import csv
import itertools
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from stmload import load_raster, load_ycontrol, data, out, detrend, corr, rms, fisher_mean


def main():
    rows = []

    # ------------------------------------------------- the two wide 2D images
    xs1, ys1, F1, B1 = load_raster(data("2026-09-17-bench", "scan_wide_25nm_1.csv"))
    xs2, ys2, F2, B2 = load_raster(data("2026-09-17-bench", "scan_wide_25nm_2.csv"))
    assert list(xs1) == list(xs2) and ys1 == ys2, "grids differ"
    print("THE 2026-09-17 PLACE TEST AT +-15,000, from scan_wide_25nm_1/2.csv")
    print("  X grid %d..%d (%d points), Y places %s" % (xs1[0], xs1[-1], len(xs1), ys1))
    D1 = np.array([detrend(f) for f in F1])
    D2 = np.array([detrend(f) for f in F2])
    print("  detrended forward-line RMS: image 1 %.0f counts, image 2 %.0f counts"
          % (np.mean([rms(d) for d in D1]), np.mean([rms(d) for d in D2])))

    same = [corr(D1[k], D2[k]) for k in range(len(ys1))]
    other = [corr(D1[j], D2[k]) for j in range(len(ys1)) for k in range(len(ys1)) if j != k]
    ms, ss, ns = fisher_mean(same)
    mo, so, no = fisher_mean(other)
    d = ms - mo
    sed = (ss ** 2 + so ** 2) ** 0.5
    print("  SAME place  (image1 Yk vs image2 Yk)  r = %+.3f +- %.3f   n = %d" % (ms, ss, ns))
    print("  OTHER place (image1 Yj vs image2 Yk)  r = %+.3f +- %.3f   n = %d" % (mo, so, no))
    print("  difference  %+.3f +- %.3f  =  %+.1f sigma" % (d, sed, d / sed))
    print("  a surface needs SAME to beat OTHER. %s" % (
        "It does not." if d / sed < 2 else "It does, at %.1f sigma." % (d / sed)))
    rows.append(["scan_wide_25nm_1/2", "place test, forward passes",
                 "%+.3f+-%.3f" % (ms, ss), "%+.3f+-%.3f" % (mo, so), "%+.2f" % (d / sed)])

    # the same test on the BACKWARD passes, an independent half of the same data
    E1 = np.array([detrend(b) for b in B1])
    E2 = np.array([detrend(b) for b in B2])
    same_b = [corr(E1[k], E2[k]) for k in range(len(ys1))]
    other_b = [corr(E1[j], E2[k]) for j in range(len(ys1)) for k in range(len(ys1)) if j != k]
    msb, ssb, _ = fisher_mean(same_b)
    mob, sob, _ = fisher_mean(other_b)
    db = msb - mob
    sedb = (ssb ** 2 + sob ** 2) ** 0.5
    print("  the same on the BACKWARD passes: same %+.3f, other %+.3f, %+.1f sigma"
          % (msb, mob, db / sedb))
    rows.append(["scan_wide_25nm_1/2", "place test, backward passes",
                 "%+.3f+-%.3f" % (msb, ssb), "%+.3f+-%.3f" % (mob, sob), "%+.2f" % (db / sedb)])

    # ------------------------------------- pixel-index (time) locked component
    print("\nIS THE SHAPE LOCKED TO PIXEL INDEX RATHER THAN TO X?")
    print("  X and pixel index are the same axis inside one pass, so they can only be")
    print("  separated by a pass that has NO X motion, or by the backward pass.")
    allD = np.concatenate([D1, D2, E1, E2])
    mean_shape = allD.mean(axis=0)
    print("  mean of all %d detrended passes in the two images: %.0f counts RMS"
          % (len(allD), rms(mean_shape)))
    resid = allD - mean_shape
    print("  scatter about that common mean: %.0f counts RMS per pass"
          % np.mean([rms(r) for r in resid]))
    frac = rms(mean_shape) ** 2 / np.mean([rms(a) ** 2 for a in allD])
    print("  the one common shape accounts for %.0f%% of the variance of a pass" % (100 * frac))
    rows.append(["scan_wide_25nm_1/2", "common shape / pass variance",
                 "%.0f counts" % rms(mean_shape), "%.0f counts scatter"
                 % np.mean([rms(r) for r in resid]), "%.2f" % frac])

    # ------------------------------------------ the 12-pass repeat, over time
    print("\nTHE 12-PASS LINE REPEAT: does agreement decay with separation in TIME?")
    xs, pl, P = load_ycontrol(data("2026-09-17-bench", "line_repeated_wide.csv"))
    passes = np.array([v for p in pl for v in P[p]])[0::2]     # forward only (fwd==back bug)
    D = np.array([detrend(v) for v in passes])
    print("  lag  mean r    n")
    for lag in range(1, len(D)):
        rs = [corr(D[i], D[i + lag]) for i in range(len(D) - lag)]
        m, s, n = fisher_mean(rs)
        print("  %3d  %+.3f  %3d" % (lag, m, n))
        rows.append(["line_repeated_wide", "pass-separation %d" % lag, "%+.3f" % m, "", str(n)])
    prof = D.mean(axis=0)

    print("\n  HOW MUCH OF THE 636-COUNT PROFILE IS A SIMPLE BOW?")
    t = np.arange(len(prof), dtype=float)
    for deg in (2, 3, 4, 6):
        fit = np.polyval(np.polyfit(t, prof, deg), t)
        print("    polynomial degree %d explains %5.1f%% of its variance"
              % (deg, 100 * (1 - np.var(prof - fit) / np.var(prof))))
        rows.append(["line_repeated_wide", "poly deg %d of mean profile" % deg,
                     "%.1f%%" % (100 * (1 - np.var(prof - fit) / np.var(prof))), "", ""])

    print("\n  DOES THE 12-PASS PROFILE MATCH THE TWO 2D IMAGES AT THE SAME WIDTH?")
    print("    (same night, same tip, same sample, same X grid)")
    for tag, arr in (("image 1 forward lines", D1), ("image 2 forward lines", D2),
                     ("image 1 backward lines", E1), ("image 2 backward lines", E2)):
        cs = [corr(prof, a) for a in arr]
        m, s, n = fisher_mean(cs)
        print("    vs %-24s r = %+.3f +- %.3f over %d lines (mean shape r = %+.3f)"
              % (tag, m, s, n, corr(prof, arr.mean(axis=0))))
        rows.append(["line_repeated_wide profile", "vs " + tag, "%+.3f+-%.3f" % (m, s),
                     "%+.3f" % corr(prof, arr.mean(axis=0)), str(n)])

    with open(out("work", "0917_wide_place_test.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["source", "test", "a", "b", "c"])
        w.writerows(rows)
    print("\n-> %s" % out("work", "0917_wide_place_test.csv"))


if __name__ == "__main__":
    main()
