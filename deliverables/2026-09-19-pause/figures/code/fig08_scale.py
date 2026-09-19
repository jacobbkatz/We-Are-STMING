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

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stmstyle as S  # noqa: E402

from matplotlib.patches import FancyBboxPatch  # noqa: E402

# (value in amps, label, provenance, emphasise?)
CURRENTS = [
    (3.125e-12, "one converter count\nis 3.125 picoamps", "CALC", False),
    (4.0e-12, "the amplifier's own input\ncurrent: about 4 picoamps", "MEAS 2026-09-15", False),
    (1.306e-10, "the spread of a single reading\nwith the room still: 131 picoamps",
     "MEAS 2026-09-19", False),
    (1.0e-9, "ONE NANOAMP\nthe current a tunnelling gap would give", "the target", True),
    (3.17e-8, "the largest current we measured\nthrough a junction: 31.7 nanoamps",
     "MEAS 2026-09-17", False),
    (1.024e-7, "the most this chain can report\nat all: 102.4 nanoamps", "CALC", False),
    (1.0, "a phone charger, about 1 amp —\na billion times larger", "ILLUSTRATIVE", False),
]

# (value in metres, label, provenance, emphasise?)
LENGTHS = [
    (1.5e-10, "1 to 2 ångström: the distance over which a\n"
              "tunnelling current changes ten-fold", "CALC", True),
    (1.0e-7, "the gold leaf is about 100 nanometres thick", "SAID, docs/INVENTORY.md", False),
    (7.0e-5, "a human hair, about 70 microns", "ILLUSTRATIVE", False),
]


def ladder(ax, items, lo, hi, unit_ticks, unit_labels, xlabel, title):
    c_em = S.series(0)
    ax.set_xscale("log")
    ax.set_xlim(lo, hi)
    ax.set_ylim(-0.5, len(items) - 0.5)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xticks(unit_ticks)
    ax.set_xticklabels(unit_labels)
    S.tidy(ax, xlabel=xlabel, title=title, grid="x")
    for i, (v, label, prov, em) in enumerate(items):
        y = len(items) - 1 - i
        col = c_em if em else S.C["muted"]
        ax.plot([lo, v], [y, y], "-", color=S.C["grid"], lw=1.0, zorder=2)
        ax.plot([v], [y], "o", color=col, ms=13 if em else 10,
                markeredgecolor=S.C["surface"], markeredgewidth=2.0, zorder=5)
        txt = (S.key if em else S.note)
        txt(ax, v * 1.6, y + 0.08, label, ha="left", va="bottom",
            fontsize=S.TYPE["annot"] if em else S.TYPE["annot"])
        S.note(ax, v * 1.6, y - 0.10, prov, ha="left", va="top",
               fontsize=S.TYPE["small"], color=S.C["muted"])


def main():
    S.set_theme("light")
    fig, (axc, axl) = S.plt.subplots(1, 2, figsize=(13.0, 6.4), width_ratios=[1.35, 1.0])
    fig.subplots_adjust(top=0.740, bottom=0.300, left=0.035, right=0.985, wspace=0.10)

    ladder(axc, CURRENTS, 1e-12, 4e4,
           [1e-12, 1e-9, 1e-6, 1e-3, 1],
           ["1 picoamp", "1 nanoamp", "1 microamp", "1 milliamp", "1 amp"],
           "Current (each step is a thousand times the last)",
           "Current: this is the half we can put numbers on")

    ladder(axl, LENGTHS, 1e-10, 3e-2,
           [1e-10, 1e-8, 1e-6, 1e-4],
           ["1 ångström", "10 nanometres", "1 micron", "100 microns"],
           "Length (each step is a hundred times the last)",
           "Length: this is the half we cannot")

    # The honest gap in the right-hand ladder, drawn as the gap it is.
    axl.add_patch(FancyBboxPatch(
        (1.6e-10, -0.42), 2.0e-2, 0.80,
        boxstyle="round,pad=0,rounding_size=0.06",
        facecolor=S.C["band"], edgecolor="none", zorder=1,
        transform=axl.transData))
    S.key(axl, 2.6e-10, 0.16,
          "How far one Z count moves the tip is UNKNOWN for this instrument.",
          ha="left", va="center")
    S.note(axl, 2.6e-10, -0.20,
           "The 0.016 nm per count in circulation is inherited from another builder's "
           "scanner.\nThat is why no figure in this set carries a scale bar, and why "
           "every axis stays in DAC counts.",
           ha="left", va="center", fontsize=S.TYPE["small"])

    S.titles_keyed(
        fig,
        "How small is a nanoamp, and how big is the gap we cannot measure",
        "<One nanoamp> is the current a tunnelling gap would give: about a billionth of what a phone charger "
        "delivers, and this instrument resolves it to\nthree picoamps. The distances are the other story — "
        "the project can say what a tunnelling gap requires, but not what its own scanner does.",
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
