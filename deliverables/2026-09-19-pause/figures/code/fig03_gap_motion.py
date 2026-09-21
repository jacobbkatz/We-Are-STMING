"""Figure 3 - the blocker, found and measured.

    python3 deliverables/2026-09-19-pause/figures/code/fig03_gap_motion.py

SOURCE. `sessions/data/2026-09-19-morning/release_watch_run1.log`, read verbatim by this
script - the nine printed events are the whole measurement. Measured 2026-09-19, 12:54:10
to 12:56:19 UTC, written up in `sessions/2026-09-19-morning.md` section 3.9.

WHAT WAS AND WAS NOT MOVING. The motor was still and nobody was touching the instrument.
The only thing being driven was the Z piezo, sweeping its range every 3 s looking for the
surface. Each point is the Z code at which current first appeared on that sweep - that is,
where the surface was at that moment.

THE FLAT "OUT OF REACH" BARS ARE NOT INVENTED. The watcher printed a line only when the
state changed, or on every contact:
`sessions/data/2026-09-19-morning/scripts/release_and_watch.py`,
`if state != last or state == "found"`, sweeping every PERIOD = 3 s throughout. So between
a printed FAR and the next printed contact, every intervening sweep also reported FAR -
that is what "the state did not change" means. The bars are drawn from that, and the
caption says so.

THE HONEST CAVEAT, which a knowledgeable viewer will raise. The first excursion starts
0.1 s after a 60-step motor retract finished, so post-move relaxation cannot be excluded
for that one event. It does not carry the result: the motion reverses and overshoots its
own starting point, which relaxation does not do, and the 56,000-count figure spans 6.4 s
to 111 s. It is on the figure, not buried here.

RESOLUTION. Every onset is a multiple of 1,000: `fastwood.sweep` bound its step size as a
default argument, so the 250-count step the script asked for never took effect
(`sessions/data/2026-09-19-morning/README.md`). The motion is far larger than the step, so
the conclusion does not depend on it, but no onset here is better than +/-1,000 counts.

THE COMPARISON SCALE is `docs/FACTS.md`, "Tunneling for comparison: a decade per ~6-13 Z
counts" - CALCULATED from a Z scale inherited from Dan Berard's scanner, never measured on
ours. It is drawn as a calculated band and labeled as one. No distance scale appears on
this figure, because this instrument has never established one from its own hardware.
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
    return [(t, pts[i + 1][0] if i + 1 < len(pts) else t)
            for i, (t, z) in enumerate(pts) if z is None]


def bursts_of(pts):
    """Runs of consecutive contacts, so a line is never drawn across a FAR gap."""
    out, cur = [], []
    for t, z in pts:
        if z is None:
            if cur:
                out.append(cur)
            cur = []
        else:
            cur.append((t, z))
    if cur:
        out.append(cur)
    return out


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
    fig, (ax, axz) = S.plt.subplots(1, 2, figsize=(10.6, 8.4), width_ratios=[2.75, 1.15])
    fig.subplots_adjust(top=0.775, bottom=0.255, left=0.086, right=0.985, wspace=0.28)

    c = S.series(0)          # blue   - a contact was found
    c_far = S.series(1)      # orange - nothing found anywhere in the sweep

    ax.axhspan(SWEEP_TOP, 70500, color=S.C["band"], zorder=0)
    S.note(ax, 16, 67300, "above this line the surface was out of reach",
           ha="left", va="center", fontsize=S.TYPE["small"])

    for a, b in spans:
        ax.plot([a, b], [SWEEP_TOP, SWEEP_TOP], "-", color=c_far, lw=3.2, zorder=4,
                solid_capstyle="butt")
        ax.annotate("", xy=(a, 65700), xytext=(a, SWEEP_TOP + 700),
                    arrowprops=dict(arrowstyle="-|>", color=c_far, lw=1.8,
                                    shrinkA=0, shrinkB=0), zorder=5)
    # WRAPPED ONTO TWO LINES, 2026-09-21. On one line this ran from t = 16 s to
    # t = 138 s at a height of 54,000-59,000 counts, and the double-headed arrow at
    # t = 105 s spans 6,000-62,000 - so the arrow went straight through the words
    # "none of which found it". check_layout.py did not see it: it compares text
    # against text, and an arrow is not text.
    S.note(ax, 16, SWEEP_TOP - 3100,
           "%.0f seconds out of reach —\nabout %d sweeps, none of which found it"
           % (spans[0][1] - spans[0][0], round((spans[0][1] - spans[0][0]) / PERIOD)),
           ha="left", va="top", fontsize=S.TYPE["small"])

    for b in bursts_of(pts):
        if len(b) > 1:
            ax.plot([t for t, _ in b], [z for _, z in b], "-", color=c, lw=2.2, zorder=3)
    ax.plot([t for t, _ in found], [z for _, z in found], "o", color=c, ms=10,
            markeredgecolor=S.C["surface"], markeredgewidth=2.0, zorder=6)

    S.tidy(ax, xlabel="Seconds after the tip was released, with the motor and hands still",
           ylabel="Where the surface was, in Z piezo counts", grid="both")
    S.thousands(ax, "y")
    ax.set_xlim(-6, 138)
    ax.set_ylim(0, 70500)

    ax.annotate("", xy=(8.5, SWEEP_TOP), xytext=(8.5, 19000),
                arrowprops=dict(arrowstyle="<->", color=S.C["ink"], lw=1.7), zorder=7)
    S.key(ax, 13.0, 40500, "at least 43,000 counts\nin 6.4 seconds",
          ha="left", va="center")
    ax.annotate("", xy=(105, 6000), xytext=(105, SWEEP_TOP),
                arrowprops=dict(arrowstyle="<->", color=S.C["ink"], lw=1.7), zorder=7)
    S.key(ax, 101, 28000, "and at least 56,000\nback again inside\ntwo minutes",
          ha="right", va="center")

    # --- the zoom panel: the same axis, magnified -------------------------------------
    zoom_top = 60.0
    axz.axhspan(TUNNEL_LO, TUNNEL_HI, color=S.series(2), alpha=0.28, zorder=2)
    axz.axhline(TUNNEL_LO, color=S.series(2), lw=2.0, zorder=3)
    axz.axhline(TUNNEL_HI, color=S.series(2), lw=2.0, zorder=3)
    S.tidy(axz, ylabel="Z piezo counts", grid="y")
    axz.set_xlim(0, 1)
    axz.set_ylim(0, zoom_top)
    axz.set_xticks([])
    axz.spines["bottom"].set_visible(False)
    axz.set_title("The same axis,\nmagnified about %d times"
                  % (round(Z_FULL / zoom_top / 100) * 100))
    axz.annotate("", xy=(0.32, TUNNEL_HI + 0.5), xytext=(0.32, 19.6),
                 arrowprops=dict(arrowstyle="-|>", color=S.C["ink2"], lw=1.5), zorder=5)
    S.key(axz, 0.06, 39.0,
          "%d–13 counts. A real tunneling\ncurrent changes ten-fold\nacross this whole band."
          % TUNNEL_LO, ha="left", va="bottom", linespacing=1.45)
    S.note(axz, 0.06, 21.0,
           "Calculated from a Z scale borrowed\nfrom another builder's scanner —\n"
           "never measured on ours.",
           ha="left", va="bottom", fontsize=S.TYPE["small"], linespacing=1.45)

    S.titles_keyed(
        fig,
        "We found what is stopping us, and measured it",
        "With the motor off and nobody touching the instrument, <the surface the tip was hunting for> moved by "
        "most of the piezo's\nwhole range within seconds — and <went out of reach altogether> for nearly two "
        "minutes. Knowing this, precisely, is the result.",
        [{"color": S.word(0), "fontweight": S.W_EMPH},
         {"color": S.word(1), "fontweight": S.W_EMPH}])

    S.footer(fig, y=0.008, text=
             "Source: sessions/data/2026-09-19-morning/release_watch_run1.log, parsed line by line by this "
             "script. Measured 2026-09-19, 12:54:10\u201312:56:19 UTC; sessions/2026-09-19-morning.md section 3.9.\n"
             "The orange out-of-reach bars are not printed points: the watcher logs only when the state changes "
             "(release_and_watch.py) and swept every 3 s throughout.\n"
             "THE FAIR QUESTION: the first excursion begins 0.1 s after a 60-step motor retract ended, so "
             "relaxation after that move cannot be excluded for that one event \u2014 but the surface reverses\n"
             "direction and overshoots its own starting point, which relaxation does not do, and the "
             "56,000-count figure spans 6.4 s to 111 s.\n"
             "WHAT THIS DOES NOT SHOW: what is moving, or why \u2014 still UNKNOWN; nine events are too sparse "
             "to say whether it is periodic. Onsets are multiples of 1,000 counts because the sweep step was\n"
             "stuck there. The 6\u201313 band is calculated from an inherited Z scale, and no distance scale "
             "appears here because this instrument has never established one from its own hardware. The blue\n"
             "dots are contact points, not an image \u2014 this project has never produced an image.")

    S.save(fig, "fig03_gap_motion")


if __name__ == "__main__":
    main()
