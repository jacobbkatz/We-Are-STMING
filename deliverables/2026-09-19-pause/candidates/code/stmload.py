"""Shared loaders and statistics for the candidate-image search.

Read-only with respect to sessions/data/. Nothing here writes into the raw data.

Two file shapes are handled:

  RASTER    y,dir,<x0>,<x1>,...        rows alternate dir=fwd / dir=back
            Written by scan2.py / stm_feedback_scan.py. The value in each cell
            is the Z DAC code the constant-current loop needed at that pixel.
            IMPORTANT: the `back` row is stored X-ASCENDING (scan2.py reverses
            it before writing), so array index i is the same X in both rows but
            the TIME order of `back` is reversed.

  YCONTROL  y_offset,pass,<x0>,<x1>,... one row per (place, pass)
            Written by Code/pc/stm_y_control.py and by the 2026-09-17
            line_three_y_positions.csv / line_repeated_wide.csv diagnostics.

Detrending: every pass has a straight line (least squares in X) subtracted
before any correlation or RMS. This is the project's existing convention
(Code/pc/stm_y_control.py detrend()) and it exists because there is a fixed
-0.1 to -0.2 counts-of-Z per count-of-X tilt between tip and sample which
otherwise dominates every correlation.
"""
import csv
import math
import os

import numpy as np


# ---------------------------------------------------------------- loaders

def load_raster(path):
    """Return (xs, ys, F, B) for a y,dir,... file.

    xs : np.array of X DAC codes (the column headers)
    ys : list of Y DAC codes, in the order the raster took them
    F  : (nlines, npix) forward passes, X-ascending, time-ascending
    B  : (nlines, npix) backward passes, X-ascending, time-DESCENDING
         (B[:, ::-1] is the backward pass in time order)
    """
    with open(path) as fh:
        rows = list(csv.reader(fh))
    xs = np.array([int(v) for v in rows[0][2:]])
    fwd, back, order = {}, {}, []
    for r in rows[1:]:
        if not r:
            continue
        y = int(r[0])
        vals = np.array([float(v) for v in r[2:]])
        if r[1] == "fwd":
            fwd[y] = vals
            order.append(y)
        else:
            back[y] = vals
    ys = [y for y in order if y in fwd]
    F = np.array([fwd[y] for y in ys])
    B = np.array([back[y] for y in ys if y in back]) if back else np.zeros((0, len(xs)))
    if len(B) != len(F):           # an aborted run can lack the last back pass
        n = min(len(B), len(F))
        F, B, ys = F[:n], B[:n], ys[:n]
    return xs, ys, F, B


def load_ycontrol(path):
    """Return (xs, places, P) for a y_offset,pass,... file.

    places : sorted list of the distinct y_offset values
    P      : dict place -> (npasses, npix) array, passes in the order recorded
    """
    with open(path) as fh:
        rows = list(csv.reader(fh))
    xs = np.array([int(v) for v in rows[0][2:]])
    P = {}
    for r in rows[1:]:
        if not r:
            continue
        place = int(r[0])
        P.setdefault(place, []).append([float(v) for v in r[2:]])
    places = sorted(P)
    return xs, places, {k: np.array(v) for k, v in P.items()}


# ------------------------------------------------------------- statistics

def detrend(a):
    """Subtract the least-squares straight line in index. Returns a new array."""
    a = np.asarray(a, dtype=float)
    n = len(a)
    if n < 3:
        return a - a.mean()
    t = np.arange(n, dtype=float)
    m, c = np.polyfit(t, a, 1)
    return a - (m * t + c)


def corr(a, b):
    """Pearson r, or None when either side is constant."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if len(a) != len(b) or len(a) < 3:
        return None
    sa, sb = a.std(), b.std()
    if sa == 0 or sb == 0:
        return None
    return float(((a - a.mean()) * (b - b.mean())).mean() / (sa * sb))


def rms(a):
    a = np.asarray(a, dtype=float)
    return float(np.sqrt((a ** 2).mean()))


def fisher_mean(rs):
    """Mean of correlations through Fisher z, with the standard error of the mean.

    Returns (r_mean, se_in_r_units, n). Correlations at exactly +-1 are clipped.
    """
    rs = [r for r in rs if r is not None and abs(r) < 0.999999]
    if not rs:
        return None, None, 0
    z = np.arctanh(np.array(rs))
    zm = z.mean()
    if len(z) > 1:
        se_z = z.std(ddof=1) / math.sqrt(len(z))
    else:
        se_z = float("nan")
    return float(np.tanh(zm)), float(se_z * (1 - np.tanh(zm) ** 2)), len(rs)


# ------------------------------------------- the time-versus-position test

def trace_retrace_pair(F, B):
    """The discriminator that separates a position-locked from a time-locked signal.

    Each pass is detrended first.

      r_pos  = corr(fwd[i],        back[i])          same X, different time
      r_time = corr(fwd[i],  back[npix-1-i])         different X, but this puts
                                                     the two passes back into a
                                                     single ascending TIME axis

    Reasoning. The forward pass visits x_0..x_(n-1) at times 0..n-1. The
    backward pass visits x_(n-1)..x_0 at times n..2n-1 and is then stored
    X-ascending, so back[i] was taken at time 2n-1-i. Therefore back[n-1-i] was
    taken at time n+i: reversing the stored backward row recovers a signal
    sampled at steadily increasing time. A feature fixed to the SAMPLE appears
    at the same X in both passes and lifts r_pos. A feature that is a function
    of TIME (drift, an oscillation, the loop's own dynamics) is continuous
    across the join and lifts r_time instead.

    Returns (r_pos list, r_time list), one entry per line.
    """
    rp, rt = [], []
    for f, b in zip(F, B):
        fd, bd = detrend(f), detrend(b)
        rp.append(corr(fd, bd))
        rt.append(corr(fd, bd[::-1]))
    return rp, rt


def line_rms(F):
    """Mean RMS of the detrended forward passes: the project's 'corrugation'."""
    return float(np.mean([rms(detrend(f)) for f in F])) if len(F) else float("nan")


# ---------------------------------------------------------------- helpers

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))


def data(*parts):
    return os.path.join(REPO, "sessions", "data", *parts)


def out(*parts):
    p = os.path.join(REPO, "deliverables", "2026-09-19-pause", "candidates", *parts)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    return p
