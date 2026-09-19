"""After an approach: let the mechanics settle with NOTHING moving, then record a junction.

Args: z_retract (the end that pulls away), wait_s, record_s, out.csv
1. Hold Z at z_retract, -0.5 V, for wait_s; one 64-read mean per second (current at the retract end).
2. Sweep from z_retract toward the other end in 250-count steps (16 reads) until |I| >= 1000.
   If nothing is found, report and stop. Back off 500 counts from that point: Z_hold.
3. Record every ADCR at Z_hold for record_s with timestamps. Watchdog: if 2000 consecutive
   reads are pinned (>= 32000), go to z_retract and end.
Exit: Z at z_retract, bias 0 V. No motor.
"""
import sys, time, statistics as st
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
import serial
from stm_approach import Device, find_teensy
from stm_feedback_scan import read_averaged

ZR, WAIT, REC, OUT = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
toward = -1 if ZR > 32768 else 1
p = serial.Serial(find_teensy(), 115200, timeout=0.2)
d = Device(p)
rows = []
ts = lambda: time.strftime("%H:%M:%S", time.gmtime())


def setz(z):
    d._write(("DACZ %d\n" % z).encode())
    time.sleep(0.003)


try:
    d._write(b"BIAS 38229\n"); time.sleep(0.1)
    setz(ZR)
    t0 = time.time()
    waits = []
    while time.time() - t0 < WAIT:
        v = [x for x in (read_averaged(d) for _ in range(64)) if x is not None]
        waits.append((round(time.time() - t0, 1), round(st.mean(v))))
        rows.append((time.time(), "wait", ZR, round(st.mean(v))))
        time.sleep(max(0, 1.0 - 0.02))
    print(ts(), "1. at Z %d for %.0f s: current (s:counts) %s" % (
        ZR, WAIT, " ".join("%.0f:%d" % w for w in waits[::10] + waits[-1:])), flush=True)
    onset = None
    z = ZR
    while 0 <= z <= 65535 and abs(z - ZR) <= 50000:
        setz(z)
        v = [x for x in (read_averaged(d) for _ in range(16)) if x is not None]
        if abs(st.median(v)) >= 1000:
            onset = z
            break
        z += toward * 250
    if onset is None:
        print(ts(), "2. no current anywhere toward the gold from Z %d" % ZR, flush=True)
    else:
        zh = onset - toward * 500
        setz(zh)
        print(ts(), "2. onset at Z %d; holding at Z %d" % (onset, zh), flush=True)
        t1 = time.perf_counter()
        pinned = 0
        vals = []
        while time.perf_counter() - t1 < REC:
            x = read_averaged(d)
            if x is None:
                continue
            tt = time.perf_counter() - t1
            rows.append((round(tt, 5), "rec", zh, x))
            vals.append(x)
            pinned = pinned + 1 if abs(x) >= 32000 else 0
            if pinned >= 2000:
                print(ts(), "   pinned for 2000 reads: retracting", flush=True)
                break
        n = len(vals)
        k = max(1, n // 12)
        seg = [round(st.mean(vals[i:i + k])) for i in range(0, n - k + 1, k)]
        print(ts(), "3. %d reads over %.0f s at Z %d: mean %.0f sd %.0f; means per ~%.0f s: %s" % (
            n, REC, zh, st.mean(vals), st.pstdev(vals), REC / 12.0, " ".join(str(s) for s in seg)), flush=True)
finally:
    setz(ZR)
    d._write(b"BIAS 32768\n"); time.sleep(0.05)
    p.close()
    with open(OUT, "w") as f:
        f.write("t,tag,z,value\n")
        for r in rows:
            f.write("%s,%s,%s,%s\n" % r)
    print(ts(), "end: Z %d, bias 0 V; wrote %s" % (ZR, OUT))
