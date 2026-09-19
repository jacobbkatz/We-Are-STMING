"""At whatever junction is present: toggle Z (and X) by large amplitudes around midscale, 30
cycles each, 6 reads per state; report the current in each state and the difference. Bias -0.5 V.
Exit: Z midscale, X/Y midscale, bias 0 V. No motor."""
import sys, time, math, statistics as st
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
import serial
from stm_approach import Device, find_teensy
from stm_feedback_scan import read_averaged
OUT = sys.argv[1]
p = serial.Serial(find_teensy(), 115200, timeout=0.2); d = Device(p); rows = []
ts = lambda: time.strftime("%H:%M:%S", time.gmtime())
def w(s): d._write(s.encode()); time.sleep(0.003)
def med(n):
    v = [x for x in (read_averaged(d) for _ in range(n)) if x is not None]; return st.median(v)
try:
    w("BIAS 38229\n"); w("DACX 32768\n"); w("DACY 32768\n"); w("DACZ 32768\n"); time.sleep(0.1)
    print(ts(), "at midscale: %.0f counts" % med(64), flush=True)
    for axis, amps in (("Z", (2000, 8000, 20000)), ("X", (5000, 15000)), ("Z", (20000,))):
        for a in amps:
            lo, hi, df = [], [], []
            for c in range(30):
                w("DAC%s %d\n" % (axis, 32768 - a)); x1 = med(6)
                w("DAC%s %d\n" % (axis, 32768 + a)); x2 = med(6)
                lo.append(x1); hi.append(x2); df.append(x2 - x1)
                rows.append((round(time.time(), 3), axis, a, x1, x2))
            w("DAC%s 32768\n" % axis)
            m = st.mean(df); se = st.stdev(df) / math.sqrt(len(df))
            print(ts(), "%s +-%5d: I(-) %6.0f  I(+) %6.0f  diff %+7.0f +- %4.0f  (%.1f sigma)" % (
                axis, a, st.mean(lo), st.mean(hi), m, se, abs(m) / se if se else 0), flush=True)
    print(ts(), "at midscale again: %.0f counts" % med(64), flush=True)
finally:
    w("DACZ 32768\n"); w("DACX 32768\n"); w("DACY 32768\n"); w("BIAS 32768\n"); time.sleep(0.05); p.close()
    with open(OUT, "w") as f:
        f.write("t,axis,amp,i_minus,i_plus\n")
        for r in rows: f.write("%s,%s,%s,%s,%s\n" % r)
