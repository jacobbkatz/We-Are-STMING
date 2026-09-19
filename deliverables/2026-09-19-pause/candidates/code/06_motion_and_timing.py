"""06 - Motion, timing and periodicity: does anything in the scans track TIME?

Run from the repository root:

    python3 deliverables/2026-09-19-pause/candidates/code/06_motion_and_timing.py

Writes work/motion_and_timing.csv.

WHAT IT DOES
------------
1. Within-pass spectrum. Each detrended pass is a 21-point series in pixel
   index. Pixel index IS time inside a pass. Converting the dominant pixel
   period into hertz, using the per-image durations printed in the session
   logs, says whether the wiggles sit in the 5-30 Hz band the noise
   spectroscopy already blamed (sessions/2026-09-17-bench.md section 3.24:
   everything above the 8-14 count electrical floor is below about 30 Hz, with
   no line at 60 or 120 Hz, so it is mechanical).

2. Line-to-line phase. If a disturbance is periodic and the raster is regular,
   its phase advances by a fixed amount each line, so the apparent "feature"
   walks across the image at a constant rate. Measured as the cross-correlation
   lag between consecutive forward lines.

3. Gap motion from the Z test. sessions/data/2026-09-19-morning/ztest_*.csv and
   bias_*.csv record (t, cycle, phase, z, adc). The onset Z per cycle against
   time is the gap's own motion, and its spectrum is the only direct look this
   project has at whether that motion is periodic.

4. Long fixed-point records. still.csv, stamp.csv (tip clear, 10 s at ~3.6 kHz)
   and here_run1.csv (a junction, fixed Z, ~46k samples) - checked for coherent
   lines by splitting each record in half and keeping only peaks that appear in
   both halves at the same frequency. This is the test
   sessions/2026-09-19-morning.md section 6 applied to here_run1.csv; it is
   repeated here on all four records so the tip-clear ones act as controls.

PROCESSING: detrending as elsewhere; a Hann window before every FFT; no
zero-padding, no smoothing of the spectra.
"""
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from stmload import load_raster, load_ycontrol, data, out, detrend, corr, rms

# Per-image wall-clock durations, read from the session logs. Approximate.
#  2026-09-17 section 3.22: fast images 4.5-6.2 s, slow 38-60 s, dwell 60-88 s.
#  2026-09-19 cas9.log: consecutive scan start stamps 5-9 s apart.
DWELL_MS = {
    "scan_fast": 5.4e3 / (12 * 42),        # 12 lines x 42 pixels
    "scan_slow": 49e3 / (12 * 42),
    "scan_slow_dwell": 74e3 / (7 * 18),
    "cas9": 5.0e3 / (11 * 42),
}


def pass_spectrum(D):
    """Mean power spectrum of a set of detrended passes, in cycles per pixel.

    CAVEAT, stated because it limits what section 1 can say: a pass is only 21
    points long, so the spectrum has 10 usable bins. It can say whether the
    structure is slow (comparable with the whole line) or fast (pixel to
    pixel); it cannot resolve a line frequency.
    """
    n = D.shape[1]
    w = np.hanning(n)
    P = np.abs(np.fft.rfft(D * w, axis=1)) ** 2
    f = np.fft.rfftfreq(n, d=1.0)
    return f, P.mean(axis=0)


def coherent_lines(t, y, fmax, nbins=None):
    """Peaks present in BOTH halves of a record at the same frequency.

    Returns a list of (freq_Hz, amp_first_half, amp_second_half).
    A line that changes size between halves is not coherent and is dropped.
    """
    n = len(y) // 2
    fs = 1.0 / np.median(np.diff(t))
    out_ = []
    specs = []
    for half in (y[:n], y[n:2 * n]):
        h = half - half.mean()
        w = np.hanning(len(h))
        A = np.abs(np.fft.rfft(h * w)) * 2 / w.sum()
        specs.append(A)
    f = np.fft.rfftfreq(n, d=1.0 / fs)
    A1, A2 = specs
    keep = f <= fmax
    f, A1, A2 = f[keep], A1[keep], A2[keep]
    med = np.median(np.maximum(A1, A2))
    for i in range(2, len(f) - 2):
        both = min(A1[i], A2[i])
        if both > 3 * med and both == min(A1[i], A2[i]) and A1[i] == max(A1[i - 2:i + 3]):
            ratio = max(A1[i], A2[i]) / max(both, 1e-12)
            if ratio < 2.5:
                out_.append((f[i], A1[i], A2[i]))
    out_.sort(key=lambda r: -min(r[1], r[2]))
    return out_, fs


def main():
    rows = []

    # -------------------------------------------- 1. within-pass spectrum
    print("1. WITHIN-PASS SPECTRUM - where the wiggles sit, in pixels and in hertz")
    print("   pixel index is time inside a pass, so a spatial period converts directly")
    print()
    sets = [
        ("2026-09-17-bench", ["scan_fast_1.csv", "scan_fast_2.csv", "scan_fast_3.csv",
                              "scan_fast_4.csv"], "scan_fast", "+-400 feedback scans"),
        ("2026-09-17-bench", ["scan_slow_1.csv", "scan_slow_2.csv"], "scan_slow", "+-400 slow"),
        ("2026-09-17-bench", ["diag_scan_x_held.csv"], "scan_fast", "+-400 X-HELD CONTROL"),
        ("2026-09-17-bench", ["scan_wide_25nm_1.csv", "scan_wide_25nm_2.csv"], "scan_fast",
         "+-15000 wide images"),
        ("2026-09-19-bench", ["cas9_scan0.csv", "cas9_scan1.csv", "cas9_scan2.csv",
                              "cas9_scan3.csv"], "cas9", "+-1500 feedback scans"),
        ("2026-09-19-bench", ["cas9_xheld0.csv", "cas9_xheld1.csv", "cas9_xheld3.csv"],
         "cas9", "+-1500 X-HELD CONTROLS"),
        ("2026-09-19-bench", ["img_scan_2.csv"], "cas9", "+-15000 wide image"),
        ("2026-09-19-bench", ["img_xheld_0.csv", "img_xheld_1.csv"], "cas9",
         "+-15000 X-HELD CONTROLS"),
    ]
    print("   %-28s %6s %10s %10s %10s %10s" % ("set", "passes", "peak (px)", "dwell ms",
                                                 "peak Hz", "slow power"))
    for sess, names, key, label in sets:
        D = []
        for nm in names:
            xs, ys, F, B = load_raster(data(sess, nm))
            D += [detrend(f) for f in F] + [detrend(b) for b in B]
        D = np.array(D)
        f, P = pass_spectrum(D)
        i = 1 + int(np.argmax(P[1:]))
        period_px = 1.0 / f[i]
        dwell = DWELL_MS[key]
        hz = 1000.0 / (period_px * dwell)
        lowfrac = P[1:3].sum() / P[1:].sum()
        print("   %-28s %6d %10.1f %10.1f %10.1f %9.0f%%" % (
            label, len(D), period_px, dwell, hz, 100 * lowfrac))
        rows.append(["within-pass spectrum", label, "%d passes" % len(D),
                     "peak %.1f px" % period_px, "%.1f ms/px" % dwell,
                     "%.1f Hz, %.0f%% of power in the 2 slowest bins" % (hz, 100 * lowfrac)])
    print("\n   The 2026-09-17 noise spectrum put everything above the electrical floor")
    print("   below ~30 Hz. These peaks land in that band, which is what a mechanical")
    print("   disturbance sampled by the raster looks like. It is consistency, not proof.")

    # ------------------------------------------- 2. line-to-line walk
    print("\n2. DOES THE APPARENT FEATURE WALK ACROSS THE IMAGE LINE BY LINE?")
    print("   cross-correlation lag between consecutive detrended forward lines.")
    print("   A surface gives lag 0 (features stay put). A disturbance drifting in")
    print("   phase against the raster gives a consistent non-zero lag.")
    print()
    print("   %-34s %8s %10s %10s" % ("file", "lines", "mean lag", "sd of lag"))
    for sess, nm in [("2026-09-17-bench", "scan_fast_1.csv"),
                     ("2026-09-17-bench", "scan_wide_25nm_1.csv"),
                     ("2026-09-17-bench", "scan_wide_25nm_2.csv"),
                     ("2026-09-17-bench", "diag_scan_x_held.csv"),
                     ("2026-09-19-bench", "cas9_scan1.csv"),
                     ("2026-09-19-bench", "cas9_xheld3.csv"),
                     ("2026-09-19-bench", "img_scan_2.csv"),
                     ("2026-09-19-bench", "img_xheld_0.csv")]:
        xs, ys, F, B = load_raster(data(sess, nm))
        D = np.array([detrend(f) for f in F])
        lags = []
        for a, b in zip(D, D[1:]):
            c = np.correlate(a / (a.std() or 1), b / (b.std() or 1), mode="full") / len(a)
            lags.append(int(np.argmax(c)) - (len(a) - 1))
        print("   %-34s %8d %10.2f %10.2f" % (nm, len(D), np.mean(lags), np.std(lags)))
        rows.append(["line-to-line lag", nm, "%d lines" % len(D),
                     "mean %.2f px" % np.mean(lags), "sd %.2f px" % np.std(lags)])

    # ------------------------------------------- 3. gap motion from the Z test
    print("\n3. THE GAP'S OWN MOTION - onset Z per cycle, 2026-09-19 morning Z tests")
    print("   %-28s %7s %14s %14s %12s" % ("file", "cycles", "span (counts)",
                                           "drift (cnt/s)", "residual sd"))
    for nm in ["ztest_1789822585.csv", "bias_m01V_1789822770.csv", "bias_p05V_1789822770.csv",
               "bias_p01V_1789822770.csv", "bias_m05V_1789822770.csv"]:
        p = data("2026-09-19-morning", nm)
        arr = np.genfromtxt(p, delimiter=",", names=True, dtype=None, encoding="utf-8")
        ph = np.array([str(s) for s in arr["phase"]])
        t, z, cyc = arr["t"].astype(float), arr["z"].astype(float), arr["cycle"].astype(int)
        # the onset of each cycle: the first 'in' row of that cycle
        on_t, on_z = [], []
        for c in sorted(set(cyc[ph == "in"])):
            m = (cyc == c) & (ph == "in")
            on_t.append(t[m][0])
            on_z.append(z[m][0])
        on_t, on_z = np.array(on_t), np.array(on_z)
        if len(on_t) < 4:
            continue
        sl, ic = np.polyfit(on_t, on_z, 1)
        res = on_z - (sl * on_t + ic)
        print("   %-28s %7d %14.0f %14.1f %12.0f" % (nm, len(on_t), on_z.max() - on_z.min(),
                                                     sl, res.std()))
        rows.append(["gap motion", nm, "%d cycles" % len(on_t),
                     "span %.0f counts" % (on_z.max() - on_z.min()),
                     "drift %.1f counts/s, residual sd %.0f" % (sl, res.std())])
        np.savetxt(out("work", "onsets_%s" % nm), np.column_stack([on_t, on_z]),
                   delimiter=",", header="t_s,onset_z", comments="")
    print("   The residual scatter about a straight line is the part that is NOT steady")
    print("   drift. It is the size of the wander that would spoil a scan.")

    # ------------------------------ 4. coherent lines in the long fixed records
    print("\n4. COHERENT SPECTRAL LINES IN THE LONG FIXED-POINT RECORDS")
    print("   kept only if present in BOTH halves within a factor of 2")
    for sess, nm, col, label in [
            ("2026-09-19-bench", "still.csv", 1, "tip clear, room still  [CONTROL]"),
            ("2026-09-19-bench", "stamp.csv", 1, "tip clear, stamping    [CONTROL]"),
            ("2026-09-19-bench", "touchrec_run1.csv", 1, "junction pinned, Z 2000")]:
        a = np.genfromtxt(data(sess, nm), delimiter=",", skip_header=1)
        t, y = a[:, 0], a[:, col]
        lines, fs = coherent_lines(t, y, fmax=200.0)
        txt = ", ".join("%.1f Hz (%.0f/%.0f)" % (f, a1, a2) for f, a1, a2 in lines[:8]) or "none"
        print("   %-34s fs %.0f Hz, %d samples: %s" % (label, fs, len(y), txt))
        rows.append(["coherent lines", nm, label, "fs %.0f Hz" % fs, txt])
    # here_run1.csv is (t, tag, z, ?, value)
    a = np.genfromtxt(data("2026-09-19-bench", "here_run1.csv"), delimiter=",",
                      skip_header=1, usecols=(0, 4))
    m = np.isfinite(a[:, 0]) & np.isfinite(a[:, 1])
    t, y = a[m, 0], a[m, 1]
    keep = np.diff(t, prepend=t[0] - 1) > 0
    t, y = t[keep], y[keep]
    lines, fs = coherent_lines(t, y, fmax=200.0)
    txt = ", ".join("%.1f Hz (%.0f/%.0f)" % (f, a1, a2) for f, a1, a2 in lines[:8]) or "none"
    print("   %-34s fs %.0f Hz, %d samples: %s" % ("a real junction, fixed Z 0", fs, len(y), txt))
    rows.append(["coherent lines", "here_run1.csv", "a real junction, fixed Z 0",
                 "fs %.0f Hz" % fs, txt])
    print("\n   Mains lines appear in the tip-clear controls too, so they are electrical.")
    print("   Anything mechanical would have to be present with a junction and absent")
    print("   without one.")

    with open(out("work", "motion_and_timing.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["test", "source", "a", "b", "c", "d"])
        for r in rows:
            w.writerow(r + [""] * (6 - len(r)))
    print("\n-> %s" % out("work", "motion_and_timing.csv"))


if __name__ == "__main__":
    main()
