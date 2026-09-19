"""Figure 3 - the gap will not hold still. The central negative result.

    python3 deliverables/2026-09-19-pause/figures/code/fig03_gap_motion.py

SOURCE. `sessions/data/2026-09-19-morning/release_watch_run1.log`, read verbatim by this
script - the nine lines it prints are the whole measurement. Measured 2026-09-19,
12:54:10 to 12:56:19 UTC, written up in `sessions/2026-09-19-morning.md` section 3.9.

WHAT WAS AND WAS NOT MOVING. The motor was still and nobody was touching the instrument.
The only thing being driven was the Z piezo, sweeping its range every 3 s looking for the
surface. Each point is the Z code at which current first appeared on that sweep - that is,
where the surface was at that moment.

THE FLAT "OUT OF REACH" SEGMENTS ARE NOT INVENTED. The watcher printed a line only when
the state changed, or on every contact:
`sessions/data/2026-09-19-morning/scripts/release_and_watch.py`,
`if state != last or state == "found"`. It swept every 3 s throughout. So between a
printed FAR and the next printed contact, every intervening sweep also reported FAR - that
is what "the state did not change" means. The segments are drawn from that, and the
caption says so.

RESOLUTION. Every onset is a multiple of 1,000: `fastwood.sweep` bound its step size as a
default argument, so the 250-count step the script asked for never took effect
(`sessions/data/2026-09-19-morning/README.md`). The motion is far larger than the step, so
the conclusion does not depend on it, but no onset here is better than +/-1,000 counts.

THE COMPARISON SCALE is `docs/FACTS.md`, "Tunnelling for comparison: a decade per ~6-13 Z
counts" - CALCULATED from a Z scale inherited from Dan Berard's scanner, never measured on
ours. It is drawn as a calculated band and labelled as one.
"""
from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stmstyle as S  # noqa: E402

LOG = S.data_path("2026-09-19-morning", "release_watch_run1.log")

SWEEP_TOP = 62000        # the top of the watcher's sweep; "FAR" means nothing at or below
Z_FULL = 65535           # the Z DAC's full range, docs/FACTS.md
TUNNEL_LO, TUNNEL_HI = 6, 13     # counts per decade of current, CALC, docs/FACTS.md
PERIOD = 3.0             # seconds between sweeps, release_and_watch.py PERIOD


def read_log(path):
    """(seconds since release, Z onset or None for FAR) from the watcher's own log."""
    out = []
    pat = re.compile(r"^\S+\s+([\d.]+)s\s+(FOUND onset Z (\d+)|FAR)\s*$")
    with open(path) as f:
        for line in f:
            m = pat.match(line.strip())
            if m:
                out.append((float(m.group(1)),
                            int(m.group(3)) if m.group(3) else None))
    return out


def far_spans(pts):
    """Intervals over which the printed state was FAR and never changed."""
    spans = []
    for i, (t, z) in enumerate(pts):
        if z is None:
            end = pts[i + 1][0] if i + 1 < len(pts) else t
            spans.append((t, end))
    return spans


def main():
    pts = read_log(LOG)
    found = [(t, z) for t, z in pts if z is not None]
    spans = far_spans(pts)
    print("%d printed events, %d contacts, %d FAR" %
          (len(pts), len(found), len(pts) - len(found)))
    for t, z in pts:
        print("   %7.1f s   %s" % (t, "%6d" % z if z is not None else "FAR (> %d)" % SWEEP_TOP))
    for a, b in spans:
        print("   out of reach %.1f s -> %.1f s  (%.0f s, about %d sweeps, none found)"
              % (a, b, b - a, round((b - a) / PERIOD)))

    S.set_theme("light")
    fig, (ax, axz) = S.plt.subplots(1, 2, figsize=(10.0, 5.6), width_ratios=[2.85, 1.15])
    fig.subplots_adjust(top=0.775, bottom=0.215, left=0.086, right=0.985, wspace=0.30)

    c = S.series(0)          # blue - a contact was found
    c_far = S.series(1)      # orange - nothing found anywhere in the sweep

    ax.axhspan(SWEEP_TOP, 70500, color=S.C["band"], zorder=0)
    S.note(ax, 14, 67600, "above this line the surface was out of reach",
           ha="left", va="center", fontsize=S.TYPE["small"])

    # --- out of reach: every sweep in these spans reported FAR ------------------------
    for k, (a, b) in enumerate(spans):
        ax.plot([a, b], [SWEEP_TOP, SWEEP_TOP], "-", color=c_far, lw=3.0, zorder=4,
                solid_capstyle="butt",
                label="nothing found anywhere in Z" if k == 0 else None)
        for t in (a, b):
            ax.annotate("", xy=(t, 68800), xytext=(t, SWEEP_TOP + 700),
                        arrowprops=dict(arrowstyle="-|>", color=c_far, lw=1.8,
                                        shrinkA=0, shrinkB=0), zorder=5)
    S.note(ax, (spans[0][0] + spans[0][1]) / 2.0, SWEEP_TOP - 2400,
           "out of reach for %.0f seconds — about %d sweeps, none of which found it"
           % (spans[0][1] - spans[0][0], round((spans[0][1] - spans[0][0]) / PERIOD)),
           ha="center", va="top", color=S.C["ink2"], fontsize=S.TYPE["small"])

    # --- the contacts, joined only inside a single unbroken burst ---------------------
    bursts, burst = [], []
    for t, z in pts:
        if z is None:
            if burst:
                bursts.append(burst)
            burst = []
        else:
            burst.append((t, z))
    if burst:
        bursts.append(burst)
    for b in bursts:
        if len(b) > 1:
            ax.plot([t for t, _ in b], [z for _, z in b], "-", color=c, lw=2.0, zorder=3)
    ax.plot([t for t, _ in found], [z for _, z in found], "o", color=c, ms=10,
            markeredgecolor=S.C["surface"], markeredgewidth=2.0, zorder=6,
            label="where the surface was found")

    S.tidy(ax, xlabel="Seconds after the tip was released, with the motor and hands still",
           ylabel="Where the surface was, in Z piezo counts", grid="both")
    S.thousands(ax, "y")
    ax.set_xlim(-6, 138)
    ax.set_ylim(0, 70500)
    ax.legend(loc="upper left", bbox_to_anchor=(0.20, 0.34), labelspacing=0.55,
              handletextpad=0.7, frameon=True, facecolor=S.C["surface"],
              edgecolor="none", framealpha=1.0)

    ax.annotate("", xy=(8.0, SWEEP_TOP), xytext=(8.0, 19000),
                arrowprops=dict(arrowstyle="<->", color=S.C["ink"], lw=1.7), zorder=7)
    S.note(ax, 12.0, 40500, "at least 43,000 counts\nin 6.4 seconds",
           ha="left", va="center", color=S.C["ink"], fontweight="bold", linespacing=1.6)
    ax.annotate("", xy=(105, 6000), xytext=(105, SWEEP_TOP),
                arrowprops=dict(arrowstyle="<->", color=S.C["ink"], lw=1.7), zorder=7)
    S.note(ax, 101, 30000, "and at least 56,000\nback again inside\ntwo minutes",
           ha="right", va="center", color=S.C["ink"], fontweight="bold", linespacing=1.6)

    # --- the zoom panel: the same axis, magnified -------------------------------------
    zoom_top = 60.0
    axz.axhspan(TUNNEL_LO, TUNNEL_HI, color=S.series(2), alpha=0.25, zorder=2)
    axz.axhline(TUNNEL_LO, color=S.series(2), lw=2.0, zorder=3)
    axz.axhline(TUNNEL_HI, color=S.series(2), lw=2.0, zorder=3)
    S.tidy(axz, ylabel="Z piezo counts", grid="y")
    axz.set_xlim(0, 1)
    axz.set_ylim(0, zoom_top)
    axz.set_xticks([])
    axz.spines["bottom"].set_visible(False)
    axz.annotate("", xy=(0.30, TUNNEL_HI + 0.4), xytext=(0.30, 19.8),
                 arrowprops=dict(arrowstyle="-|>", color=S.C["ink2"], lw=1.5), zorder=5)
    S.note(axz, 0.06, 20.5,
           "%d–%d counts.\nA real tunnelling current\nchanges ten-fold across\n"
           "this whole band."
           % (TUNNEL_LO, TUNNEL_HI),
           ha="left", va="bottom", color=S.C["ink"], linespacing=1.6)
    S.note(axz, 0.06, 40.0,
           "Calculated from a Z scale\nborrowed from another\nbuilder's scanner —\n"
           "never measured on ours.",
           ha="left", va="bottom", fontsize=S.TYPE["small"], linespacing=1.55)
    S.note(axz, 0.06, 56.5, "the same axis, magnified about %d times"
           % (round(Z_FULL / zoom_top / 100) * 100),
           ha="left", va="bottom", color=S.C["ink"], fontweight="bold",
           fontsize=S.TYPE["small"])

    S.titles(fig,
             "Nothing was moving, and the surface still crossed most of the instrument's range",
             "The motor was off and nobody was touching it. Only the Z piezo was sweeping, hunting for the surface "
             "every three seconds.\nThe surface it found kept moving — by thousands of times the distance a "
             "tunnelling gap is allowed to change. This is what stops imaging.")

    S.footer(fig, y=0.008, text=
             "Source: sessions/data/2026-09-19-morning/release_watch_run1.log, parsed line by line by this script. "
             "Measured 2026-09-19, 12:54:10–12:56:19 UTC; written up in\n"
             "sessions/2026-09-19-morning.md section 3.9. The orange out-of-reach bars are not printed points: the "
             "watcher logs only when the state changes (release_and_watch.py), and it swept every 3 s throughout.\n"
             "WHAT THIS DOES NOT SHOW: what is moving, or why — still UNKNOWN. Nine printed events are too "
             "sparse to say whether the motion is periodic. Every onset is a multiple of 1,000 counts because the "
             "sweep step was stuck at 1,000,\nso each is good to about ±1,000. The 6–13 count comparison "
             "is calculated from an inherited Z scale, not measured here. The blue dots are contact points, not an "
             "image — this project has never produced an image.")

    S.save(fig, "fig03_gap_motion")


if __name__ == "__main__":
    main()
