"""Record the current at a FIXED Z for SECS seconds, every ADCR kept (for the rhythm of an
intermittent contact). Watchdog: 5 s continuously pinned -> Z to the other end, stop.
Bias -0.5 V. Exit: Z unchanged unless the watchdog fired, bias 0 V. No motor."""
import sys, time, math, cmath, statistics as st
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
import serial
from stm_approach import Device, find_teensy
from stm_feedback_scan import read_averaged
Z, SECS, OUT = int(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
p = serial.Serial(find_teensy(), 115200, timeout=0.2); d = Device(p)
t, v = [], []
try:
    d._write(b"BIAS 38229\n"); time.sleep(0.05)
    d._write(("DACZ %d\n" % Z).encode()); time.sleep(0.05)
    t0 = time.perf_counter(); pin_since = None
    while time.perf_counter() - t0 < SECS:
        x = read_averaged(d)
        if x is None: continue
        tt = time.perf_counter() - t0; t.append(tt); v.append(x)
        if abs(x) >= 32000:
            pin_since = pin_since if pin_since is not None else tt
            if tt - pin_since > 5:
                other = 50000 if Z < 32768 else 2000
                d._write(("DACZ %d\n" % other).encode()); print("pinned 5 s: Z ->", other); break
        else:
            pin_since = None
finally:
    d._write(b"BIAS 32768\n"); time.sleep(0.05); p.close()
    with open(OUT, "w") as f:
        f.write("t,value\n")
        for a, b in zip(t, v): f.write("%.5f,%d\n" % (a, b))
n = len(v); dur = t[-1]
print("n %d over %.1f s (%.0f/s) at Z %d: mean %.0f sd %.0f median %.0f" % (n, dur, n / dur, Z, st.mean(v), st.pstdev(v), st.median(v)))
for thr in (300, 1000, 5000, 32000):
    print("  fraction of time |I| >= %5d: %.3f" % (thr, sum(1 for x in v if abs(x) >= thr) / float(n)))
# contact events: rising crossings of 1000
ev = [t[i] for i in range(1, n) if abs(v[i]) >= 1000 > abs(v[i - 1])]
print("  rising crossings of 1000 counts: %d (%.2f per second)" % (len(ev), len(ev) / dur))
if len(ev) > 3:
    gaps = [b - a for a, b in zip(ev, ev[1:])]
    print("  interval between contacts: median %.3f s, 10th pct %.3f, 90th pct %.3f" % (
        st.median(gaps), sorted(gaps)[len(gaps) // 10], sorted(gaps)[9 * len(gaps) // 10]))
# spectrum of log-ish signal (clip) at a set of frequencies
m = st.mean(v); x = [a - m for a in v]
step = max(1, n // 20000); xs = x[::step]; tsx = t[::step]; nn = len(xs)
def amp(f): return 2 * abs(sum(a * cmath.exp(-2j * math.pi * f * b) for a, b in zip(xs, tsx))) / nn
fr = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 2, 2.5, 3, 3.5, 4, 5, 6, 7, 8, 10, 12, 15, 20, 25, 30, 40, 50, 60]
a = {f: amp(f) for f in fr}
print("  line amplitude (counts):", " ".join("%g:%.0f" % (f, a[f]) for f in fr))
