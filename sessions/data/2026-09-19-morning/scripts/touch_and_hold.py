"""Hand-set WITHOUT a hand back-off: turn in until the beeps, then STOP. The laptop does the rest.

2026-09-19 morning. Why: a 1/4-80 side screw moves ~0.9 um per DEGREE, and the piezo's whole Z
range is ~1 um (inherited scale), so any hand back-off overshoots the piezo's reach - it did this
morning (ztest_run1: nothing up to Z 62000 after a live back-off) and on 2026-09-19 at 03:41.
On 2026-09-19 what worked was a contact followed by single MOTOR retract steps (pinned 23 steps,
clear on the 24th), after which the gold was inside the Z range.

Z at midscale (32768), sample -0.5 V. At the first averaged reading >= THRESH:
  Z -> 0 at once (fully retracted for the tip fitted ~03:00 UTC 2026-09-19), SIX beeps,
  "STOP TURNING. Hands off. Leave the room." Then WATCH s of readings at Z 0, logged, and exit.
The next step (backoff_motor.py, or ztest.py from Z 0) is run separately.

Usage: py touch_and_hold.py      py touch_and_hold.py --test
"""
import sys, time, statistics as st

THRESH, MID, WATCH = 1000, 32768, 60.0


def run(write, read, beep, now, sleep, out, maxtime=900):
    write("DACX 32768\n"); write("DACY 32768\n"); write("DACZ %d\n" % MID)
    write("BIAS 38229\n"); sleep(0.2)
    t0 = now()
    while now() - t0 < maxtime:
        v = [x for x in (read() for _ in range(60)) if x is not None]
        m = st.mean(v) if v else 0.0
        if abs(m) >= THRESH:
            write("DACZ 0\n")
            out("%6.1fs %7.0f counts  <<< CONTACT. STOP TURNING. Hands off. Leave the room. >>>"
                % (now() - t0, m))
            beep(6)
            t1 = now()
            while now() - t1 < WATCH:
                v = [x for x in (read() for _ in range(60)) if x is not None]
                out("   Z 0: %7.0f counts" % (st.mean(v) if v else float("nan")))
                sleep(5.0)
            return "contact"
    return "timeout"


def self_test():
    class W:
        def __init__(self, t_touch):
            self.t, self.z, self.log, self.tt = 0.0, None, [], t_touch
        def write(self, s):
            self.log.append(s.strip())
            if s.startswith("DACZ"):
                self.z = int(s.split()[1])
        def read(self):
            self.t += 0.002
            return 20000 if (self.t >= self.tt and self.z == MID) else 3
        def now(self): return self.t
        def sleep(self, s): self.t += s
    w = W(30.0)
    res = run(w.write, w.read, lambda n: None, w.now, w.sleep, lambda s: None)
    assert res == "contact" and w.z == 0, (res, w.z)
    i = w.log.index("DACZ 0")
    assert all(not s.startswith("DACZ") or s == "DACZ 0" for s in w.log[i:]), "Z must stay retracted"
    w = W(1e9)
    res = run(w.write, w.read, lambda n: None, w.now, w.sleep, lambda s: None, maxtime=100)
    assert res == "timeout" and w.z == MID
    print("self-test: pass (contact -> Z 0 and stays; timeout leaves midscale)")


if __name__ == "__main__":
    # Added 2026-09-19 after a --test run of a script WITHOUT a self-test went straight to its
    # hardware path (no port was connected, so nothing was sent). Unknown options now refuse.
    _bad = [a for a in sys.argv[1:] if a.startswith('-') and a not in ['--test']]
    if _bad:
        sys.exit('refusing unknown option(s) %s: this script drives the instrument%s'
                 % (_bad, '' if True else ' and has NO self-test'))
    if "--test" in sys.argv:
        self_test(); sys.exit(0)
    import serial, winsound
    sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
    from stm_approach import Device, find_teensy
    from stm_feedback_scan import read_averaged
    port = serial.Serial(find_teensy(), 115200, timeout=0.2)
    dev = Device(port)

    def beep(n):
        for _ in range(n):
            winsound.Beep(1500, 300)
            time.sleep(0.1)
    try:
        res = run(lambda s: (dev._write(s.encode()), time.sleep(0.02)), lambda: read_averaged(dev),
                  beep, time.time, time.sleep,
                  lambda s: print(time.strftime("%H:%M:%S", time.gmtime()), s, flush=True))
        print("RESULT:", res, flush=True)
    finally:
        port.close()
