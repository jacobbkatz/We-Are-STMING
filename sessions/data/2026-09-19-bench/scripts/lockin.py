"""Z direction by lock-in: toggle Z between Zc-D and Zc+D, reading the current in each state.
Slow creep moves both states together and cancels in the difference. Picks Zc where the
current is moderate. Bias -0.5 V. Exit: Z at the end that read LOWER current, bias 0 V."""
import sys, time, math, statistics as st
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
import serial
from stm_approach import Device, find_teensy
from stm_feedback_scan import read_averaged
OUT = sys.argv[1]
p = serial.Serial(find_teensy(), 115200, timeout=0.2); d = Device(p); rows = []
ts = lambda: time.strftime("%H:%M:%S", time.gmtime())
def setz(z): d._write(("DACZ %d\n" % z).encode()); time.sleep(0.004)
def rd(n): 
    v = [x for x in (read_averaged(d) for _ in range(n)) if x is not None]; return st.mean(v) if v else 0.0
park = 32768
try:
    d._write(b"BIAS 38229\n"); time.sleep(0.1)
    survey = []
    for z in (10000, 16000, 22000, 28000, 32768, 38000, 44000, 50000):
        setz(z); survey.append((z, rd(32)))
    print(ts(), "survey:", " ".join("%d:%.0f" % s for s in survey), flush=True)
    cands = [s for s in survey if 300 <= abs(s[1]) <= 15000]
    if not cands:
        print(ts(), "no moderate current anywhere; nothing to lock onto", flush=True)
    else:
        zc = min(cands, key=lambda s: abs(abs(s[1]) - 3000))[0]
        for D in (1000, 3000):
            if zc - D < 0 or zc + D > 65535: continue
            diffs, lo_all, hi_all = [], [], []
            for c in range(60):
                setz(zc - D); a = rd(6)
                setz(zc + D); b = rd(6)
                diffs.append(b - a); lo_all.append(a); hi_all.append(b)
                rows.append((round(time.time(), 3), zc, D, round(a), round(b)))
            md = st.mean(diffs); se = st.pstdev(diffs) / math.sqrt(len(diffs))
            lo, hi = st.mean(lo_all), st.mean(hi_all)
            dec = math.log10(abs(hi) / abs(lo)) if lo and hi and lo * hi > 0 else float("nan")
            print(ts(), "Zc %d, D %d: I(Zc-D) %.0f  I(Zc+D) %.0f  diff %.0f +- %.0f  -> %.2f decades per %d counts" % (
                zc, D, lo, hi, md, se, dec, 2 * D), flush=True)
            park = zc - 20000 if hi > lo else zc + 20000
finally:
    park = max(0, min(65535, park))
    setz(park); d._write(b"BIAS 32768\n"); time.sleep(0.05); p.close()
    with open(OUT, "w") as f:
        f.write("t,zc,d,i_low,i_high\n")
        for r in rows: f.write("%s,%s,%s,%s,%s\n" % r)
    print(ts(), "end: Z parked at %d (the side that read less current), bias 0 V" % park)
