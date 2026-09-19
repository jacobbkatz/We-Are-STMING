"""03 - The +-15,000 reproducible profile: is it the sample, the scanner, or nothing?

Run from the repository root:

    python3 deliverables/2026-09-19-pause/candidates/code/03_wide_profile.py

Writes work/wide_profile.csv, work/wide_profiles.npz and prints the tables.

BACKGROUND
----------
sessions/2026-09-17-bench.md section 3.25, in the correction added at the wrap,
is the strongest open candidate this project has ever had:

    "At +-15,000 there is a reproducible profile of about 636 counts, and
     whether it is the sample or the scanner's own bow is UNDETERMINED. The
     experiment that would settle it - the same line at three separated Y
     positions AT +-15,000 - has NOT been run."

It HAS been run since. Code/pc/stm_y_control.py was written for exactly this,
and sessions/data/2026-09-19-bench/ycontrol_run{1,2,3,4}*.csv are it, on the
same X grid (17768..47768, 21 points, 1500 apart) as
sessions/data/2026-09-17-bench/line_repeated_wide.csv. This script:

  A. Re-derives the 2026-09-17 numbers from the committed file.
  B. Runs the three-Y discrimination on the 2026-09-19 runs at the SAME width,
     single pass against single pass on both sides, with the X-held controls
     put through the identical statistic.
  C. THE TEST NOBODY HAS RUN: compares the 2026-09-17 profile shape directly
     with the 2026-09-19 profile shapes on the identical X grid. Different
     night, different tip (the 2026-09-17 tip was replaced ~03:00 UTC
     2026-09-19), different gold, power cycled in between. A shape that
     survives all of that is the instrument, not any sample.

PROCESSING
----------
Every pass is detrended (least-squares straight line in X removed) before any
correlation or RMS. Nothing else is done to any pass: no smoothing, no
interpolation, no alignment, no outlier rejection.
"""
import csv
import itertools
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from stmload import load_ycontrol, data, out, detrend, corr, rms, fisher_mean

GRID = "17768..47768"   # 21 points, 1500 apart, +-15000 about midscale


def within_between(P, places):
    """Single-pass-against-single-pass correlations, within a place and between places.

    Both sides use exactly the same averaging depth (none), which is the defect
    that invalidated the 2026-09-17 control.
    """
    D = {p: np.array([detrend(v) for v in P[p]]) for p in places}
    within, between = [], []
    for p in places:
        for a, b in itertools.combinations(range(len(D[p])), 2):
            c = corr(D[p][a], D[p][b])
            if c is not None:
                within.append(c)
    for p, q in itertools.combinations(places, 2):
        for a in range(len(D[p])):
            for b in range(len(D[q])):
                c = corr(D[p][a], D[q][b])
                if c is not None:
                    between.append(c)
    mw, sw, nw = fisher_mean(within)
    mb, sb, nb = fisher_mean(between)
    diff = (mw - mb) if (mw is not None and mb is not None) else None
    sed = (sw ** 2 + sb ** 2) ** 0.5 if (sw and sb) else None
    return dict(within=mw, se_within=sw, n_within=nw,
                between=mb, se_between=sb, n_between=nb,
                diff=diff, se_diff=sed,
                sigma=(diff / sed) if (diff is not None and sed) else None)


def mean_profile(P, places):
    """Mean of the detrended passes, pooled over every pass at every place."""
    allp = [detrend(v) for p in places for v in P[p]]
    return np.mean(allp, axis=0)


def main():
    rows = []

    # ------------------------------------------------ A. 2026-09-17 re-derived
    print("A. THE 2026-09-17 +-15,000 LINE REPEAT, re-derived from the committed file")
    print("   sessions/data/2026-09-17-bench/line_repeated_wide.csv")
    xs17, pl17, P17 = load_ycontrol(data("2026-09-17-bench", "line_repeated_wide.csv"))
    # the file stores fwd and back per pass; section 3.25's review found they are
    # BYTE-IDENTICAL (the scratch diagnostic stored the forward pass twice), so
    # only the forward passes carry information. Confirm that here.
    raw = open(data("2026-09-17-bench", "line_repeated_wide.csv")).read().splitlines()[1:]
    ident = sum(1 for a, b in zip(raw[0::2], raw[1::2])
                if a.split(",", 2)[2] == b.split(",", 2)[2])
    print("   fwd/back rows byte-identical in %d of %d pairs (the known scratch-tool bug)"
          % (ident, len(raw) // 2))
    passes17 = np.array([v for p in pl17 for v in P17[p]])[0::2]   # forward only
    D17 = np.array([detrend(v) for v in passes17])
    cons = [corr(D17[i], D17[i + 1]) for i in range(len(D17) - 1)]
    mc, sc, nc = fisher_mean(cons)
    odd, even = D17[1::2].mean(axis=0), D17[0::2].mean(axis=0)
    prof17 = D17.mean(axis=0)
    print("   %d forward passes, consecutive-pass r %+.3f +- %.3f (n=%d)" % (len(D17), mc, sc, nc))
    print("   odd-pass average vs even-pass average r %+.3f" % corr(odd, even))
    print("   amplitude of the averaged profile: %.0f counts RMS" % rms(prof17))
    print("   (the session log records +0.515, +0.923 and 636 counts)")
    rows.append(["2026-09-17-bench/line_repeated_wide.csv", "12 passes, one place", GRID,
                 "%.3f" % mc, "%.3f" % corr(odd, even), "%.0f" % rms(prof17), "", "", ""])

    # -------------------------------------- B. the three-Y test at the SAME width
    print("\nB. THE THREE-Y DISCRIMINATION AT +-15,000 - single pass vs single pass")
    print("   'within' beating 'between' means the profile belongs to the PLACE (surface).")
    print("   'between' as good as 'within' means one fixed shape wherever it points (scanner).")
    print()
    print("   %-42s %-8s %7s %17s %17s %8s" % ("file", "y_sep", "passes",
                                               "within place", "between places", "sigma"))
    print("   " + "-" * 104)
    yfiles = [
        ("2026-09-19-bench", "ycontrol_run1.csv", "3000", "scan"),
        ("2026-09-19-bench", "ycontrol_xheld_run1.csv", "3000", "XHELD"),
        ("2026-09-19-bench", "ycontrol_run2_ysep12000.csv", "12000", "scan"),
        ("2026-09-19-bench", "ycontrol_run3_ysep12000_xheld.csv", "12000", "XHELD"),
        ("2026-09-19-bench", "ycontrol_run4_ysep12000_repeat.csv", "12000", "scan"),
        ("2026-09-17-bench", "line_three_y_positions.csv", "4000 (+-8000 X)", "scan"),
    ]
    profs = {}
    for sess, name, ysep, kind in yfiles:
        xs, places, P = load_ycontrol(data(sess, name))
        r = within_between(P, places)
        npass = sum(len(v) for v in P.values())
        print("   %-42s %-8s %7d  %+.3f +- %.3f  %+.3f +- %.3f  %s" % (
            name + ("" if kind == "scan" else "  [CONTROL]"), ysep, npass,
            r["within"], r["se_within"], r["between"], r["se_between"],
            "  --  " if r["sigma"] is None else "%+.1f" % r["sigma"]))
        rows.append(["%s/%s" % (sess, name), "three-Y %s, %s" % (ysep, kind),
                     "%d..%d" % (xs[0], xs[-1]), "", "", "",
                     "%+.3f+-%.3f" % (r["within"], r["se_within"]),
                     "%+.3f+-%.3f" % (r["between"], r["se_between"]),
                     "" if r["sigma"] is None else "%+.2f" % r["sigma"]])
        if int(xs[0]) == 17768:
            profs[name] = mean_profile(P, places)

    # ------------------------------- C. the cross-night shape comparison (new)
    print("\nC. THE CROSS-NIGHT TEST: is the 2026-09-17 shape still there on 2026-09-19?")
    print("   Same X grid %s. Different tip, different gold, powered down between." % GRID)
    print("   A shape that survives a tip change is the INSTRUMENT, not any sample.")
    print()
    profs["line_repeated_wide.csv (2026-09-17)"] = prof17
    names = list(profs)
    print("   %-44s %8s  %s" % ("mean detrended profile", "RMS", "r against 2026-09-17"))
    print("   " + "-" * 84)
    base = profs["line_repeated_wide.csv (2026-09-17)"]
    for n in names:
        c = corr(base, profs[n])
        print("   %-44s %8.0f  %s" % (n, rms(profs[n]),
                                      "   (self)" if n.startswith("line_repeated") else "%+.3f" % c))
        rows.append(["profile:%s" % n, "mean detrended profile", GRID, "", "",
                     "%.0f" % rms(profs[n]), "", "",
                     "" if n.startswith("line_repeated") else "%+.3f" % c])

    print("\n   full cross-correlation matrix of the mean profiles")
    print("   " + "".join("%9s" % ("P%d" % i) for i in range(len(names))))
    for i, a in enumerate(names):
        print("   P%-2d %s   %s" % (i, "".join("%9.2f" % corr(profs[a], profs[b])
                                               for b in names), a))

    np.savez(out("work", "wide_profiles.npz"), xs=xs17,
             **{k.replace(" ", "_"): v for k, v in profs.items()})
    with open(out("work", "wide_profile.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["source", "what", "x_grid", "consecutive_r", "split_half_r",
                    "profile_rms_counts", "within_place_r", "between_places_r", "sigma_or_r"])
        w.writerows(rows)
    print("\n-> %s" % out("work", "wide_profile.csv"))


if __name__ == "__main__":
    main()
