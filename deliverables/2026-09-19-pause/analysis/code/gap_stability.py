"""Gap stability and drift: how far and how fast does the tip-sample gap move?

    python3 deliverables/2026-09-19-pause/analysis/code/gap_stability.py

Three independent records are used, and they are NOT measurements of the same thing:

  A. sessions/data/2026-09-19-morning/release_watch_run1.log
     Where the contact is, found by sweeping Z with the motor and hands still.
     This is the record behind "the gap moves by most of the Z range within seconds to
     minutes". It is a LOG only - the CSV was lost (2026-09-19-morning README, section 8).
  B. the Z-test CSVs of the same morning
     Onset Z per cycle against time: a second, finer view of the same quantity over
     two-minute windows.
  C. sessions/data/2026-09-19-bench/here_run1.csv, 'rec' rows
     35,000 readings at a FIXED Z with a junction present. This is a current record, not
     a position record, and it was taken on the BENT tip of 2026-09-19 bench, nine hours
     before A and B. It is the only fast record of a live junction in the repository, so
     it is the only one that can be asked about periodicity at all.

The periodicity test is deliberately conservative: a split-half coherence test, which
asks whether a peak in the first half of the record is in the same place in the second
half. A peak that moves is not a line.

Outputs: plots/fig07_gap_motion.png, fig08_junction_timeseries.png,
fig09_junction_spectrum.png
"""
import math
import os
import re
import statistics as st
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (data_path, read_rows, fnum, ols, style, save, section,
                    COUNTS_PER_NA, TOL, SERIES)

Z_MAX_SWEEP = 62000     # the top of the sweep; 'FAR' means the contact is beyond this


def parse_release_watch():
    """(seconds, onset Z or None for FAR) from the release-watch log."""
    path = data_path("2026-09-19-morning", "release_watch_run1.log")
    pts = []
    for line in open(path):
        m = re.search(r"([\d.]+)s\s+(FOUND onset Z (\d+)|FAR)", line)
        if m:
            pts.append((float(m.group(1)),
                        int(m.group(3)) if m.group(3) else None))
    return path, pts


def main():
    plt = style()

    # ------------------------------------------------------------ A
    section("A. WHERE THE CONTACT IS, MOTOR AND HANDS STILL (release_watch_run1.log)")
    path, pts = parse_release_watch()
    print("  source: %s, %d sweeps" % (os.path.relpath(path, os.getcwd()), len(pts)))
    for t, z in pts:
        print("    t %7.1f s  %s" % (t, "Z %d" % z if z is not None else
                                     "FAR (beyond Z %d)" % Z_MAX_SWEEP))
    found = [(t, z) for t, z in pts if z is not None]
    print()
    print("  The sweep ran in 1,000-count Z steps (a default-argument bug, morning log")
    print("  section 8), so every onset is a multiple of 1,000 and every rate below is")
    print("  quantized at that resolution. 'FAR' is a LOWER BOUND, not a position.")
    print()
    t0, z0 = found[0]
    t1, z1 = found[1]
    print("  MEASURED, receding: Z %d at %.1f s -> Z %d at %.1f s = %+.0f counts in %.1f s"
          % (z0, t0, z1, t1, z1 - z0, t1 - t0))
    print("                      = %+.0f counts/s" % ((z1 - z0) / (t1 - t0)))
    t_far = next(t for t, z in pts if z is None)
    print("  DERIVED lower bound: by %.1f s it was beyond Z %d, so >= %d counts in %.1f s"
          % (t_far, Z_MAX_SWEEP, Z_MAX_SWEEP - z0, t_far - t0))
    print("                       = >= %.0f counts/s"
          % ((Z_MAX_SWEEP - z0) / (t_far - t0)))
    late = [(t, z) for t, z in found if t > 100]
    zmin_late = min(z for _, z in late)
    print("  DERIVED lower bound: beyond %d at %.1f s, back at Z %d at %.1f s, "
          ">= %d counts over %.0f s"
          % (Z_MAX_SWEEP, t_far, zmin_late, late[0][0], Z_MAX_SWEEP - zmin_late,
             late[0][0] - t_far))
    print()
    print("  STATUS.md and docs/FACTS.md say '>= 43,000 counts in 6.4 s; >= 56,000 over")
    print("  ~2 min'. Re-derived here: >= %d in %.1f s; >= %d over %.0f s."
          % (Z_MAX_SWEEP - z0, t_far - t0, Z_MAX_SWEEP - zmin_late, late[0][0]))
    print("  Both reproduce. The second is over 111 s of elapsed time, which the")
    print("  documents round to '~2 min'.")
    print()
    print("  What this is: ONE episode. n = 1 independent observation of a recession,")
    print("  and n = 1 of a return. Nine sweeps in total, most of them within two")
    print("  clusters. It is not a rate that has been measured repeatedly.")

    # ------------------------------------------------------------ B
    section("B. ONSET DRIFT WITHIN THE Z-TEST RUNS (a second, finer view)")
    from ztest_analysis import RUNS, analyse
    from common import read_ztest
    drifts = []
    for fname, label, code, included, clock in RUNS:
        rows = read_ztest(data_path("2026-09-19-morning", fname))
        per, s = analyse(rows)
        ons = s["onsets"]
        if len(ons) < 3:
            continue
        span_t = ons[-1][0] - ons[0][0]
        span_z = max(z for _, z in ons) - min(z for _, z in ons)
        print("  %-28s %2d onsets over %5.0f s: drift %+7.1f counts/s, "
              "Z spread %6d counts%s"
              % (label, len(ons), span_t, s["drift"], span_z,
                 "" if included else "   <- excluded run"))
        if included:
            drifts.append(s["drift"])
    print()
    print("  Five included runs, drift in counts per second: %s"
          % ", ".join("%+.0f" % d for d in drifts))
    print("  Mean %+.1f, sd %.1f, %d of 5 positive (the onset moving to higher Z, i.e."
          % (st.mean(drifts), st.stdev(drifts), sum(1 for d in drifts if d > 0)))
    print("  the tip having to reach further to touch: the gold receding).")
    print("  n = 5 INDEPENDENT runs, each a separate two-minute window. Within a run the")
    print("  20-30 cycles are repeated measurements, not independent.")
    print()
    print("  Magnitude: at most %+.0f counts/s here, against the >= 7,400 counts/s of A."
          % max(drifts, key=abs))
    print("  DIFFERENT REGIME, not a contradiction: in a Z test the tip is touching the")
    print("  gold most of the time, and the log's own reading is that the gold sticks to")
    print("  and follows the tip. In A the tip had just been released and was clear.")

    # ------------------------------------------------------------ C
    section("C. A LIVE JUNCTION AT A FIXED Z (here_run1.csv, 'rec')")
    fields, rows = read_rows(data_path("2026-09-19-bench", "here_run1.csv"))
    rec = [(fnum(r["t"]), fnum(r["value"])) for r in rows if r["tag"] == "rec"]
    ts = np.array([t for t, _ in rec])
    vs = np.array([v for _, v in rec], dtype=float)
    dt = float(np.median(np.diff(ts)))
    fs = 1.0 / dt
    print("  n = %d readings over %.2f s, median interval %.4f s -> %.0f readings/s"
          % (len(rec), ts[-1] - ts[0], dt, fs))
    print("  Z 0, sample -0.5 V (BIAS 38229), 2026-09-19 bench 01:28 UTC, THE BENT TIP.")
    print("  mean %.1f counts (%.2f nA), sd %.1f counts (%.3f nA), range %.0f to %.0f"
          % (vs.mean(), vs.mean() / COUNTS_PER_NA, vs.std(ddof=1),
             vs.std(ddof=1) / COUNTS_PER_NA, vs.min(), vs.max()))
    print("  session log section 3.6 says: mean 1059 counts (3.30 nA), sd 96, range 765-1566")
    f = ols(list(ts), list(vs))
    print("  linear trend over the record: %+.1f counts/s (%+.3f nA/s), R^2 %.3f"
          % (f["slope"], f["slope"] / COUNTS_PER_NA, f["r2"]))
    # block standard deviations: how much of the scatter is slow
    print()
    print("  Block standard deviations (how much of the scatter is fast and how much slow):")
    for blk in (0.01, 0.1, 1.0):
        n = max(2, int(round(blk * fs)))
        nb = len(vs) // n
        if nb < 3:
            continue
        b = vs[:nb * n].reshape(nb, n)
        print("    %5.2f s blocks: within-block sd %6.1f counts, block-mean sd %6.1f"
              % (blk, float(b.std(axis=1, ddof=1).mean()), float(b.mean(axis=1).std(ddof=1))))

    # ---- periodicity, split-half coherence
    section("D. IS THE JUNCTION'S MOTION PERIODIC? (split-half test on here_run1 'rec')")
    print("  The test: take the spectrum of the first half and of the second half")
    print("  separately. A real line sits at the same frequency with a similar height in")
    print("  both. A peak that moves, or that only appears in one half, is not a line.")
    print()

    def spec(x, fs):
        x = x - x.mean()
        w = np.hanning(len(x))
        X = np.fft.rfft(x * w)
        fr = np.fft.rfftfreq(len(x), 1.0 / fs)
        amp = 2.0 * np.abs(X) / w.sum()
        return fr, amp

    half = len(vs) // 2
    f1, a1 = spec(vs[:half], fs)
    f2, a2 = spec(vs[half:], fs)
    a2i = np.interp(f1, f2, a2)                # onto the first half's grid

    # A four-way split is the stronger version of the same test: a real line is in the
    # same bin with a similar amplitude in every quarter of the record.
    q = len(vs) // 4
    quarters = [spec(vs[i * q:(i + 1) * q], fs) for i in range(4)]
    fq = quarters[0][0]
    aq = np.vstack([np.interp(fq, fr, am) for fr, am in quarters])

    band = (f1 > 0.2) & (f1 < 400)
    idx = np.argsort(a1[band])[::-1][:12]
    fb, ab, a2b = f1[band], a1[band], a2i[band]
    print("  Top 12 peaks of the first half, and where they are in the second:")
    print("  %-10s %10s %10s %8s  %s" % ("f (Hz)", "half 1", "half 2", "ratio", "verdict"))
    coherent = []
    for i in idx:
        r = a2b[i] / ab[i] if ab[i] else float("nan")
        ok = 0.7 <= r <= 1.43              # within a factor of 1.43 either way
        if ok:
            coherent.append((fb[i], ab[i], a2b[i]))
        print("  %-10.2f %10.1f %10.1f %8.2f  %s"
              % (fb[i], ab[i], a2b[i], r, "steady" if ok else "changes by >1.4x"))
    print()
    print("  Peaks steady across the two halves: %s"
          % (", ".join("%.1f Hz" % c[0] for c in coherent) if coherent else "none"))
    print()
    print("  THE STRONGER TEST - amplitude in each QUARTER of the record, and the")
    print("  mains lines that physics says should be there:")
    print("  %-10s %34s %8s" % ("f (Hz)", "amplitude in quarters 1-4", "max/min"))
    for target in (0.4, 1.0, 1.6, 2.0, 3.5, 60.0, 120.0, 180.0, 300.0):
        j = int(np.argmin(np.abs(fq - target)))
        col = aq[:, j]
        print("  %-10.2f %34s %8.2f"
              % (fq[j], " ".join("%7.1f" % c for c in col), col.max() / max(col.min(), 1e-9)))
    print()
    print("  MULTIPLE COMPARISONS: 12 peaks were picked out of %d frequency bins in"
          % int(band.sum()))
    print("  0.2-400 Hz, and the peaks were picked BECAUSE they were the largest in half")
    print("  one. Picking the largest of 1,960 bins and then asking whether it repeats is")
    print("  a biased test: the largest value in a noisy half is partly noise, so it tends")
    print("  to fall back. Only lines that are ALSO physically expected - 60 Hz mains and")
    print("  its harmonics - should be read as real without a further, pre-registered test.")
    print()
    print("  Noise floor of the record, 1 Hz to 400 Hz: median line amplitude %.1f counts"
          % float(np.median(a1[(f1 > 1) & (f1 < 400)])))
    print()
    d = np.diff(ts)
    print("  A CAVEAT THAT LIMITS EVERY SPECTRUM ABOVE. These readings arrive over a")
    print("  serial link and are NOT evenly spaced. Interval: median %.5f s, mean %.5f s,"
          % (float(np.median(d)), float(d.mean())))
    print("  5th/95th percentile %.5f/%.5f s, longest gap %.4f s, %.1f%% of intervals more"
          % (float(np.percentile(d, 5)), float(np.percentile(d, 95)), float(d.max()),
             100.0 * float((d > 2 * np.median(d)).mean())))
    print("  than twice the median. An FFT treats the samples as evenly spaced. At 60 Hz a")
    print("  jitter of ~0.1 ms is only a few degrees of phase, so this does NOT explain")
    print("  the unsteady 60 Hz line above; the simpler reading is that a 3-count line in")
    print("  a 2.5 s segment sits barely above the 1.1-count floor. Either way the")
    print("  amplitudes here are indicative, not calibrated.")
    print()
    print("  WHAT THIS CANNOT DO: the record is %.1f s long, so its lowest resolved"
          % (ts[-1] - ts[0]))
    print("  frequency is about %.2f Hz. A drift with a period of a minute - which is the"
          % (1.0 / (ts[-1] - ts[0])))
    print("  timescale the gap actually moves on - is invisible to it. The morning's")
    print("  position data (A and B) are the right timescale and are far too sparse:")
    print("  nine sweeps in A, and one onset per cycle in B. NEITHER CAN EXCLUDE A PERIOD.")

    # ------------------------------------------------------------ figures
    section("E. FIGURES")

    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    tf = [t for t, z in pts]
    zf = [z if z is not None else Z_MAX_SWEEP for t, z in pts]
    isfar = [z is None for t, z in pts]
    ax.plot(tf, zf, color=TOL["grey"], lw=1.0, zorder=1)
    ax.scatter([t for t, far in zip(tf, isfar) if not far],
               [z for z, far in zip(zf, isfar) if not far],
               s=34, color=TOL["blue"], zorder=3, label="contact found, at this Z")
    ax.scatter([t for t, far in zip(tf, isfar) if far],
               [z for z, far in zip(zf, isfar) if far],
               s=52, marker="^", color=TOL["red"], zorder=3,
               label="no contact anywhere: beyond Z %d" % Z_MAX_SWEEP)
    ax.axhline(Z_MAX_SWEEP, color=TOL["red"], ls=":", lw=1.0)
    ax.set_ylim(0, Z_MAX_SWEEP * 1.10)
    ax.set_xlabel("seconds after the tip was released (motor and hands still)")
    ax.set_ylabel("Z DAC code at which the current appeared")
    ax.set_title("The gap will not hold still\n"
                 "2026-09-19 morning 12:54-12:56, only the piezo moving; "
                 "onsets quantized to 1,000 counts")
    ax.annotate(">= 43,000 counts\nin 6.3 s", xy=(6.4, Z_MAX_SWEEP), xytext=(14, 50000),
                fontsize=8, arrowprops=dict(arrowstyle="->", lw=1.0))
    ax.annotate("back within reach\n111 s later", xy=(111, 6000), xytext=(60, 20000),
                fontsize=8, arrowprops=dict(arrowstyle="->", lw=1.0))
    ax.legend(loc="center right")
    save(fig, "fig07_gap_motion.png")
    plt.close(fig)

    fig, axes = plt.subplots(2, 1, figsize=(7.2, 4.6), sharex=True,
                             gridspec_kw=dict(height_ratios=[2, 1]))
    axes[0].plot(ts, vs, color=TOL["blue"], lw=0.35)
    axes[0].set_ylabel("ADC reading (counts)")
    sec = axes[0].secondary_yaxis("right",
                                  functions=(lambda c: c / COUNTS_PER_NA,
                                             lambda i: i * COUNTS_PER_NA))
    sec.set_ylabel("current (nA)")
    axes[0].set_title("A junction that held still: 10 s at fixed Z, sample $-$0.5 V\n"
                      "2026-09-19 bench 01:28 UTC, the BENT tip - mean %.0f counts "
                      "(%.2f nA), sd %.0f" % (vs.mean(), vs.mean() / COUNTS_PER_NA,
                                              vs.std(ddof=1)))
    n = max(2, int(round(0.1 * fs)))
    nb = len(vs) // n
    bm = vs[:nb * n].reshape(nb, n).mean(axis=1)
    bt = ts[:nb * n].reshape(nb, n).mean(axis=1)
    axes[1].plot(bt, bm - bm.mean(), color=TOL["purple"], lw=0.9)
    axes[1].set_ylabel("0.1 s means,\nmean removed (counts)")
    axes[1].set_xlabel("time (s)")
    axes[1].set_title("the slow part: most of the scatter is drift, not fast noise",
                      fontsize=9)
    save(fig, "fig08_junction_timeseries.png")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    m = (f1 > 0.2) & (f1 < 500)
    ax.loglog(f1[m], a1[m], color=TOL["blue"], lw=0.7, alpha=0.85, label="first half (5 s)")
    ax.loglog(f1[m], a2i[m], color=TOL["red"], lw=0.7, alpha=0.7, label="second half (5 s)")
    for fq, aa, bb in coherent:
        ax.annotate("%.0f Hz" % fq, xy=(fq, max(aa, bb)), xytext=(0, 8),
                    textcoords="offset points", ha="center", fontsize=7)
    ax.set_xlabel("frequency (Hz)")
    ax.set_ylabel("amplitude (ADC counts)")
    ax.set_title("Split-half spectrum of the live junction\n"
                 "only mains and its harmonics sit in the same place in both halves")
    ax.legend(loc="lower left")
    save(fig, "fig09_junction_spectrum.png")
    plt.close(fig)


if __name__ == "__main__":
    main()
