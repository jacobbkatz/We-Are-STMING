"""Measure ADCR noise every `every` s (tip clear, -0.5 V); exit when sd < target or at deadline."""
import sys, time, serial, statistics as st
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
from stm_approach import Device
from stm_feedback_scan import read_averaged
target = float(sys.argv[1]); every = float(sys.argv[2]); deadline = time.time() + float(sys.argv[3])
while True:
    port = serial.Serial("COM3", 115200, timeout=0.2)
    dev = Device(port)
    vals = []; t0 = time.time()
    while time.time() - t0 < 3:
        v = read_averaged(dev)
        if v is not None: vals.append(v)
    port.close()
    sd = st.pstdev(vals)
    print(time.strftime("%H:%M:%S", time.gmtime()), "n=%d mean %.0f sd %.0f" % (len(vals), st.mean(vals), sd), flush=True)
    if sd < target:
        print("SETTLED"); break
    if time.time() > deadline:
        print("DEADLINE, not settled"); break
    time.sleep(every)
