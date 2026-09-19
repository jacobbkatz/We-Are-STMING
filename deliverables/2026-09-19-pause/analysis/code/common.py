"""Shared helpers for the 2026-09-19 pause-point data analysis.

Every script in this directory imports this. Nothing here writes to sessions/data/,
which is read-only. All paths are derived from the repository root, which is found by
walking up from this file, so no absolute path outside the repository is ever used.

Run any script in this directory from the repository root, e.g.

    python3 deliverables/2026-09-19-pause/analysis/code/calibration.py
"""
from __future__ import annotations

import csv
import math
import os
import re
import statistics as st

# ---------------------------------------------------------------- paths

HERE = os.path.dirname(os.path.abspath(__file__))
ANALYSIS = os.path.dirname(HERE)                     # .../analysis
REPO = os.path.abspath(os.path.join(ANALYSIS, "..", "..", ".."))
DATA = os.path.join(REPO, "sessions", "data")
PLOTS = os.path.join(ANALYSIS, "plots")
SESSIONS = ["2026-09-17-bench", "2026-09-18-bench", "2026-09-19-bench", "2026-09-19-morning"]


def data_path(session: str, name: str) -> str:
    return os.path.join(DATA, session, name)


def ensure_plots() -> str:
    os.makedirs(PLOTS, exist_ok=True)
    return PLOTS


# ---------------------------------------------------------------- instrument constants
#
# These are CITED from docs/FACTS.md, not redefined here. docs/FACTS.md is the only
# register of constants in this repository (CLAUDE.md section 3bb); the values below are
# used inside the arithmetic of this analysis and each names its source.

COUNTS_PER_NA = 320.5          # docs/FACTS.md "Counts per nA", MEAS 2026-09-16
BIAS_MIDSCALE = 32768          # docs/FACTS.md, AD5761 bias DAC midscale
BIAS_VOLT_FULL = 3.0           # docs/FACTS.md "X, Y, bias range" = +-3 V
BIAS_PATH_GAIN = -1.0          # docs/FACTS.md "Bias path gain", MEAS 2026-08-31


def bias_code_to_sample_volts(code: int) -> float:
    """Sample-holder voltage for a BIAS DAC code.

    Derived from docs/FACTS.md: the bias DAC spans +-3 V over 0..65535 with midscale at
    32768, and the bias path gain is -1. Check: code 38229 -> -0.4927 V, which the
    session logs call "sample -0.5 V"; code 0 -> +3.000 V, which the 2026-09-16 dummy
    junction test measured as +3.000 V on the bias wire.
    """
    return BIAS_PATH_GAIN * (code - BIAS_MIDSCALE) / 32768.0 * BIAS_VOLT_FULL


# ---------------------------------------------------------------- readers

def read_rows(path):
    """Every row of a CSV as a dict. Returns (fieldnames, rows)."""
    with open(path, newline="") as f:
        r = csv.DictReader(f)
        return list(r.fieldnames or []), list(r)


def fnum(v):
    """float(v) or None for blank / 'None' / unparseable."""
    if v is None:
        return None
    v = v.strip()
    if v in ("", "None", "nan", "NaN"):
        return None
    try:
        return float(v)
    except ValueError:
        return None


def read_scan(path):
    """A feedback-scan or y-control CSV.

    Layout (sessions/data/2026-09-17-bench/README.md): first header cell is the row
    label ('y' or 'y_offset'), second is the pass label ('dir' or 'pass'), the rest are
    X DAC codes. Each data row is one pass over one line; the cells are the Z DAC code
    the loop needed to hold the setpoint.

    Returns (x_codes, [(row_label, pass_label, [z or None, ...]), ...]).
    Short rows are padded with None, which is how an aborted scan appears.
    """
    fields, rows = read_rows(path)
    xs = [int(c) for c in fields[2:]]
    out = []
    for r in rows:
        vals = []
        for c in fields[2:]:
            vals.append(fnum(r.get(c)))
        out.append((fnum(r[fields[0]]), r[fields[1]], vals))
    return xs, out


def read_ztest(path):
    """A Z-test CSV: columns t, cycle, phase, z, adc (sessions/data/2026-09-19-morning/README.md)."""
    _, rows = read_rows(path)
    out = []
    for r in rows:
        out.append((fnum(r["t"]), int(r["cycle"]), r["phase"], int(r["z"]), fnum(r["adc"])))
    return out


# ---------------------------------------------------------------- statistics

def pearson(a, b):
    """Pearson r over the positions where both are finite. None if fewer than 3."""
    p = [(x, y) for x, y in zip(a, b) if x is not None and y is not None]
    if len(p) < 3:
        return None
    xs = [x for x, _ in p]
    ys = [y for _, y in p]
    mx, my = st.mean(xs), st.mean(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    if sxx <= 0 or syy <= 0:
        return None
    return sum((x - mx) * (y - my) for x, y in p) / math.sqrt(sxx * syy)


def ols(xs, ys):
    """Ordinary least squares y = a + b x.

    Returns dict with slope, intercept, their standard errors, r2, n and the residual
    standard deviation. Standard errors are the textbook OLS ones and assume the
    residuals are independent, which for a burst of readings taken 1.4 s apart is an
    assumption, not a fact.
    """
    n = len(xs)
    mx, my = st.mean(xs), st.mean(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    b = sxy / sxx
    a = my - b * mx
    resid = [y - (a + b * x) for x, y in zip(xs, ys)]
    sse = sum(r * r for r in resid)
    sst = sum((y - my) ** 2 for y in ys)
    dof = n - 2
    s2 = sse / dof
    return dict(slope=b, intercept=a,
                se_slope=math.sqrt(s2 / sxx),
                se_intercept=math.sqrt(s2 * (1.0 / n + mx * mx / sxx)),
                r2=1.0 - sse / sst, n=n, resid_sd=math.sqrt(s2), resid=resid)


def detrend(vals):
    """Remove a straight line in index from a list, keeping None in place."""
    idx = [i for i, v in enumerate(vals) if v is not None]
    if len(idx) < 3:
        return list(vals)
    f = ols([float(i) for i in idx], [vals[i] for i in idx])
    return [None if v is None else v - (f["intercept"] + f["slope"] * i)
            for i, v in enumerate(vals)]


# ---------------------------------------------------------------- plotting style
#
# Colourblind-safe: Paul Tol's bright qualitative set, which is distinguishable under
# deuteranopia, protanopia and tritanopia and stays legible in greyscale order.

TOL = dict(blue="#4477AA", cyan="#66CCEE", green="#228833", yellow="#CCBB44",
           red="#EE6677", purple="#AA3377", grey="#BBBBBB", black="#000000")
SERIES = [TOL["blue"], TOL["red"], TOL["green"], TOL["purple"], TOL["cyan"], TOL["yellow"]]


def style():
    """Apply the shared figure style. Call before making any figure."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({
        "figure.dpi": 160,
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.labelsize": 9,
        "axes.grid": True,
        "grid.alpha": 0.25,
        "grid.linewidth": 0.6,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "legend.frameon": False,
        "legend.fontsize": 8,
        "lines.linewidth": 1.4,
    })
    return plt


def save(fig, name):
    p = os.path.join(ensure_plots(), name)
    fig.savefig(p)
    print("  wrote %s" % os.path.relpath(p, REPO))
    return p


def section(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)
