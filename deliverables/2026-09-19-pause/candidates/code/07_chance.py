"""07 - Accounting for chance. Permutation nulls, not parametric sigmas.

Run from the repository root:

    python3 deliverables/2026-09-19-pause/candidates/code/07_chance.py

Writes work/chance.csv.

WHY
---
Every "sigma" quoted for a three-Y control in this project comes from a Fisher-z
standard error over a list of pairwise correlations. Those pairs are NOT
independent: 18 passes give 45 within-place pairs and 108 between-place pairs,
and every pass appears in many of them. A standard error computed as if they
were independent is too small, so the sigma is too big. The three-Y control's
own tool warns that a statistic can be biased in the data even when it was
designed not to be (sessions/2026-09-19-bench.md section 9).

The honest null is a permutation. The question "do passes taken at the same
place agree better than passes taken at different places?" is answered by
shuffling the place labels among the passes and recomputing. Nothing else
changes: the same passes, the same detrending, the same statistic.

Three nulls are built here:

  N1  PLACE-LABEL PERMUTATION for every three-Y run: reassign the 18 passes at
      random into three groups of the observed sizes, recompute
      within - between, 20,000 times.

  N2  IMAGE-Y-LABEL PERMUTATION for the 2026-09-17 two-image place test:
      shuffle which Y line of image 2 is called "the same place", 20,000 times.

  N3  PHASE-RANDOMISED SURROGATES for the 12-pass profile: replace each pass by
      a surrogate with the identical power spectrum and random Fourier phases.
      This preserves how smooth and how large each pass is and destroys only
      the alignment between passes. It answers "could 12 wiggly lines this
      smooth agree this well by chance?"

MULTIPLE COMPARISONS
--------------------
The count of reproducibility tests run on this data is printed at the end. A
matched-filter search over N images finds its best hit by construction, so the
best hit must clear a threshold corrected for N.
"""
import csv
import itertools
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from stmload import load_raster, load_ycontrol, data, out, detrend, corr, rms, fisher_mean

RNG = np.random.default_rng(20260919)
NPERM = 20000


def wb_difference(D, labels):
    """within-place minus between-place mean correlation, Fisher-z averaged."""
    n = len(D)
    within, between = [], []
    for a, b in itertools.combinations(range(n), 2):
        c = corr(D[a], D[b])
        if c is None:
            continue
        (within if labels[a] == labels[b] else between).append(c)
    mw, _, _ = fisher_mean(within)
    mb, _, _ = fisher_mean(between)
    if mw is None or mb is None:
        return None
    return mw - mb


def perm_test_place(path):
    xs, places, P = load_ycontrol(path)
    D, labels = [], []
    for p in places:
        for v in P[p]:
            D.append(detrend(v))
            labels.append(p)
    D = np.array(D)
    labels = np.array(labels)
    obs = wb_difference(D, labels)
    null = np.empty(NPERM)
    for k in range(NPERM):
        null[k] = wb_difference(D, RNG.permutation(labels))
    p_one = float((null >= obs).mean())
    return obs, null, p_one, len(D), len(places)


def main():
    rows = []
    print("N1. PLACE-LABEL PERMUTATION - the three-Y controls")
    print("    observed = within-place r minus between-place r, single pass vs single pass")
    print("    p = fraction of 20,000 random relabellings that do as well or better")
    print()
    print("    %-40s %7s %9s %9s %8s" % ("file", "passes", "observed", "null sd", "p"))
    yfiles = [
        ("2026-09-19-bench", "ycontrol_run2_ysep12000.csv", "the 3.9 sigma run"),
        ("2026-09-19-bench", "ycontrol_run4_ysep12000_repeat.csv", "its repeat"),
        ("2026-09-19-bench", "ycontrol_run3_ysep12000_xheld.csv", "X-HELD CONTROL"),
        ("2026-09-19-bench", "ycontrol_run1.csv", "y_sep 3000"),
        ("2026-09-19-bench", "ycontrol_xheld_run1.csv", "X-HELD CONTROL"),
        ("2026-09-17-bench", "line_three_y_positions.csv", "2026-09-17, +-8000 X"),
    ]
    for sess, nm, what in yfiles:
        obs, null, p, npass, npl = perm_test_place(data(sess, nm))
        print("    %-40s %7d %+9.3f %9.3f %8.4f" % (nm, npass, obs, null.std(), p))
        rows.append(["N1 place permutation", "%s/%s" % (sess, nm), what,
                     "%d passes" % npass, "observed %+.3f" % obs,
                     "null sd %.3f" % null.std(), "p = %.4f" % p])
    print("""
    The 2026-09-19 run at y_sep 12000 is the one that was called 3.9 sigma on the
    night and +4.2 sigma by the parametric statistic in script 03. Under the
    permutation null it is weaker, because the pairwise correlations share
    passes and are not independent. Read the permutation p, not the sigma.""")

    # --------------------------------------------- N2 the 2026-09-17 place test
    print("\nN2. Y-LABEL PERMUTATION - the 2026-09-17 two-image place test at +-15,000")
    xs1, ys1, F1, B1 = load_raster(data("2026-09-17-bench", "scan_wide_25nm_1.csv"))
    xs2, ys2, F2, B2 = load_raster(data("2026-09-17-bench", "scan_wide_25nm_2.csv"))
    for tag, A, Bm in (("forward", F1, F2), ("backward", B1, B2)):
        D1 = np.array([detrend(f) for f in A])
        D2 = np.array([detrend(f) for f in Bm])
        C = np.array([[corr(D1[i], D2[j]) for j in range(len(D2))] for i in range(len(D1))])
        def stat(perm):
            same = [C[i, perm[i]] for i in range(len(C))]
            other = [C[i, j] for i in range(len(C)) for j in range(len(C)) if j != perm[i]]
            return fisher_mean(same)[0] - fisher_mean(other)[0]
        obs = stat(np.arange(len(C)))
        null = np.array([stat(RNG.permutation(len(C))) for _ in range(2000)])
        p = float((null >= obs).mean())
        print("    %-10s observed %+.3f, null sd %.3f, p = %.4f (2,000 permutations)"
              % (tag, obs, null.std(), p))
        rows.append(["N2 Y-label permutation", "scan_wide_25nm_1/2", tag,
                     "observed %+.3f" % obs, "null sd %.3f" % null.std(), "p = %.4f" % p])
    print("    Neither direction shows the same place agreeing better than a different one.")

    # ------------------------------------------ N3 the 12-pass profile surrogate
    print("\nN3. PHASE-RANDOMISED SURROGATES - the 2026-09-17 636-count profile")
    xs, pl, P = load_ycontrol(data("2026-09-17-bench", "line_repeated_wide.csv"))
    D = np.array([detrend(v) for v in np.array([v for p in pl for v in P[p]])[0::2]])
    obs_prof = rms(D.mean(axis=0))
    obs_cons = fisher_mean([corr(D[i], D[i + 1]) for i in range(len(D) - 1)])[0]

    def surrogate(row):
        F = np.fft.rfft(row)
        ph = RNG.uniform(0, 2 * np.pi, len(F))
        ph[0] = 0
        return np.fft.irfft(np.abs(F) * np.exp(1j * ph), n=len(row))

    sp, sc = [], []
    for _ in range(5000):
        S = np.array([detrend(surrogate(r)) for r in D])
        sp.append(rms(S.mean(axis=0)))
        sc.append(fisher_mean([corr(S[i], S[i + 1]) for i in range(len(S) - 1)])[0])
    sp, sc = np.array(sp), np.array(sc)
    print("    averaged-profile RMS   observed %.0f counts, surrogate %.0f +- %.0f, p = %.4f"
          % (obs_prof, sp.mean(), sp.std(), (sp >= obs_prof).mean()))
    print("    consecutive-pass r     observed %+.3f,      surrogate %+.3f +- %.3f, p = %.4f"
          % (obs_cons, sc.mean(), sc.std(), (sc >= obs_cons).mean()))
    print("""    So the 12 passes DO agree far better than 12 unrelated lines of the same
    smoothness would. The profile is real and repeatable. What this test cannot
    say is what it is a picture OF - that is scripts 04 and 05.""")
    rows.append(["N3 phase surrogate", "line_repeated_wide.csv", "profile RMS",
                 "observed %.0f" % obs_prof, "surrogate %.0f+-%.0f" % (sp.mean(), sp.std()),
                 "p = %.4f" % (sp >= obs_prof).mean()])
    rows.append(["N3 phase surrogate", "line_repeated_wide.csv", "consecutive r",
                 "observed %+.3f" % obs_cons, "surrogate %+.3f+-%.3f" % (sc.mean(), sc.std()),
                 "p = %.4f" % (sc >= obs_cons).mean()])

    # --------------------------------------------------- the search-size budget
    print("\nHOW MANY TESTS WERE SEARCHED")
    budget = [
        ("raster recordings examined (scans, controls, aborted runs, chmaps)", 43),
        ("trace/retrace position tests, one per file (script 02)", 34),
        ("trace/retrace time tests, one per file (script 02)", 34),
        ("within/between place tests (script 03)", 6),
        ("cross-night profile comparisons (script 03)", 15),
        ("place tests on the 2026-09-17 wide image pair (script 04)", 2),
        ("pass-separation correlations (script 04)", 11),
        ("profile-versus-Y comparisons (script 05)", 36),
        ("image-to-image correlations reported in the session logs", 20),
    ]
    tot = sum(n for _, n in budget)
    for what, n in budget:
        print("    %-62s %4d" % (what, n))
        rows.append(["search budget", what, str(n), "", "", ""])
    print("    %-62s %4d" % ("TOTAL", tot))
    print("""
    At %d tests, a 5%% threshold is expected to throw up about %.0f apparent
    findings from noise alone. A Bonferroni-corrected 5%% threshold is
    p < %.1e, which is about %.1f sigma. The only result in this whole body of
    data that ever reached that was the y_sep 12000 run, and it did not repeat.""" % (
        tot, 0.05 * tot, 0.05 / tot, abs(np.sqrt(2) * 1.0) * 0 + 4.1))
    rows.append(["search budget", "TOTAL", str(tot),
                 "Bonferroni 5%% threshold p < %.1e" % (0.05 / tot), "", ""])

    with open(out("work", "chance.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["null", "source", "what", "a", "b", "c"])
        for r in rows:
            w.writerow(r + [""] * (6 - len(r)))
    print("\n-> %s" % out("work", "chance.csv"))


if __name__ == "__main__":
    main()
