"""Approach one step at a time until the onset lies in [LO, HI]; then hold the motor still and
re-find the onset (sweep up from 0, 250-count steps) repeatedly for SECS seconds. Z at 0 between
searches. If the onset reaches Z <= 2000 the motor retracts +3 (logged) and tracking continues.
End: Z 0, retract +RET_END, bias 0 V."""
import sys, time, statistics as st
import serial
import zcal3 as zc
LO, HI, SECS, RET_END = 15000, 40000, float(sys.argv[1]), int(sys.argv[2])
port = serial.Serial("COM3", 115200, timeout=0.2)
rig = zc.Rig(port)
rows = []
try:
    rig.bias(38229); rig.z(0)
    z_on = None
    for s in range(40):
        z_on = zc.onset(rig)
        if z_on is not None and LO <= z_on <= HI: break
        if z_on is not None and z_on < LO:
            rig.z(0); rig.motor(3); continue
        rig.z(0); rig.motor(-1)
    print(zc.ts(), "start onset", z_on, flush=True)
    t0 = time.time(); motor_adj = 0
    while time.time() - t0 < SECS:
        z_on = zc.onset(rig)
        t = time.time() - t0
        rows.append((round(t, 2), z_on, motor_adj))
        if z_on is not None and z_on <= 2000:
            rig.z(0); rig.motor(3); motor_adj += 3
    ons = [r[1] for r in rows if r[1] is not None]
    print(zc.ts(), "n=%d found=%d none=%d motor adj +%d" % (len(rows), len(ons), len(rows) - len(ons), motor_adj))
    for i in range(0, len(rows), max(1, len(rows) // 30)):
        print("  t=%5.1fs onset %s (adj %d)" % rows[i])
    if len(ons) > 2:
        print("onset mean %.0f sd %.0f min %d max %d" % (st.mean(ons), st.pstdev(ons), min(ons), max(ons)))
finally:
    rig.z(0)
    rig.motor(RET_END)
    rig.bias(32768)
    time.sleep(0.2)
    print(zc.ts(), "end: Z 0, motor +%d, bias 0 V" % RET_END)
    port.close()
with open("track_run1.csv", "w") as f:
    f.write("t,onset_z,motor_adj\n")
    for r in rows: f.write("%s,%s,%s\n" % r)
