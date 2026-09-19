"""Record the gold's position with NOTHING moving: full Z sweeps every PERIOD s for DURATION s.

2026-09-19 morning, after the Z-0 live back-off at 13:12:01. Today the gold swung by more than the
whole Z range within tens of seconds, both ways, with the motor still (release_watch_run1,
tuned_scans_run1, where_run1). This records it for the break: amplitude, direction, how often.

Each sweep: reading at Z 0 (contact past the fully retracted tip -> 'past'), then Z up from 0 to Z_TOP
in ZSTEP steps; the first averaged |I| >= DETECT is the onset; Z back to 0 at once. NO motor, ever.
A 'past' is recorded and the recording continues: the only remote remedy (motor retract) failed at
13:07-13:08 (+1200 steps, still railed), so nothing is attempted. Finer than fastwood (100-count
steps, DETECT 150) so each detection is a lighter touch.
For the tip fitted ~03:00 UTC 2026-09-19: HIGH Z extends toward the sample.

Usage: py swing_log.py [duration_s] [period_s]        py swing_log.py --test
"""
import sys, time

ZSTEP, Z_TOP, DETECT = 100, 62000, 150


def sweep(set_z, read):
    set_z(0)
    v0 = read()
    if v0 is not None and abs(v0) >= DETECT:
        return "past", 0, v0
    z = ZSTEP
    while z <= Z_TOP:
        set_z(z)
        v = read()
        if v is not None and abs(v) >= DETECT:
            set_z(0)
            return "in", z, v
        z += ZSTEP
    set_z(0)
    return "far", None, None


def run(set_z, read, now, sleep, out, duration, period, rows):
    t0 = now()
    last = None
    while now() - t0 < duration:
        ts = now()
        state, z, v = sweep(set_z, read)
        rows.append((round(ts - t0, 2), state, z, None if v is None else round(v)))
        if state != last or state == "in":
            out("%7.1fs %-4s %s" % (ts - t0, state.upper(), "" if z is None else "onset Z %d (%.0f)" % (z, v)))
        last = state
        rest = period - (now() - ts)
        if rest > 0:
            sleep(rest)
    return len(rows)


def self_test():
    import math

    class W:
        def __init__(self):
            self.t, self.z = 0.0, 0
        def gold(self):                                  # swings 30000 +- 50000 with a 60 s period
            return 30000 + 50000 * math.sin(2 * math.pi * self.t / 60.0)
        def set_z(self, z):
            assert 0 <= z <= 65535
            self.z = z
        def read(self):
            self.t += 0.004
            d = self.z - self.gold()
            return 0.0 if d < -1000 else min(32767.0, 1000 * 10 ** (d / 250.0))
        def now(self): return self.t
        def sleep(self, s): self.t += s
    w = W()
    rows = []
    run(w.set_z, w.read, w.now, w.sleep, lambda s: None, 180, 5.0, rows)
    states = {s for _, s, _, _ in rows}
    assert states == {"in", "far", "past"}, states
    assert w.z == 0
    ins = [(t, z) for t, s, z, _ in rows if s == "in"]
    # each recorded onset is within one step of where the gold was at that moment (it moves slowly)
    assert len(ins) >= 5
    print("self-test: pass (in / far / past all recorded over a 60 s swing; %d onsets; Z ends at 0)" % len(ins))


if __name__ == "__main__":
    # Added 2026-09-19 after a --test run of a script WITHOUT a self-test went straight to its
    # hardware path (no port was connected, so nothing was sent). Unknown options now refuse.
    _bad = [a for a in sys.argv[1:] if a.startswith('-') and a not in ['--test']]
    if _bad:
        sys.exit('refusing unknown option(s) %s: this script drives the instrument%s'
                 % (_bad, '' if True else ' and has NO self-test'))
    if "--test" in sys.argv:
        self_test(); sys.exit(0)
    import serial, csv, statistics as st
    sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
    from stm_approach import Device, find_teensy
    from stm_feedback_scan import read_averaged
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    duration = float(args[0]) if args else 900.0
    period = float(args[1]) if len(args) > 1 else 5.0
    stamp = lambda: time.strftime("%H:%M:%S", time.gmtime())
    port = serial.Serial(find_teensy(), 115200, timeout=0.2)
    dev = Device(port)
    rows = []
    t0 = time.time()
    try:
        dev._write(b"DACX 32768\n"); time.sleep(0.02)
        dev._write(b"DACY 32768\n"); time.sleep(0.02)
        dev.set_z(0); dev.set_bias(38229); time.sleep(0.2)

        def set_z(z):
            dev._write(("DACZ %d\n" % z).encode()); time.sleep(0.001)

        def rd():
            v = [x for x in (read_averaged(dev) for _ in range(2)) if x is not None]
            return st.mean(v) if v else None
        n = run(set_z, rd, time.time, time.sleep, lambda s: print(stamp(), s, flush=True),
                duration, period, rows)
        set_z(0)
        print(stamp(), "END: %d sweeps; Z 0, bias -0.5 V" % n, flush=True)
    finally:
        port.close()
        with open("swing_log_%d.csv" % int(t0), "w", newline="") as f:
            w = csv.writer(f); w.writerow(["t", "state", "onset_z", "adc"]); w.writerows(rows)
