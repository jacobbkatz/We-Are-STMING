import sys, time, statistics as st, json
import serial
import zcal3 as zc
import fasttrack as ft

class FastRig(zc.Rig):
    def z(self, v):
        v = int(max(0, min(zc.ZCAP, v)))
        self.d._write(("DACZ %d\n" % v).encode())
        time.sleep(0.0003)

port = serial.Serial("COM3", 115200, timeout=0.2)
rig = FastRig(port)
res = {}
def log(s): print(zc.ts(), s, flush=True)
try:
    rig.bias(38229); rig.z(0); rig.xy("X", zc.MID); rig.xy("Y", zc.MID)
    z_on = None; steps = 0
    for s in range(60):
        z_on = zc.onset(rig)
        if z_on is not None and 15000 <= z_on <= 40000: break
        rig.z(0)
        if z_on is not None and z_on < 15000: rig.motor(2); steps += 2
        else: rig.motor(-1); steps -= 1
    log("positioned: onset %s after motor %+d" % (z_on, steps))
    smp = ft.track(rig, 20.0, z_seed=z_on or 25000)
    log("hold A: " + ft.summary(smp)); res["A"] = smp
    sp = ft.spectrum(smp, list(range(1, 31)))
    log("spectrum A (counts): " + " ".join("%d:%.0f" % (f, a) for f, a in sorted(sp.items())))
    for axis in ("X", "Y"):
        seq = []
        for off in (0, 10000, 0, -10000, 0, 10000, 0, -10000, 0):
            rig.z(0); rig.xy(axis, zc.MID + off); time.sleep(0.05)
            s2 = ft.track(rig, 3.0, z_seed=z_on or 25000)
            found = [z for _, z, f in s2 if f == 0]
            seq.append((off, round(st.mean(found)) if found else None, len(found), len(s2)))
            res.setdefault(axis, []).append((off, s2))
        rig.z(0); rig.xy(axis, zc.MID)
        log("%s: " % axis + " ".join("%+d:%s(%d/%d)" % q for q in seq))
    smp = ft.track(rig, 20.0, z_seed=z_on or 25000)
    log("hold B: " + ft.summary(smp)); res["B"] = smp
    sp = ft.spectrum(smp, list(range(1, 31)))
    log("spectrum B (counts): " + " ".join("%d:%.0f" % (f, a) for f, a in sorted(sp.items())))
finally:
    rig.z(0); rig.xy("X", zc.MID); rig.xy("Y", zc.MID)
    rig.motor(20); rig.bias(32768); time.sleep(0.2)
    log("end: Z 0, X/Y mid, motor +20, bias 0 V")
    port.close()
    json.dump({k: v for k, v in res.items()}, open("ft_run1.json", "w"))
