"""A faster woodpecker: single motor steps toward the sample, a COARSE Z sweep after each.

2026-09-19 morning. Every hand-set so far has left the gold out of the piezo's reach within minutes
(the screw presses the plate; it springs back on release - sessions/2026-09-19-bench.md 3.4, and
ztest_run1 / stairs_run1 this morning). The motor is the only fine actuator (a few nm per step at
the tip, if the lever is ~40), so it has to close the last micrometres, and it must be quick:
Code/pc/stm_approach.py spends ~2.8 s per step on a 200-point sweep. This spends ~0.8 s.

For the tip fitted ~03:00 UTC 2026-09-19: HIGH Z extends toward the sample; NEGATIVE MTMV approaches.

Each cycle: Z at 0 (fully retracted) for the motor move; MTMV -1 (skipped with --wait); then Z up
from 0 to Z_TOP in ZSTEP steps, one averaged ADCR each. At the first |reading| >= DETECT: Z -> 0 at
once, report the Z, stop. Before each sweep the reading at Z 0 is checked: >= DETECT there means the
gold came in past the fully retracted tip (a slip) -> stop, Z stays 0, says "back the motor off".
The motor never moves unless the whole sweep came back clear.

Usage: py fastwood.py [max_steps] [--wait]        py fastwood.py --test
  --wait: no motor at all, just a sweep every WAIT_PERIOD s (is the gold creeping back by itself?)
"""
import sys, time

DETECT = 300            # averaged ADCR sd ~35 counts tip clear, so ~9 sigma
ZSTEP, Z_TOP = 1000, 62000
WAIT_PERIOD = 10.0


def sweep(set_z, read, z_top=Z_TOP, zstep=ZSTEP):
    """Returns (z, reading) at the first detection (Z already back at 0), or (None, None)."""
    z = 0
    while z <= z_top:
        set_z(z)
        v = read()
        if v is not None and abs(v) >= DETECT:
            set_z(0)
            return z, v
        z += zstep
    set_z(0)
    return None, None


def run(set_z, read, motor1, now, sleep, out, max_steps=700, wait=False, rows=None):
    """Returns (status, steps, z_hit)."""
    rows = rows if rows is not None else []
    steps = 0
    t_last = -1e9
    while True:
        set_z(0)
        v0 = read()
        if v0 is not None and abs(v0) >= DETECT:
            rows.append((round(now(), 3), steps, 0, v0))
            out("CONTACT AT Z 0 after %d steps (%.0f counts): the gold is past the retracted tip. "
                "Back the motor off." % (steps, v0))
            return "at-zero", steps, 0
        z, v = sweep(set_z, read)
        rows.append((round(now(), 3), steps, z, v))
        if z is not None:
            out("FOUND at Z %d (%.0f counts) after %d steps; Z back to 0" % (z, v, steps))
            return "found", steps, z
        if steps % 25 == 0:
            out("%d steps, nothing in Z 0..%d" % (steps, Z_TOP))
        if wait:
            if now() - t_last < WAIT_PERIOD:
                sleep(max(0.0, WAIT_PERIOD - (now() - t_last)))
            t_last = now()
            if steps >= max_steps:
                return "limit", steps, None
            steps += 1              # counts sweeps in --wait mode
            continue
        if steps >= max_steps:
            return "limit", steps, None
        motor1()
        steps += 1


def self_test():
    import random

    class W:
        """Gold at Z g (counts); each approach step moves it DOWN by k after `backlash` steps."""
        def __init__(self, g=90000, k=250, backlash=150, slip=None, seed=3):
            self.g, self.k, self.back, self.n, self.z = g, k, backlash, 0, 0
            self.slip, self.rng, self.t, self.deepest = slip, random.Random(seed), 0.0, -1e9
        def set_z(self, z):
            assert 0 <= z <= 65535
            self.z = z
            self.deepest = max(self.deepest, z - self.g)
        def read(self):
            self.t += 0.004
            d = self.z - self.g
            i = 0.0 if d < -1000 else min(32767.0, 1000 * 10 ** (d / 250.0))
            return i + self.rng.gauss(0, 35)
        def motor1(self):
            self.n += 1
            self.t += 0.52
            if self.n > self.back:
                self.g -= self.k
            if self.slip and self.n == self.slip[0]:
                self.g -= self.slip[1]
        def now(self): return self.t
        def sleep(self, s): self.t += s
    w = W()
    res, steps, z = run(w.set_z, w.read, w.motor1, w.now, w.sleep, lambda s: None)
    assert res == "found" and w.z == 0, (res, w.z)
    assert w.deepest <= ZSTEP, "pressed %.0f counts past the gold" % w.deepest
    assert 150 < steps < 300, steps
    # A big slip lands the gold past the retracted tip: must stop at once, motor still.
    w = W(g=70000, slip=(40, 80000))
    res, steps, z = run(w.set_z, w.read, w.motor1, w.now, w.sleep, lambda s: None)
    assert res in ("at-zero", "found") and w.n == 40, (res, w.n)
    # Nothing in reach: stops at the limit with Z at 0.
    w = W(g=10 ** 7)
    res, steps, z = run(w.set_z, w.read, w.motor1, w.now, w.sleep, lambda s: None, max_steps=50)
    assert res == "limit" and w.z == 0 and w.n == 50
    # --wait never moves the motor.
    w = W(g=10 ** 7)
    res, steps, z = run(w.set_z, w.read, w.motor1, w.now, w.sleep, lambda s: None, max_steps=5, wait=True)
    assert w.n == 0 and res == "limit"
    # 20-step chunks (5000 counts per cycle at 250/step): still found with <= 1 Z step of press.
    w = W(g=300000, k=5000, backlash=8)
    res, steps, z = run(w.set_z, w.read, w.motor1, w.now, w.sleep, lambda s: None)
    assert res == "found" and w.z == 0 and w.deepest <= ZSTEP, (res, w.z, w.deepest)
    assert 55000 <= z <= 62000, "a chunked approach must meet the gold at the TOP of the range (%d)" % z
    print("self-test: pass (found after backlash with <= 1 Z step of press; slip stops; limit; "
          "--wait; 20-step chunks meet it at the top)")


def red_check():
    global DETECT
    keep = DETECT
    DETECT = 10 ** 9        # detection disabled: the sweep would run on into the gold
    try:
        import random
        class W:
            def __init__(self): self.g, self.z, self.n, self.t, self.deepest = 60000, 0, 0, 0.0, -1e9
            def set_z(self, z):
                self.z = z; self.deepest = max(self.deepest, z - self.g)
            def read(self):
                d = self.z - self.g
                return 0.0 if d < -1000 else min(32767.0, 1000 * 10 ** (d / 250.0))
            def motor1(self): self.n += 1; self.g -= 250
            def now(self): return self.t
            def sleep(self, s): self.t += s
        w = W()
        run(w.set_z, w.read, w.motor1, w.now, w.sleep, lambda s: None, max_steps=30)
        caught = w.deepest > ZSTEP
    finally:
        DETECT = keep
    assert caught, "red check failed: with detection disabled the press test still passed"
    print("red check: pass (detection disabled -> pressed %.0f counts past the gold)" % w.deepest)


if __name__ == "__main__":
    if "--test" in sys.argv:
        self_test(); red_check(); sys.exit(0)
    import serial, csv, statistics as st
    sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
    from stm_approach import Device, find_teensy
    from stm_feedback_scan import read_averaged
    # --chunk N: N motor steps per cycle instead of 1. Added 12:13 UTC with Jacob's OK ("Yes, up to
    # 20 steps"): ~80 nm at the tip per chunk if a step is ~4 nm (2026-09-17), ~12x under the Z
    # range, so the full Z sweep between chunks still sees the gold arrive at the top of the range.
    chunk = int(sys.argv[sys.argv.index("--chunk") + 1]) if "--chunk" in sys.argv else 1
    assert 1 <= chunk <= 20, "Jacob approved chunks of up to 20 steps"
    args = [a for i, a in enumerate(sys.argv[1:], 1)
            if not a.startswith("--") and sys.argv[i - 1] != "--chunk"]
    mx = int(args[0]) if args else 700
    wait = "--wait" in sys.argv
    stamp = lambda: time.strftime("%H:%M:%S", time.gmtime())
    out = lambda s: print(stamp(), s, flush=True)
    port = serial.Serial(find_teensy(), 115200, timeout=0.2)
    dev = Device(port)
    rows = []
    t0 = time.time()
    fname = "fastwood_%d.csv" % int(t0)
    try:
        dev._write(b"DACX 32768\n"); time.sleep(0.02)
        dev._write(b"DACY 32768\n"); time.sleep(0.02)
        dev.set_z(0)
        dev.set_bias(38229); time.sleep(0.2)

        def set_z(z):
            dev._write(("DACZ %d\n" % z).encode()); time.sleep(0.001)

        def rd():
            v = [x for x in (read_averaged(dev) for _ in range(2)) if x is not None]
            return st.mean(v) if v else None
        res, steps, z = run(set_z, rd, lambda: dev.move_motor(-chunk), lambda: time.time() - t0,
                            time.sleep, out, max_steps=mx, wait=wait, rows=rows)
        set_z(0)
        out("RESULT: %s after %d %s of %d = %d motor steps; Z left at 0"
            % (res, steps, "sweeps" if wait else "approach chunks", chunk, steps * chunk))
    finally:
        port.close()
        with open(fname, "w", newline="") as f:
            w = csv.writer(f); w.writerow(["t", "steps", "z_hit", "adc"]); w.writerows(rows)
