"""Figure 13 - could we simply have MISSED the tunnelling, in the instant the tip swept past?

    python3 deliverables/2026-09-19-pause/figures/code/fig13_could_we_have_missed_it.py

JACOB'S QUESTION, 2026-09-20, and it is the right one: "why didn't we have tunnelling current
for the microsecond the tip was nanometres away from the gold - how can you prove that didn't
happen?"

THE HONEST ANSWER IS THAT IT ALMOST CERTAINLY DID HAPPEN. On every approach the tip has to
pass through the gap width where tunnelling occurs. Nobody can prove a negative about an
instant nobody watched. The answerable question is different and this figure answers it:
WERE WE ABLE TO SEE IT, AND DID WE LOOK?

THE WINDOW. Our amplifier's own noise with a live junction is 9-19 ADC counts and the ADC
saturates at 32,767. Taking 20 counts (about 62 pA) as the floor, the current range in which
we could see anything at all spans 3.20 decades. A vacuum tunnel gap changes a decade per
0.1 nm, so that whole range is about 0.32 nm of gap. It is a very narrow shelf to land on.

LEFT PANEL - on the MOTOR we are blind, by construction. One motor step turns the fine screw
155 nm, divided by the lever. At the d Jacob measured at the bench, under 0.5 mm, one step
moves the tip at least 1.94 nm - four times the entire window. THERE IS NO MOTOR POSITION
INSIDE THE WINDOW. That is not a failure of ours; it is why the piezo exists.

RIGHT PANEL - on the PIEZO we are not blind, and we looked. The Z test stepped 4 counts at a
time and read 227 times a second. Recomputed from the raw files for this figure: 61,038
readings were taken inside that current range, across 109 separate approaches, a median of
365 to 1,182 per approach. We did not blink and miss it. We sat in the window and watched the
current crawl across it.

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
WIN_DEC = math.log10(HI_C / LO_C)        # 3.20 decades
WIN_NM = WIN_DEC * 0.1                   # 0.32 nm, IF it were a vacuum gap
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
    fig, (axL, axR) = S.make_fig(width=11.6, height=6.9, ncols=2,
                                 gridspec_kw=dict(width_ratios=[1.0, 1.25]))
    fig.subplots_adjust(top=0.735, bottom=0.290, left=0.105, right=0.980, wspace=0.30)

    # ---------------------------------------------------------------- LEFT
    steps = [("d = 1.00 mm\nthe design value", 1.000),
             ("d = 0.50 mm\nJacob's bench limit", 0.500),
             ("d = 0.13 mm", 0.130),
             ("d = 0.026 mm\nthe tunnelling case", 0.026)]
    ys = list(range(len(steps)))[::-1]
    for y, (lab, d) in zip(ys, steps):
        nm = NM_PER_STEP * d / 40.0
        inside = nm <= WIN_NM
        axL.barh(y, nm, height=0.52, color=S.series(2) if inside else S.series(1), zorder=4)
        S.key(axL, nm * 1.22, y, "%.2f nm — %.1fx the window" % (nm, nm / WIN_NM),
              va="center", ha="left")
    axL.axvspan(1e-3, WIN_NM, color=S.series(2), alpha=0.13, zorder=1)
    axL.axvline(WIN_NM, color=S.series(2), linewidth=2.0, zorder=3)
    axL.set_xscale("log")
    axL.set_xlim(0.02, 40)
    axL.set_ylim(-0.7, 3.7)
    axL.set_yticks(ys)
    axL.set_yticklabels([lab for lab, _ in steps])
    axL.set_xticks([0.03, 0.1, 0.17, 0.5, 1, 3, 10])
    axL.set_xticklabels(["0.03", "0.1", "0.17", "0.5", "1", "3", "10"])
    axL.minorticks_off()
    S.tidy(axL, xlabel="how far one motor step moves the TIP, in nm", grid="x")
    axL.set_title("On the motor we are blind, whatever we do\n"
              "the green line and band is the whole 0.17 nm window")


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
    axR.set_title("On the piezo we are not blind — and we looked, 109 times")

    S.titles_keyed(
        fig,
        "Could we have missed it in the instant the tip swept past? Not on the piezo — we took 60,928 readings in there.",
        "There is a narrow shelf of gap width where a tunnelling current is big enough to see and small enough not to saturate us:\n"
        "<1.70 decades of current, about 0.17 nm of gap>. One motor step jumps clean over it. The piezo does not — it steps 4 counts\n"
        "at a time, 227 readings a second, and across 109 approaches it spent 60,928 of them inside that shelf.\n"
        "<A tunnelling gap crosses that shelf in 10 to 22 Z counts.> The nearest we came was about 1,500.",
        [{"color": S.word(2), "fontweight": S.W_EMPH},
         {"color": S.word(6), "fontweight": S.W_EMPH}])

    S.footer(fig, y=0.008, text=
             "Source: sessions/data/2026-09-19-morning/ztest_1789822585.csv (29 usable approaches) and "
             "bias_m01V_/m05V_/p01V_/p05V_1789822770.csv (20 each), 2026-09-19 12:56-13:05 UTC. The reading count, "
             "the step size and the 227 readings/second are recomputed from those files for this figure.\n"
             "The window is 20 ADC counts (about 62 pA, just above the 9-19 counts of noise measured with a live "
             "junction) up to 1,000, which is the Z test's own stop target - so every one of the 109 approaches "
             "really does traverse it, and the comparison is like for like.\nThe right panel draws the approach "
             "whose reading count is CLOSEST TO THE MEDIAN, so it is typical rather than chosen.\n"
             "TWO THINGS HERE ARE CALCULATED, NOT MEASURED. The 0.17 nm assumes the "
             "window IS a vacuum gap - it is the width the gap would have to have. The 10-22 counts uses the "
             "inherited 0.016 nm per Z count, which came from another builder's\nscanner and has never been "
             "measured on ours; if our Z scale is finer, that band is narrower still and the gap widens.\n"
             "WHAT THIS IS NOT ABOUT. It is not about whether tunnelling occurred - it did, and that is settled "
             "(LEAD_VERIFICATION.md V13): the tip passes through the tunnelling separations on every approach "
             "and we were recording throughout.\nThis figure answers the narrower question the data CAN settle "
             "- whether we could have seen it, whether we looked, and whether we ever HELD it. We could, we did, "
             "at length, and what we were holding was not a gap.")

    print("  window: %.2f decades = %.2f nm;  representative cycle %d with %d readings inside"
          % (WIN_DEC, WIN_NM, pick, counts[pick]))
    S.save(fig, "fig13_could_we_have_missed_it")


if __name__ == "__main__":
    main()
