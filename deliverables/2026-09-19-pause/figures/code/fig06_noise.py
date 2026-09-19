"""Figure 6 - the noise floor, and what actually sets it.

    python3 deliverables/2026-09-19-pause/figures/code/fig06_noise.py

SOURCE. `sessions/data/2026-09-19-bench/still.csv` (room still) and `stamp.csv` (someone
stamping on the floor about 2 m away), each 10 s of `ADCR` readings at about 3.7 kHz,
measured 2026-09-19 00:54-02:25 UTC with the TIP CLEAR. Written up in
`sessions/2026-09-19-bench.md` section 3.3 and `sessions/data/2026-09-19-bench/README.md`.

WHAT THE STILL-VERSUS-STAMPING PAIR TESTS. With the tip clear there is no junction, so
nothing mechanical can reach the amplifier through the tunnel gap. The pair therefore
tests ELECTRICAL pickup only: whether footsteps get into the measurement through the
mains, the cabling or the ground. They do not. It says nothing about whether footsteps
move the gap, which is a different question and figure 3's.

TIMEBASE. The recorded timestamps are close to uniform but not exactly so (median
0.271 ms, 5th to 95th percentile 0.24 to 0.38 ms). The series is linearly interpolated
onto a uniform grid at the median rate before the spectrum is computed, which is stated
in the caption; the jitter smears the highest frequencies and does not affect the mains
peaks.

WHICH NIGHT, WHICH TIP. These are 2026-09-19 tip-clear numbers. The 2026-09-18 figures of
341-350 counts belong to a different night and a different tip, and tools still quote
them; do not mix them.
"""
from __future__ import annotations

import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stmstyle as S  # noqa: E402

SESSION = "2026-09-19-bench"
PA_PER_COUNT = 3.125          # docs/FACTS.md, "Current per ADC count", CALC 2026-09-07
MAINS = 60.0                  # measured here, not assumed: the largest peak in both files


def read(name):
    import numpy as np
    t, v = [], []
    with open(S.data_path(SESSION, name)) as f:
        for r in csv.DictReader(f):
            t.append(float(r["t_s"]))
            v.append(float(r["adcr"]))
    return np.array(t), np.array(v)


def spectrum(t, v):
    import numpy as np
    from scipy import signal
    fs = 1.0 / float(np.median(np.diff(t)))
    grid = np.arange(t[0], t[-1], 1.0 / fs)
    vu = np.interp(grid, t, v)
    f, p = signal.welch(vu - vu.mean(), fs=fs, nperseg=4096)
    return f[1:], np.sqrt(p[1:]), fs      # drop DC


def main():
    import numpy as np

    runs = [("room still", "still.csv", S.series(0), S.word(0)),
            ("someone stamping, about 2 m away", "stamp.csv", S.series(1), S.word(1))]
    data = {}
    for label, name, col, wcol in runs:
        t, v = read(name)
        f, asd, fs = spectrum(t, v)
        data[name] = dict(label=label, t=t, v=v, f=f, asd=asd, fs=fs,
                          sd=float(np.std(v)), n=len(v),
                          dur=float(t[-1] - t[0]))
        print("%-32s n=%d  %.1f s  %.0f Hz  sd %.1f counts (%.0f pA)"
              % (label, len(v), t[-1] - t[0], fs, np.std(v), np.std(v) * PA_PER_COUNT))
        for target in (MAINS, 3 * MAINS, 5 * MAINS):
            k = int(np.argmin(np.abs(f - target)))
            print("      %5.0f Hz: %.2f counts/sqrt(Hz)" % (f[k], asd[k]))

    S.set_theme("light")
    fig, (ax, axh) = S.plt.subplots(1, 2, figsize=(11.0, 6.2), width_ratios=[1.62, 1.0])
    fig.subplots_adjust(top=0.760, bottom=0.250, left=0.068, right=0.900, wspace=0.26)

    # ---- panel A: the spectrum ------------------------------------------------------
    for label, name, col, wcol in runs:
        d = data[name]
        ax.plot(d["f"], d["asd"], "-", color=col, lw=1.3, alpha=0.9, zorder=4)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(2, 1900)
    ax.set_ylim(0.15, 12)
    ax.set_xticks([10, 60, 100, 180, 300, 1000])
    ax.set_xticklabels(["10", "60", "100", "180", "300", "1,000"])
    ax.set_yticks([0.2, 0.5, 1, 2, 5, 10])
    ax.set_yticklabels(["0.2", "0.5", "1", "2", "5", "10"])
    S.tidy(ax, xlabel="Frequency (Hz)",
           ylabel="Noise at the tip (ADC counts per √Hz)", grid="both")

    sec = ax.secondary_yaxis("right",
                             functions=(lambda c: c * PA_PER_COUNT,
                                        lambda a: a / PA_PER_COUNT))
    sec.set_ylabel("the same noise, in picoamps per √Hz", color=S.C["muted"],
                   fontsize=S.TYPE["annot"], labelpad=12)
    sec.tick_params(colors=S.C["muted"], labelsize=S.TYPE["small"])
    sec.spines["right"].set_color(S.C["axis"])

    for k, h in enumerate((1, 3, 5)):
        ax.axvline(MAINS * h, color=S.C["grid"], lw=1.0, zorder=1)
    S.key(ax, MAINS, 9.6, "60 Hz mains\nand its odd harmonics", ha="center", va="bottom",
          fontsize=S.TYPE["small"])
    d0 = data["still.csv"]
    S.key(ax, 700, float(np.median(d0["asd"][d0["f"] > 400])) * 2.4,
          "room still", ha="center", va="bottom", color=S.word(0))
    S.key(ax, 6.5, 2.6, "someone stamping", ha="left", va="bottom", color=S.word(1))
    ax.set_title("The floor is not getting in electrically: the two traces lie on top of "
                 "each other.\nWhat is left is mains pickup on a few sharp lines, not "
                 "broadband amplifier noise.")

    # ---- panel B: the readings themselves -------------------------------------------
    bins = np.arange(-180, 182, 8)
    for label, name, col, wcol in runs:
        d = data[name]
        axh.hist(d["v"], bins=bins, histtype="step", color=col, lw=2.0, zorder=4,
                 density=True)
    S.tidy(axh, xlabel="A single reading (ADC counts)",
           ylabel="How often a reading landed there", grid="y")
    axh.set_yticks([])
    axh.set_xlim(-180, 180)
    axh.set_title("Every reading from both ten-second runs.\n"
                  "The two distributions are the same.")
    sd_still = data["still.csv"]["sd"]
    sd_stamp = data["stamp.csv"]["sd"]
    axh.text(-172, axh.get_ylim()[1] * 0.93,
             "room still            %.1f counts  (%.0f pA)\n"
             "someone stamping   %.1f counts  (%.0f pA)"
             % (sd_still, sd_still * PA_PER_COUNT, sd_stamp, sd_stamp * PA_PER_COUNT),
             ha="left", va="top", fontsize=S.TYPE["annot"], fontweight=S.W_EMPH,
             color=S.C["ink"], linespacing=1.9,
             bbox=dict(boxstyle="round,pad=0.6", facecolor=S.C["band"], edgecolor="none"))
    S.note(axh, 0, axh.get_ylim()[1] * 0.50,
           "spread of a single reading,\nas a standard deviation", ha="center",
           va="top", fontsize=S.TYPE["small"])

    S.titles_keyed(
        fig,
        "The amplifier is quiet, and footsteps do not get into it electrically",
        "Ten seconds of readings with the tip clear, <with the room still> and again <with someone stamping on the "
        "floor about two metres away>.\nThe two are indistinguishable. What noise there is sits on the mains "
        "frequency and its harmonics — a wiring problem with known fixes, not a limit of the amplifier.",
        [{"color": S.word(0), "fontweight": S.W_EMPH},
         {"color": S.word(1), "fontweight": S.W_EMPH}])

    S.footer(fig, y=0.008, text=
             "Source: sessions/data/2026-09-19-bench/still.csv and stamp.csv, 10 s of ADCR readings each at about "
             "%.0f Hz, measured 2026-09-19 00:54–02:25 UTC with the TIP CLEAR; "
             "sessions/2026-09-19-bench.md section 3.3.\n"
             "The recorded timestamps are near-uniform but not exact (median 0.271 ms, 5th–95th percentile "
             "0.24–0.38 ms), so the series is interpolated onto a uniform grid at the median rate before "
             "Welch's method (4,096-point segments).\nThat jitter smears the highest frequencies; it does not "
             "move the mains lines. Counts are converted to picoamps at 3.125 pA per count (docs/FACTS.md).\n"
             "WHAT THIS DOES NOT SHOW: with the tip clear there is no junction, so this tests ELECTRICAL pickup "
             "only — it says nothing about whether footsteps move the gap, which is a different question "
             "and figure 3's. These are\n2026-09-19 tip-clear numbers; the 2026-09-18 figures of 341–350 "
             "counts belong to a different night and a different tip, and some tools still quote them."
             % data["still.csv"]["fs"])

    S.save(fig, "fig06_noise")


if __name__ == "__main__":
    main()
