import math, time, random
import fasttrack as ft
random.seed(3)
class Fake:
    def __init__(self): self.zv = 0; self.t0 = time.perf_counter(); self.zmax = 0
    def s(self):
        t = time.perf_counter() - self.t0
        return 25000 + 7000 * math.sin(2 * math.pi * 5 * t) + 3000 * math.sin(2 * math.pi * 13 * t)
    def z(self, v): self.zv = int(max(0, min(ft.ZCAP, v))); self.zmax = max(self.zmax, self.zv); time.sleep(0.0003)
    def read(self):
        time.sleep(0.00027)
        return int(min(32767, 3000 * 10 ** min((self.zv - self.s()) / 50.0, 6) + random.gauss(0, 20)))
f = Fake()
smp = ft.track(f, 6.0)
print(ft.summary(smp))
sp = ft.spectrum(smp, list(range(1, 26)))
top = sorted(sp.items(), key=lambda kv: -kv[1])[:4]
print("top lines:", top)
ok = {5, 13} <= {k for k, _ in top[:3]}
print("PASS" if ok and f.zv == 0 else "FAIL")
raise SystemExit(0 if ok else 1)
