import random, lift, onset0 as o
random.seed(6)
class Fake:
    def __init__(s, zworks, per_step, slack):
        s.zworks, s.per, s.slack, s.m, s.z, s.code, s.maxv = zworks, per_step, slack, 0, 0, o.BZERO, 0
    def set_z(s, z): s.z = int(max(0, min(o.ZCAP, z)))
    def bias(s, c): s.code = c
    def motor(s, n): s.m += n
    def read(s):
        real = max(0, s.m - s.slack)            # retract steps that actually moved the plate
        gap = real * s.per - (s.z if s.zworks else 0) - 500   # surface 500 counts past Z 0 at start
        i = 1500 * 10 ** min(-gap / 250.0, 6) if gap > -2000 else 1500 * 10 ** 6
        sg = 1 if s.code == o.BNEG else (-1 if s.code == o.BPOS else 0)
        v = int(max(-32768, min(32767, sg * min(i, 3000) + random.gauss(0, 40))))
        s.maxv = max(s.maxv, abs(v)); return v
for zworks in (True, False):
    f = Fake(zworks, 20000, 5); lines = []
    run = o.Run(f, log=lines.append)
    try:
        t = lift.main(f, run, lines.append)
    except o.Abort as e:
        t = None; lines.append("ABORT %s" % e)
    print("Z works:" if zworks else "Z dead:")
    for l in lines: print("   ", l[:110])
    print("    final Z", f.z, "motor", f.m, "max read", f.maxv)
