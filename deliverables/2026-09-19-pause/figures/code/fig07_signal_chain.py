"""Figure 7 - the signal chain, with the real numbers on it.

    python3 deliverables/2026-09-19-pause/figures/code/fig07_signal_chain.py

This is the ten-second explanation of the instrument: what turns a voltage into a current
and a current into a number on a laptop screen, and what each step is worth.

EVERY NUMBER HERE IS FROM `docs/FACTS.md`, and each box says where it came from:
  DS    a manufacturer datasheet
  CALC  arithmetic on a datasheet figure, shown
  MEAS  measured on our own hardware

They are cited inside an explanation, which `CLAUDE.md` section 3bb expressly allows;
`docs/FACTS.md` remains the only register, and nothing here is a second one.

NO DISTANCE SCALE APPEARS ON THIS FIGURE. The gap between tip and sample is drawn as a
gap and never given a size: this instrument has never established a distance scale from
its own hardware.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stmstyle as S  # noqa: E402

from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

# (heading, what it does, the number that matters, provenance tag)
STAGES = [
    ("Bias DAC",
     "sets the voltage\non the sample",
     "\u00b13 V, and\n0.0916 mV per step", "DS + MEAS"),
    ("The sample",
     "gold leaf, sitting\nat that voltage",
     "\u22120.5 V in\nmost runs", "the usual setting"),
    ("The gap",
     "current crosses from\nsample to tip here",
     "about 1 nA is\nwhat we are after", "the target"),
    ("The preamplifier",
     "an OPA627 with a 100 M\u03a9\nfeedback resistor",
     "1 nA becomes\n0.1 volts", "DS + CALC"),
    ("The converter",
     "an LTC2326-16,\n16 bits over its range",
     "\u00b110.24 V full scale,\n0.3125 mV per count", "DS + CALC"),
    ("The reading",
     "what Jacob and Nuh\nactually see",
     "320.5 counts\nper nanoamp", "MEASURED"),
]


def main():
    S.set_theme("light")
    fig = S.plt.figure(figsize=(13.4, 6.6))
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    n = len(STAGES)
    left, right = 3.0, 97.0
    gapw = 2.0
    boxw = (right - left - gapw * (n - 1)) / n
    ytop, ybot = 80.0, 42.0
    c_meas = S.series(0)
    c_ds = S.C["muted"]

    for i, (head, does, num, prov) in enumerate(STAGES):
        x = left + i * (boxw + gapw)
        measured = prov.startswith("DS + MEAS") or prov.startswith("MEASURED")
        edge = c_meas if measured else c_ds
        ax.add_patch(FancyBboxPatch(
            (x, ybot), boxw, ytop - ybot,
            boxstyle="round,pad=0,rounding_size=1.4",
            facecolor=S.C["surface"], edgecolor=edge, linewidth=1.6, zorder=3))
        ax.add_patch(FancyBboxPatch(
            (x, ytop - 1.0), boxw, 1.0,
            boxstyle="round,pad=0,rounding_size=0.45",
            facecolor=edge, edgecolor="none", zorder=4))

        cx = x + boxw / 2.0
        ax.text(cx, ytop - 4.2, head, ha="center", va="top",
                fontsize=S.TYPE["label"], fontweight=S.W_TITLE, color=S.C["ink"])
        ax.text(cx, ytop - 11.0, does, ha="center", va="top",
                fontsize=S.TYPE["annot"], color=S.C["ink2"], linespacing=1.8)
        ax.plot([x + 2.5, x + boxw - 2.5], [ybot + 13.5, ybot + 13.5], "-",
                color=S.C["grid"], lw=1.0, zorder=4)
        ax.text(cx, ybot + 8.4, num, ha="center", va="center",
                fontsize=S.TYPE["annot"], fontweight=S.W_EMPH,
                color=c_meas if measured else S.C["ink"], linespacing=1.9)
        ax.text(cx, ybot + 2.4, prov, ha="center", va="center",
                fontsize=S.TYPE["small"], color=S.C["muted"])

        if i < n - 1:
            xa = x + boxw
            ax.add_patch(FancyArrowPatch(
                (xa + 0.25, (ytop + ybot) / 2.0), (xa + gapw - 0.25, (ytop + ybot) / 2.0),
                arrowstyle="-|>", mutation_scale=15, linewidth=1.8,
                color=S.C["axis"], zorder=5))

    # ---- the worked example ----------------------------------------------------------
    ax.add_patch(FancyBboxPatch(
        (left, 17.0), right - left, 17.0,
        boxstyle="round,pad=0,rounding_size=1.4",
        facecolor=S.C["band"], edgecolor="none", zorder=2))
    ax.text(left + 2.6, 29.7, "Follow one nanoamp through it",
            ha="left", va="center", fontsize=S.TYPE["label"], fontweight=S.W_TITLE,
            color=S.C["ink"])
    ax.text(left + 2.6, 22.3,
            "1 nanoamp at the tip   \u2192   0.1 volts out of the amplifier   \u2192   "
            "320 counts on the laptop.\n"
            "One count is 3.125 picoamps, and the largest current the chain can report "
            "is 102.4 nanoamps.",
            ha="left", va="center", fontsize=S.TYPE["annot"], color=S.C["ink2"],
            linespacing=2.1)

    ax.text(right - 2.6, 29.7, "blue = measured on this instrument",
            ha="right", va="center", fontsize=S.TYPE["annot"], fontweight=S.W_EMPH,
            color=S.word(0))
    ax.text(right - 2.6, 24.4, "grey = from a datasheet, or arithmetic on one",
            ha="right", va="center", fontsize=S.TYPE["annot"], color=S.C["ink2"])

    S.titles_keyed(
        fig,
        "How the instrument turns a gap into a number",
        "Six stages. <The last one was measured end to end> against what Ohm's law requires, and agreed to 0.16% "
        "(figure 1);\nthe rest come from the parts' own datasheets and the arithmetic on them.",
        [{"color": S.word(0), "fontweight": S.W_EMPH}])

    S.footer(fig, y=0.010, text=
             "Every number on this diagram is the canonical one from docs/FACTS.md, cited here inside an "
             "explanation; that file remains the only register of constants in this project.\n"
             "NO DISTANCE SCALE APPEARS ANYWHERE ON THIS FIGURE. The gap is drawn as a gap and never given a "
             "size, because this instrument has never established a distance scale from its own hardware — "
             "the nanometres-per-count figure\nin circulation is inherited from another builder's scanner. "
             "\"About 1 nA is what we are after\" is the target a tunnelling junction would give, not a "
             "measurement of one: this project has never demonstrated a stable tunnelling gap.")

    S.save(fig, "fig07_signal_chain")


if __name__ == "__main__":
    main()
