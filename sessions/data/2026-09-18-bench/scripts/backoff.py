"""Retract with the motor (POSITIVE retracts) in chunks until the tip is clear at Z = ZTEST.
Z is held at 0 (retracted end) during every motor move. Bias -0.5 V for the checks."""
import sys, time, serial, statistics as st
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
from stm_approach import Device
from stm_feedback_scan import read_averaged
chunk = int(sys.argv[1]); limit = int(sys.argv[2]); ztest = int(sys.argv[3])
port = serial.Serial("COM3", 115200, timeout=0.2)
dev = Device(port)
moved = 0
def check():
    dev.set_z(ztest); time.sleep(0.05)
    v = [x for x in (read_averaged(dev) for _ in range(64)) if x is not None]
    dev.set_z(0)
    return st.mean(v), max(abs(x) for x in v)
try:
    dev._write(b"BIAS 38229\n"); time.sleep(0.1)
    dev.set_z(0)
    m, mx = check()
    print("%s start: at Z %d mean %.0f max|%d|" % (time.strftime("%H:%M:%S", time.gmtime()), ztest, m, mx), flush=True)
    while moved < limit and not (abs(m) < 500 and mx < 3000):
        dev.set_z(0)
        dev.move_motor(chunk); moved += chunk
        time.sleep(0.3)
        m, mx = check()
        print("%s +%d: at Z %d mean %.0f max|%d|" % (time.strftime("%H:%M:%S", time.gmtime()), moved, ztest, m, mx), flush=True)
    print("CLEAR" if (abs(m) < 500 and mx < 3000) else "NOT CLEAR at limit", "after +%d" % moved)
finally:
    dev.set_z(0); time.sleep(0.02)
    port.close()
