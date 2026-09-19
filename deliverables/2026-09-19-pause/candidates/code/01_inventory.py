"""01 - Inventory every recorded scan, control and line-repeat, with its shape.

Run from the repository root:

    python3 deliverables/2026-09-19-pause/candidates/code/01_inventory.py

Writes deliverables/2026-09-19-pause/candidates/work/inventory.csv and prints it.
Reads only sessions/data/. Nothing is modified.
"""
import csv
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from stmload import load_raster, load_ycontrol, data, out, line_rms

RASTER = [
    # (session, file, what it is, kind)
    ("2026-09-17-bench", "scan_slow_1.csv", "first image, pre-timeout-fix", "scan"),
    ("2026-09-17-bench", "scan_slow_2.csv", "second image, pre-timeout-fix", "scan"),
    ("2026-09-17-bench", "scan_fast_1.csv", "fast image 1 of 4, same patch", "scan"),
    ("2026-09-17-bench", "scan_fast_2.csv", "fast image 2 of 4", "scan"),
    ("2026-09-17-bench", "scan_fast_3.csv", "fast image 3 of 4", "scan"),
    ("2026-09-17-bench", "scan_fast_4.csv", "fast image 4 of 4", "scan"),
    ("2026-09-17-bench", "diag_scan_normal_1.csv", "15 loop corrections/pixel", "scan"),
    ("2026-09-17-bench", "diag_scan_normal_2.csv", "15 loop corrections/pixel", "scan"),
    ("2026-09-17-bench", "diag_scan_x_held.csv", "CONTROL: identical timing, X never moved", "xheld"),
    ("2026-09-17-bench", "scan_slow_dwell_1.csv", "250 corrections/pixel", "scan"),
    ("2026-09-17-bench", "scan_slow_dwell_2.csv", "250 corrections/pixel", "scan"),
    ("2026-09-17-bench", "scan_wide_25nm_1.csv", "wide image, +-15000 X (the 25 nm pair)", "scan"),
    ("2026-09-17-bench", "scan_wide_25nm_2.csv", "wide image, +-15000 X (the 25 nm pair)", "scan"),
    ("2026-09-17-bench", "scan_wide_slow_1.csv", "wide +-4000 X, slow loop", "scan"),
    ("2026-09-17-bench", "scan_wide_slow_2.csv", "wide +-4000 X, slow loop", "scan"),
    ("2026-09-19-bench", "cas9_scan0.csv", "feedback scan 0, +-1500", "scan"),
    ("2026-09-19-bench", "cas9_scan1.csv", "feedback scan 1, +-1500", "scan"),
    ("2026-09-19-bench", "cas9_scan2.csv", "feedback scan 2, +-1500", "scan"),
    ("2026-09-19-bench", "cas9_scan3.csv", "feedback scan 3, +-1500", "scan"),
    ("2026-09-19-bench", "cas9_xheld0.csv", "CONTROL 0, X held", "xheld"),
    ("2026-09-19-bench", "cas9_xheld1.csv", "CONTROL 1, X held", "xheld"),
    ("2026-09-19-bench", "cas9_xheld2.csv", "CONTROL 2, X held (aborted)", "xheld"),
    ("2026-09-19-bench", "cas9_xheld3.csv", "CONTROL 3, X held", "xheld"),
    ("2026-09-19-bench", "img_scan_0.csv", "wide image 0, +-15000 (aborted)", "scan"),
    ("2026-09-19-bench", "img_scan_1.csv", "wide image 1, +-15000 (aborted)", "scan"),
    ("2026-09-19-bench", "img_scan_2.csv", "wide image 2, +-15000", "scan"),
    ("2026-09-19-bench", "img_xheld_0.csv", "CONTROL, wide, X held", "xheld"),
    ("2026-09-19-bench", "img_xheld_1.csv", "CONTROL, wide, X held", "xheld"),
    ("2026-09-19-morning", "tuned_s3k_scan0.csv", "tuned loop scan 0 (aborted)", "scan"),
    ("2026-09-19-morning", "tuned_s3k_scan1.csv", "tuned loop scan 1 (aborted)", "scan"),
    ("2026-09-19-morning", "tuned_s3k_scan2.csv", "tuned loop scan 2 (aborted)", "scan"),
    ("2026-09-19-morning", "tuned_s3k_xheld0.csv", "CONTROL tuned 0 (aborted)", "xheld"),
    ("2026-09-19-morning", "tuned_s3k_xheld1.csv", "CONTROL tuned 1 (aborted)", "xheld"),
    ("2026-09-19-morning", "tuned_s3k_xheld2.csv", "CONTROL tuned 2 (aborted)", "xheld"),
]
RASTER += [("2026-09-19-bench", os.path.basename(p),
            "constant-height map at hard contact (saturated)",
            "chmap_xheld" if "xheld" in p else "chmap")
           for p in sorted(glob.glob(data("2026-09-19-bench", "cas8_chmap_*.csv")))]

YCTRL = [
    ("2026-09-17-bench", "line_repeated_wide.csv", "12 passes of one line, +-15000 X", "repeat"),
    ("2026-09-17-bench", "diag_line_repeated.csv", "10 passes of one line, narrow", "repeat"),
    ("2026-09-17-bench", "line_three_y_positions.csv", "three-Y control at +-8000 (wrong width)", "yctrl"),
    ("2026-09-19-bench", "ycontrol_run1.csv", "three-Y, y_sep 3000, +-15000 X", "yctrl"),
    ("2026-09-19-bench", "ycontrol_xheld_run1.csv", "three-Y CONTROL, X held, y_sep 3000", "yctrl_xheld"),
    ("2026-09-19-bench", "ycontrol_run2_ysep12000.csv", "three-Y, y_sep 12000 (the 3.9 sigma run)", "yctrl"),
    ("2026-09-19-bench", "ycontrol_run3_ysep12000_xheld.csv", "three-Y CONTROL, X held, y_sep 12000", "yctrl_xheld"),
    ("2026-09-19-bench", "ycontrol_run4_ysep12000_repeat.csv", "three-Y, y_sep 12000, REPEAT", "yctrl"),
]


def main():
    rows = []
    for sess, name, what, kind in RASTER:
        p = data(sess, name)
        if not os.path.exists(p):
            rows.append([sess, name, kind, what, "MISSING", "", "", "", "", ""])
            continue
        xs, ys, F, B = load_raster(p)
        rows.append([sess, name, kind, what, "raster", len(F), len(xs),
                     int(xs[0]), int(xs[-1]),
                     "" if not len(F) else "%.0f" % line_rms(F)])
    for sess, name, what, kind in YCTRL:
        p = data(sess, name)
        xs, places, P = load_ycontrol(p)
        rows.append([sess, name, kind, what, "ycontrol",
                     sum(len(v) for v in P.values()), len(xs),
                     int(xs[0]), int(xs[-1]),
                     "%.0f" % np.mean([line_rms(v) for v in P.values()])])

    hdr = ["session", "file", "kind", "what", "shape", "n_passes_or_lines",
           "n_pixels", "x_first", "x_last", "mean_detrended_rms_counts"]
    with open(out("work", "inventory.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(hdr)
        w.writerows(rows)
    print(",".join(hdr))
    for r in rows:
        print(",".join(str(v) for v in r))
    print("\n%d recordings inventoried -> %s" % (len(rows), out("work", "inventory.csv")))


if __name__ == "__main__":
    main()
