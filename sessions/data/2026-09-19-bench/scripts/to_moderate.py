"""Back the motor off ONE step at a time (positive retracts) from a hard contact until the current
at midscale is moderate (LO..HI counts) or gone. Z midscale, -0.5 V throughout. Logs every step."""
import sys, time, statistics as st
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
import serial
from stm_approach import Device, find_teensy
from stm_feedback_scan import read_averaged
LO, HI, MAXK = 300, 8000, int(sys.argv[1]) if len(sys.argv) > 1 else 80
p = serial.Serial(find_teensy(), 115200, timeout=0.2); d = Device(p)
def rd(n=64):
    v = [x for x in (read_averaged(d) for _ in range(n)) if x is not None]; return st.mean(v)
try:
    d._write(b"BIAS 38229\n"); time.sleep(0.05); d._write(b"DACZ 32768\n"); time.sleep(0.05)
    k = 0; m = rd()
    print(time.strftime("%H:%M:%S", time.gmtime()), "start: %.0f" % m, flush=True)
    while k < MAXK and abs(m) >= HI:
        d.move_motor(1); k += 1; time.sleep(0.2)
        m = rd()
        print(time.strftime("%H:%M:%S", time.gmtime()), "+%d: %.0f" % (k, m), flush=True)
    state = "MODERATE" if LO <= abs(m) < HI else ("CLEAR" if abs(m) < LO else "STILL HARD")
    print(time.strftime("%H:%M:%S", time.gmtime()), "stopped after +%d: %.0f -> %s" % (k, m, state), flush=True)
finally:
    d._write(b"DACZ 32768\n"); time.sleep(0.02); p.close()
