"""Simulated-junction tests for characterize.py. Run before it touches hardware."""
import random
import time
import characterize as ch

random.seed(1)


class FakeRig:
    def __init__(self, s0, cpd=250.0, reversed_=False, drift=0.0, noise=341.0):
        self.s0, self.cpd, self.rev, self.drift, self.noise = s0, cpd, reversed_, drift, noise
        self.t0 = time.time()
        self.z = 32768
        self.code = ch.BIAS_NEG
        self.zs = []
        self.max_read = 0

    def surface(self):
        return self.s0 + self.drift * (time.time() - self.t0)

    def set_z(self, z):
        z = int(max(ch.Z_FLOOR, min(ch.Z_CAP, z)))
        self.z = z
        self.zs.append(z)

    def bias(self, code):
        self.code = code

    def read(self):
        gap = (self.surface() - self.z) if self.rev else (self.z - self.surface())
        mag = 3000.0 * 10 ** min(gap / self.cpd, 6)
        sign = {ch.BIAS_NEG: 1, ch.BIAS_POS: -1}.get(self.code, 0)
        v = sign * mag + random.gauss(-10, self.noise / 18.0)   # ADCR-block-like noise
        v = int(max(-32768, min(32767, v)))
        self.max_read = max(self.max_read, abs(v))
        return v


def run(rig, drift_s=0.0):
    lines = []
    r, s = ch.main(rig, drift_s, log=lines.append)
    return r, s, lines


fails = []


def check(cond, msg):
    print(("  ok   " if cond else "  FAIL ") + msg)
    if not cond:
        fails.append(msg)


print("T1 normal, 250 counts/decade, surface at Z 20000")
rig = FakeRig(20000)
r, s, lines = run(rig, 2)
check(s.get("onset") is not None and 19700 <= s["onset"] <= 20000, "onset near 20000: %s" % s.get("onset"))
check(s.get("counts_per_decade") and 180 < s["counts_per_decade"] < 350,
      "counts/decade ~250: %s" % s.get("counts_per_decade"))
check(max(rig.zs) <= s["onset"] + ch.MAX_PUSH + 1600, "never far past onset: max Z %d" % max(rig.zs))
flip = dict((f[0] + str(i), f[1]) for i, f in enumerate(s.get("flip", [])))
check(flip and flip["-0.5 V0"] > 500 and flip["+0.5 V1"] < -500 and abs(flip["0 V2"]) < 300,
      "bias flip follows the sign: %s" % s.get("flip"))
check(rig.z == ch.HOME and "abort" not in s, "ends retracted at HOME, no abort (Z %d)" % rig.z)

print("T2 weak Z throw, 8000 counts/decade, surface at Z 30000")
rig = FakeRig(30000, cpd=8000)
r, s, lines = run(rig, 0)
check(s.get("onset") is not None, "onset found: %s" % s.get("onset"))
check(s.get("counts_per_decade") and 5000 < s["counts_per_decade"] < 12000,
      "counts/decade ~8000: %s" % s.get("counts_per_decade"))
check("abort" not in s, "no abort: %s" % s.get("abort"))

print("T3 REVERSED holder, surface close: contact at HOME")
rig = FakeRig(12000, reversed_=True)
r, s, lines = run(rig, 0)
check("abort" in s and "HOME" in s["abort"], "aborts on contact at home: %s" % s.get("abort"))
check(rig.z == ch.HOME and rig.code == ch.BIAS_ZERO,
      "Z NOT moved (a Z move might extend), bias zeroed: Z %d bias %d" % (rig.z, rig.code))

print("T4 REVERSED holder, surface out of reach")
rig = FakeRig(3000, cpd=250, reversed_=True)
r, s, lines = run(rig, 0)
check(s.get("onset") is None and max(rig.zs) <= ch.Z_CAP, "no onset, Z within cap")

print("T5 normal, contact already at HOME")
rig = FakeRig(9900)
r, s, lines = run(rig, 0)
check("abort" in s and rig.z == ch.HOME and rig.code == ch.BIAS_ZERO, "abort, Z left, bias zeroed")

print("T6 drift -300 counts/s toward the tip")
rig = FakeRig(25000, drift=-300.0)
r, s, lines = run(rig, 6)
rate = s.get("drift_rate")
check(rate is not None and -450 < rate < -150, "drift rate ~-300: %s" % rate)

print("T7 steep junction, 40 counts/decade: the push must stop short")
rig = FakeRig(20000, cpd=40)
r, s, lines = run(rig, 0)
check("abort" not in s, "no saturation abort: %s" % s.get("abort"))
check(rig.max_read < ch.SAT_STOP, "never read past SAT_STOP: max %d" % rig.max_read)

print("T8 direction check, synthetic responses")
class Z:  # minimal rig for direction_check
    z = 20000
    code = None
    def set_z(self, z): self.z = z
    def bias(self, c): self.code = c
rr = ch.Run(Z(), log=lambda *a: None)
try:
    rr.direction_check([(0, 1000), (-10, 990), (-25, 950), (-50, 900), (-100, 800), (-200, 700), (-400, 600),
                        (-800, 800), (-1600, 1500), (-3200, 3000)])
    check(False, "reversed response must abort")
except ch.Abort as e:
    check("ROSE" in str(e) and rr.rig.z == ch.Z_CAP, "reversed -> abort to Z_CAP")
rr = ch.Run(Z(), log=lambda *a: None)
try:
    rr.direction_check([(0, 1000)] + [(o, 950) for o in (-10, -25, -50, -100, -200, -400, -800, -1600, -3200)])
    check(False, "flat response must abort")
except ch.Abort as e:
    check("NOT confirmed" in str(e), "flat -> not confirmed")

print("\n%d failure(s)" % len(fails))
raise SystemExit(1 if fails else 0)
