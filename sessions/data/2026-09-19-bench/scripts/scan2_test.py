"""scan2 against simulated junctions of BOTH directions, and the wrong sign must fail safe."""
import sys, math
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
import stm_feedback_scan as fs
import scan2
SET = 1000.0
class Fake:
    """current = SET * 10**(toward*(z - surface(x))/cpd)"""
    def __init__(s, toward, surface, cpd=100.0):
        s.toward, s.surface, s.cpd, s.z, s.x, s._port, s.zs = toward, surface, cpd, 30000, fs.MID, None, []
    def _write(s, frame):
        c = frame.decode().split()
        if c[0] == "DACZ": s.z = int(c[1]); s.zs.append(s.z)
        elif c[0] == "DACX": s.x = int(c[1])
    def read_adc(s, timeout=None):
        e = s.toward * (s.z - s.surface(s.x)) / s.cpd
        return int(max(-32768, min(32767, SET * 10 ** max(-6, min(6, e)))))
fails = []
def chk(c, m):
    print(("ok   " if c else "FAIL ") + m)
    if not c: fails.append(m)
fs.COUNTS_PER_DECADE = 100.0
for toward in (+1, -1):
    bump = lambda x: 30000 + (600 if abs(x - fs.MID) < 300 else 0)
    d = Fake(toward, bump)
    rows, loop = scan2.scan(d, toward, 1000, 100, 3, SET, log=lambda *a: None)
    chk(rows is not None, "toward %+d: found the surface" % toward)
    f = rows[1][1]; xs = list(range(fs.MID - 1000, fs.MID + 1001, 100))
    on = [z for x, z in zip(xs, f) if abs(x - fs.MID) < 300]; off = [z for x, z in zip(xs, f) if abs(x - fs.MID) > 500]
    got = sum(on) / len(on) - sum(off) / len(off)
    chk(abs(abs(got) - 600) < 250, "toward %+d: follows a 600-count bump (measured %.0f)" % (toward, got))
    chk(max(d.zs) <= fs.Z_MAX_SAFE + 2000 and min(d.zs) >= fs.Z_MIN_SAFE - 2000, "toward %+d: Z stayed in the window" % toward)
    chk(loop.clamped == 0 and loop.saturated <= 0.15 * 3 * 21 * 2 * fs.ITERS,
        "toward %+d: no clamp; saturation only at the bump's cliff edges (%d, %d)" % (toward, loop.clamped, loop.saturated))
    d = Fake(toward, lambda x: 30000)
    rows, loop = scan2.scan(d, toward, 1000, 100, 3, SET, log=lambda *a: None)
    zs = [v for _, f_, b_ in rows for v in f_ + b_]
    chk(loop.saturated == 0 and loop.clamped == 0 and max(zs) - min(zs) < 150,
        "toward %+d: holds a FLAT surface with no saturation (Z spread %d)" % (toward, max(zs) - min(zs)))
# the WRONG sign must run into a clamp and abort, not hold the current
d = Fake(-1, lambda x: 30000)
rows, loop = scan2.scan(d, +1, 1000, 100, 3, SET, log=lambda *a: None)
chk(rows is None or loop.clamped > 0 or loop.saturated > 0, "wrong sign: detected (clamped %s, saturated %s)" % (
    getattr(loop, "clamped", None), getattr(loop, "saturated", None)))
print("%d failure(s)" % len(fails)); raise SystemExit(1 if fails else 0)
