"""The I-V curve of a real junction, and what its shape does and does not prove.

    python3 deliverables/2026-09-19-pause/analysis/code/iv_barrier.py

Source: sessions/data/2026-09-19-bench/here_run1.csv, the 'iv' rows - 21 bias DAC codes,
32 readings each, taken at Z 0 on 2026-09-19 bench at about 01:28 UTC, on the tip that
Jacob later said was BENT. Also the 'flip' rows (the bias flip that proves the junction
is real) and the 'slope' rows (Z 0 to 3000 at fixed bias).

Two curves are compared against the measurement:
  - a straight line through the origin, which is what an ohmic contact gives
  - the Simmons low-bias form I = a*V + b*V^3, which is the leading shape of a
    symmetric tunnel barrier at small bias
A cubic term is necessary for a barrier but NOT sufficient: a pressed contact through a
thin insulating film gives the same shape. The session logs say this; the fit below is
the arithmetic behind it.

Outputs: plots/fig12_iv_curve.png, fig13_bias_flip.png
"""
import math
import os
import statistics as st
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (data_path, read_rows, fnum, bias_code_to_sample_volts, ols,
                    style, save, section, COUNTS_PER_NA, TOL, SERIES)


def main():
    plt = style()
    _, rows = read_rows(data_path("2026-09-19-bench", "here_run1.csv"))

    section("1. THE I-V, 21 BIAS POINTS x 32 READINGS  (here_run1.csv, tag 'iv')")
    by_bias = {}
    for r in rows:
        if r["tag"] != "iv":
            continue
        by_bias.setdefault(int(r["bias"]), []).append(fnum(r["value"]))
    pts = []
    print("  %-8s %+9s %10s %9s %9s %12s" % ("BIAS", "V sample", "mean", "sd", "n", "current nA"))
    for code in sorted(by_bias):
        v = bias_code_to_sample_volts(code)
        vals = [x for x in by_bias[code] if x is not None]
        m = st.mean(vals)
        sd = st.stdev(vals) if len(vals) > 1 else float("nan")
        pts.append((v, m, sd, len(vals)))
        print("  %-8d %+9.3f %10.1f %9.1f %9d %12.3f"
              % (code, v, m, sd, len(vals), m / COUNTS_PER_NA))
    pts.sort()

    section("2. EXCLUSIONS BEFORE ANY FIT")
    RAIL = 32700.0
    railed = sorted(code for code, vals in by_bias.items()
                    if any(v is not None and abs(v) >= RAIL for v in vals))
    print("  The ADC rails at +-32,767 counts (docs/FACTS.md, 16-bit two's complement).")
    print("  Bias codes with at least one railed reading, EXCLUDED from every fit below:")
    for code in railed:
        n_rail = sum(1 for v in by_bias[code] if v is not None and abs(v) >= RAIL)
        print("    BIAS %-6d (%+.3f V): %d of %d readings at the rail"
              % (code, bias_code_to_sample_volts(code), n_rail, len(by_bias[code])))
    keep = [p for p in pts if abs(p[0]) <= 0.81 and
            not any(v is not None and abs(v) >= RAIL for v in by_bias[
                min(by_bias, key=lambda c: abs(bias_code_to_sample_volts(c) - p[0]))])]
    print("  Also excluded: |V| > 0.81 V, where the Simmons low-bias expansion used below")
    print("  does not apply and where the +1.000 V point has a standard deviation of")
    print("  %.0f counts across its 32 readings - the junction was changing during it."
          % max(p[2] for p in pts if abs(p[0]) > 0.81))
    print("  Points kept: %d of %d, spanning %+0.1f to %+0.1f V"
          % (len(keep), len(pts), min(p[0] for p in keep), max(p[0] for p in keep)))
    vs = np.array([p[0] for p in keep])
    cs = np.array([p[1] for p in keep])

    section("3. IS IT A STRAIGHT LINE? (an ohmic contact would be)")
    lin = ols(list(vs), list(cs))
    print("  straight line fit: %.1f counts/V, R^2 %.5f" % (lin["slope"], lin["r2"]))
    print("  equivalent resistance from the slope: %.0f MOhm"
          % (1e3 / abs(lin["slope"] / COUNTS_PER_NA)))
    lowv = [p for p in keep if abs(p[0]) <= 0.105 and abs(p[0]) > 0.05]
    if lowv:
        r = [1e3 * abs(p[0]) / (abs(p[1]) / COUNTS_PER_NA) for p in lowv]
        print("  resistance from the +-0.1 V points alone: %s MOhm  (the session log says ~190)"
              % ", ".join("%.0f" % x for x in r))
    # cubic, no constant term: I = a V + b V^3
    A = np.vstack([vs, vs ** 3]).T
    coef, res, *_ = np.linalg.lstsq(A, cs, rcond=None)
    pred = A @ coef
    ss_res = float(((cs - pred) ** 2).sum())
    ss_tot = float(((cs - cs.mean()) ** 2).sum())
    print("  cubic fit  I = a*V + b*V^3 : a = %.1f counts/V, b = %.1f counts/V^3, R^2 %.5f"
          % (coef[0], coef[1], 1 - ss_res / ss_tot))
    print("  the cubic term is worth %.1f%% of the current at |V| = 0.8 V"
          % (100 * abs(coef[1] * 0.8 ** 3) / abs(coef[0] * 0.8 + coef[1] * 0.8 ** 3)))
    # F test of the extra term
    n = len(vs)
    lin0 = float(((cs - lin["slope"] * vs - lin["intercept"]) ** 2).sum())
    F = ((lin0 - ss_res) / 1) / (ss_res / (n - 2))
    print("  F for adding the cubic term: %.1f on 1 and %d degrees of freedom" % (F, n - 2))
    print()
    print("  The symmetric form fits only moderately well, and that is itself the result:")
    print("  a*V + b*V^3 is symmetric by construction and this curve is not. Fitting each")
    print("  polarity separately as a power law I = k |V|^p:")
    for name, sel in (("sample negative", vs < -0.02), ("sample positive", vs > 0.02)):
        x = np.log10(np.abs(vs[sel]))
        y = np.log10(np.abs(cs[sel]))
        f2 = ols(list(x), list(y))
        print("    %-16s p = %.2f +- %.2f, R^2 %.3f, n = %d"
              % (name, f2["slope"], f2["se_slope"], f2["r2"], f2["n"]))
    print("    p = 1 is ohmic. Both polarities are well above 1, which is the")
    print("    superlinearity. They differ from each other, which is the asymmetry.")

    section("4. IS IT SYMMETRIC? (a symmetric barrier would be)")
    print("  %-9s %12s %12s %10s" % ("|V|", "sample -ve", "sample +ve", "ratio"))
    for target in (0.1, 0.2, 0.4, 0.5, 0.6, 0.8):
        neg = min(pts, key=lambda p: abs(p[0] + target))
        pos = min(pts, key=lambda p: abs(p[0] - target))
        if abs(abs(neg[0]) - target) > 0.06 or abs(abs(pos[0]) - target) > 0.06:
            continue
        print("  %-9.2f %12.1f %12.1f %10.2f"
              % (target, neg[1], pos[1], abs(neg[1] / pos[1]) if pos[1] else float("nan")))
    print()
    print("  Session log 3.6 quotes +-0.1 V: 177 / -166 (~190 MOhm); +-0.5 V: 2280 / -1479;")
    print("  +-0.8 V: 12148 / -3334. The rows above are the same measurement; small")
    print("  differences are because the log quotes single points and these are the means")
    print("  of all 32 readings at each code.")

    section("5. WHAT THE SHAPE PROVES, AND WHAT IT DOES NOT")
    print("  PROVES (measured): the current follows the sign of the sample voltage, is")
    print("  superlinear, and is asymmetric above about 0.6 V. That is a junction, not a")
    print("  leak, and not an amplifier offset.")
    print("  DOES NOT PROVE: tunnelling through vacuum. A tip resting on the gold through")
    print("  a thin oxide or contamination film gives the same superlinear, asymmetric")
    print("  shape. A new tungsten tip carries an oxide unless it is etched. The session")
    print("  log says this in the same paragraph as the measurement, and the Z tests of")
    print("  the following morning argue for the pressed-contact reading.")
    print("  ALSO: this curve was taken with the tip that Jacob identified as BENT about")
    print("  90 minutes later. Nothing about it transfers to the tip fitted at ~03:00.")

    section("6. THE BIAS FLIP - the control that makes this a junction (tag 'flip')")
    seq, cur = [], None
    for r in rows:
        if r["tag"] != "flip":
            continue
        code = int(r["bias"])
        if cur is None or code != cur[0]:
            cur = (code, [])
            seq.append(cur)
        cur[1].append(fnum(r["value"]))
    for code, vals in seq:
        vals = [x for x in vals if x is not None]
        print("  BIAS %-6d (%+.3f V sample): mean %+8.1f counts (%+.2f nA), sd %.1f, n %d"
              % (code, bias_code_to_sample_volts(code), st.mean(vals),
                 st.mean(vals) / COUNTS_PER_NA,
                 st.stdev(vals) if len(vals) > 1 else float("nan"), len(vals)))
    print("  session log 3.6 quotes -0.5 V 1156, +0.5 V -811, 0 V -1, -0.5 V 1033.")

    section("7. CURRENT AGAINST Z AT THIS JUNCTION (tag 'slope', Z 0 to 3000)")
    byz = {}
    for r in rows:
        if r["tag"] != "slope":
            continue
        byz.setdefault(int(r["z"]), []).append(fnum(r["value"]))
    zs = sorted(byz)
    print("  Z from %d to %d in %d distinct steps, %d readings each"
          % (zs[0], zs[-1], len(zs), len(byz[zs[0]])))
    prof = [(z, st.mean([x for x in byz[z] if x is not None])) for z in zs]
    for z, m in prof[::max(1, len(prof) // 12)]:
        print("    Z %5d  %8.1f counts (%.2f nA)" % (z, m, m / COUNTS_PER_NA))
    good = [(z, m) for z, m in prof if m > 0]
    f = ols([float(z) for z, _ in good], [math.log10(m) for _, m in good])
    print("  straight-line fit of log10(current) against Z: %+0.3e decades per count"
          % f["slope"])
    print("  = %s counts per decade%s"
          % ("%.0f" % (1 / abs(f["slope"])) if f["slope"] else "infinite",
             ", and the sign is NEGATIVE: pushing Z up REDUCED the current here"
             if f["slope"] < 0 else ""))
    print("  R^2 %.3f over %d points" % (f["r2"], f["n"]))
    print("  The session log calls this 'current ~2000 falling slowly to ~1400 - no rise'.")
    print("  This was one of the pieces of evidence that the Z direction was unresolved")
    print("  for the bent tip; it was settled the other way for the replacement tip.")

    # ------------------------------------------------------------ figures
    section("8. FIGURES")
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.6))
    ax = axes[0]
    excl = [p for p in pts if p not in keep]
    ax.errorbar(vs, cs, yerr=[p[2] for p in keep], fmt="o", ms=4, color=TOL["blue"],
                ecolor=TOL["grey"], capsize=2, lw=1.0,
                label="measured (mean of 32, $\\pm$1 sd)")
    if excl:
        ax.scatter([p[0] for p in excl], [p[1] for p in excl], s=26, marker="x",
                   color=TOL["grey"],
                   label="excluded: at or near the ADC rail, or |V| > 0.8 V")
    g = np.linspace(vs.min(), vs.max(), 200)
    ax.plot(g, lin["intercept"] + lin["slope"] * g, color=TOL["grey"], ls="--", lw=1.1,
            label="straight line (an ohmic contact)")
    ax.plot(g, coef[0] * g + coef[1] * g ** 3, color=TOL["red"], lw=1.2,
            label="$aV + bV^3$ (a symmetric barrier)")
    ax.axhline(0, color=TOL["black"], lw=0.7)
    ax.axvline(0, color=TOL["black"], lw=0.7)
    ax.set_xlabel("sample voltage (V)")
    ax.set_ylabel("ADC reading (counts)")
    sec = ax.secondary_yaxis("right", functions=(lambda c: c / COUNTS_PER_NA,
                                                 lambda i: i * COUNTS_PER_NA))
    sec.set_ylabel("current (nA)")
    ax.set_title("I-V of a real junction\n2026-09-19 bench 01:28 UTC, Z 0, the BENT tip")
    ax.legend(loc="upper left", fontsize=7)

    ax = axes[1]
    ax.semilogy(np.abs(vs[vs < 0]), np.abs(cs[vs < 0]), "o-", ms=4, color=TOL["purple"],
                label="sample negative")
    ax.semilogy(np.abs(vs[vs > 0]), np.abs(cs[vs > 0]), "s-", ms=4, color=TOL["green"],
                label="sample positive")
    ax.set_xlabel("|sample voltage| (V)")
    ax.set_ylabel("|ADC reading| (counts)")
    ax.set_title("The two polarities separate above ~0.6 V\n"
                 "a symmetric vacuum barrier would keep them together")
    ax.legend(loc="upper left")
    save(fig, "fig12_iv_curve.png")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.6, 3.2))
    x0 = 0
    for i, (code, vals) in enumerate(seq):
        vals = [v for v in vals if v is not None]
        xs = np.arange(x0, x0 + len(vals))
        ax.plot(xs, vals, lw=0.8, color=SERIES[i % len(SERIES)],
                label="sample %+.1f V" % bias_code_to_sample_volts(code))
        x0 += len(vals)
    ax.axhline(0, color=TOL["black"], lw=0.8)
    ax.set_xlabel("reading number, in the order taken")
    ax.set_ylabel("ADC reading (counts)")
    ax.set_title("The bias flip: the current follows the sign of the sample voltage\n"
                 "this is the control that separates a junction from an amplifier offset")
    ax.legend(loc="center right", ncol=2)
    save(fig, "fig13_bias_flip.png")
    plt.close(fig)


if __name__ == "__main__":
    main()
