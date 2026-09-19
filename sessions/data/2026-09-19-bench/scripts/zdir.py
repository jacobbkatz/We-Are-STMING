"""Which way does Z move this tip? Sweep Z down 50000 -> 0 and back up, repeated, at a gentle
bias, 32 averaged reads per point. A leg ends early (and turns round) if |I| passes CAP.
Nothing moves the motor. Exit: Z at the end of the last up-leg (50000), bias 0 V."""
import sys, time, statistics as st
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
import serial
from stm_approach import Device, find_teensy
from stm_feedback_scan import read_averaged
BIAS, CAP, REPS, OUT = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
p = serial.Serial(find_teensy(), 115200, timeout=0.2); d = Device(p)
rows = []
def rd(z, leg):
    d._write(("DACZ %d\n" % z).encode()); time.sleep(0.004)
    v = [x for x in (read_averaged(d) for _ in range(32)) if x is not None]
    m = st.mean(v); rows.append((round(time.time(), 3), leg, z, round(m))); return m
try:
    d._write(("BIAS %d\n" % BIAS).encode()); time.sleep(0.1)
    for r in range(REPS):
        down, up = [], []
        for z in range(50000, -1, -1000):
            m = rd(z, "down%d" % r); down.append((z, m))
            if abs(m) >= CAP: break
        zlow = down[-1][0]
        for z in range(zlow, 50001, 1000):
            m = rd(z, "up%d" % r); up.append((z, m))
        fmt = lambda L: " ".join("%d:%.0f" % (z // 1000, m) for z, m in L if abs(m) > 150) or "(nothing over 150)"
        print(time.strftime("%H:%M:%S", time.gmtime()), "rep %d DOWN (Z in thousands:counts) %s" % (r, fmt(down)), flush=True)
        print(time.strftime("%H:%M:%S", time.gmtime()), "rep %d UP   %s" % (r, fmt(up)), flush=True)
finally:
    d._write(b"DACZ 50000\n"); time.sleep(0.02); d._write(b"BIAS 32768\n"); time.sleep(0.05)
    p.close()
    with open(OUT, "w") as f:
        f.write("t,leg,z,mean\n")
        for row in rows: f.write("%s,%s,%s,%s\n" % row)
    print("end: Z 50000, bias 0 V")
