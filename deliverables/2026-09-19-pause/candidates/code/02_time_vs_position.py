"""02 - Does the structure in each scan track POSITION or TIME?

Run from the repository root:

    python3 deliverables/2026-09-19-pause/candidates/code/02_time_vs_position.py

Writes work/time_vs_position.csv and prints a table.

THE TEST
--------
Each raster line is scanned twice: forward (X ascending) then backward (X
descending). scan2.py stores the backward pass X-ascending, so array index i is
the same X in both rows while the backward row's TIME order is reversed.

  r_pos  = corr( detrend(fwd)[i], detrend(back)[i] )
           Same X, so a feature fixed to the SAMPLE lands on the same index in
           both passes and pushes this up.

  r_time = corr( detrend(fwd)[i], detrend(back)[n-1-i] )
           Reversing the stored backward row puts the two passes back onto one
           steadily increasing TIME axis. A drift, an oscillation or the loop's
           own dynamics is continuous across the join and pushes THIS up.

Both are computed on detrended passes (a least-squares straight line in X
removed from each pass separately). Detrending is required: there is a fixed
-0.1 to -0.2 counts-of-Z per count-of-X tilt between tip and sample which
otherwise dominates every correlation (Code/pc/stm_y_control.py says so, and
sessions/2026-09-17-bench.md section 3.22 measured the tilt).

The X-held controls get exactly the same treatment. In a control X never moves,
so there is NO sample structure in it by construction: whatever r_pos it shows
is the size of a false positive from this instrument on this night.
"""
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from stmload import load_raster, data, out, detrend, corr, fisher_mean, line_rms

# Same list as 01_inventory, kept flat here so this script stands alone.
FILES = [
    ("2026-09-17-bench", "scan_slow_1.csv", "scan", "narrow +-400"),
    ("2026-09-17-bench", "scan_slow_2.csv", "scan", "narrow +-400"),
    ("2026-09-17-bench", "scan_fast_1.csv", "scan", "narrow +-400"),
    ("2026-09-17-bench", "scan_fast_2.csv", "scan", "narrow +-400"),
    ("2026-09-17-bench", "scan_fast_3.csv", "scan", "narrow +-400"),
    ("2026-09-17-bench", "scan_fast_4.csv", "scan", "narrow +-400"),
    ("2026-09-17-bench", "diag_scan_normal_1.csv", "scan", "narrow +-400"),
    ("2026-09-17-bench", "diag_scan_normal_2.csv", "scan", "narrow +-400"),
    ("2026-09-17-bench", "diag_scan_x_held.csv", "XHELD", "narrow +-400"),
    ("2026-09-17-bench", "scan_slow_dwell_1.csv", "scan", "narrow +-400"),
    ("2026-09-17-bench", "scan_slow_dwell_2.csv", "scan", "narrow +-400"),
    ("2026-09-17-bench", "scan_wide_25nm_1.csv", "scan", "wide +-15000"),
    ("2026-09-17-bench", "scan_wide_25nm_2.csv", "scan", "wide +-15000"),
    ("2026-09-17-bench", "scan_wide_slow_1.csv", "scan", "mid +-4000"),
    ("2026-09-17-bench", "scan_wide_slow_2.csv", "scan", "mid +-4000"),
    ("2026-09-19-bench", "cas9_scan0.csv", "scan", "narrow +-1500"),
    ("2026-09-19-bench", "cas9_scan1.csv", "scan", "narrow +-1500"),
    ("2026-09-19-bench", "cas9_scan2.csv", "scan", "narrow +-1500"),
    ("2026-09-19-bench", "cas9_scan3.csv", "scan", "narrow +-1500"),
    ("2026-09-19-bench", "cas9_xheld0.csv", "XHELD", "narrow +-1500"),
    ("2026-09-19-bench", "cas9_xheld1.csv", "XHELD", "narrow +-1500"),
    ("2026-09-19-bench", "cas9_xheld2.csv", "XHELD", "narrow +-1500"),
    ("2026-09-19-bench", "cas9_xheld3.csv", "XHELD", "narrow +-1500"),
    ("2026-09-19-bench", "img_scan_0.csv", "scan", "wide +-15000"),
    ("2026-09-19-bench", "img_scan_1.csv", "scan", "wide +-15000"),
    ("2026-09-19-bench", "img_scan_2.csv", "scan", "wide +-15000"),
    ("2026-09-19-bench", "img_xheld_0.csv", "XHELD", "wide +-15000"),
    ("2026-09-19-bench", "img_xheld_1.csv", "XHELD", "wide +-15000"),
    ("2026-09-19-morning", "tuned_s3k_scan0.csv", "scan", "mid +-3000 tuned"),
    ("2026-09-19-morning", "tuned_s3k_scan1.csv", "scan", "mid +-3000 tuned"),
    ("2026-09-19-morning", "tuned_s3k_scan2.csv", "scan", "mid +-3000 tuned"),
    ("2026-09-19-morning", "tuned_s3k_xheld0.csv", "XHELD", "mid +-3000 tuned"),
    ("2026-09-19-morning", "tuned_s3k_xheld1.csv", "XHELD", "mid +-3000 tuned"),
    ("2026-09-19-morning", "tuned_s3k_xheld2.csv", "XHELD", "mid +-3000 tuned"),
]


def analyse(path):
    xs, ys, F, B = load_raster(path)
    rp, rt = [], []
    for f, b in zip(F, B):
        fd, bd = detrend(f), detrend(b)
        rp.append(corr(fd, bd))
        rt.append(corr(fd, bd[::-1]))
    mp, sp, np_ = fisher_mean(rp)
    mt, st, nt = fisher_mean(rt)
    return dict(nlines=len(F), npix=len(xs), rms=line_rms(F) if len(F) else float("nan"),
                r_pos=mp, se_pos=sp, n_pos=np_, r_time=mt, se_time=st, n_time=nt,
                rp=rp, rt=rt)


def main():
    rows = []
    print("%-38s %-6s %-16s %4s %7s   %-16s %-16s" % (
        "file", "kind", "width", "line", "rms", "r_pos (position)", "r_time (time)"))
    print("-" * 118)
    for sess, name, kind, width in FILES:
        r = analyse(data(sess, name))
        fmt = lambda m, s: ("  --  " if m is None else
                            "%+.3f +- %.3f" % (m, s if s == s else 0.0))
        print("%-38s %-6s %-16s %4d %7.0f   %-16s %-16s" % (
            name, kind, width, r["nlines"], r["rms"], fmt(r["r_pos"], r["se_pos"]),
            fmt(r["r_time"], r["se_time"])))
        rows.append([sess, name, kind, width, r["nlines"], r["npix"], "%.0f" % r["rms"],
                     "" if r["r_pos"] is None else "%.4f" % r["r_pos"],
                     "" if r["se_pos"] is None else "%.4f" % r["se_pos"],
                     "" if r["r_time"] is None else "%.4f" % r["r_time"],
                     "" if r["se_time"] is None else "%.4f" % r["se_time"]])

    # Group summaries: pool every line of every file in the group.
    print()
    groups = {}
    for sess, name, kind, width in FILES:
        r = analyse(data(sess, name))
        key = (width, kind)
        groups.setdefault(key, {"rp": [], "rt": [], "files": 0})
        groups[key]["rp"] += r["rp"]
        groups[key]["rt"] += r["rt"]
        groups[key]["files"] += 1
    print("POOLED OVER EVERY LINE IN THE GROUP")
    print("%-18s %-6s %5s %6s   %-18s %-18s" % ("width", "kind", "files", "lines",
                                                "r_pos", "r_time"))
    print("-" * 82)
    for (width, kind) in sorted(groups):
        g = groups[(width, kind)]
        mp, sp, n1 = fisher_mean(g["rp"])
        mt, st, n2 = fisher_mean(g["rt"])
        print("%-18s %-6s %5d %6d   %+.3f +- %.3f (%2d) %+.3f +- %.3f (%2d)" % (
            width, kind, g["files"], len(g["rp"]), mp or 0, sp or 0, n1, mt or 0, st or 0, n2))
        rows.append(["POOLED", width, kind, "", g["files"], len(g["rp"]), "",
                     "%.4f" % (mp or 0), "%.4f" % (sp or 0),
                     "%.4f" % (mt or 0), "%.4f" % (st or 0)])

    with open(out("work", "time_vs_position.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["session", "file", "kind", "width", "nlines", "npix", "rms_counts",
                    "r_pos", "se_pos", "r_time", "se_time"])
        w.writerows(rows)
    print("\n-> %s" % out("work", "time_vs_position.csv"))


if __name__ == "__main__":
    main()
