"""Z to midscale, optional motor move, then the current at Z 0, 16000, 32768, 48000 at -0.14 V.
Ends at Z midscale, bias 0 V."""
import sys, time, statistics as st
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
import serial
from stm_approach import Device, find_teensy
from stm_feedback_scan import read_averaged
steps = int(sys.argv[1])
p = serial.Serial(find_teensy(), 115200, timeout=0.2); d = Device(p)
try:
    d._write(b"BIAS 32768\n"); time.sleep(0.02)
    d._write(b"DACZ 32768\n"); time.sleep(0.05)
    if steps:
        d.move_motor(steps)
    d._write(b"BIAS 34321\n"); time.sleep(0.1)
    row = []
    for z in (32768, 16000, 0, 48000, 32768):
        d._write(("DACZ %d\n" % z).encode()); time.sleep(0.03)
        v = [x for x in (read_averaged(d) for _ in range(64)) if x is not None]
        row.append("Z%d:%.0f" % (z, st.mean(v)))
    print(time.strftime("%H:%M:%S", time.gmtime()), "after motor %+d: %s" % (steps, " ".join(row)), flush=True)
finally:
    d._write(b"DACZ 32768\n"); time.sleep(0.02); d._write(b"BIAS 32768\n"); time.sleep(0.05)
    p.close()
