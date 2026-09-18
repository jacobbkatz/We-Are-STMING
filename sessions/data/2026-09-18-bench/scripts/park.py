"""Retract with the motor until a slow static scan of the WHOLE Z range (0..50000) at -0.5 V shows
no current anywhere, twice in a row; then park Z, X, Y, bias at midscale."""
import time, statistics as st
import serial
import zcal3 as zc
port = serial.Serial("COM3", 115200, timeout=0.2)
rig = zc.Rig(port)
def scan():
    worst = 0
    for z in range(0, 50001, 1000):
        rig.z(z); time.sleep(0.01)
        v = [x for x in (rig.read() for _ in range(16)) if x is not None]
        m = abs(st.mean(v)); worst = max(worst, m)
        if m > 3000: break
    rig.z(0)
    return worst
try:
    rig.bias(38229); rig.z(0); rig.xy("X", zc.MID); rig.xy("Y", zc.MID)
    total = 0; clean = 0
    while total < 400:
        w = scan()
        print(zc.ts(), "retracted +%d: worst |I| over Z 0..50000 = %.0f" % (total, w), flush=True)
        clean = clean + 1 if w < 600 else 0
        if clean >= 2: break
        rig.z(0); rig.motor(25); total += 25; time.sleep(0.5)
    rig.z(0); rig.motor(50); total += 50
    w = scan()
    print(zc.ts(), "after +50 margin (total +%d): worst |I| %.0f" % (total, w))
finally:
    rig.z(0)
    rig.bias(32768); time.sleep(0.05)
    for c in ("DACX 32768\n", "DACY 32768\n", "DACZ 32768\n"):
        rig.d._write(c.encode()); time.sleep(0.02)
    time.sleep(0.1)
    v = [x for x in (rig.read() for _ in range(64)) if x is not None]
    print(zc.ts(), "parked: Z/X/Y/bias midscale; reading %.0f" % st.mean(v))
    port.close()
