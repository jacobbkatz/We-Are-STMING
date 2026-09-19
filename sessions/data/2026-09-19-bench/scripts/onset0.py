"""Piezo-only characterisation after the hand-set of 2026-09-19 (UTC). No motor.

The hand-set touched at Z 10000 and was clear at Z 0, so the surface is inside the Z range and
HOME is now 0 (fully retracted; the HIGH end extends toward the sample, 2026-09-17/18).

  A. baseline at Z 0, sample -0.5 V. Abort if current is already there.
  B. onset: creep Z up from 0 in 50-count steps; stop at |median| >= ONSET (300 counts, ~0.9 nA)
  C. slope: from onset-1000 in 10-count steps, 32 reads each, stop at STOPC (5000, ~16 nA)
  D. bias flip at the Z where |I| was nearest 1500: -0.5, +0.5, 0, -0.5 V
  E. drift: re-find the onset every ~2 s for DRIFT s, climbing from last-2000
Any single read at or past SAT (20000) pulls Z to 0 at once. Exit: Z 0, bias 0 V.
"""
import sys
import time
import statistics as st

HOME, ZCAP = 0, 50000
ONSET, STOPC, SAT = 300, 5000, 20000
BNEG, BPOS, BZERO = 38229, 27307, 32768


class Abort(Exception):
    pass


class Run:
    def __init__(self, rig, log=print):
        self.rig, self.log, self.rows = rig, log, []
        self.t0 = time.time()

    def reads(self, n, tag, bias=BNEG):
        out = []
        for _ in range(n):
            v = self.rig.read()
            if v is None:
                continue
            self.rows.append((round(time.time() - self.t0, 4), tag, self.rig.z, bias, v))
            if abs(v) >= SAT:
                self.rig.set_z(HOME)
                raise Abort("read %d at Z %d: past %d, Z pulled to %d" % (v, self.rows[-1][2], SAT, HOME))
            out.append(v)
        return out

    def onset(self, z_from, step=50, tag="onset"):
        z = max(HOME, z_from)
        while z <= ZCAP:
            self.rig.set_z(z)
            v = self.reads(16, tag)
            if v and abs(st.median(v)) >= ONSET:
                w = self.reads(32, tag)
                if w and abs(st.median(w)) >= ONSET:
                    return z
            z += step
        return None

    def main(self, drift_s):
        res = {}
        self.rig.bias(BNEG)
        self.rig.set_z(HOME)
        time.sleep(0.3)
        b = self.reads(400, "base")
        res["base"] = (st.mean(b), st.pstdev(b))
        self.log("A. Z %d, -0.5 V: mean %.0f sd %.0f" % (HOME, res["base"][0], res["base"][1]))
        if abs(res["base"][0]) > 200:
            self.rig.bias(BZERO)
            raise Abort("current already at Z %d (mean %.0f): back the screws off a hair" % (HOME, res["base"][0]))
        z0 = self.onset(HOME)
        res["onset"] = z0
        if z0 is None:
            self.log("B. no current up to Z %d" % ZCAP)
            return res
        self.rig.set_z(HOME)
        self.log("B. onset (|I| >= %d) at Z %d" % (ONSET, z0))
        # C. slope
        pts = []
        z = max(HOME, z0 - 1000)
        while z <= min(ZCAP, z0 + 1500):
            self.rig.set_z(z)
            v = self.reads(32, "slope")
            m = st.mean(v)
            pts.append((z, m))
            if abs(m) >= STOPC:
                break
            z += 10
        self.rig.set_z(HOME)
        res["slope"] = pts
        show = [p for p in pts if abs(p[1]) > 100]
        self.log("C. slope, points over 100 counts: " + " ".join("%d:%.0f" % p for p in show[:40]))
        # D. bias flip where |I| was nearest 1500
        cand = [p for p in pts if 300 <= abs(p[1]) <= 5000]
        if cand:
            zf = min(cand, key=lambda p: abs(abs(p[1]) - 1500))[0]
            flip = []
            self.rig.set_z(zf)
            for code, name in ((BNEG, "-0.5 V"), (BPOS, "+0.5 V"), (BZERO, "0 V"), (BNEG, "-0.5 V")):
                self.rig.bias(code)
                v = self.reads(64, "flip", bias=code)
                flip.append((name, st.mean(v), min(v), max(v)))
            self.rig.set_z(HOME)
            self.rig.bias(BNEG)
            res["flip"] = (zf, flip)
            self.log("D. flip at Z %d: " % zf + " | ".join("%s %.0f (%d..%d)" % f for f in flip))
        # E. drift
        track = []
        last = z0
        t_end = time.time() + drift_s
        while time.time() < t_end:
            tc = time.time()
            z = self.onset(last - 2000, step=50, tag="drift")
            self.rig.set_z(max(HOME, (z if z is not None else last) - 2000))
            track.append((round(time.time() - self.t0, 1), z))
            if z is None:
                self.log("E. onset lost above Z %d" % ZCAP)
                break
            if z < 500:
                self.rig.set_z(HOME)
                raise Abort("surface crept to Z %d, at the retract limit: stop and back off" % z)
            last = z
            time.sleep(max(0, 2.0 - (time.time() - tc)))
        self.rig.set_z(HOME)
        res["drift"] = track
        if len(track) > 1:
            self.log("E. onset vs time: " + " ".join("%.0fs:%s" % p for p in track))
        return res


class Rig:
    def __init__(self, port):
        sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
        from stm_approach import Device
        from stm_feedback_scan import read_averaged
        self.d, self._r, self.z = Device(port), read_averaged, None

    def set_z(self, z):
        z = int(max(HOME, min(ZCAP, z)))
        self.d._write(("DACZ %d\n" % z).encode())
        self.z = z
        time.sleep(0.002)

    def read(self):
        return self._r(self.d)

    def bias(self, code):
        self.d._write(("BIAS %d\n" % code).encode())
        time.sleep(0.05)


if __name__ == "__main__":
    import serial
    import json
    sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
    from stm_approach import find_teensy
    drift_s = float(sys.argv[1]) if len(sys.argv) > 1 else 60
    out = sys.argv[2] if len(sys.argv) > 2 else "onset0.csv"
    port = serial.Serial(find_teensy(), 115200, timeout=0.2)
    rig = Rig(port)
    run = Run(rig, log=lambda s: print(time.strftime("%H:%M:%S", time.gmtime()), s, flush=True))
    try:
        run.main(drift_s)
    except Abort as e:
        print("ABORT:", e, flush=True)
    finally:
        rig.set_z(HOME)
        rig.bias(BZERO)
        port.close()
        with open(out, "w") as f:
            f.write("t,tag,z,bias,value\n")
            for r in run.rows:
                f.write("%s,%s,%s,%s,%s\n" % r)
        print("end: Z %d, bias 0 V; wrote %s (%d rows)" % (HOME, out, len(run.rows)))
