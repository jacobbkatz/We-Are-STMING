"""Current against Z at several biases, Z confined to [0, ZCAP] (already visited). Compact output."""
import sys, time, serial, statistics as st
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
from stm_approach import Device
from stm_feedback_scan import read_averaged
biases = [int(b) for b in sys.argv[1].split(",")]
zs = [int(z) for z in sys.argv[2].split(",")]
ZCAP = int(sys.argv[3])
port = serial.Serial("COM3", 115200, timeout=0.2)
dev = Device(port)
try:
    for b in biases:
        dev._write(("BIAS %d\n" % b).encode()); time.sleep(0.1)
        row = []
        for z in zs:
            z = min(z, ZCAP)
            dev.set_z(z); time.sleep(0.03)
            v = [x for x in (read_averaged(dev) for _ in range(32)) if x is not None]
            row.append("%d:%.0f" % (z, st.mean(v)))
        print("%s bias %d | %s" % (time.strftime("%H:%M:%S", time.gmtime()), b, "  ".join(row)), flush=True)
finally:
    dev.set_z(0); time.sleep(0.02)
    dev._write(b"BIAS 32768\n"); time.sleep(0.05)
    print("end: Z 0, bias 0 V")
    port.close()
