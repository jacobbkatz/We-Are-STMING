"""Measure the junction that is present at Z 0, before anything moves.

1. 10 s record at Z 0, sample -0.5 V, every ADCR kept with a timestamp (spectrum later)
2. bias flip at Z 0
3. I-V at Z 0: -1.0 .. +1.0 V in 0.1 V steps, 32 reads each, interleaved order
4. slope: Z up from 0 in 10-count steps, 32 reads each, stop at |I| >= 5000
Watchdog: any read >= 30000 in magnitude pulls Z to 0 and ends the step that caused it.
Exit: Z 0, bias 0 V. The motor is never touched here.
"""
import sys
import time
import statistics as st
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
import serial
from stm_approach import Device, find_teensy
from stm_feedback_scan import read_averaged

PIN = 30000
out_prefix = sys.argv[1]
port = serial.Serial(find_teensy(), 115200, timeout=0.2)
dev = Device(port)
rows = []


def w(s):
    dev._write(s.encode())
    time.sleep(0.02)


def reads(n, tag, z, b):
    v = []
    for _ in range(n):
        x = read_averaged(dev)
        if x is None:
            continue
        rows.append((round(time.perf_counter() - T0, 5), tag, z, b, x))
        v.append(x)
    return v


T0 = time.perf_counter()
try:
    w("DACZ 0\n"); w("BIAS 38229\n"); time.sleep(0.2)
    # 1. record
    v = reads(35000, "rec", 0, 38229)
    print(time.strftime("%H:%M:%S", time.gmtime()), "1. Z 0, -0.5 V, 10 s: n %d mean %.0f sd %.0f min %d max %d"
          % (len(v), st.mean(v), st.pstdev(v), min(v), max(v)), flush=True)
    # 2. flip
    res = []
    for code, name in ((38229, "-0.5"), (27307, "+0.5"), (32768, "0"), (38229, "-0.5")):
        w("BIAS %d\n" % code); time.sleep(0.1)
        v = reads(256, "flip", 0, code)
        res.append("%s V %.0f" % (name, st.mean(v)))
    print(time.strftime("%H:%M:%S", time.gmtime()), "2. flip at Z 0:", " | ".join(res), flush=True)
    # 3. I-V, interleaved so drift cannot fake a slope
    volts = [round(-1.0 + 0.1 * i, 1) for i in range(21)]
    order = volts[0::2] + volts[1::2]
    iv = {}
    for vv in order:
        code = int(round(32768 - vv * 5461 / 0.5))   # sample volts -> BIAS code (38229 = -0.5 V)
        w("BIAS %d\n" % code); time.sleep(0.03)
        v = reads(32, "iv", 0, code)
        iv[vv] = st.mean(v)
    w("BIAS 38229\n")
    print(time.strftime("%H:%M:%S", time.gmtime()), "3. I-V at Z 0 (sample V: counts):",
          " ".join("%+.1f:%.0f" % (k, iv[k]) for k in volts), flush=True)
    # 4. slope
    pts = []
    z = 0
    while z <= 3000:
        w("DACZ %d\n" % z)
        v = reads(32, "slope", z, 38229)
        m = st.mean(v)
        pts.append((z, m))
        if abs(m) >= 5000 or max(abs(x) for x in v) >= PIN:
            break
        z += 10
    w("DACZ 0\n")
    print(time.strftime("%H:%M:%S", time.gmtime()), "4. slope from Z 0:",
          " ".join("%d:%.0f" % p for p in pts[::2] + pts[-1:]), flush=True)
finally:
    w("DACZ 0\n"); w("BIAS 32768\n")
    port.close()
    with open(out_prefix + ".csv", "w") as f:
        f.write("t,tag,z,bias,value\n")
        for r in rows:
            f.write("%s,%s,%s,%s,%s\n" % r)
    print("end: Z 0, bias 0 V; wrote %s.csv (%d rows)" % (out_prefix, len(rows)))
