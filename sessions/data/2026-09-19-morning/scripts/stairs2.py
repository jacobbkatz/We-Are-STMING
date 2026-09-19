"""Motor staircase in EITHER direction, re-finding the gold after every single step.

2026-09-19 morning. stairs.py only retracts. After fastwood.py finds the gold near the TOP of the Z
range it has to come further IN (toward the sample) to reach mid-range, so this takes a direction:

  --dir in   MTMV -1 per step (toward the sample): the onset Z should FALL; stop when <= target
  --dir out  MTMV +1 per step (away):              the onset Z should RISE; stop when >= target

For the tip fitted ~03:00 UTC 2026-09-19: HIGH Z extends toward the sample; NEGATIVE MTMV approaches.

Two-stage find, ALWAYS from Z 0, so a slip can never press the tip in by more than one coarse step:
  coarse: Z 0 -> Z_TOP in CSTEP, first averaged |I| >= DETECT;   fine: from (coarse - CSTEP) in
  FSTEP until |I| >= TARGET. The onset is the fine Z. Z -> 0 after every find and for every motor move.

Stops, Z left at 0:
  target reached; step limit;
  contact at Z 0 (the gold is past the fully retracted tip) - at once in 'in' mode;
  the onset trending the WRONG way over the last 10 positions (slope beyond WRONG_SLOPE);
  the gold lost (nothing in 0..Z_TOP) twice running.
Also reports Z counts per motor step and the steps of slack before the onset first moved.

Usage: py stairs2.py --dir in|out [max_steps] [target]        py stairs2.py --test
"""
import sys, time, statistics as st

TARGET, DETECT = 1000, 300
CSTEP, FSTEP, Z_TOP = 1000, 16, 62000
WRONG_SLOPE = 50
NREAD = 3


def find(set_z, read):
    """Returns onset Z or None. Z ends at 0."""
    z, hit = 0, None
    while z <= Z_TOP:
        set_z(z)
        v = read()
        if v is not None and abs(v) >= DETECT:
            hit = z
            break
        z += CSTEP
    if hit is None:
        set_z(0)
        return None
    z = max(0, hit - CSTEP)
    onset = hit
    while z <= hit:
        set_z(z)
        v = read()
        if v is not None and abs(v) >= TARGET:
            onset = z
            break
        z += FSTEP
    set_z(0)
    return onset


def run(set_z, read, motor, now, out, direction, max_steps=400, target=30000, rows=None):
    """direction +1 = 'in' (MTMV -1, onset falls), -1 = 'out' (MTMV +1, onset rises)."""
    rows = rows if rows is not None else []
    hist = []
    lost = 0
    steps = 0
    while True:
        set_z(0)
        v0 = read()
        if v0 is not None and abs(v0) >= DETECT:
            rows.append((round(now(), 3), steps, 0))
            out("CONTACT AT Z 0 at step %d (%.0f counts)" % (steps, v0))
            if direction > 0:
                return "at-zero", steps, 0
        on = find(set_z, read)
        rows.append((round(now(), 3), steps, on))
        if steps % 5 == 0 or on is None:
            out("step %3d: onset %s" % (steps, on))
        if on is None:
            lost += 1
            if lost >= 2:
                return "lost", steps, None
        else:
            lost = 0
            hist.append((steps, on))
            if (direction > 0 and on <= target) or (direction < 0 and on >= target):
                return "target", steps, on
            if direction > 0 and on <= FSTEP:
                return "at-zero", steps, on
            if len(hist) >= 10:
                xs = [a for a, _ in hist[-10:]]
                ys = [b for _, b in hist[-10:]]
                xm, ym = st.mean(xs), st.mean(ys)
                sxx = sum((x - xm) ** 2 for x in xs)
                slope = sum((x - xm) * (y - ym) for x, y in zip(xs, ys)) / sxx if sxx else 0.0
                # 'in' wants the onset to fall (slope < 0); a clear RISE means the wrong way.
                if direction * slope > WRONG_SLOPE:
                    return "wrong-way", steps, on
        if steps >= max_steps:
            return "limit", steps, (hist[-1][1] if hist else None)
        set_z(0)
        motor(-direction)
        steps += 1


def analyse(rows, out=print):
    pts = [(s, o) for (_, s, o) in rows if o is not None]
    if len(pts) < 3:
        out("too few onsets"); return None, None
    # slack: steps before the onset first moved by more than 3x the fine step from its start
    o0 = pts[0][1]
    slack = next((s for s, o in pts if abs(o - o0) > 3 * CSTEP), None)
    moving = [(s, o) for s, o in pts if slack is not None and s >= slack] or pts
    xs, ys = [a for a, _ in moving], [b for _, b in moving]
    xm, ym = st.mean(xs), st.mean(ys)
    sxx = sum((x - xm) ** 2 for x in xs)
    k = sum((x - xm) * (y - ym) for x, y in zip(xs, ys)) / sxx if sxx else None
    out("onset moved after %s steps of slack; then %s Z counts per motor step (%d onsets)"
        % (slack, "%.1f" % k if k is not None else "-", len(moving)))
    return slack, k


def _world(g, k, slack, sign_ok=True, slip=None, seed=4):
    import random

    class W:
        def __init__(self):
            self.g, self.z, self.n, self.t = g, 0, 0, 0.0
            self.rng, self.deepest = random.Random(seed), -1e9
            self.moved = 0
        def set_z(self, z):
            assert 0 <= z <= 65535
            self.z = z; self.deepest = max(self.deepest, z - self.g)
        def read(self):
            self.t += 0.004
            d = self.z - self.g
            i = 0.0 if d < -1000 else min(32767.0, 1000 * 10 ** (d / 250.0))
            return i + self.rng.gauss(0, 35)
        def motor(self, s):
            self.n += 1; self.t += 0.52
            self.moved += 1
            if self.moved > slack:
                self.g += (s if sign_ok else -s) * k      # MTMV -1 brings the gold DOWN in Z
            if slip and self.n == slip[0]:
                self.g -= slip[1]
        def now(self): return self.t
    return W()


def self_test():
    # 'in' from a gold near the top: slack 120 steps, then 250 counts/step; stops at 30000.
    w = _world(60000, 250, 120)
    rows = []
    res, steps, on = run(w.set_z, w.read, w.motor, w.now, lambda s: None, +1, rows=rows)
    assert res == "target" and on <= 30000 and w.z == 0, (res, on, w.z)
    assert w.deepest <= CSTEP, w.deepest
    slack, k = analyse(rows, out=lambda s: None)
    assert slack is not None and 100 <= slack <= 140 and abs(k + 250) < 30, (slack, k)
    # 'out' from a gold near the bottom.
    w = _world(2000, 250, 0)
    res, steps, on = run(w.set_z, w.read, w.motor, w.now, lambda s: None, -1, target=20000)
    assert res == "target" and on >= 20000, (res, on)
    # Wrong sign in 'in' mode: onset rises -> stops within ~20 steps, not 400.
    w = _world(40000, 250, 0, sign_ok=False)
    res, steps, on = run(w.set_z, w.read, w.motor, w.now, lambda s: None, +1)
    assert res in ("wrong-way", "lost") and steps <= 25, (res, steps)
    # A slip lands the gold past the retracted tip: stop at once in 'in' mode.
    w = _world(50000, 250, 0, slip=(30, 60000))
    res, steps, on = run(w.set_z, w.read, w.motor, w.now, lambda s: None, +1)
    assert res == "at-zero" and w.n == 30, (res, w.n)
    print("self-test: pass (in with slack 120 -> 250/step; out; wrong sign stops; slip stops)")


def red_check():
    global WRONG_SLOPE
    keep = WRONG_SLOPE
    WRONG_SLOPE = 10 ** 9
    try:
        w = _world(40000, 250, 0, sign_ok=False)
        res, steps, on = run(w.set_z, w.read, w.motor, w.now, lambda s: None, +1, max_steps=60)
        caught = steps > 25
    finally:
        WRONG_SLOPE = keep
    assert caught, "red check failed"
    print("red check: pass (wrong-way guard disabled -> %d steps the wrong way, %s)" % (steps, res))


if __name__ == "__main__":
    if "--test" in sys.argv:
        self_test(); red_check(); sys.exit(0)
    import serial, csv
    sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
    from stm_approach import Device, find_teensy
    from stm_feedback_scan import read_averaged
    d = sys.argv[sys.argv.index("--dir") + 1]
    assert d in ("in", "out")
    direction = +1 if d == "in" else -1
    args = [a for a in sys.argv[1:] if not a.startswith("--") and a not in ("in", "out")]
    mx = int(args[0]) if args else 400
    target = int(args[1]) if len(args) > 1 else 30000
    stamp = lambda: time.strftime("%H:%M:%S", time.gmtime())
    out = lambda s: print(stamp(), s, flush=True)
    port = serial.Serial(find_teensy(), 115200, timeout=0.2)
    dev = Device(port)
    rows = []
    t0 = time.time()
    fname = "stairs2_%s_%d.csv" % (d, int(t0))
    try:
        dev._write(b"DACX 32768\n"); time.sleep(0.02)
        dev._write(b"DACY 32768\n"); time.sleep(0.02)
        dev.set_z(0)
        dev.set_bias(38229); time.sleep(0.2)

        def set_z(z):
            dev._write(("DACZ %d\n" % z).encode()); time.sleep(0.001)

        def rd():
            v = [x for x in (read_averaged(dev) for _ in range(NREAD)) if x is not None]
            return st.mean(v) if v else None
        res, steps, on = run(set_z, rd, lambda s: dev.move_motor(s), lambda: time.time() - t0,
                             out, direction, max_steps=mx, target=target, rows=rows)
        set_z(0)
        out("RESULT: %s after %d steps (%s), onset %s; Z left at 0" % (res, steps, d, on))
    finally:
        port.close()
        with open(fname, "w", newline="") as f:
            w = csv.writer(f); w.writerow(["t", "motor_steps", "onset_z"]); w.writerows(rows)
    analyse(rows, out=out)
