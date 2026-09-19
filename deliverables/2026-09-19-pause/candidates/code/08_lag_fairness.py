"""08 - The fairness test: could a scan lag be hiding real structure in the retrace?

Run from the repository root:

    python3 deliverables/2026-09-19-pause/candidates/code/08_lag_fairness.py

Writes work/lag_fairness.csv.

WHY
---
Script 05 rejects the 2026-09-17 636-count profile as a surface because it
matches the mean FORWARD shape of two independent 2D images (r +0.76) and not
the mean BACKWARD shape (r -0.27). That argument is only fair if a real surface
feature WOULD have shown up in the backward pass. It might not: if the feedback
loop lags, the forward pass reports a feature late and the backward pass
reports it late in the other direction, so the same bump lands several pixels
apart in the two stored rows. Over 21 points a shift of a few pixels can
destroy a correlation.

So: scan the correlation over every lag, both directions. If a real feature is
present with a lag, there is a clear positive peak at some non-zero lag, and the
lag is the same sign in every comparison and roughly the size the loop's own
settling implies. If there is no peak at any lag, no lag can rescue it.

The same sweep is run on the 2026-09-19 wide images, whose trace/retrace
anti-correlation of -0.75 to -0.94 is the other thing a lag has been invoked
for (sessions/2026-09-19-bench.md section 3.16, corrected on 2026-09-19 morning
to "the loop hunting"). If a lag explained it, shifting one pass would turn the
anti-correlation positive.

PROCESSING: detrending as elsewhere. Lags are applied by trimming both arrays
to their overlap - no padding, no wrap-around, no interpolation.
"""
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from stmload import load_raster, load_ycontrol, data, out, detrend, corr, rms, fisher_mean


def lag_sweep(a, b, maxlag=8):
    """r between a and b with b shifted by each lag. Overlap only."""
    out_ = {}
    n = len(a)
    for L in range(-maxlag, maxlag + 1):
        if L >= 0:
            x, y = a[L:], b[:n - L] if L else b
        else:
            x, y = a[:n + L], b[-L:]
        if len(x) >= 8:
            out_[L] = corr(x, y)
    return out_


def main():
    rows = []
    xs, pl, P = load_ycontrol(data("2026-09-17-bench", "line_repeated_wide.csv"))
    prof = np.array([detrend(v) for v in
                     np.array([v for p in pl for v in P[p]])[0::2]]).mean(axis=0)
    means = {}
    for img in ("1", "2"):
        _, ys, F, B = load_raster(data("2026-09-17-bench", "scan_wide_25nm_%s.csv" % img))
        means["fwd%s" % img] = np.array([detrend(f) for f in F]).mean(axis=0)
        means["back%s" % img] = np.array([detrend(b) for b in B]).mean(axis=0)
    fwd = (means["fwd1"] + means["fwd2"]) / 2
    back = (means["back1"] + means["back2"]) / 2

    print("A. THE 2026-09-17 PROFILE AGAINST THE BACKWARD PASSES, AT EVERY LAG")
    print("   lag is in pixels; each pixel is 1500 X DAC counts")
    print("   %5s %10s %10s" % ("lag", "vs forward", "vs backward"))
    sw_f, sw_b = lag_sweep(prof, fwd), lag_sweep(prof, back)
    for L in sorted(sw_f):
        print("   %5d %10.3f %10.3f" % (L, sw_f[L], sw_b[L]))
        rows.append(["0917 profile vs image means", "lag %d" % L,
                     "%.3f" % sw_f[L], "%.3f" % sw_b[L]])
    bl = max(sw_b, key=lambda L: sw_b[L])
    bf = max(sw_f, key=lambda L: sw_f[L])
    print("\n   best against forward:  lag %+d, r %+.3f" % (bf, sw_f[bf]))
    print("   best against backward: lag %+d, r %+.3f" % (bl, sw_b[bl]))
    print("""
   The forward match needs NO shift. The backward match never gets near it at
   any lag inside +-8 pixels, which is +-12,000 X counts - most of the scan.
   No lag rescues it, so the "a lag hid it" escape is closed.""")
    rows.append(["0917 profile", "best lag vs forward", "%+d" % bf, "%+.3f" % sw_f[bf]])
    rows.append(["0917 profile", "best lag vs backward", "%+d" % bl, "%+.3f" % sw_b[bl]])

    print("\nB. THE 2026-09-19 WIDE IMAGES' TRACE/RETRACE ANTI-CORRELATION, AT EVERY LAG")
    print("   if a lag caused it, some shift turns it positive")
    for sess, nm, kind in [("2026-09-19-bench", "img_scan_2.csv", "scan"),
                           ("2026-09-19-bench", "img_scan_1.csv", "scan"),
                           ("2026-09-19-bench", "img_xheld_0.csv", "CONTROL"),
                           ("2026-09-19-bench", "img_xheld_1.csv", "CONTROL")]:
        _, ys, F, B = load_raster(data(sess, nm))
        per_lag = {}
        for f, b in zip(F, B):
            for L, r in lag_sweep(detrend(f), detrend(b)).items():
                per_lag.setdefault(L, []).append(r)
        mean_lag = {L: fisher_mean(v)[0] for L, v in per_lag.items()}
        best = max(mean_lag, key=lambda L: mean_lag[L])
        print("   %-18s %-8s lag 0: %+.3f   best lag %+d: %+.3f" % (
            nm, kind, mean_lag[0], best, mean_lag[best]))
        rows.append(["0919 wide trace/retrace", nm, kind,
                     "lag0 %+.3f best lag %+d -> %+.3f" % (mean_lag[0], best, mean_lag[best])])
    print("""
   No shift turns the real scans' anti-correlation positive, and the X-held
   controls do not show it at any lag. So it is not a simple lag: it needs X
   motion to appear, and it is not a surface (a surface gives trace/retrace
   POSITIVE). This is consistent with the 2026-09-19 morning correction - the
   loop hunting, driven by X motion - and does not settle the mechanism.""")

    with open(out("work", "lag_fairness.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["test", "source", "a", "b"])
        for r in rows:
            w.writerow(r + [""] * (4 - len(r)))
    print("\n-> %s" % out("work", "lag_fairness.csv"))


if __name__ == "__main__":
    main()
