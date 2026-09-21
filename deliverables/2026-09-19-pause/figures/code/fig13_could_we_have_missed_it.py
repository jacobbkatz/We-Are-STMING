"""Figure 13 - we were inside the tunneling window, and we never parked in it.

    python3 deliverables/2026-09-19-pause/figures/code/fig13_could_we_have_missed_it.py

JACOB'S QUESTION, 2026-09-20, and it is the right one: "why didn't we have tunneling current
for the microsecond the tip was nanometers away from the gold - how can you prove that didn't
happen?"

THE ANSWER IS THAT IT DID HAPPEN, and that is settled - LEAD_VERIFICATION.md V13. On every
approach the tip passes through the separations where tunneling is the only mechanism
available, and bias was applied with the amplifier recording throughout. SO THIS FIGURE IS NOT
ABOUT WHETHER TUNNELING OCCURRED, and it must not be titled as though it were.

REPHRASED 2026-09-20, second pass. It used to be headed "Could we have blinked and missed it?
No." - which reads to anyone who is not holding the whole argument in their head as "we looked
and there was nothing there", the exact opposite of what this project claims and of what the
page it sits on says two screens above. Jacob caught it. The figure's claim is now stated the
way the evidence actually runs: WE WERE IN THERE, RECORDING, THE WHOLE WAY THROUGH - AND WE
NEVER STAYED.

THE WINDOW. Our amplifier's own noise with a live junction is 9-19 ADC counts and the ADC
saturates at 32,767. Taking 20 counts (about 62 pA) as the floor and 1,000 counts as the
ceiling - the Z test's own stop target, so that every approach really does traverse it - the
window spans 1.70 decades. A vacuum tunnel gap changes a decade per 0.1 nm, so that whole
window is about 0.17 nm of gap. It is a very narrow shelf to land on.

WHAT IS PLOTTED. One approach, the one whose reading count is closest to the median, drawn
from the raw file. Behind it, the whole distribution: every crossing in all five files is
measured by `crossing_stats()` below and the numbers go straight into the subtitle, so they
cannot drift away from the data the way a typed-in figure can.

THE 1,500 THAT WAS WRONG. The website's caption said "the nearest we came was about 1,500
counts". Nothing produced that number. Recomputed here across all 109 approaches, the
crossings run 52 to 7,540 Z counts with a median of 2,108, and the two narrowest are real
readings rather than a sampling artifact (14 and 12 readings inside the window, at a 4-count
step). Corrected on the page in the same pass.

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
                                 # comparison against a tunneling gap is like for like.
WIN_DEC = math.log10(HI_C / LO_C)        # 1.70 decades
WIN_NM = WIN_DEC * 0.1                   # 0.17 nm, IF it were a vacuum gap
NM_PER_STEP = 0.31750 / 2048 * 1e6       # 155.03 nm of screw per motor step
TUN_LO, TUN_HI = 6, 13           # Z counts per decade for tunneling, on the INHERITED scale

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


def reading_rate(paths):
    """Readings per second, from the timestamps in the files themselves.

    The footer used to claim "Counts, step size and the 227 readings/second are
    recomputed from those files" while 227 was typed into that sentence. It is not
    what the files give: 227/s is the median rate of three of the four bias files,
    but the 30-cycle ztest file runs at 257/s and the five together give 232/s. A
    sentence that says a number was recomputed has to be the number that was.
    """
    import statistics as _st
    gaps = []
    for path in paths:
        ts = [float(r["t"]) for r in csv.DictReader(open(path))]
        gaps += [b - a for a, b in zip(ts, ts[1:]) if 0 < b - a < 1]
    return 1.0 / _st.median(gaps)


def approach_paths():
    import glob
    return [S.data_path(SESSION, FILE)] + sorted(
        glob.glob(os.path.join(S.DATA, SESSION, "bias_*_1789822770.csv")))


def crossing_stats():
    """Every approach in all five files: how many readings inside the window, and how
    many Z counts it took to cross it.

    The subtitle used to carry 60,928 and 109 as typed-in literals and the website
    carried a crossing figure that nothing produced. These come off the files.
    """
    paths = approach_paths()
    rows, readings, per_file = [], 0, {}
    for path in paths:
        n = 0
        for v in in_cycles(path).values():
            inw = [(z, a) for z, a in v if LO_C <= a <= HI_C]
            if len(inw) < 2:
                continue
            rows.append((abs(inw[-1][0] - inw[0][0]), len(inw)))
            readings += len(inw)
            n += 1
        per_file[os.path.basename(path)] = n
    rows.sort()
    widths = [w for w, _n in rows]
    steps = sorted({abs(b - a) for p in paths for v in in_cycles(p).values()
                    for (a, _x), (b, _y) in zip(v, v[1:]) if b != a})
    return dict(approaches=len(widths), readings=readings, lo=widths[0],
                med=int(round(st.median(widths))), hi=widths[-1],
                narrow=rows[:2], per_file=per_file,
                step=steps[0] if steps else None)


def main():
    # How many Z counts a vacuum gap would take to cross this same window, on the
    # INHERITED scale. Computed from the band and the window, not typed in: "10 to
    # 22" appeared in three places on this sheet and would have had to be edited in
    # all three if either the window or the 6-13 band ever moved.
    tun_lo, tun_hi = int(round(TUN_LO * WIN_DEC)), int(round(TUN_HI * WIN_DEC))

    S.set_theme("light")
    fig, axR = S.make_fig(width=10.2, height=7.4)
    fig.subplots_adjust(top=0.760, bottom=0.235, left=0.095, right=0.975)

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
    # What a tunneling gap would look like on exactly these axes, drawn from the same
    # start point. CALCULATED, on the inherited Z scale - labeled as such.
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
    # Anchored at the GEOMETRIC CENTRE of the window, not at a hand-picked height.
    # This label carries an opaque box, and the window's two green edges sit at
    # LO_C/CPN and HI_C/CPN; a box centred anywhere else grows through one of them
    # as the wording changes, which is what adding "(calculated)" first did to the
    # upper edge. Centring it leaves the most room on both sides by construction.
    S.key(axR, z0 + 55, math.sqrt(LO_C * HI_C) / CPN,
          "a tunneling gap\ncrosses this shelf\nin %d to %d counts\n(calculated)"
          % (tun_lo, tun_hi),
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

    cs = crossing_stats()
    S.titles_keyed(
        fig,
        "Passing through the tunneling window is not the same as parking in it",
        "The green band is the window: wide enough to see a tunneling current, narrow enough not to saturate us.\n"
        "<Across %d approaches the tip spent %s readings in there> \u2014 the current was recorded the whole way "
        "through.\n<A clean vacuum gap crosses that shelf in %d to %d Z counts (calculated).> These crossings "
        "took %d to %s, a median of %s."
        % (cs["approaches"], format(cs["readings"], ","), tun_lo, tun_hi, cs["lo"],
           format(cs["hi"], ","), format(cs["med"], ",")),
        [{"color": S.word(2), "fontweight": S.W_EMPH},
         {"color": S.word(6), "fontweight": S.W_EMPH}])

    S.footer(fig, y=0.012, text=
             "Source: sessions/data/2026-09-19-morning/ztest_1789822585.csv (%d usable approaches)\n"
             "and bias_m01V_/m05V_/p01V_/p05V_1789822770.csv (%d each), 2026-09-19 12:56-13:05 UTC.\n"
             "Counts, step size and the %.0f readings/second are recomputed from those files. This is\n"
             "the approach whose reading count is CLOSEST TO THE MEDIAN, so it is typical.\n"
             "The window runs from %d ADC counts (about %.0f pA) to %s, the Z test's own stop target.\n"
             "CALCULATED, NOT MEASURED: the %d-%d counts uses an inherited 0.016 nm per Z count.\n"
             "The two narrowest crossings, %d and %d counts, are real readings rather than a\n"
             "sampling artifact: %d and %d readings inside the window, at a %d-count Z step."
             % (cs["per_file"][FILE],
                max(n for f, n in cs["per_file"].items() if f != FILE),
                reading_rate(approach_paths()),
                int(LO_C), LO_C / CPN * 1000, format(int(HI_C), ","),
                tun_lo, tun_hi,
                cs["narrow"][0][0], cs["narrow"][1][0],
                cs["narrow"][0][1], cs["narrow"][1][1], cs["step"]))

    print("  window: %.2f decades = %.2f nm;  representative cycle %d with %d readings inside"
          % (WIN_DEC, WIN_NM, pick, counts[pick]))
    print("  %d approaches, %s readings inside; crossings %d to %d counts, median %d"
          % (cs["approaches"], format(cs["readings"], ","), cs["lo"], cs["hi"], cs["med"]))
    S.save(fig, "fig13_could_we_have_missed_it")


if __name__ == "__main__":
    main()
