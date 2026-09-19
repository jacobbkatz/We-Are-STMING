"""The coarse approach: motor step size, backlash, stick-slip, and what a step actually does.

    python3 deliverables/2026-09-19-pause/analysis/code/approach_and_motor.py

Everything here is about the 28BYJ-48 stepper driving the fine screw, watched through the
only sensor there is: the Z code at which the current first appears. That code is a proxy
for where the gold is, so a motor step is judged by how far the onset moves.

Sources, and they are NOT one experiment:
  sessions/data/2026-09-18-bench/zcal3_run1.csv   one motor step at a time, onset after each
  sessions/data/2026-09-18-bench/track_run1.csv   90 s of onsets with the motor STILL
  sessions/data/2026-09-18-bench/lash_run1.log    fast-tracker medians after single steps
  sessions/data/2026-09-19-morning/fastwood_*.csv 650 and 200 single/chunked steps
  sessions/data/2026-09-19-morning/stairs_*.csv   two full finds, nothing anywhere
  sessions/data/2026-09-19-bench/*.log            approach runs, back-offs, live back-offs

The central question the records answer: CAN THE MOTOR PARK THE TIP AT A MODERATE CURRENT?
The control that makes the answer meaningful is track_run1: the same onset measurement with
the motor NOT moving. If the motor's scatter is no larger than the still scatter, the motor
is not what is moving the gold.

Outputs: plots/fig16_motor_steps.png, fig17_still_vs_stepping.png
"""
import math
import os
import re
import statistics as st
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (DATA, data_path, read_rows, fnum, style, save, section,
                    TOL, SERIES, REPO)


def main():
    plt = style()

    section("1. THE CONTROL: ONSET SCATTER WITH THE MOTOR STILL (track_run1.csv)")
    _, rows = read_rows(data_path("2026-09-18-bench", "track_run1.csv"))
    ts = [fnum(r["t"]) for r in rows]
    on = [fnum(r["onset_z"]) for r in rows]
    adj = set(r["motor_adj"] for r in rows)
    found = [v for v in on if v is not None]
    print("  %d searches over %.1f s; motor_adj values present: %s"
          % (len(rows), max(ts), sorted(adj)))
    print("  found an onset in %d of %d searches (%.0f%% found nothing)"
          % (len(found), len(rows), 100 * (1 - len(found) / len(rows))))
    print("  onset mean %.0f, sd %.0f, median %.0f, range %.0f to %.0f Z counts"
          % (st.mean(found), st.stdev(found), st.median(found), min(found), max(found)))
    print("  session log 3.7 says: mean 24,067, sd 7,548, range 7,250-44,250,")
    print("  27 of 276 searches finding nothing.")
    print()
    print("  MEASURED, and this is the number everything else is compared against:")
    print("  WITH THE MOTOR STILL the apparent position of the gold moves over a range of")
    print("  %.0f Z counts within 90 seconds, sd %.0f." % (max(found) - min(found),
                                                           st.stdev(found)))
    still_sd = st.stdev(found)

    section("2. ONE MOTOR STEP AT A TIME (zcal3_run1.csv, 2026-09-18)")
    _, rows = read_rows(data_path("2026-09-18-bench", "zcal3_run1.csv"))
    # tag is 'p<pass>_s<step>'; the onset of each step is the LOWEST Z of that tag's scan
    by_tag = {}
    for r in rows:
        by_tag.setdefault(r["tag"], []).append((int(r["z"]), fnum(r["mean"])))
    seq = {}
    for tag, pts in by_tag.items():
        m = re.match(r"p(\d+)_s(\d+)", tag)
        if not m:
            continue
        seq.setdefault(int(m.group(1)), {})[int(m.group(2))] = min(z for z, _ in pts)
    print("  The file holds only the slope scan taken AT each onset, so the onset is read")
    print("  as the lowest Z in that scan. The session log's own table is the fuller")
    print("  record; this is a check on it.")
    steps_all = []
    for p in sorted(seq):
        ss = sorted(seq[p])
        print("  pass %d: %s" % (p, "  ".join("step %d -> Z %d" % (s, seq[p][s]) for s in ss)))
        for a, b in zip(ss, ss[1:]):
            if b - a == 1:
                steps_all.append(abs(seq[p][b] - seq[p][a]))
    if steps_all:
        print("  single-step onset changes seen in this file: %s"
              % ", ".join("%d" % d for d in steps_all))
        print("  median %.0f, max %.0f Z counts per motor step"
              % (st.median(steps_all), max(steps_all)))
    print("  Session log 3.7: 'where a single step changed things, it moved the onset")
    print("  14,000-29,000 counts'; in between the onset wandered by thousands with no")
    print("  systematic direction.")
    print()
    print("  AGAINST THE CONTROL: the still scatter is sd %.0f counts (section 1). A step"
          % still_sd)
    print("  that moves the onset by 14,000-29,000 is %0.1f to %0.1f times that, so THOSE"
          % (14000 / still_sd, 29000 / still_sd))
    print("  steps did something. The smaller between-step wander is inside the still")
    print("  scatter and IS NOT EVIDENCE that the motor moved anything.")

    section("3. FAST-TRACKER MEDIANS AFTER SINGLE STEPS (lash_run1.log, 2026-09-18)")
    med, pos, lab = [], [], []
    for line in open(data_path("2026-09-18-bench", "lash_run1.log")):
        m = re.search(r"(start|c(\d+) (in|out)\s+pos (-?\d+)): median ([\d.]+)", line)
        if m:
            med.append(float(m.group(5)))
            pos.append(0 if m.group(1) == "start" else int(m.group(4)))
            lab.append("start" if m.group(1) == "start" else "%s%s" % (m.group(3), m.group(2)))
    print("  %d medians recorded; motor positions %d to %d"
          % (len(med), min(pos), max(pos)))
    print("  median of the medians %.0f, sd %.0f, range %.0f to %.0f"
          % (st.median(med), st.stdev(med), min(med), max(med)))
    first20 = [m for m, p in zip(med, pos) if -20 <= p <= 0]
    print("  first 20 approach steps: median %.0f, sd %.0f, range %.0f to %.0f"
          % (st.median(first20), st.stdev(first20), min(first20), max(first20)))
    print("  Session log 3.8: '20 approach steps with the median unmoved at 15,000-17,000'.")
    inband = [m for m in first20 if 14000 <= m <= 18000]
    print("  Re-derived, precisely: %d of the %d points sit in 14,400-18,000; the"
          % (len(inband), len(first20)))
    print("  exceptions are %s. The claim holds for the body of the run but not for"
          % ", ".join("%.0f" % m for m in first20 if m not in inband))
    print("  every point, so read it as 'the median did not walk', not 'no point moved'.")
    print()
    print("  CAVEAT THE DATA README ATTACHES TO THIS FILE: the fast tracker records where")
    print("  the current first passed 1,000 counts on a fast climb, and the same 'onsets'")
    print("  appeared with the bias at 0 V. So these locate SNAP-IN events, not a")
    print("  tunnelling onset, and every statistic from them is provisional.")

    section("4. THE 2026-09-19 MORNING APPROACHES")
    for name, what in (("fastwood_1789819103.csv", "650 single steps, 1,000-count sweep"),
                       ("fastwood_1789820034.csv", "20-step chunks"),
                       ("apz_approach_1789822231.csv", "20-step chunks, then the Z test"),
                       ("stairs_1789818942.csv", "two full finds"),
                       ("release_watch_1789823258.csv", "+1,200 retract steps in chunks")):
        p = data_path("2026-09-19-morning", name)
        fields, rows = read_rows(p)
        hits = [r for r in rows
                if any(fnum(r.get(k)) is not None for k in ("z_hit", "onset_z"))]
        print("  %-32s %-38s %4d rows, %d with a hit"
              % (name, what, len(rows), len(hits)))
        for r in hits:
            z = fnum(r.get("z_hit")) if "z_hit" in fields else fnum(r.get("onset_z"))
            steps = r.get("steps") or r.get("chunks") or r.get("motor_steps") or "?"
            print("      t %-9s after %-6s steps/chunks -> Z %s, reading %s"
                  % (r.get("t", "?"), steps, int(z), r.get("adc", "-")))
    print()
    print("  MEASURED: 650 single steps toward the sample found nothing at all")
    print("  (fastwood_1789819103.csv has %d rows and no hit)."
          % len(read_rows(data_path("2026-09-19-morning", "fastwood_1789819103.csv"))[1]))
    print("  MEASURED: 20-step chunks found the gold twice, at 200 and 180 steps.")
    print("  NOT ESTABLISHED: that chunks work better than single steps. Eleven hand")
    print("  nudges happened between the two attempts (2026-09-19-morning.md 3.6), so the")
    print("  comparison is confounded. The session log says this itself.")

    section("5. BACKLASH AND STICK-SLIP: WHAT A RETRACT DOES TO A HARD CONTACT")
    print("  Every recorded attempt to release a hard contact with the motor:")
    events = [
        ("2026-09-18 bench 3.4", "MTMV +500 with Z at 0", "cleared it",
         "sessions/2026-09-18-bench.md"),
        ("2026-09-18 bench 3.6", "MTMV +25", "cleared it", "sessions/2026-09-18-bench.md"),
        ("2026-09-19 bench 3.7", "+83 single retract steps", "NOT cleared",
         "sessions/2026-09-19-bench.md"),
        ("2026-09-19 bench 3.7", "+200 more with Z at midscale", "cleared it",
         "sessions/2026-09-19-bench.md"),
        ("2026-09-19 bench 3.11", "+2,927 net retract steps", "NOT cleared; the hand did",
         "sessions/2026-09-19-bench.md"),
        ("2026-09-19 bench 3.13", "1 step at a time after a 5-step approach",
         "pinned for 23 steps, clear at 24 - nothing in between",
         "sessions/2026-09-19-bench.md"),
        ("2026-09-19 morning 3.3", "+80 then +300 single retract steps", "NOT cleared",
         "sessions/2026-09-19-morning.md"),
        ("2026-09-19 morning 3.12", "+1,200 in 20-step chunks", "NOT cleared",
         "sessions/2026-09-19-morning.md"),
    ]
    for where, what, result, src in events:
        print("    %-26s %-42s %s" % (where, what, result))
    cleared = sum(1 for e in events if e[2].startswith("cleared"))
    print("  %d of %d motor retract attempts cleared a hard contact." % (cleared, len(events)))
    print("  n = %d INDEPENDENT episodes across three sessions and two tips." % len(events))
    print()
    print("  THE SINGLE MOST USEFUL NUMBER FOR THE REBUILD: on 2026-09-19 bench 3.13 the")
    print("  contact stayed pinned for 23 single retract steps and was clear on the 24th,")
    print("  with NO moderate current at any step in between. In the other direction a")
    print("  5-step approach cycle went from out of reach to metal contact. So one motor")
    print("  step spans the whole useful range, and THE MOTOR CANNOT PARK THE TIP AT A")
    print("  MODERATE CURRENT. That is a mechanical statement about the coarse stage, and")
    print("  it does not depend on the unmeasured Z scale.")

    section("6. WHAT ONE MOTOR STEP IS, IN LENGTH - and why the number is not settled")
    print("  docs/FACTS.md carries: 1/4-80 thread = 0.31750 mm per turn; 2,048 steps per")
    print("  motor revolution; lever ratio 20, 30 or 40 UNRESOLVED, giving 3.88, 5.17 or")
    print("  7.75 nm per step. All three are DERIVED from CAD geometry, not measured.")
    print("  0.31750 mm / 2048 = %.4f um of screw per step, before any lever ratio."
          % (0.31750 / 2048 * 1000))
    print("  The 2026-09-17 session measured '250 Z counts per motor step' from a")
    print("  staircase; 2026-09-18 3.7 then found that staircase ran inside that night's")
    print("  own 100-250 steps of measured slack, so the figure is SUSPECT. Nothing since")
    print("  has replaced it. Treat the nm-per-step figure as unmeasured.")

    # ------------------------------------------------------------ figures
    section("7. FIGURES")
    # Plot CHRONOLOGICALLY, not by motor position: the run walked in and then back out
    # several times, so joining points by position would draw a zigzag that is an artefact
    # of the ordering rather than anything the instrument did.
    fig, ax = plt.subplots(figsize=(7.6, 3.8))
    idx = list(range(len(med)))
    ax.plot(idx, med, lw=0.7, color=TOL["grey"], zorder=1)
    seen = set()
    for i_, (m, l) in enumerate(zip(med, lab)):
        col = TOL["blue"] if l.startswith("in") else (
            TOL["red"] if l.startswith("out") else TOL["black"])
        name = ("approaching" if l.startswith("in") else
                "retracting" if l.startswith("out") else "start")
        ax.scatter([i_], [m], s=13, color=col, zorder=3,
                   label=name if name not in seen else None)
        seen.add(name)
    ax.axhspan(14400, 18000, color=TOL["green"], alpha=0.25, zorder=0)
    ax.text(2, 19000, "21 consecutive single approach steps with the median unmoved\n"
            "(20 of 21 inside this band)", fontsize=7.5, color=TOL["green"])
    ax.set_xlabel("reading number, in the order taken (one per single motor step)")
    ax.set_ylabel("fast-tracker median onset (Z counts)")
    ax.set_title("A single motor step does nothing, until one does everything\n"
                 "2026-09-18 bench, lash_run1.log - these locate SNAP-IN events, "
                 "not a tunnelling onset")
    ax.legend(loc="upper right", ncol=3)
    save(fig, "fig16_motor_steps.png")
    plt.close(fig)

    _, rows = read_rows(data_path("2026-09-18-bench", "track_run1.csv"))
    ts = [fnum(r["t"]) for r in rows]
    on = [fnum(r["onset_z"]) for r in rows]
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    ok = [(t, z) for t, z in zip(ts, on) if z is not None]
    miss = [t for t, z in zip(ts, on) if z is None]
    ax.plot([t for t, _ in ok], [z for _, z in ok], marker=".", ms=4, lw=0.6,
            color=TOL["blue"], label="onset found (n = %d)" % len(ok))
    ax.scatter(miss, [0] * len(miss), marker="x", s=18, color=TOL["red"],
               label="nothing found anywhere (n = %d)" % len(miss))
    m = st.mean([z for _, z in ok])
    s = st.stdev([z for _, z in ok])
    ax.axhline(m, color=TOL["black"], lw=1.0)
    ax.axhspan(m - s, m + s, color=TOL["grey"], alpha=0.3,
               label="mean $\\pm$ 1 sd = %.0f $\\pm$ %.0f counts" % (m, s))
    ax.set_xlabel("time (s)")
    ax.set_ylabel("Z code at which the current appeared")
    ax.set_title("The control everything else is measured against\n"
                 "90 s of repeated searches with the MOTOR STILL, 2026-09-18 bench")
    ax.legend(loc="upper right")
    save(fig, "fig17_still_vs_stepping.png")
    plt.close(fig)


if __name__ == "__main__":
    main()
