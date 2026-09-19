"""12 - What the 2026-09-17 636-count profile actually is: a start-of-pass transient.

Run from the repository root:

    python3 deliverables/2026-09-19-pause/candidates/code/12_start_of_pass_transient.py

Writes work/start_of_pass_transient.csv.

THE FINDING
-----------
Plotting the twelve raw passes (gallery/01) shows every one of them starting
low at the first X point and jumping up by one to two thousand Z counts within
one or two pixels. That is the feedback loop settling after the line begins,
not the sample.

sessions/2026-09-17-bench.md section 3.22 already caught this exact failure once,
one level up:

    "A result I nearly believed, and the check that killed it. The earlier slow
     pair of images correlated at r = +0.75 ... Dropping the first LINE of each
     image took it to +0.22, and dropping two took it to +0.04. The entire
     agreement was the feedback loop's settling transient on the first line."

This is the same thing with PIXELS in place of LINES, inside a single line, and
nobody has applied the check at that level. This script does.

Three tests:
  1. Drop leading points and watch the headline numbers.
  2. Measure the jump directly, pass by pass, and show it GROWS through the run
     - a settling transient that is getting worse, which no fixed surface can do.
  3. Check the other end. In the two 2D wide images the BACKWARD pass starts at
     the opposite end of X. If this is a start-of-pass effect its transient must
     move to the other end of the stored row. If it were the sample it would
     stay where the sample is.

PROCESSING: detrending as elsewhere, applied AFTER any points are dropped, so
the tilt is fitted to what is actually being compared.
"""
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from stmload import load_raster, load_ycontrol, data, out, detrend, corr, rms, fisher_mean

RNG = np.random.default_rng(20260919)


def main():
    rows = []
    xs, pl, P = load_ycontrol(data("2026-09-17-bench", "line_repeated_wide.csv"))
    raw = np.array([v for p in pl for v in P[p]])[0::2]     # forward passes only

    print("1. DROP LEADING POINTS AND WATCH THE HEADLINE NUMBERS COLLAPSE")
    print("   %5s %6s %11s %13s %12s" % ("drop", "points", "profile RMS",
                                         "consecutive r", "split-half r"))
    for d in range(0, 7):
        D = np.array([detrend(v[d:]) for v in raw])
        prof = D.mean(axis=0)
        cons = fisher_mean([corr(D[i], D[i + 1]) for i in range(len(D) - 1)])[0]
        sh = corr(D[0::2].mean(axis=0), D[1::2].mean(axis=0))
        print("   %5d %6d %11.0f %13.3f %12.3f" % (d, D.shape[1], rms(prof), cons, sh))
        rows.append(["drop leading points", "drop %d" % d, "%d points" % D.shape[1],
                     "profile RMS %.0f" % rms(prof), "consecutive r %+.3f" % cons,
                     "split-half %+.3f" % sh])
    print("""
   The published headline was consecutive-pass r +0.515 and a 636-count profile.
   Dropping ONE point takes it to +0.317 and 339 counts. Dropping TWO takes it
   to +0.048 and 233 counts. THE AGREEMENT BETWEEN PASSES IS IN THE FIRST TWO
   PIXELS. This is the same check that killed the +0.75 image pair on the same
   night (section 3.22) - one level down, on pixels instead of lines.

   The split-half figure falls much more slowly (+0.923 to +0.672) because it
   averages six passes a side, and averaging lifts any residual common shape.
   That is why the single-pass statistic is the one to read - the same lesson
   the three-Y control was built around.""")

    print("\n2. THE JUMP, MEASURED PASS BY PASS")
    j0 = np.array([v[1] - v[0] for v in raw])
    j1 = np.array([v[2] - v[1] for v in raw])
    jl = np.array([v[11] - v[10] for v in raw])
    print("   pass          " + " ".join("%6d" % i for i in range(len(raw))))
    print("   point 0 -> 1  " + " ".join("%+6.0f" % v for v in j0))
    print("   point 1 -> 2  " + " ".join("%+6.0f" % v for v in j1))
    print("   point 10 -> 11" + " ".join("%+6.0f" % v for v in jl))
    sl = np.polyfit(np.arange(len(j0)), j0, 1)[0]
    print("\n   mean first jump %+.0f counts, mean mid-line step %+.0f counts - a factor of %.0f"
          % (j0.mean(), jl.mean(), abs(j0.mean() / jl.mean())))
    print("   and the first jump GROWS through the run: %+.0f counts per pass, %+.0f to %+.0f"
          % (sl, j0[0], j0[-1]))
    print("""   A surface feature is the same size on pass 1 and pass 12. A settling
   transient that is getting worse as the junction drifts is not. This one
   more than triples.""")
    rows.append(["the jump", "first step", "mean %+.0f counts" % j0.mean(),
                 "mid-line step mean %+.0f" % jl.mean(),
                 "grows %+.0f counts per pass" % sl])

    print("\n3. THE OTHER END - the backward pass starts where X ENDS")
    print("   in scan_wide_25nm_1/2 the backward pass sweeps X downward, so its")
    print("   start-of-pass transient must land at the HIGH-X end of the stored row")
    print()
    print("   %-24s %-10s %14s %14s %14s" % ("file", "direction", "jump at low X",
                                             "jump at high X", "mid-line step"))
    for img in ("1", "2"):
        _, ys, F, B = load_raster(data("2026-09-17-bench", "scan_wide_25nm_%s.csv" % img))
        for tag, A in (("forward", F), ("backward", B)):
            lo = np.mean([v[1] - v[0] for v in A])
            hi = np.mean([v[-2] - v[-1] for v in A])
            mid = np.mean([v[11] - v[10] for v in A])
            print("   %-24s %-10s %14.0f %14.0f %14.0f" % (
                "scan_wide_25nm_%s.csv" % img, tag, lo, hi, mid))
            rows.append(["other end", "scan_wide_25nm_%s %s" % (img, tag),
                         "low-X jump %.0f" % lo, "high-X jump %.0f" % hi,
                         "mid step %.0f" % mid])
    print("""
   The transient sits at the end of the row where each direction BEGINS, and
   follows the scan rather than staying at one X. A feature on the sample
   cannot do that. This is the same evidence as the trace/retrace mirror in
   gallery/05, seen at the start of the line instead of across it.""")

    print("\n4. IS ANYTHING LEFT ONCE THE TRANSIENT IS GONE?")
    D = np.array([detrend(v[2:]) for v in raw])
    obs_prof, obs_cons = rms(D.mean(axis=0)), fisher_mean(
        [corr(D[i], D[i + 1]) for i in range(len(D) - 1)])[0]
    mag = np.abs(np.fft.rfft(D, axis=1))
    n = D.shape[1]
    t = np.arange(n, dtype=float)
    A = np.vstack([t, np.ones_like(t)]).T
    Pd = np.eye(n) - A @ np.linalg.pinv(A)
    sp, sc = np.empty(4000), np.empty(4000)
    for k in range(4000):
        ph = RNG.uniform(0, 2 * np.pi, mag.shape)
        ph[:, 0] = 0
        S = np.fft.irfft(mag * np.exp(1j * ph), n=n, axis=1) @ Pd.T
        sp[k] = rms(S.mean(axis=0))
        sc[k] = fisher_mean([corr(S[i], S[i + 1]) for i in range(len(S) - 1)])[0]
    print("   with the first two points dropped, against phase-randomised surrogates:")
    print("     profile RMS     observed %3.0f counts   surrogate %3.0f +- %2.0f   p = %.3f"
          % (obs_prof, sp.mean(), sp.std(), (sp >= obs_prof).mean()))
    print("     consecutive r   observed %+.3f        surrogate %+.3f +- %.3f  p = %.3f"
          % (obs_cons, sc.mean(), sc.std(), (sc >= obs_cons).mean()))
    rows.append(["after dropping 2 points", "profile RMS", "%.0f" % obs_prof,
                 "surrogate %.0f+-%.0f" % (sp.mean(), sp.std()),
                 "p = %.3f" % (sp >= obs_prof).mean()])
    rows.append(["after dropping 2 points", "consecutive r", "%+.3f" % obs_cons,
                 "surrogate %+.3f+-%.3f" % (sc.mean(), sc.std()),
                 "p = %.3f" % (sc >= obs_cons).mean()])
    print("""
   NOTHING SURVIVES. Once the start-of-pass transient is removed, the twelve
   passes agree no better than twelve phase-randomised lines of the same
   smoothness. CANDIDATE A IS CLOSED, and it is closed by the simplest
   mechanism available rather than by any of the subtler arguments in scripts
   04, 05, 08 and 09 - which remain true but are no longer what carries it.""")

    with open(out("work", "start_of_pass_transient.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["test", "what", "a", "b", "c"])
        for r in rows:
            w.writerow(list(r) + [""] * (5 - len(r)))
    print("\n-> %s" % out("work", "start_of_pass_transient.csv"))


if __name__ == "__main__":
    main()
