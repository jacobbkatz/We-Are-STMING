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
    ("2026-09-19", "Feedback scans and their X-held controls: no image.\n"
                   "The Z test: a pressed contact, not a tunnelling gap.\n"
                   "The gap measured crossing most of the Z range in seconds.",
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

    S.set_theme("light")
    fig = S.plt.figure(figsize=(13.4, 7.4))
    ax = fig.add_axes([0.035, 0.235, 0.950, 0.545])
    ax.axis("off")

    lo = dt.date(2026, 8, 28)
    hi = dt.date(2026, 9, 22)
    span = (hi - lo).days

    def x(d):
        return (d - lo).days / float(span)

    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.30, 1.10)

    # ---- the spine and its week marks -----------------------------------------------
    ybase = 0.06
    ax.plot([0, 1], [ybase, ybase], "-", color=S.C["axis"], lw=1.6, zorder=3)
    d = dt.date(2026, 8, 31)
    while d <= hi:
        ax.plot([x(d)], [ybase], "|", color=S.C["axis"], ms=9, mew=1.4, zorder=4)
        S.note(ax, x(d), ybase - 0.075, d.strftime("%d %b"), ha="center", va="top",
               fontsize=S.TYPE["small"])
        d += dt.timedelta(days=7)

    # ---- one tick per logged session -------------------------------------------------
    counts = {}
    for dd, _ in sess:
        counts[dd] = counts.get(dd, 0) + 1
    for dd, n in sorted(counts.items()):
        for k in range(n):
            ax.add_patch(Rectangle((x(dd) - 0.0022, ybase + 0.022 + k * 0.030),
                                   0.0044, 0.024,
                                   facecolor=S.C["muted"], edgecolor="none", zorder=4))
    S.note(ax, 0.0, ybase - 0.20,
           "Each small bar is one logged work session: %d of them across %d days, "
           "%s to %s.\nThe parts were being ordered well before that — the "
           "suspension springs are on an order dated 2026-06-21."
           % (len(sess), len(days), days[0].strftime("%d %b"),
              days[-1].strftime("%d %b %Y")),
           ha="left", va="top", fontsize=S.TYPE["small"])

    # ---- the milestones ---------------------------------------------------------------
    levels = [0.30, 0.50, 0.70, 0.93]
    for datestr, head, src, lvl in MILESTONES:
        dd = dt.date(*(int(g) for g in datestr.split("-")))
        xx = x(dd)
        yy = levels[lvl]
        big = head.startswith("THE WHOLE CHAIN") or head.startswith("A REAL TIP")
        col = S.series(0) if big else S.C["muted"]
        ax.plot([xx, xx], [ybase + 0.012, yy - 0.012], "-", color=S.C["grid"], lw=1.2,
                zorder=2)
        ax.plot([xx], [ybase], "o", color=col, ms=10 if big else 8,
                markeredgecolor=S.C["surface"], markeredgewidth=2.0, zorder=6)
        side = "left" if xx < 0.70 else "right"
        xt = xx + 0.011 if side == "left" else xx - 0.011
        S.note(ax, xt, yy, datestr, ha=side, va="bottom",
               fontsize=S.TYPE["small"], color=col, fontweight=S.W_EMPH)
        (S.key if big else S.note)(ax, xt, yy - 0.018, head, ha=side, va="top")
        nlines = head.count("\n") + 1
        S.note(ax, xt, yy - 0.020 - 0.043 * nlines, src, ha=side, va="top",
               fontsize=S.TYPE["small"], color=S.C["muted"])

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
