"""Motor staircase: single RETRACT steps, re-finding the gold with the piezo after each.

2026-09-19 morning, after the Z-0 live back-off left the gold at the very bottom of the Z range.
Two jobs at once:
  1. walk the gold up to mid-range (onset >= STOP_ONSET) so the Z test has room both ways;
  2. measure Z counts per motor step with NO reversal in the way. (2026-09-17's 250 counts/step was
     measured inside the reversal slack, and is suspect since sessions/2026-09-18-bench.md.) The
     motor's last moves this morning were retracts (backoff_motor runs 1 and 2, +380).

For the tip fitted ~03:00 UTC 2026-09-19: HIGH Z extends toward the sample, POSITIVE MTMV retracts.

Each step: Z -> 0, MTMV +1, then walk Z up from max(0, last onset - LOOKBACK) in FIND_STEP steps
until the averaged current >= TARGET; that Z is the onset. Z back to 0 at once. Watchdog: >= HARD
-> Z 0. Stops at STOP_ONSET, at MAX_STEPS, or if the onset FALLS by more than FALL counts over the
last 10 steps (the motor is not doing what it should) - Z left at 0.
Every onset is repeated REPEAT times at each motor position, so creep between reads is visible.

Usage: py stairs.py [max_steps] [stop_onset]        py stairs.py --test
"""
import sys, time, statistics as st

TARGET, HARD = 1000, 8000
FIND_STEP, LOOKBACK = 16, 1500
Z_TOP = 62000
NREAD, REPEAT = 5, 2
FALL_SLOPE = 50         # counts per step, downward trend over the last 10 positions
AT_ZERO = 40            # consecutive positions in contact at Z 0 (2026-09-19: pinned 23, clear 24th)


def find_onset(set_z, read_mean, z_from):
    """Walk up from z_from. Returns (onset, reading) or (None, None). Z is left AT the onset."""
    z = max(0, z_from)
    while z <= Z_TOP:
        set_z(z)
        m = read_mean()
        if m is not None and abs(m) >= TARGET:
            return z, m
        z += FIND_STEP
    return None, None


def run(set_z, read_mean, motor1, now, out, max_steps=200, stop_onset=20000, rows=None):
    rows = rows if rows is not None else []
    set_z(0)
    m0 = read_mean()
    if m0 is not None and abs(m0) >= TARGET:
        out("contact at Z 0 before any step (%.0f): stepping out first" % m0)
    last = 0
    steps = 0
    per_step = []
    at_zero = 0
    while True:
        onsets = []
        for r in range(REPEAT):
            on, m = find_onset(set_z, read_mean, last - LOOKBACK)
            set_z(0)
            if on is not None and m is not None and abs(m) >= HARD:
                out("  step %d: HARD reading %.0f at Z %d -> Z 0" % (steps, m, on))
            rows.append((round(now(), 3), steps, r, on, None if m is None else round(m)))
            onsets.append(on)
        good = [o for o in onsets if o is not None]
        if good:
            last = min(good)
            per_step.append((steps, last))
        out("step %3d: onsets %s" % (steps, onsets))
        if good and last >= stop_onset:
            return "mid-range", steps, last
        if not good:
            return "lost", steps, last
        # Guard 1: the onset TRENDING DOWN over the last 10 positions means each step brings the
        # gold closer - the motor is going the wrong way. (First version compared two single
        # points against a 3000-count drop and let a wrong-sign run drive 200 steps: caught by the
        # simulated test before hardware.)
        if len(per_step) >= 10:
            xs = [a for a, _ in per_step[-10:]]
            ys = [b for _, b in per_step[-10:]]
            xm, ym = st.mean(xs), st.mean(ys)
            sxx = sum((x - xm) ** 2 for x in xs)
            slope = sum((x - xm) * (y - ym) for x, y in zip(xs, ys)) / sxx if sxx else 0.0
            if slope < -FALL_SLOPE:
                return "falling", steps, last
        # Guard 2: in contact at Z 0 (onset at the bottom) for AT_ZERO steps in a row.
        at_zero = at_zero + 1 if last <= FIND_STEP else 0
        if at_zero >= AT_ZERO:
            return "stuck-at-0", steps, last
        if steps >= max_steps:
            return "limit", steps, last
        motor1()
        steps += 1


def analyse(rows, out=print):
    """Onset against motor step: least-squares slope = Z counts per motor step."""
    pts = [(s, o) for (_, s, r, o, _) in rows if o is not None]
    if len(pts) < 3:
        out("too few onsets")
        return None
    xs, ys = [a for a, _ in pts], [b for _, b in pts]
    xm, ym = st.mean(xs), st.mean(ys)
    sxx = sum((x - xm) ** 2 for x in xs)
    if sxx == 0:
        out("all onsets at one motor position: no slope")
        return None
    k = sum((x - xm) * (y - ym) for x, y in zip(xs, ys)) / sxx
    res = [y - (ym + k * (x - xm)) for x, y in zip(xs, ys)]
    rep = [abs(rows[i][3] - rows[i + 1][3]) for i in range(len(rows) - 1)
           if rows[i][1] == rows[i + 1][1] and rows[i][3] is not None and rows[i + 1][3] is not None]
    out("Z counts per motor step: %.1f  (%d onsets, residual sd %.0f, repeat |diff| median %s)"
        % (k, len(pts), st.pstdev(res), st.median(rep) if rep else "-"))
    return k


def self_test():
    import random

    class W:
        def __init__(self, k, g0=300, noise=16, sign=+1, stick=0, seed=2):
            self.k, self.g, self.z, self.n, self.sign = k, g0, 0, 0, sign
            self.rng, self.noise, self.stick, self.t = random.Random(seed), noise, stick, 0.0
        def set_z(self, z):
            assert 0 <= z <= 65535
            self.z = z
        def read(self):
            self.t += 0.01
            d = self.z - self.g
            i = 0.0 if d < -1000 else min(32767.0, 1000 * 10 ** (d / 250.0))
            return i + self.rng.gauss(0, self.noise)
        def motor1(self):
            self.n += 1
            if self.stick and self.n % self.stick:
                return                              # stick: nothing, then a slip
            self.g += self.sign * self.k * (self.stick or 1)
        def now(self): return self.t
    w = W(200)
    rows = []
    res, steps, last = run(w.set_z, w.read, w.motor1, w.now, lambda s: None, rows=rows)
    assert res == "mid-range" and last >= 20000, (res, last)
    k = analyse(rows, out=lambda s: None)
    assert abs(k - 200) < 20, k
    assert w.z == 0, "must end with Z at 0"
    # Wrong motor sign: the onset falls; must stop, not run on toward the sample.
    w = W(200, g0=15000, sign=-1)
    res, steps, last = run(w.set_z, w.read, w.motor1, w.now, lambda s: None)
    assert res in ("falling", "lost") and steps <= 25 and w.z == 0, (res, steps, w.z)
    # Stick-slip (nothing for 9 steps, then 10 at once): still converges, slope still ~k.
    w = W(200, stick=10)
    rows = []
    res, steps, last = run(w.set_z, w.read, w.motor1, w.now, lambda s: None, rows=rows)
    assert res == "mid-range" and abs(analyse(rows, out=lambda s: None) - 200) < 40
    print("self-test: pass (200 counts/step recovered; wrong sign stops; stick-slip converges)")


def red_check():
    global FALL_SLOPE, AT_ZERO
    keep = FALL_SLOPE, AT_ZERO
    FALL_SLOPE, AT_ZERO = 10 ** 9, 10 ** 9      # both guards disabled
    try:
        import random
        class W:
            def __init__(self): self.g, self.z, self.t = 15000, 0, 0.0
            def set_z(self, z): self.z = z
            def read(self):
                self.t += 0.01
                d = self.z - self.g
                return 0.0 if d < -1000 else min(32767.0, 1000 * 10 ** (d / 250.0))
            def motor1(self): self.g -= 200
            def now(self): return self.t
        w = W()
        res, steps, last = run(w.set_z, w.read, w.motor1, w.now, lambda s: None, max_steps=60)
        caught = steps > 25
    finally:
        FALL_SLOPE, AT_ZERO = keep
    assert caught, "red check failed: the wrong-sign test passed with the guard disabled"
    print("red check: pass (guard disabled -> ran %d steps the wrong way)" % steps)


if __name__ == "__main__":
    # Added 2026-09-19 after a --test run of a script WITHOUT a self-test went straight to its
    # hardware path (no port was connected, so nothing was sent). Unknown options now refuse.
    _bad = [a for a in sys.argv[1:] if a.startswith('-') and a not in ['--test']]
    if _bad:
        sys.exit('refusing unknown option(s) %s: this script drives the instrument%s'
                 % (_bad, '' if True else ' and has NO self-test'))
    if "--test" in sys.argv:
        self_test(); red_check(); sys.exit(0)
    import serial, csv
    sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
    from stm_approach import Device, find_teensy
    from stm_feedback_scan import read_averaged
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    mx = int(args[0]) if args else 200
    stop = int(args[1]) if len(args) > 1 else 20000
    stamp = lambda: time.strftime("%H:%M:%S", time.gmtime())
    out = lambda s: print(stamp(), s, flush=True)
    port = serial.Serial(find_teensy(), 115200, timeout=0.2)
    dev = Device(port)
    rows = []
    t0 = time.time()
    fname = "stairs_%d.csv" % int(t0)
    try:
        dev._write(b"DACX 32768\n"); time.sleep(0.02)
        dev._write(b"DACY 32768\n"); time.sleep(0.02)
        dev.set_bias(38229); time.sleep(0.2)

        def set_z(z):
            dev._write(("DACZ %d\n" % z).encode()); time.sleep(0.002)

        def rd():
            v = [x for x in (read_averaged(dev) for _ in range(NREAD)) if x is not None]
            return st.mean(v) if v else None
        res, steps, last = run(set_z, rd, lambda: dev.move_motor(+1), lambda: time.time() - t0,
                               out, max_steps=mx, stop_onset=stop, rows=rows)
        set_z(0)
        out("RESULT: %s after %d retract steps, last onset Z %s; Z left at 0" % (res, steps, last))
    finally:
        port.close()
        with open(fname, "w", newline="") as f:
            w = csv.writer(f); w.writerow(["t", "motor_steps", "repeat", "onset_z", "adc"]); w.writerows(rows)
    analyse(rows, out=out)
