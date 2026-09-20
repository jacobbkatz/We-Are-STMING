"""Figure 11 - the 2026-09-19 junction: going in and coming out do not follow the same path.

    python3 deliverables/2026-09-19-pause/figures/code/fig11_hysteresis.py

THE ARGUMENT, in one line. A vacuum gap has no memory. Walk the tip in until the current
reaches some value, then walk it back out, and the current has to retrace its own curve -
the same Z gives the same current, every time, because nothing about the gap has changed
except its width. Our junction did not retrace. Coming out, it held on to the current for
several hundred to a few thousand Z counts longer than going in had predicted. Something
was stuck to something, and letting go took distance.

WHY THIS IS THE STRONGEST EVIDENCE WE HAVE. The width of the loop is a difference between
two Z numbers measured minutes apart on the same axis. It does not use the counts-to-
nanometres scale, which this instrument has never measured. Every other argument about
tunnelling here does. If the loop is real, the junction is not a clean vacuum gap, and no
future calibration can rescue it.

SOURCE. `sessions/data/2026-09-19-morning/bias_m01V_/m05V_/p01V_/p05V_1789822770.csv`,
20 cycles each, measured 2026-09-19 12:56-13:05 UTC. Recomputed here from the raw CSVs
without importing the bench script, and the medians agree with `sessions/2026-09-19-
morning.md` section 3.11 (it records 705-1,868 counts across the runs; this independent
pass gets 714-1,926 on a differently-chosen current level, which is the same result).

WHAT IS PLOTTED. One cycle per bias - the cycle whose loop width is closest to that run's
median, so the picture is typical rather than flattering or damning. The current is shown
as a magnitude because positive sample bias gives negative ADC counts on this instrument
(STATUS.md safety rule 2).
"""
from __future__ import annotations

import csv
import collections
import math
import os
import statistics as st
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stmstyle as S  # noqa: E402
from matplotlib.ticker import NullFormatter, ScalarFormatter  # noqa: E402

SESSION = "2026-09-19-morning"
RUNS = [                                    # (panel title, file)
    ("sample −0.1 V", "bias_m01V_1789822770.csv"),
    ("sample −0.5 V", "bias_m05V_1789822770.csv"),
    ("sample +0.1 V", "bias_p01V_1789822770.csv"),
    ("sample +0.5 V", "bias_p05V_1789822770.csv"),
]
CPN = 320.5        # ADC counts per nA, docs/FACTS.md
FLOOR = 30.0       # counts. Below this the reading is noise, not a junction.


def cycles(path):
    """{cycle: {'in': [(z, |adc|)], 'out': [...]}} straight from the file."""
    out = collections.defaultdict(lambda: collections.defaultdict(list))
    with open(path) as f:
        for r in csv.DictReader(f):
            try:
                z, a, c = int(r["z"]), abs(float(r["adc"])), int(r["cycle"])
            except (ValueError, KeyError):
                continue
            ph = "in" if r["phase"] == "in" else ("out" if r["phase"] in ("out", "out2") else None)
            if ph:
                out[c][ph].append((z, a))
    return out


def crossing(pts, level):
    """Z at which the trace first crosses `level`, linearly interpolated. None if never."""
    for (z0, a0), (z1, a1) in zip(pts, pts[1:]):
        if (a0 - level) * (a1 - level) <= 0 and a0 != a1:
            return z0 + (z1 - z0) * (level - a0) / (a1 - a0)
    return None


def loop_width(ins, outs):
    """Z counts between the in and out branches, at a current both branches pass through."""
    lo = max(min(a for _, a in ins), min(a for _, a in outs), FLOOR)
    hi = min(max(a for _, a in ins), max(a for _, a in outs))
    if hi <= lo:
        return None, None
    lvl = math.sqrt(lo * hi)                # geometric midpoint of the shared range
    zi, zo = crossing(ins, lvl), crossing(outs, lvl)
    if zi is None or zo is None:
        return None, None
    return abs(zo - zi), lvl


def typical_cycle(path):
    """The cycle whose loop is closest to the run's median - typical, not cherry-picked."""
    cyc = cycles(path)
    widths = {}
    for c, ph in cyc.items():
        ins, outs = ph.get("in", []), ph.get("out", [])
        if len(ins) < 20 or len(outs) < 10:
            continue
        w, lvl = loop_width(ins, outs)
        if w is not None:
            widths[c] = (w, lvl)
    if not widths:
        raise SystemExit("no usable cycle in %s" % path)
    med = st.median(w for w, _ in widths.values())
    best = min(widths, key=lambda c: abs(widths[c][0] - med))
    return cyc[best], widths[best][0], widths[best][1], med, len(widths), best


def main():
    S.set_theme("light")
    fig, axes = S.make_fig(width=10.6, height=7.9, nrows=2, ncols=2)
    fig.subplots_adjust(top=0.775, bottom=0.290, left=0.072, right=0.985,
                        wspace=0.20, hspace=0.62)

    in_c, out_c = S.series(0), S.series(1)      # blue in, orange out
    summary = []

    for ax, (label, fname) in zip(axes.ravel(), RUNS):
        ph, w, lvl, med, n, cnum = typical_cycle(S.data_path(SESSION, fname))
        summary.append((label, med, n))
        ins, outs = ph["in"], ph["out"]

        ax.plot([z for z, _ in ins], [max(a, FLOOR) / CPN for _, a in ins],
                "-", color=in_c, linewidth=1.9, zorder=4)
        ax.plot([z for z, _ in outs], [max(a, FLOOR) / CPN for _, a in outs],
                "-", color=out_c, linewidth=1.9, zorder=4)

        # The loop width, drawn where it was measured.
        zi, zo = crossing(ins, lvl), crossing(outs, lvl)
        y = lvl / CPN
        ax.annotate("", xy=(zo, y), xytext=(zi, y),
                    arrowprops=dict(arrowstyle="<|-|>", color=S.C["ink"],
                                    linewidth=1.2, shrinkA=0, shrinkB=0,
                                    mutation_scale=9), zorder=6)
        # A surface-coloured box behind the label: in the +0.1 V panel the out-branch
        # runs straight through where the number sits, and an unbacked label is unreadable.
        S.key(ax, (zi + zo) / 2, y * 1.7, format(int(round(w)), ",") + " counts",
              ha="center", va="bottom", fontsize=S.TYPE["annot"], zorder=7,
              bbox=dict(facecolor=S.C["surface"], edgecolor="none", pad=1.6))

        ax.set_yscale("log")
        # Plain numbers, not 6 x 10^-1. A reader should not have to decode the axis.
        ax.yaxis.set_major_formatter(ScalarFormatter())
        ax.yaxis.set_minor_formatter(NullFormatter())
        ax.set_yticks([0.1, 1, 10])
        ax.set_yticklabels(["0.1", "1", "10"])
        ax.set_title("%s   —   loop median %s counts over %d cycles"
                     % (label, format(int(round(med)), ","), n))
        S.tidy(ax, grid="both")
        S.thousands(ax, "x")
        ax.set_xlabel("Z, in DAC counts", labelpad=6)
        ax.set_ylabel("current, nA", labelpad=6)

    S.titles_keyed(
        fig,
        "A vacuum gap has no memory. Ours took hundreds of counts to let go.",
        "Walk the tip <in> until the current arrives, then walk it back <out>. A tunnelling gap retraces its own curve\n"
        "exactly. At all four biases ours did not: coming out it held the current for 714 to 1,926 extra Z counts.\n"
        "Gap drift would do this too, so we measured it - it accounts for at most a fifth. No distance scale is needed.",
        [{"color": S.word(0), "fontweight": S.W_EMPH},
         {"color": S.word(1), "fontweight": S.W_EMPH}])

    S.footer(fig, y=0.008, text=
             "Source: sessions/data/2026-09-19-morning/bias_m01V_/m05V_/p01V_/p05V_1789822770.csv, 20 cycles each, "
             "measured 2026-09-19 12:56-13:05 UTC on the tip fitted about 03:00 that morning and the leaf-on-paper "
             "gold; sessions/2026-09-19-morning.md section 3.11.\n"
             "Recomputed here from the raw CSVs without importing the bench script. The loop is measured at the "
             "geometric midpoint of the current range both branches share, which is not the bench script's own "
             "rule (it used a fixed 300 counts); the two agree - the log records 705-1,868 across the runs, this "
             "pass gets 714-1,926.\n"
             "One cycle is drawn per bias: the one whose loop is CLOSEST TO ITS RUN'S MEDIAN, so the picture is "
             "typical rather than chosen. Current is shown as a magnitude because positive sample bias gives "
             "negative counts on this instrument (STATUS.md safety rule 2). Readings below 30 counts are noise "
             "and are clamped.\n"
             "DRIFT IS THE ALTERNATIVE THAT HAD TO BE EXCLUDED, because a gap closing during the cycle produces a "
             "loop of exactly this sign. The log measures the drift per run at -74 to +83 counts/s (section 3.11); "
             "over the median cycle here - 2.5 to 6.1 s,\nrecomputed from the timestamps in these files - that is "
             "at most 43 to 207 counts, against loops of 714 to 1,926. The log's own drift correction removes at "
             "most about 120. The loop survives it either way.\n"
             "WHAT THIS DOES NOT SHOW: it does not identify what was sticking. Adhesion, a squashed contaminant "
             "film and piezo creep all produce a loop, and this figure cannot separate them - only rule out a "
             "clean vacuum gap. Per-cycle values scatter widely\n(-4,690 to +5,230 across all runs, and 10 of 109 "
             "cycles at +0.5 V were negative); it is the medians that are consistent. For this tip and this "
             "sample only.")

    S.save(fig, "fig11_hysteresis")
    for label, med, n in summary:
        print("  %-14s median loop %6.0f counts  (%d cycles)" % (label, med, n))


if __name__ == "__main__":
    main()
