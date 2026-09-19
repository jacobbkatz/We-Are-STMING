import sys, time, serial, statistics as st
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
from stm_approach import Device, find_teensy
from stm_feedback_scan import read_averaged
port = serial.Serial(find_teensy(), 115200, timeout=0.2)
dev = Device(port)
for c in ("DACX 32768\n", "DACY 32768\n", "DACZ 10000\n"):
    dev._write(c.encode()); time.sleep(0.05)
out = []
for code, name in ((32768, "0 V"), (38229, "-0.5 V"), (27307, "+0.5 V"), (32768, "0 V")):
    dev._write(("BIAS %d\n" % code).encode()); time.sleep(0.3)
    v = [x for x in (read_averaged(dev) for _ in range(2000)) if x is not None]
    out.append("%s: n=%d mean %.0f sd %.0f" % (name, len(v), st.mean(v), st.pstdev(v)))
dev._write(b"BIAS 32768\n"); time.sleep(0.05)
port.close()
print(time.strftime("%H:%M:%S", time.gmtime()), "Z 10000 | " + " | ".join(out))
