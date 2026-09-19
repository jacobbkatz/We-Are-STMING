"""Re-derive the 100 MOhm dummy-junction calibration of 2026-09-16 from the raw readings.

    python3 deliverables/2026-09-19-pause/analysis/code/calibration.py

Outputs: plots/fig01_calibration.png, plots/fig02_calibration_residuals.png
and a printed table of every number this analysis reproduces or disputes.

WHERE THE RAW DATA LIVE. There is no CSV for this test. The 53 individual ADCR readings
are tabulated in sessions/2026-09-16-bench.md section 3.4, and that table IS the raw
record. They are transcribed below, reading-by-reading, exactly as the log prints them.
The transcription is checked against the log's own per-step means before anything is
fitted, so a typing error in this file fails loudly rather than quietly changing a
result.

The x axis is the voltage on the bias wire, converted from the BIAS DAC code with the
conversion in common.py, which is itself derived from docs/FACTS.md. The log quotes the
same voltages, so the conversion is independently checked too.
"""
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (bias_code_to_sample_volts, ols, style, save, section,
                    COUNTS_PER_NA, TOL)

# (BIAS code, the log's printed bias-wire voltage, [ADCR readings], the log's printed mean)
# sessions/2026-09-16-bench.md section 3.4, the table headed "UTC / BIAS code / Bias wire
# / ADCR readings / Mean / Predicted". The 19:23:00 GSTS row is NOT included: it is a raw
# GSTS field, taken before RSET, not an ADCR reading, and the log excludes it from its own
# 53-reading fit.
STEPS = [
    (0,     +3.000, [-9625, -9145, -9868, -9442, -9851], -9586),
    (32768,  0.000, [28, 104, 691, -95, 301, -19, -73, -307, 32, -303], 36),
    (40000, -0.662, [1613, 2415, 2181, 1829, 2081, 2204], 2054),
    (50000, -1.578, [5335, 5548, 5314, 5634, 5065, 4434], 5222),
    (32768,  0.000, [-616, 282, 576, -51, -83, -141], -6),
    (25000, +0.711, [-1718, -2271, -1875, -1791, -2311, -2589], -2093),
    (15000, +1.627, [-4965, -5077, -5390, -4788, -5428, -5038], -5114),
    (32768,  0.000, [-148, -102, 581, -480, -49, 228, 219, 59], 39),
]

# The prediction the session log states, and which this analysis tests rather than assumes:
# one volt across a nominal 100 MOhm dummy is 10 nA; at the ADC's 0.3125 mV per count
# through a nominal 100 MOhm feedback resistor that is 3,200 counts, negative by the
# measured sign convention (docs/FACTS.md, "Sign: bias wire voltage to ADC counts").
PREDICTED_SLOPE = -3200.0


def main():
    section("1. TRANSCRIPTION CHECK - does this file hold the log's numbers?")
    bad = 0
    for code, v_log, reads, mean_log in STEPS:
        v_calc = bias_code_to_sample_volts(code)
        mean_calc = sum(reads) / len(reads)
        dv = abs(v_calc - v_log)
        dm = abs(mean_calc - mean_log)
        flag = ""
        if dv > 0.001:
            flag += " VOLTAGE MISMATCH"
            bad += 1
        if dm > 0.5:
            flag += " MEAN MISMATCH"
            bad += 1
        print("  BIAS %-6d log %+7.3f V  derived %+7.3f V | n=%2d  log mean %+7.1f  "
              "recomputed %+8.2f%s" % (code, v_log, v_calc, len(reads), mean_log, mean_calc, flag))
    n_total = sum(len(r) for _, _, r, _ in STEPS)
    print("  readings transcribed: %d (the session log fits 53)" % n_total)
    if bad or n_total != 53:
        raise SystemExit("TRANSCRIPTION CHECK FAILED - do not trust anything below")
    print("  PASS: every step's derived voltage and recomputed mean match the log.")

    section("2. LEAST SQUARES ON ALL 53 INDIVIDUAL READINGS")
    xs, ys = [], []
    for code, _, reads, _ in STEPS:
        v = bias_code_to_sample_volts(code)
        for r in reads:
            xs.append(v)
            ys.append(float(r))
    f = ols(xs, ys)
    print("  slope      %+9.1f +- %.1f counts per volt on the bias wire" % (f["slope"], f["se_slope"]))
    print("  intercept  %+9.1f +- %.1f counts" % (f["intercept"], f["se_intercept"]))
    print("  R^2        %9.4f" % f["r2"])
    print("  residual sd%9.1f counts per reading" % f["resid_sd"])
    print("  n          %9d" % f["n"])
    print()
    print("  SESSION LOG SAYS: slope -3,205 +- 37, intercept +58, R^2 0.993, residual 320, n 53")
    print("  THIS ANALYSIS  : slope %.0f +- %.0f, intercept %+.0f, R^2 %.3f, residual %.0f, n %d"
          % (f["slope"], f["se_slope"], f["intercept"], f["r2"], f["resid_sd"], f["n"]))

    section("3. AGAINST THE PREDICTION")
    ratio = f["slope"] / PREDICTED_SLOPE
    sigma = (f["slope"] - PREDICTED_SLOPE) / f["se_slope"]
    cpna = abs(f["slope"]) / 10.0      # 1 V across 100 MOhm is 10 nA
    se_cpna = f["se_slope"] / 10.0
    print("  predicted slope        %+.1f counts per volt (1 V / 100 MOhm = 10 nA)" % PREDICTED_SLOPE)
    print("  measured / predicted   %.4f" % ratio)
    print("  measured - predicted   %.2f standard errors" % sigma)
    print("  counts per nA          %.1f +- %.1f  (docs/FACTS.md carries %.1f)"
          % (cpna, se_cpna, COUNTS_PER_NA))
    print("  intercept vs zero      %.2f standard errors" % (f["intercept"] / f["se_intercept"]))

    section("4. THE THREE ZERO-BIAS VISITS - drift and hysteresis")
    zeros = [(i, s) for i, s in enumerate(STEPS) if s[0] == 32768]
    for i, (code, _, reads, _) in zeros:
        m = sum(reads) / len(reads)
        sd = math.sqrt(sum((r - m) ** 2 for r in reads) / (len(reads) - 1))
        print("  visit at step %d: mean %+7.2f counts, sd %6.1f, n %d" % (i + 1, m, sd, len(reads)))
    allz = [r for _, s in zeros for r in s[2]]
    mz = sum(allz) / len(allz)
    sdz = math.sqrt(sum((r - mz) ** 2 for r in allz) / (len(allz) - 1))
    print("  pooled zero-bias: mean %+.1f counts, sd %.1f, n %d" % (mz, sdz, len(allz)))
    print("  in current: %+.3f nA offset, %.3f nA of scatter per reading"
          % (mz / COUNTS_PER_NA, sdz / COUNTS_PER_NA))

    section("5. PER-STEP AGREEMENT WITH THE FIT")
    print("  %-8s %8s %9s %9s %8s %8s" % ("BIAS", "volts", "mean", "fit", "diff", "diff/se"))
    for code, _, reads, _ in STEPS:
        v = bias_code_to_sample_volts(code)
        m = sum(reads) / len(reads)
        pred = f["intercept"] + f["slope"] * v
        se_m = f["resid_sd"] / math.sqrt(len(reads))
        print("  %-8d %+8.3f %+9.1f %+9.1f %+8.1f %+8.2f"
              % (code, v, m, pred, m - pred, (m - pred) / se_m))

    # ---------------------------------------------------------------- figures
    plt = style()

    fig, ax = plt.subplots(figsize=(5.4, 4.0))
    ax.axhline(0, color=TOL["grey"], lw=0.8, zorder=0)
    ax.axvline(0, color=TOL["grey"], lw=0.8, zorder=0)
    ax.scatter(xs, ys, s=16, color=TOL["blue"], alpha=0.75, zorder=3,
               label="individual ADCR readings (n = 53)")
    lo, hi = min(xs) - 0.25, max(xs) + 0.25
    ax.plot([lo, hi], [f["intercept"] + f["slope"] * lo, f["intercept"] + f["slope"] * hi],
            color=TOL["red"], zorder=4,
            label="least squares: %.0f $\\pm$ %.0f counts/V" % (f["slope"], f["se_slope"]))
    ax.plot([lo, hi], [PREDICTED_SLOPE * lo, PREDICTED_SLOPE * hi],
            color=TOL["black"], ls="--", lw=1.1, zorder=2,
            label="predicted from 100 M$\\Omega$: %.0f counts/V" % PREDICTED_SLOPE)
    ax.set_xlabel("voltage on the bias wire (V)")
    ax.set_ylabel("ADC reading (counts)")
    ax.set_title("The measurement chain, end to end\n"
                 "100 M$\\Omega$ dummy junction, 2026-09-16, R$^2$ = %.3f" % f["r2"])
    sec = ax.secondary_yaxis("right", functions=(lambda c: c / COUNTS_PER_NA,
                                                 lambda i: i * COUNTS_PER_NA))
    sec.set_ylabel("current (nA)  [at %.1f counts/nA]" % COUNTS_PER_NA)
    ax.legend(loc="upper right")
    save(fig, "fig01_calibration.png")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(5.4, 3.0))
    ax.axhline(0, color=TOL["red"], lw=1.0)
    ax.scatter(xs, f["resid"], s=16, color=TOL["blue"], alpha=0.75)
    ax.axhline(f["resid_sd"], color=TOL["grey"], ls=":", lw=1.0)
    ax.axhline(-f["resid_sd"], color=TOL["grey"], ls=":", lw=1.0,
               label="$\\pm$1 sd = %.0f counts" % f["resid_sd"])
    ax.set_xlabel("voltage on the bias wire (V)")
    ax.set_ylabel("residual (counts)")
    ax.set_title("Residuals: no curvature, no hysteresis between the three zero-bias visits")
    ax.legend(loc="upper right")
    save(fig, "fig02_calibration_residuals.png")
    plt.close(fig)

    return f


if __name__ == "__main__":
    main()
