"""Figure 4 - the control, and what it settled.

    python3 deliverables/2026-09-19-pause/figures/code/fig04_control.py

WHAT A CONTROL IS FOR. Every scan was immediately followed by an X-HELD control: the same
loop, the same junction, the same number of points, with the lateral sweep switched off.
X never moves, so a control cannot contain surface structure by construction. Whatever it
produces is the instrument talking to itself. It is the cheapest and most decisive test
this project ran, and it is what stopped a plausible-looking picture being believed.

SOURCE. `sessions/data/2026-09-19-bench/cas9_scan0-3.csv` and `cas9_xheld0-3.csv`,
measured 2026-09-19 from about 03:48 UTC, `sessions/2026-09-19-bench.md` section 3.14.
Every number on this figure is recomputed here from those CSVs, with the same statistics
the project's own tool uses (`sessions/data/2026-09-19-bench/scripts/analyze_scans.py`
and `Code/pc/stm_y_control.py`: remove each line's straight-line tilt, then correlate the
flattened forward images).

THE CORRECTION THIS FIGURE CARRIES.
`deliverables/2026-09-19-pause/LEAD_VERIFICATION.md` V4: the published control mean of
+0.37 came from `cas9_xheld2.csv`, which is a ONE-LINE file - the run aborted after the
first line - and the comparison silently truncated both images to the shorter one, so two
of the three control correlations were computed over 21 points instead of 231. Dropping
that file and using full images only gives +0.04 for the scans and +0.07 for the
controls: indistinguishable. This script therefore uses only equal-length, full-image
pairs, and refuses to correlate two images of different length rather than truncating.

WHAT IS AND IS NOT CLAIMED. Neither the scans nor the controls reproduce. That is the
result. It is NOT a claim that the controls beat the scans, and neither panel here is an
image of a surface: this project has never produced an image.
"""
from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stmstyle as S  # noqa: E402

SESSION = "2026-09-19-bench"
SCANS = ["cas9_scan0.csv", "cas9_scan1.csv", "cas9_scan2.csv", "cas9_scan3.csv"]
CONTROLS = ["cas9_xheld0.csv", "cas9_xheld1.csv", "cas9_xheld2.csv", "cas9_xheld3.csv"]


# --- the project's own statistics, reimplemented exactly -----------------------------

def detrend(ys):
    """Remove the straight-line tilt from one pass (Code/pc/stm_y_control.py)."""
    n = len(ys)
    if n < 3:
        return list(ys)
    mx = (n - 1) / 2.0
    my = sum(ys) / float(n)
    sxx = sum((i - mx) ** 2 for i in range(n))
    sxy = sum((i - mx) * (v - my) for i, v in enumerate(ys))
    slope = sxy / sxx if sxx else 0.0
    return [v - (my + slope * (i - mx)) for i, v in enumerate(ys)]


def corr(a, b):
    n = len(a)
    if n != len(b) or n < 3:
        return None
    ma, mb = sum(a) / n, sum(b) / n
    sa = math.sqrt(sum((x - ma) ** 2 for x in a))
    sb = math.sqrt(sum((y - mb) ** 2 for y in b))
    if sa == 0 or sb == 0:
        return None
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / (sa * sb)


def rms(xs):
    m = sum(xs) / len(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / len(xs))


def load(name):
    """(x codes, y codes, forward passes) from a feedback-scan CSV."""
    path = S.data_path(SESSION, name)
    with open(path) as f:
        head = f.readline().strip().split(",")
        xs = [int(c) for c in head[2:]]
        fwd = {}
        for line in f:
            p = line.strip().split(",")
            if len(p) < 3 or p[1] != "fwd":
                continue
            fwd[int(p[0])] = [float(v) for v in p[2:]]
    ys = sorted(fwd)
    return xs, ys, [fwd[y] for y in ys]


def flat(name):
    _xs, _ys, F = load(name)
    return [v for row in F for v in detrend(row)]


def main():
    # ---- the numbers, recomputed ----------------------------------------------------
    stats = {}
    for n in SCANS + CONTROLS:
        xs, ys, F = load(n)
        fl = [v for row in F for v in detrend(row)]
        stats[n] = dict(lines=len(ys), npts=len(fl), corrugation=rms(fl))
        print("%-18s lines %2d  points %3d  corrugation %6.1f counts"
              % (n, len(ys), len(fl), rms(fl)))

    full_scans = [n for n in SCANS if stats[n]["npts"] == 231]
    full_ctrls = [n for n in CONTROLS if stats[n]["npts"] == 231]
    dropped = [n for n in CONTROLS if stats[n]["npts"] != 231]
    print("dropped as not a full image: %s" % (dropped or "none"))

    def pairs(names):
        out = []
        for a, b in zip(names, names[1:]):
            fa, fb = flat(a), flat(b)
            if len(fa) != len(fb):           # never truncate: that is the V4 defect
                continue
            out.append((a, b, corr(fa, fb), len(fa)))
        return out

    sp = pairs(full_scans)
    cp = pairs(full_ctrls)
    se = 1.0 / math.sqrt(231 - 3)            # Fisher-z standard error at n = 231
    for tag, ps in (("real scans", sp), ("X-held controls", cp)):
        print("%-16s %s  mean %+.3f  (se per pair %.3f)"
              % (tag, " ".join("%+.3f" % c for _a, _b, c, _n in ps),
                 sum(c for _a, _b, c, _n in ps) / len(ps), se))

    # ---- the figure -----------------------------------------------------------------
    from cmcrameri import cm as ccm
    import numpy as np

    show_scan, show_ctrl = "cas9_scan1.csv", "cas9_xheld0.csv"
    maps = {}
    for n in (show_scan, show_ctrl):
        xs, ys, F = load(n)
        maps[n] = (np.array(xs), np.array(ys), np.array([detrend(r) for r in F]))
    vmax = max(float(np.abs(m[2]).max()) for m in maps.values())

    S.set_theme("light")
    fig = S.plt.figure(figsize=(11.2, 6.6))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.0, 1.0, 1.55],
                          left=0.052, right=0.985, top=0.755, bottom=0.255, wspace=0.34)
    axa = fig.add_subplot(gs[0, 0])
    axb = fig.add_subplot(gs[0, 1])
    axc = fig.add_subplot(gs[0, 2])

    for ax, name, head in ((axa, show_scan, "A feedback scan"),
                           (axb, show_ctrl, "Its X-held control")):
        X, Y, Z = maps[name]
        ext = [X.min(), X.max(), Y.min(), Y.max()]
        im = ax.imshow(Z, cmap=ccm.vik, vmin=-vmax, vmax=+vmax, origin="lower",
                       extent=ext, aspect="auto", interpolation="nearest")
        ax.grid(False)
        ax.set_xticks([X.min(), X.max()])
        ax.set_yticks([Y.min(), Y.max()])
        ax.set_xticklabels([format(int(X.min()), ","), format(int(X.max()), ",")])
        ax.set_yticklabels([format(int(Y.min()), ","), format(int(Y.max()), ",")])
        ax.set_xlabel("X piezo counts", labelpad=6)
        ax.set_title("%s\n%s\ncorrugation %.0f counts"
                     % (head, "the tip swept across X" if name == show_scan
                        else "X never moved at all",
                        stats[name]["corrugation"]))
    axa.set_ylabel("Y piezo counts", labelpad=6)

    cb = fig.colorbar(im, ax=[axa, axb], orientation="horizontal", fraction=0.075,
                      pad=0.17, aspect=38)
    cb.set_label("Z the loop needed, after each line's tilt is removed (counts)."
                 "  Zero is that line's own average.",
                 color=S.C["ink2"], fontsize=S.TYPE["small"], labelpad=7)
    cb.ax.tick_params(colors=S.C["muted"], labelsize=S.TYPE["small"])
    cb.outline.set_visible(False)

    # ---- panel C: every image-to-image correlation, with its uncertainty -------------
    rows = [(1.0, sp, S.series(0), "Feedback scans"),
            (0.0, cp, S.series(1), "X-held controls")]
    axc.axvline(0, color=S.C["ink"], lw=1.4, zorder=2)
    for y, ps, col, lab in rows:
        vals = [c for _a, _b, c, _n in ps]
        for k, v in enumerate(vals):
            yy = y + (k - (len(vals) - 1) / 2.0) * 0.16
            axc.errorbar([v], [yy], xerr=[se], fmt="o", color=col, ms=9,
                         markeredgecolor=S.C["surface"], markeredgewidth=2.0,
                         ecolor=col, elinewidth=2.0, capsize=0, zorder=5, alpha=0.95)
        m = sum(vals) / len(vals)
        axc.plot([m, m], [y - 0.30, y + 0.30], "-", color=S.C["ink"], lw=2.0, zorder=6)
        S.key(axc, m, y + 0.345, "mean %+.2f" % m, ha="center", va="bottom")
        S.note(axc, -0.44, y, "%s\n%d pairs" % (lab, len(ps)), ha="left", va="center",
               color=S.C["ink"], fontweight=S.W_EMPH)

    axc.set_ylim(-0.62, 1.62)
    axc.set_xlim(-0.46, 0.46)
    axc.set_yticks([])
    axc.spines["left"].set_visible(False)
    S.tidy(axc, xlabel="How well one image repeats the next (correlation)", grid="x")
    axc.set_title("Both sit on zero. Bars are ±1 standard error\n"
                  "on each pair (231 points each).")
    S.note(axc, 0.0, -0.50, "no repeatability", ha="center", va="center",
           fontsize=S.TYPE["small"])

    S.titles_keyed(
        fig,
        "The control that stopped us fooling ourselves",
        "After every scan we ran the same scan again with the lateral sweep switched off, so <the control> could "
        "not contain surface\nstructure at all. <The real scans> repeat no better than those controls do. That "
        "single test is what settles the imaging question —\nand running it was the right thing to do.",
        [{"color": S.word(1), "fontweight": S.W_EMPH},
         {"color": S.word(0), "fontweight": S.W_EMPH}])

    S.footer(fig, y=0.008, text=
             "Source: sessions/data/2026-09-19-bench/cas9_scan0-3.csv and cas9_xheld0-3.csv, measured 2026-09-19 "
             "from about 03:48 UTC; sessions/2026-09-19-bench.md section 3.14. Every number here is recomputed "
             "from those files by this script.\n"
             "CORRECTION CARRIED: the previously published control mean of +0.37 came from cas9_xheld2.csv, a "
             "ONE-LINE file whose run aborted, silently truncated to 21 points against another image's first "
             "line (LEAD_VERIFICATION.md V4). Only\nfull 231-point images are used here, and this script refuses "
             "to correlate two images of different length. The honest comparison is +0.04 against +0.07.\n"
             "NEITHER PANEL IS AN IMAGE OF A SURFACE. They are the Z code the feedback loop asked for at each "
             "point, with each line's tilt removed; the colour map is Crameri's vik, centred on zero, and "
             "nothing is interpolated or smoothed.\nAxes are in DAC counts because this instrument has never "
             "established a distance scale from its own hardware. WHAT THIS DOES NOT SHOW: with 3 and 2 pairs, "
             "neither mean is distinguishable from zero or from the other —\nthe comparison was never "
             "powered to support \"better\", in either direction.")

    S.save(fig, "fig04_control")


if __name__ == "__main__":
    main()
