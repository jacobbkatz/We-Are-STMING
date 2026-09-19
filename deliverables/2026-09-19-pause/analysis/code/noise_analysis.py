"""Noise: the still-versus-stamping spectra, and the ADCR scatter across sessions.

    python3 deliverables/2026-09-19-pause/analysis/code/noise_analysis.py

The only raw noise samples in this repository are
sessions/data/2026-09-19-bench/still.csv and stamp.csv. Everything earlier survives
only as published standard deviations and band means in the session logs, which is
exactly why the 2026-09-19 plan asked for both CSVs to be committed.

This re-derives the still/stamp comparison from the raw samples, independently of
Code/pc/stm_noise_spectrum.py, and then lays the published per-session figures beside
each other with the tip, the night and the junction state attached to each, because a
noise figure taken with the tip clear and one taken with a junction are not the same
measurement.

Outputs: plots/fig10_noise_spectra.png, fig11_noise_by_session.png
"""
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import data_path, read_rows, fnum, style, save, section, COUNTS_PER_NA, TOL

BANDS = [(2, 10), (10, 30), (30, 100), (100, 400), (400, 1600)]

# Published ADCR standard deviations, with the conditions that make them comparable or
# not. Every figure is quoted from the session log named in the last column; none of them
# is recomputed here because the raw samples were not kept before 2026-09-19.
PUBLISHED = [
    # label, sd counts, tip, junction?, source
    ("2026-09-17 bench, room empty",        46,  "the blunt/bent placeholder", "clear",
     "sessions/2026-09-17-bench.md 3.25"),
    ("2026-09-18 bench 01:47, ADCR only",   341, "the same placeholder, holder rebuilt",
     "clear", "sessions/2026-09-18-bench.md 3.5"),
    ("2026-09-18 bench 01:47-01:59",        346, "the same placeholder, holder rebuilt",
     "clear", "sessions/2026-09-18-bench.md 3.5 (range 343-350)"),
    ("2026-09-19 bench 01:01, tip clear",    40, "the BENT tip", "clear",
     "sessions/2026-09-19-bench.md 3.2"),
    ("2026-09-19 bench 01:08 still.csv",     42, "the BENT tip", "clear",
     "sessions/2026-09-19-bench.md 3.3"),
    ("2026-09-19 bench 01:08 stamp.csv",     42, "the BENT tip", "clear",
     "sessions/2026-09-19-bench.md 3.3"),
    ("2026-09-19 bench 03:05, new tip",      35, "the very blunt tip", "clear",
     "sessions/2026-09-19-bench.md 3.13 (range 34-36)"),
    ("2026-09-19 morning 11:22 baseline",    35, "the very blunt tip", "clear",
     "sessions/2026-09-19-morning.md 3.1 (range 33.5-37.1)"),
    ("2026-09-19 morning 12:11 touch test",  46, "the very blunt tip", "junction at Z 20000",
     "sessions/2026-09-19-morning.md 3.6 (46.5 and 46.3)"),
]

# Height-channel wobble, which is a DIFFERENT quantity: the Z the loop needed, not the
# ADC reading. Quoted so the two are not confused, since the tools still print the first.
HEIGHT_WOBBLE = [
    ("2026-09-17 bench, loop at one fixed point", "287-419 counts RMS",
     "sessions/2026-09-17-bench.md 3.25"),
    ("2026-09-19 bench, three-Y control with X held", "9-19 counts RMS",
     "sessions/2026-09-19-bench.md 3.15"),
]


def load(path):
    _, rows = read_rows(path)
    ts = np.array([fnum(r["t_s"]) for r in rows], dtype=float)
    vs = np.array([fnum(r["adcr"]) for r in rows], dtype=float)
    ok = np.isfinite(ts) & np.isfinite(vs)
    return ts[ok], vs[ok]


def amp_spectrum(ts, vs):
    """Hann-windowed amplitude spectrum, treating the samples as evenly spaced."""
    n = len(vs)
    fs = (n - 1) / (ts[-1] - ts[0])
    x = vs - vs.mean()
    w = np.hanning(n)
    X = np.fft.rfft(x * w)
    fr = np.fft.rfftfreq(n, 1.0 / fs)
    return fs, fr, 2.0 * np.abs(X) / w.sum()


def white_floor(sd, n):
    """Expected amplitude per line for white noise of this sd, same normalisation."""
    # For a Hann-windowed rfft normalised by 2/sum(w), white noise of standard deviation
    # sd gives a mean line amplitude of about sd * sqrt(2 * 1.5 / n) * sqrt(pi/2).
    # Rather than rely on that algebra, the figure is taken from a synthetic run below.
    rng = np.random.default_rng(7)
    x = rng.normal(0, sd, n)
    w = np.hanning(n)
    X = np.fft.rfft(x * w)
    return float(np.mean(2.0 * np.abs(X) / w.sum()))


def main():
    plt = style()

    section("1. THE STILL / STAMPING PAIR - re-derived from the raw samples")
    runs = {}
    for name in ("still", "stamp"):
        ts, vs = load(data_path("2026-09-19-bench", "%s.csv" % name))
        fs, fr, amp = amp_spectrum(ts, vs)
        runs[name] = dict(ts=ts, vs=vs, fs=fs, fr=fr, amp=amp,
                          sd=float(vs.std(ddof=1)), n=len(vs))
        print("  %-6s n = %6d, %.2f s, %.0f readings/s, mean %+.2f counts, sd %.2f counts"
              " (%.4f nA)"
              % (name, len(vs), ts[-1] - ts[0], fs, vs.mean(), vs.std(ddof=1),
                 vs.std(ddof=1) / COUNTS_PER_NA))
    print("  session log 3.3 says: ADCR sd 42 for both. Re-derived: %.1f and %.1f."
          % (runs["still"]["sd"], runs["stamp"]["sd"]))
    print()
    print("  Difference in sd: %+.2f counts (%+.1f%%)."
          % (runs["stamp"]["sd"] - runs["still"]["sd"],
             100 * (runs["stamp"]["sd"] / runs["still"]["sd"] - 1)))
    # An F test on the two variances, which is the right test for 'is the scatter larger'
    try:
        from scipy.stats import f as fdist
        v1, v2 = runs["stamp"]["sd"] ** 2, runs["still"]["sd"] ** 2
        n1, n2 = runs["stamp"]["n"], runs["still"]["n"]
        F = v1 / v2
        p = 2 * min(fdist.cdf(F, n1 - 1, n2 - 1), 1 - fdist.cdf(F, n1 - 1, n2 - 1))
        print("  F test on the two variances: F = %.4f, two-sided p = %.3f" % (F, p))
        print("  CAVEAT: this test assumes independent samples. Consecutive ADCR readings")
        print("  0.28 ms apart are NOT independent - the firmware averages five")
        print("  conversions - so the true p is larger than this. It is quoted only to")
        print("  show that even the optimistic test finds nothing.")
    except Exception as exc:                                        # pragma: no cover
        print("  scipy unavailable (%s)" % exc)

    section("2. BAND CONTENT, WITH EACH RUN'S OWN WHITE FLOOR REMOVED")
    print("  Why the floor is removed: white noise sits under every band, so two runs")
    print("  with different broadband noise would differ in every band for no mechanical")
    print("  reason. The 400-1600 Hz band is the control: it should come out near zero.")
    print()
    print("  %-14s %12s %12s %12s" % ("band (Hz)", "still", "stamp", "stamp - still"))
    res = {}
    for name in ("still", "stamp"):
        r = runs[name]
        fl = white_floor(r["sd"], r["n"])
        res[name] = dict(floor=fl, bands={})
        for lo, hi in BANDS:
            m = (r["fr"] >= lo) & (r["fr"] < hi)
            res[name]["bands"][(lo, hi)] = float(r["amp"][m].mean()) - fl
        print("  (white floor for %s: %.2f counts per line)" % (name, fl))
    for b in BANDS:
        a, c = res["still"]["bands"][b], res["stamp"]["bands"][b]
        print("  %-14s %12.2f %12.2f %12.2f" % ("%d-%d" % b, a, c, c - a))
    print()
    print("  The session log's own figures, from the bench tool:")
    print("    still  2-10 Hz 0.0, 10-30 Hz 0.3, 30-100 Hz 1.2, 100-400 Hz 2.1")
    print("    stamp  2-10 Hz 0.4, 10-30 Hz 0.4, 30-100 Hz 1.2, 100-400 Hz 1.4")
    print("  The numbers here are computed with a different window and floor estimate, so")
    print("  they are not expected to agree digit for digit; the CONCLUSION is the same.")

    section("3. THE STRONGEST LINES IN EACH")
    for name in ("still", "stamp"):
        r = runs[name]
        m = (r["fr"] > 1) & (r["fr"] < 500)
        fr, amp = r["fr"][m], r["amp"][m]
        # distinct peaks only: at least 3 Hz apart, so one broadened line is not
        # reported five times
        picked = []
        for i in np.argsort(amp)[::-1]:
            if all(abs(fr[i] - f0) > 3.0 for f0, _ in picked):
                picked.append((fr[i], amp[i]))
            if len(picked) == 6:
                break
        print("  %-6s %s" % (name, ", ".join("%.0f Hz %.1f" % p for p in picked)))
    for target in (60, 120, 180, 240, 300):
        row = []
        for name in ("still", "stamp"):
            r = runs[name]
            j = int(np.argmin(np.abs(r["fr"] - target)))
            row.append(r["amp"][j])
        print("  %3d Hz: still %.1f, stamp %.1f counts" % (target, row[0], row[1]))

    section("4. WHAT THIS TEST CAN AND CANNOT SAY")
    print("  Both files were taken WITH THE TIP CLEAR. There was no junction, so there")
    print("  was nothing for floor vibration to modulate. A negative result therefore")
    print("  rules out electrical and microphonic pickup of the stamping, and NOTHING")
    print("  MORE. It does not show the building is not getting in when a gap exists.")
    print("  The session log states this itself; it is restated here because the")
    print("  stamp-versus-still pair is the only controlled A/B in the noise record and")
    print("  it is easy to over-read.")
    print()
    print("  n: ONE still run and ONE stamp run, 10 s each, taken 36 s apart. That is")
    print("  n = 1 independent observation per condition, not a repeated measurement.")

    section("5. ADCR SCATTER ACROSS THE SESSIONS - which figure belongs to which tip")
    print("  %-38s %6s  %-30s %s" % ("when", "sd", "tip", "junction"))
    for lab, sd, tip, junc, src in PUBLISHED:
        print("  %-38s %6d  %-30s %s" % (lab, sd, tip, junc))
    print()
    print("  Sources, in order:")
    for lab, sd, tip, junc, src in PUBLISHED:
        print("    %-38s %s" % (lab, src))
    print()
    print("  THE CROSS-SESSION COMPARISON IS UNSAFE IN ONE DIRECTION AND SAFE IN ANOTHER.")
    print("  Safe: 2026-09-18's 341-350 is about eight times 2026-09-17's 46 and about")
    print("  eight times 2026-09-19's 40-42, all with the tip clear, all ADCR. The 2026-")
    print("  09-18 excursion is real and it went away.")
    print("  Unsafe: comparing any of those with the 46 of the 2026-09-19 morning touch")
    print("  test, which had a JUNCTION at Z 20,000. A junction is a current source; the")
    print("  tip-clear figure is the instrument's own floor.")
    print()
    print("  A SEPARATE QUANTITY, OFTEN CONFUSED WITH THESE - the HEIGHT channel wobble:")
    for lab, val, src in HEIGHT_WOBBLE:
        print("    %-48s %-20s %s" % (lab, val, src))
    print("  These are Z DAC counts the feedback loop needed, not ADC counts. The tools")
    print("  still print the 2026-09-17 figure; it belongs to the 2026-09-17 tip and")
    print("  junction (sessions/data/2026-09-19-bench/README.md says so explicitly).")

    # ------------------------------------------------------------ figures
    section("6. FIGURES")
    fig, axes = plt.subplots(1, 2, figsize=(9.0, 3.6))
    ax = axes[0]
    for name, col in (("still", TOL["blue"]), ("stamp", TOL["red"])):
        r = runs[name]
        m = (r["fr"] > 1) & (r["fr"] < 600)
        # smooth for legibility; the numbers above are computed unsmoothed
        k = 31
        sm = np.convolve(r["amp"][m], np.ones(k) / k, mode="same")
        ax.loglog(r["fr"][m], sm, color=col, lw=1.0,
                  label="%s (sd %.0f counts)" % (name, r["sd"]))
    ax.set_xlabel("frequency (Hz)")
    ax.set_ylabel("amplitude (ADC counts, 31-line smoothed)")
    ax.set_title("Room still against someone stamping 2 m away\ntip clear, no junction")
    ax.legend(loc="lower left")

    ax = axes[1]
    xs = np.arange(len(BANDS))
    w = 0.36
    ax.bar(xs - w / 2, [res["still"]["bands"][b] for b in BANDS], w,
           color=TOL["blue"], label="still")
    ax.bar(xs + w / 2, [res["stamp"]["bands"][b] for b in BANDS], w,
           color=TOL["red"], label="stamping")
    ax.axhline(0, color=TOL["black"], lw=0.8)
    ax.set_xticks(xs)
    ax.set_xticklabels(["%d-%d" % b for b in BANDS], fontsize=7.5)
    ax.set_xlabel("band (Hz)   -   the last one is the control")
    ax.set_ylabel("content above this run's own white floor (counts)")
    ax.set_title("Stamping adds nothing outside the noise\n"
                 "with the tip clear this tests electrical pickup only")
    ax.legend(loc="upper left")
    save(fig, "fig10_noise_spectra.png")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.6, 3.8))
    labs = [p[0] for p in PUBLISHED]
    sds = [p[1] for p in PUBLISHED]
    cols = [TOL["grey"] if p[3] == "clear" else TOL["purple"] for p in PUBLISHED]
    ys = np.arange(len(labs))[::-1]
    ax.barh(ys, sds, color=cols, height=0.62)
    for y, s in zip(ys, sds):
        ax.text(s + 5, y, "%d" % s, va="center", fontsize=8)
    ax.set_yticks(ys)
    ax.set_yticklabels(labs, fontsize=7.5)
    ax.set_xlabel("ADCR standard deviation (counts)   [%.1f counts = 1 nA]" % COUNTS_PER_NA)
    ax.set_title("The published ADC scatter, session by session\n"
                 "grey: tip clear   purple: a junction present - NOT the same measurement")
    ax.set_xlim(0, max(sds) * 1.18)
    save(fig, "fig11_noise_by_session.png")
    plt.close(fig)


if __name__ == "__main__":
    main()
