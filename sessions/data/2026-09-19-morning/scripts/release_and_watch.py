"""Release the gold with motor RETRACT chunks, then WATCH where it goes with the motor still.

2026-09-19 morning. apz_run1 (12:50): after a 20-step approach chunk found the gold at Z 17000, it
kept coming toward the tip at ~15,000 Z counts/s for ~1 s (the onset fell 17000 -> 12520 -> 11952 ->
8792 while Z was RETRACTING) and ended pressed on the tip at Z 0. After the hand back-offs the gold
went the OTHER way, out of reach within minutes. Hypothesis: after every coarse move the gold keeps
moving the same way for seconds (drive-train / rubber-band / leaf relaxation). This measures it.

Phase 1 (release): Z 0, sample -0.5 V. MTMV +CHUNK (retract) until CONFIRM readings in a row at Z 0
are under CLEAR, or MAX_CHUNKS. Jacob, 12:5x UTC: "move in bigger chunks ... if you lose it".
Phase 2 (watch): NO motor. Every PERIOD s, sweep Z 0 -> Z_TOP in ZSTEP steps (fastwood.sweep):
record (t, onset) or 'far', Z back to 0 at once. Contact at Z 0 -> record 'past' and stop.
For the tip fitted ~03:00 UTC 2026-09-19: HIGH Z extends toward the sample; POSITIVE MTMV retracts.

Usage: py release_and_watch.py [watch_s]        py release_and_watch.py --test
"""
import sys, time
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\sessions\data\2026-09-19-morning\scripts")
import fastwood

fastwood.ZSTEP, fastwood.DETECT = 250, 200
CHUNK, MAX_CHUNKS, CLEAR, CONFIRM = 20, 60, 150, 3
PERIOD = 3.0


def release(set_z, read, motor_chunk, out):
    set_z(0)
    ok = 0
    for n in range(1, MAX_CHUNKS + 1):
        motor_chunk()
        v = read()
        ok = ok + 1 if (v is not None and abs(v) < CLEAR) else 0
        if n % 5 == 0 or ok:
            out("release chunk %d (+%d steps): %s counts" % (n, n * CHUNK, v))
        if ok >= CONFIRM:
            return "clear", n
    return "limit", MAX_CHUNKS


def watch(set_z, read, now, sleep, out, duration, rows):
    t0 = now()
    last = None
    while now() - t0 < duration:
        # fastwood.sweep returns (z_hit, reading), or (None, None). A first version unpacked it as
        # (state, z) and logged READINGS as onsets - caught by the simulated test, not the bench.
        z, _reading = fastwood.sweep(set_z, read)
        state = "found" if z is not None else "far"
        set_z(0)
        v0 = read()
        if v0 is not None and abs(v0) >= fastwood.DETECT:
            rows.append((round(now() - t0, 2), "past", 0))
            out("%6.1fs PAST: contact at Z 0 (%.0f counts) - stop watching" % (now() - t0, v0))
            return "past"
        rows.append((round(now() - t0, 2), state, z))
        if state != last or state == "found":
            out("%6.1fs %s%s" % (now() - t0, state.upper(), "" if z is None else " onset Z %d" % z))
        last = state
        sleep(PERIOD)
    return "done"


def self_test():
    class W:
        """Gold position relaxes toward a target set by the motor, time constant tau."""
        def __init__(self, g, tau=20.0, per_step=300.0):
            self.g, self.target, self.tau, self.k = g, g, tau, per_step
            self.t, self.z = 0.0, 0
        def _adv(self, dt):
            self.g += (self.target - self.g) * min(1.0, dt / self.tau)
            self.t += dt
        def set_z(self, z):
            assert 0 <= z <= 65535
            self.z = z
        def read(self):
            self._adv(0.004)
            d = self.z - self.g
            return 0.0 if d < -1000 else min(32767.0, 1000 * 10 ** (d / 250.0))
        def motor_chunk(self):
            self.target += CHUNK * self.k
            self._adv(0.8)
        def now(self): return self.t
        def sleep(self, s): self._adv(s)
    # pressed 3000 counts past the retracted tip: releases, then creeps away and is tracked
    w = W(g=-3000)
    res, n = release(w.set_z, w.read, w.motor_chunk, lambda s: None)
    assert res == "clear" and w.z == 0, (res, w.z)
    rows = []
    r = watch(w.set_z, w.read, w.now, w.sleep, lambda s: None, 60, rows)
    found = [z for _, s, z in rows if s == "found"]
    assert len(found) >= 3 and found[-1] > found[0], "must track the gold moving away (%s)" % found[:5]
    # a world where the gold creeps IN after release: must stop at 'past'
    w = W(g=-3000)
    release(w.set_z, w.read, w.motor_chunk, lambda s: None)
    w.target = -20000
    r = watch(w.set_z, w.read, w.now, w.sleep, lambda s: None, 120, [])
    assert r == "past", r
    print("self-test: pass (release clears; watch tracks a receding gold; stops when it comes past)")


def red_check():
    global CONFIRM
    keep = CONFIRM
    CONFIRM = 10 ** 9
    try:
        class W:
            def __init__(self): self.n = 0
            def set_z(self, z): pass
            def read(self): return 0.0 if self.n > 3 else 32767.0
            def motor_chunk(self): self.n += 1
        w = W()
        res, n = release(w.set_z, w.read, w.motor_chunk, lambda s: None)
        caught = res == "limit" and w.n == MAX_CHUNKS
    finally:
        CONFIRM = keep
    assert caught
    print("red check: pass (without the clear test the release runs all %d chunks)" % MAX_CHUNKS)


if __name__ == "__main__":
    # Added 2026-09-19 after a --test run of a script WITHOUT a self-test went straight to its
    # hardware path (no port was connected, so nothing was sent). Unknown options now refuse.
    _bad = [a for a in sys.argv[1:] if a.startswith('-') and a not in ['--test']]
    if _bad:
        sys.exit('refusing unknown option(s) %s: this script drives the instrument%s'
                 % (_bad, '' if True else ' and has NO self-test'))
    if "--test" in sys.argv:
        self_test(); red_check(); sys.exit(0)
    import serial, csv, statistics as st
    sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
    from stm_approach import Device, find_teensy
    from stm_feedback_scan import read_averaged
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    duration = float(args[0]) if args else 180.0
    stamp = lambda: time.strftime("%H:%M:%S", time.gmtime())
    out = lambda s: print(stamp(), s, flush=True)
    port = serial.Serial(find_teensy(), 115200, timeout=0.2)
    dev = Device(port)
    rows = []
    t0 = time.time()
    try:
        dev._write(b"DACX 32768\n"); time.sleep(0.02)
        dev._write(b"DACY 32768\n"); time.sleep(0.02)
        dev.set_z(0)
        dev.set_bias(38229); time.sleep(0.2)

        def set_z(z):
            dev._write(("DACZ %d\n" % z).encode()); time.sleep(0.001)

        def rd():
            v = [x for x in (read_averaged(dev) for _ in range(3)) if x is not None]
            return st.mean(v) if v else None
        res, n = release(set_z, rd, lambda: dev.move_motor(+CHUNK), out)
        out("RELEASE: %s after %d chunks (+%d steps)" % (res, n, n * CHUNK))
        if res == "clear":
            r = watch(set_z, rd, time.time, time.sleep, out, duration, rows)
            out("WATCH: %s" % r)
        set_z(0)
        out("END: Z 0, bias -0.5 V")
    finally:
        port.close()
        with open("release_watch_%d.csv" % int(t0), "w", newline="") as f:
            w = csv.writer(f); w.writerow(["t", "state", "onset_z"]); w.writerows(rows)
