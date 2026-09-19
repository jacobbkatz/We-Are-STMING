"""The laptop as a nano-amp continuity beeper, for hand-setting the gap with power ON.

Holds Z at HOME (10000, the approach tool's retracted start) and the sample at -0.5 V, and
prints the current about four times a second. The moment the averaged current passes THRESH
(1000 counts, about 3 nA -- a far lighter touch than a meter's beep, which needs a near-short):
  * Z is pulled to 0, the fully retracted end, at once;
  * the laptop beeps and prints CONTACT -- STOP TURNING;
  * the alarm LATCHES: it keeps warning even if the current drops, so a retract that makes the
    reading fall cannot be mistaken for "all clear".
After a latch it keeps reading at Z 0 so the operator can back off until the reading is clean.
Exit (Ctrl-C, or MAXTIME): Z 0, bias 0 V. Nothing here moves the motor.
"""
import sys
import time
import statistics as st

THRESH = 1000
HOME = 10000
BIAS_NEG, BIAS_ZERO = 38229, 32768
MAXTIME = float(sys.argv[1]) if len(sys.argv) > 1 else 900.0


def run(dev_write, read, beep, now=time.time, out=print, maxtime=MAXTIME):
    dev_write("DACX 32768\n"); dev_write("DACY 32768\n")
    dev_write("DACZ %d\n" % HOME)
    dev_write("BIAS %d\n" % BIAS_NEG)
    time.sleep(0.2)
    latched = False
    z = HOME
    t0 = now()
    last_beep = 0.0
    try:
        while now() - t0 < maxtime:
            vals = [v for v in (read() for _ in range(200)) if v is not None]
            if not vals:
                continue
            m = st.mean(vals)
            t = now() - t0
            if not latched and abs(m) >= THRESH:
                dev_write("DACZ 0\n")
                z = 0
                latched = True
                out("%6.1fs  %7.0f counts  %6.2f nA   <<< CONTACT -- STOP TURNING. Z pulled back to 0. >>>"
                    % (t, m, m / 320.5))
                beep(); last_beep = now()
                continue
            tag = ""
            if latched:
                tag = "   LATCHED at Z 0 -- %s" % ("still touching, back off a hair" if abs(m) >= THRESH
                                                   else "clear at Z 0 now")
                if now() - last_beep > 2.0 and abs(m) >= THRESH:
                    beep(); last_beep = now()
            out("%6.1fs  %7.0f counts  %6.2f nA%s" % (t, m, m / 320.5, tag))
    finally:
        dev_write("DACZ 0\n")
        dev_write("BIAS %d\n" % BIAS_ZERO)
        out("end: Z 0 (fully retracted), bias 0 V. Latched: %s" % latched)
    return latched


if __name__ == "__main__":
    import serial
    import winsound
    sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
    from stm_approach import Device, find_teensy
    from stm_feedback_scan import read_averaged
    port = serial.Serial(find_teensy(), 115200, timeout=0.2)
    dev = Device(port)
    try:
        run(lambda s: (dev._write(s.encode()), time.sleep(0.02)),
            lambda: read_averaged(dev),
            lambda: winsound.Beep(1800, 400),
            out=lambda s: print(time.strftime("%H:%M:%S", time.gmtime()), s, flush=True))
    finally:
        port.close()
