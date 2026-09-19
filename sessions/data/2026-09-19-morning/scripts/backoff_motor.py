"""Back the motor off ONE step at a time until the contact clears. Z fully retracted throughout.

2026-09-19 morning. For when the gold is in contact even with Z fully retracted (the piezo cannot
pull away). For the tip fitted ~03:00 UTC 2026-09-19: Z code 0 is fully retracted, and POSITIVE
MTMV retracts (sessions/2026-09-19-bench.md: +200 cleared contacts three times).

Each step: MTMV +1 (blocking, waited out), then NREAD averaged ADCR at Z 0, sample -0.5 V.
Stops when CONFIRM consecutive readings are under CLEAR, or after MAX steps (then says so).
Last night a contact stayed pinned for 23 single retract steps and cleared on the 24th, so the
default allows 80.

Usage: py backoff_motor.py [max_steps]      py backoff_motor.py --test
"""
import sys, time, statistics as st

CLEAR, CONFIRM, NREAD = 150, 3, 10


def run(move1, read_mean, out, max_steps=80):
    """Returns (status, steps). status 'clear' or 'limit'."""
    ok = 0
    for n in range(1, max_steps + 1):
        move1()
        m = read_mean()
        ok = ok + 1 if (m is not None and abs(m) < CLEAR) else 0
        out("step +%d: %s counts" % (n, "None" if m is None else "%.0f" % m))
        if ok >= CONFIRM:
            return "clear", n
    return "limit", max_steps


def self_test():
    class Fake:
        def __init__(self, k): self.k, self.n = k, 0
        def move1(self): self.n += 1
        def read(self): return 5 if self.n >= self.k else 20000
    f = Fake(24)
    res, n = run(f.move1, f.read, lambda s: None)
    assert res == "clear" and n == 24 + CONFIRM - 1, (res, n)
    f = Fake(500)
    res, n = run(f.move1, f.read, lambda s: None, max_steps=80)
    assert res == "limit" and f.n == 80, (res, f.n)
    # red: a version that stops on the first low reading must fail the CONFIRM expectation
    class Flicker(Fake):
        def read(self):
            return 5 if self.n in (3,) or self.n >= self.k else 20000
    f = Flicker(24)
    res, n = run(f.move1, f.read, lambda s: None)
    assert n >= 24, "a single flicker must not end the back-off (n=%d)" % n
    print("self-test: pass (clears at 24 + confirm; stops at the limit; one flicker ignored)")


if __name__ == "__main__":
    if "--test" in sys.argv:
        self_test(); sys.exit(0)
    import serial
    sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
    from stm_approach import Device, find_teensy
    from stm_feedback_scan import read_averaged
    mx = int(sys.argv[1]) if len(sys.argv) > 1 else 80
    stamp = lambda: time.strftime("%H:%M:%S", time.gmtime())
    out = lambda s: print(stamp(), s, flush=True)
    port = serial.Serial(find_teensy(), 115200, timeout=0.2)
    dev = Device(port)
    try:
        dev.set_z(0)
        dev.set_bias(38229); time.sleep(0.2)

        def rd():
            v = [x for x in (read_averaged(dev) for _ in range(NREAD)) if x is not None]
            return st.mean(v) if v else None
        out("start: %.0f counts at Z 0" % (rd() or float("nan")))
        res, n = run(lambda: dev.move_motor(+1), rd, out, max_steps=mx)
        out("RESULT: %s after %d retract steps (Z 0, bias -0.5 V)" % (res, n))
    finally:
        port.close()
