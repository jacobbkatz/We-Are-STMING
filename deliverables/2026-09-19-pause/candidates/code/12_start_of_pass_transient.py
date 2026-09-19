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

Four tests:
  1. Drop leading points and watch the headline numbers.
  2. Measure the jump directly, pass by pass, and show it GROWS through the run
     - a settling transient that is getting worse, which no fixed surface can do.
  3. THE MECHANISM, with arithmetic that predicts the transient's presence AND
     its absence. This tool flies X back 30,000 counts between passes; there is
     a fixed tilt between tip and sample; so after each flyback the loop is
     tilt x 30,000 counts out and has to climb back. Two other data sets are
     used as the test: the 2D wide images raster continuously and never fly
     back, and the 2026-09-19 three-Y runs fly back but have almost no tilt.
     Neither shows the transient, exactly as the arithmetic says.
  4. Surrogate test on what is left once the first two points are dropped.

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
    print("   %5s %6s %11s %13s %12s %12s" % ("drop", "points", "profile RMS",
                                         "consec r (am)", "consec r (z)", "split-half r"))
    for d in range(0, 7):
        D = np.array([detrend(v[d:]) for v in raw])
        prof = D.mean(axis=0)
        pairs = [corr(D[i], D[i + 1]) for i in range(len(D) - 1)]
        cons_am = float(np.mean(pairs))           # the project's convention (section 3.25's +0.515)
        cons_z = fisher_mean(pairs)[0]            # Fisher-z, quoted alongside, never instead
        sh = corr(D[0::2].mean(axis=0), D[1::2].mean(axis=0))
        print("   %5d %6d %11.0f %13.3f %12.3f %12.3f"
              % (d, D.shape[1], rms(prof), cons_am, cons_z, sh))
        rows.append(["drop leading points", "drop %d" % d, "%d points" % D.shape[1],
                     "profile RMS %.0f" % rms(prof),
                     "consecutive r arithmetic %+.3f, Fisher-z %+.3f" % (cons_am, cons_z),
                     "split-half %+.3f" % sh])
    print("""
   CONVENTION: 'consec r (am)' is the ARITHMETIC mean of the 11 pairwise
   correlations - the project's convention, and the +0.515 that
   sessions/2026-09-17-bench.md section 3.25 published. 'consec r (z)' is the
   Fisher-z mean of the same 11 numbers. Fisher-z is the better estimator and it
   is larger here because the pairs are spread (-0.21 to +0.95), but THE NUMBER
   TO QUOTE IS THE ARITHMETIC MEAN, so that one figure is in circulation.

   The published headline was consecutive-pass r +0.515 and a 636-count profile.
   Dropping ONE point takes it to +0.249 and 339 counts. Dropping TWO takes it
   to +0.025 and 233 counts. THE AGREEMENT BETWEEN PASSES IS IN THE FIRST TWO
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
    interior = float(np.mean([np.abs(np.diff(v[2:])).mean() for v in raw]))
    print("\n   CONVENTION, stated so one number is quoted: 'an ordinary step' is the MEAN")
    print("   ABSOLUTE step over the interior points (index 2 onward), which is %.0f counts."
          % interior)
    print("   The signed mean of one particular step (index 10 to 11) is %+.0f counts and is NOT"
          % jl.mean())
    print("   the right comparison, because signed steps of an undulating line partly cancel.")
    print("   mean first jump |%.0f| counts against an ordinary step of %.0f - a factor of %.1f"
          % (abs(j0.mean()), interior, abs(j0.mean()) / interior))
    print("   and the first jump GROWS through the run: %+.0f counts per pass, %+.0f to %+.0f"
          % (sl, j0[0], j0[-1]))
    print("""   A surface feature is the same size on pass 1 and pass 12. A settling
   transient that is getting worse as the junction drifts is not. This one
   more than triples.""")
    rows.append(["the jump", "first step", "mean %+.0f counts" % j0.mean(),
                 "ordinary interior step, mean absolute %.0f" % interior,
                 "factor %.1f; grows %+.0f counts per pass" % (abs(j0.mean()) / interior, sl)])

    print("\n3. THE MECHANISM: THE X FLYBACK BETWEEN PASSES")
    print("   The line-repeat tool scans X from low to high, then jumps ALL THE WAY BACK")
    print("   to start the next pass. There is a fixed tilt between tip and sample, so")
    print("   after that jump the loop is a long way from the Z it needs and has to")
    print("   climb back - and it climbs back identically every pass, because the")
    print("   flyback is identical every pass. THAT is what reproduces.")
    print()
    tilt = np.mean([np.polyfit(xs.astype(float), v, 1)[0] for v in raw])
    span = float(xs[-1] - xs[0])
    pred = abs(tilt) * span
    print("   tilt of the 12 passes                 %+.3f Z counts per X count" % tilt)
    print("   X flyback between passes              %.0f counts (%d back to %d)"
          % (span, xs[-1], xs[0]))
    print("   PREDICTED Z error to recover          %.0f counts" % pred)
    print("   OBSERVED recovery in the first pixel  %+.0f counts"
          % np.mean([v[1] - v[0] for v in raw]))
    print("   OBSERVED recovery in the first two    %+.0f counts"
          % np.mean([v[2] - v[0] for v in raw]))
    rows.append(["flyback", "line_repeated_wide", "tilt %+.3f Z/X" % tilt,
                 "flyback %.0f X counts" % span, "predicted %.0f, observed %.0f"
                 % (pred, np.mean([v[2] - v[0] for v in raw]))])

    print("\n   THE PREDICTION TESTED ON TWO DATA SETS THAT HAVE NO FLYBACK")
    print("   %-40s %10s %12s %14s %14s"
          % ("recording", "tilt Z/X", "flyback X", "predicted Z", "observed jump"))
    for img in ("1", "2"):
        _, ys, F, B = load_raster(data("2026-09-17-bench", "scan_wide_25nm_%s.csv" % img))
        t = np.mean([np.polyfit(xs.astype(float), v, 1)[0] for v in F])
        print("   %-40s %10.3f %12s %14s %14.0f"
              % ("scan_wide_25nm_%s.csv (2D raster)" % img, t, "0", "0",
                 np.mean([v[1] - v[0] for v in F])))
        rows.append(["flyback", "scan_wide_25nm_%s" % img, "tilt %+.3f" % t,
                     "no flyback", "observed jump %.0f" % np.mean([v[1] - v[0] for v in F])])
    for nm in ("ycontrol_run1.csv", "ycontrol_run2_ysep12000.csv"):
        x2, pls, P2 = load_ycontrol(data("2026-09-19-bench", nm))
        A = np.array([v for p_ in pls for v in P2[p_]])
        t = np.mean([np.polyfit(x2.astype(float), v, 1)[0] for v in A])
        sp2 = float(x2[-1] - x2[0])
        print("   %-40s %10.4f %12.0f %14.0f %14.0f"
              % (nm + " (2026-09-19)", t, sp2, abs(t) * sp2, np.mean(A[:, 1] - A[:, 0])))
        rows.append(["flyback", nm, "tilt %+.4f" % t, "flyback %.0f" % sp2,
                     "predicted %.0f, observed %.0f" % (abs(t) * sp2,
                                                        np.mean(A[:, 1] - A[:, 0]))])
    print("""
   The 2D images raster back and forth without lifting X, so X is CONTINUOUS
   across every join: a forward pass ends at X 47768 and the backward pass
   begins at X 47768. No flyback, and no transient - their first-pixel jumps
   are 37 to 126 counts, the same size as an ordinary mid-line step.

   The 2026-09-19 three-Y runs DO fly back, but their tilt is almost zero
   (-0.0009 and +0.0079 against the 2026-09-17 run's -0.105), so the predicted
   recovery is 28 and 238 counts - and the observed jumps are -99 and +47.

   Three data sets, one arithmetic, and it predicts the presence AND the
   absence of the transient from the tilt alone. This is the mechanism.""")

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
   The reproduction is gone: consecutive-pass r +0.048 against a surrogate
   +0.001 +- 0.102, p = 0.33. The averaged profile is still a little larger
   than a surrogate's (233 against 166 +- 36, p = 0.035), so SOMETHING common
   to the twelve passes remains - but p = 0.035 is one test out of the 201 in
   script 07, where about 10 results at that level are expected from noise, and
   it is nowhere near the corrected threshold of p < 2.5e-4.

   CANDIDATE A IS CLOSED. What was 636 counts and r +0.515 is, once the
   flyback recovery is dropped, 233 counts and r +0.048. The residue is worth
   ONE cheap bench check when the instrument is rebuilt (see VERDICT.md), not
   a claim.""")

    with open(out("work", "start_of_pass_transient.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["test", "what", "a", "b", "c"])
        for r in rows:
            w.writerow(list(r) + [""] * (5 - len(r)))
    print("\n-> %s" % out("work", "start_of_pass_transient.csv"))


if __name__ == "__main__":
    main()
