"""1. Static I(Z), 0..50000 in 1000 steps, 20 ms settle, 32 reads, at -0.5 V, 0 V, +0.5 V.
   A biased scan stops (and retracts) at |I| > 10000.
2. The step transient: at bias 0 V, Z held where there is no static current, step Z by +800 and
   by -4000 and read immediately (2 reads), then again after 5 ms and 20 ms. Repeated 20 times."""
import sys, time, statistics as st
import serial
import zcal3 as zc
port = serial.Serial("COM3", 115200, timeout=0.2)
rig = zc.Rig(port)
def reads(n):
    return [x for x in (rig.read() for _ in range(n)) if x is not None]
try:
    rig.xy("X", zc.MID); rig.xy("Y", zc.MID)
    for code, name in ((38229, "-0.5 V"), (32768, "0 V"), (27307, "+0.5 V")):
        rig.bias(code); rig.z(0); time.sleep(0.05)
        row = []
        for z in range(0, 50001, 1000):
            rig.z(z); time.sleep(0.02)
            m = st.mean(reads(32))
            row.append((z, m))
            if code != 32768 and abs(m) > 10000: break
        rig.z(0)
        big = [(z, round(m)) for z, m in row if abs(m) > 300]
        print(zc.ts(), "static", name.rjust(6), "points %d, |I|>300 at: %s" % (len(row), big if big else "none"), flush=True)
    rig.bias(32768); time.sleep(0.05)
    for base, step in ((20000, 800), (24000, -4000), (20000, 4000)):
        imm, at5, at20 = [], [], []
        for _ in range(20):
            rig.z(base); time.sleep(0.03)
            rig.d._write(("DACZ %d\n" % (base + step)).encode())
            time.sleep(0.0003)
            imm.append(st.median(reads(2)))
            time.sleep(0.005); at5.append(st.median(reads(2)))
            time.sleep(0.015); at20.append(st.median(reads(2)))
        print(zc.ts(), "0 V, Z %d -> %+d: immediate median %.0f (max|%.0f|), +5 ms %.0f, +20 ms %.0f" % (
            base, step, st.median(imm), max(abs(x) for x in imm), st.median(at5), st.median(at20)), flush=True)
finally:
    rig.z(0); rig.bias(32768); time.sleep(0.05)
    print(zc.ts(), "end: Z 0, bias 0 V"); port.close()
