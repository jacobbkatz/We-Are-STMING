"""Approach ONE motor step at a time (NEGATIVE approaches), Z held at 0 during every step.
After each step sweep Z up from 0 in ZSTEP to ZCAP; record where |I| first reaches ONSET, retract to 0.
Stops when the onset reaches Z <= ZSTOP (surface nearly at the retracted end), or contact at Z 0,
or MAXSTEPS. Then retracts the motor +RETRACT steps."""
import sys, time, serial, statistics as st
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
from stm_approach import Device
from stm_feedback_scan import read_averaged
MAXSTEPS, ZSTEP, ZSTOP, RETRACT = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
ONSET, ZCAP = 1000, 50000
port = serial.Serial("COM3", 115200, timeout=0.2)
dev = Device(port)
def sweep():
    z = 0
    while z <= ZCAP:
        dev.set_z(z)
        v = [x for x in (read_averaged(dev) for _ in range(4)) if x is not None]
        if v and abs(st.median(v)) >= ONSET:
            w = [x for x in (read_averaged(dev) for _ in range(8)) if x is not None]
            if w and abs(st.median(w)) >= ONSET:
                dev.set_z(0); return z, st.median(w)
        z += ZSTEP
    dev.set_z(0); return None, None
steps = 0; first = None
try:
    dev._write(b"BIAS 38229\n"); time.sleep(0.1); dev.set_z(0)
    while steps < MAXSTEPS:
        z, i = sweep()
        if z is not None:
            if first is None: first = steps
            print("%s step -%d: onset Z %d (I %.0f)" % (time.strftime("%H:%M:%S", time.gmtime()), steps, z, i), flush=True)
            if z <= ZSTOP:
                print("onset at/below Z %d: stop approaching" % ZSTOP); break
        elif steps % 10 == 0:
            print("%s step -%d: no onset up to %d" % (time.strftime("%H:%M:%S", time.gmtime()), steps, ZCAP), flush=True)
        dev.set_z(0); dev.move_motor(-1); steps += 1; time.sleep(0.2)
    print("approached %d steps; first onset after %s" % (steps, first))
finally:
    dev.set_z(0); time.sleep(0.05)
    if RETRACT: dev.move_motor(RETRACT)
    time.sleep(0.2)
    v = [x for x in (read_averaged(dev) for _ in range(64)) if x is not None]
    print("end: Z 0, retracted +%d, reading at Z 0: mean %.0f" % (RETRACT, st.mean(v)))
    port.close()
