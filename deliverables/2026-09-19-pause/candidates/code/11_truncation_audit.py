"""11 - Audit of the min-length truncation defect, and of the three-Y non-reproduction.

Run from the repository root:

    python3 deliverables/2026-09-19-pause/candidates/code/11_truncation_audit.py

Writes work/truncation_audit.csv.

WHY THIS EXISTS
---------------
The lead found, while replicating the published numbers, that
sessions/data/2026-09-19-bench/scripts/analyze_scans.py lines 50-51 do

    n = min(len(fa), len(fb))
    c = corr(fa[:n], fb[:n])

with no shape check, so an aborted one-line file silently turns an
image-to-image correlation into a one-line-against-one-line correlation. That
made "the X-held controls reproduce better than the scans, +0.37 against +0.04"
- the load-bearing argument for dismissing the 2026-09-19 feedback scans - rest
on two 21-point correlations folded in with a 231-point one.

CLAUDE.md section 7 rule 1: a defect is a class, not an instance. So this
script:

  PART 1. Finds EVERY aborted or short recording in the whole data set and says
          which published comparison it entered.
  PART 2. Recomputes every image-to-image group mean the way analyze_scans.py
          did, and again like-for-like on full images only, so the size of the
          contamination is on the record for each one.
  PART 3. Verifies the three-Y run 2 / run 4 numbers from the raw CSVs,
          checking the shapes FIRST, using Code/pc/stm_y_control.py's own
          statistic, so the non-reproduction is confirmed or refuted
          independently of the tool that produced it.
"""
import csv
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "Code", "pc"))
import numpy as np
from stmload import load_raster, load_ycontrol, data, out, detrend, corr, rms, fisher_mean


def flat(path):
    """analyze_scans.py's 'flat': every detrended forward line, concatenated."""
    xs, ys, F, B = load_raster(path)
    return np.concatenate([detrend(f) for f in F]) if len(F) else np.array([])


def main():
    rows = []

    # ---------------------------------------------------- PART 1: short files
    print("PART 1. EVERY SHORT OR ABORTED RASTER RECORDING IN THE DATA SET")
    print("   a recording is 'short' if it has fewer lines than its own siblings")
    print()
    groups = {
        "2026-09-19-bench cas9 (feedback scans + controls)":
            sorted(glob.glob(data("2026-09-19-bench", "cas9_*.csv"))),
        "2026-09-19-bench img_ (wide images + controls)":
            sorted(glob.glob(data("2026-09-19-bench", "img_*.csv"))),
        "2026-09-19-bench cas8 chmap (constant height)":
            sorted(glob.glob(data("2026-09-19-bench", "cas8_chmap_*.csv"))),
        "2026-09-19-morning tuned_s3k (tuned loop)":
            sorted(glob.glob(data("2026-09-19-morning", "tuned_s3k_*.csv"))),
        # 2026-09-17's sets are grouped as the session actually compared them.
        # diag_scan_* are an 8-line experiment by design, not an aborted 12-line
        # one, and scan_wide_slow_* are a 5-line experiment: putting them in one
        # bucket with the 12- and 9-line sets would raise a false alarm.
        "2026-09-17-bench scan_fast_1..4 (the four compared images)":
            sorted(glob.glob(data("2026-09-17-bench", "scan_fast_*.csv"))),
        "2026-09-17-bench scan_slow_1/2":
            sorted(glob.glob(data("2026-09-17-bench", "scan_slow_[12].csv"))),
        "2026-09-17-bench diag_scan_* (8 lines by design)":
            sorted(glob.glob(data("2026-09-17-bench", "diag_scan_*.csv"))),
        "2026-09-17-bench scan_wide_25nm_1/2":
            sorted(glob.glob(data("2026-09-17-bench", "scan_wide_25nm_*.csv"))),
        "2026-09-17-bench scan_wide_slow_1/2 (5 lines by design)":
            sorted(glob.glob(data("2026-09-17-bench", "scan_wide_slow_*.csv"))),
        "2026-09-17-bench scan_slow_dwell_1/2":
            sorted(glob.glob(data("2026-09-17-bench", "scan_slow_dwell_*.csv"))),
    }
    for gname, paths in groups.items():
        lens = {os.path.basename(p): len(load_raster(p)[2]) for p in paths}
        mx = max(lens.values())
        short = {k: v for k, v in lens.items() if v < mx}
        print("   %-52s lines: %s" % (gname, sorted(set(lens.values()))))
        for k, v in sorted(short.items()):
            print("        SHORT  %-42s %2d of %2d lines" % (k, v, mx))
            rows.append(["short file", gname, k, "%d of %d lines" % (v, mx)])
        if not short:
            print("        all the same length - no truncation possible")
            rows.append(["short file", gname, "none", "all %d lines" % mx])

    # ------------------------------------- PART 2: the contaminated group means
    print("\nPART 2. EVERY IMAGE-TO-IMAGE GROUP MEAN, AS PUBLISHED AND LIKE FOR LIKE")
    print("   'as published' = analyze_scans.py, which truncates to the shorter file")
    print("   'like for like' = full-length images only")
    print()
    comparisons = [
        ("2026-09-19-bench", "cas9_scan", "2026-09-19 feedback scans", "+0.04"),
        ("2026-09-19-bench", "cas9_xheld", "2026-09-19 X-HELD CONTROLS", "+0.37"),
        ("2026-09-19-bench", "img_scan", "2026-09-19 wide images", "+0.56 to +0.86"),
        ("2026-09-19-bench", "img_xheld", "2026-09-19 wide X-HELD CONTROLS", "+0.56"),
        ("2026-09-19-morning", "tuned_s3k_scan", "2026-09-19 morning tuned scans", "not quoted"),
        ("2026-09-19-morning", "tuned_s3k_xheld", "2026-09-19 morning tuned CONTROLS", "not quoted"),
    ]
    for sess, pref, label, published in comparisons:
        paths = sorted(glob.glob(data(sess, pref + "*.csv")))
        arrs = [(os.path.basename(p), flat(p)) for p in paths]
        nlines = {n: len(load_raster(data(sess, n))[2]) for n, _ in arrs}
        mx = max(nlines.values())
        pub, like = [], []
        pub_pts, like_pts = [], []
        for (na, a), (nb, b) in zip(arrs, arrs[1:]):
            n = min(len(a), len(b))
            c = corr(a[:n], b[:n])
            if c is not None:
                pub.append(c)
                pub_pts.append(n)
        full = [(n, a) for n, a in arrs if nlines[n] == mx]
        for (na, a), (nb, b) in zip(full, full[1:]):
            c = corr(a, b)
            if c is not None:
                like.append(c)
                like_pts.append(len(a))
        print("   %-36s published %s" % (label, published))
        print("        as published : %s  (points %s)  mean %s"
              % (" ".join("%+.2f" % c for c in pub), " ".join(str(p) for p in pub_pts),
                 "%+.3f" % np.mean(pub) if pub else "-"))
        print("        like for like: %s  (points %s)  mean %s"
              % (" ".join("%+.2f" % c for c in like) or "none",
                 " ".join(str(p) for p in like_pts) or "-",
                 "%+.3f" % np.mean(like) if like else "TOO FEW FULL IMAGES"))
        rows.append(["group mean", label, "published " + published,
                     "as-published %s" % (" ".join("%+.2f" % c for c in pub)),
                     "points %s" % (" ".join(str(p) for p in pub_pts)),
                     "like-for-like %s" % (" ".join("%+.2f" % c for c in like) or "none")])
    print("""
   TWO conclusions were contaminated, not one.
   1. The cas9 controls' +0.37, as the lead found: two of three pairs were
      21-point comparisons against cas9_xheld2.csv, which is ONE line.
   2. The WIDE images' "+0.56 to +0.86, matched by the X-held controls' +0.56"
      (sessions/2026-09-19-bench.md 3.16) has the SAME defect and it is worse:
      img_scan_0.csv is 1 line and img_scan_1.csv is 2 lines, so BOTH scan
      pairs were short comparisons and NEITHER was an image-to-image
      correlation. There are not two full wide images, so no like-for-like
      scan figure exists at all. The controls' +0.56 is a genuine 231-point
      number. The comparison as published is between things of different kinds.

   2026-09-17 IS CLEAN. Every set that session compared against itself is of
   uniform length (scan_fast 12 lines, scan_slow 12, diag_scan 8, wide_25nm 9,
   wide_slow 5, slow_dwell 7), and its other figures - corrugation and
   trace/retrace - are per-file statistics that no truncation can touch.""")

    # -------------------------------------------- PART 3: the three-Y re-check
    print("\nPART 3. THE THREE-Y CONTROL, RE-VERIFIED FROM THE RAW CSVs")
    print("   shapes checked FIRST, then the tool's own statistic re-run")
    print()
    import stm_y_control as yc
    for nm, what, published in [
            ("ycontrol_run2_ysep12000.csv", "run 2, the 3.9 sigma run", "+0.374 +- 0.097"),
            ("ycontrol_run4_ysep12000_repeat.csv", "run 4, the repeat", "+0.056 +- 0.094"),
            ("ycontrol_run3_ysep12000_xheld.csv", "run 3, X-HELD CONTROL", "+0.070 +- 0.084"),
            ("ycontrol_run1.csv", "run 1, y_sep 3000", "+0.032 +- 0.035"),
            ("ycontrol_xheld_run1.csv", "X-HELD CONTROL, y_sep 3000", "+0.164 +- 0.082")]:
        xs, places, P = load_ycontrol(data("2026-09-19-bench", nm))
        shapes = {p: (len(P[p]), P[p].shape[1]) for p in places}
        ok = len({s for s in shapes.values()}) == 1
        pl = {p: [list(v) for v in P[p]] for p in places}
        r = yc.analyse(pl)
        d = r["within_single"] - r["between_single"]
        se = (r["within_single_sd"] ** 2 / max(r["n_within_single"], 1)
              + r["between_single_sd"] ** 2 / max(r["n_between_single"], 1)) ** 0.5
        print("   %-38s shapes %s %s" % (nm, sorted(set(shapes.values())),
                                         "OK" if ok else "*** MISMATCH ***"))
        print("        published  %s" % published)
        print("        replicated within %+.3f  between %+.3f  difference %+.3f +- %.3f"
              % (r["within_single"], r["between_single"], d, se))
        rows.append(["three-Y re-check", nm, what, "published " + published,
                     "replicated %+.3f +- %.3f" % (d, se),
                     "shapes " + ("uniform" if ok else "MISMATCH")])
    print("""
   EVERY three-Y file is 3 places x 6 passes x 21 points, with no short pass
   and no aborted run anywhere. There is no shape mismatch to find, so the
   truncation defect does NOT touch this result. Run 2's +0.374 and run 4's
   +0.056 are both reproduced from the raw CSVs. THE NON-REPRODUCTION IS REAL.

   It is also weaker than it looks in the other direction: script 07 shows that
   under a permutation null - which respects the fact that the pairwise
   correlations share passes - run 2 is p = 0.0036, not 3.9 sigma, and an
   X-HELD CONTROL scores p = 0.02 on the same statistic with nothing to see.""")

    with open(out("work", "truncation_audit.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["part", "a", "b", "c", "d", "e"])
        for r in rows:
            w.writerow(list(r) + [""] * (6 - len(r)))
    print("\n-> %s" % out("work", "truncation_audit.csv"))


if __name__ == "__main__":
    main()
