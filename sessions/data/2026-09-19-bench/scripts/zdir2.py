"""Down from Z 50000 toward LOW in 500-count steps until |I| >= 1000 (32 reads per point), then
back up to 50000 through the same points; at each onset a fine slope from onset+1000 down in
50-count steps, stopping at 5000. Repeated REPS times. Bias -0.5 V. Exit: Z 50000, bias 0 V."""
import sys, time, statistics as st
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
import serial
from stm_approach import Device, find_teensy
from stm_feedback_scan import read_averaged
REPS, OUT = int(sys.argv[1]), sys.argv[2]
p = serial.Serial(find_teensy(), 115200, timeout=0.2); d = Device(p); rows = []
def rd(z, tag, n=32):
    d._write(("DACZ %d\n" % z).encode()); time.sleep(0.004)
    v = [x for x in (read_averaged(d) for _ in range(n)) if x is not None]
    m = st.mean(v); rows.append((round(time.time(), 3), tag, z, round(m))); return m
ts = lambda: time.strftime("%H:%M:%S", time.gmtime())
try:
    d._write(b"BIAS 38229\n"); time.sleep(0.1)
    for r in range(REPS):
        onset = None
        for z in range(50000, -1, -500):
            m = rd(z, "down%d" % r)
            if abs(m) >= 1000:
                onset = z; break
        slope = []
        if onset is not None:
            z = min(50000, onset + 1000)
            while z >= max(0, onset - 1500):
                m = rd(z, "fine%d" % r); slope.append((z, round(m)))
                if abs(m) >= 5000: break
                z -= 50
        up = []
        start = onset if onset is not None else 0
        for z in range(start, 50001, 500):
            m = rd(z, "up%d" % r); up.append((z, round(m)))
        big_up = [(z, m) for z, m in up if abs(m) > 150]
        print(ts(), "rep %d: onset going DOWN at Z %s | fine: %s | going UP, points over 150: %s" % (
            r, onset, " ".join("%d:%d" % q for q in slope) if slope else "-",
            " ".join("%d:%d" % q for q in big_up) if big_up else "none"), flush=True)
        time.sleep(1.0)
finally:
    d._write(b"DACZ 50000\n"); time.sleep(0.02); d._write(b"BIAS 32768\n"); time.sleep(0.05); p.close()
    with open(OUT, "w") as f:
        f.write("t,tag,z,mean\n")
        for row in rows: f.write("%s,%s,%s,%s\n" % row)
    print("end: Z 50000, bias 0 V")
