"""Figure 9 - what was established, and when.

    python3 deliverables/2026-09-19-pause/figures/code/fig09_timeline.py

THE SESSION TICKS ARE READ OFF THE REPOSITORY, not typed in: every `sessions/*.md` whose
name starts with a date contributes one tick, so the row of ticks is exactly the set of
work sessions logged. Two logs on the same date are two sessions and both count
(`sessions/README.md`).

EACH MILESTONE NAMES ITS SOURCE in the list below. Nothing here is a new claim: every one
is already in `docs/FACTS.md`, `STATUS.md` or the session log for that day.

WHAT IS DELIBERATELY NOT ON IT. There is no milestone for "tunnelling achieved" or "first
image", because neither happened. The last marker is the instrument being packed up, and
that is the honest end of the line.
"""
from __future__ import annotations

import datetime as dt
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stmstyle as S  # noqa: E402

from matplotlib.patches import Rectangle  # noqa: E402

SESSIONS_DIR = os.path.join(S.REPO, "sessions")

# (date, headline, where it is recorded, level 0-3 for label stacking)
MILESTONES = [
    ("2026-08-31", "First work session logged in this repository",
     "sessions/2026-08-31-results.md", 0),
    ("2026-09-07", "The converter's full scale corrected to ±10.24 V —\n"
                   "every current in the project was wrong by 2.5× until this",
     "docs/FACTS.md, retired values", 1),
    ("2026-09-13", "The preamplifier's ground found unconnected\n"
                   "in the board as fabricated: no copper pour at all",
     "docs/FACTS.md, NETLIST + BENCH", 2),
    ("2026-09-15", "The amplifier's own input current measured for the\n"
                   "first time on a board whose 0 V is actually connected: 4 pA",
     "docs/FACTS.md, MEAS 2026-09-15", 3),
    ("2026-09-16", "THE WHOLE CHAIN CALIBRATED against Ohm's law\n"
                   "through a known 100 MΩ: 320.5 counts per nanoamp",
     "sessions/2026-09-16-bench.md 3.4 · figure 1", 0),
    ("2026-09-17", "A REAL TIP-AND-SAMPLE JUNCTION, and an I-V curve\n"
                   "with the shape a barrier requires",
     "sessions/2026-09-17-bench.md 3.15 · figure 2", 1),
    ("2026-09-19", "NO IMAGE, AND WE KNOW WHY: the scans match their own controls,\n"
                   "the Z test says pressed contact, and the gap crosses most of Z in seconds",
     "sessions/2026-09-19-bench.md, -morning.md · figures 3–5", 2),
    ("2026-09-19", "The instrument taken apart to be moved",
     "STATUS.md, Jacob about 14:19 UTC", 3),
]


def session_dates():
    """Every dated session log in sessions/, as (date, filename)."""
    out = []
    for p in sorted(glob.glob(os.path.join(SESSIONS_DIR, "*.md"))):
        m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", os.path.basename(p))
        if m:
            out.append((dt.date(*(int(g) for g in m.groups())), os.path.basename(p)))
    return out


def main():
    sess = session_dates()
    days = sorted({d for d, _ in sess})
    print("%d dated session logs on %d distinct days, %s to %s"
          % (len(sess), len(days), days[0], days[-1]))

    lo = dt.date(2026, 8, 28)
    hi = dt.date(2026, 9, 22)
    span = (hi - lo).days

    def x(d):
        return (d - lo).days / float(span)

    S.set_theme("light")
    fig = S.plt.figure(figsize=(12.6, 9.6))
    ax = fig.add_axes([0.030, 0.185, 0.955, 0.655])
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # ---- the milestones, one per row, read top to bottom -----------------------------
    # Each milestone is a block that reads downward from its dot: date and dot at the
    # top, then the headline, then the file it is recorded in.
    n = len(MILESTONES)
    xspine, xtext = 0.115, 0.140
    top = 0.975
    rowh = (top - 0.030) / n
    lh = 0.0315          # one line of body text, in axes units at this figure size
    for k, (datestr, head, src, _lvl) in enumerate(MILESTONES):
        y = top - rowh * k
        big = head.startswith("THE WHOLE CHAIN") or head.startswith("A REAL TIP")
        col = S.series(0) if big else S.C["muted"]
        if k < n - 1:
            ax.plot([xspine, xspine], [y - rowh, y - 0.014], "-",
                    color=S.C["grid"], lw=1.6, zorder=1)
        ax.plot([xspine], [y], "o", color=col, ms=14 if big else 11,
                markeredgecolor=S.C["surface"], markeredgewidth=2.5, zorder=5)
        S.note(ax, xspine - 0.020, y, datestr, ha="right", va="center",
               fontweight=S.W_EMPH, color=col)
        nlines = head.count("\n") + 1
        (S.key if big else S.note)(ax, xtext, y + lh * 0.42, head,
                                   ha="left", va="top")
        S.note(ax, xtext, y + lh * 0.42 - lh * nlines - 0.006, src, ha="left", va="top",
               fontsize=S.TYPE["small"], color=S.C["muted"])

    # ---- the true date axis, with one bar per logged session -------------------------
    axs = fig.add_axes([0.150, 0.112, 0.470, 0.024])
    axs.set_xlim(x(lo), x(hi))
    axs.set_ylim(0, 3.4)
    axs.axis("off")
    counts = {}
    for dd, _ in sess:
        counts[dd] = counts.get(dd, 0) + 1
    axs.plot([x(lo), x(hi)], [0, 0], "-", color=S.C["axis"], lw=1.4)
    for dd, cnt in sorted(counts.items()):
        for k in range(cnt):
            axs.add_patch(Rectangle((x(dd) - 0.004, 0.22 + k * 0.95), 0.008, 0.75,
                                    facecolor=S.C["muted"], edgecolor="none"))
    d = dt.date(2026, 8, 31)
    while d <= hi:
        axs.text(x(d), -0.45, d.strftime("%d %b"), ha="center", va="top",
                 fontsize=S.TYPE["small"], color=S.C["muted"])
        d += dt.timedelta(days=7)
    fig.text(0.665, 0.122,
             "Each bar is one logged work session: %d of them across %d days, %s to %s.\n"
             "Parts were being ordered well before that \u2014 the suspension springs are "
             "on an order dated 2026-06-21."
             % (len(sess), len(days), days[0].strftime("%d %b"),
                days[-1].strftime("%d %b %Y")),
             ha="left", va="center", fontsize=S.TYPE["small"], color=S.C["ink2"],
             linespacing=1.7)

    S.titles_keyed(
        fig,
        "Eleven weeks: what was established, and when",
        "Two people who do not write code designed, ordered, assembled and characterised a working scanning-probe "
        "measurement chain.\n<The calibration> and <the first junction> are the two results the rest of this set "
        "rests on; both came in the last four days of work.",
        [{"color": S.word(0), "fontweight": S.W_EMPH},
         {"color": S.word(0), "fontweight": S.W_EMPH}])

    S.footer(fig, y=0.010, text=
             "The session bars are read off the repository by this script — every file in sessions/ whose "
             "name begins with a date contributes one, so the row is exactly the set of logged sessions. Two logs "
             "on one date are two sessions.\nEach milestone names the file that records it; none of them is a new "
             "claim. The 2026-06-21 spring order is from docs/INVENTORY.md, an order record.\n"
             "WHAT IS DELIBERATELY ABSENT: there is no milestone for tunnelling achieved or for a first image, "
             "because neither happened. The last marker is the instrument being packed up, and that is the "
             "honest end of the line.")

    S.save(fig, "fig09_timeline")


if __name__ == "__main__":
    main()
