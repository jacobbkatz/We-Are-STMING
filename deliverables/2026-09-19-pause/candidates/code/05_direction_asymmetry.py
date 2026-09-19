"""05 - Is the 2026-09-17 636-count profile a SURFACE or a FORWARD-SCAN signature?

Run from the repository root:

    python3 deliverables/2026-09-19-pause/candidates/code/05_direction_asymmetry.py

Writes work/direction_asymmetry.csv.

THE ARGUMENT
------------
line_repeated_wide.csv holds 12 passes of one line at +-15,000 X. Its forward
and backward rows are byte-identical - the scratch diagnostic stored the
forward pass twice (found by an independent review, recorded in
sessions/2026-09-17-bench.md section 3.25). So all 12 of its passes are
FORWARD passes. Its averaged detrended profile is 636 counts RMS and it is the
project's strongest surviving candidate.

A profile that belongs to the SAMPLE must appear when the same line is scanned
in the other direction, at the same X. A profile that is the scan's own
signature - loop lag, piezo hysteresis, a settling transient indexed by pixel
number - appears in one direction and reverses or vanishes in the other.

scan_wide_25nm_1.csv and _2.csv give us both directions on the same X grid, the
same night, the same tip, the same sample: 9 forward and 9 backward passes each.

Also here: which of the 9 Y places, if any, the 12-pass profile prefers. If the
profile is the surface at one Y it should match THAT line and not the others.

PROCESSING: least-squares straight line in X removed from every pass. Nothing
else.
"""
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from stmload import load_raster, load_ycontrol, data, out, detrend, corr, rms, fisher_mean


def main():
    rows = []
    xs, pl, P = load_ycontrol(data("2026-09-17-bench", "line_repeated_wide.csv"))
    D = np.array([detrend(v) for v in np.array([v for p in pl for v in P[p]])[0::2]])
    prof = D.mean(axis=0)
    per_pass = np.mean([rms(d) for d in D])
    print("THE 12-PASS +-15,000 PROFILE (sessions/data/2026-09-17-bench/line_repeated_wide.csv)")
    print("  per-pass detrended RMS  %.0f counts" % per_pass)
    print("  averaged profile RMS    %.0f counts" % rms(prof))
    print("  the common shape is %.0f%% of a single pass's variance"
          % (100 * rms(prof) ** 2 / np.mean([rms(d) ** 2 for d in D])))
    rows.append(["line_repeated_wide", "per-pass RMS", "%.0f" % per_pass])
    rows.append(["line_repeated_wide", "profile RMS", "%.0f" % rms(prof)])

    print("\nTHE SAME X GRID, BOTH DIRECTIONS (scan_wide_25nm_1.csv and _2.csv)")
    means = {}
    for img in ("1", "2"):
        xs2, ys, F, B = load_raster(data("2026-09-17-bench", "scan_wide_25nm_%s.csv" % img))
        assert list(xs2) == list(xs)
        means["img%s_fwd" % img] = np.array([detrend(f) for f in F]).mean(axis=0)
        means["img%s_back" % img] = np.array([detrend(b) for b in B]).mean(axis=0)
    print("  %-14s %8s  %s" % ("mean shape", "RMS", "r against the 12-pass profile"))
    for k, v in means.items():
        c = corr(prof, v)
        print("  %-14s %8.0f  %+.3f" % (k, rms(v), c))
        rows.append(["scan_wide_25nm", "mean shape " + k, "RMS %.0f, r vs profile %+.3f" % (rms(v), c)])
    fwd_mean = (means["img1_fwd"] + means["img2_fwd"]) / 2
    back_mean = (means["img1_back"] + means["img2_back"]) / 2
    print("\n  forward mean of both images  vs the 12-pass profile: r = %+.3f" % corr(prof, fwd_mean))
    print("  backward mean of both images vs the 12-pass profile: r = %+.3f" % corr(prof, back_mean))
    print("  forward mean vs backward mean:                       r = %+.3f" % corr(fwd_mean, back_mean))
    print("""
  READ THIS WITH SCRIPT 08 AND 09. The obvious reading - "a surface profile must
  appear in both directions, this one does not, so it is not a surface" - is
  what this script originally concluded and it is NOT SOUND. Trace and retrace
  in a scanning probe are routinely offset from each other by piezo hysteresis
  and loop delay, so a real feature can sit at a different stored index in the
  two directions. Script 08 checked and found the backward match reaches +0.848
  at a shift of 4 pixels, HIGHER than the forward match at zero shift. Script 09
  then puts a null under that lag search and finds the best-of-13-lags
  correlation is +0.51 +- 0.15 for phase-randomised noise, so neither number is
  far from chance. The direction argument alone settles nothing; the place test
  in script 04 is what carries the weight.""")
    rows.append(["scan_wide_25nm", "fwd mean vs profile", "%+.3f" % corr(prof, fwd_mean)])
    rows.append(["scan_wide_25nm", "back mean vs profile", "%+.3f" % corr(prof, back_mean)])
    rows.append(["scan_wide_25nm", "fwd mean vs back mean", "%+.3f" % corr(fwd_mean, back_mean)])

    print("\nDOES THE PROFILE PREFER ONE Y PLACE? (it should, if it is the surface)")
    print("  %-8s %10s %10s %10s %10s" % ("Y", "img1 fwd", "img2 fwd", "img1 back", "img2 back"))
    xs1, ys1, F1, B1 = load_raster(data("2026-09-17-bench", "scan_wide_25nm_1.csv"))
    xs2, ys2, F2, B2 = load_raster(data("2026-09-17-bench", "scan_wide_25nm_2.csv"))
    for k, y in enumerate(ys1):
        cs = [corr(prof, detrend(a[k])) for a in (F1, F2, B1, B2)]
        print("  %-8d %10.2f %10.2f %10.2f %10.2f" % (y, *cs))
        rows.append(["scan_wide_25nm", "profile vs Y=%d" % y,
                     " ".join("%+.2f" % c for c in cs)])
    allf = [corr(prof, detrend(a[k])) for a in (F1, F2) for k in range(len(ys1))]
    m, s, n = fisher_mean(allf)
    best = max(allf)
    print("\n  mean over the 18 forward lines %+.3f +- %.3f; best single line %+.3f" % (m, s, best))
    print("  No single place stands out at zero lag. Script 09 repeats this with a lag")
    print("  allowed on every line and finds every line inside the surrogate distribution.")
    rows.append(["scan_wide_25nm", "profile vs 18 fwd lines", "mean %+.3f+-%.3f best %+.3f" % (m, s, best)])

    with open(out("work", "direction_asymmetry.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["source", "quantity", "value"])
        w.writerows(rows)
    print("\n-> %s" % out("work", "direction_asymmetry.csv"))


if __name__ == "__main__":
    main()
