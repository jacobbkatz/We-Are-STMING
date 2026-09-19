"""The 2026-09-19 live back-off, with Z held FULLY RETRACTED (code 0) instead of midscale.

Why. With Z at midscale, "silence" leaves the gold just beyond the tip at HALF extension, so any hand
overshoot past ~half the Z range puts it out of the piezo's reach - which happened at 11:24 this
morning (ztest_run1: nothing up to Z 62000) and at 03:41 on 2026-09-19. A 1/4-80 side screw moves
~0.9 um per degree and the whole Z range is ~1 um (inherited scale). With Z at 0 (fully retracted
for the tip fitted ~03:00 UTC 2026-09-19), "silence" leaves the gold just beyond the RETRACTED tip,
so the WHOLE Z range can reach it: twice the tolerance for overshoot. If there is no overshoot at
all, the gold sits at the bottom of the range and single motor RETRACT steps (no backlash - the
motor's last moves were retracts) open it up a few nm at a time.

Same tested code as sessions/data/2026-09-19-bench/scripts/live_backoff.py (and its test,
live_backoff_test.py); only the module constant MID is changed before run().
"""
import sys, time
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\sessions\data\2026-09-19-bench\scripts")
import live_backoff

live_backoff.MID = 0

if __name__ == "__main__":
    # Added 2026-09-19 after a --test run of a script WITHOUT a self-test went straight to its
    # hardware path (no port was connected, so nothing was sent). Unknown options now refuse.
    _bad = [a for a in sys.argv[1:] if a.startswith('-') and a not in []]
    if _bad:
        sys.exit('refusing unknown option(s) %s: this script drives the instrument%s'
                 % (_bad, '' if False else ' and has NO self-test'))
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
        res = live_backoff.run(lambda s: (dev._write(s.encode()), time.sleep(0.02)),
                               lambda: read_averaged(dev), beep, time.time, time.sleep,
                               lambda s: print(time.strftime("%H:%M:%S", time.gmtime()), s, flush=True))
        print("RESULT:", res, "(Z held at %d)" % live_backoff.MID, flush=True)
    finally:
        port.close()
