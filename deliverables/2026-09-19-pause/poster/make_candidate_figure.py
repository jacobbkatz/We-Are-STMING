#!/usr/bin/env python3
"""The poster's candidate-image figure: the three-Y run, its repeat, and its control.

    python3 deliverables/2026-09-19-pause/poster/make_candidate_figure.py

WHY THIS SCRIPT EXISTS, and it is worth reading before changing anything.

Jacob asked for the candidate image to go on the poster. The gallery already has a
picture of it - `../candidates/gallery/03_candidateB_three_y.png` - but it cannot be
used on the poster as it stands, for two reasons and neither is cosmetic:

  1. Its heading calls run 2 "the 3.9 sigma run". That sigma was withdrawn at the
     2026-09-19 pause point: it treated 45 within-place and 108 between-place pairwise
     correlations as independent when every pass appears in many of them. The honest
     figure is the permutation p, and it is p = 0.0036 (`../candidates/VERDICT.md` 4).
  2. Its heading says the runs are "~2 min" apart. `../LEAD_VERIFICATION.md` V9 and V5b
     correct that: NEITHER ycontrol log carries a timestamp, so the interval between
     any two of them is UNKNOWN, bounded only by the ~5 minutes between the two
     timestamped sections that surround them. "Two minutes" was an inference.

So this script re-draws the same measurement, from the same raw files, in the figure
set's own house style, with the corrected statements. NOTHING about the data is
changed: same files, same detrending convention, same three places.

WHAT IS PLOTTED. One panel per run. Each pass has its own straight line in X removed -
the project's own convention (`Code/pc/stm_y_control.py`), because a fixed tip-to-sample
tilt otherwise dominates everything - and the six passes at each of the three places are
averaged into one thick line. The thin lines behind are the individual passes, so the
scatter the average came out of is visible rather than hidden.

WHAT IS NOT CLAIMED. This is not an image and the figure says so. Both axes are in DAC
counts, because this instrument has never established a distance scale from its own
hardware. No scale bar appears, here or anywhere else in this set.
"""
from __future__ import annotations

import csv
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PAUSE = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(PAUSE))
sys.path.insert(0, os.path.join(PAUSE, "figures", "code"))
import stmstyle as S  # noqa: E402

DATA = os.path.join(REPO, "sessions", "data", "2026-09-19-bench")
OUT = os.path.join(HERE, "assets")

# The three runs, in the order a reader should meet them: the positive, its repeat,
# and the control that cannot contain a surface at all.
RUNS = [
    ("ycontrol_run2_ysep12000.csv",
     "RUN 2 - the one that looked like a surface",
     "within-place +0.239, between-place -0.135\ndifference +0.374, permutation p = 0.0036"),
    ("ycontrol_run4_ysep12000_repeat.csv",
     "RUN 4 - the same three places again, minutes later",
     "difference +0.059, permutation p = 0.26\nit did not repeat"),
    ("ycontrol_run3_ysep12000_xheld.csv",
     "RUN 3 - the X-HELD CONTROL, X never moved",
     "difference +0.226, permutation p = 0.020\nwith nothing there to see"),
]


def load(path):
    """(xs, places, {place: (npasses, npix)}) from a y_offset,pass,... file."""
    with open(path) as fh:
        rows = [r for r in csv.reader(fh) if r]
    xs = np.array([int(v) for v in rows[0][2:]], dtype=float)
    P = {}
    for r in rows[1:]:
        P.setdefault(int(r[0]), []).append([float(v) for v in r[2:]])
    return xs, sorted(P), {k: np.array(v) for k, v in P.items()}


def detrend(a):
    """Subtract the least-squares straight line - the project's own convention."""
    a = np.asarray(a, dtype=float)
    t = np.arange(len(a), dtype=float)
    m, c = np.polyfit(t, a, 1)
    return a - (m * t + c)


def clear_the_header(fig, gap_in=0.22):
    """Drop the three panels until the title block stops running through them.

    THE SAME PROBLEM `stmstyle.fit_footer` SOLVES, at the other end of the figure.
    The title and subtitle are placed as fractions of the figure height, and the axes
    start at another fraction (`top=` in the subplots_adjust below). Both were tuned by
    hand against one type size. When the figure set's type went up about a quarter on
    2026-09-20 for poster legibility, the subtitle's second line grew down into the
    three panel titles - "RUN 2 - the one that looked like a surface" and its
    neighbors - and printed straight through them.

    So this asks the renderer where the title block really ends and where the panels
    really begin (tight boxes, so each panel's own title counts), and slides every
    panel down far enough to leave `gap_in` inches of clear paper between them.
    `fit_footer`, called afterwards, then adds paper at the bottom for the footer, so
    nothing is squeezed. There is no number here to re-tune next time.
    """
    foot = getattr(fig, "_stm_footer", None)
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    header = [t.get_window_extent(r).y0 for t in fig.texts if t is not foot]
    panels = [ax.get_tightbbox(r).y1 for ax in fig.axes
              if ax.get_tightbbox(r) is not None]
    if not header or not panels:
        return 0.0
    overlap = max(panels) - (min(header) - gap_in * fig.dpi)
    if overlap <= 1.0:
        return 0.0
    drop = overlap / fig.bbox.height          # pixels -> figure fraction
    for ax in fig.axes:
        p = ax.get_position()
        ax.set_position([p.x0, p.y0 - drop, p.width, p.height])
    return overlap / fig.dpi


def main():
    os.makedirs(OUT, exist_ok=True)
    fig, axes = S.plt.subplots(1, 3, figsize=(13.6, 5.9))

    # One y range for all three panels: the control is genuinely smaller than the
    # other two, and squeezing it to fill its own axes would hide exactly that.
    lo, hi = -800, 800

    for ax, (name, head, stat) in zip(axes, RUNS):
        xs, places, P = load(os.path.join(DATA, name))
        for i, p in enumerate(places):
            M = np.array([detrend(v) for v in P[p]])
            for v in M:                                   # the individual passes
                ax.plot(xs, v, color=S.series(i), lw=0.9, alpha=0.30, zorder=2)
            ax.plot(xs, M.mean(axis=0), color=S.series(i), lw=2.6, zorder=3,
                    solid_capstyle="round")
        ax.axhline(0, color=S.C["axis"], lw=0.8, zorder=1)
        ax.set_ylim(lo, hi)
        ax.set_title(head + "\n" + stat, fontsize=S.TYPE["annot"],
                     fontweight=S.W_EMPH, linespacing=1.6)
        ax.set_xlabel("X piezo counts")
        # FOUR TICKS AT MOST, not six. Three panels share a 13.6 in figure, so each
        # x axis is about 4.3 in wide. At the type size the figure set moved to on
        # 2026-09-20 six labels of the form "20,000" touch each other and read as one
        # run of digits. Thinning the ticks is the fix that keeps the labels in full;
        # shrinking the type back would undo the legibility the raise was for.
        ax.xaxis.set_major_locator(S.plt.MaxNLocator(nbins=4, steps=[1, 2, 5, 10]))
        ax.xaxis.set_major_formatter(
            S.plt.FuncFormatter(lambda v, _: format(int(v), ",")))
    axes[0].set_ylabel("Z counts, each pass detrended")

    S.titles_keyed(
        fig,
        "The one measurement that still looks like a surface - and why it stays an open question",
        "Six passes of one line, at three places 12,000 Y counts apart: "
        "<Y -12,000>, <Y 0>, <Y +12,000>. Thick lines are each place's six-pass average;\n"
        "thin lines are the passes themselves. Reading a surface, passes at one place would "
        "agree with each other and differ from the other two places.",
        [{"color": S.word(0), "fontweight": S.W_EMPH},
         {"color": S.word(1), "fontweight": S.W_EMPH},
         {"color": S.word(2), "fontweight": S.W_EMPH}],
        y=0.988, gap=0.055)

    S.footer(fig,
             "Source: sessions/data/2026-09-19-bench/ycontrol_run2_ysep12000.csv, "
             "ycontrol_run4_ysep12000_repeat.csv, ycontrol_run3_ysep12000_xheld.csv.\n"
             "Measured 2026-09-19 between 03:48 and 03:53 UTC; sessions/2026-09-19-bench.md 3.15. "
             "Each pass detrended in X, the project's own convention (Code/pc/stm_y_control.py). "
             "Every file is 3 places x 6 passes x 21 points - no truncation.\n"
             "THE STATISTICS ARE PERMUTATION TESTS, not the 3.9 sigma reported on the night: that "
             "sigma treated overlapping pairs as independent, and was withdrawn at the\n"
             "2026-09-19 pause point (candidates/VERDICT.md 4). WHAT THIS DOES NOT SHOW: it is not "
             "an image and it is not evidence of one. Across 209 reproducibility tests on this\n"
             "data the honest threshold is p < 2.4e-4 - run 2 falls a factor of 14 short of it. "
             "Neither log carries a timestamp, so the interval between runs is UNKNOWN, bounded\n"
             "by the ~5 minutes between the sections around them (LEAD_VERIFICATION.md V9). Axes "
             "are in DAC counts: this instrument has never established a distance scale.",
             y=0.008)

    fig.subplots_adjust(left=0.058, right=0.995, top=0.700, bottom=0.320, wspace=0.18)

    # MEASURE THE FOOTER, DO NOT GUESS AT IT. `bottom=0.320` above only leaves enough
    # room under the axes for one particular type size, and on 2026-09-20 the figure
    # set's type was raised about a quarter for poster legibility. Re-running this
    # script after that put six lines of footer straight through the x-axis tick
    # labels and the words "X piezo counts" on all three panels.
    #
    # These are the figure set's own two helpers, the same pair `stmstyle.save()`
    # calls for every other figure, so this figure now behaves like the rest:
    #   narrow_footer  re-wraps the footer to the width of the chart, so the chart is
    #                  not shrunk to pay for the footer's long lines;
    #   fit_footer     asks the renderer where the footer really ends and where the
    #                  axes really begin, and adds paper at the bottom if they meet.
    # Nothing is hand-tuned, so the next type change cannot break it again.
    moved = clear_the_header(fig)
    if moved:
        print("  dropped the panels %.2f in to clear the title block" % moved)
    S.narrow_footer(fig)
    S.fit_footer(fig)

    for path, dpi in ((os.path.join(OUT, "fig10_candidate.png"), 300),):
        # Same write settings as stmstyle.save(), so this figure sits on the poster
        # at the same scale and with the same margin as fig01-fig09 beside it.
        fig.savefig(path, dpi=dpi, facecolor=S.C["surface"],
                    bbox_inches="tight", pad_inches=0.32)
        im_w = fig.get_size_inches()[0]
        print("  wrote %s  (%.1f in wide at 300 dpi)" % (os.path.relpath(path, REPO), im_w))
    S.plt.close(fig)


if __name__ == "__main__":
    main()
