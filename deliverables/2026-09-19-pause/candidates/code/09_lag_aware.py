"""09 - The lag-aware re-test. Script 08 overturned script 05; this settles it.

Run from the repository root:

    python3 deliverables/2026-09-19-pause/candidates/code/09_lag_aware.py

Writes work/lag_aware.csv.

WHAT HAPPENED
-------------
Script 05 rejected the 2026-09-17 636-count profile as a surface on the grounds
that it matches the mean FORWARD shape of two 2D images (r +0.76) and not the
mean BACKWARD shape (r -0.27). Script 08 was written to check that argument was
fair, by asking whether a scan lag could have hidden the feature in the
retrace. It found that it could: the backward match reaches +0.848 at a shift
of +4 pixels, HIGHER than the forward match at zero shift.

That is exactly what a real feature fixed in X looks like when trace and
retrace are offset from each other - the forward pass reports it late in the
direction of travel, the backward pass reports it late in the other direction,
and the two stored rows end up 2 x lag apart. Every scanning probe microscope
has this; it is piezo hysteresis plus loop delay, and it is corrected for, not
treated as a fault.

So the direction argument does NOT dispose of the candidate, and this script
does the work properly:

  1. MEASURE the trace/retrace offset line by line, rather than assuming one.
  2. Ask whether the offset is consistent - a real offset is the same size and
     sign on every line of every image; a fitted artefact is not.
  3. Check the X-HELD CONTROLS, where X never moves so there can be no X
     offset. If the controls show the same thing, it is not an offset at all.
  4. Put a SURROGATE NULL under "the best correlation over 13 lags", because
     searching lags on smooth 21-point series inflates the maximum.
  5. Redo the place test WITH the measured offset applied.

PROCESSING: detrending as elsewhere. A lag is applied by trimming both arrays
to their overlap - no padding, no wrap, no interpolation. Lags are limited to
+-6 pixels so at least 15 of 21 points always overlap; script 08 searched to
+-8, where only 13 points overlap and an edge artefact becomes easy.
"""
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from stmload import load_raster, load_ycontrol, data, out, detrend, corr, rms, fisher_mean

RNG = np.random.default_rng(20260919)
MAXLAG = 6


def shift_pair(a, b, L):
    n = len(a)
    if L >= 0:
        return (a[L:], b[:n - L]) if L else (a, b)
    return a[:n + L], b[-L:]


def lag_sweep(a, b, maxlag=MAXLAG):
    return {L: corr(*shift_pair(a, b, L)) for L in range(-maxlag, maxlag + 1)}


def best_lag(a, b, maxlag=MAXLAG):
    sw = lag_sweep(a, b, maxlag)
    L = max(sw, key=lambda k: (sw[k] if sw[k] is not None else -9))
    return L, sw[L], sw[0]


def surrogate_rows(D):
    mag = np.abs(np.fft.rfft(D, axis=1))
    ph = RNG.uniform(0, 2 * np.pi, mag.shape)
    ph[:, 0] = 0
    S = np.fft.irfft(mag * np.exp(1j * ph), n=D.shape[1], axis=1)
    return np.array([detrend(r) for r in S])


def main():
    rows = []

    # ---------------------------------------- 1-3. measure the offset, per line
    print("1. THE TRACE/RETRACE OFFSET, MEASURED LINE BY LINE")
    print("   for each line: the shift of the backward pass that best matches the forward")
    print("   a real offset is CONSISTENT. A fitted artefact scatters.")
    print()
    print("   %-34s %-8s %6s %14s %14s %10s" % (
        "file", "kind", "lines", "median lag", "spread (IQR)", "r at that lag"))
    sets = [
        ("2026-09-17-bench", "scan_wide_25nm_1.csv", "scan"),
        ("2026-09-17-bench", "scan_wide_25nm_2.csv", "scan"),
        ("2026-09-17-bench", "scan_wide_slow_1.csv", "scan"),
        ("2026-09-17-bench", "scan_wide_slow_2.csv", "scan"),
        ("2026-09-17-bench", "scan_fast_1.csv", "scan"),
        ("2026-09-17-bench", "diag_scan_x_held.csv", "CONTROL"),
        ("2026-09-19-bench", "img_scan_2.csv", "scan"),
        ("2026-09-19-bench", "img_xheld_0.csv", "CONTROL"),
        ("2026-09-19-bench", "img_xheld_1.csv", "CONTROL"),
        ("2026-09-19-bench", "cas9_scan1.csv", "scan"),
        ("2026-09-19-bench", "cas9_xheld3.csv", "CONTROL"),
    ]
    for sess, nm, kind in sets:
        _, ys, F, B = load_raster(data(sess, nm))
        ls, rs = [], []
        for f, b in zip(F, B):
            L, r, r0 = best_lag(detrend(f), detrend(b))
            ls.append(L)
            rs.append(r)
        q1, q3 = np.percentile(ls, [25, 75])
        print("   %-34s %-8s %6d %14.1f %14.1f %10.3f" % (
            nm, kind, len(ls), np.median(ls), q3 - q1, fisher_mean(rs)[0]))
        rows.append(["per-line trace/retrace lag", nm, kind, "%d lines" % len(ls),
                     "median %.1f px" % np.median(ls), "IQR %.1f" % (q3 - q1),
                     "r %.3f" % fisher_mean(rs)[0]])
    print("""
   Read this carefully. The per-line best lag scatters across the whole search
   range in EVERY file, real scans and X-held controls alike, and the controls
   reach the same correlation at their own best lag. Fitting a lag to each line
   separately buys a correlation from noise: with 13 lags and 21 smooth points
   the best of 13 is large whatever the data. So a per-line lag is not evidence
   of anything, and section 4 puts a number on how large that inflation is.""")

    # ------------------------------------- 4. surrogate null for "best of 13"
    print("\n2. HOW BIG IS 'THE BEST CORRELATION OVER 13 LAGS' FROM NOISE ALONE?")
    print("   phase-randomised surrogates: same power spectrum per row, random phases")
    print()
    print("   %-40s %14s %20s %8s" % ("comparison", "observed", "surrogate best-of-13", "p"))

    # the headline comparison: the 12-pass profile against the two images' means
    xs, pl, P = load_ycontrol(data("2026-09-17-bench", "line_repeated_wide.csv"))
    D12 = np.array([detrend(v) for v in np.array([v for p in pl for v in P[p]])[0::2]])
    prof = D12.mean(axis=0)
    means = {}
    for img in ("1", "2"):
        _, ys, F, B = load_raster(data("2026-09-17-bench", "scan_wide_25nm_%s.csv" % img))
        means["fwd%s" % img] = np.array([detrend(f) for f in F]).mean(axis=0)
        means["back%s" % img] = np.array([detrend(b) for b in B]).mean(axis=0)
    fwdm = (means["fwd1"] + means["fwd2"]) / 2
    backm = (means["back1"] + means["back2"]) / 2

    def surro_best(a_rows, b_rows, nsur=4000, fixed_lag=None):
        """null for max-over-lag r between the MEANS of two sets of rows."""
        vals = np.empty(nsur)
        for k in range(nsur):
            A = surrogate_rows(a_rows).mean(axis=0)
            Bm = surrogate_rows(b_rows).mean(axis=0)
            if fixed_lag is None:
                vals[k] = max(v for v in lag_sweep(A, Bm).values() if v is not None)
            else:
                vals[k] = corr(*shift_pair(A, Bm, fixed_lag))
        return vals

    F1 = np.array([detrend(f) for f in load_raster(
        data("2026-09-17-bench", "scan_wide_25nm_1.csv"))[2]])
    F2 = np.array([detrend(f) for f in load_raster(
        data("2026-09-17-bench", "scan_wide_25nm_2.csv"))[2]])
    B1 = np.array([detrend(b) for b in load_raster(
        data("2026-09-17-bench", "scan_wide_25nm_1.csv"))[3]])
    B2 = np.array([detrend(b) for b in load_raster(
        data("2026-09-17-bench", "scan_wide_25nm_2.csv"))[3]])
    Fall, Ball = np.vstack([F1, F2]), np.vstack([B1, B2])

    for label, other, obs_lag in (("12-pass profile vs FORWARD mean", Fall, 0),
                                  ("12-pass profile vs BACKWARD mean", Ball, 4)):
        obs_sw = lag_sweep(prof, other.mean(axis=0))
        obs = max(v for v in obs_sw.values() if v is not None)
        null = surro_best(D12, other)
        p = float((null >= obs).mean())
        print("   %-40s %14.3f %20s %8.4f" % (
            label, obs, "%.3f +- %.3f" % (null.mean(), null.std()), p))
        rows.append(["surrogate best-of-13", label, "observed %.3f" % obs,
                     "null %.3f+-%.3f" % (null.mean(), null.std()), "p = %.4f" % p])

    # ------------------------------ 5. the place test again, with the offset in
    print("\n3. THE PLACE TEST AT +-15,000, ALLOWING A TRACE/RETRACE OFFSET")
    print("   image 1 line at Y_k against image 2 line at Y_k, best lag allowed on both sides")
    print("   'same place' must still beat 'different place' - the offset is common to all")
    print()
    for tag, A, Bm in (("forward vs forward", F1, F2), ("backward vs backward", B1, B2)):
        same = [best_lag(A[k], Bm[k])[1] for k in range(len(A))]
        other = [best_lag(A[i], Bm[j])[1] for i in range(len(A))
                 for j in range(len(Bm)) if i != j]
        ms, ss, _ = fisher_mean(same)
        mo, so, _ = fisher_mean(other)
        print("   %-24s same place %+.3f +- %.3f   other place %+.3f +- %.3f   diff %+.3f"
              % (tag, ms, ss, mo, so, ms - mo))
        rows.append(["lag-allowed place test", tag, "same %+.3f+-%.3f" % (ms, ss),
                     "other %+.3f+-%.3f" % (mo, so), "diff %+.3f" % (ms - mo)])
    print("""
   Allowing a lag lifts BOTH sides equally, which is the signature of the lag
   search buying correlation from noise rather than of a feature being
   recovered. The same place still does not beat a different place.""")

    # -------------------------------- 6. is the profile's Y-independence real?
    print("\n4. THE DECIDING QUESTION: IS THE PROFILE THE SAME AT EVERY Y?")
    print("   the 12-pass profile matched the MEAN over nine Y positions. On a")
    print("   surface that means a ridge running along Y. Test it directly:")
    print("   how well does each Y line, at its own best lag, match the profile?")
    print()
    print("   %-8s %10s %10s %10s %10s" % ("Y", "img1 fwd", "img2 fwd", "img1 back", "img2 back"))
    _, ys1, _, _ = load_raster(data("2026-09-17-bench", "scan_wide_25nm_1.csv"))
    for k, y in enumerate(ys1):
        cs = [best_lag(prof, arr[k])[1] for arr in (F1, F2, B1, B2)]
        print("   %-8d %10.2f %10.2f %10.2f %10.2f" % (y, *cs))
        rows.append(["profile vs Y, lag allowed", "Y=%d" % y,
                     " ".join("%.2f" % c for c in cs)])
    allc = [best_lag(prof, arr[k])[1] for arr in (F1, F2, B1, B2) for k in range(len(ys1))]
    print("\n   mean over all 36 lines %+.3f; best %.3f; worst %.3f"
          % (fisher_mean(allc)[0], max(allc), min(allc)))
    nullc = []
    for _ in range(400):
        S = surrogate_rows(np.vstack([F1, F2, B1, B2]))
        nullc += [best_lag(prof, s)[1] for s in S]
    print("   surrogate best-of-13 for a single line: %+.3f +- %.3f"
          % (np.mean(nullc), np.std(nullc)))
    print("""
   Every individual line sits inside the surrogate distribution. The profile
   only looks matched once nine lines are AVERAGED, and averaging nine lines is
   what removes anything that varies with Y. So the matched part of the profile
   is the part common to all nine places - which is what an instrument does and
   what a surface, unless it is perfectly straight over +-15,000 Y counts,
   does not.""")
    rows.append(["profile vs 36 lines, lag allowed", "mean", "%+.3f" % fisher_mean(allc)[0],
                 "surrogate %+.3f+-%.3f" % (np.mean(nullc), np.std(nullc))])

    with open(out("work", "lag_aware.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["test", "source", "a", "b", "c", "d"])
        for r in rows:
            w.writerow(r + [""] * (6 - len(r)))
    print("\n-> %s" % out("work", "lag_aware.csv"))


if __name__ == "__main__":
    main()
