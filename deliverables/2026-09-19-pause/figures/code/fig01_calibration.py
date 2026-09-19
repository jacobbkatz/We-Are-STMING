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
import os
import statistics as st
import sys

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

# Predicted slope. NOT fitted, NOT tuned: 1 V across 100 MOhm is 10 nA and the converter
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
    sse = sum((y - (a + b * x)) ** 2 for x, y in zip(xs, ys))
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
        2, 1, figsize=(8.8, 7.4), height_ratios=[2.5, 1.0], sharex=True)
    fig.subplots_adjust(top=0.815, bottom=0.200, left=0.108, right=0.852, hspace=0.17)

    c_meas = S.series(0)     # blue   - what the instrument read
    c_pred = S.series(1)     # orange - what theory required, before the measurement

    span = [-1.95, 3.45]
    ax.plot(span, [PREDICTED_SLOPE * v for v in span], "-", color=c_pred, lw=2.4, zorder=2)
    ax.plot(xs, ys, "o", color=c_meas, ms=6.5, markeredgecolor=S.C["surface"],
            markeredgewidth=1.6, zorder=4)

    S.tidy(ax, ylabel="What the converter read (counts)", grid="both")
    S.thousands(ax, "y")
    ax.set_xlim(*span)
    ax.set_ylim(-10900, 6700)
    ax.axhline(0, color=S.C["axis"], lw=0.9, zorder=1)
    ax.axvline(0, color=S.C["axis"], lw=0.9, zorder=1)

    # Unit twin: the same reading in nanoamps. One measurement, two units - not a second
    # y-scale carrying a different quantity.
    sec = ax.secondary_yaxis("right", functions=(lambda c: c / COUNTS_PER_NA,
                                                 lambda a: a * COUNTS_PER_NA))
    sec.set_ylabel("the same reading, in nanoamps", color=S.C["muted"],
                   fontsize=S.TYPE["annot"], labelpad=14)
    sec.tick_params(colors=S.C["muted"], labelsize=S.TYPE["small"], pad=4)
    sec.spines["right"].set_color(S.C["axis"])

    # The headline, stated on the chart so it survives being cropped into a slide.
    ax.text(-1.80, -7950,
            "measured   −3,204.8 ± 36.5 counts per volt\n"
            "predicted   −3,200\n"
            "the two agree to 0.13 of one standard error, R² = 0.9934",
            ha="left", va="center", fontsize=S.TYPE["annot"], fontweight=S.W_EMPH,
            color=S.C["ink"], linespacing=1.9,
            bbox=dict(boxstyle="round,pad=0.7", facecolor=S.C["band"], edgecolor="none"))

    # --- residuals against the PREDICTION, not against the fit -----------------------
    res = [y - PREDICTED_SLOPE * x for x, y in zip(xs, ys)]
    axr.axhline(0, color=c_pred, lw=2.4, zorder=2)
    axr.plot(xs, res, "o", color=c_meas, ms=5.0, alpha=0.5, markeredgecolor="none",
             zorder=3)
    for v, rs in READINGS:
        r = [y - PREDICTED_SLOPE * v for y in rs]
        m = st.mean(r)
        sem = st.stdev(r) / math.sqrt(len(r)) if len(r) > 1 else 0.0
        axr.errorbar([v], [m], yerr=[sem], fmt="o", color=S.C["ink"], ms=7.5,
                     markeredgecolor=S.C["surface"], markeredgewidth=1.8,
                     ecolor=S.C["ink2"], elinewidth=1.6, capsize=4, zorder=6)

    S.tidy(axr, xlabel="Voltage on the bias wire, driving the 100 MΩ dummy (V)",
           ylabel="Reading minus\nprediction (counts)", grid="both",
           title="Dark dots are each setting's mean, with its standard error. "
                 "Pale dots are every individual reading.")
    S.thousands(axr, "y")
    axr.set_ylim(-820, 820)
    axr.set_title(axr.get_title(loc="left"), loc="left", fontsize=S.TYPE["small"],
                  color=S.C["muted"], fontweight=S.W_BODY, pad=6)

    # The key is the subtitle: the words are coloured, so there is no legend box to
    # collide with the data.
    S.titles_keyed(
        fig,
        "The whole measurement chain works end to end — and agrees with theory to 0.16%",
        "A known 100 MΩ resistor stood in for the tunnelling junction. <The 53 readings> landed on "
        "<the line Ohm's law requires>,\nwhich was worked out before the bench run and is not fitted to "
        "anything.",
        [{"color": S.word(0), "fontweight": S.W_EMPH},
         {"color": S.word(1), "fontweight": S.W_EMPH}])

    S.footer(fig, y=0.008, text=
             "Source: sessions/2026-09-16-bench.md section 3.4 (no CSV exists for that date). Measured 2026-09-16, "
             "19:23–19:25 UTC, cover off, no tip fitted.\n"
             "WHAT THIS DOES NOT SHOW: the slope is the ratio of the feedback resistor to the dummy, both nominal "
             "100 MΩ, neither tolerance recorded — so this confirms the scale to within those\ntolerances, "
             "not independently of them. The 53 readings are repeats at 8 settings, not 53 independent "
             "observations. The 320-count scatter is not a noise figure (cover off, clips on the input).")

    S.save(fig, "fig01_calibration")


if __name__ == "__main__":
    main()
