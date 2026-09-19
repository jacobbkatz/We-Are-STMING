"""Constant-current scans with the loop constant MEASURED today, each followed by an X-held control.

2026-09-19 morning. The Z test measured this junction at ~1,650-1,970 counts per decade going in
at sample -0.5 V (ztest_run3, bias_series_run1). The 2026-09-19 bench scans ran the loop with
COUNTS_PER_DECADE = 100: each correction was ~18x too small for this junction, which fits the lag
and hunting found in those images. This is the first scan with the constant measured on the
junction being scanned.

Uses sessions/data/2026-09-19-bench/scripts/scan2.py (tested: scan2_test.py) unchanged, with
fs.COUNTS_PER_DECADE set to CPD. For each size in SIZES, REPS times: a real scan, then an X-held
control with identical timing. Z back to the retracted end between images. HIGH Z extends toward
the sample for the tip fitted ~03:00 UTC 2026-09-19 (toward = +1).

Usage: py tuned_scans.py            py tuned_scans.py --test
"""
import sys, time
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\sessions\data\2026-09-19-bench\scripts")
import stm_feedback_scan as fs
import scan2

CPD = 1800.0
SETPOINT = 1000.0
TOWARD = +1
SIZES = [("s3k", 3000, 300), ("w15k", 15000, 1500)]
NLINES, REPS = 11, 3


def write_csv(path, half, step, rows):
    with open(path, "w") as f:
        f.write("y,dir," + ",".join(str(x) for x in range(fs.MID - half, fs.MID + half + 1, step)) + "\n")
        for y, fwd, back in rows:
            f.write("%d,fwd,%s\n" % (y, ",".join(str(v) for v in fwd)))
            f.write("%d,back,%s\n" % (y, ",".join(str(v) for v in back)))


def run(dev, out, prefix="tuned"):
    fs.COUNTS_PER_DECADE = CPD
    done = []
    for tag, half, step in SIZES:
        for r in range(REPS):
            for kind, xheld in (("scan", False), ("xheld", True)):
                t0 = time.time()
                rows, loop = scan2.scan(dev, TOWARD, half, step, NLINES, SETPOINT, xheld=xheld, log=out)
                dev._write(("DACZ %d\n" % scan2.retracted_end(TOWARD)).encode())
                dev._write(("DACX %d\n" % fs.MID).encode())
                if rows is None:
                    out("%s %s%d: no junction in reach" % (tag, kind, r))
                    continue
                path = "%s_%s_%s%d.csv" % (prefix, tag, kind, r)
                write_csv(path, half, step, rows)
                zs = [v for _, f_, b_ in rows for v in f_ + b_]
                out("%s %s%d: %d lines %.1f s, Z %d..%d, saturated %d, clamped %d, lost %d -> %s" % (
                    tag, kind, r, len(rows), time.time() - t0, min(zs), max(zs), loop.saturated,
                    loop.clamped, loop.lost, path))
                done.append(path)
                time.sleep(0.2)
    return done


def self_test():
    import math

    class Fake:
        def __init__(s, surface, cpd):
            s.surface, s.cpd, s.z, s.x, s._port = surface, cpd, 30000, fs.MID, None
        def _write(s, frame):
            c = frame.decode().split()
            if c[0] == "DACZ": s.z = int(c[1])
            elif c[0] == "DACX": s.x = int(c[1])
        def read_adc(s, timeout=None):
            e = (s.z - s.surface(s.x)) / s.cpd
            return int(max(-32768, min(32767, SETPOINT * 10 ** max(-6, min(6, e)))))
    bump = lambda x: 30000 + (1500 if abs(x - fs.MID) < 600 else 0)
    xs = list(range(fs.MID - 3000, fs.MID + 3001, 300))

    def follow(cpd_loop):
        fs.COUNTS_PER_DECADE = cpd_loop
        d = Fake(bump, 1800.0)
        rows, loop = scan2.scan(d, TOWARD, 3000, 300, 3, SETPOINT, log=lambda *a: None)
        f = rows[1][1]
        on = [z for x, z in zip(xs, f) if abs(x - fs.MID) < 600]
        off = [z for x, z in zip(xs, f) if abs(x - fs.MID) > 1200]
        return sum(on) / len(on) - sum(off) / len(off)
    good = follow(CPD)
    bad = follow(100.0)
    assert abs(good - 1500) < 400, "tuned loop must follow a 1500-count bump (got %.0f)" % good
    assert abs(bad - 1500) > 600, "the old constant should visibly fail to follow (got %.0f)" % bad
    fs.COUNTS_PER_DECADE = CPD
    print("self-test: pass (tuned loop follows the bump: %.0f of 1500; old 100/decade: %.0f)" % (good, bad))


if __name__ == "__main__":
    # Added 2026-09-19 after a --test run of a script WITHOUT a self-test went straight to its
    # hardware path (no port was connected, so nothing was sent). Unknown options now refuse.
    _bad = [a for a in sys.argv[1:] if a.startswith('-') and a not in ['--test']]
    if _bad:
        sys.exit('refusing unknown option(s) %s: this script drives the instrument%s'
                 % (_bad, '' if True else ' and has NO self-test'))
    if "--test" in sys.argv:
        self_test(); sys.exit(0)
    import serial
    from stm_approach import Device, find_teensy
    stamp = lambda: time.strftime("%H:%M:%S", time.gmtime())
    out = lambda s: print(stamp(), s, flush=True)
    port = serial.Serial(find_teensy(), 115200, timeout=0.2)
    dev = Device(port)
    try:
        dev._write(("DACZ %d\n" % scan2.retracted_end(TOWARD)).encode())
        dev._write(("DACX %d\n" % fs.MID).encode())
        dev._write(("DACY %d\n" % fs.MID).encode())
        dev._write(("BIAS %d\n" % scan2.BIAS).encode())
        time.sleep(0.2)
        files = run(dev, out)
        out("DONE: %d images" % len(files))
    finally:
        dev._write(("DACZ %d\n" % scan2.retracted_end(TOWARD)).encode())
        dev._write(("DACX %d\n" % fs.MID).encode())
        dev._write(("DACY %d\n" % fs.MID).encode())
        time.sleep(0.05)
        port.close()
        print(stamp(), "end: Z retracted, X/Y mid, bias left at -0.5 V", flush=True)
