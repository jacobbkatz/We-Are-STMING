"""Is the fast tracker's 'onset' a real junction? Real current vanishes at 0 V bias and flips
sign with it. Z-electrode coupling artefacts do not care about the bias."""
import sys, time, statistics as st
import serial
import zcal3 as zc
import fasttrack as ft
class FastRig(zc.Rig):
    def z(self, v):
        v = int(max(0, min(zc.ZCAP, v)))
        self.d._write(("DACZ %d\n" % v).encode()); time.sleep(0.0003)
port = serial.Serial("COM3", 115200, timeout=0.2)
rig = FastRig(port)
try:
    rig.z(0); rig.xy("X", zc.MID); rig.xy("Y", zc.MID)
    for code, name in ((38229, "-0.5 V"), (32768, "0 V"), (27307, "+0.5 V"), (32768, "0 V"), (38229, "-0.5 V")):
        rig.bias(code); rig.z(0)
        smp = ft.track(rig, 3.0, z_seed=25000)
        print(zc.ts(), name.rjust(6), ft.summary(smp), flush=True)
    # and the signed value at a fixed Z inside the band, both biases, slow and gentle
    for code, name in ((38229, "-0.5 V"), (27307, "+0.5 V"), (32768, "0 V")):
        rig.bias(code)
        row = []
        for z in (0, 10000, 15000, 20000, 25000, 30000):
            rig.z(z); time.sleep(0.01)
            v = [x for x in (rig.read() for _ in range(64)) if x is not None]
            row.append("%d:%.0f" % (z, st.mean(v)))
            if abs(st.mean(v)) > 15000: break
        rig.z(0)
        print(zc.ts(), "static", name.rjust(6), " ".join(row), flush=True)
finally:
    rig.z(0); rig.bias(32768); time.sleep(0.05)
    print(zc.ts(), "end: Z 0, bias 0 V"); port.close()
