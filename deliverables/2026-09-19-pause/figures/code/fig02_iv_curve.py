"""Figure 2 - the current-voltage curve of the 2026-09-17 junction.

    python3 deliverables/2026-09-19-pause/figures/code/fig02_iv_curve.py

SOURCE. `sessions/2026-09-17-bench.md` section 3.15, round 7 of eight rounds in which the
bias polarity was interleaved so that drift could not fake a slope. Measured 2026-09-17
from about 19:54:51 UTC. No CSV of this sweep exists in `sessions/data/`, so the session
log's six-row table is the primary record and is transcribed below.

THE EXPONENT. The session log reads the shape as "roughly V^2". That is wrong, and the
lead's own refit says so (`deliverables/2026-09-19-pause/LEAD_VERIFICATION.md` V2): the
six points give V^1.55, log-log R^2 0.985. A pure V^2 would put 85 nA at 0.5 V where 31.7
was measured. This figure draws V^2 as the rejected model it is, and recomputes the
exponent from the table every time it runs rather than quoting it.
"""
from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stmstyle as S  # noqa: E402

# sessions/2026-09-17-bench.md section 3.15, round 7. Bias magnitude in volts, current
# magnitude in nA. The log records the junction as symmetric in both polarities to about
# 10%, so these are magnitudes and the sign is not plotted.
V = [0.05, 0.10, 0.15, 0.25, 0.35, 0.50]
I = [0.85, 2.0, 3.3, 7.5, 14.6, 31.7]


def loglog_fit(xs, ys):
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys]
    n = len(lx)
    mx, my = sum(lx) / n, sum(ly) / n
    sxx = sum((x - mx) ** 2 for x in lx)
    b = sum((x - mx) * (y - my) for x, y in zip(lx, ly)) / sxx
    a = my - b * mx
    sse = sum((y - (a + b * x)) ** 2 for x, y in zip(lx, ly))
    sst = sum((y - my) ** 2 for y in ly)
    return b, math.exp(a), 1.0 - sse / sst


def main():
    n_exp, _amp, r2 = loglog_fit(V, I)
    R = [v / (i * 1e-9) / 1e6 for v, i in zip(V, I)]      # MOhm
    g0 = I[0] / V[0]                                       # nA per V at the lowest bias
    ohmic_at_max = g0 * V[-1]
    vsq_at_max = I[0] * (V[-1] / V[0]) ** 2
    print("power-law exponent %.3f  (log-log R2 %.3f)" % (n_exp, r2))
    print("resistance %.1f -> %.1f MOhm" % (R[0], R[-1]))
    print("at %.2f V: measured %.1f nA, ohmic %.1f nA, pure V^2 %.1f nA"
          % (V[-1], I[-1], ohmic_at_max, vsq_at_max))
    print("measured / ohmic at the top of the sweep = %.2fx" % (I[-1] / ohmic_at_max))

    S.set_theme("light")
    fig, (ax, ax2) = S.plt.subplots(1, 2, figsize=(10.4, 6.0), width_ratios=[1.22, 1.0])
    fig.subplots_adjust(top=0.745, bottom=0.225, left=0.070, right=0.985, wspace=0.24)

    c_meas, c_ohm, c_rej = S.series(0), S.series(1), S.C["muted"]
    grid_v = [0.005 * k for k in range(101)]               # 0 to 0.50 V

    # --- the rejected model, in the de-emphasis grey ---------------------------------
    ax.plot(grid_v, [I[0] * (v / V[0]) ** 2 for v in grid_v], "-", color=c_rej, lw=1.8,
            zorder=2)
    # --- the reference model: an ordinary resistor of the low-bias resistance ---------
    ax.plot(grid_v, [g0 * v for v in grid_v], "-", color=c_ohm, lw=2.4, zorder=3)
    # --- the measurement --------------------------------------------------------------
    ax.plot(V, I, "-", color=c_meas, lw=2.2, zorder=4)
    ax.plot(V, I, "o", color=c_meas, ms=8, markeredgecolor=S.C["surface"],
            markeredgewidth=2.0, zorder=5)

    S.tidy(ax, xlabel="Voltage across the junction (V)",
           ylabel="Current through the junction (nA)", grid="both")
    ax.set_xlim(0, 0.735)
    ax.set_ylim(0, 96)
    ax.set_xticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5])

    # Direct labels at the curve ends, outside the data. No legend box anywhere.
    S.note(ax, 0.518, vsq_at_max, "a pure V² law\nneeds %.0f nA" % vsq_at_max,
           ha="left", va="center", color=S.C["ink2"])
    S.key(ax, 0.518, I[-1], "measured\n%.1f nA" % I[-1], ha="left", va="center")
    S.note(ax, 0.518, ohmic_at_max, "Ohm's law\ngives %.1f nA" % ohmic_at_max,
           ha="left", va="center", color=S.C["ink2"])

    ax.set_title("At half a volt it passes %.1f times the current an ordinary %.0f M\u03a9\n"
                 "resistor would. Fitted to the six points, current rises as V^%.2f"
                 % (I[-1] / ohmic_at_max, R[0], n_exp))

    # --- right panel: the resistance is not a constant --------------------------------
    ax2.plot([0, 0.735], [R[0], R[0]], "-", color=c_ohm, lw=2.4, zorder=3)
    ax2.plot(V, R, "-", color=c_meas, lw=2.2, zorder=4)
    ax2.plot(V, R, "o", color=c_meas, ms=8, markeredgecolor=S.C["surface"],
             markeredgewidth=2.0, zorder=5)
    S.tidy(ax2, xlabel="Voltage across the junction (V)",
           ylabel="Junction resistance (MΩ)", grid="both")
    ax2.set_xlim(0, 0.735)
    ax2.set_ylim(0, 72)
    ax2.set_xticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5])
    S.note(ax2, 0.525, R[0], "a resistor would\nstay on this line",
           ha="left", va="center", color=S.C["ink2"])
    S.key(ax2, 0.525, R[-1], "it falls to\n%.0f MΩ" % R[-1], ha="left", va="center")
    ax2.set_title("The resistance is not a constant: it falls from\n"
                  "%.0f MΩ to %.0f MΩ over a ten-fold voltage range" % (R[0], R[-1]))

    S.titles_keyed(
        fig,
        "We made a real tip-and-sample junction, and it behaves like a barrier",
        "<The measured current> climbs far faster than the voltage does \u2014 ruling out a metallic short, "
        "which would follow\n<the straight line of Ohm's law>, and an open circuit, which would give nothing. "
        "Both polarities agreed to about 10%, interleaved so drift could not fake it.",
        [{"color": S.word(0), "fontweight": S.W_EMPH},
         {"color": S.word(1), "fontweight": S.W_EMPH}])

    S.footer(fig, y=0.008, text=
             "Source: sessions/2026-09-17-bench.md section 3.15, round 7 of 8 (no CSV exists for this sweep). "
             "Measured 2026-09-17 from about 19:54:51 UTC, on the 2026-09-17 tip and sample.\n"
             "WHAT THIS DOES NOT SHOW: a barrier is not the same claim as a vacuum tunnelling gap — a "
             "contaminant film, a thin oxide or a dirty near-contact are all superlinear too. 16–59 MΩ "
             "sits at the low end of the\nrange tunnelling occupies, which usually starts above 100 MΩ. A "
             "different tip and sample two nights later gave a different verdict (figure 5). The session log's "
             "\"roughly V²\" reading is wrong; the refit is V^%.2f." % n_exp)

    S.save(fig, "fig02_iv_curve")


if __name__ == "__main__":
    main()
