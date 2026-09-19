"""Watch the junction with NOTHING moving, and pull Z back if the gold creeps into hard contact.

2026-09-19 morning, straight after the live back-off (Z midscale, sample -0.5 V, gold just outside
detection). Holds whatever Z and bias are already set - sends no DAC command unless the watchdog
fires. Logs a line every LOG_EVERY s and every change of state; writes every reading to CSV.

For the tip fitted ~03:00 UTC 2026-09-19, LOW Z is retracted (sessions/2026-09-19-bench.md 3.14).
Watchdog: averaged |I| >= HARD -> Z down by BACK counts (never below 0), logged.
"""
import sys, time, statistics as st

HARD, ARRIVE, BACK, LOG_EVERY = 8000, 300, 12768, 30.0


def run(set_z, read, now, sleep, out, z0=32768, maxtime=1200, rows=None):
    z = z0
    t0 = now()
    arrived = False
    last_log = -1e9
    while now() - t0 < maxtime:
        v = [x for x in (read() for _ in range(20)) if x is not None]
        m = st.mean(v) if v else None
        t = now() - t0
        if rows is not None:
            rows.append((t, z, m))
        if m is not None and abs(m) >= HARD:
            nz = max(0, z - BACK)
            set_z(nz)
            out("%7.1fs Z %5d  %7.0f counts  WATCHDOG: Z -> %d" % (t, z, m, nz))
            z = nz
            continue
        if m is not None and not arrived and abs(m) >= ARRIVE:
            arrived = True
            out("%7.1fs Z %5d  %7.0f counts  ARRIVED (first reading over %d)" % (t, z, m, ARRIVE))
        if t - last_log >= LOG_EVERY:
            out("%7.1fs Z %5d  %7.0f counts" % (t, z, m if m is not None else float("nan")))
            last_log = t
        sleep(0.2)
    return z


def self_test():
    class World:
        def __init__(self, broken=False):
            self.t, self.z, self.broken = 0.0, 32768, broken
        def now(self): return self.t
        def sleep(self, s): self.t += s
        def set_z(self, z):
            assert 0 <= z <= 65535
            if not self.broken:
                self.z = z
        def read(self):
            self.t += 0.001
            gold = 30000 + 50 * self.t            # the gold creeps toward the tip, 50 counts/s
            gap = gold - self.z                   # contact when the tip (z) reaches the gold... reversed:
            # current rises as the tip gets within 2000 counts of the gold line
            depth = self.z - (gold - 2000)
            return 0 if depth < 0 else min(32767, 10 ** (depth / 250.0))
    w = World()
    run(w.set_z, w.read, w.now, w.sleep, lambda s: None, maxtime=300)
    assert w.z < 32768, "watchdog must retract when the gold arrives"
    w2 = World(broken=True)
    run(w2.set_z, w2.read, w2.now, w2.sleep, lambda s: None, maxtime=300)
    assert w2.z == 32768, "sanity: a broken DAC path leaves Z where it was"
    print("self-test: pass (watchdog retracts on arrival)")


if __name__ == "__main__":
    if "--test" in sys.argv:
        self_test(); sys.exit(0)
    import serial, csv
    sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
    from stm_approach import Device, find_teensy
    from stm_feedback_scan import read_averaged
    maxtime = float(sys.argv[1]) if len(sys.argv) > 1 else 1200
    stamp = lambda: time.strftime("%H:%M:%S", time.gmtime())
    port = serial.Serial(find_teensy(), 115200, timeout=0.2)
    dev = Device(port)
    rows = []
    try:
        z = run(lambda z: dev._write(("DACZ %d\n" % z).encode()), lambda: read_averaged(dev),
                time.time, time.sleep, lambda s: print(stamp(), s, flush=True), maxtime=maxtime, rows=rows)
        print(stamp(), "END: Z %d" % z, flush=True)
    finally:
        port.close()
        with open("creep_watch_%d.csv" % int(time.time()), "w", newline="") as f:
            w = csv.writer(f); w.writerow(["t_s", "z", "adc_mean20"]); w.writerows(rows)
