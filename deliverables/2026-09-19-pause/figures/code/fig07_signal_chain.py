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

# The agreement figure quoted in the subtitle is figure 1's, so it is IMPORTED from
# figure 1 rather than retyped here. Both used to carry a hand-typed "0.16%"; the
# arithmetic gives 0.15%, and one of the two would always have been fixed alone.
import fig01_calibration as F1  # noqa: E402

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
    # Recomputed from figure 1's own readings and its own fit, so the two figures
    # cannot disagree about a number they both quote.
    xs = [v for v, rs in F1.READINGS for _ in rs]
    ys = [float(r) for _, rs in F1.READINGS for r in rs]
    agreed_pct, _sigma = F1.agreement(F1.ols(xs, ys))
    print("  agreement with Ohm's law, imported from figure 1: %.4f%%" % agreed_pct)

    S.set_theme("light")
    # THREE ACROSS, TWO DOWN. Six boxes in a row made the figure twice as wide as it
    # was tall, so a browser column scaled it to about a third and a phone to a tenth -
    # the text inside was 4 px. Wrapping the chain halves the width and the whole thing
    # reads at twice the size for the same number of pixels.
    fig = S.plt.figure(figsize=(10.4, 12.0))
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    ncol = 3
    left, right = 3.0, 97.0
    gapw = 4.0
    boxw = (right - left - gapw * (ncol - 1)) / ncol
    ROWS = [(84.0, 62.0), (54.0, 32.0)]        # (top, bottom) of each row of boxes
    c_meas = S.series(0)
    c_ds = S.C["muted"]

    def box_x(i):
        return left + (i % ncol) * (boxw + gapw)

    for i, (head, does, num, prov) in enumerate(STAGES):
        ytop, ybot = ROWS[i // ncol]
        x = box_x(i)
        measured = prov.startswith("DS + MEAS") or prov.startswith("MEASURED")
        edge = c_meas if measured else c_ds
        ax.add_patch(FancyBboxPatch(
            (x, ybot), boxw, ytop - ybot,
            boxstyle="round,pad=0,rounding_size=1.0",
            facecolor=S.C["surface"], edgecolor=edge, linewidth=1.6, zorder=3))
        ax.add_patch(FancyBboxPatch(
            (x, ytop - 0.8), boxw, 0.8,
            boxstyle="round,pad=0,rounding_size=0.3",
            facecolor=edge, edgecolor="none", zorder=4))

        cx = x + boxw / 2.0
        ax.text(cx, ytop - 2.5, head, ha="center", va="top",
                fontsize=S.TYPE["label"], fontweight=S.W_TITLE, color=S.C["ink"])
        ax.text(cx, ytop - 7.0, does, ha="center", va="top",
                fontsize=S.TYPE["annot"], color=S.C["ink2"], linespacing=1.55)
        ax.plot([x + 2.5, x + boxw - 2.5], [ybot + 9.0, ybot + 9.0], "-",
                color=S.C["grid"], lw=1.0, zorder=4)
        ax.text(cx, ybot + 5.6, num, ha="center", va="center",
                fontsize=S.TYPE["annot"], fontweight=S.W_EMPH,
                color=c_meas if measured else S.C["ink"], linespacing=1.6)
        ax.text(cx, ybot + 1.3, prov, ha="center", va="center",
                fontsize=S.TYPE["small"], color=S.C["muted"])

        if i % ncol < ncol - 1 and i < len(STAGES) - 1:
            xa = x + boxw
            ax.add_patch(FancyArrowPatch(
                (xa + 0.5, (ytop + ybot) / 2.0), (xa + gapw - 0.5, (ytop + ybot) / 2.0),
                arrowstyle="-|>", mutation_scale=15, linewidth=1.8,
                color=S.C["axis"], zorder=5))

    # The wrap: out of the last box on row one, round the end, into the first on row two.
    r0t, r0b = ROWS[0]
    r1t, r1b = ROWS[1]
    mid = (r0t + r0b) / 2.0
    xend = box_x(ncol - 1) + boxw
    ybar = (r0b + r1t) / 2.0
    ax.plot([xend + 0.5, xend + 2.0], [mid, mid], "-", color=S.C["axis"], lw=1.8,
            zorder=5, solid_capstyle="round")
    ax.plot([xend + 2.0, xend + 2.0], [mid, ybar], "-", color=S.C["axis"], lw=1.8,
            zorder=5, solid_capstyle="round")
    ax.plot([xend + 2.0, left - 2.0], [ybar, ybar], "-", color=S.C["axis"], lw=1.8,
            zorder=5, solid_capstyle="round")
    ax.plot([left - 2.0, left - 2.0], [ybar, (r1t + r1b) / 2.0], "-",
            color=S.C["axis"], lw=1.8, zorder=5, solid_capstyle="round")
    ax.add_patch(FancyArrowPatch(
        (left - 2.0, (r1t + r1b) / 2.0), (left - 0.5, (r1t + r1b) / 2.0),
        arrowstyle="-|>", mutation_scale=15, linewidth=1.8,
        color=S.C["axis"], zorder=5))

    # ---- the worked example ----------------------------------------------------------
    ax.add_patch(FancyBboxPatch(
        # y 12 to 30, not 14 to 34. The box row above ends at y = 32, so the old
        # band overlapped it by two units and its heading sat about two points
        # under the "The preamplifier" border - close enough that the heading read
        # as part of that box rather than of the worked example.
        (left, 12.0), right - left, 18.0,
        boxstyle="round,pad=0,rounding_size=1.4",
        facecolor=S.C["band"], edgecolor="none", zorder=2))
    ax.text(left + 2.6, 27.4, "Follow one nanoamp through it",
            ha="left", va="center", fontsize=S.TYPE["label"], fontweight=S.W_TITLE,
            color=S.C["ink"])
    ax.text(left + 2.6, 17.6,
            "1 nanoamp at the tip   \u2192   0.1 volts out of the amplifier   \u2192   "
            "320 counts on the laptop.\n"
            "One count is 3.125 picoamps, and the largest current the chain can report "
            "is 102.4 nanoamps.",
            ha="left", va="center", fontsize=S.TYPE["annot"], color=S.C["ink2"],
            linespacing=2.1)

    ax.text(right - 2.6, 27.4, "blue = measured on this instrument",
            ha="right", va="center", fontsize=S.TYPE["annot"], fontweight=S.W_EMPH,
            color=S.word(0))
    ax.text(right - 2.6, 23.4, "gray = from a datasheet, or arithmetic on one",
            ha="right", va="center", fontsize=S.TYPE["annot"], color=S.C["ink2"])

    S.titles_keyed(
        fig,
        "How the instrument turns a gap into a number",
        "Six stages. <The last one was measured end to end> against what Ohm's law requires, and agreed to %.2f%% "
        "(figure 1);\nthe rest come from the parts' own datasheets and the arithmetic on them." % agreed_pct,
        [{"color": S.word(0), "fontweight": S.W_EMPH}])

    S.footer(fig, y=0.010, text=
             "Every number on this diagram is the canonical one from docs/FACTS.md, cited here inside an "
             "explanation; that file remains the only register of constants in this project.\n"
             "NO DISTANCE SCALE APPEARS ANYWHERE ON THIS FIGURE. The gap is drawn as a gap and never given a "
             "size, because this instrument has never established a distance scale from its own hardware — "
             "the nanometers-per-count figure\nin circulation is inherited from another builder's scanner. "
             "\"About 1 nA is what we are after\" is the target a tunneling junction would give, not a "
             "measurement of one: this project has never demonstrated a stable tunneling gap.")

    S.save(fig, "fig07_signal_chain")


if __name__ == "__main__":
    main()
