import sys, time, serial
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
from stm_approach import Device
secs = float(sys.argv[1]) if len(sys.argv) > 1 else 5
port = serial.Serial("COM3", 115200, timeout=0.2)
dev = Device(port)
t0 = time.time(); out = []
while time.time() - t0 < secs:
    v = dev.read_adc()
    if v is not None: out.append((round(time.time()-t0,2), v))
port.close()
n = len(out); k = max(1, n // 8)
for i in range(0, n, k):
    seg = [v for _, v in out[i:i+k]]
    print("t=%5.1fs  mean %7.0f  min %7d  max %7d  (n=%d)" % (out[i][0], sum(seg)/len(seg), min(seg), max(seg), len(seg)))
