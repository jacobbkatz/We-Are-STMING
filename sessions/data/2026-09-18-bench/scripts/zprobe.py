"""Does Z move the tip? At a low bias, read the current at a sequence of Z codes.
Toward-sample moves are capped at ZMAX. Any |reading| >= 30000 on the way UP ends the up-leg."""
import sys, time, serial, statistics as st
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
from stm_approach import Device
from stm_feedback_scan import read_averaged
bias = int(sys.argv[1]); seq = [int(s) for s in sys.argv[2].split(",")]; ZMAX = int(sys.argv[3])
port = serial.Serial("COM3", 115200, timeout=0.2)
dev = Device(port)
try:
    dev._write(("BIAS %d\n" % bias).encode()); time.sleep(0.1)
    prev = None
    for z in seq:
        if z > ZMAX: print("skip Z %d > cap %d" % (z, ZMAX)); continue
        dev.set_z(z); time.sleep(0.05)
        v = [x for x in (read_averaged(dev) for _ in range(64)) if x is not None]
        m = st.mean(v)
        print("%s Z %5d: mean %7.0f  min %6d max %6d" % (time.strftime("%H:%M:%S", time.gmtime()), z, m, min(v), max(v)), flush=True)
        if prev is not None and z > prev and abs(m) >= 30000:
            print("pinned on the way up: stop"); break
        prev = z
finally:
    dev.set_z(0); time.sleep(0.02)
    dev._write(b"BIAS 32768\n"); time.sleep(0.05)
    print("end: Z 0, bias 0 V")
    port.close()
