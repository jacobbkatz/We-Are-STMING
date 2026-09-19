"""Passive log of the contact at Z 0: NOTHING moves. One DACZ 0 at the start, then ADCR only.
2026-09-19 morning, 13:09: the gold pressed on the tip at full retraction after +1200 retract steps.
Logs every state change (railed >= 32000 / contact >= 200 / clear) and a line every 60 s."""
import sys, time, statistics as st
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")

if __name__ == "__main__":
    import serial, csv
    from stm_approach import Device, find_teensy
    from stm_feedback_scan import read_averaged
    maxtime = float(sys.argv[1]) if len(sys.argv) > 1 else 1800
    port = serial.Serial(find_teensy(), 115200, timeout=0.2)
    dev = Device(port)
    rows, t0, last, last_line = [], time.time(), None, -1e9
    stamp = lambda: time.strftime("%H:%M:%S", time.gmtime())
    try:
        dev.set_z(0); dev.set_bias(38229); time.sleep(0.2)
        while time.time() - t0 < maxtime:
            v = [x for x in (read_averaged(dev) for _ in range(20)) if x is not None]
            m = st.mean(v) if v else float("nan")
            t = time.time() - t0
            rows.append((round(t, 1), round(m, 1)))
            state = "RAILED" if abs(m) >= 32000 else ("CONTACT" if abs(m) >= 200 else "CLEAR")
            if state != last or t - last_line >= 60:
                print(stamp(), "%6.0fs Z 0: %8.1f counts  %s" % (t, m, state), flush=True)
                last, last_line = state, t
            time.sleep(5.0)
    finally:
        port.close()
        with open("passive_z0_%d.csv" % int(t0), "w", newline="") as f:
            w = csv.writer(f); w.writerow(["t", "adc_mean20"]); w.writerows(rows)
