"""Position the onset high in the Z window, then track continuously in 10 s chunks for TOTAL s.
If a chunk's median onset falls below LOW, retract the motor (+LASH+1 the first time, +1 after)
and log it. End: Z 0, X/Y mid, motor +20, bias 0 V."""
import sys, time, statistics as st, json
import serial
import zcal3 as zc
import fasttrack as ft

TOTAL, LOW, LASH = float(sys.argv[1]), 8000, 5

class FastRig(zc.Rig):
    def z(self, v):
        v = int(max(0, min(zc.ZCAP, v)))
        self.d._write(("DACZ %d\n" % v).encode())
        time.sleep(0.0003)

port = serial.Serial("COM3", 115200, timeout=0.2)
rig = FastRig(port)
chunks = []
def log(s): print(zc.ts(), s, flush=True)
try:
    rig.bias(38229); rig.z(0); rig.xy("X", zc.MID); rig.xy("Y", zc.MID)
    z_on = None; steps = 0
    for s in range(60):
        z_on = zc.onset(rig)
        if z_on is not None and 30000 <= z_on <= 48000: break
        rig.z(0)
        if z_on is not None and z_on < 30000: rig.motor(1); steps += 1
        else: rig.motor(-1); steps -= 1
    log("positioned: onset %s after motor %+d" % (z_on, steps))
    t_start = time.time(); seed = z_on or 30000; retracted_once = False; adj = 0
    while time.time() - t_start < TOTAL:
        smp = ft.track(rig, 10.0, z_seed=seed)
        found = [z for _, z, f in smp if f == 0]
        below = sum(1 for s_ in smp if s_[2] == 1)
        med = st.median(found) if found else None
        chunks.append({"t": round(time.time() - t_start, 1), "n": len(smp), "found": len(found),
                       "below": below, "median": med,
                       "sd": round(st.pstdev(found)) if len(found) > 2 else None,
                       "adj": adj, "samples": smp})
        log("t=%4.0fs median %s sd %s below %d (n %d) motor adj %+d" % (
            chunks[-1]["t"], med, chunks[-1]["sd"], below, len(smp), adj))
        seed = med or seed
        if med is not None and med < LOW:
            rig.z(0)
            n = (LASH + 1) if not retracted_once else 1
            rig.motor(n); adj += n; retracted_once = True
            log("  onset below %d: motor +%d" % (LOW, n))
            seed = 30000
    if chunks:
        last = chunks[-1]["samples"]
        sp = ft.spectrum(last, list(range(1, 31)))
        log("spectrum of last chunk: " + " ".join("%d:%.0f" % kv for kv in sorted(sp.items())))
finally:
    rig.z(0); rig.xy("X", zc.MID); rig.xy("Y", zc.MID)
    rig.motor(20); rig.bias(32768); time.sleep(0.2)
    log("end: Z 0, X/Y mid, motor +20, bias 0 V")
    port.close()
    json.dump(chunks, open("ft_long_%d.json" % int(time.time()), "w"))
