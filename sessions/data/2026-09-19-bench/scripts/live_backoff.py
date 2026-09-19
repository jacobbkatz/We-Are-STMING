"""Hand-set with a LIVE back-off: the smallest possible gap.

Z at midscale (direction-neutral), sample -0.5 V throughout.
Phase 1 - approach: at the first average past THRESH, SIX beeps: stop turning in.
Phase 2 - back-off: the bias STAYS ON. While the current is over CLEAR_T, a short beep about every
0.4 s. The operator backs off in tiny steps. When the current has stayed under CLEAR_T for HOLD s:
two short beeps, "CLEAR", and the script ends with the bias still at -0.5 V and Z at midscale, so
the gap is left just outside detection. A contact at -0.5 V saturates the preamp at ~130 nA through
its own feedback, which is electrically harmless (2026-09-17).
"""
import sys, time, statistics as st

THRESH, CLEAR_T, HOLD, MID = 1000, 300, 2.0, 32768


def run(write, read, beep, now, sleep, out, maxtime=900):
    write("DACX 32768\n"); write("DACY 32768\n"); write("DACZ %d\n" % MID)
    write("BIAS 38229\n"); sleep(0.2)
    t0 = now()
    def avg(n):
        v = [x for x in (read() for _ in range(n)) if x is not None]
        return st.mean(v) if v else 0.0
    phase = 1
    clear_since = None
    last_beep = 0.0
    while now() - t0 < maxtime:
        m = avg(120)
        t = now() - t0
        if phase == 1:
            if abs(m) >= THRESH:
                out("%6.1fs %7.0f counts  <<< CONTACT: STOP TURNING IN. Now back off in tiny steps until the beeping stops. >>>" % (t, m))
                beep(6)
                phase = 2
            continue
        if abs(m) >= CLEAR_T:
            clear_since = None
            if now() - last_beep > 0.4:
                beep(1); last_beep = now()
        else:
            if clear_since is None:
                clear_since = now()
                out("%6.1fs %7.0f counts  current gone - hold still" % (t, m))
            elif now() - clear_since >= HOLD:
                out("%6.1fs %7.0f counts  CLEAR for %.0f s: STOP. Leave the room." % (t, m, HOLD))
                beep(2)
                return "clear"
    return "timeout"


if __name__ == "__main__":
    import serial, winsound
    sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
    from stm_approach import Device, find_teensy
    from stm_feedback_scan import read_averaged
    port = serial.Serial(find_teensy(), 115200, timeout=0.2)
    dev = Device(port)

    def beep(n):
        for _ in range(n):
            winsound.Beep(1500, 300 if n > 2 else 120)
            if n > 1:
                time.sleep(0.1)

    try:
        res = run(lambda s: (dev._write(s.encode()), time.sleep(0.02)), lambda: read_averaged(dev), beep,
                  time.time, time.sleep, lambda s: print(time.strftime("%H:%M:%S", time.gmtime()), s, flush=True))
        print("RESULT:", res, flush=True)
    finally:
        port.close()
