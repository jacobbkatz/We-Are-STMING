import random, zcal3 as zc
random.seed(2)
class Fake:
    def __init__(self, s0, cps):
        self.s0, self.cps = s0, cps; self.m = 0; self.zv = 0; self.x = zc.MID; self.y = zc.MID
        self.b = 32768; self.zmax_seen = 0; self.xmax = 0; self.motor_total = 0; self.max_i = 0
    def z(self, v): self.zv = int(max(0, min(zc.ZCAP, v))); self.zmax_seen = max(self.zmax_seen, self.zv)
    def xy(self, a, v):
        v = int(max(zc.MID - zc.DX, min(zc.MID + zc.DX, v)))
        if a == "X": self.x = v
        else: self.y = v
        self.xmax = max(self.xmax, abs(v - zc.MID))
    def motor(self, n): self.m += n; self.motor_total += n
    def bias(self, c): self.b = c
    def surface(self): return self.s0 + self.cps * self.m - 0.17 * (self.x - zc.MID) + 0.05 * (self.y - zc.MID)
    def read(self):
        i = 3000 * 10 ** min((self.zv - self.surface()) / 500.0, 6)
        s = 1 if self.b == 38229 else (-1 if self.b == 27307 else 0)
        v = int(max(-32768, min(32767, s * i + random.gauss(0, 20))))
        self.max_i = max(self.max_i, abs(v)); return v
fails = []
for cps, s0 in ((20000, 90000), (250, 30000), (8000, 60000)):
    f = Fake(s0, cps); lines = []
    res, rows = zc.main(f, 3, log=lines.append)
    for l in lines: print("   ", l)
    p = res["passes"]
    ok = all(len(o) >= 1 for o in p)
    print("cps %d: passes %s, xy %s, zmax %d, motor net %d, final Z %d bias %d" % (cps, [len(o) for o in p], res["xy"], f.zmax_seen, f.motor_total, f.zv, f.b))
    if not ok: fails.append("cps %d: a pass found no onset" % cps)
    if f.zv != 0 or f.b != 32768 or f.x != zc.MID or f.y != zc.MID: fails.append("cps %d: bad final state" % cps)
    if f.xmax > zc.DX: fails.append("xy out of bounds")
    # per-step onset shift in pass 0
    o = p[0]
    if len(o) >= 2:
        d = [(o[i][1] - o[i+1][1]) / float(o[i+1][0] - o[i][0]) for i in range(len(o) - 1)]
        print("   measured Z counts per step:", d)
print("%d failure(s)" % len(fails)); raise SystemExit(1 if fails else 0)
