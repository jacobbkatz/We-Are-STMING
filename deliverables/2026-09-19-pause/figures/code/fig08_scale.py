"""Figure 8 - how small these quantities are, and which of them we can put a number on.

    python3 deliverables/2026-09-19-pause/figures/code/fig08_scale.py

Two ladders, both logarithmic. The left one is CURRENT, where this project has real
measured numbers. The right one is LENGTH, where it does not - and saying so plainly is
the point of that half of the figure.

EVERY MARKER CARRIES ITS PROVENANCE, in the same words `docs/FACTS.md` uses:
  MEAS         measured on our own hardware
  CALC         arithmetic on a datasheet figure
  SAID         someone told us, no measurement behind it
  ILLUSTRATIVE a round everyday figure, put here only to give a sense of scale.
               It is not a measurement of anything and nothing depends on it.

NOTHING HERE IS A SECOND REGISTER OF CONSTANTS. `docs/FACTS.md` remains the only one;
these are its numbers cited inside an explanation, which `CLAUDE.md` section 3bb allows.

THE ONE THING THIS FIGURE REFUSES TO DO is put a number on the gap, or on how far one Z
count moves the tip. That number is genuinely unknown for this instrument, and the
"0.016 nm per count" in circulation is inherited from Dan Berard's scanner, never
measured on ours.
"""
from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stmstyle as S  # noqa: E402

from matplotlib.patches import FancyBboxPatch  # noqa: E402

# (value in amps, label, provenance, emphasise?)
CURRENTS = [
    (3.125e-12, "3.125 picoamps — one converter count", "CALC", False),
    (4.0e-12, "about 4 picoamps — the amplifier's own input current",
     "MEAS 2026-09-15", False),
    (1.306e-10, "131 picoamps — the spread of one reading, room still",
     "MEAS 2026-09-19", False),
    (1.0e-9, "ONE NANOAMP — what a tunnelling gap would give", "the target", True),
    (3.17e-8, "31.7 nanoamps — the largest we measured through a junction",
     "MEAS 2026-09-17", False),
    (1.024e-7, "102.4 nanoamps — the most this chain can report", "CALC", False),
    (1.0, "1 amp — a phone charger, a billion times larger", "ILLUSTRATIVE", False),
]

# (value in metres, label, provenance, emphasise?)
LENGTHS = [
    (1.5e-10, "1 to 2 ångström — a tunnelling current's ten-fold distance",
     "CALC, what tunnelling requires", True),
    (1.0e-7, "about 100 nanometres — the gold leaf's thickness",
     "SAID, docs/INVENTORY.md", False),
    (7.0e-5, "about 70 microns — a human hair", "ILLUSTRATIVE", False),
]


def ladder(ax, items, lo, hi, ticks, tick_labels, xlabel, title, ybot=-0.5):
    c_em = S.series(0)
    ax.set_xscale("log")
    ax.set_xlim(lo, hi)
    ax.set_ylim(ybot, len(items) - 0.4)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xticks(ticks)
    ax.set_xticklabels(tick_labels)
    S.tidy(ax, xlabel=xlabel, title=title, grid="x")
    span = math.log10(hi) - math.log10(lo)
    for i, (v, label, prov, em) in enumerate(items):
        y = len(items) - 1 - i
        col = c_em if em else S.C["muted"]
        ax.plot([lo, v], [y, y], "-", color=S.C["grid"], lw=1.0, zorder=2)
        ax.plot([v], [y], "o", color=col, ms=13 if em else 10,
                markeredgecolor=S.C["surface"], markeredgewidth=2.0, zorder=5)
        # Labels go to the right of the marker, unless the marker is far enough along
        # the axis that they would not fit.
        rightwards = (math.log10(v) - math.log10(lo)) / span < 0.60
        x = v * 1.8 if rightwards else v / 1.8
        ha = "left" if rightwards else "right"
        (S.key if em else S.note)(ax, x, y + 0.10, label, ha=ha, va="bottom")
        S.note(ax, x, y - 0.12, prov, ha=ha, va="top",
               fontsize=S.TYPE["small"], color=S.C["muted"])


def main():
    S.set_theme("light")
    fig, (axc, axl) = S.plt.subplots(1, 2, figsize=(13.4, 8.6), width_ratios=[1.30, 1.0])
    fig.subplots_adjust(top=0.800, bottom=0.215, left=0.030, right=0.988, wspace=0.10)

    ladder(axc, CURRENTS, 1e-12, 6e4,
           [1e-12, 1e-9, 1e-6, 1e-3, 1],
           ["1 picoamp", "1 nanoamp", "1 microamp", "1 milliamp", "1 amp"],
           "Current — each labelled step is a thousand times the last",
           "CURRENT: the half we can put numbers on")

    ladder(axl, LENGTHS, 1e-10, 2e-2,
           [1e-10, 1e-8, 1e-6, 1e-4],
           ["1 ångström", "10 nanometres", "1 micron", "100 microns"],
           "Length — each labelled step is a hundred times the last",
           "LENGTH: the half we cannot", ybot=-2.6)

    # The honest gap in the right-hand ladder, drawn as the gap it is.
    from matplotlib.patches import Rectangle
    axl.add_patch(Rectangle((1.4e-10, -2.30), 1.3e-2, 1.55,
                            facecolor=S.C["band"], edgecolor="none", zorder=1))
    S.key(axl, 2.4e-10, -1.16,
          "How far one Z count moves the tip is UNKNOWN for this instrument.",
          ha="left", va="center")
    S.note(axl, 2.4e-10, -1.85,
           "The 0.016 nanometres per count in circulation was inherited from another "
           "builder's scanner.\nThat is why no figure in this set carries a scale bar, "
           "and why every axis stays in DAC counts.",
           ha="left", va="center", fontsize=S.TYPE["small"])

    S.titles_keyed(
        fig,
        "How small is a nanoamp, and how big is the gap we cannot measure",
        "<One nanoamp> is the current a tunnelling gap would give: about a billionth of what a phone charger "
        "delivers, and this instrument resolves it to three picoamps.\nDistances are the other story — the "
        "project can say what a tunnelling gap requires, but not what its own scanner does, and it says so rather "
        "than guessing.",
        [{"color": S.word(0), "fontweight": S.W_EMPH}])

    S.footer(fig, y=0.010, text=
             "Numbers are the canonical ones from docs/FACTS.md, cited here inside an explanation; that file "
             "remains the only register. Provenance is marked on every marker in that file's own vocabulary: "
             "MEAS measured on our hardware,\nCALC arithmetic on a datasheet figure, SAID told to us with no "
             "measurement behind it. ILLUSTRATIVE marks a round everyday figure put here only to give a sense of "
             "scale — it is not a measurement and nothing depends on it.\n"
             "The 131 picoamp figure is the standard deviation of a single ADCR reading with the tip clear and "
             "the room still (41.8 counts, figure 6), converted at 3.125 pA per count. The 1–2 ångström "
             "figure is what tunnelling theory requires,\nnot something measured here. \"About 100 nm\" for the "
             "gold leaf is stated in docs/INVENTORY.md and has never been measured by this project.")

    S.save(fig, "fig08_scale")


if __name__ == "__main__":
    main()
