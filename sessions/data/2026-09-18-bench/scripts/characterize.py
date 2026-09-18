"""Characterise the junction of the REBUILT tip holder, before any feedback tool
is trusted with it.

Every constant in stm_feedback_scan.py (250 Z counts per decade, the high end of
Z extends toward the sample, MAX_STEP) was measured on the OLD holder. The
holder was rebuilt on 2026-09-18 (UTC) and the tip is ~2.2 mm from where it was.
So, in order, with Z bounded and a retract on every exit path:

  A. baseline with Z at HOME (10000), sample at -0.5 V; abort if there is
     already current there
  B. creep Z up from HOME in small steps until the current reaches ONSET
  C. step Z around the onset: mostly AWAY from the sample, at most +400 toward
     it, stopping the instant the current passes STOP. Gives the direction
     and the Z counts per decade
  D. bias flip at the onset: the reading must follow the sign of the bias
  E. drift: re-find the onset every few seconds for DRIFT_S seconds

Z never leaves [Z_FLOOR, Z_CAP]. Any reading past SAT_STOP retracts at once.
If the direction turns out to be REVERSED, Z is sent to the high end and the
run stops: that end then retracts.

Usage: py characterize.py [drift_seconds] [log.csv]
"""
import sys
import time
import math
import statistics as st

Z_FLOOR, Z_CAP = 0, 50000
HOME = 10000
ONSET = 1000        # counts, ~3.1 nA: well above the 0.1 s noise (~25-30)
STOP = 10000        # counts, ~31 nA: never push toward the sample past this
SAT_STOP = 20000    # counts: any single averaged read past this -> retract
MAX_PUSH = 400      # never step more than this past the onset, toward sample
BIAS_NEG, BIAS_POS, BIAS_ZERO = 38229, 27307, 32768


class Abort(Exception):
    pass


class Rig:
    """The real instrument. set_z / read / bias only."""

    def __init__(self, port):
        sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
        from stm_approach import Device
        from stm_feedback_scan import read_averaged
        self._dev = Device(port)
        self._read = read_averaged
        self.port = port
        self.z = None

    def set_z(self, z):
        z = int(max(Z_FLOOR, min(Z_CAP, z)))
        self._dev._write(("DACZ %d\n" % z).encode())
        self.z = z
        time.sleep(0.002)

    def read(self):
        return self._read(self._dev)

    def bias(self, code):
        self._dev._write(("BIAS %d\n" % code).encode())
        time.sleep(0.05)


class Run:
    def __init__(self, rig, log=print):
        self.rig = rig
        self.log = log
        self.retract_to = HOME       # changes to Z_CAP if the direction is reversed
        self.final_z = HOME          # None = leave Z where an abort put it
        self.final_bias = BIAS_NEG
        self.rows = []               # (t, phase, z, bias, value)
        self.t0 = time.time()

    # -- primitives -------------------------------------------------------

    def reads(self, n, phase, bias=BIAS_NEG, sat_check=True):
        vals = []
        for _ in range(n):
            v = self.rig.read()
            if v is None:
                continue
            self.rows.append((round(time.time() - self.t0, 4), phase, self.rig.z, bias, v))
            if sat_check and abs(v) >= SAT_STOP:
                self.rig.set_z(self.retract_to)
                self.final_z = self.retract_to
                raise Abort("reading %d at Z %d is past %d: retracted" % (v, self.rig.z, SAT_STOP))
            vals.append(v)
        return vals

    def find_onset(self, z_from, step=50, phase="onset"):
        z = z_from
        while z <= Z_CAP:
            self.rig.set_z(z)
            v = self.reads(4, phase)
            if v and abs(st.median(v)) >= ONSET:
                more = self.reads(8, phase)
                if more and abs(st.median(more)) >= ONSET:
                    return z
            z += step
        return None

    # -- the phases -------------------------------------------------------

    def baseline(self):
        self.rig.bias(BIAS_NEG)
        self.rig.set_z(HOME)
        time.sleep(0.5)
        v = self.reads(200, "baseline", sat_check=False)
        m, sd = st.mean(v), st.pstdev(v)
        self.log("A. baseline at Z %d, -0.5 V: mean %.0f, sd %.0f (n=%d)" % (HOME, m, sd, len(v)))
        if abs(m) > 500:
            # The Z direction of the rebuilt holder is not yet confirmed, so no
            # Z move is known to retract. Zero the bias and leave Z alone: the
            # motor (positive retracts, direction-independent of the holder's
            # face) is the way out.
            self.rig.bias(BIAS_ZERO)
            self.final_z, self.final_bias = None, BIAS_ZERO
            raise Abort("current already present at HOME (mean %.0f). Bias zeroed, Z "
                        "left at %d. Back the motor off (positive) before anything else." % (m, HOME))
        return m

    def response(self, z0):
        """Mostly away from the sample. Toward it only while the PREDICTED next
        current stays under STOP, and a read at or past STOP ends the push at
        once with a retract."""
        out = []
        for off in (0, -10, -25, -50, -100, -200, -400, -800, -1600, -3200):
            self.rig.set_z(z0 + off)
            v = self.reads(16, "resp")
            out.append((off, st.mean(v)))
        cpd, _ = self.counts_per_decade(out, 30.0)
        self.away_len = len(out)
        prev_off, prev_i = 0, abs(out[0][1])
        for off in (50, 100, 200, 400):
            if off > MAX_PUSH:
                break
            if cpd is None:
                break
            if cpd is not None and prev_i * 10 ** ((off - prev_off) / cpd) > STOP:
                break
            self.rig.set_z(z0 + off)
            vals = []
            stopped = False
            for _ in range(16):
                v = self.reads(1, "resp")
                if not v:
                    continue
                vals.append(v[0])
                if abs(v[0]) >= STOP:
                    stopped = True
                    break
            if not vals:
                break
            out.append((off, st.mean(vals)))
            if stopped:
                self.rig.set_z(z0 - 1600)
                break
            prev_off, prev_i = off, abs(st.mean(vals))
        self.rig.set_z(z0 - 1600)
        return out

    def direction_check(self, resp):
        at = dict(resp[:10])          # the away-from-sample leg, first pass
        i0, i_far = abs(at[0]), abs(at[-3200])
        self.log("C. |I| at onset %.0f, at onset-3200 %.0f" % (i0, i_far))
        if i_far > i0 * 1.5:
            self.retract_to = Z_CAP
            self.rig.set_z(Z_CAP)
            self.final_z = Z_CAP
            raise Abort("current ROSE when Z went down: the LOW end extends toward "
                        "the sample for this holder. Z sent to %d." % Z_CAP)
        if not i0 > i_far * 1.5:
            self.rig.bias(BIAS_ZERO)
            self.final_z, self.final_bias = None, BIAS_ZERO
            raise Abort("direction NOT confirmed: |I| %.0f at onset against %.0f 3200 "
                        "counts lower. Bias zeroed, Z left at %d." % (i0, i_far, self.rig.z))

    def counts_per_decade(self, resp, noise):
        pts = [(off, abs(i)) for off, i in resp[:10] if off <= 0 and abs(i) > max(3 * noise, 60)]
        if len(pts) < 3:
            return None, pts
        xs = [p[0] for p in pts]
        ys = [math.log10(p[1]) for p in pts]
        mx, my = st.mean(xs), st.mean(ys)
        sxx = sum((x - mx) ** 2 for x in xs)
        slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
        return (1.0 / slope if slope > 0 else None), pts

    def bias_flip(self, z0):
        self.rig.set_z(z0)
        res = []
        for code, name in ((BIAS_NEG, "-0.5 V"), (BIAS_POS, "+0.5 V"),
                           (BIAS_ZERO, "0 V"), (BIAS_NEG, "-0.5 V")):
            self.rig.bias(code)
            v = self.reads(32, "flip", bias=code)
            res.append((name, st.mean(v), min(v), max(v)))
        self.rig.bias(BIAS_NEG)
        self.rig.set_z(z0 - 1600)
        return res

    def drift(self, z_start, seconds, every=3.0):
        track = []
        z_last = z_start
        t_end = time.time() + seconds
        while time.time() < t_end:
            t_cycle = time.time()
            z = self.find_onset(max(Z_FLOOR, z_last - 1500), step=25, phase="drift")
            if z is None:
                self.rig.set_z(self.retract_to)
                self.final_z = self.retract_to
                self.log("E. onset lost (surface moved beyond Z_CAP): stopping drift track")
                break
            track.append((round(time.time() - self.t0, 2), z))
            self.rig.set_z(z - 1500)
            z_last = z
            if z < HOME - 8000:
                self.rig.set_z(Z_FLOOR)
                self.final_z = Z_FLOOR
                raise Abort("surface has crept to Z %d, near the retract limit" % z)
            time.sleep(max(0, every - (time.time() - t_cycle)))
        return track


def main(rig, drift_s=60, log=print):
    run = Run(rig, log)
    summary = {}
    try:
        base = run.baseline()
        z0 = run.find_onset(HOME, step=25)
        if z0 is None:
            log("B. no current anywhere up to Z %d: surface out of reach" % Z_CAP)
            summary["onset"] = None
            return run, summary
        log("B. onset (|I| >= %d counts) at Z %d" % (ONSET, z0))
        summary["onset"] = z0
        resp = run.response(z0)
        log("C. response (offset: mean counts): " +
            ", ".join("%+d: %.0f" % (o, i) for o, i in resp))
        run.direction_check(resp)
        noise = 30.0
        cpd, pts = run.counts_per_decade(resp, noise)
        summary["counts_per_decade"] = cpd
        log("C. Z counts per decade (away leg, %d points): %s"
            % (len(pts), "%.0f" % cpd if cpd else "not measurable"))
        z0b = run.find_onset(z0 - 1600, step=25)
        if z0b is None:
            log("D. onset lost before bias flip")
        else:
            flip = run.bias_flip(z0b)
            summary["flip"] = flip
            log("D. bias flip at Z %d: " % z0b +
                " | ".join("%s mean %.0f (%d..%d)" % f for f in flip))
            track = run.drift(z0b, drift_s)
            summary["drift"] = track
            if len(track) >= 2:
                ts = [p[0] for p in track]
                zs = [p[1] for p in track]
                mt, mz = st.mean(ts), st.mean(zs)
                stt = sum((t - mt) ** 2 for t in ts)
                rate = sum((t - mt) * (z - mz) for t, z in zip(ts, zs)) / stt if stt else 0
                summary["drift_rate"] = rate
                log("E. drift: onset Z " + ", ".join("%.0fs:%d" % p for p in track))
                log("E. drift rate %.1f Z counts/s (negative = surface coming toward the tip)"
                    % rate)
    except Abort as e:
        log("ABORT: %s" % e)
        summary["abort"] = str(e)
    finally:
        try:
            if run.final_z is not None:
                rig.set_z(run.final_z)
            rig.bias(run.final_bias)
        except Exception:
            pass
    return run, summary


if __name__ == "__main__":
    import serial
    drift_s = float(sys.argv[1]) if len(sys.argv) > 1 else 60
    out = sys.argv[2] if len(sys.argv) > 2 else "characterize.csv"
    port = serial.Serial("COM3", 115200, timeout=0.2)
    try:
        run, summary = main(Rig(port), drift_s)
    finally:
        port.close()
    with open(out, "w") as f:
        f.write("t,phase,z,bias,value\n")
        for r in run.rows:
            f.write("%s,%s,%s,%s,%s\n" % r)
    print("wrote %s (%d rows)" % (out, len(run.rows)))
