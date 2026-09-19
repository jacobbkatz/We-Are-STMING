import random, time, onset0 as o
random.seed(5)
class Fake:
    def __init__(s, surf, cpd, drift=0.0):
        s.surf, s.cpd, s.drift, s.z, s.code, s.t0, s.maxv, s.zmax = surf, cpd, drift, 0, o.BZERO, time.time(), 0, 0
    def set_z(s, z): s.z = int(max(o.HOME, min(o.ZCAP, z))); s.zmax = max(s.zmax, s.z)
    def bias(s, c): s.code = c
    def read(s):
        surf = s.surf + s.drift * (time.time() - s.t0)
        i = 3000 * 10 ** min((s.z - surf) / s.cpd, 6)
        sg = {o.BNEG: 1, o.BPOS: -1}.get(s.code, 0)
        v = int(max(-32768, min(32767, sg * i + random.gauss(0, 150))))
        s.maxv = max(s.maxv, abs(v)); return v
fails = []
def chk(c, m):
    print(("ok   " if c else "FAIL ") + m)
    if not c: fails.append(m)
for surf, cpd in ((20000, 250), (20000, 40), (8000, 1500)):
    f = Fake(surf, cpd); r = o.Run(f, log=lambda *a: None)
    try:
        res = r.main(4)
    except o.Abort as e:
        res = {"abort": str(e)}
    zon = res.get("onset")
    chk("abort" not in res, "surf %d cpd %d: no abort (%s)" % (surf, cpd, res.get("abort")))
    chk(zon is not None and zon <= surf, "  onset %s at or before the surface" % zon)
    chk(f.maxv < o.SAT, "  never read past SAT (max %d)" % f.maxv)
    chk(f.z == o.HOME, "  ends at HOME (Z %d)" % f.z)
    fl = res.get("flip")
    chk(fl and fl[1][0][1] > 150 and fl[1][1][1] < -150, "  flip follows the sign")
# surface creeping in: must abort at the retract limit, Z home
f = Fake(3000, 250, drift=-2000.0); r = o.Run(f, log=lambda *a: None)
try:
    r.main(6); chk(False, "creeping surface must abort")
except o.Abort as e:
    chk("retract limit" in str(e) or "already" in str(e) or "past" in str(e), "creep -> abort: %s" % e)
chk(f.z == o.HOME, "  creep abort leaves Z at HOME (Z %d)" % f.z)
print("%d failure(s)" % len(fails)); raise SystemExit(1 if fails else 0)
