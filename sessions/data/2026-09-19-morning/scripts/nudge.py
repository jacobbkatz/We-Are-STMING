"""Hand-set judged with the hand OFF: nudge, let go, listen.

2026-09-19 morning. Three hand-sets in a row left the gold within reach while a hand was on the
screw and far out of reach within a minute of letting go (ztest_run1, stairs_run1, and 2026-09-19
bench 3.4). HYPOTHESIS: the side screws run in PRINTED threads with axial play; the rubber-band
preload holds each screw at the back of its play; fingers pushing while turning take the play up;
on release the preload pushes it back. So the position that matters is the one with the hand OFF,
and every beeper so far has judged it with the hand ON.

The laptop sweeps Z 0 -> Z_TOP in ZSTEP steps about once a second (sample -0.5 V) and says:
  FAR       nothing anywhere in Z: one short tick every ~3 s.  -> nudge IN a hair, LET GO, wait.
  PAST      current even at Z 0 (gold past the fully retracted tip): three low beeps each sweep.
            -> nudge OUT a hair, LET GO, wait.
  IN RANGE  first current at Z between LO and HI: one high beep. It must hold for CONFIRM sweeps
            in a row, hands off, before it is believed -> then four high beeps, "DONE: leave",
            and the script ends with Z at 0, bias -0.5 V.
For the tip fitted ~03:00 UTC 2026-09-19: HIGH Z extends toward the sample; Z 0 is fully retracted.
Every sweep ends with Z at 0. A reading >= HARD anywhere sends Z to 0 at once.

Usage: py nudge.py            py nudge.py --test
"""
import sys, time

DETECT, HARD = 300, 8000
ZSTEP, Z_TOP = 1000, 62000
LO, HI = 3000, 59000
CONFIRM = 5
TICK_EVERY = 3.0


def sweep(set_z, read):
    """('past', 0) / ('in', z) / ('far', None). Z ends at 0."""
    set_z(0)
    v = read()
    if v is not None and abs(v) >= DETECT:
        return "past", 0
    z = ZSTEP
    while z <= Z_TOP:
        set_z(z)
        v = read()
        if v is not None and abs(v) >= DETECT:
            set_z(0)
            return "in", z
        z += ZSTEP
    set_z(0)
    return "far", None


def run(set_z, read, beep, now, sleep, out, maxtime=1800):
    t0 = now()
    ok = 0
    last_tick = -1e9
    last_state = None
    while now() - t0 < maxtime:
        state, z = sweep(set_z, read)
        if state == "in" and not (LO <= z <= HI):
            state = "edge"
        if state != last_state:
            out("%6.1fs %s%s" % (now() - t0, state.upper(), "" if z is None else " at Z %d" % z))
            last_state = state
        if state == "in":
            ok += 1
            beep("high1")
            if ok >= CONFIRM:
                out("%6.1fs IN RANGE at Z %d for %d sweeps with hands off: DONE. Leave the room."
                    % (now() - t0, z, ok))
                beep("done")
                return "in", z
        else:
            ok = 0
            if state == "past":
                beep("low3")
            elif state in ("far", "edge") and now() - last_tick >= TICK_EVERY:
                beep("tick")
                last_tick = now()
        sleep(0.2)
    return "timeout", None


def self_test():
    import random

    class W:
        def __init__(self, plan):
            self.plan, self.t, self.z, self.beeps, self.rng = plan, 0.0, 0, [], random.Random(5)
        def gold(self):
            g = None
            for t, gg in self.plan:
                if self.t >= t:
                    g = gg
            return g
        def set_z(self, z):
            assert 0 <= z <= 65535
            self.z = z
        def read(self):
            self.t += 0.004
            d = self.z - self.gold()
            i = 0.0 if d < -1000 else min(32767.0, 1000 * 10 ** (d / 250.0))
            return i + self.rng.gauss(0, 35)
        def beep(self, k): self.beeps.append(k)
        def now(self): return self.t
        def sleep(self, s): self.t += s

    # far, then a nudge puts it past, then a nudge back puts it in range and it stays: done.
    w = W([(0, 200000), (10, -5000), (20, 30000)])
    res, z = run(w.set_z, w.read, w.beep, w.now, w.sleep, lambda s: None)
    assert res == "in" and 25000 <= z <= 31000 and w.z == 0, (res, z, w.z)
    assert "low3" in w.beeps and "tick" in w.beeps and w.beeps[-1] == "done"
    # In range for ONE sweep then springs back out (the hand-release case): must NOT say done.
    w = W([(0, 30000), (0.5, 200000)])
    res, z = run(w.set_z, w.read, w.beep, w.now, w.sleep, lambda s: None, maxtime=30)
    assert res == "timeout", res
    print("self-test: pass (far -> past -> in range held = done; a one-sweep visit is not done)")


def red_check():
    global CONFIRM
    keep = CONFIRM
    CONFIRM = 1
    try:
        import random
        class W:
            def __init__(self): self.t, self.z = 0.0, 0
            def set_z(self, z): self.z = z
            def read(self):
                self.t += 0.004
                g = 30000 if self.t < 0.5 else 200000
                d = self.z - g
                return 0.0 if d < -1000 else min(32767.0, 1000 * 10 ** (d / 250.0))
            def now(self): return self.t
            def sleep(self, s): self.t += s
        w = W()
        res, z = run(w.set_z, w.read, lambda k: None, w.now, w.sleep, lambda s: None, maxtime=30)
        caught = res == "in"
    finally:
        CONFIRM = keep
    assert caught, "red check failed"
    print("red check: pass (CONFIRM=1 declares done on a one-sweep visit, as the test forbids)")


if __name__ == "__main__":
    if "--test" in sys.argv:
        self_test(); red_check(); sys.exit(0)
    import serial, winsound, statistics as st
    sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
    from stm_approach import Device, find_teensy
    from stm_feedback_scan import read_averaged
    port = serial.Serial(find_teensy(), 115200, timeout=0.2)
    dev = Device(port)

    def beep(kind):
        if kind == "tick":
            winsound.Beep(900, 60)
        elif kind == "low3":
            for _ in range(3):
                winsound.Beep(500, 150); time.sleep(0.05)
        elif kind == "high1":
            winsound.Beep(2000, 150)
        elif kind == "done":
            for _ in range(4):
                winsound.Beep(2000, 300); time.sleep(0.1)

    def set_z(z):
        dev._write(("DACZ %d\n" % z).encode()); time.sleep(0.001)

    def rd():
        v = [x for x in (read_averaged(dev) for _ in range(2)) if x is not None]
        return st.mean(v) if v else None
    try:
        dev._write(b"DACX 32768\n"); time.sleep(0.02)
        dev._write(b"DACY 32768\n"); time.sleep(0.02)
        dev.set_z(0)
        dev.set_bias(38229); time.sleep(0.2)
        res, z = run(set_z, rd, beep, time.time, time.sleep,
                     lambda s: print(time.strftime("%H:%M:%S", time.gmtime()), s, flush=True))
        set_z(0)
        print("RESULT:", res, z, "(Z left at 0, bias -0.5 V)", flush=True)
    finally:
        port.close()
