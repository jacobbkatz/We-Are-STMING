"""Where is the gold, over a long quiet stretch? Every PERIOD s: read the current at Z 50000
(32 reads), then sweep DOWN in 250-count steps (16 reads, median) until |I| >= 1000; record the
onset Z (or none) and return to Z 50000 at once. Two-minute summaries. Bias -0.5 V.
Exit: Z 50000, bias 0 V. No motor."""
import sys, time, statistics as st
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
import serial
from stm_approach import Device, find_teensy
from stm_feedback_scan import read_averaged
SECS, PERIOD, OUT = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
p = serial.Serial(find_teensy(), 115200, timeout=0.2); d = Device(p); rows = []
ts = lambda: time.strftime("%H:%M:%S", time.gmtime())
def med(n):
    v = [x for x in (read_averaged(d) for _ in range(n)) if x is not None]; return st.median(v)
try:
    d._write(b"BIAS 38229\n"); time.sleep(0.1)
    t0 = time.time(); nxt = t0; rep_at = t0 + 120; chunk = []
    while time.time() - t0 < SECS:
        while time.time() < nxt: time.sleep(0.05)
        nxt += PERIOD
        d._write(b"DACZ 50000\n"); time.sleep(0.01)
        i_top = med(32)
        onset = None
        if abs(i_top) < 1000:
            for z in range(49750, -1, -250):
                d._write(("DACZ %d\n" % z).encode()); time.sleep(0.002)
                if abs(med(16)) >= 1000:
                    onset = z; break
        else:
            onset = 50000
        d._write(b"DACZ 50000\n")
        t = round(time.time() - t0, 1)
        rows.append((ts(), t, round(i_top), onset)); chunk.append((round(i_top), onset))
        if time.time() >= rep_at:
            print(ts(), "t=%4.0fs:" % t, " ".join("%s" % (o if o is not None else "-") for _, o in chunk),
                  "| I at Z50000:", " ".join(str(i) for i, _ in chunk), flush=True)
            chunk = []; rep_at += 120
finally:
    d._write(b"DACZ 50000\n"); time.sleep(0.02); d._write(b"BIAS 32768\n"); time.sleep(0.05); p.close()
    with open(OUT, "w") as f:
        f.write("utc,t,i_at_50000,onset_z\n")
        for r in rows: f.write("%s,%s,%s,%s\n" % r)
    print(ts(), "end: Z 50000, bias 0 V; %d cycles" % len(rows))
