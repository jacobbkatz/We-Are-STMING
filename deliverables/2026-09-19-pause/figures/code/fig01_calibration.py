"""Figure 1 - the end-to-end calibration against Ohm's law.

    python3 deliverables/2026-09-19-pause/figures/code/fig01_calibration.py

SOURCE. `sessions/2026-09-16-bench.md` section 3.4, the table of `ADCR` readings at eight
bias settings, measured 2026-09-16 about 19:23-19:25 UTC. There is NO CSV for that date -
`sessions/data/` starts at 2026-09-17 - so the session log's table is the primary record
and the 53 readings are transcribed from it below, one line per bias setting.

The straight line on this chart is NOT fitted. It is -3,200 counts per volt: Ohm's law
through the nominal 100 MOhm dummy resistor, divided by the converter's 0.3125 mV per
count (both in `docs/FACTS.md`). It was worked out before the measurement was taken.
"""
from __future__ import annotations

import math
import statistics as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stmstyle as S  # noqa: E402

# ------------------------------------------------------------------ the data
# sessions/2026-09-16-bench.md section 3.4. (bias-wire volts, [ADCR readings]).
# The boot reading (GSTS raw -10,659, taken before RSET) is NOT in the fit: the log
# reports it separately and it is a GSTS raw field, not an averaged ADCR read.

READINGS = [
    (+3.000, [-9625, -9145, -9868, -9442, -9851]),
    (0.000, [28, 104, 691, -95, 301, -19, -73, -307, 32, -303]),
    (-0.662, [1613, 2415, 2181, 1829, 2081, 2204]),
    (-1.578, [5335, 5548, 5314, 5634, 5065, 4434]),
    (0.000, [-616, 282, 576, -51, -83, -141]),
    (+0.711, [-1718, -2271, -1875, -1791, -2311, -2589]),
    (+1.627, [-4965, -5077, -5390, -4788, -5428, -5038]),
    (0.000, [-148, -102, 581, -480, -49, 228, 219, 59]),
]

# Predicted slope. NOT fitted, NOT tuned: 1 V across 100 MOhm is 10 nA, and the converter
# reads 320 counts per nA (docs/FACTS.md), with the sign set by the transimpedance stage.
PREDICTED_SLOPE = -3200.0
COUNTS_PER_NA = 320.5          # docs/FACTS.md, measured 2026-09-16


def ols(xs, ys):
    n = len(xs)
    mx, my = st.mean(xs), st.mean(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    b = sxy / sxx
    a = my - b * mx
    resid = [y - (a + b * x) for x, y in zip(xs, ys)]
    sse = sum(r * r for r in resid)
    sst = sum((y - my) ** 2 for y in ys)
    s2 = sse / (n - 2)
    return dict(slope=b, intercept=a,
                se_slope=math.sqrt(s2 / sxx),
                se_intercept=math.sqrt(s2 * (1.0 / n + mx * mx / sxx)),
                r2=1.0 - sse / sst, n=n, sd=math.sqrt(s2))


def main():
    xs = [v for v, rs in READINGS for _ in rs]
    ys = [float(r) for _, rs in READINGS for r in rs]
    f = ols(xs, ys)
    sigma = abs(f["slope"] - PREDICTED_SLOPE) / f["se_slope"]
    print("n=%d  slope=%.1f +/- %.1f  intercept=%+.1f +/- %.1f  R2=%.4f  sd=%.0f  "
          "agreement=%.2f sigma" % (f["n"], f["slope"], f["se_slope"], f["intercept"],
                                    f["se_intercept"], f["r2"], f["sd"], sigma))

    S.set_theme("light")
    fig, (ax, axr) = S.plt.subplots(
        2, 1, figsize=(8.2, 6.6), height_ratios=[2.45, 1.0], sharex=True)
    fig.subplots_adjust(top=0.845, bottom=0.135, left=0.105, right=0.845, hspace=0.13)

    c_meas = S.series(0)     # blue  - what the instrument read
    c_pred = S.series(1)     # orange - what theory required, before the measurement

    # --- the prediction, drawn first and underneath ---------------------------------
    span = [-1.95, 3.35]
    ax.plot(span, [PREDICTED_SLOPE * v for v in span], "-", color=c_pred, lw=2.4,
            zorder=2, label="Ohm's law through 100 MΩ — no fitting")
    # --- the 53 readings -------------------------------------------------------------
    ax.plot(xs, ys, "o", color=c_meas, ms=6.5, markeredgecolor=S.C["surface"],
            markeredgewidth=1.6, zorder=4, label="53 readings at 8 bias settings")

    S.tidy(ax, ylabel="What the converter read (counts)", grid="both")
    S.thousands(ax, "y")
    ax.set_xlim(*span)
    ax.set_ylim(-10800, 6600)
    ax.axhline(0, color=S.C["axis"], lw=0.9, zorder=1)
    ax.axvline(0, color=S.C["axis"], lw=0.9, zorder=1)

    # Unit twin: the same reading in nanoamps. One measurement, two units - not a
    # second y-scale carrying a different quantity.
    sec = ax.secondary_yaxis("right", functions=(lambda c: c / COUNTS_PER_NA,
                                                 lambda a: a * COUNTS_PER_NA))
    sec.set_ylabel("the same reading, in nanoamps", color=S.C["muted"],
                   fontsize=S.TYPE["tick"])
    sec.tick_params(colors=S.C["muted"], labelsize=S.TYPE["small"])
    sec.spines["right"].set_color(S.C["axis"])

    ax.legend(loc="upper right", bbox_to_anchor=(1.0, 1.0),
              handletextpad=0.6, labelspacing=0.5)

    S.note(ax, 2.92, PREDICTED_SLOPE * 2.92 + 620,
           "predicted line", color=c_pred, ha="right", va="bottom",
           fontweight="bold", fontsize=S.TYPE["annot"])

    # The headline, stated on the chart so it survives being cropped into a slide.
    ax.text(-1.82, -8250,
            "measured   −3,204.8 ± 36.5 counts per volt\n"
            "predicted   −3,200\n"
            "they agree to 0.13 of one standard error, R² = 0.9934",
            ha="left", va="center", fontsize=S.TYPE["annot"], color=S.C["ink"],
            linespacing=1.6,
            bbox=dict(boxstyle="round,pad=0.55", facecolor=S.C["band"],
                      edgecolor="none"))

    # --- residuals against the PREDICTION, not against the fit -----------------------
    res = [y - PREDICTED_SLOPE * x for x, y in zip(xs, ys)]
    axr.axhline(0, color=c_pred, lw=2.4, zorder=2)
    axr.plot(xs, res, "o", color=c_meas, ms=5.0, alpha=0.55,
             markeredgecolor="none", zorder=3)

    for v, rs in READINGS:
        r = [y - PREDICTED_SLOPE * v for y in rs]
        m = st.mean(r)
        sem = st.stdev(r) / math.sqrt(len(r)) if len(r) > 1 else 0.0
        axr.errorbar([v], [m], yerr=[sem], fmt="o", color=S.C["ink"], ms=7.5,
                     markeredgecolor=S.C["surface"], markeredgewidth=1.8,
                     ecolor=S.C["ink2"], elinewidth=1.6, capsize=4, zorder=6)

    S.tidy(axr, xlabel="Voltage on the bias wire, driving the 100 MΩ dummy (V)",
           ylabel="Reading minus\nprediction (counts)", grid="both")
    S.thousands(axr, "y")
    axr.set_ylim(-760, 760)
    S.note(axr, -1.82, 600,
           "black = mean of each setting, with its standard error;\n"
           "blue = every individual reading",
           va="top", fontsize=S.TYPE["small"], linespacing=1.5)

    S.titles(fig,
             "The whole measurement chain agrees with theory to 0.16%",
             "A known 100 MΩ resistor stood in for the tunnelling junction. The line is not a fit through the "
             "dots —\nit is what Ohm's law requires, worked out before the bench run. The dots landed on it.")

    S.footer(fig,
             "Source: sessions/2026-09-16-bench.md section 3.4 (no CSV exists for that date). Measured 2026-09-16, "
             "19:23–19:25 UTC, cover off, no tip fitted.\n"
             "WHAT THIS DOES NOT SHOW: the slope is the ratio of the feedback resistor to the dummy, both nominal "
             "100 MΩ, neither tolerance recorded — so this confirms the scale to within those\ntolerances, "
             "not independently of them. The 53 readings are repeats at 8 settings, not 53 independent "
             "observations. The 320-count scatter is not a noise figure (cover off, clips on the input).")

    S.save(fig, "fig01_calibration")


if __name__ == "__main__":
    main()
