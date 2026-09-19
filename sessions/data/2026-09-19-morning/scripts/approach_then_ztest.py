"""Chunked motor approach, then the Z test IMMEDIATELY - no human or AI latency in between.

2026-09-19 morning. At 12:14:04 fastwood_run2 (20-step chunks) found the gold at Z 51000, but its
1000-count Z sweep met it already railed (31008 counts), and 30 s later - the time it took to read the
log and launch ztest by hand - the gold was pressed against the tip even at Z 0 (ztest_run2: STUCK).
Hands were off (SAID). So:
  1. the approach sweep is 4x finer (ZSTEP 250, DETECT 200): a lighter touch at detection;
  2. Z ramps up to (hit - BELOW) in RAMP-count steps (zjump_run1: a single 0->28000 jump put 3714
     counts on the next read, which ztest would take for contact);
  3. ztest.run starts at once from there.
Chunks of up to 20 motor steps: Jacob's OK, 12:13 UTC. NEGATIVE MTMV approaches; HIGH Z extends
toward the sample (tip fitted ~03:00 UTC 2026-09-19).

Usage: py approach_then_ztest.py [max_chunks] [cycles]        py approach_then_ztest.py --test
"""
import sys, time
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\sessions\data\2026-09-19-morning\scripts")
import fastwood, ztest

fastwood.ZSTEP, fastwood.DETECT = 250, 200
CHUNK, BELOW, RAMP = 20, 1500, 1000


def ramp(set_z, z_to):
    z = 0
    while z < z_to:
        z = min(z + RAMP, z_to)
        set_z(z)


def run(set_z, read, motor_chunk, now, sleep, out, max_chunks=400, cycles=30, rows_a=None, rows_z=None):
    res, n, z_hit = fastwood.run(set_z, read, motor_chunk, now, sleep, out, max_steps=max_chunks,
                                 rows=rows_a)
    if res != "found":
        return res, None
    z_start = max(0, z_hit - BELOW)
    out("found at Z %d -> ramp to %d and start the Z test NOW" % (z_hit, z_start))
    ramp(set_z, z_start)
    return "ztest", ztest.run(set_z, read, now, out, z_start=z_start, cycles=cycles, rows=rows_z)


def self_test():
    class W(ztest.World):
        def __init__(self, k, backlash, **kw):
            ztest.World.__init__(self, **kw)
            self.k, self.back, self.n, self.z = k, backlash, 0, 0
        def motor_chunk(self):
            for _ in range(CHUNK):
                self.n += 1
                if self.n > self.back:
                    self.gold0 -= self.k
            self.t += 0.8
        def sleep(self, s): self.t += s
    w = W(k=250, backlash=0, gold=150000, cpd=250.0)
    ra, rz = [], []
    res, zres = run(w.set_z, w.read1, w.motor_chunk, w.now, w.sleep, lambda s: None,
                    cycles=8, rows_a=ra, rows_z=rz)
    assert res == "ztest" and zres[0] == "done", (res, zres)
    s = ztest.analyse(rz, out=lambda s: None)
    assert abs(s["cpd_in_median"] - 250) < 50, s
    assert w.max_depth <= fastwood.ZSTEP + 50, "approach pressed %.0f past the gold" % w.max_depth
    # the ramp never jumps more than RAMP counts at a time
    zs = [0] + [r[3] for r in rz]
    print("self-test: pass (found, ramped, Z test done with cpd %.0f; press <= one 250-count step)"
          % s["cpd_in_median"])


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
    mx = int(args[0]) if args else 400
    cyc = int(args[1]) if len(args) > 1 else 30
    stamp = lambda: time.strftime("%H:%M:%S", time.gmtime())
    out = lambda s: print(stamp(), s, flush=True)
    port = serial.Serial(find_teensy(), 115200, timeout=0.2)
    dev = Device(port)
    t0 = time.time()
    ra, rz = [], []
    try:
        dev._write(b"DACX 32768\n"); time.sleep(0.02)
        dev._write(b"DACY 32768\n"); time.sleep(0.02)
        dev.set_z(0)
        dev.set_bias(38229); time.sleep(0.2)

        def set_z(z):
            dev._write(("DACZ %d\n" % z).encode()); time.sleep(0.002)
        res, zres = run(set_z, lambda: read_averaged(dev), lambda: dev.move_motor(-CHUNK),
                        lambda: time.time() - t0, time.sleep, out, max_chunks=mx, cycles=cyc,
                        rows_a=ra, rows_z=rz)
        set_z(0)
        out("RESULT: %s %s; Z left at 0, bias -0.5 V" % (res, zres))
    finally:
        port.close()
        tag = int(t0)
        with open("apz_approach_%d.csv" % tag, "w", newline="") as f:
            w = csv.writer(f); w.writerow(["t", "chunks", "z_hit", "adc"]); w.writerows(ra)
        with open("apz_ztest_%d.csv" % tag, "w", newline="") as f:
            w = csv.writer(f); w.writerow(["t", "cycle", "phase", "z", "adc"]); w.writerows(rz)
    if rz:
        ztest.analyse(rz, out=out)
