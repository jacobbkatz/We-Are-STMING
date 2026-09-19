"""The Z test: does Z control a TUNNELLING current, is it reversible, and how fast does the gold drift?

2026-09-19 morning. For the tip fitted ~03:00 UTC 2026-09-19, HIGH Z extends toward the sample
(sessions/2026-09-19-bench.md 3.14), so walking Z UP approaches.

Why. On 2026-09-19 at the touch that settled the direction, retracting Z by 2000 counts still left
~26,000 counts (82 nA). If Z moves the tip ~0.016 nm/count (docs/INVENTORY.md, itself suspect) that
is ~30 nm, and a tunnelling current falls a decade per ~1-2 Angstrom, i.e. per ~7-15 counts. So
either the junction is a sticky/soft contact, or Z moves the tip far less than assumed.

What it does, repeated for CYCLES cycles at a fixed X, Y (midscale), sample -0.5 V:
  IN : Z up DZ at a time, NREAD averaged ADCR per point, until the current reaches TARGET.
  OUT: Z down DZ at a time for SPAN counts; if the current is still over CLEAR there, keep going
       down (OUT2) until it is. That captures how far the gold follows the tip back.
Every point goes to CSV. The next cycle starts from where OUT ended, so drift between cycles is
tracked, not assumed away: the Z of each onset IS the gold's position.

Safety: any averaged reading >= HARD -> Z down JUMP at once (never below Z_MIN), marked 'snap'.
A missing reading never advances Z. First find: Z walks up in FIND_STEP steps from the start Z to
Z_MAX; if nothing, returns 'lost' with Z back at the start Z.

What it measures, per cycle:
  counts per decade  - fit of log10|I| against Z for |I| in [FIT_LO, FIT_HI], IN and OUT separately
  hysteresis         - Z where IN first passed MID_I, minus Z where OUT last fell below MID_I.
                       ~0 for a clean junction; hundreds+ if the gold sticks and follows the tip
  onset              - Z of the IN crossing of TARGET, against time: the drift in counts per second

Expected (state it before the run):
  tunnelling, inherited 0.016 nm/count : ~7-15 counts per decade, hysteresis ~0
  the 2026-09-17 junction              : ~250 counts per decade (stm_feedback_scan.py)
  a 2026-09-18 snap-in                 : 1,000 -> 10,000 within 25-75 counts
  sticky / soft contact                : hysteresis of hundreds to thousands of counts, snaps

Usage:  py ztest.py [start_z] [cycles]          (hardware)
        py ztest.py --test                      (simulated worlds, including red checks)
        py ztest.py --analyse ztest_XXXX.csv
"""
import sys, time, math, random, statistics as st

BIAS_NEG = 38229                    # sample -0.5 V
TARGET, HARD, CLEAR = 1000, 8000, 150
FIT_LO, FIT_HI, MID_I = 100, 1000, 300
DZ, SPAN, JUMP = 4, 600, 3000
FIND_STEP = 16
NREAD = 5
Z_MIN, Z_MAX = 0, 62000
OUT2_STEP = 50


class Aborted(Exception):
    pass


def run(set_z, read1, now, out, z_start=32768, cycles=30, rows=None):
    """Returns (status, z_end). status in {'done', 'lost', 'error'}."""
    rows = rows if rows is not None else []
    state = {"z": z_start, "cycle": 0}

    def point(z, phase):
        z = int(max(Z_MIN, min(Z_MAX, z)))
        set_z(z)
        state["z"] = z
        v = [x for x in (read1() for _ in range(NREAD)) if x is not None]
        tries = 0
        while not v and tries < 3:
            v = [x for x in (read1() for _ in range(NREAD)) if x is not None]
            tries += 1
        m = st.mean(v) if v else None
        rows.append((round(now(), 4), state["cycle"], phase, z, None if m is None else round(m, 1)))
        return m

    def watchdog(m):
        """True if it fired. Z goes down JUMP, then on down until the current is gone."""
        if m is None or abs(m) < HARD:
            return False
        out("  SNAP: %.0f counts at Z %d -> Z down %d" % (m, state["z"], JUMP))
        z = state["z"] - JUMP
        m = point(z, "snap")
        while (m is None or abs(m) >= CLEAR) and state["z"] > Z_MIN:
            m = point(state["z"] - 1000, "snap")
        return True

    # Start: if already in contact, back out first.
    m = point(z_start, "start")
    if m is None:
        return "error", state["z"]
    if abs(m) >= TARGET:
        out("in contact at the start (%.0f counts): backing out" % m)
        if not watchdog(m):
            while abs(m) >= CLEAR and state["z"] > Z_MIN:
                m = point(state["z"] - 200, "pre")
                if m is None:
                    return "error", state["z"]
        m = point(state["z"], "pre")
        if m is None or abs(m) >= CLEAR:
            out("STUCK: still %s counts with Z fully retracted (%d). Back the MOTOR off."
                % (m, state["z"]))
            return "stuck", state["z"]

    # First find, coarse.
    found = False
    z = state["z"]
    while z < Z_MAX:
        z += FIND_STEP
        m = point(z, "find")
        if m is None:
            point(state["z"] - JUMP, "err")
            return "error", state["z"]
        if watchdog(m):
            found = True
            break
        if abs(m) >= TARGET:
            found = True
            break
    if not found:
        point(z_start, "lost")
        out("LOST: nothing up to Z %d; Z back to %d" % (Z_MAX, z_start))
        return "lost", state["z"]
    # Back off SPAN below the find so the first IN curve is complete.
    point(state["z"] - SPAN, "pre")

    for c in range(1, cycles + 1):
        state["cycle"] = c
        # IN
        m = point(state["z"], "in")
        guard = 0
        while m is not None and abs(m) >= TARGET and guard < 20:     # the gold came in meanwhile
            m = point(state["z"] - SPAN, "pre"); guard += 1
        while True:
            if state["z"] + DZ > Z_MAX:
                point(z_start, "lost")
                out("LOST during cycle %d: reached Z %d" % (c, Z_MAX))
                return "lost", state["z"]
            m = point(state["z"] + DZ, "in")
            if m is None:
                point(state["z"] - JUMP, "err")
                return "error", state["z"]
            if watchdog(m):
                break
            if abs(m) >= TARGET:
                break
        # OUT
        z_top = state["z"]
        while state["z"] > max(Z_MIN, z_top - SPAN):
            m = point(state["z"] - DZ, "out")
            if m is None:
                point(state["z"] - JUMP, "err")
                return "error", state["z"]
            watchdog(m)
        while m is not None and abs(m) >= CLEAR and state["z"] > Z_MIN:
            m = point(state["z"] - OUT2_STEP, "out2")
        if c % 5 == 0:
            out("cycle %d done, Z %d" % (c, state["z"]))
    return "done", state["z"]


# ---------------------------------------------------------------- analysis

def fit_cpd(pts):
    """Counts per decade from (z, I) with FIT_LO <= |I| <= FIT_HI. None if < 3 points."""
    p = [(z, math.log10(abs(i))) for z, i in pts if i is not None and FIT_LO <= abs(i) <= FIT_HI]
    if len(p) < 3:
        return None, len(p)
    zs, ls = [a for a, _ in p], [b for _, b in p]
    zm, lm = st.mean(zs), st.mean(ls)
    sxx = sum((z - zm) ** 2 for z in zs)
    if sxx == 0:
        return None, len(p)
    slope = sum((z - zm) * (l - lm) for z, l in zip(zs, ls)) / sxx
    if slope == 0:
        return None, len(p)
    return 1.0 / abs(slope), len(p)


def analyse(rows, out=print):
    cyc = {}
    for t, c, ph, z, m in rows:
        if c >= 1:
            cyc.setdefault(c, []).append((t, ph, z, m))
    res = []
    for c, pts in sorted(cyc.items()):
        pin = [(z, m) for t, ph, z, m in pts if ph == "in"]
        pout = [(z, m) for t, ph, z, m in pts if ph in ("out", "out2")]
        snaps = sum(1 for t, ph, z, m in pts if ph == "snap")
        cin, nin = fit_cpd(pin)
        cout, nout = fit_cpd(pout)
        # IN: first Z where |I| >= MID_I.  OUT: last Z (walking down) where |I| >= MID_I.
        zin = next((z for z, m in pin if m is not None and abs(m) >= MID_I), None)
        zout = None
        for z, m in pout:
            if m is not None and abs(m) >= MID_I:
                zout = z
        onset = next(((t, z) for t, ph, z, m in pts if ph == "in" and m is not None and abs(m) >= TARGET), None)
        res.append(dict(cycle=c, cpd_in=cin, n_in=nin, cpd_out=cout, n_out=nout,
                        hyst=None if zin is None or zout is None else zin - zout,
                        onset=onset, snaps=snaps))
    ok_in = [r["cpd_in"] for r in res if r["cpd_in"]]
    ok_out = [r["cpd_out"] for r in res if r["cpd_out"]]
    hy = [r["hyst"] for r in res if r["hyst"] is not None]
    on = [r["onset"] for r in res if r["onset"]]
    drift = None
    if len(on) >= 3:
        ts, zs = [a for a, _ in on], [b for _, b in on]
        tm, zm = st.mean(ts), st.mean(zs)
        sxx = sum((t - tm) ** 2 for t in ts)
        drift = sum((t - tm) * (z - zm) for t, z in zip(ts, zs)) / sxx if sxx else None
    summary = dict(
        cycles=len(res),
        cpd_in_median=st.median(ok_in) if ok_in else None, cpd_in_n=len(ok_in),
        cpd_out_median=st.median(ok_out) if ok_out else None, cpd_out_n=len(ok_out),
        hyst_median=st.median(hy) if hy else None, hyst_n=len(hy),
        drift_counts_per_s=drift,
        onset_first=on[0][1] if on else None, onset_last=on[-1][1] if on else None,
        snaps=sum(r["snaps"] for r in res))
    for r in res:
        out("cycle %2d  in %s (%d pts)  out %s (%d pts)  hyst %s  onset %s  snaps %d" % (
            r["cycle"], "%6.1f" % r["cpd_in"] if r["cpd_in"] else "   -  ", r["n_in"],
            "%6.1f" % r["cpd_out"] if r["cpd_out"] else "   -  ", r["n_out"],
            "%6d" % r["hyst"] if r["hyst"] is not None else "   -  ",
            "%d" % r["onset"][1] if r["onset"] else "-", r["snaps"]))
    out("SUMMARY: " + ", ".join("%s=%s" % (k, ("%.2f" % v) if isinstance(v, float) else v)
                                  for k, v in summary.items()))
    return summary


# ---------------------------------------------------------------- simulated worlds

class World:
    """Gold at Z = gold(t); the current is TARGET at z == gold_eff and changes a decade per cpd.
    hyst: STICKY gold. Once the current has reached TARGET the leaf sticks to the tip and follows
    it back (gap held, current held near TARGET) until the tip is `hyst` counts behind the gold's
    rest position; then it lets go and springs back. (A first version shifted the gold by `hyst`
    the instant Z reversed, which put a 1500x current jump at every turnaround - unphysical.)
    snap: the current is 0 below gold_eff and railed at or above it."""
    def __init__(self, gold=40000, cpd=250.0, hyst=0, drift=0.0, noise=16.0, snap=False, seed=1,
                 slip=None):
        self.t, self.z = 0.0, 32768
        self.gold0, self.cpd, self.hyst, self.drift = gold, cpd, hyst, drift
        self.noise, self.snap = noise, snap
        self.slip = slip            # (t, counts): at time t the gold jumps `counts` TOWARD the tip
        self.rng = random.Random(seed)
        self.stuck = False
        self.max_depth = -1e9
    def now(self): return self.t
    def set_z(self, z):
        assert 0 <= z <= 65535
        self.z = z
    def read1(self):
        self.t += 0.002
        g_rest = self.gold0 + self.drift * self.t
        if self.slip and self.t >= self.slip[0]:
            g_rest -= self.slip[1]
        g = g_rest
        if self.stuck:
            if self.z < g_rest - self.hyst:
                self.stuck = False                  # lets go
            else:
                g = min(g_rest, self.z)             # follows the tip back: gap held at zero
        d = self.z - g
        self.max_depth = max(self.max_depth, self.z - g_rest)
        if self.snap:
            i = 32767.0 if d >= 0 else 0.0
        else:
            i = 0.0 if d < -4 * self.cpd else min(32767.0, TARGET * 10 ** (d / self.cpd))
        if self.hyst and i >= TARGET:
            self.stuck = True
        return int(i + self.rng.gauss(0, self.noise * math.sqrt(NREAD)))


def _sim(w, cycles=12):
    rows = []
    status, z = run(w.set_z, w.read1, w.now, lambda s: None, cycles=cycles, rows=rows)
    return status, z, rows, analyse(rows, out=lambda s: None)


def self_test():
    # 1. The 2026-09-17 junction: 250 counts per decade, no hysteresis, no drift.
    st_, z, rows, s = _sim(World(cpd=250))
    assert st_ == "done", st_
    assert abs(s["cpd_in_median"] - 250) < 50 and abs(s["cpd_out_median"] - 250) < 50, s
    assert abs(s["hyst_median"]) < 40, s
    # 2. Steep, as tunnelling on the inherited scale would be.
    st_, z, rows, s = _sim(World(cpd=10))
    assert st_ == "done" and s["cpd_in_median"] is not None and s["cpd_in_median"] < 30, s
    # 3. Sticky: the gold follows the tip back 800 counts. The IN curve passes MID_I about
    #    250*log10(1000/300) = 131 counts before the gold's rest position, so expect ~670.
    st_, z, rows, s = _sim(World(cpd=250, hyst=800))
    assert 550 < s["hyst_median"] < 800, s
    # 4. Drift: the gold moves +5 counts/s; the onsets must see it.
    st_, z, rows, s = _sim(World(cpd=250, drift=5.0), cycles=20)
    assert s["drift_counts_per_s"] is not None and abs(s["drift_counts_per_s"] - 5.0) < 1.5, s
    # 5. Out of reach: lost, and Z back at the start.
    w = World(gold=70000)
    st_, z, rows, s = _sim(w)
    assert st_ == "lost" and w.z == 32768, (st_, w.z)
    # 6. A hard snap: the watchdog must keep the tip from being driven on into the gold.
    w = World(snap=True)
    st_, z, rows, s = _sim(w, cycles=5)
    assert s["snaps"] >= 1, s
    assert w.max_depth <= FIND_STEP, "drove %.0f counts into a snapped contact" % w.max_depth
    assert w.z < w.gold0, "must end out of contact"
    # 7. Already in contact at the start: backs out, then measures.
    st_, z, rows, s = _sim(World(gold=30000, cpd=250))
    assert st_ == "done" and abs(s["cpd_in_median"] - 250) < 50, (st_, s)
    # 8. The gold SLIPS 3000 counts toward the tip mid-run (as on 2026-09-19): the tip must
    #    escape within a couple of readings, not sit in a railed contact while OUT creeps back.
    assert _longest_hard_run(World(cpd=250, slip=(15.0, 3000))) <= 3
    # 9. In contact even at full retraction: must stop and say so, not run cycles in contact.
    w = World(gold=-5000, cpd=250)
    st_, z, rows, s = _sim(w)
    assert st_ == "stuck" and s["cycles"] == 0, (st_, s)
    print("self-test: pass (250 and 10 counts/decade, sticky 800, drift 5/s, lost, snap, "
          "start in contact, slip, stuck at full retraction)")


def _longest_hard_run(w, cycles=12):
    rows = []
    run(w.set_z, w.read1, w.now, lambda s: None, cycles=cycles, rows=rows)
    best = cur = 0
    for t, c, ph, z, m in rows:
        cur = cur + 1 if (m is not None and abs(m) >= 8000) else 0
        best = max(best, cur)
    return best


def red_checks():
    """Break the safety on purpose; the test that guards it must go red."""
    global HARD
    keep = HARD
    HARD = 10 ** 9                      # watchdog disabled
    try:
        n = _longest_hard_run(World(cpd=250, slip=(15.0, 3000)))
    finally:
        HARD = keep
    assert n > 3, "red check failed: the slip test passed with the watchdog disabled (%d)" % n
    print("red check: pass (watchdog disabled -> %d railed readings in a row after the slip)" % n)


if __name__ == "__main__":
    # Added 2026-09-19 after a --test run of a script WITHOUT a self-test went straight to its
    # hardware path (no port was connected, so nothing was sent). Unknown options now refuse.
    _bad = [a for a in sys.argv[1:] if a.startswith('-') and a not in ['--test', '--analyse']]
    if _bad:
        sys.exit('refusing unknown option(s) %s: this script drives the instrument%s'
                 % (_bad, '' if True else ' and has NO self-test'))
    if "--test" in sys.argv:
        self_test(); red_checks(); sys.exit(0)
    if "--analyse" in sys.argv:
        import csv
        f = sys.argv[sys.argv.index("--analyse") + 1]
        rows = []
        for r in csv.DictReader(open(f)):
            rows.append((float(r["t"]), int(r["cycle"]), r["phase"], int(r["z"]),
                         None if r["adc"] in ("", "None") else float(r["adc"])))
        analyse(rows); sys.exit(0)
    import serial, csv
    sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
    from stm_approach import Device, find_teensy
    from stm_feedback_scan import read_averaged
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    z_start = int(args[0]) if args else 32768
    cycles = int(args[1]) if len(args) > 1 else 30
    stamp = lambda: time.strftime("%H:%M:%S", time.gmtime())
    out = lambda s: print(stamp(), s, flush=True)
    port = serial.Serial(find_teensy(), 115200, timeout=0.2)
    dev = Device(port)
    rows = []
    fname = "ztest_%d.csv" % int(time.time())
    t0 = time.time()
    try:
        dev._write(b"DACX 32768\n"); time.sleep(0.02)
        dev._write(b"DACY 32768\n"); time.sleep(0.02)
        dev.set_bias(BIAS_NEG); time.sleep(0.2)

        def set_z(z):
            dev._write(("DACZ %d\n" % z).encode())
            time.sleep(0.002)
        status, z = run(set_z, lambda: read_averaged(dev), lambda: time.time() - t0, out,
                        z_start=z_start, cycles=cycles, rows=rows)
        out("END: %s, Z %d, %d points -> %s" % (status, z, len(rows), fname))
    finally:
        port.close()
        with open(fname, "w", newline="") as f:
            w = csv.writer(f); w.writerow(["t", "cycle", "phase", "z", "adc"]); w.writerows(rows)
    analyse(rows, out=out)
