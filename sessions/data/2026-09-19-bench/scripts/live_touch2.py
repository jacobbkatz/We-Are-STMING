"""Hand-set beeper, direction-neutral.

Z parked at MIDSCALE (the Z direction of this tip is unknown, so no Z move is known to retract).
Sample -0.5 V. The current is read continuously. At the first average past THRESH:
  * the BIAS goes to 0 V at once (no current can flow; nothing mechanical moves),
  * SIX beeps: STOP TURNING,
  * latched. After WAIT s the bias returns to -0.5 V for a check:
      clear   -> two short beeps, and the script ends;
      touching -> six beeps again, bias back to 0 V, check again after WAIT s (up to 10 times).
Exit: bias 0 V, Z midscale. Nothing here moves the motor.
"""
import sys, time, statistics as st

THRESH = 1000
MID = 32768


def run(write, read, beep, now, sleep, out, maxtime=900, wait=20):
    write("DACX 32768\n"); write("DACY 32768\n"); write("DACZ %d\n" % MID)
    write("BIAS 38229\n"); sleep(0.2)
    t0 = now()
    try:
        while now() - t0 < maxtime:
            v = [x for x in (read() for _ in range(200)) if x is not None]
            if not v:
                continue
            m = st.mean(v)
            if abs(m) >= THRESH:
                write("BIAS 32768\n")
                out("%6.1fs  %7.0f counts  <<< CONTACT: STOP TURNING. Bias set to 0 V. >>>" % (now() - t0, m))
                beep(6)
                for attempt in range(10):
                    sleep(wait)
                    write("BIAS 38229\n"); sleep(0.2)
                    c = st.mean([x for x in (read() for _ in range(400)) if x is not None])
                    if abs(c) < 300:
                        write("BIAS 32768\n")
                        out("%6.1fs  check: %.0f counts -> CLEAR" % (now() - t0, c))
                        beep(2)
                        return "clear"
                    write("BIAS 32768\n")
                    out("%6.1fs  check: %.0f counts -> STILL TOUCHING, back off a hair more" % (now() - t0, c))
                    beep(6)
                return "still touching"
            out("%6.1fs  %7.0f counts" % (now() - t0, m))
        return "timeout"
    finally:
        write("BIAS 32768\n"); write("DACZ %d\n" % MID)


if __name__ == "__main__":
    import serial, winsound
    sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
    from stm_approach import Device, find_teensy
    from stm_feedback_scan import read_averaged
    port = serial.Serial(find_teensy(), 115200, timeout=0.2)
    dev = Device(port)

    def beep(n):
        for _ in range(n):
            winsound.Beep(1500, 300 if n > 2 else 150)
            time.sleep(0.1)

    try:
        res = run(lambda s: (dev._write(s.encode()), time.sleep(0.02)), lambda: read_averaged(dev), beep,
                  time.time, time.sleep,
                  lambda s: print(time.strftime("%H:%M:%S", time.gmtime()), s, flush=True))
        print("RESULT:", res, flush=True)
    finally:
        port.close()
