"""Z throw of the rebuilt holder, and whether X and Y reach the gap.

Phase 1, repeated NPASS times: approach ONE motor step at a time (negative approaches), Z at 0
during every step. After each step sweep Z up from 0 to find the onset (|I| >= ONSET). At every
onset found, a slope scan: from onset-600 up in 25-count steps, 16 averaged reads each, until
|I| >= SLOPE_STOP or onset+1200. Pass ends when an onset is at/below ZLOW; then retract +RET
steps and check clear at Z 0.

Phase 2: approach until the onset lies in [ZMID_LO, ZMID_HI]; then find the onset at
X = mid, mid+DX, mid, mid-DX, mid and the same for Y, Z at 0 during every X/Y move.

Bounds: Z in [0, 50000], X/Y in [mid-DX, mid+DX]. Exit: Z 0, X/Y mid, bias 0 V, and a motor
retract if there is current at Z 0.
"""
import sys
import time
import statistics as st

ONSET, SLOPE_STOP, ZCAP, ZSTEP = 1000, 10000, 50000, 250
ZLOW, RET, MAXAPP = 8000, 6, 40
ZMID_LO, ZMID_HI = 12000, 40000
MID, DX = 32768, 10000


class Rig:
    def __init__(self, port):
        sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
        from stm_approach import Device
        from stm_feedback_scan import read_averaged
        self.d = Device(port)
        self._r = read_averaged

    def z(self, v):
        v = int(max(0, min(ZCAP, v)))
        self.d._write(("DACZ %d\n" % v).encode())
        time.sleep(0.001)

    def xy(self, axis, v):
        v = int(max(MID - DX, min(MID + DX, v)))
        self.d._write(("DAC%s %d\n" % (axis, v)).encode())
        time.sleep(0.02)

    def read(self):
        return self._r(self.d)

    def motor(self, n):
        self.d.move_motor(n)

    def bias(self, code):
        self.d._write(("BIAS %d\n" % code).encode())
        time.sleep(0.05)


def ts():
    return time.strftime("%H:%M:%S", time.gmtime())


def med(rig, n):
    v = [x for x in (rig.read() for _ in range(n)) if x is not None]
    return st.median(v) if v else 0.0


def onset(rig, step=ZSTEP):
    z = 0
    while z <= ZCAP:
        rig.z(z)
        if abs(med(rig, 4)) >= ONSET and abs(med(rig, 8)) >= ONSET:
            rig.z(0)
            return z
        z += step
    rig.z(0)
    return None


def slope_scan(rig, z_on, rows, tag):
    z = max(0, z_on - 600)
    pts = []
    while z <= min(ZCAP, z_on + 1200):
        rig.z(z)
        m = st.mean([x for x in (rig.read() for _ in range(16)) if x is not None] or [0])
        pts.append((z, m))
        rows.append((ts(), tag, z, round(m)))
        if abs(m) >= SLOPE_STOP:
            break
        z += 25
    rig.z(0)
    return pts


def clear_at_zero(rig):
    rig.z(0)
    return abs(med(rig, 32)) < 500


def main(rig, npass=3, log=print, rows=None):
    rows = [] if rows is None else rows
    rig.bias(38229)
    rig.z(0)
    result = {"passes": [], "xy": {}}
    try:
        for p in range(npass):
            onsets = []
            for s in range(MAXAPP + 1):
                z_on = onset(rig)
                if z_on is not None:
                    onsets.append((s, z_on))
                    pts = slope_scan(rig, z_on, rows, "p%d_s%d" % (p, s))
                    log("%s pass %d step -%d: onset Z %d | slope pts %s" % (
                        ts(), p, s, z_on,
                        " ".join("%d:%.0f" % q for q in pts[::4] + pts[-1:])))
                    if z_on <= ZLOW:
                        break
                if s < MAXAPP:
                    rig.z(0)
                    rig.motor(-1)
            result["passes"].append(onsets)
            rig.z(0)
            rig.motor(RET)
            extra = 0
            while not clear_at_zero(rig) and extra < 30:
                rig.motor(3)
                extra += 3
            log("%s pass %d done: onsets %s; retracted +%d" % (ts(), p, onsets, RET + extra))
        # phase 2
        z_on = None
        for s in range(MAXAPP + 1):
            z_on = onset(rig)
            if z_on is not None and z_on <= ZMID_HI:
                break
            rig.z(0)
            rig.motor(-1)
        if z_on is None or not (ZMID_LO <= z_on <= ZMID_HI):
            log("%s phase 2: onset %s not in the middle band; skipping X/Y" % (ts(), z_on))
        else:
            for axis in ("X", "Y"):
                seq = []
                for v in (MID, MID + DX, MID, MID - DX, MID):
                    rig.z(0)
                    rig.xy(axis, v)
                    seq.append((v - MID, onset(rig, step=100)))
                rig.z(0)
                rig.xy(axis, MID)
                result["xy"][axis] = seq
                log("%s %s offsets -> onset Z: %s" % (ts(), axis, seq))
    finally:
        rig.z(0)
        rig.xy("X", MID)
        rig.xy("Y", MID)
        if not clear_at_zero(rig):
            rig.motor(RET)
        rig.bias(32768)
        log("%s end: Z 0, X/Y mid, bias 0 V" % ts())
    return result, rows


if __name__ == "__main__":
    import serial
    npass = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    out = sys.argv[2] if len(sys.argv) > 2 else "zcal3.csv"
    port = serial.Serial("COM3", 115200, timeout=0.2)
    try:
        res, rows = main(Rig(port), npass, log=lambda s: print(s, flush=True))
    finally:
        port.close()
    with open(out, "w") as f:
        f.write("t,tag,z,mean\n")
        for r in rows:
            f.write("%s,%s,%s,%s\n" % r)
    print("wrote", out)
