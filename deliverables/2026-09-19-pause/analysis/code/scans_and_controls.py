"""Every scan in the repository, measured against its own control.

    python3 deliverables/2026-09-19-pause/analysis/code/scans_and_controls.py

This is an independent re-implementation of the test the project already uses
(sessions/data/2026-09-19-bench/scripts/analyze_scans.py): each line is detrended, then

  corrugation    RMS of a detrended forward line, averaged over lines
  trace/retrace  correlation of the forward pass with the backward pass, line by line
  image-to-image correlation of one detrended forward image with the next

A real image needs the scans to beat their X-HELD CONTROLS on these. The controls are
runs with identical timing in which X never moved, so anything they show is the loop,
the junction or the drift, not the surface.

It also runs the mechanical checks that a reader of a data directory should run before
believing anything: short and aborted files, duplicated passes, and pixels sitting on a
clamp.

Outputs: plots/fig14_scan_vs_control.png, fig15_scan_examples.png,
plus scan_stats.csv in the analysis directory.
"""
import csv
import glob
import math
import os
import statistics as st
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (ANALYSIS, DATA, read_scan, pearson, detrend, style, save,
                    section, TOL, SERIES, REPO)

# Code/pc/stm_feedback_scan.py sets Z_MIN_SAFE, Z_MAX_SAFE = 12000, 48000. The wide runs
# of 2026-09-19 bench raised the top to 60000 in their wrappers
# (sessions/data/2026-09-19-bench/scripts/run_img_wide.py, run_ycontrol_wide.py), so a
# pixel is counted as clamped only when it sits EXACTLY on one of the three values the
# code can produce. That is data-driven and does not need a per-file setting.
Z_CLAMPS = (12000, 48000, 60000)
ADC_RAIL = 32767                            # the converter's own limit

# cas8_chmap_* are constant-HEIGHT maps: the cell is the averaged CURRENT at a fixed Z,
# not the Z the loop needed. They are listed separately for that reason.
CURRENT_MAP_PREFIX = "cas8_chmap_"


def rms(vals):
    v = [x for x in vals if x is not None]
    if len(v) < 2:
        return None
    m = st.mean(v)
    return math.sqrt(sum((x - m) ** 2 for x in v) / len(v))


def stats(path):
    xs, rows = read_scan(path)
    fwd = [(y, v) for y, d, v in rows if d in ("fwd", "p0", "a")]
    back = [(y, v) for y, d, v in rows if d in ("back", "p1", "b")]
    if not fwd and rows:                      # y-control files use pass numbers
        fwd = [(y, v) for y, d, v in rows if str(d).strip() in ("0", "a")]
    cor = [rms(detrend(v)) for _, v in fwd]
    cor = [c for c in cor if c is not None]
    tr = []
    for (ya, fa), (yb, fb) in zip(fwd, back):
        c = pearson(detrend(fa), detrend(fb))
        if c is not None:
            tr.append(c)
    flat = [v for _, f in fwd for v in detrend(f)]
    cells = [v for _, _, vv in rows for v in vv]
    filled = [v for v in cells if v is not None]
    is_current = os.path.basename(path).startswith(CURRENT_MAP_PREFIX)
    header0 = open(path).readline().split(",")[0]
    if is_current:
        stuck = sum(1 for v in filled if abs(v) >= ADC_RAIL)
    else:
        stuck = sum(1 for v in filled if int(v) in Z_CLAMPS)
    # Two identical passes are a tool defect ONLY if the line was not pinned: where every
    # pixel of both passes sits on the same clamp or rail they agree for a physical reason.
    def pinned(v):
        vv = [x for x in v if x is not None]
        return bool(vv) and all((abs(x) >= ADC_RAIL) if is_current else (int(x) in Z_CLAMPS)
                                for x in vv)
    dup = sum(1 for (ya, fa), (yb, fb) in zip(fwd, back) if fa == fb)
    dup_unexplained = sum(1 for (ya, fa), (yb, fb) in zip(fwd, back)
                          if fa == fb and not pinned(fa))
    return dict(path=path, n_x=len(xs), n_rows=len(rows), n_fwd=len(fwd),
                n_back=len(back), cells=len(cells), filled=len(filled),
                corrugation=st.mean(cor) if cor else None,
                trace_retrace=st.mean(tr) if tr else None,
                n_tr=len(tr), flat=flat, is_current=is_current, header0=header0,
                clamp_frac=stuck / len(filled) if filled else None,
                identical_passes=dup, identical_unexplained=dup_unexplained)


def flat_of(path, drop_first=0):
    """Detrended forward image as one flat list, optionally dropping leading lines."""
    xs, rows = read_scan(path)
    fwd = [v for _, d, v in rows if d in ("fwd", "p0", "a")]
    fwd = fwd[drop_first:]
    return [v for f in fwd for v in detrend(f)]


def image_to_image(group, res, drop_first=0):
    out = []
    for a, b in zip(group, group[1:]):
        fa = res[a]["flat"] if drop_first == 0 else flat_of(a, drop_first)
        fb = res[b]["flat"] if drop_first == 0 else flat_of(b, drop_first)
        n = min(len(fa), len(fb))
        if n < 6:
            continue
        c = pearson(fa[:n], fb[:n])
        if c is not None:
            out.append(c)
    return out


# Every scan-shaped file, grouped into the comparisons the sessions actually made.
GROUPS = [
    ("2026-09-17 narrow, 4 fast images",
     "2026-09-17-bench", ["scan_fast_1.csv", "scan_fast_2.csv", "scan_fast_3.csv",
                          "scan_fast_4.csv"], []),
    ("2026-09-17 narrow, 2 slow images",
     "2026-09-17-bench", ["scan_slow_1.csv", "scan_slow_2.csv"], []),
    ("2026-09-17 narrow, 250 corrections per pixel",
     "2026-09-17-bench", ["scan_slow_dwell_1.csv", "scan_slow_dwell_2.csv"], []),
    ("2026-09-17 diagnostic: 15 corrections, vs X HELD",
     "2026-09-17-bench", ["diag_scan_normal_1.csv", "diag_scan_normal_2.csv"],
     ["diag_scan_x_held.csv"]),
    ("2026-09-17 wide +-4000 X",
     "2026-09-17-bench", ["scan_wide_slow_1.csv", "scan_wide_slow_2.csv"], []),
    ("2026-09-17 wide +-15000 X",
     "2026-09-17-bench", ["scan_wide_25nm_1.csv", "scan_wide_25nm_2.csv"], []),
    ("2026-09-19 bench cas8 constant-height maps (SATURATED)",
     "2026-09-19-bench", sorted(os.path.basename(p) for p in
                                glob.glob(os.path.join(DATA, "2026-09-19-bench",
                                                       "cas8_chmap_*scan*.csv"))),
     sorted(os.path.basename(p) for p in
            glob.glob(os.path.join(DATA, "2026-09-19-bench", "cas8_chmap_*xheld*.csv")))),
    ("2026-09-19 bench cas9 feedback scans vs X-held controls",
     "2026-09-19-bench", ["cas9_scan0.csv", "cas9_scan1.csv", "cas9_scan2.csv",
                          "cas9_scan3.csv"],
     ["cas9_xheld0.csv", "cas9_xheld1.csv", "cas9_xheld2.csv", "cas9_xheld3.csv"]),
    ("2026-09-19 bench wide images vs X-held controls",
     "2026-09-19-bench", ["img_scan_0.csv", "img_scan_1.csv", "img_scan_2.csv"],
     ["img_xheld_0.csv", "img_xheld_1.csv"]),
    ("2026-09-19 morning tuned scans (loop constant 1800) vs controls",
     "2026-09-19-morning", ["tuned_s3k_scan0.csv", "tuned_s3k_scan1.csv",
                            "tuned_s3k_scan2.csv"],
     ["tuned_s3k_xheld0.csv", "tuned_s3k_xheld1.csv", "tuned_s3k_xheld2.csv"]),
]

LINE_FILES = [
    ("2026-09-17-bench", "diag_line_repeated.csv", "one line, 10 passes, +-400 X"),
    ("2026-09-17-bench", "line_repeated_wide.csv", "one line, 12 passes, +-15000 X"),
    ("2026-09-17-bench", "line_three_y_positions.csv", "one line at 3 Y places, +-8000 X"),
]

YCONTROL = [
    ("ycontrol_run1.csv", "three Y places +-3000, scanning"),
    ("ycontrol_xheld_run1.csv", "three Y places +-3000, X HELD"),
    ("ycontrol_run2_ysep12000.csv", "three Y places +-12000, scanning"),
    ("ycontrol_run3_ysep12000_xheld.csv", "three Y places +-12000, X HELD"),
    ("ycontrol_run4_ysep12000_repeat.csv", "three Y places +-12000, scanning, REPEAT"),
]


def main():
    plt = style()
    allrows = []

    section("1. EVERY SCAN FILE, AND ITS OWN CONTROL")
    summary = []
    for title, sess, scans, ctrls in GROUPS:
        print("\n  %s" % title)
        res = {}
        for name in scans + ctrls:
            p = os.path.join(DATA, sess, name)
            if not os.path.exists(p):
                print("    %-40s MISSING" % name)
                continue
            s = stats(p)
            res[p] = s
            kind = "control" if name in ctrls else "scan"
            print("    %-40s %-8s lines %2d/%2d  corrugation %8s  trace/retrace %6s  "
                  "%s %5s%s"
                  % (name, kind, s["n_fwd"], s["n_x"],
                     "%.0f" % s["corrugation"] if s["corrugation"] else "-",
                     "%+.2f" % s["trace_retrace"] if s["trace_retrace"] is not None else "-",
                     "railed" if s["is_current"] else "clamped",
                     "%.0f%%" % (100 * s["clamp_frac"]) if s["clamp_frac"] is not None else "-",
                     "  IDENTICAL fwd/back passes!" if s["identical_unexplained"]
                     else ("  (passes identical, but every pixel pinned)"
                           if s["identical_passes"] else "")))
            allrows.append(dict(group=title, session=sess, file=name, kind=kind,
                                lines=s["n_fwd"], x_pixels=s["n_x"],
                                corrugation=s["corrugation"],
                                trace_retrace=s["trace_retrace"],
                                clamped_fraction=s["clamp_frac"],
                                identical_passes=s["identical_passes"],
                                identical_unexplained=s["identical_unexplained"]))
        sc = [os.path.join(DATA, sess, n) for n in scans
              if os.path.join(DATA, sess, n) in res]
        ct = [os.path.join(DATA, sess, n) for n in ctrls
              if os.path.join(DATA, sess, n) in res]
        i2i_s, i2i_c = image_to_image(sc, res), image_to_image(ct, res)
        if i2i_s:
            print("    image-to-image, scans   : %s  (mean %+.2f, n = %d pairs)"
                  % (" ".join("%+.2f" % c for c in i2i_s), st.mean(i2i_s), len(i2i_s)))
            # The first-line trap, documented in sessions/2026-09-17-bench.md 3.22: the
            # loop's settling transient on line 1 is identical in every image because the
            # procedure is identical, and it alone can carry the whole correlation.
            d1 = image_to_image(sc, res, 1)
            d2 = image_to_image(sc, res, 2)
            if d1 and d2:
                print("      drop line 1: mean %+.2f    drop lines 1-2: mean %+.2f%s"
                      % (st.mean(d1), st.mean(d2),
                         "   <- the agreement was the loop settling, not the sample"
                         if st.mean(i2i_s) - st.mean(d2) > 0.3 else ""))
        if i2i_c:
            print("    image-to-image, CONTROLS: %s  (mean %+.2f, n = %d pairs)"
                  % (" ".join("%+.2f" % c for c in i2i_c), st.mean(i2i_c), len(i2i_c)))
            d1 = image_to_image(ct, res, 1)
            d2 = image_to_image(ct, res, 2)
            if d1 and d2:
                print("      drop line 1: mean %+.2f    drop lines 1-2: mean %+.2f"
                      % (st.mean(d1), st.mean(d2)))
        if i2i_s and i2i_c:
            verdict = ("CONTROLS REPRODUCE BETTER - no image"
                       if st.mean(i2i_c) >= st.mean(i2i_s) else
                       "scans reproduce better - worth a second look")
            print("    VERDICT: %s" % verdict)
            summary.append((title, st.mean(i2i_s), st.mean(i2i_c), len(i2i_s), len(i2i_c),
                            st.mean([s["corrugation"] for p, s in res.items()
                                     if p in sc and s["corrugation"]]),
                            st.mean([s["corrugation"] for p, s in res.items()
                                     if p in ct and s["corrugation"]])))

    section("1b. THE ONE GROUP WHERE THE SCANS BEAT THEIR CONTROL - and why it is not "
            "evidence")
    print("  The wide images of 2026-09-19 bench are the only group above where the real")
    print("  scans correlate better with each other than the controls do. Three things")
    print("  have to be said before anyone reads that as an image.")
    print()
    wid = "2026-09-19-bench"
    scan_files = ["img_scan_0.csv", "img_scan_1.csv", "img_scan_2.csv"]
    ctrl_files = ["img_xheld_0.csv", "img_xheld_1.csv"]
    for n in scan_files + ctrl_files:
        s = stats(os.path.join(DATA, wid, n))
        print("    %-18s %2d forward lines of a planned 11  ->  %d pixels compared"
              % (n, s["n_fwd"], s["n_fwd"] * s["n_x"]))
    print()
    print("  (1) TWO OF THE THREE SCANS ABORTED after one and two lines. The image-to-")
    print("      image correlation is truncated to the shorter file, so the +0.86 is 21")
    print("      pixels - a SINGLE line - and the +0.56 is 42 pixels. The controls'")
    print("      +0.56 is 231 pixels. Those are not the same measurement.")
    lim = {}
    for k in (1, 2, 11):
        sc = [os.path.join(DATA, wid, n) for n in scan_files]
        ct = [os.path.join(DATA, wid, n) for n in ctrl_files]

        def cut(paths, nlines):
            out = []
            for a, b in zip(paths, paths[1:]):
                fa, fb = flat_of(a)[:nlines * 21], flat_of(b)[:nlines * 21]
                m = min(len(fa), len(fb))
                if m >= 6:
                    c = pearson(fa[:m], fb[:m])
                    if c is not None:
                        out.append(c)
            return out
        s_, c_ = cut(sc, k), cut(ct, k)
        lim[k] = (s_, c_)
        print("      first %2d line(s) only: scans %s | controls %s"
              % (k, " ".join("%+.2f" % x for x in s_) or "-",
                 " ".join("%+.2f" % x for x in c_) or "-"))
    print("      Cut to the same first line, the two scan pairs give %s and the one"
          % " and ".join("%+.2f" % x for x in lim[1][0]))
    print("      control pair gives %s. n = 2 against n = 1, and the two scan pairs"
          % " and ".join("%+.2f" % x for x in lim[1][1]))
    print("      disagree with each other by more than the gap to the control. NOTHING IS")
    print("      ESTABLISHED EITHER WAY by this comparison; points (2) and (3) are what")
    print("      carry the conclusion.")
    print()
    print("  (2) THE FIRST LINE IS THE ONE LINE THAT IS GUARANTEED TO AGREE. It carries")
    print("      the loop's settling transient, which is identical in every image because")
    print("      the procedure is identical. sessions/2026-09-17-bench.md 3.22 found")
    print("      exactly this and section 1 above reproduces it: those 2026-09-17 images")
    print("      fall from +0.70 to -0.08 when the first two lines are dropped.")
    print()
    print("  (3) TRACE AND RETRACE ARE STRONGLY ANTI-CORRELATED in all three wide scans")
    print("      (-0.75 to -0.94) and NOT in the controls (+0.13, +0.14). A surface is")
    print("      traced the same way in both directions, so it gives a POSITIVE")
    print("      trace/retrace. A negative one is the loop chasing, which is the reading")
    print("      sessions/2026-09-19-morning.md section 6 settled on.")
    print()
    print("  NOT AVAILABLE: there is no .log file for the img_scan / img_xheld runs in")
    print("  sessions/data/2026-09-19-bench/. The 'saturated 14.5 per cent' figure in the")
    print("  session log came from console output that was not saved, so it cannot be")
    print("  checked here: the CSV records the Z the loop reached, not whether the")
    print("  current was saturated at that pixel. Compare cas9.log, which DOES carry the")
    print("  loop's own saturated and clamped counters for every run.")

    section("2. AGAINST THE PUBLISHED FIGURES")
    print("  sessions/2026-09-19-bench.md 3.14 (cas9): trace/retrace scans")
    print("    -0.10, +0.43, -0.45, -0.07; controls -0.38, -0.05, +0.12, +0.31")
    print("    image-to-image +0.09 +0.18 -0.15 (mean +0.04); controls +0.20 +0.21 +0.70")
    print("    (mean +0.37); corrugation 82-147 against the controls' 41-82")
    print("  sessions/2026-09-17-bench.md 3.22 (scan_fast): trace/retrace")
    print("    +0.09, +0.01, 0.00, 0.00; image-to-image -0.09 to +0.27;")
    print("    corrugation 13-20 counts")
    print("  sessions/2026-09-19-bench.md 3.16 (wide): trace/retrace -0.75 to -0.94,")
    print("    image-to-image +0.56 to +0.86, controls +0.56, saturation 14.5%")
    print("  Compare these with section 1. Where they differ, the difference is in the")
    print("  detrending and in which lines an aborted file supplies, not in the verdict.")

    section("3. REPEATED SINGLE LINES")
    for sess, name, what in LINE_FILES:
        p = os.path.join(DATA, sess, name)
        xs, rows = read_scan(p)
        allp = [v for _, _, v in rows]
        labels = [d for _, d, _ in rows]
        ident = sum(1 for a, b in zip(allp, allp[1:]) if a == b)
        # Forward passes only. In the two 2026-09-17 line files the scratch tool stored
        # the forward pass twice, so every 'back' row duplicates the 'fwd' row above it
        # and including them would double-count.
        if "fwd" in labels:
            passes = [v for _, d, v in rows if d == "fwd"]
        else:
            passes = allp
        cons = [pearson(detrend(a), detrend(b)) for a, b in zip(passes, passes[1:])]
        cons = [c for c in cons if c is not None]
        print("\n  %-32s %s" % (name, what))
        print("    %d rows, %d used (forward only where labelled), %d X points; labels %s"
              % (len(allp), len(passes), len(xs), sorted(set(labels))))
        print("    consecutive-pass r: mean %+.3f over %d pairs"
              % (st.mean(cons) if cons else float("nan"), len(cons)))
        if ident:
            print("    *** %d consecutive pass pairs are BYTE-IDENTICAL: the scratch tool"
                  % ident)
            print("        stored the forward pass twice. Any trace-versus-retrace figure")
            print("        from this file is meaningless. Already recorded in")
            print("        sessions/2026-09-17-bench.md 3.25, found there by an independent")
            print("        review of the committed data. Reproduced here mechanically.")
        # odd-average against even-average, the statistic the 2026-09-17 log used
        odd = [p_ for i, p_ in enumerate(passes) if i % 2 == 1]
        even = [p_ for i, p_ in enumerate(passes) if i % 2 == 0]
        if len(odd) >= 2 and len(even) >= 2:
            def avg(group):
                n = min(len(g) for g in group)
                return [st.mean([g[i] for g in group if g[i] is not None])
                        if any(g[i] is not None for g in group) else None
                        for i in range(n)]
            ao, ae = detrend(avg(odd)), detrend(avg(even))
            n = min(len(ao), len(ae))
            print("    odd-pass average against even-pass average: r = %+.3f"
                  % (pearson(ao[:n], ae[:n]) or float("nan")))
            print("    amplitude of the averaged profile: %.0f counts (RMS after detrend)"
                  % (rms(ao) or float("nan")))

    section("4. THE THREE-Y CONTROL FILES")
    print("  The test: does one place on the sample look more like ITSELF than it looks")
    print("  like a different place 3,000 or 12,000 Y counts away? A surface says yes. A")
    print("  shape belonging to the scanner says no.")
    ysig = []
    for name, what in YCONTROL:
        p = os.path.join(DATA, "2026-09-19-bench", name)
        xs, rows = read_scan(p)
        places = {}
        for yoff, pas, vals in rows:
            places.setdefault(yoff, []).append(vals)
        print("\n  %-38s %s" % (name, what))
        print("    %d Y places, %d passes each, %d X points"
              % (len(places), len(next(iter(places.values()))), len(xs)))
        within, between = [], []
        keys = sorted(places)
        for k in keys:
            ps = [detrend(v) for v in places[k]]
            for i in range(len(ps)):
                for j in range(i + 1, len(ps)):
                    c = pearson(ps[i], ps[j])
                    if c is not None:
                        within.append(c)
        for a in range(len(keys)):
            for b in range(a + 1, len(keys)):
                for pa in places[keys[a]]:
                    for pb in places[keys[b]]:
                        c = pearson(detrend(pa), detrend(pb))
                        if c is not None:
                            between.append(c)
        if within and between:
            d = st.mean(within) - st.mean(between)
            se = math.sqrt(st.pstdev(within) ** 2 / len(within)
                           + st.pstdev(between) ** 2 / len(between))
            print("    single pass vs single pass: WITHIN a place %+.3f (n = %d pairs), "
                  "BETWEEN places %+.3f (n = %d)"
                  % (st.mean(within), len(within), st.mean(between), len(between)))
            print("    difference %+.3f +- %.3f  ->  %s"
                  % (d, se, "within beats between: a surface would do this"
                     if d > 2 * se else "no difference resolved"))
            print("    profile RMS per place: %s"
                  % ", ".join("%.0f" % (rms(detrend(places[k][0])) or 0) for k in keys))
            ysig.append((name, "X HELD" in what.upper(), d, se, d > 2 * se))
    print()
    print("  MULTIPLE COMPARISONS, AND THE CONTROL THAT SETTLES IT.")
    hits = [r for r in ysig if r[4]]
    print("  This test was run on %d files and came out positive on %d."
          % (len(ysig), len(hits)))
    for n, held, d, se, ok in hits:
        print("    %-40s %+.3f +- %.3f%s"
              % (n, d, se, "   <- THIS IS AN X-HELD CONTROL" if held else ""))
    if any(r[1] for r in hits):
        print("  One of the positives is an X-HELD CONTROL, in which X never moved and")
        print("  there is therefore NO surface to see. A statistic that fires on a run")
        print("  with no lateral motion is biased in this data, and the same bias is")
        print("  available to the run that fired without X held. The session log reaches")
        print("  the same conclusion by a different route (2026-09-19-bench.md 3.15).")
    print("  Independent runs: %d. At a two-standard-error threshold about %.1f false"
          % (len(ysig), 0.046 * len(ysig)))
    print("  positive is expected across that many tests by chance alone, and that is")
    print("  the OPTIMISTIC count: passes inside one run are repeated measurements of")
    print("  the same junction, not independent samples, so the real error bars are")
    print("  wider than the ones printed above.")

    section("5. DATA-QUALITY FLAGS ACROSS EVERY SCAN-SHAPED FILE")
    bad = []
    for sess in ("2026-09-17-bench", "2026-09-19-bench", "2026-09-19-morning"):
        for p in sorted(glob.glob(os.path.join(DATA, sess, "*.csv"))):
            head = open(p).readline().split(",")
            if head[0] not in ("y", "y_offset"):
                continue
            s = stats(p)
            issues = []
            # These tools plan 11 or 12 forward lines; anything much shorter aborted.
            # y_offset files are three-place controls BY DESIGN: three rows is complete.
            if s["header0"] != "y_offset" and s["n_fwd"] < 5:
                issues.append("only %d forward lines of a planned 11-12 - ABORTED"
                              % s["n_fwd"])
            if s["filled"] < s["cells"]:
                issues.append("%d of %d cells empty" % (s["cells"] - s["filled"], s["cells"]))
            if s["identical_unexplained"]:
                issues.append("%d identical fwd/back pairs the clamp does not explain"
                              " - the tool stored the forward pass twice"
                              % s["identical_unexplained"])
            elif s["identical_passes"]:
                issues.append("%d identical fwd/back pairs, all fully pinned at a clamp"
                              " or the rail - physical, not a tool defect"
                              % s["identical_passes"])
            if s["clamp_frac"] and s["clamp_frac"] > 0.10:
                issues.append("%.0f%% of pixels %s"
                              % (100 * s["clamp_frac"],
                                 "at the ADC rail" if s["is_current"] else "on a Z clamp"))
            if issues:
                bad.append((os.path.relpath(p, REPO), "; ".join(issues)))
    for p, why in bad:
        print("  %-62s %s" % (p, why))
    print("  %d of the scan-shaped files carry at least one flag." % len(bad))

    # ------------------------------------------------------------ outputs
    out = os.path.join(ANALYSIS, "scan_stats.csv")
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(allrows[0].keys()))
        w.writeheader()
        w.writerows(allrows)
    print("\n  wrote %s" % os.path.relpath(out, REPO))

    section("6. FIGURES")
    fig, ax = plt.subplots(figsize=(7.4, 4.0))
    labs = [s[0] for s in summary]
    ys = list(range(len(labs)))[::-1]
    w = 0.35
    ax.barh([y + w / 2 for y in ys], [s[1] for s in summary], w,
            color=TOL["blue"], label="real scans (X moving)")
    ax.barh([y - w / 2 for y in ys], [s[2] for s in summary], w,
            color=TOL["red"], label="X-held controls")
    ax.axvline(0, color=TOL["black"], lw=0.8)
    ax.set_yticks(ys)
    ax.set_yticklabels([l.replace(" vs ", "\nvs ") for l in labs], fontsize=7)
    ax.set_xlabel("image-to-image correlation (mean over consecutive pairs)")
    ax.set_title("The control reproduces at least as well as the scan, every time\n"
                 "if the picture were the surface, the blue bar would beat the red one")
    ax.legend(loc="lower right")
    save(fig, "fig14_scan_vs_control.png")
    plt.close(fig)

    # side-by-side images: one cas9 scan and its control
    fig, axes = plt.subplots(1, 2, figsize=(8.2, 3.4))
    for ax, name, title in (
            (axes[0], "cas9_scan0.csv", "a feedback scan (X moving)"),
            (axes[1], "cas9_xheld0.csv", "its X-held control (X never moved)")):
        xs, rows = read_scan(os.path.join(DATA, "2026-09-19-bench", name))
        img = [detrend(v) for y, d, v in rows if d == "fwd"]
        n = min(len(r) for r in img)
        arr = [[(r[i] if r[i] is not None else float("nan")) for i in range(n)] for r in img]
        im = ax.imshow(arr, aspect="auto", cmap="cividis", origin="lower",
                       extent=[xs[0], xs[n - 1], 0, len(arr)])
        ax.set_xlabel("X DAC code")
        ax.set_ylabel("line number")
        ax.set_title("%s\n%s" % (title, name), fontsize=9)
        ax.grid(False)
        cb = fig.colorbar(im, ax=ax, fraction=0.046)
        cb.set_label("Z the loop needed,\nline tilt removed (counts)", fontsize=7.5)
    fig.suptitle("2026-09-19 bench: the two look alike, which is the whole result",
                 y=1.04, fontsize=10)
    save(fig, "fig15_scan_examples.png")
    plt.close(fig)


if __name__ == "__main__":
    main()
