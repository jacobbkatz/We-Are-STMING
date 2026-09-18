"""Lash and true step size. Cycles of: approach (-1 per step) until the 2 s median onset is
below LOWZ, then retract (+1 per step) until the onset is out of range (mostly 'none') for 2
consecutive steps, then approach again. After every single step: wait SETTLE s, then 2 s of
fast tracking -> median onset, and fractions below/none. Logged per step."""
import sys, time, statistics as st, json
import serial
import zcal3 as zc
import fasttrack as ft

CYCLES, LOWZ, SETTLE, MAXLEG = int(sys.argv[1]), 12000, 1.0, 40

class FastRig(zc.Rig):
    def z(self, v):
        v = int(max(0, min(zc.ZCAP, v)))
        self.d._write(("DACZ %d\n" % v).encode())
        time.sleep(0.0003)

port = serial.Serial("COM3", 115200, timeout=0.2)
rig = FastRig(port)
rows = []
def log(s): print(zc.ts(), s, flush=True)
def measure(seed):
    smp = ft.track(rig, 2.0, z_seed=seed)
    found = [z for _, z, f in smp if f == 0]
    n = len(smp)
    below = sum(1 for s in smp if s[2] == 1) / float(n)
    none = sum(1 for s in smp if s[2] == 2) / float(n)
    med = st.median(found) if found else None
    return med, below, none
try:
    rig.bias(38229); rig.z(0); rig.xy("X", zc.MID); rig.xy("Y", zc.MID)
    pos = 0; seed = 30000
    med, below, none = measure(seed)
    log("start: median %s below %.2f none %.2f" % (med, below, none))
    for c in range(CYCLES):
        # approach leg
        for k in range(MAXLEG):
            if med is not None and med < LOWZ and none < 0.5: break
            rig.z(0); rig.motor(-1); pos -= 1; time.sleep(SETTLE)
            med, below, none = measure(med or 40000)
            rows.append((c, "in", pos, med, round(below, 2), round(none, 2)))
            log("c%d in  pos %+d: median %s below %.2f none %.2f" % (c, pos, med, below, none))
        # retract leg
        outs = 0
        for k in range(MAXLEG):
            rig.z(0); rig.motor(1); pos += 1; time.sleep(SETTLE)
            med, below, none = measure(med or 20000)
            rows.append((c, "out", pos, med, round(below, 2), round(none, 2)))
            log("c%d out pos %+d: median %s below %.2f none %.2f" % (c, pos, med, below, none))
            outs = outs + 1 if none > 0.8 else 0
            if outs >= 2: break
finally:
    rig.z(0); rig.xy("X", zc.MID); rig.xy("Y", zc.MID)
    rig.motor(20); rig.bias(32768); time.sleep(0.2)
    log("end: Z 0, X/Y mid, motor +20 more, bias 0 V")
    port.close()
    with open("lash_run1.csv", "w") as f:
        f.write("cycle,dir,pos,median_onset,frac_below,frac_none\n")
        for r in rows: f.write("%s,%s,%s,%s,%s,%s\n" % r)
