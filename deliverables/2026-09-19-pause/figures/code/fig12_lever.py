"""Figure 12 - the best junction we ever made, and the one number that decides it.

    python3 deliverables/2026-09-19-pause/figures/code/fig12_lever.py

THE MEASUREMENT BEING EXPLAINED. On 2026-09-17, in the settled state, one step of the
coarse motor changed the tunnelling current by roughly ten times
(`sessions/2026-09-17-bench.md` sections 3.14 and 3.19: about 250 Z counts per decade and
about 250 Z counts per motor step, so one step is about one decade).

WHY THAT IS NOT YET AN ANSWER. A vacuum tunnel gap changes ten-fold for every 0.1 nm it
opens. One motor step turns the fine screw by 155 nm. Those two only agree if the scan
head's lever divides the screw's motion by about 1,550 - and how much it divides by
depends on ONE distance nobody has measured: how far the tip sits from the pivot line,
called `d`. Everything on this chart follows from `d` and nothing else.

    tip travel per motor step  =  155 nm  x  d / 40 mm

EVERY INPUT IS OURS AND IS MEASURED, EXCEPT `d`.
  fine screw pitch      0.31750 mm/turn      docs/FACTS.md
  motor steps per turn  2,048                28BYJ-48 through its gearbox
  pivot line to screw   40 mm                MESH, PiezoPlate.stl, Y 135.28 against 95.28
  one decade of tunnelling current per 0.1 nm    textbook, not ours

THIS CHART DOES NOT USE THE INHERITED PIEZO SCALE. The 0.016 nm per Z count that appears
elsewhere in this project came from another builder's scanner and has never been measured
on ours. It is not used here. That is what makes this the strongest form of the argument.

STATUS OF `d` AS OF 2026-09-20: NOT ESTABLISHED. Jacob measured it at the bench and
reports it is under 0.5 mm, which is a real constraint and is drawn. It cannot resolve
26 um, so it does not settle the question. docs/FACTS.md carries the row as CONTESTED.
"""
from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stmstyle as S  # noqa: E402

PITCH_MM = 0.31750          # mm per turn of the fine screw, docs/FACTS.md
STEPS_PER_TURN = 2048       # 28BYJ-48 through its gearbox
ARM_MM = 40.0               # pivot line to motor screw, MESH from PiezoPlate.stl
NM_PER_STEP = PITCH_MM / STEPS_PER_TURN * 1e6          # 155.0 nm
TUNNEL_NM = 0.1             # one decade of tunnelling current per 0.1 nm


def nm_per_decade(d_mm):
    """How far the TIP moves per motor step, which on 2026-09-17 was one decade."""
    return NM_PER_STEP * np.asarray(d_mm) / ARM_MM


D_CROSS = TUNNEL_NM * ARM_MM / NM_PER_STEP             # 0.0258 mm = 26 um

# (d in mm, label, horizontal align, vertical align, x multiplier, y multiplier).
# The offsets are hand-set: every automatic placement put one of these through the
# tunnelling line or through the curve.
MARKS = [
    (1.000, "1.00 mm\nthe design value", "left", "top", 1.16, 0.80),
    (0.500, "0.50 mm\nJacob's bench limit,\n2026-09-20", "right", "top", 0.88, 0.72),
    (0.130, "0.13 mm\nthe figure the plan quoted —\nit is a different test", "right", "bottom", 0.82, 1.55),
    (D_CROSS, "0.026 mm\nthe only value that works", "right", "bottom", 0.80, 1.50),
]


def main():
    S.set_theme("light")
    fig, ax = S.make_fig(width=9.4, height=6.4)
    fig.subplots_adjust(top=0.780, bottom=0.255, left=0.088, right=0.975)

    d = np.logspace(np.log10(0.008), np.log10(3.0), 400)
    y = nm_per_decade(d)

    # The tunnelling requirement, as a line rather than a region: it is a sharp number.
    ax.axhline(TUNNEL_NM, color=S.series(2), linewidth=2.0, zorder=4)
    ax.fill_between(d, 1e-3, TUNNEL_NM, color=S.series(2), alpha=0.10, zorder=1)

    # What Jacob's bench measurement actually excludes.
    ax.axvspan(0.5, 3.0, color=S.C["band"], zorder=0)

    ax.plot(d, y, "-", color=S.series(1), linewidth=2.4, zorder=5)

    for dm, label, ha, va, mx, my in MARKS:
        yv = float(nm_per_decade(dm))
        hit = dm == D_CROSS
        S.dot(ax, dm, yv, S.series(2) if hit else S.series(1), size=9, z=6)
        S.key(ax, dm * mx, yv * my, label, ha=ha, va=va, zorder=7,
              color=S.word(2) if hit else S.C["ink"],
              bbox=dict(facecolor=S.C["surface"], edgecolor="none", pad=1.8))

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(0.008, 3.0)
    ax.set_ylim(0.02, 20)
    ax.set_xticks([0.01, 0.03, 0.1, 0.3, 1, 3])
    ax.set_xticklabels(["0.01", "0.03", "0.1", "0.3", "1", "3"])
    ax.set_yticks([0.03, 0.1, 0.3, 1, 3, 10])
    ax.set_yticklabels(["0.03", "0.1", "0.3", "1", "3", "10"])
    ax.minorticks_off()
    S.tidy(ax,
           xlabel="d — how far the tip sits from the pivot line, in mm   (never pinned down closer than this)",
           ylabel="how far the tip moved per decade of current, in nm",
           grid="both")

    S.note(ax, 2.7, 0.078, "a tunnelling gap: one decade per 0.1 nm",
           ha="right", va="top", color=S.word(2), fontweight=S.W_EMPH)
    S.note(ax, 0.52, 14.0,
           "excluded at the bench,\n2026-09-20: d is under 0.5 mm",
           ha="left", va="top", zorder=7,
           bbox=dict(facecolor=S.C["surface"], edgecolor="none", pad=1.8))

    S.titles_keyed(
        fig,
        "Our best junction needs the tip within 26 micrometres of the pivot to have been tunnelling.",
        "On 2026-09-17 one motor step changed the current ten-fold. The screw moves 155 nm per step, so how far\n"
        "<the tip actually moved> depends entirely on the lever - and that on one distance, d, nobody has measured.\n"
        "It has to land on <the tunnelling line> for our best junction to have been a vacuum gap.",
        [{"color": S.word(1), "fontweight": S.W_EMPH},
         {"color": S.word(2), "fontweight": S.W_EMPH}])

    S.footer(fig, y=0.008, text=
             "Sources: sessions/2026-09-17-bench.md sections 3.14, 3.19 and 3.25 (the measurement); docs/FACTS.md "
             "(0.31750 mm/turn fine screw, 2,048 steps per turn); CAD PiezoPlate.stl, Y 135.28 against Y 95.28, "
             "for the 40 mm pivot-to-screw arm.\n"
             "EVERY INPUT HERE IS OURS AND MEASURED EXCEPT d AND THE 0.1 nm. This chart does NOT use the 0.016 nm "
             "per Z count that appears elsewhere in this project - that number came from another builder's scanner "
             "and has never been measured on ours.\n"
             "d IS STILL NOT ESTABLISHED as of 2026-09-20. Jacob measured at the bench that it is under 0.5 mm, "
             "which is drawn; that cannot resolve 26 um, so it does not settle the question. docs/FACTS.md carries "
             "the row as CONTESTED and docs/OPEN_QUESTIONS.md keeps it open.\n"
             "WHAT THIS DOES NOT SHOW: it assumes the whole 155 nm of screw travel reaches the lever, with no "
             "backlash, flexure or slip - the same assumption the bench made. It treats 'one motor step, one "
             "decade' as exact when the four sweeps behind it ranged 125 to 433 counts per decade.")

    print("  155.0 nm/step check: %.2f" % NM_PER_STEP)
    print("  crossing d = %.4f mm = %.1f um" % (D_CROSS, D_CROSS * 1000))
    for dm, lab, _, _, _, _ in MARKS:
        print("  d = %6.3f mm -> lever %7.1f, %6.3f nm per decade, %5.1fx too slow"
              % (dm, ARM_MM / dm, nm_per_decade(dm), nm_per_decade(dm) / TUNNEL_NM))
    S.save(fig, "fig12_lever")


if __name__ == "__main__":
    main()
