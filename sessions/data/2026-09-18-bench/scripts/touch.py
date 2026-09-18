import sys, time, serial, statistics as st
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
from stm_approach import Device
from stm_feedback_scan import read_averaged
z = int(sys.argv[1])
port = serial.Serial("COM3", 115200, timeout=0.2)
dev = Device(port)
dev._write(b"BIAS 38229\n"); time.sleep(0.05)
dev.set_z(z); time.sleep(0.3)
v = [x for x in (read_averaged(dev) for _ in range(400)) if x is not None]
print(time.strftime("%H:%M:%S", time.gmtime()), "Z %d, -0.5 V: n=%d mean %.0f sd %.0f min %d max %d" % (z, len(v), st.mean(v), st.pstdev(v), min(v), max(v)))
if abs(st.mean(v)) > 500:
    dev.set_z(0); print("CURRENT PRESENT -> Z back to 0")
port.close()
