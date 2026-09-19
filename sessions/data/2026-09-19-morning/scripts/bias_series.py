"""The Z test at several biases back to back: is the snap / stickiness driven by the bias?

2026-09-19 morning. ztest_run3 (12:56-12:58, sample -0.5 V) gave ~1,650 counts per decade going in,
~3,440 coming out, ~1,160 counts of in/out hysteresis and 14 snaps in 30 cycles - a soft, sticky
contact. The electrostatic pull on the leaf goes as V^2 (V the tip-sample potential difference,
including the W/Au contact potential, which is unmeasured), so if the leaf is being PULLED:
  lower |bias| -> fewer snaps, less hysteresis, and a steeper, more tunnelling-like curve.
If nothing changes with bias, the soft element is mechanical, not electrostatic.

Runs ztest.run once per bias in BIASES, each starting BELOW counts under the previous run's last
onset, with no delay between runs (the gold drifts ~74 counts/s). ztest's own safety applies
throughout (watchdog, lost, stuck). Stops the series on 'lost', 'stuck' or 'error'.
Bias codes: 32768 = 0 V; 5461 counts per 0.5 V; ABOVE midscale = sample NEGATIVE.

Usage: py bias_series.py <start_z> [cycles]        py bias_series.py --test
"""
import sys, time
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\sessions\data\2026-09-19-morning\scripts")
import ztest

BIASES = [("-0.1 V", 33860), ("+0.5 V", 27307), ("+0.1 V", 31676), ("-0.5 V", 38229)]
BELOW = 4000


def series(set_bias, set_z, read, now, out, z_start, cycles=20, rows_by=None):
    rows_by = rows_by if rows_by is not None else {}
    z = z_start
    results = []
    for name, code in BIASES:
        set_bias(code)
        rows = rows_by.setdefault(name, [])
        out("==== bias %s (code %d), start Z %d ====" % (name, code, z))
        status, zend = ztest.run(set_z, read, now, out, z_start=z, cycles=cycles, rows=rows)
        s = ztest.analyse(rows, out=out)
        results.append((name, status, s))
        if status in ("lost", "stuck", "error"):
            out("series stopped: %s at bias %s" % (status, name))
            break
        last = s.get("onset_last") or zend
        z = max(0, int(last) - BELOW)
        set_z(z)
    return results


def self_test():
    w = ztest.World(gold=40000, cpd=250.0)
    biases = []
    res = series(lambda c: biases.append(c), w.set_z, w.read1, w.now, lambda s: None, 35000, cycles=6)
    assert [b for b in biases] == [c for _, c in BIASES], biases
    assert all(st_ == "done" for _, st_, _ in res) and len(res) == len(BIASES), res
    for name, st_, s in res:
        assert abs(s["cpd_in_median"] - 250) < 60, (name, s)
    # a 'stuck' world stops the series at the first bias
    w = ztest.World(gold=-5000, cpd=250.0)
    res = series(lambda c: None, w.set_z, w.read1, w.now, lambda s: None, 3000, cycles=4)
    assert len(res) == 1 and res[0][1] == "stuck", res
    print("self-test: pass (four biases chained, each measured; a stuck run stops the series)")


if __name__ == "__main__":
    if "--test" in sys.argv:
        self_test(); sys.exit(0)
    import serial, csv
    sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
    from stm_approach import Device, find_teensy
    from stm_feedback_scan import read_averaged
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    z_start = int(args[0])
    cycles = int(args[1]) if len(args) > 1 else 20
    stamp = lambda: time.strftime("%H:%M:%S", time.gmtime())
    out = lambda s: print(stamp(), s, flush=True)
    port = serial.Serial(find_teensy(), 115200, timeout=0.2)
    dev = Device(port)
    t0 = time.time()
    rows_by = {}
    try:
        dev._write(b"DACX 32768\n"); time.sleep(0.02)
        dev._write(b"DACY 32768\n"); time.sleep(0.02)

        def set_z(z):
            dev._write(("DACZ %d\n" % z).encode()); time.sleep(0.002)
        # gentle ramp from 0 (zjump_run1: big jumps spike the next read)
        dev.set_z(0); time.sleep(0.05)
        for z in range(1000, z_start + 1, 1000):
            set_z(z)
        res = series(lambda c: (dev.set_bias(c), time.sleep(0.2)), set_z, lambda: read_averaged(dev),
                     lambda: time.time() - t0, out, z_start, cycles=cycles, rows_by=rows_by)
        set_z(0)
        dev.set_bias(38229)
        out("END: Z 0, bias -0.5 V")
        out("SERIES SUMMARY:")
        for name, st_, s in res:
            out("  %-7s %-5s cpd_in %s  cpd_out %s  hyst %s  snaps %s  drift %s  cycles %s" % (
                name, st_, s.get("cpd_in_median"), s.get("cpd_out_median"), s.get("hyst_median"),
                s.get("snaps"), s.get("drift_counts_per_s"), s.get("cycles")))
    finally:
        port.close()
        for name, rows in rows_by.items():
            tag = name.replace(" ", "").replace("+", "p").replace("-", "m").replace(".", "")
            with open("bias_%s_%d.csv" % (tag, int(t0)), "w", newline="") as f:
                w = csv.writer(f); w.writerow(["t", "cycle", "phase", "z", "adc"]); w.writerows(rows)
