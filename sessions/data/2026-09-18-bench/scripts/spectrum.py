"""Noise spectrum of ADCR with the tip clear, by direct DFT on the real timestamps."""
import sys, time, math, cmath, serial, statistics as st
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
from stm_approach import Device
from stm_feedback_scan import read_averaged
secs = float(sys.argv[1]) if len(sys.argv) > 1 else 4
port = serial.Serial("COM3", 115200, timeout=0.2)
dev = Device(port)
ts, vs = [], []
t0 = time.perf_counter()
while time.perf_counter() - t0 < secs:
    v = read_averaged(dev)
    if v is not None:
        ts.append(time.perf_counter() - t0); vs.append(v)
port.close()
m = st.mean(vs); x = [v - m for v in vs]; n = len(x)
print(time.strftime("%H:%M:%S", time.gmtime()), "n=%d rate %.0f/s sd %.0f" % (n, n / secs, st.pstdev(vs)))
def amp(f):
    s = sum(xi * cmath.exp(-2j * math.pi * f * ti) for xi, ti in zip(x, ts))
    return 2 * abs(s) / n
freqs = list(range(2, 101, 1)) + [110, 120, 130, 150, 180, 200, 240, 300, 360, 420, 480, 500, 600, 700, 800, 900, 1000, 1200, 1500]
a = {f: amp(f) for f in freqs}
floor = st.median(a.values())
print("median line amplitude %.1f counts" % floor)
top = sorted(a.items(), key=lambda kv: -kv[1])[:10]
print("strongest lines:", ", ".join("%d Hz %.0f" % kv for kv in top))
bands = [(2, 10), (10, 30), (30, 100), (100, 400), (400, 1600)]
for lo, hi in bands:
    vals = [a[f] for f in freqs if lo <= f < hi]
    if vals: print("  %4d-%4d Hz: mean line amplitude %.1f (%d lines)" % (lo, hi, st.mean(vals), len(vals)))
