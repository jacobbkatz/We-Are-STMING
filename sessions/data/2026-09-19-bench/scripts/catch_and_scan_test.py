import sys, math, random
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
import stm_feedback_scan as fs, scan2, creeptrack2, catch_and_scan as cs
random.seed(8); fs.COUNTS_PER_DECADE = 100.0
class World:
    """Surface creeps toward the tip at `rate` counts/s from far away; `toward` = which Z end extends."""
    def __init__(w, toward, rate=400.0):
        w.toward, w.rate, w.t, w.z, w.x, w._port, w.bias = toward, rate, 0.0, cs.MID, fs.MID, None, 32768
        w.surface0 = cs.MID + toward * 60000          # far out of reach at the start
        w.zs = []
    def surf(w, x): return w.surface0 - w.toward * w.rate * w.t + (300 if abs(x - fs.MID) < 300 else 0) * w.toward
    # run() interface
    def set_z(w, z): w.z = int(z); w.t += 0.002; w.zs.append(w.z)
    def set_bias(w, c): w.bias = c
    def motor(w, n): pass
    # scan2 / fs interface
    def _write(w, frame):
        c = frame.decode().split(); w.t += 0.0003
        if c[0] == "DACZ": w.z = int(c[1]); w.zs.append(w.z)
        elif c[0] == "DACX": w.x = int(c[1])
    def read_adc(w, timeout=None):
        w.t += 0.0003
        e = w.toward * (w.z - w.surf(w.x)) / 100.0
        return int(max(-32768, min(32767, 1000 * 10 ** max(-6, min(6, e))) + random.gauss(0, 20)))
    def med(w, n):
        v = sorted(w.read_adc() for _ in range(n)); return v[len(v) // 2]
    def now(w): return w.t
    def sleep(w, d): w.t += d
for toward in (+1, -1):
    w = World(toward); lines = []
    got, scans = cs.run(w, w.med, creeptrack2.lockin,
                        lambda dev, tw, xh: scan2.scan(w, tw, 1500, 150, 11, 1000.0, xheld=xh, log=lambda *a: None),
                        w.now, w.sleep, lines.append, secs=600, period=3, reps=2)
    ok = got == toward and len(scans) >= 2
    print("toward %+d: decided %s, %d scans -> %s" % (toward, got, len(scans), "ok" if ok else "FAIL"))
    for l in lines[:4]: print("    ", l)
