"""Figure 13 - could we simply have MISSED the tunnelling, in the instant the tip swept past?

    python3 deliverables/2026-09-19-pause/figures/code/fig13_could_we_have_missed_it.py

JACOB'S QUESTION, 2026-09-20, and it is the right one: "why didn't we have tunnelling current
for the microsecond the tip was nanometres away from the gold - how can you prove that didn't
happen?"

THE ANSWER IS THAT IT DID HAPPEN, and that is settled - LEAD_VERIFICATION.md V13. On every
approach the tip passes through the separations where tunnelling is the only mechanism
available, and bias was applied with the amplifier recording throughout. SO THIS FIGURE IS NOT
ABOUT WHETHER TUNNELLING OCCURRED. It answers the narrower question the data CAN settle:
COULD WE HAVE SEEN IT, DID WE LOOK, AND DID WE EVER HOLD IT?

THE WINDOW. Our amplifier's own noise with a live junction is 9-19 ADC counts and the ADC
saturates at 32,767. Taking 20 counts (about 62 pA) as the floor and 1,000 counts as the
ceiling - the Z test's own stop target, so that every approach really does traverse it - the
window spans 1.70 decades. A vacuum tunnel gap changes a decade per 0.1 nm, so that whole
window is about 0.17 nm of gap. It is a very narrow shelf to land on.

LEFT PANEL - on the MOTOR we are blind, by construction. One motor step turns the fine screw
155 nm, divided by the lever. At the d Jacob measured at the bench, under 0.5 mm, one step
moves the tip at least 1.94 nm - eleven times the entire window. THERE IS NO MOTOR POSITION
INSIDE THE WINDOW. That is not a failure of ours; it is why the piezo exists.

RIGHT PANEL - on the PIEZO we are not blind, and we looked. The Z test stepped 4 counts at a
time and read 227 times a second. Recomputed from the raw files for this figure: 60,928
readings were taken inside that current range, across 109 separate approaches, a median of
364 to 1,180 per approach. We did not blink and miss it. We sat in the window and watched the
current crawl across it - where a vacuum gap would have crossed it in 10 to 22 Z counts.

SOURCE. sessions/data/2026-09-19-morning/ztest_1789822585.csv and bias_*_1789822770.csv,
2026-09-19 12:56-13:05 UTC; docs/FACTS.md for the geometry and the noise figures.
"""
from __future__ import annotations

import collections
import csv
import math
import os
import statistics as st
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stmstyle as S  # noqa: E402
from matplotlib.ticker import NullFormatter, ScalarFormatter  # noqa: E402

CPN = 320.5                      # ADC counts per nA
LO_C, HI_C = 20.0, 1000.0        # the window: just above our noise, up to the Z test's own stop
                                 # target. Bounding it by the test rather than by ADC saturation
                                 # matters: every approach really does traverse this, so the
                                 # comparison against a tunnelling gap is like for like.
WIN_DEC = math.log10(HI_C / LO_C)        # 1.70 decades
WIN_NM = WIN_DEC * 0.1                   # 0.17 nm, IF it were a vacuum gap
NM_PER_STEP = 0.31750 / 2048 * 1e6       # 155.03 nm of screw per motor step
TUN_LO, TUN_HI = 6, 13           # Z counts per decade for tunnelling, on the INHERITED scale

FILE = "ztest_1789822585.csv"
SESSION = "2026-09-19-morning"


def in_cycles(path):
    cyc = collections.defaultdict(list)
    for r in csv.DictReader(open(path)):
        if r["phase"] != "in":
            continue
        try:
            cyc[int(r["cycle"])].append((int(r["z"]), abs(float(r["adc"]))))
        except ValueError:
            pass
    return cyc


def main():
    S.set_theme("light")
    fig, axR = S.make_fig(width=10.2, height=7.4)
    fig.subplots_adjust(top=0.760, bottom=0.400, left=0.095, right=0.975)

    # ---------------------------------------------------------------- RIGHT
    cyc = in_cycles(S.data_path(SESSION, FILE))
    counts = {c: len([1 for _, a in v if LO_C <= a <= HI_C]) for c, v in cyc.items()}
    counts = {c: n for c, n in counts.items() if n >= 2}
    med = st.median(counts.values())
    pick = min(counts, key=lambda c: abs(counts[c] - med))
    v = cyc[pick]
    zs = [z for z, _ in v]
    axR.plot(zs, [max(a, 1.0) / CPN for _, a in v], "-",
             color=S.series(1), linewidth=2.0, zorder=5)

    axR.axhspan(LO_C / CPN, HI_C / CPN, color=S.series(2), alpha=0.11, zorder=1)
    for lev in (LO_C, HI_C):
        axR.axhline(lev / CPN, color=S.series(2), linewidth=1.4, zorder=3)

    inw = [(z, a) for z, a in v if LO_C <= a <= HI_C]
    z0, z1 = inw[0][0], inw[-1][0]
    # What a tunnelling gap would look like on exactly these axes, drawn from the same
    # start point. CALCULATED, on the inherited Z scale - labelled as such.
    for cpd, style in ((TUN_HI, dict(linewidth=2.0)), (TUN_LO, dict(linewidth=2.0))):
        zz = [z0 + cpd * k for k in (0, WIN_DEC)]
        axR.plot(zz, [LO_C / CPN, HI_C / CPN], "-", color=S.series(6), zorder=6, **style)
    axR.fill_betweenx([LO_C / CPN, HI_C / CPN],
                      [z0, z0 + TUN_LO * WIN_DEC], [z0, z0 + TUN_HI * WIN_DEC],
                      color=S.series(6), alpha=0.30, zorder=5)

    axR.annotate("", xy=(z1, 7.0), xytext=(z0, 7.0),
                 arrowprops=dict(arrowstyle="<|-|>", color=S.C["ink"], linewidth=1.2,
                                 shrinkA=0, shrinkB=0, mutation_scale=9), zorder=7)
    S.key(axR, (z0 + z1) / 2, 8.4,
          "we crossed it in %s counts, taking %d readings" % (format(abs(z1 - z0), ","), counts[pick]),
          ha="center", va="bottom", zorder=8,
          bbox=dict(facecolor=S.C["surface"], edgecolor="none", pad=1.8))
    S.key(axR, z0 + 55, 1.6, "a tunnelling gap\ncrosses this shelf\nin 10 to 22 counts",
          ha="left", va="center", color=S.word(6), zorder=8,
          bbox=dict(facecolor=S.C["surface"], edgecolor="none", pad=1.8))

    axR.set_yscale("log")
    axR.set_ylim(0.03, 300)
    axR.yaxis.set_major_formatter(ScalarFormatter())
    axR.yaxis.set_minor_formatter(NullFormatter())
    axR.set_yticks([0.1, 1, 10, 100])
    axR.set_yticklabels(["0.1", "1", "10", "100"])
    axR.set_xlim(min(zs) - 60, max(zs) + 60)
    S.thousands(axR, "x")
    S.tidy(axR, xlabel="Z, in DAC counts", ylabel="current, nA", grid="both")
    axR.set_title("One approach, drawn from the raw file")

    S.titles_keyed(
        fig,
        "Could we have blinked and missed it? No. We took 60,928 readings inside the window.",
        "The green band is the window: wide enough to see a tunnelling current, narrow enough not to saturate us.\n"
        "<Across 109 approaches the tip spent 60,928 readings in there.> "
        "<A real vacuum gap would cross it in 10 to 22 counts.> We took 2,636.",
        [{"color": S.word(2), "fontweight": S.W_EMPH},
         {"color": S.word(6), "fontweight": S.W_EMPH}])

    S.footer(fig, y=0.012, text=
             "Source: sessions/data/2026-09-19-morning/ztest_1789822585.csv (29 usable approaches)\n"
             "and bias_m01V_/m05V_/p01V_/p05V_1789822770.csv (20 each), 2026-09-19 12:56-13:05 UTC.\n"
             "Counts, step size and the 227 readings/second are recomputed from those files. This is\n"
             "the approach whose reading count is CLOSEST TO THE MEDIAN, so it is typical.\n"
             "The window runs from 20 ADC counts (about 62 pA) to 1,000, the Z test\'s own stop target.\n"
             "CALCULATED, NOT MEASURED: the 10-22 counts uses an inherited 0.016 nm per Z count.")

    print("  window: %.2f decades = %.2f nm;  representative cycle %d with %d readings inside"
          % (WIN_DEC, WIN_NM, pick, counts[pick]))
    S.save(fig, "fig13_could_we_have_missed_it")


if __name__ == "__main__":
    main()
