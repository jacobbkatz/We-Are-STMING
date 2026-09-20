"""Figure 10 - the 2026-09-17 junction: pushing in and pulling out are not mirror images.

    python3 deliverables/2026-09-19-pause/figures/code/fig10_push_pull.py

WHY THIS TEST MATTERS MORE THAN THE OTHERS. Nearly every argument about whether this
instrument was tunnelling runs through a distance we have never measured - how far the
tip moves per Z count. This one does not. It compares the junction against ITSELF: move
Z a fixed amount toward the sample, then the same amount away, and ask whether the
current answers the same way both times.

A VACUUM GAP IS SYMMETRIC. Current through a tunnel gap depends on the width of the gap
and nothing else, so closing by X and opening by X change the current by the same factor
in opposite directions. Whatever the distance scale is, the two have to match. They did
not: pulling away gave most of what was predicted, pushing in gave about a fifth of it.
Something was taking up the push - a surface deforming, not a vacuum closing.

SOURCE. `sessions/2026-09-17-bench.md` section 3.25, measured 2026-09-17 with averaged
ADC reads. THE NUMBERS ARE FROM THE SESSION LOG, NOT FROM A RAW FILE: this sweep was run
interactively at the bench and its raw output was never written to `sessions/data/`. It
is the only figure in this set that cannot be recomputed from a CSV, and that is why it
is said here rather than buried in a caption.

The "predicted" column is the log's own: the 250 Z counts per decade measured minutes
earlier in the same settled state (section 3.19), applied to each step.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stmstyle as S  # noqa: E402

# sessions/2026-09-17-bench.md section 3.25, verbatim.
# (Z step in counts, decades predicted at 250 counts/decade, decades measured)
STEPS = [
    (+400, +1.60, +0.36),
    (+200, +0.80, +0.22),
    (-200, -0.80, -0.32),
    (-400, -1.60, -1.13),
]


def main():
    S.set_theme("light")
    fig, ax = S.make_fig(width=10.6, height=6.7)
    fig.subplots_adjust(top=0.790, bottom=0.315, left=0.225, right=0.985)

    ys = list(range(len(STEPS)))[::-1]
    h = 0.32
    pred_c, meas_c = S.series(4), S.series(1)   # magenta = predicted, orange = measured

    for y, (step, pred, meas) in zip(ys, STEPS):
        ax.barh(y + h * 0.58, pred, height=h, color=pred_c, alpha=0.30,
                edgecolor=pred_c, linewidth=1.0, zorder=3)
        ax.barh(y - h * 0.58, meas, height=h, color=meas_c, zorder=4)
        frac = abs(meas / pred)
        right = meas > 0
        S.key(ax, meas + (0.08 if right else -0.08), y - h * 0.58,
              "%.0f%% of it arrived" % (frac * 100),
              ha="left" if right else "right", va="center")

    ax.axvline(0, color=S.C["axis"], linewidth=1.0, zorder=2)
    ax.set_yticks(ys)
    ax.set_yticklabels(["Z +400  (toward the sample)", "Z +200  (toward)",
                        "Z −200  (away)", "Z −400  (away)"])
    ax.set_xlim(-2.60, 4.25)
    ax.set_xticks([-2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5])
    ax.set_ylim(-0.75, 3.75)
    S.tidy(ax, xlabel="Change in current, in decades   (one decade = ten times more current)",
           grid="x")

    # The two halves of the result, said inside the plot rather than in a caption.
    ax.axhspan(1.52, 3.75, color=S.C["band"], zorder=0)
    # Anchored to the right of the bars, in a column the axis is widened to make.
    # At the 2026-09-20 type scale the old column was sixteen characters across.
    S.note(ax, 4.18, 3.55, "PUSHING IN\nbarely moved the current.\nAbout a quarter of the\npush reached the junction.",
           ha="right", va="top", fontweight=S.W_EMPH, color=S.word(1))
    S.note(ax, 4.18, 1.35, "PULLING AWAY\nbehaved much more like a gap —\nand at the larger step gave 3.1x\nmore than the same push did.",
           ha="right", va="top", fontweight=S.W_EMPH, color=S.word(0))

    S.titles_keyed(
        fig,
        "A vacuum gap answers the same way in both directions. Ours did not.",
        "Same junction, same minute: <what a tunnelling gap predicts> against <what we measured>.\n"
        "Pushing in returned 23-28% of the predicted change; pulling away returned 40-71%. A vacuum gap\n"
        "cannot tell the two apart, whatever the distance scale is. A surface being squashed can.",
        [{"color": S.word(4), "fontweight": S.W_EMPH},
         {"color": S.word(1), "fontweight": S.W_EMPH}])

    S.footer(fig, y=0.008, text=
             "Source: sessions/2026-09-17-bench.md section 3.25, measured 2026-09-17 with averaged ADC reads on "
             "the 2026-09-17 tip and the gold-on-copper-tape sample.\n"
             "The prediction is the log's own: 250 Z counts per decade, measured minutes earlier in the same "
             "settled state (section 3.19), applied to each step. THIS SWEEP WAS RUN INTERACTIVELY AT THE BENCH "
             "AND ITS RAW OUTPUT WAS NEVER SAVED,\nso unlike every other figure in this set it cannot be "
             "recomputed from a file in sessions/data/. It is reproduced here exactly as the log records it.\n"
             "WHAT THIS DOES NOT SHOW: it does not measure a distance, and it does not need one - that is the "
             "point of it. It does not rule out a tunnelling gap being shorted intermittently by something "
             "softer; it rules out a clean vacuum gap.")

    S.save(fig, "fig10_push_pull")


if __name__ == "__main__":
    main()
