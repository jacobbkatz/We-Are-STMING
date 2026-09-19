"""Where is the gold, over time, with nothing else moving? Every cycle: from Z 50000 down in
1000-count steps (16 reads each) until |I| >= 1000, record that Z (or none), return to 50000,
pause. Summary every 30 s. Bias -0.5 V. Exit: Z 50000, bias 0 V. No motor."""
import sys, time, statistics as st
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
import serial
from stm_approach import Device, find_teensy
from stm_feedback_scan import read_averaged
SECS, OUT = float(sys.argv[1]), sys.argv[2]
p = serial.Serial(find_teensy(), 115200, timeout=0.2); d = Device(p); rows = []
ts = lambda: time.strftime("%H:%M:%S", time.gmtime())
try:
    d._write(b"BIAS 38229\n"); time.sleep(0.1)
    t0 = time.time(); chunk = []; next_rep = t0 + 30
    while time.time() - t0 < SECS:
        onset, first = None, None
        for z in range(50000, -1, -1000):
            d._write(("DACZ %d\n" % z).encode()); time.sleep(0.003)
            v = [x for x in (read_averaged(d) for _ in range(16)) if x is not None]
            m = st.median(v)
            if first is None: first = m
            if abs(m) >= 1000:
                onset = z; break
        d._write(b"DACZ 50000\n")
        t = round(time.time() - t0, 1)
        rows.append((t, onset, round(first)))
        chunk.append(onset)
        if time.time() >= next_rep:
            found = [c for c in chunk if c is not None]
            at_top = sum(1 for c in chunk if c == 50000)
            print(ts(), "t=%4.0fs  sweeps %d  found %d (at Z 50000 itself: %d)  onset median %s  min %s  max %s" % (
                t, len(chunk), len(found), at_top,
                st.median(found) if found else "-", min(found) if found else "-", max(found) if found else "-"), flush=True)
            chunk = []; next_rep += 30
        time.sleep(0.3)
finally:
    d._write(b"DACZ 50000\n"); time.sleep(0.02); d._write(b"BIAS 32768\n"); time.sleep(0.05); p.close()
    with open(OUT, "w") as f:
        f.write("t,onset_z,first_reading_at_50000\n")
        for r in rows: f.write("%s,%s,%s\n" % r)
    print("end: Z 50000, bias 0 V; %d sweeps" % len(rows))
