"""10 - Every gallery figure. RAW and PROCESSED side by side, captioned.

Run from the repository root:

    python3 deliverables/2026-09-19-pause/candidates/code/10_gallery_figures.py

Writes PNGs into deliverables/2026-09-19-pause/candidates/gallery/.

RULES FOLLOWED HERE
-------------------
  * Every figure shows the RAW recorded Z DAC codes as well as anything derived.
  * The ONLY transformation applied anywhere is a least-squares straight line in
    X removed from each pass, and it is named in the panel title every time.
  * No smoothing, no interpolation, no denoising, no inpainting, no
    super-resolution, no reconstruction of any kind. Every pixel drawn is a
    number that came off the instrument, or a plain average of such numbers.
  * Colour scales are stated in the caption and are symmetric about zero for
    detrended panels so that a bump and a dip look equally strong.
  * Where a control exists it is drawn on the SAME colour scale as the scan it
    controls, because a control on its own scale always looks like an image.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from stmload import load_raster, load_ycontrol, data, out, detrend, corr, rms, fisher_mean

plt.rcParams.update({
    "figure.dpi": 150, "savefig.dpi": 150, "font.size": 8.5,
    "axes.titlesize": 9, "axes.labelsize": 8.5, "axes.grid": True,
    "grid.alpha": 0.25, "grid.linewidth": 0.5, "figure.facecolor": "white",
    "savefig.bbox": "tight", "axes.spines.top": False, "axes.spines.right": False,
})
CMAP = "RdBu_r"


def G(name):
    return out("gallery", name)


def imshow(ax, M, xs, ys, vmax=None, cmap=CMAP, label="Z DAC counts"):
    if vmax is None:
        vmax = np.abs(M).max() or 1
    im = ax.imshow(M, aspect="auto", origin="lower", cmap=cmap, vmin=-vmax, vmax=vmax,
                   extent=[xs[0], xs[-1], ys[0], ys[-1]], interpolation="nearest")
    ax.set_xlabel("X DAC code")
    ax.set_ylabel("Y DAC code")
    ax.grid(False)
    cb = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
    cb.set_label(label, fontsize=7.5)
    cb.ax.tick_params(labelsize=7)
    return im


# ---------------------------------------------------------------- figure 1
def fig_candidate_a():
    """The 2026-09-17 +-15,000 twelve-pass profile - the strongest candidate."""
    xs, pl, P = load_ycontrol(data("2026-09-17-bench", "line_repeated_wide.csv"))
    raw = np.array([v for p in pl for v in P[p]])[0::2]
    D = np.array([detrend(v) for v in raw])
    prof = D.mean(axis=0)

    fig = plt.figure(figsize=(11, 7.2))
    gs = GridSpec(2, 3, figure=fig, hspace=0.42, wspace=0.3)

    ax = fig.add_subplot(gs[0, 0])
    for i, r in enumerate(raw):
        ax.plot(xs, r, lw=0.9, alpha=0.85)
    ax.set_title("RAW - 12 passes of one line, as recorded\nno processing at all")
    ax.set_xlabel("X DAC code")
    ax.set_ylabel("Z DAC code the loop needed")

    ax = fig.add_subplot(gs[0, 1])
    for r in D:
        ax.plot(xs, r, lw=0.9, alpha=0.7)
    ax.plot(xs, prof, "k", lw=2.4, label="mean of 12")
    ax.set_title("PROCESSED - straight line in X removed\nfrom each pass, nothing else")
    ax.set_xlabel("X DAC code")
    ax.set_ylabel("Z counts about the local tilt")
    ax.legend(fontsize=7.5, frameon=False)

    ax = fig.add_subplot(gs[0, 2])
    ax.plot(xs, D[0::2].mean(axis=0), lw=1.8, label="odd passes (6)")
    ax.plot(xs, D[1::2].mean(axis=0), lw=1.8, label="even passes (6)")
    ax.set_title("SPLIT HALF - r = %+.3f\nit really does repeat" % corr(D[0::2].mean(axis=0),
                                                                       D[1::2].mean(axis=0)))
    ax.set_xlabel("X DAC code")
    ax.set_ylabel("Z counts")
    ax.legend(fontsize=7.5, frameon=False)

    ax = fig.add_subplot(gs[1, 0])
    lags = range(1, len(D))
    ax.plot(list(lags), [fisher_mean([corr(D[i], D[i + L])
                                      for i in range(len(D) - L)])[0] for L in lags],
            "o-", lw=1.5, ms=4)
    ax.axhline(0, color="k", lw=0.8)
    ax.set_title("Agreement does NOT decay with time\n(passes ~5 s apart)")
    ax.set_xlabel("separation between passes")
    ax.set_ylabel("mean r")
    ax.set_ylim(-0.4, 1)

    ax = fig.add_subplot(gs[1, 1])
    t = np.arange(len(prof), dtype=float)
    ax.plot(xs, prof, "k", lw=2.2, label="the 636-count profile")
    for deg, st in ((2, "--"), (4, ":")):
        ax.plot(xs, np.polyval(np.polyfit(t, prof, deg), t), st, lw=1.4,
                label="degree %d fit (%.0f%%)" % (
                    deg, 100 * (1 - np.var(prof - np.polyval(np.polyfit(t, prof, deg), t))
                                / np.var(prof))))
    ax.set_title("It is NOT a simple bow\na parabola explains only 15%")
    ax.set_xlabel("X DAC code")
    ax.set_ylabel("Z counts")
    ax.legend(fontsize=7, frameon=False)

    ax = fig.add_subplot(gs[1, 2])
    ax.axis("off")
    ax.text(0, 1, "CANDIDATE A\n"
            "sessions/data/2026-09-17-bench/line_repeated_wide.csv\n\n"
            "12 passes of one line, X 17768-47768 (+-15,000 counts),\n"
            "21 points 1500 apart. 2026-09-17 bench, ~20:00 UTC.\n\n"
            "per-pass RMS after detrending   864 counts\n"
            "averaged profile                636 counts\n"
            "consecutive-pass r              +0.647\n"
            "odd-half vs even-half r         +0.923\n"
            "phase-randomised surrogate      p < 2e-4\n\n"
            "IT IS REAL AND IT REPEATS.\n"
            "What it is a picture OF is figure 2.\n\n"
            "Every fwd/back row pair in this file is byte-\n"
            "identical: the scratch tool stored the forward\n"
            "pass twice. All 12 passes above are FORWARD.",
            va="top", ha="left", fontsize=7.6, family="monospace")
    fig.suptitle("Candidate A - the 636-count profile at +-15,000 X, 2026-09-17", y=0.985,
                 fontsize=11, fontweight="bold")
    fig.savefig(G("01_candidateA_wide_profile.png"))
    plt.close(fig)
    return prof, xs


# ---------------------------------------------------------------- figure 2
def fig_candidate_a_place(prof, xs):
    """The place test that decides candidate A."""
    _, ys1, F1, B1 = load_raster(data("2026-09-17-bench", "scan_wide_25nm_1.csv"))
    _, ys2, F2, B2 = load_raster(data("2026-09-17-bench", "scan_wide_25nm_2.csv"))
    D1 = np.array([detrend(f) for f in F1])
    D2 = np.array([detrend(f) for f in F2])

    fig = plt.figure(figsize=(11.5, 7.6))
    gs = GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35)

    v = max(np.abs(F1 - F1.mean()).max(), np.abs(F2 - F2.mean()).max())
    ax = fig.add_subplot(gs[0, 0])
    imshow(ax, F1 - F1.mean(), xs, ys1, vmax=v)
    ax.set_title("RAW image 1, mean subtracted\nscan_wide_25nm_1.csv, forward")
    ax = fig.add_subplot(gs[0, 1])
    imshow(ax, F2 - F2.mean(), xs, ys1, vmax=v)
    ax.set_title("RAW image 2, mean subtracted\nscan_wide_25nm_2.csv, forward")

    vd = max(np.abs(D1).max(), np.abs(D2).max())
    ax = fig.add_subplot(gs[1, 0])
    imshow(ax, D1, xs, ys1, vmax=vd)
    ax.set_title("PROCESSED image 1 - line detrended")
    ax = fig.add_subplot(gs[1, 1])
    imshow(ax, D2, xs, ys1, vmax=vd)
    ax.set_title("PROCESSED image 2 - same scale")

    ax = fig.add_subplot(gs[0, 2])
    same = [corr(D1[k], D2[k]) for k in range(len(ys1))]
    other = [corr(D1[i], D2[j]) for i in range(len(ys1)) for j in range(len(ys1)) if i != j]
    ax.hist(other, bins=14, alpha=0.65, density=True, label="different place (72)")
    for s in same:
        ax.axvline(s, color="crimson", lw=1.2, alpha=0.9)
    ax.axvline(np.nan, color="crimson", lw=1.2, label="same place (9)")
    ax.set_title("THE PLACE TEST\nsame %+.3f, different %+.3f, p = 0.24"
                 % (fisher_mean(same)[0], fisher_mean(other)[0]))
    ax.set_xlabel("correlation between two lines")
    ax.set_ylabel("density")
    ax.legend(fontsize=7, frameon=False)

    ax = fig.add_subplot(gs[1, 2])
    ax.axis("off")
    ax.text(0, 1, "THE TEST THAT DECIDES CANDIDATE A\n\n"
            "sessions/2026-09-17-bench.md 3.25 says the test\n"
            "that would settle the 636-count profile - the same\n"
            "line at separated Y positions AT +-15,000 - had\n"
            "never been run.\n\n"
            "IT DID NOT NEED TO BE. scan_wide_25nm_1.csv and\n"
            "_2.csv are two complete images of the SAME nine Y\n"
            "places on the SAME X grid, taken the same night\n"
            "with the same tip and the same gold. That is nine\n"
            "same-place pairs and 72 different-place pairs.\n\n"
            "same place    r = +0.216 +- 0.228\n"
            "other place   r = +0.074 +- 0.063\n"
            "permutation   p = 0.24 (forward)\n"
            "              p = 0.28 (backward)\n"
            "with a lag allowed on every line: +0.744 against\n"
            "+0.641, and the lag search alone buys +0.51 +- 0.15\n"
            "from phase-randomised noise.\n\n"
            "A place this profile belongs to is not detected.\n"
            "POWER: with 9 pairs this can only exclude a\n"
            "same-minus-other difference bigger than about\n"
            "+0.47. A weak surface signal is NOT excluded.",
            va="top", ha="left", fontsize=7.4, family="monospace")
    fig.suptitle("Candidate A decided - two images of nine places at the same width, 2026-09-17",
                 y=0.985, fontsize=11, fontweight="bold")
    fig.savefig(G("02_candidateA_place_test.png"))
    plt.close(fig)


# ---------------------------------------------------------------- figure 3
def fig_candidate_b():
    """The three-Y control at y_sep 12000 - the 3.9 sigma run and its repeat."""
    fig = plt.figure(figsize=(11.5, 7.6))
    gs = GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.33)
    files = [("ycontrol_run2_ysep12000.csv", "run 2 - the 3.9 sigma run", 0),
             ("ycontrol_run4_ysep12000_repeat.csv", "run 4 - the REPEAT", 1),
             ("ycontrol_run3_ysep12000_xheld.csv", "run 3 - X-HELD CONTROL", 2)]
    for nm, title, col in files:
        xs, places, P = load_ycontrol(data("2026-09-19-bench", nm))
        ax = fig.add_subplot(gs[0, col])
        for p in places:
            for v in P[p]:
                ax.plot(xs, v, lw=0.8, alpha=0.8)
        ax.set_title("RAW - %s\n%s" % (title, nm), fontsize=8)
        ax.set_xlabel("X DAC code")
        ax.set_ylabel("Z DAC code")
        ax = fig.add_subplot(gs[1, col])
        for p, c in zip(places, ["tab:blue", "tab:orange", "tab:green"]):
            M = np.array([detrend(v) for v in P[p]])
            ax.plot(xs, M.mean(axis=0), color=c, lw=2, label="Y %+d" % p)
            for v in M:
                ax.plot(xs, v, color=c, lw=0.6, alpha=0.35)
        ax.set_title("PROCESSED - detrended, by place", fontsize=8)
        ax.set_xlabel("X DAC code")
        ax.set_ylabel("Z counts")
        ax.legend(fontsize=7, frameon=False)
        if col == 2:
            ax.set_ylim(-120, 120)
    fig.suptitle("Candidate B - the three-Y control at 12,000 counts apart, 2026-09-19 bench\n"
                 "run 2 within-minus-between +0.523 (permutation p = 0.0036);  "
                 "run 4 repeat +0.059 (p = 0.26);  X-held control +0.226 (p = 0.02)",
                 y=0.99, fontsize=10, fontweight="bold")
    fig.savefig(G("03_candidateB_three_y.png"))
    plt.close(fig)


# ---------------------------------------------------------------- figure 4
def fig_feedback_scans():
    """The 2026-09-19 feedback scans against their own X-held controls."""
    names = [("cas9_scan0.csv", "scan 0"), ("cas9_scan1.csv", "scan 1"),
             ("cas9_scan2.csv", "scan 2"), ("cas9_scan3.csv", "scan 3"),
             ("cas9_xheld0.csv", "CONTROL 0"), ("cas9_xheld1.csv", "CONTROL 1"),
             ("cas9_xheld3.csv", "CONTROL 3")]
    # cas9_xheld2.csv is deliberately absent: it is ONE line, the run aborted,
    # and folding it into an image-to-image mean is the defect the lead found.
    fig, axes = plt.subplots(2, 4, figsize=(13.5, 6.4))
    Ds = {}
    for nm, _ in names:
        xs, ys, F, B = load_raster(data("2026-09-19-bench", nm))
        Ds[nm] = (xs, ys, np.array([detrend(f) for f in F]))
    vd = np.percentile(np.abs(np.concatenate([d[2].ravel() for d in Ds.values()])), 99)
    for ax, (nm, lab) in zip(axes.ravel(), names):
        xs, ys, D = Ds[nm]
        imshow(ax, D, xs, ys, vmax=vd)
        ax.set_title("%s\n%s   RMS %.0f counts" % (lab, nm, np.mean([rms(d) for d in D])),
                     fontsize=7.6,
                     color=("crimson" if "CONTROL" in lab else "black"))
    axes.ravel()[-1].axis("off")
    axes.ravel()[-1].text(0, 1,
                          "ALL SEVEN ON ONE COLOUR SCALE\n"
                          "+-%.0f Z counts, each line detrended.\n\n"
                          "The four on the left had X scanning.\n"
                          "The three in red had X STANDING STILL:\n"
                          "there is no sample structure in them at\n"
                          "all, by construction.\n\n"
                          "image-to-image r, forward, FULL images\n"
                          "only (231 points each):\n"
                          "   scans    +0.09 +0.18 -0.15  mean +0.04\n"
                          "   controls +0.20      -0.06  mean +0.07\n\n"
                          "NEITHER reproduces. Both means are\n"
                          "indistinguishable from zero and from\n"
                          "each other.\n\n"
                          "CORRECTION, found by the lead on\n"
                          "2026-09-19: the published +0.37 for the\n"
                          "controls folded in TWO 21-point\n"
                          "correlations against cas9_xheld2.csv,\n"
                          "which is a single aborted line. The\n"
                          "controls do NOT reproduce better. The\n"
                          "scans still do not reproduce at all,\n"
                          "which is what carries the conclusion." % vd,
                          va="top", ha="left", fontsize=7.4, family="monospace")
    fig.suptitle("The 2026-09-19 feedback scans and their X-held controls, on one scale\n"
                 "full images only - the one-line aborted control is excluded, see caption",
                 y=1.02, fontsize=10.5, fontweight="bold")
    fig.tight_layout()
    fig.savefig(G("04_feedback_scans_vs_controls.png"))
    plt.close(fig)


# ---------------------------------------------------------------- figure 5
def fig_wide_images():
    """The wide 2026-09-19 images: trace/retrace, and the lag sweep."""
    def sweep(F, B, mx=12):
        per = {}
        for f, b in zip(F, B):
            fd, bd = detrend(f), detrend(b)
            n = len(fd)
            for L in range(-mx, mx + 1):
                x, y = (fd[L:], bd[:n - L]) if L > 0 else (
                    (fd[:n + L], bd[-L:]) if L < 0 else (fd, bd))
                if len(x) >= 9:
                    c = corr(x, y)
                    if c is not None:
                        per.setdefault(L, []).append(c)
        return {L: fisher_mean(v)[0] for L, v in per.items()}

    fig = plt.figure(figsize=(12.5, 7.2))
    gs = GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.34)
    xs, ys, F, B = load_raster(data("2026-09-19-bench", "img_scan_2.csv"))
    ax = fig.add_subplot(gs[0, 0])
    imshow(ax, F - F.mean(), xs, ys)
    ax.set_title("RAW forward, mean subtracted\nimg_scan_2.csv")
    ax = fig.add_subplot(gs[0, 1])
    imshow(ax, B - B.mean(), xs, ys)
    ax.set_title("RAW backward, mean subtracted\nsame lines, other direction")
    ax = fig.add_subplot(gs[1, 0])
    DF = np.array([detrend(f) for f in F])
    DB = np.array([detrend(b) for b in B])
    v = max(np.abs(DF).max(), np.abs(DB).max())
    imshow(ax, DF, xs, ys, vmax=v)
    ax.set_title("PROCESSED forward - line detrended")
    ax = fig.add_subplot(gs[1, 1])
    imshow(ax, DB, xs, ys, vmax=v)
    ax.set_title("PROCESSED backward - same scale\nnote it is the MIRROR IMAGE, not a repeat")

    ax = fig.add_subplot(gs[:, 2])
    for nm, style, lab in [("img_scan_2.csv", "-", "wide scan 2 (X moving)"),
                           ("img_scan_1.csv", "-", "wide scan 1 (X moving)"),
                           ("img_xheld_0.csv", "--", "X-HELD control 0"),
                           ("img_xheld_1.csv", "--", "X-HELD control 1")]:
        _, _, f_, b_ = load_raster(data("2026-09-19-bench", nm))
        m = sweep(f_, b_)
        ax.plot(sorted(m), [m[L] for L in sorted(m)], style, lw=1.8, marker="o", ms=3, label=lab)
    ax.axhline(0, color="k", lw=0.8)
    ax.axvline(0, color="k", lw=0.8)
    ax.set_xlabel("shift of the backward pass, pixels (1 px = 1500 X counts)")
    ax.set_ylabel("trace-retrace correlation")
    ax.set_title("THE SHAPE OF THE ANTI-CORRELATION\n"
                 "lowest at zero shift, high at BOTH +-10:\n"
                 "a roughly line-periodic signal, mirrored")
    ax.legend(fontsize=7, frameon=False, loc="lower center")
    fig.suptitle("The wide +-15,000 images, 2026-09-19 bench - trace against retrace",
                 y=0.99, fontsize=11, fontweight="bold")
    fig.savefig(G("05_wide_images_trace_retrace.png"))
    plt.close(fig)


# ---------------------------------------------------------------- figure 6
def fig_cross_night():
    """Does any wide profile survive from one night to the next?"""
    xs, pl, P = load_ycontrol(data("2026-09-17-bench", "line_repeated_wide.csv"))
    prof17 = np.array([detrend(v) for v in
                       np.array([v for p in pl for v in P[p]])[0::2]]).mean(axis=0)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.3))
    ax1.plot(xs, prof17, "k", lw=2.4, label="2026-09-17, 636 counts")
    for nm, lab in [("ycontrol_run1.csv", "2026-09-19 run 1 (195)"),
                    ("ycontrol_run2_ysep12000.csv", "2026-09-19 run 2 (51)"),
                    ("ycontrol_run4_ysep12000_repeat.csv", "2026-09-19 run 4 (66)"),
                    ("ycontrol_xheld_run1.csv", "2026-09-19 X-HELD (9)")]:
        x2, pls, P2 = load_ycontrol(data("2026-09-19-bench", nm))
        m = np.array([detrend(v) for p in pls for v in P2[p]]).mean(axis=0)
        ax1.plot(x2, m, lw=1.5, alpha=0.9, label="%s  r %+.2f" % (lab, corr(prof17, m)))
    ax1.set_title("Mean detrended profile, identical X grid, two nights\n"
                  "nothing carries over: r -0.18 to +0.41")
    ax1.set_xlabel("X DAC code")
    ax1.set_ylabel("Z counts")
    ax1.legend(fontsize=7, frameon=False)

    x2, pls, P2 = load_ycontrol(data("2026-09-19-bench", "ycontrol_run1.csv"))
    m_scan = np.array([detrend(v) for p in pls for v in P2[p]]).mean(axis=0)
    x3, pls3, P3 = load_ycontrol(data("2026-09-19-bench", "ycontrol_xheld_run1.csv"))
    m_ctrl = np.array([detrend(v) for p in pls3 for v in P3[p]]).mean(axis=0)
    ax2.plot(x2, m_scan / rms(m_scan), lw=2.2, label="run 1, X scanning (195 counts)")
    ax2.plot(x3, m_ctrl / rms(m_ctrl), lw=2.2, ls="--", label="its X-HELD control (9 counts)")
    ax2.set_title("THE SAME NIGHT'S CONTROL HAS THE SAME SHAPE\n"
                  "r = %+.2f, scaled to equal size to show it\n"
                  "X never moved in the dashed one" % corr(m_scan, m_ctrl))
    ax2.set_xlabel("X DAC code")
    ax2.set_ylabel("normalised Z")
    ax2.legend(fontsize=7.5, frameon=False)
    fig.suptitle("Cross-night and cross-control comparison of the wide profile",
                 y=1.03, fontsize=11, fontweight="bold")
    fig.savefig(G("06_cross_night_profiles.png"))
    plt.close(fig)


# ---------------------------------------------------------------- figure 7
def fig_rejected():
    """The rejected and partial recordings, shown rather than described."""
    fig, axes = plt.subplots(2, 3, figsize=(12.5, 6.6))
    ax = axes[0, 0]
    xs, ys, F, B = load_raster(data("2026-09-19-bench", "cas8_chmap_t1_scan_1789789628.csv"))
    ax.imshow(F, aspect="auto", origin="lower", cmap="gray",
              extent=[xs[0], xs[-1], ys[0], ys[-1]], interpolation="nearest")
    ax.set_title("cas8 constant-height map\nEVERY pixel 32767 - amplifier railed", fontsize=8)
    ax.grid(False)
    ax = axes[0, 1]
    for nm, lab in [("tuned_s3k_scan1.csv", "tuned scan 1"),
                    ("tuned_s3k_scan2.csv", "tuned scan 2"),
                    ("tuned_s3k_xheld1.csv", "tuned CONTROL 1")]:
        xs, ys, F, B = load_raster(data("2026-09-19-morning", nm))
        for f in F:
            ax.plot(xs, f, lw=0.8, alpha=0.75)
    ax.axhline(48000, color="crimson", ls="--", lw=1.2)
    ax.axhline(12000, color="crimson", ls="--", lw=1.2)
    ax.set_title("2026-09-19 morning tuned scans, RAW\nall six pinned on a clamp (red)", fontsize=8)
    ax.set_xlabel("X DAC code")
    ax.set_ylabel("Z DAC code")
    ax = axes[0, 2]
    xs, ys, F, B = load_raster(data("2026-09-19-bench", "img_scan_0.csv"))
    ax.plot(xs, F[0], lw=1.6, label="forward")
    ax.plot(xs, B[0], lw=1.6, label="backward")
    ax.set_title("img_scan_0.csv - aborted after ONE line\nraw, no processing", fontsize=8)
    ax.set_xlabel("X DAC code")
    ax.set_ylabel("Z DAC code")
    ax.legend(fontsize=7, frameon=False)

    ax = axes[1, 0]
    xs, ys, F, B = load_raster(data("2026-09-17-bench", "diag_scan_x_held.csv"))
    D = np.array([detrend(f) for f in F])
    imshow(ax, D, xs, ys, vmax=np.abs(D).max())
    ax.set_title("2026-09-17 X-HELD CONTROL, detrended\nRMS 87 counts - and X never moved", fontsize=8)
    ax = axes[1, 1]
    xs, ys, F, B = load_raster(data("2026-09-17-bench", "scan_fast_1.csv"))
    D2 = np.array([detrend(f) for f in F])
    imshow(ax, D2, xs, ys, vmax=np.abs(D).max())
    ax.set_title("a REAL 2026-09-17 scan on the same scale\nRMS 43 counts - HALF the control's", fontsize=8)
    ax = axes[1, 2]
    ax.axis("off")
    ax.text(0, 1, "THE REJECTED AND PARTIAL RECORDINGS\n\n"
            "Nine cas8 constant-height maps: 4,158 pixels,\n"
            "every one 32767. Zero information. Correctly\n"
            "recorded as saturated at the time.\n\n"
            "Six 2026-09-19 morning tuned scans: all six\n"
            "aborted against a Z clamp. Two at the top,\n"
            "four at the bottom with the tip pressed on the\n"
            "gold. No usable height data in any of them.\n\n"
            "img_scan_0 (1 line) and img_scan_1 (2 lines)\n"
            "aborted on saturation. Their lines behave like\n"
            "the completed one: trace/retrace -0.94, -0.92.\n\n"
            "Bottom row is the control that has done the\n"
            "most damage to this project's hopes: with X\n"
            "STANDING STILL the 2026-09-17 diagnostic shows\n"
            "TWICE the corrugation of a real scan taken the\n"
            "same night on the same junction.",
            va="top", ha="left", fontsize=7.3, family="monospace")
    fig.suptitle("What is in the recordings that were set aside", y=1.0, fontsize=11,
                 fontweight="bold")
    fig.tight_layout()
    fig.savefig(G("07_rejected_and_partial.png"))
    plt.close(fig)


# ---------------------------------------------------------------- figure 8
def fig_motion():
    """The gap's own motion - the mechanical blocker, measured."""
    fig, axes = plt.subplots(1, 3, figsize=(12.5, 3.9))
    ax = axes[0]
    for nm, lab in [("ztest_1789822585.csv", "-0.5 V, 30 cycles"),
                    ("bias_m05V_1789822770.csv", "-0.5 V repeat"),
                    ("bias_p05V_1789822770.csv", "+0.5 V"),
                    ("bias_p01V_1789822770.csv", "+0.1 V"),
                    ("bias_m01V_1789822770.csv", "-0.1 V")]:
        a = np.genfromtxt(data("2026-09-19-morning", nm), delimiter=",", names=True,
                          dtype=None, encoding="utf-8")
        ph = np.array([str(s) for s in a["phase"]])
        t, z, c = a["t"].astype(float), a["z"].astype(float), a["cycle"].astype(int)
        ot, oz = [], []
        for cc in sorted(set(c[ph == "in"])):
            m = (c == cc) & (ph == "in")
            ot.append(t[m][0])
            oz.append(z[m][0])
        ax.plot(ot, oz, "o-", ms=3, lw=1.1, label=lab)
    ax.set_xlabel("seconds into the run")
    ax.set_ylabel("Z DAC code where current appeared")
    ax.set_title("RAW - where the gap was, cycle by cycle\n2026-09-19 morning Z tests")
    ax.legend(fontsize=6.5, frameon=False)

    ax = axes[1]
    a = np.genfromtxt(data("2026-09-19-morning", "ztest_1789822585.csv"), delimiter=",",
                      names=True, dtype=None, encoding="utf-8")
    ph = np.array([str(s) for s in a["phase"]])
    t, z, c = a["t"].astype(float), a["z"].astype(float), a["cycle"].astype(int)
    ot, oz = [], []
    for cc in sorted(set(c[ph == "in"])):
        m = (c == cc) & (ph == "in")
        ot.append(t[m][0])
        oz.append(z[m][0])
    ot, oz = np.array(ot), np.array(oz)
    sl, ic = np.polyfit(ot, oz, 1)
    ax.plot(ot, oz - (sl * ot + ic), "o-", ms=4, lw=1.2, color="crimson")
    ax.axhline(0, color="k", lw=0.8)
    ax.set_xlabel("seconds into the run")
    ax.set_ylabel("Z counts about the straight-line drift")
    ax.set_title("PROCESSED - steady drift (%.0f counts/s) removed\n"
                 "what is left wanders by %.0f counts RMS" % (sl, (oz - (sl * ot + ic)).std()))

    ax = axes[2]
    ax.axis("off")
    ax.text(0, 1, "WHY THIS MATTERS FOR AN IMAGE\n\n"
            "A 21 x 11 image takes about 5 seconds.\n\n"
            "In 5 seconds this gap moves by hundreds to\n"
            "thousands of Z counts - the residual scatter\n"
            "above is 396 to 1,722 counts across the five\n"
            "runs, after the steady drift is taken out.\n\n"
            "The corrugation in every candidate image in\n"
            "this gallery is 13 to 460 counts.\n\n"
            "The thing being measured is SMALLER THAN THE\n"
            "WAY THE GAP MOVES WHILE IT IS BEING MEASURED.\n"
            "That is the single clearest reason no image\n"
            "survives, and it is a mechanical fact about\n"
            "the instrument, not a fault in the analysis.\n\n"
            "It is also the reason Jacob's hypothesis is\n"
            "the right shape: motion IS what stopped the\n"
            "imaging. What the data do not support is the\n"
            "second half of it - that a real image is\n"
            "sitting inside the recordings underneath it.",
            va="top", ha="left", fontsize=7.3, family="monospace")
    fig.suptitle("The gap's own motion - measured, 2026-09-19 morning", y=1.04,
                 fontsize=11, fontweight="bold")
    fig.tight_layout()
    fig.savefig(G("08_gap_motion.png"))
    plt.close(fig)


def main():
    prof, xs = fig_candidate_a()
    fig_candidate_a_place(prof, xs)
    fig_candidate_b()
    fig_feedback_scans()
    fig_wide_images()
    fig_cross_night()
    fig_rejected()
    fig_motion()
    for f in sorted(os.listdir(os.path.dirname(G("x")))):
        print("  gallery/%s" % f)


if __name__ == "__main__":
    main()
