import sys, time, serial, statistics as st
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
from stm_approach import Device
secs = float(sys.argv[1]); label = sys.argv[2]
port = serial.Serial("COM3", 115200, timeout=0.2)
dev = Device(port)
raw = []; avg = []
t0 = time.time()
while time.time() - t0 < secs:
    v = dev.read_adc()
    if v is not None: raw.append(v)
    # averaged read: ADCR
    port.reset_input_buffer(); port.write(b"ADCR"); port.flush()
    line = port.readline().decode("ascii", "replace").strip()
    try: avg.append(int(line))
    except ValueError: pass
port.close()
print("%s: %.0f s  raw GSTS n=%d mean %.0f sd %.0f | ADCR n=%d mean %.0f sd %.0f" % (
    label, secs, len(raw), st.mean(raw), st.pstdev(raw), len(avg), st.mean(avg), st.pstdev(avg)))
