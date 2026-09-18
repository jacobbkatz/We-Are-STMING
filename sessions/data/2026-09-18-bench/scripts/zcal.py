"""Z counts per motor step, measured by onset tracking.
At each motor position: find the Z where |I| first reaches ONSET (sweeping up from ZLO in ZSTEP),
twice, retracting to 0 between. Then MTMV +k (retract direction, backlash already taken up)."""
import sys, time, serial, statistics as st
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
from stm_approach import Device
from stm_feedback_scan import read_averaged
k = int(sys.argv[1]); nmoves = int(sys.argv[2]); zstep = int(sys.argv[3])
ONSET, ZCAP, SAT = 1000, 50000, 20000
port = serial.Serial("COM3", 115200, timeout=0.2)
dev = Device(port)
def onset():
    z = 0
    while z <= ZCAP:
        dev.set_z(z)
        v = [x for x in (read_averaged(dev) for _ in range(4)) if x is not None]
        if v and abs(st.median(v)) >= ONSET:
            w = [x for x in (read_averaged(dev) for _ in range(8)) if x is not None]
            if w and abs(st.median(w)) >= ONSET:
                dev.set_z(0)
                return z, st.median(w)
        if v and max(abs(x) for x in v) >= SAT:
            dev.set_z(0); return z, max(v)
        z += zstep
    dev.set_z(0)
    return None, None
try:
    dev._write(b"BIAS 38229\n"); time.sleep(0.1)
    total = 0
    for i in range(nmoves + 1):
        a = onset(); time.sleep(0.5); b = onset()
        print("%s motor +%d: onset Z %s (I %s), again %s (I %s)" % (
            time.strftime("%H:%M:%S", time.gmtime()), total, a[0], a[1], b[0], b[1]), flush=True)
        if a[0] is None and b[0] is None:
            print("onset beyond Z %d: stop" % ZCAP); break
        if i < nmoves:
            dev.set_z(0); dev.move_motor(k); total += k; time.sleep(0.3)
finally:
    dev.set_z(0); time.sleep(0.02)
    print("end: Z 0, motor moved +%d this run" % total)
    port.close()
