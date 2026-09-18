"""ADCR-only noise, at two biases. Tip must be clear (Z retracted). Read-only apart from BIAS."""
import sys, time, serial, statistics as st
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
from stm_approach import Device
from stm_feedback_scan import read_averaged
secs = float(sys.argv[1]) if len(sys.argv) > 1 else 5
port = serial.Serial("COM3", 115200, timeout=0.2)
dev = Device(port)
out = []
def block(code, label):
    port.write(("BIAS %d\n" % code).encode()); port.flush(); time.sleep(0.3)
    port.reset_input_buffer()
    vals = []; t0 = time.time()
    while time.time() - t0 < secs:
        v = read_averaged(dev)
        if v is not None: vals.append(v)
    rate = len(vals) / secs
    k = max(1, int(rate * 0.1))          # 0.1 s blocks
    means = [st.mean(vals[i:i+k]) for i in range(0, len(vals) - k + 1, k)]
    out.append("%s: n=%d (%.0f/s) mean %.0f sd %.0f | 0.1 s block means sd %.0f" % (
        label, len(vals), rate, st.mean(vals), st.pstdev(vals), st.pstdev(means)))
try:
    block(38229, "-0.5 V")
    block(32768, " 0 V ")
finally:
    port.write(b"BIAS 38229\n"); port.flush(); time.sleep(0.05)
    port.close()
print(time.strftime("%H:%M:%S", time.gmtime()), " || ".join(out))
