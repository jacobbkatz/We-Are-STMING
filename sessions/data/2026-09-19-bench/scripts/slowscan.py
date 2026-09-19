"""From Z 50000 DOWN in 100-count steps (64 reads each) until |I| >= STOP, then back UP to
50000 in the same steps. REPS times. Bias -0.5 V. Exit: Z 50000, bias 0 V. No motor."""
import sys, time, math, statistics as st
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
import serial
from stm_approach import Device, find_teensy
from stm_feedback_scan import read_averaged
REPS, STOP, OUT = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
p = serial.Serial(find_teensy(), 115200, timeout=0.2); d = Device(p); rows = []
ts = lambda: time.strftime("%H:%M:%S", time.gmtime())
def rd(z, tag):
    d._write(("DACZ %d\n" % z).encode()); time.sleep(0.003)
    v = [x for x in (read_averaged(d) for _ in range(64)) if x is not None]
    m = st.mean(v); rows.append((round(time.time(), 3), tag, z, round(m))); return m
try:
    d._write(b"BIAS 38229\n"); time.sleep(0.1)
    for r in range(REPS):
        down = []
        z = 50000
        while z >= 0:
            m = rd(z, "down%d" % r); down.append((z, m))
            if abs(m) >= STOP: break
            z -= 100
        zlow = down[-1][0]
        up = [(zz, rd(zz, "up%d" % r)) for zz in range(zlow, 50001, 100)]
        def fmt(L):
            L = [(z, m) for z, m in L if abs(m) >= 100]
            return " ".join("%d:%.0f" % q for q in L[:25]) + (" ..." if len(L) > 25 else "") if L else "none over 100"
        print(ts(), "rep %d DOWN reached Z %d (last %.0f): %s" % (r, zlow, down[-1][1], fmt(down[-30:])), flush=True)
        print(ts(), "rep %d UP: %s" % (r, fmt(up[:30])), flush=True)
finally:
    d._write(b"DACZ 50000\n"); time.sleep(0.02); d._write(b"BIAS 32768\n"); time.sleep(0.05); p.close()
    with open(OUT, "w") as f:
        f.write("t,leg,z,mean\n")
        for row in rows: f.write("%s,%s,%s,%s\n" % row)
    print(ts(), "end: Z 50000, bias 0 V")
