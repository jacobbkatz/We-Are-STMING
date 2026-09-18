"""Sample the gap fast (~30-50 Hz) by repeated short onset searches, never holding the tip in.

Each search starts BACK from the last onset by BACKOFF counts, climbs in STEP counts until the
averaged current reaches ONSET, records that Z, and immediately drops back. The tip only ever
meets the current threshold, then retreats ~BACKOFF counts. If the current is already over ONSET
at the start point, the start is recorded as an upper bound ("below") and the next search starts
further back. Nothing here moves the motor.

Used for: the spectrum of the gap wander (is it the 17th's 5-20 Hz?), and X/Y coupling at
good precision (many samples per setting, settings interleaved against drift).
"""
import sys
import time
import math
import cmath
import statistics as st

ONSET, ZCAP, STEP, BACKOFF = 1000, 50000, 800, 4000


def track(rig, seconds, z_seed=25000):
    out = []           # (t, z, flag) flag 0 = found, 1 = at/below start (upper bound), 2 = none
    last = z_seed
    t0 = time.perf_counter()
    while time.perf_counter() - t0 < seconds:
        start = max(0, last - BACKOFF)
        rig.z(start)
        v = [rig.read(), rig.read()]
        v = [x for x in v if x is not None]
        t = time.perf_counter() - t0
        if v and abs(st.median(v)) >= ONSET:
            out.append((t, start, 1))
            last = start - BACKOFF if start > 0 else 0
            rig.z(max(0, last - BACKOFF))
            continue
        z = start
        found = None
        while z <= ZCAP:
            z += STEP
            rig.z(z)
            v = [x for x in (rig.read(), rig.read()) if x is not None]
            if v and abs(st.median(v)) >= ONSET:
                found = z
                break
        rig.z(max(0, (found if found is not None else z) - BACKOFF))
        t = time.perf_counter() - t0
        if found is None:
            out.append((t, ZCAP, 2))
            last = ZCAP
        else:
            out.append((t, found, 0))
            last = found
    rig.z(0)
    return out


def spectrum(samples, freqs):
    """Direct DFT on uneven timestamps of the found samples (flags 0 and 1)."""
    pts = [(t, z) for t, z, f in samples if f in (0, 1)]
    if len(pts) < 20:
        return {}
    m = st.mean(z for _, z in pts)
    n = len(pts)
    res = {}
    for f in freqs:
        s = sum((z - m) * cmath.exp(-2j * math.pi * f * t) for t, z in pts)
        res[f] = 2 * abs(s) / n
    return res


def summary(samples):
    found = [z for _, z, f in samples if f == 0]
    below = sum(1 for s in samples if s[2] == 1)
    none = sum(1 for s in samples if s[2] == 2)
    dur = samples[-1][0] if samples else 0
    rate = len(samples) / dur if dur else 0
    if len(found) > 2:
        return ("n=%d (%.0f/s) found=%d below=%d none=%d | onset mean %.0f sd %.0f min %d max %d"
                % (len(samples), rate, len(found), below, none, st.mean(found), st.pstdev(found),
                   min(found), max(found)))
    return "n=%d found=%d below=%d none=%d" % (len(samples), len(found), below, none)
