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
import re
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


def image_to_image(group, res, drop_first=0, full_only=True):
    """Correlation of each consecutive pair of detrended forward images.

    THE DEFECT THIS GUARDS AGAINST. The project's own analyze_scans.py truncates each
    pair to the shorter file with no shape check (its lines 50-51). Where one file of a
    pair ABORTED after a line or two, the resulting 'image-to-image correlation' is
    computed over 21 or 42 pixels - one or two lines - while a pair of complete images is
    computed over 231. Those are not the same statistic, and the short one is dominated by
    the first line, which is the one line guaranteed to agree because it carries the
    loop's settling transient (see the drop-line check below).

    full_only=True therefore DROPS any file with fewer than the modal number of forward
    lines for its group before pairing, so every correlation is over complete images.
    full_only=False reproduces the published, truncating behaviour for comparison.

    Returns (correlations, notes) where notes names any pair that was dropped or truncated.
    """
    flats = [(g, res[g]["n_fwd"] if drop_first == 0 else res[g]["n_fwd"] - drop_first,
              res[g]["flat"] if drop_first == 0 else flat_of(g, drop_first))
             for g in group]
    notes = []
    if full_only and flats:
        modal = max(n for _, n, _ in flats)
        short = [(g, n) for g, n, _ in flats if n < modal]
        for g, n in short:
            notes.append("%s dropped: %d forward line(s) of %d"
                         % (os.path.basename(g), n, modal))
        flats = [f for f in flats if f[1] >= modal]
    out = []
    for (ga, na, fa), (gb, nb, fb) in zip(flats, flats[1:]):
        n = min(len(fa), len(fb))
        if n < 6:
            continue
        if not full_only and na != nb:
            notes.append("%s vs %s TRUNCATED to %d line(s)"
                         % (os.path.basename(ga), os.path.basename(gb), n // 21))
        c = pearson(fa[:n], fb[:n])
        if c is not None:
            out.append(c)
    return out, notes


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
        # FULL IMAGES ONLY is the headline; the truncating version is printed beside it
        # so the difference is visible rather than silently corrected.
        i2i_s, note_s = image_to_image(sc, res)
        i2i_c, note_c = image_to_image(ct, res)
        pub_s, tn_s = image_to_image(sc, res, full_only=False)
        pub_c, tn_c = image_to_image(ct, res, full_only=False)
        for role, vals, notes, pub, tn in (("scans", i2i_s, note_s, pub_s, tn_s),
                                           ("CONTROLS", i2i_c, note_c, pub_c, tn_c)):
            if not pub:
                continue
            truncated = bool(notes or tn)
            if vals:
                print("    image-to-image, %-8s: %s  (mean %+.3f, n = %d pair%s, "
                      "COMPLETE IMAGES ONLY)"
                      % (role, " ".join("%+.2f" % c for c in vals), st.mean(vals),
                         len(vals), "" if len(vals) == 1 else "s"))
            else:
                print("    image-to-image, %-8s: **NO PAIR OF COMPLETE IMAGES EXISTS** - "
                      "only one of them ran to the end" % role)
            if truncated:
                print("      as published (truncating to the shorter file): %s "
                      "(mean %+.3f, n = %d)"
                      % (" ".join("%+.2f" % c for c in pub), st.mean(pub), len(pub)))
                for nt in (tn or notes):
                    print("        %s" % nt)
                print("        ^ the truncated pairs are computed over one or two LINES,")
                print("          not a whole image, and the first line is the one that is")
                print("          guaranteed to agree. They are not the same statistic.")
            if vals:
                # standard error of r, optimistic: it treats the 21 pixels of a line as
                # independent, which the Z ramp along a line makes false.
                npix = min(len(res[g]["flat"]) for g in (sc if role == "scans" else ct)
                           if res[g]["n_fwd"] >= max(res[h]["n_fwd"]
                                                     for h in (sc if role == "scans" else ct)))
                print("      optimistic s.e. of each r at n = %d pixels: %.3f"
                      % (npix, 1.0 / math.sqrt(npix - 3)))
        if i2i_s:
            # The first-line trap, documented in sessions/2026-09-17-bench.md 3.22: the
            # loop's settling transient on line 1 is identical in every image because the
            # procedure is identical, and it alone can carry the whole correlation.
            d1, _ = image_to_image(sc, res, 1)
            d2, _ = image_to_image(sc, res, 2)
            if d1 and d2:
                print("      scans, drop line 1: mean %+.2f    drop lines 1-2: mean %+.2f%s"
                      % (st.mean(d1), st.mean(d2),
                         "   <- the agreement was the loop settling, not the sample"
                         if st.mean(i2i_s) - st.mean(d2) > 0.3 else ""))
        if i2i_c:
            d1, _ = image_to_image(ct, res, 1)
            d2, _ = image_to_image(ct, res, 2)
            if d1 and d2:
                print("      controls, drop line 1: mean %+.2f    drop lines 1-2: mean %+.2f"
                      % (st.mean(d1), st.mean(d2)))
        if not (i2i_s and i2i_c) and (pub_s and pub_c):
            print("    VERDICT: NO COMPARISON IS POSSIBLE between complete images in this")
            print("             group. The figures once published for it came entirely")
            print("             from truncated pairs.")
        if i2i_s and i2i_c:
            se = 1.0 / math.sqrt(231 - 3)  # optimistic: pixels along a line are not independent
            gap = st.mean(i2i_s) - st.mean(i2i_c)
            if abs(gap) < 2 * se:
                verdict = ("NEITHER REPRODUCES: scans %+.3f, controls %+.3f, "
                           "difference %+.3f against an optimistic s.e. of %.3f - "
                           "indistinguishable, and neither differs from zero"
                           % (st.mean(i2i_s), st.mean(i2i_c), gap, se))
            elif gap < 0:
                verdict = "the controls reproduce better than the scans"
            else:
                verdict = "scans reproduce better - worth a second look"
            print("    VERDICT: %s" % verdict)
            summary.append((title, st.mean(i2i_s), st.mean(i2i_c), len(i2i_s), len(i2i_c),
                            st.mean([s["corrugation"] for p, s in res.items()
                                     if p in sc and s["corrugation"]]),
                            st.mean([s["corrugation"] for p, s in res.items()
                                     if p in ct and s["corrugation"]])))

    section("1b. THE TRUNCATION DEFECT - A CLASS, NOT AN INSTANCE")
    print("  sessions/data/2026-09-19-bench/scripts/analyze_scans.py lines 50-51 truncate")
    print("  each image pair to the shorter file with NO SHAPE CHECK. Where one file of a")
    print("  pair aborted, the resulting 'image-to-image correlation' is computed over one")
    print("  or two LINES while a complete pair is computed over eleven.")
    print()
    print("  I found this in the wide images first and DID NOT SWEEP THE CLASS. It is in")
    print("  four groups, on both the scan side and the control side:")
    print()
    print("  %-52s %-9s %s" % ("group [role]", "pairs hit", "which"))
    n_affected = 0
    for title, sess, scans, ctrls in GROUPS:
        for role, names in (("scan", scans), ("control", ctrls)):
            paths = [os.path.join(DATA, sess, n) for n in names
                     if os.path.exists(os.path.join(DATA, sess, n))]
            if len(paths) < 2:
                continue
            nf = [(os.path.basename(p_), stats(p_)["n_fwd"]) for p_ in paths]
            modal = max(n for _, n in nf)
            bad = [(a, b, min(na, nb)) for (a, na), (b, nb) in zip(nf, nf[1:])
                   if min(na, nb) < modal]
            if bad:
                n_affected += 1
                print("  %-52s %-9d %s"
                      % ((title[:44] + " [" + role + "]"), len(bad),
                         "; ".join("%s/%s -> %d of %d lines" % (a, b, m, modal)
                                   for a, b, m in bad)))
    print()
    print("  GROUPS AFFECTED: %d. Every image-to-image figure above is therefore computed"
          % n_affected)
    print("  over COMPLETE IMAGES ONLY, with the truncating version printed beside it.")
    print()
    print("  WHAT IT CHANGES, and it changes one published conclusion:")
    print("    cas9 controls, as published (truncating): +0.20 +0.21 +0.70, mean +0.37")
    print("    cas9 controls, complete images only     : +0.20 -0.06,       mean +0.07")
    print("    cas9 scans (all complete, unaffected)   : +0.09 +0.18 -0.15, mean +0.04")
    print("  cas9_xheld2.csv is a SINGLE LINE - one y value, fwd and back - where the")
    print("  other seven carry eleven, so two of the three control correlations were 21")
    print("  points instead of 231.")
    print()
    print("  'THE CONTROLS REPRODUCE BETTER' IS WITHDRAWN. The correct statement is that")
    print("  NEITHER the scans NOR the controls reproduce: +0.04 against +0.07, a")
    print("  difference of -0.03 against an optimistic standard error of 0.066, and")
    print("  neither differs from zero. The scans show no more reproducible structure")
    print("  than a control in which the tip never moved across the surface.")
    print("  THE IMAGING CONCLUSION IS UNCHANGED and needs no rescuing: the real scans do")
    print("  not reproduce, and that carries it on its own.")
    print()
    print("  For the wide images and the tuned scans the honest answer is stronger still:")
    print("  only ONE image in each group ran to the end, so there is NO pair of complete")
    print("  images to compare at all. The +0.71 once quoted for the wide scans came")
    print("  entirely from a single shared line - and the first line is the one guaranteed")
    print("  to agree, because it carries the loop's settling transient")
    print("  (sessions/2026-09-17-bench.md 3.22; the drop-line check below reproduces it).")
    print()
    print("  The wide scans also have trace/retrace of -0.94, -0.91 and -0.75 against")
    print("  +0.14 and +0.13 in their controls. A surface is traced the same way in both")
    print("  directions and gives a POSITIVE trace/retrace; a negative one is the loop")
    print("  hunting (sessions/2026-09-19-morning.md 6).")
    print()
    print("  NOT AVAILABLE: there is no .log file for the img_scan / img_xheld runs, so")
    print("  the 'saturated 14.5 per cent' figure in the session log came from console")
    print("  output that was not saved and cannot be checked here. cas9.log DOES carry the")
    print("  loop's own saturated and clamped counters for every run.")

    section("1c. THE ONSET Z OF EVERY THREE-Y RUN - a measurement sitting unused")
    print("  The first line of each ycontrol_run*.log records the Z at which the loop")
    print("  found the surface before that run started. Nobody has used it. It is a")
    print("  direct measurement of where the gap was at five moments inside one five-")
    print("  minute window, and it is the only such series in the repository.")
    print()
    onsets = []
    for name, what in (("ycontrol_run1.log", "run 1, +-3000 Y, scanning"),
                       ("ycontrol_xheld_run1.log", "X-held control, +-3000 Y"),
                       ("ycontrol_run2.log", "run 2, +-12000 Y, scanning"),
                       ("ycontrol_run3.log", "run 3, +-12000 Y, X HELD"),
                       ("ycontrol_run4.log", "run 4, +-12000 Y, REPEAT of run 2")):
        head = open(os.path.join(DATA, "2026-09-19-bench", name)).readline()
        m = re.search(r"onset Z=(\d+)", head)
        z = int(m.group(1)) if m else None
        onsets.append((name, what, z))
        print("    %-26s %-34s onset Z = %s" % (name, what, z))
    zs = [z for _, _, z in onsets if z is not None]
    print()
    print("  Spread across all five: %d counts (%d to %d)."
          % (max(zs) - min(zs), min(zs), max(zs)))
    z2 = next(z for n, _, z in onsets if n == "ycontrol_run2.log")
    z4 = next(z for n, _, z in onsets if n == "ycontrol_run4.log")
    print("  BETWEEN RUN 2 AND ITS REPEAT, RUN 4: %+d counts." % (z4 - z2))
    print("  That is %.1f%% of the 65,536-count Z range and %.1f%% of the 48,000-count"
          % (100.0 * abs(z4 - z2) / 65536, 100.0 * abs(z4 - z2) / 48000))
    print("  window the loop was given for these runs (12,000 to 60,000).")
    print()
    print("  WHY IT MATTERS, AND IT DOES NOT GO THE WAY THIS PROJECT ASSUMED.")
    print("  The standing explanation for run 2 not reproducing in run 4 is that the")
    print("  surface moved out from under the scanner. Across exactly that interval the")
    print("  gap moved 2,200 counts - a few per cent of the range, not most of it. So")
    print("  'the surface moved' is a POORER explanation for the non-reproduction than it")
    print("  looked. This WEAKENS the candidate rather than rescuing it.")
    print()
    print("  IT DOES NOT CLOSE IT. Onset Z measures the GAP, not LATERAL position. A")
    print("  sideways drift would carry the tip to a different patch of gold while barely")
    print("  changing the Z at which it finds the surface. LATERAL DRIFT HAS NEVER BEEN")
    print("  MEASURED IN THIS PROJECT.")
    print()
    print("  TIMING, and it is weaker than any of these numbers. NEITHER ycontrol LOG")
    print("  CARRIES A TIMESTAMP. sessions/2026-09-19-bench.md is chronological: section")
    print("  3.14 is timestamped 03:48 and section 3.16 is timestamped 03:53, and section")
    print("  3.15 - all five three-Y runs - sits between them. So ALL FIVE fit inside")
    print("  about five minutes. The interval between any two of them is NOT RECORDED.")
    print("  An earlier version of this analysis said 'nine minutes' between runs 2 and 4")
    print("  and another said 'half an hour'; both were guesses and both were too long.")
    print()
    dt_max = 5 * 60.0
    print("  The most that can be said about the rate: 2,200 counts over an interval of at")
    print("  most %d s, so a mean of AT LEAST %.0f counts/s. Compare the Z-test onset"
          % (dt_max, abs(z4 - z2) / dt_max))
    print("  drifts of -74 to +83 counts/s and the release-watch's >= 7,400 counts/s.")

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
    print("  Compare these with section 1. The cas9 trace/retrace and corrugation figures")
    print("  reproduce exactly. The cas9 CONTROL image-to-image figure does NOT, and")
    print("  section 1b says why: two of its three pairs were truncated to one line.")

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
    se = 1.0 / math.sqrt(231 - 3)
    fig, ax = plt.subplots(figsize=(7.2, 2.9))
    pts = []
    for s_ in summary:
        pts.append(("real scans\n(X moving across the surface)", s_[1], s_[3], TOL["blue"]))
        pts.append(("X-held control\n(the tip never moved across it)", s_[2], s_[4],
                    TOL["red"]))
    ys = [1, 0]
    for (lab, v, n, col), y in zip(pts, ys):
        ax.errorbar([v], [y], xerr=[se], fmt="o", ms=8, color=col,
                    ecolor=col, elinewidth=2.0, capsize=5)
        ax.text(v, y + 0.22, "%+.3f   n = %d pairs" % (v, n), ha="center", fontsize=8.5,
                color=col)
    ax.axvline(0, color=TOL["black"], lw=1.0)
    ax.text(0, -0.55, "zero: no repeatable structure at all", ha="center", fontsize=7.5)
    ax.set_yticks(ys)
    ax.set_yticklabels([pts[0][0], pts[1][0]], fontsize=8)
    ax.set_ylim(-0.75, 1.55)
    ax.set_xlim(-0.30, 0.45)
    ax.set_xlabel("image-to-image correlation, complete images only\n"
                  "bars are $\\pm$1 standard error (%.2f), and that error is optimistic"
                  % se)
    ax.set_title("2026-09-19 bench, the four feedback scans and their four controls\n"
                 "neither reproduces, and they are indistinguishable from each other")
    save(fig, "fig14_scan_vs_control.png")
    plt.close(fig)

    # A second panel for the class of defect, since it is the finding that changed a
    # published number.
    fig, ax = plt.subplots(figsize=(7.6, 3.0))
    groups = ["cas9 controls", "wide images, scans", "tuned scans, scans",
              "tuned scans, controls"]
    published = [0.373, 0.708, -0.246, 0.034]
    corrected = [0.068, None, None, None]
    ys2 = list(range(len(groups)))[::-1]
    ax.barh(ys2, published, 0.5, color=TOL["grey"], label="as published (pairs truncated)")
    for y, g, pv, cv in zip(ys2, groups, published, corrected):
        ax.text(-0.52, y, "%+.2f" % pv, va="center", ha="right", fontsize=8)
        if cv is None:
            ax.text(0.95, y, "NO pair of complete images exists", va="center",
                    fontsize=7.5, color=TOL["purple"])
        else:
            ax.plot([cv], [y], "o", ms=8, color=TOL["blue"], zorder=3)
            ax.text(0.95, y, "complete images only: %+.2f" % cv, va="center",
                    fontsize=7.5, color=TOL["blue"])
    ax.axvline(0, color=TOL["black"], lw=0.9)
    ax.set_yticks(ys2)
    ax.set_yticklabels(groups, fontsize=8)
    ax.set_xlim(-0.75, 1.95)
    ax.set_xlabel("image-to-image correlation")
    ax.set_title("The truncation defect is a class, in four groups\n"
                 "a pair is silently cut to the shorter file, so one aborted image\n"
                 "turns an image comparison into a single line")
    ax.legend(loc="lower right", bbox_to_anchor=(1.0, -0.02))
    save(fig, "fig18_truncation_class.png")
    plt.close(fig)

    # side-by-side images: one cas9 scan and its control, ON ONE SHARED COLOUR SCALE,
    # because separate scales would make two different things look alike or unalike for
    # no physical reason.
    panels = [("cas9_scan0.csv", "a feedback scan (X moving)"),
              ("cas9_xheld0.csv", "its X-held control (X never moved)")]
    arrs, xss = [], []
    for name, _ in panels:
        xs, rows = read_scan(os.path.join(DATA, "2026-09-19-bench", name))
        img = [detrend(v) for y, d, v in rows if d == "fwd"]
        n = min(len(r) for r in img)
        arrs.append([[(r[i_] if r[i_] is not None else float("nan"))
                      for i_ in range(n)] for r in img])
        xss.append(xs[:n])
    lim = max(max(abs(v) for row in a for v in row) for a in arrs)
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.4))
    for ax, a, xs, (name, title) in zip(axes, arrs, xss, panels):
        im = ax.imshow(a, aspect="auto", cmap="cividis", origin="lower",
                       vmin=-lim, vmax=lim,
                       extent=[xs[0], xs[-1], 0, len(a)])
        ax.set_xlabel("X DAC code")
        ax.set_title("%s\n%s" % (title, name), fontsize=9)
        ax.grid(False)
    axes[0].set_ylabel("line number")
    cb = fig.colorbar(im, ax=axes, fraction=0.035, pad=0.02)
    cb.set_label("Z the loop needed, line tilt removed (counts)\n"
                 "both panels on the same scale", fontsize=8)
    fig.suptitle("2026-09-19 bench: the two look alike, which is the whole result",
                 y=1.02, fontsize=10)
    save(fig, "fig15_scan_examples.png")
    plt.close(fig)


if __name__ == "__main__":
    main()
