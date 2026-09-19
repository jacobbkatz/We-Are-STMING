"""Re-derive the 2026-09-19 morning Z tests: counts per decade, hysteresis, drift, snaps.

    python3 deliverables/2026-09-19-pause/analysis/code/ztest_analysis.py

This is an INDEPENDENT re-implementation. It does not import the bench script
sessions/data/2026-09-19-morning/scripts/ztest.py; it re-reads the CSVs and re-does the
arithmetic from the definitions in that script's docstring, so an error in either would
show up as a disagreement. The bench script's own definitions, which this follows:

  counts per decade  straight-line fit of log10|I| against Z, using only points with
                     100 <= |I| <= 1000 counts, IN and OUT phases separately, >= 3 points
  hysteresis         (first Z going IN where |I| >= 300) minus (last Z coming OUT where
                     |I| >= 300). Positive means the current persists further out.
  onset              first Z in the IN phase where |I| >= 1000; drift is the slope of
                     onset Z against time across the cycles of one run
  snap rows          rows whose phase is 'snap'. One watchdog EVENT writes one row per
                     back-off step, so rows over-count events; events are counted here
                     as maximal runs of consecutive snap rows

Outputs: plots/fig03_ztest_curves.png, fig04_ztest_hysteresis.png,
fig05_ztest_cpd_by_bias.png, fig06_ztest_drift.png, and a printed comparison against
every number in sessions/2026-09-19-morning.md sections 3.10-3.11 and docs/FACTS.md.
"""
import math
import os
import statistics as st
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (DATA, data_path, read_ztest, ols, style, save, section,
                    bias_code_to_sample_volts, COUNTS_PER_NA, TOL, SERIES)

FIT_LO, FIT_HI, MID_I, TARGET = 100.0, 1000.0, 300.0, 1000.0

# The five Z-test runs the session log treats as results, plus the one it EXCLUDES.
# 'bias_code' is from sessions/data/2026-09-19-morning/README.md; the sample voltage is
# derived from it, not copied.
RUNS = [
    ("ztest_1789822585.csv",     "-0.5 V (run 1, 30 cycles)", 38229, True,  "12:56"),
    ("bias_m01V_1789822770.csv", "-0.1 V",                    33860, True,  "12:59"),
    ("bias_p05V_1789822770.csv", "+0.5 V",                    27307, True,  "13:01"),
    ("bias_p01V_1789822770.csv", "+0.1 V",                    31676, True,  "13:03"),
    ("bias_m05V_1789822770.csv", "-0.5 V (repeat, 20 cycles)", 38229, True, "13:04"),
    ("apz_ztest_1789822231.csv", "-0.5 V (12:50, EXCLUDED)",  38229, False, "12:50"),
]

# What the session log and docs/FACTS.md state, to be checked, not assumed.
# label -> (cpd_in, cpd_out, hyst, watchdog_events, drift counts/s)
LOG = {
    "-0.5 V (run 1, 30 cycles)":   (1650, 3442, 1162, 3, -74),
    "-0.1 V":                      (808, 4839, 1653, 0, +29),
    "+0.5 V":                      (2243, 4975, 1868, 1, +22),
    "+0.1 V":                      (4639, 12595, 1474, 0, +7),
    "-0.5 V (repeat, 20 cycles)":  (1967, 3834, 705, 0, +83),
}


def fit_cpd(pts):
    """Counts per decade from [(z, I)]. Returns (cpd, n_points_used)."""
    p = [(z, math.log10(abs(i))) for z, i in pts
         if i is not None and FIT_LO <= abs(i) <= FIT_HI]
    if len(p) < 3:
        return None, len(p)
    zs = [a for a, _ in p]
    ls = [b for _, b in p]
    if len(set(zs)) < 2:
        return None, len(p)
    f = ols(zs, ls)
    if f["slope"] == 0:
        return None, len(p)
    return 1.0 / abs(f["slope"]), len(p)


def analyse(rows):
    """Per-cycle results and a run summary."""
    cyc = {}
    for t, c, ph, z, m in rows:
        if c >= 1:
            cyc.setdefault(c, []).append((t, ph, z, m))
    per = []
    for c, pts in sorted(cyc.items()):
        pin = [(z, m) for _, ph, z, m in pts if ph == "in"]
        pout = [(z, m) for _, ph, z, m in pts if ph in ("out", "out2")]
        cin, nin = fit_cpd(pin)
        cout, nout = fit_cpd(pout)
        zin = next((z for z, m in pin if m is not None and abs(m) >= MID_I), None)
        zout = None
        for z, m in pout:
            if m is not None and abs(m) >= MID_I:
                zout = z
        onset = next(((t, z) for t, ph, z, m in pts
                      if ph == "in" and m is not None and abs(m) >= TARGET), None)
        per.append(dict(cycle=c, cpd_in=cin, n_in=nin, cpd_out=cout, n_out=nout,
                        hyst=None if (zin is None or zout is None) else zin - zout,
                        onset=onset,
                        snap_rows=sum(1 for _, ph, _, _ in pts if ph == "snap")))
    # watchdog events = maximal runs of consecutive snap rows anywhere in the file
    events, prev = 0, False
    for _, _, ph, _, _ in rows:
        if ph == "snap" and not prev:
            events += 1
        prev = (ph == "snap")
    ins = [r["cpd_in"] for r in per if r["cpd_in"]]
    outs = [r["cpd_out"] for r in per if r["cpd_out"]]
    hys = [r["hyst"] for r in per if r["hyst"] is not None]
    ons = [r["onset"] for r in per if r["onset"]]
    drift = None
    if len(ons) >= 3:
        f = ols([a for a, _ in ons], [float(b) for _, b in ons])
        drift = f["slope"]
    return per, dict(cycles=len(per),
                     cpd_in=st.median(ins) if ins else None, n_in=len(ins),
                     cpd_out=st.median(outs) if outs else None, n_out=len(outs),
                     hyst=st.median(hys) if hys else None, n_hyst=len(hys),
                     hyst_min=min(hys) if hys else None, hyst_max=max(hys) if hys else None,
                     cpd_in_min=min(ins) if ins else None, cpd_in_max=max(ins) if ins else None,
                     drift=drift, snap_rows=sum(r["snap_rows"] for r in per),
                     watchdog_events=events, onsets=ons)


def one_step_snaps(rows):
    """Onsets that went from under the 1,000-count target to over it in a single Z step.

    Counted over IN-phase points only, consecutive within one cycle, as the session log's
    '1 of 110 onsets was a one-step snap' claim requires.
    """
    out = []
    by_cycle = {}
    for t, c, ph, z, m in rows:
        if c >= 1 and ph == "in":
            by_cycle.setdefault(c, []).append((t, z, m))
    for c, pts in sorted(by_cycle.items()):
        for (t0, z0, m0), (t1, z1, m1) in zip(pts, pts[1:]):
            if m0 is None or m1 is None:
                continue
            if abs(m0) < TARGET <= abs(m1) and abs(m0) < 100:
                out.append((c, t1, z0, z1, m0, m1))
                break
    return out


def main():
    plt = style()
    results = {}

    section("1. PER-RUN SUMMARY, RE-DERIVED FROM THE CSVs")
    print("  %-28s %6s %8s %8s %8s %7s %7s %9s"
          % ("run", "cycles", "cpd in", "cpd out", "hyst", "snaprow", "wdog", "drift/s"))
    total_cycles = 0
    for fname, label, code, included, clock in RUNS:
        rows = read_ztest(data_path("2026-09-19-morning", fname))
        per, s = analyse(rows)
        results[label] = (fname, code, included, per, s, rows)
        if included:
            total_cycles += s["cycles"]
        print("  %-28s %6d %8s %8s %8s %7d %7d %9s%s"
              % (label, s["cycles"],
                 "%.0f" % s["cpd_in"] if s["cpd_in"] else "-",
                 "%.0f" % s["cpd_out"] if s["cpd_out"] else "-",
                 "%.0f" % s["hyst"] if s["hyst"] is not None else "-",
                 s["snap_rows"], s["watchdog_events"],
                 "%+.0f" % s["drift"] if s["drift"] is not None else "-",
                 "" if included else "   <- excluded by the session log"))
    print("  cycles in the five included runs: %d" % total_cycles)

    section("2. AGAINST WHAT THE SESSION LOG AND docs/FACTS.md STATE")
    print("  %-28s %-22s %-22s %s" % ("run", "quantity", "log / re-derived", "verdict"))
    disagreements = []
    for label, (cin, cout, hy, wd, dr) in LOG.items():
        _, _, _, per, s, _ = results[label]
        for name, logv, mine, tol in [
            ("counts per decade in", cin, s["cpd_in"], 1.0),
            ("counts per decade out", cout, s["cpd_out"], 1.0),
            ("hysteresis (counts)", hy, s["hyst"], 1.0),
            ("watchdog events", wd, s["watchdog_events"], 0.5),
            ("onset drift (counts/s)", dr, s["drift"], 1.0),
        ]:
            ok = mine is not None and abs(mine - logv) <= tol
            if not ok:
                disagreements.append((label, name, logv, mine))
            print("  %-28s %-22s %10s / %-10s %s"
                  % (label, name, logv,
                     "%.1f" % mine if mine is not None else "None",
                     "MATCH" if ok else "DIFFERS"))
    if disagreements:
        print("\n  DISAGREEMENTS (log value, re-derived):")
        for d in disagreements:
            print("    %s | %s | %s vs %s" % d)
    else:
        print("\n  Every published Z-test number reproduces exactly.")

    section("3. THE HYSTERESIS CLAIM: 705 to 1,868 counts in EVERY run")
    med = {}
    for fname, label, code, included, clock in RUNS:
        if not included:
            continue
        _, _, _, per, s, _ = results[label]
        med[label] = s["hyst"]
        hys = [r["hyst"] for r in per if r["hyst"] is not None]
        pos = sum(1 for h in hys if h > 0)
        print("  %-28s median %+7.0f  n %2d  range %+7.0f to %+7.0f  positive in %d of %d cycles"
              % (label, s["hyst"], len(hys), min(hys), max(hys), pos, len(hys)))
    vals = [v for v in med.values() if v is not None]
    print("  ACROSS THE FIVE RUNS: min %+.0f, max %+.0f  (the log says 705 to 1,868)"
          % (min(vals), max(vals)))
    print("  All five run medians positive: %s" % all(v > 0 for v in vals))

    section("4. DOES THE HYSTERESIS SHRINK AT +-0.1 V AGAINST +-0.5 V?")
    print("  This is the claim that the hysteresis is NOT the applied bias pulling the")
    print("  gold in. If it were electrostatic the force goes as V^2, so +-0.1 V should")
    print("  give 25x less than +-0.5 V.")
    lowV = ["-0.1 V", "+0.1 V"]
    highV = ["-0.5 V (run 1, 30 cycles)", "+0.5 V", "-0.5 V (repeat, 20 cycles)"]
    lo_meds = [med[k] for k in lowV]
    hi_meds = [med[k] for k in highV]
    print("  +-0.1 V run medians: %s  (mean %.0f)"
          % (", ".join("%.0f" % v for v in lo_meds), st.mean(lo_meds)))
    print("  +-0.5 V run medians: %s  (mean %.0f)"
          % (", ".join("%.0f" % v for v in hi_meds), st.mean(hi_meds)))
    print("  ratio of means (0.1 V / 0.5 V): %.2f   V^2 scaling would predict 0.04"
          % (st.mean(lo_meds) / st.mean(hi_meds)))
    # per-cycle, pooled, Mann-Whitney U on the two groups
    lo_cycles, hi_cycles = [], []
    for k in lowV:
        lo_cycles += [r["hyst"] for r in results[k][3] if r["hyst"] is not None]
    for k in highV:
        hi_cycles += [r["hyst"] for r in results[k][3] if r["hyst"] is not None]
    try:
        from scipy.stats import mannwhitneyu
        u, p = mannwhitneyu(lo_cycles, hi_cycles, alternative="two-sided")
        print("  pooled per-cycle: +-0.1 V n=%d median %.0f | +-0.5 V n=%d median %.0f"
              % (len(lo_cycles), st.median(lo_cycles), len(hi_cycles), st.median(hi_cycles)))
        print("  Mann-Whitney U two-sided p = %.3f  (no direction assumed)" % p)
        print("  NOTE: cycles inside one run are REPEATED MEASUREMENTS of the same contact,")
        print("        not independent observations. Treat this p as descriptive only;")
        print("        n for INDEPENDENT runs is 2 at +-0.1 V and 3 at +-0.5 V.")
    except Exception as e:                                         # pragma: no cover
        print("  scipy unavailable (%s); run medians above are the statement" % e)

    section("5. ONE-STEP SNAPS - 'gradual in 109 of 110 onsets'")
    tot_on, tot_snap = 0, 0
    for fname, label, code, included, clock in RUNS:
        if not included:
            continue
        _, _, _, per, s, rows = results[label]
        snaps = one_step_snaps(rows)
        tot_on += s["cycles"]
        tot_snap += len(snaps)
        for c, t, z0, z1, m0, m1 in snaps:
            print("  %-28s cycle %d at t %.2f s: Z %d -> %d, %.1f -> %.1f counts"
                  % (label, c, t, z0, z1, m0, m1))
    print("  one-step snaps %d in %d cycles across the five included runs" % (tot_snap, tot_on))
    ex_rows = results["-0.5 V (12:50, EXCLUDED)"][5]
    ex_snaps = one_step_snaps(ex_rows)
    print("  the EXCLUDED 12:50 run: %d one-step snaps in %d cycles"
          % (len(ex_snaps), results["-0.5 V (12:50, EXCLUDED)"][4]["cycles"]))
    for c, t, z0, z1, m0, m1 in ex_snaps:
        print("    cycle %d at t %.2f s: Z %d -> %d, %.1f -> %.1f counts" % (c, t, z0, z1, m0, m1))

    section("6. HOW FAR THE COUNTS-PER-DECADE DRIFTS INSIDE ONE RUN")
    for fname, label, code, included, clock in RUNS:
        if not included:
            continue
        _, _, _, per, s, _ = results[label]
        ins = [(r["cycle"], r["cpd_in"]) for r in per if r["cpd_in"]]
        if len(ins) >= 6:
            first = st.median([v for c, v in ins[:len(ins) // 3]])
            last = st.median([v for c, v in ins[-len(ins) // 3:]])
            print("  %-28s first third median %7.0f, last third %7.0f, ratio %.2fx  "
                  "(per-cycle range %.0f to %.0f)"
                  % (label, first, last, max(first, last) / min(first, last),
                     s["cpd_in_min"], s["cpd_in_max"]))

    # ------------------------------------------------------------ figures
    section("7. FIGURES")

    # fig03: the IN and OUT curves of the -0.5 V run 1, a handful of cycles
    rows = results["-0.5 V (run 1, 30 cycles)"][5]
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.6), sharey=True)
    for ax, phases, title in [(axes[0], ("in",), "going IN  (Z toward the sample)"),
                              (axes[1], ("out", "out2"), "coming OUT  (Z retracting)")]:
        shown = 0
        for c in [6, 10, 14, 18, 22]:
            # Below about 30 counts the reading is the amplifier noise floor, not the
            # junction, so those points are dropped rather than plotted as signal.
            pts = [(z, abs(m)) for t, cc, ph, z, m in rows
                   if cc == c and ph in phases and m is not None and abs(m) >= 30]
            if len(pts) < 5:
                continue
            z0 = min(z for z, _ in pts)
            ax.semilogy([z - z0 for z, _ in pts], [i for _, i in pts],
                        color=SERIES[shown % len(SERIES)], marker=".", ms=2.5, lw=1.0,
                        label="cycle %d" % c)
            shown += 1
        ax.axhspan(FIT_LO, FIT_HI, color=TOL["grey"], alpha=0.25, zorder=0)
        ax.set_ylim(30, 3e4)
        ax.set_xlim(-50, 2600)
        ax.set_xlabel("Z DAC code, relative to the start of the sweep (counts)")
        ax.set_title(title)
        ax.legend(loc="lower right", ncol=2, frameon=True, framealpha=0.85,
                  edgecolor="none", facecolor="white")
    axes[0].set_ylabel("|ADC reading| (counts)")
    axes[0].text(0.03, 0.97, "shaded: the 100-1,000 count band the slope is fitted over\n"
                 "readings under 30 counts are the amplifier noise floor and are not shown",
                 transform=axes[0].transAxes, fontsize=7, va="top", color="#555555")
    fig.suptitle("Current against Z at sample $-$0.5 V, 2026-09-19 morning: "
                 "a decade takes thousands of counts, not tens", y=1.03, fontsize=10)
    save(fig, "fig03_ztest_curves.png")
    plt.close(fig)

    # fig04: hysteresis per cycle, all five runs
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    labels, data = [], []
    for fname, label, code, included, clock in RUNS:
        if not included:
            continue
        per = results[label][3]
        hys = [r["hyst"] for r in per if r["hyst"] is not None]
        labels.append("%s\nn = %d cycles" % (label.replace(" (", "\n("), len(hys)))
        data.append(hys)
    bp = ax.boxplot(data, widths=0.55, showfliers=False, patch_artist=True,
                    medianprops=dict(color=TOL["black"], lw=1.6))
    for patch, c in zip(bp["boxes"], SERIES):
        patch.set_facecolor(c)
        patch.set_alpha(0.45)
        patch.set_edgecolor(c)
    for i, hys in enumerate(data, start=1):
        xs = [i + (j % 7 - 3) * 0.035 for j in range(len(hys))]
        ax.scatter(xs, hys, s=9, color=TOL["black"], alpha=0.5, zorder=3)
    ax.axhline(0, color=TOL["red"], lw=1.2, ls="--", label="zero: a clean tunnelling gap")
    ax.set_xticklabels(labels, fontsize=7.5)
    ax.set_ylabel("in/out hysteresis (Z counts)")
    ax.set_title("The current persists further out than it began in, at every bias\n"
                 "each dot one cycle; box = quartiles, bar = median")
    ax.legend(loc="upper left")
    save(fig, "fig04_ztest_hysteresis.png")
    plt.close(fig)

    # fig05: counts per decade by bias, in and out. Log scale, because the point is a
    # factor of a hundred or more against the tunnelling expectation.
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    order = ["-0.1 V", "+0.1 V", "-0.5 V (run 1, 30 cycles)",
             "-0.5 V (repeat, 20 cycles)", "+0.5 V"]
    short = ["$-$0.1 V", "+0.1 V", "$-$0.5 V\nrun 1", "$-$0.5 V\nrepeat", "+0.5 V"]
    xs = list(range(len(order)))
    ins = [results[k][4]["cpd_in"] for k in order]
    outs = [results[k][4]["cpd_out"] for k in order]
    w = 0.36
    ax.set_yscale("log")
    ax.bar([x - w / 2 for x in xs], ins, w, color=TOL["blue"], label="going in", zorder=3)
    ax.bar([x + w / 2 for x in xs], outs, w, color=TOL["red"], label="coming out", zorder=3)
    for x, v in zip(xs, ins):
        ax.text(x - w / 2, v * 1.08, "%.0f" % v, ha="center", fontsize=7.5)
    for x, v in zip(xs, outs):
        ax.text(x + w / 2, v * 1.08, "%.0f" % v, ha="center", fontsize=7.5)
    ax.axhspan(6, 13, color=TOL["green"], alpha=0.35, zorder=1)
    ax.text(len(order) - 0.45, 9, "vacuum tunnelling would be 6-13 counts\n"
            "(inherited Z scale, itself unmeasured)",
            fontsize=7.5, color=TOL["green"], ha="right", va="center")
    ax.set_ylim(4, 40000)
    ax.set_xticks(xs)
    ax.set_xticklabels(short, fontsize=8)
    ax.set_ylabel("Z counts per decade of current\n(run median, log scale)")
    ax.set_title("How far Z has to move for the current to change tenfold\n"
                 "2026-09-19 morning, 110 cycles over five runs")
    ax.legend(loc="upper left")
    save(fig, "fig05_ztest_cpd_by_bias.png")
    plt.close(fig)

    # fig06: onset Z against time, every run - the drift
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    for i, (fname, label, code, included, clock) in enumerate(
            [r for r in RUNS if r[3]]):
        s = results[label][4]
        ons = s["onsets"]
        if not ons:
            continue
        ax.plot([t for t, _ in ons], [z for _, z in ons], marker="o", ms=3.5, lw=1.0,
                color=SERIES[i % len(SERIES)],
                label="%s  (%+.0f counts/s)" % (label, s["drift"]))
    ax.set_xlabel("time within the run (s)")
    ax.set_ylabel("Z code at which the current first reached 1,000 counts")
    ax.set_title("Where the contact is, cycle by cycle\n"
                 "the slope is the gold's drift toward or away from the tip")
    ax.legend(loc="upper right", fontsize=7)
    save(fig, "fig06_ztest_drift.png")
    plt.close(fig)

    return results


if __name__ == "__main__":
    main()
