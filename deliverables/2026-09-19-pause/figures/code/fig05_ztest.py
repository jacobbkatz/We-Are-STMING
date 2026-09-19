"""Figure 5 - what the junction actually is, measured over 110 cycles and four biases.

    python3 deliverables/2026-09-19-pause/figures/code/fig05_ztest.py

WHAT THE TEST DOES. At a fixed X and Y, walk Z toward the sample 4 counts at a time until
the current reaches 1,000 counts, then walk it back out. Repeat. A tunnelling gap and a
pressed contact answer this completely differently, and the answer is a number: how many
Z counts it takes for the current to change ten-fold.

SOURCE. `sessions/data/2026-09-19-morning/ztest_1789822585.csv` (30 cycles, sample -0.5 V)
and `bias_m01V_/p05V_/p01V_/m05V_1789822770.csv` (20 cycles each, the four other biases),
measured 2026-09-19 12:56-13:05 UTC; `sessions/2026-09-19-morning.md` sections 3.10-3.11.
Every figure on this chart is recomputed here with the same statistics the bench script
used (`sessions/data/2026-09-19-morning/scripts/ztest.py`: a straight-line fit of
log10|I| against Z over 100 <= |I| <= 1,000 counts, in and out separately; hysteresis is
the Z where the current first passed 300 counts going in, minus where it last fell below
300 coming out). The medians reproduce the session log exactly.

THE COMPARISON, and its limit. A tunnelling current changes ten-fold per 1-2 Angstrom.
At the Z scale this project inherited from Dan Berard's scanner - 0.016 nm per count,
which has NEVER been measured on our hardware - that is 6-13 counts. It is drawn as a
calculated band and labelled as one. The HYSTERESIS result does not depend on that scale
at all: it is a difference in Z counts, measured directly.

NO DISTANCE SCALE APPEARS ON THIS FIGURE, because this instrument has never established
one from its own hardware.
"""
from __future__ import annotations

import csv
import math
import os
import statistics as st
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stmstyle as S  # noqa: E402

SESSION = "2026-09-19-morning"
# (label, file, cycles as the session log records them)
RUNS = [
    ("sample −0.5 V", "ztest_1789822585.csv", 30),
    ("sample −0.1 V", "bias_m01V_1789822770.csv", 20),
    ("sample +0.5 V", "bias_p05V_1789822770.csv", 20),
    ("sample +0.1 V", "bias_p01V_1789822770.csv", 20),
    ("sample −0.5 V, repeat", "bias_m05V_1789822770.csv", 20),
]

FIT_LO, FIT_HI, MID_I = 100, 1000, 300      # ztest.py's own constants
TUNNEL_LO, TUNNEL_HI = 6, 13                # counts per decade, CALC, docs/FACTS.md


def read(path):
    rows = []
    with open(path) as f:
        for r in csv.DictReader(f):
            m = r["adc"]
            rows.append((float(r["t"]), int(r["cycle"]), r["phase"], int(r["z"]),
                         None if m in ("", "None") else float(m)))
    return rows


def fit_cpd(pts):
    """Counts per decade from (z, I), over the fit window. ztest.py fit_cpd, verbatim."""
    p = [(z, math.log10(abs(i))) for z, i in pts
         if i is not None and FIT_LO <= abs(i) <= FIT_HI]
    if len(p) < 3:
        return None
    zs = [a for a, _ in p]
    ls = [b for _, b in p]
    zm, lm = st.mean(zs), st.mean(ls)
    sxx = sum((z - zm) ** 2 for z in zs)
    if sxx == 0:
        return None
    slope = sum((z - zm) * (l - lm) for z, l in zip(zs, ls)) / sxx
    return 1.0 / abs(slope) if slope else None


def per_cycle(rows):
    cyc = {}
    for t, c, ph, z, m in rows:
        if c >= 1:
            cyc.setdefault(c, []).append((t, ph, z, m))
    out = []
    for c, pts in sorted(cyc.items()):
        pin = [(z, m) for _t, ph, z, m in pts if ph == "in"]
        pout = [(z, m) for _t, ph, z, m in pts if ph in ("out", "out2")]
        zin = next((z for z, m in pin if m is not None and abs(m) >= MID_I), None)
        zout = None
        for z, m in pout:
            if m is not None and abs(m) >= MID_I:
                zout = z
        out.append(dict(cycle=c, pin=pin, pout=pout,
                        cpd_in=fit_cpd(pin), cpd_out=fit_cpd(pout),
                        hyst=None if zin is None or zout is None else zin - zout,
                        zin=zin, zout=zout))
    return out


def med(vals):
    v = [x for x in vals if x is not None]
    return st.median(v) if v else None


def main():
    summary = []
    for label, name, cycles in RUNS:
        cs = per_cycle(read(S.data_path(SESSION, name)))
        s = dict(label=label, file=name, cycles=cycles,
                 cpd_in=med([c["cpd_in"] for c in cs]),
                 cpd_out=med([c["cpd_out"] for c in cs]),
                 hyst=med([c["hyst"] for c in cs]), cyc=cs)
        summary.append(s)
        print("%-24s in %7.0f   out %7.0f   hysteresis %6.0f   (%d cycles in file)"
              % (label, s["cpd_in"], s["cpd_out"], s["hyst"], len(cs)))
    total = sum(len(s["cyc"]) for s in summary)
    print("total cycles across all five runs: %d" % total)
    print("hysteresis range across runs: %.0f to %.0f counts"
          % (min(s["hyst"] for s in summary), max(s["hyst"] for s in summary)))

    # The cycle shown in panel A is chosen by a rule, not by taste: the one whose three
    # numbers sit closest to its run's medians, summed as relative deviations.
    run0 = summary[0]

    def deviation(c):
        return (abs(c["cpd_in"] - run0["cpd_in"]) / run0["cpd_in"]
                + abs(c["cpd_out"] - run0["cpd_out"]) / run0["cpd_out"]
                + abs(c["hyst"] - run0["hyst"]) / abs(run0["hyst"]))

    pick = min((c for c in run0["cyc"]
                if c["cpd_in"] and c["cpd_out"] and c["hyst"] is not None),
               key=deviation)
    print("panel A shows cycle %d of %s: in %.0f, out %.0f, hysteresis %s"
          % (pick["cycle"], run0["file"], pick["cpd_in"], pick["cpd_out"], pick["hyst"]))

    S.set_theme("light")
    fig, (ax, axb) = S.plt.subplots(1, 2, figsize=(11.2, 6.6), width_ratios=[1.12, 1.0])
    fig.subplots_adjust(top=0.755, bottom=0.265, left=0.070, right=0.985, wspace=0.30)

    c_in, c_out = S.series(0), S.series(1)

    # ---- panel A: one cycle, in and out ---------------------------------------------
    def clean(pts):
        return [(z, abs(m)) for z, m in pts if m is not None and abs(m) >= 20]

    zin_pts, zout_pts = clean(pick["pin"]), clean(pick["pout"])
    ax.plot([z for z, _ in zin_pts], [i for _, i in zin_pts], "-", color=c_in, lw=2.0,
            zorder=4)
    ax.plot([z for z, _ in zout_pts], [i for _, i in zout_pts], "-", color=c_out, lw=2.0,
            zorder=4)
    ax.set_yscale("log")
    ax.set_ylim(40, 2600)
    ax.set_yticks([50, 100, 200, 500, 1000, 2000])
    ax.set_yticklabels(["50", "100", "200", "500", "1,000", "2,000"])

    zs = [z for z, _ in zin_pts + zout_pts]
    lo, hi = min(zs), max(zs)
    padx = 0.10 * (hi - lo)
    ax.set_xlim(lo - padx, hi + padx * 1.9)

    # What a tunnelling gap would require, drawn from the same starting point.
    z0 = pick["zin"] if pick["zin"] is not None else (lo + hi) / 2
    ends = (40, 2600)
    for cpd in (TUNNEL_LO, TUNNEL_HI):
        zz = [z0 + cpd * math.log10(v / float(MID_I)) for v in ends]
        ax.plot(zz, list(ends), "-", color=S.series(2), lw=2.6, zorder=6)
    ax.fill_betweenx(list(ends),
                     [z0 + TUNNEL_LO * math.log10(v / float(MID_I)) for v in ends],
                     [z0 + TUNNEL_HI * math.log10(v / float(MID_I)) for v in ends],
                     color=S.series(2), alpha=0.35, zorder=5)

    ax.axhline(MID_I, color=S.C["axis"], lw=1.0, zorder=2)
    if pick["zin"] is not None and pick["zout"] is not None:
        ax.annotate("", xy=(pick["zin"], MID_I), xytext=(pick["zout"], MID_I),
                    arrowprops=dict(arrowstyle="<->", color=S.C["ink"], lw=1.7), zorder=7)
        S.key(ax, (pick["zin"] + pick["zout"]) / 2.0, MID_I * 1.22,
              "hysteresis\n%d counts" % pick["hyst"], ha="center", va="bottom")

    S.tidy(ax, xlabel="Z piezo counts (higher is toward the sample)",
           ylabel="Current at the tip (ADC counts, log scale)", grid="both")
    S.thousands(ax, "x")
    ax.set_title("One cycle, chosen as the one closest to the run's median slope.\n"
                 "Going in takes %.0f counts per ten-fold change; coming out, %.0f."
                 % (pick["cpd_in"], pick["cpd_out"]))
    S.key(ax, zin_pts[-1][0] + padx * 0.12, zin_pts[-1][1], "going in",
          ha="left", va="center", color=S.word(0))
    S.key(ax, zout_pts[0][0] + padx * 0.12, zout_pts[0][1], "coming out",
          ha="left", va="center", color=S.word(1))
    S.note(ax, z0 - (hi - lo) * 0.025, 2300,
           "a tunnelling gap would be\nthis steep: the green stripe\n"
           "is only 6\u201313 counts wide",
           ha="right", va="top", color=S.word(2))

    # ---- panel B: counts per decade, every run, against the tunnelling band ----------
    ys = list(range(len(summary)))[::-1]
    axb.axvspan(TUNNEL_LO, TUNNEL_HI, color=S.series(2), alpha=0.28, zorder=1)
    axb.axvline(TUNNEL_LO, color=S.series(2), lw=2.0, zorder=2)
    axb.axvline(TUNNEL_HI, color=S.series(2), lw=2.0, zorder=2)
    for y, s in zip(ys, summary):
        axb.plot([s["cpd_in"], s["cpd_out"]], [y, y], "-", color=S.C["grid"], lw=2.0,
                 zorder=3)
        axb.plot([s["cpd_in"]], [y], "o", color=c_in, ms=10,
                 markeredgecolor=S.C["surface"], markeredgewidth=2.0, zorder=5)
        axb.plot([s["cpd_out"]], [y], "o", color=c_out, ms=10,
                 markeredgecolor=S.C["surface"], markeredgewidth=2.0, zorder=5)
    axb.set_xscale("log")
    axb.set_xlim(4, 40000)
    axb.set_ylim(-1.05, len(summary) - 0.30)
    axb.set_yticks(ys)
    axb.set_yticklabels(["%s\n%d cycles" % (s["label"], s["cycles"]) for s in summary])
    axb.tick_params(axis="y", length=0)
    axb.spines["left"].set_visible(False)
    axb.set_xticks([10, 100, 1000, 10000])
    axb.set_xticklabels(["10", "100", "1,000", "10,000"])
    S.tidy(axb, xlabel="Z counts needed for the current to change ten-fold", grid="x")
    axb.set_title("Every run, both directions, against what tunnelling would need.\n"
                  "The gap is a factor of about a hundred to a thousand.")
    S.key(axb, summary[0]["cpd_in"], ys[0] + 0.30, "going in", ha="center", va="bottom",
          color=S.word(0))
    S.key(axb, summary[0]["cpd_out"] * 1.05, ys[0] + 0.30, "coming out", ha="left",
          va="bottom", color=S.word(1))
    S.note(axb, math.sqrt(TUNNEL_LO * TUNNEL_HI), -0.85,
           "6–13 counts:\ntunnelling, calculated", ha="center", va="center",
           fontsize=S.TYPE["small"], color=S.word(2))

    S.titles_keyed(
        fig,
        "We measured what the junction is: a pressed contact, not a tunnelling gap",
        "It takes between 800 and 4,600 Z counts to change the current ten-fold <going in>, where a tunnelling gap "
        "would need about ten.\n<Coming back out> it is shallower still, and the current lingers hundreds to "
        "thousands of counts further out than it appeared — the junction sticks.\nThe same answer came from "
        "110 cycles at four different bias voltages.",
        [{"color": S.word(0), "fontweight": S.W_EMPH},
         {"color": S.word(1), "fontweight": S.W_EMPH}])

    S.footer(fig, y=0.008, text=
             "Source: sessions/data/2026-09-19-morning/ztest_1789822585.csv (30 cycles) and "
             "bias_m01V_/p05V_/p01V_/m05V_1789822770.csv (20 cycles each), measured 2026-09-19 12:56–13:05 "
             "UTC; sessions/2026-09-19-morning.md sections 3.10–3.11.\n"
             "Every number is recomputed here with the bench script's own statistics (scripts/ztest.py) and the "
             "medians reproduce the session log exactly. The tip was the one fitted about 03:00 UTC that morning; "
             "the sample was the 2026-09-19 leaf-on-paper gold.\n"
             "WHAT THIS DOES NOT SHOW: the 6–13 count comparison is CALCULATED from a Z scale inherited from "
             "another builder's scanner and never measured on ours, so the size of the gap between measured and "
             "tunnelling depends on it. The hysteresis\nresult does not — it is a difference in Z counts, "
             "measured directly. The slope is not constant: within the first run the per-cycle value fell from "
             "about 2,090 to about 380, and per-cycle values across all runs span 233 to 22,990.\n"
             "\"A soft, pressed, sticky contact\" is the interpretation on record, and it is an interpretation, "
             "not a proof. For this tip and this sample only. No distance scale appears here, because this "
             "instrument has never established one.")

    S.save(fig, "fig05_ztest")


if __name__ == "__main__":
    main()
