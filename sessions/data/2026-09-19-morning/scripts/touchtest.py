"""Is the 'in range while the hand is on the screw' signal real current, or pickup from the hand?

2026-09-19 morning, nudge_run1: every nudge gave ONE sweep of 'IN' at a random Z (18000, 31000,
4000, 47000, 45000, 6000) and FAR as soon as the hand let go. Two readings:
  FLEX   - finger pressure moves the gold into tunnelling range: the current FLIPS SIGN with the bias
  PICKUP - the hand couples into the preamp input (STATUS.md safety rule 9): does NOT follow the bias

Z fixed at Z_HOLD (lowish, so flex is less likely to become a hard contact); the sample bias
alternates -0.5 V / +0.5 V every half-period, N ADCR each. Every period prints
  flip   = (I(-0.5) - I(+0.5)) / 2      real current lives here
  common = (I(-0.5) + I(+0.5)) / 2      pickup lives here (and in the scatter)
Operator: hands off 6 s, TOUCH the screw head (no turning) 6 s, off 6 s, touch 6 s, off 6 s.
Watchdog: any |I| >= HARD -> Z 0 and bias 0 V, stop.
"""
import sys, time, statistics as st

Z_HOLD, N, HARD, DURATION = 20000, 40, 8000, 34.0
NEG, POS, ZERO = 38229, 27307, 32768


def main():
    import serial, winsound
    sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
    from stm_approach import Device, find_teensy
    from stm_feedback_scan import read_averaged
    port = serial.Serial(find_teensy(), 115200, timeout=0.2)
    dev = Device(port)
    t0 = time.time()
    out = lambda s: print("%6.1fs %s" % (time.time() - t0, s), flush=True)
    try:
        dev._write(b"DACX 32768\n"); time.sleep(0.02)
        dev._write(b"DACY 32768\n"); time.sleep(0.02)
        dev.set_z(0); time.sleep(0.1)
        for z in range(1000, Z_HOLD + 1, 1000):          # no big jump (zjump_run1: spikes)
            dev._write(("DACZ %d\n" % z).encode()); time.sleep(0.01)
        time.sleep(0.2)
        cues = [(0, "HANDS OFF"), (6, "TOUCH the screw head, do NOT turn"), (12, "HANDS OFF"),
                (18, "TOUCH again, do NOT turn"), (24, "HANDS OFF"), (30, "stay off")]
        ci = 0
        winsound.Beep(1200, 200)
        while time.time() - t0 < DURATION:
            t = time.time() - t0
            while ci < len(cues) and t >= cues[ci][0]:
                out("---- %s ----" % cues[ci][1])
                winsound.Beep(700 if "OFF" in cues[ci][1] else 1600, 250)
                ci += 1
            r = {}
            for name, code in (("neg", NEG), ("pos", POS)):
                dev.set_bias(code)
                v = [x for x in (read_averaged(dev) for _ in range(N)) if x is not None]
                r[name] = (st.mean(v), st.pstdev(v), max(abs(x) for x in v))
                if r[name][2] >= HARD:
                    dev.set_z(0); dev.set_bias(ZERO)
                    out("WATCHDOG: %.0f counts -> Z 0, bias 0 V" % r[name][2])
                    return
            flip = (r["neg"][0] - r["pos"][0]) / 2
            common = (r["neg"][0] + r["pos"][0]) / 2
            out("I(-) %7.1f sd %5.1f | I(+) %7.1f sd %5.1f | flip %7.1f  common %7.1f"
                % (r["neg"][0], r["neg"][1], r["pos"][0], r["pos"][1], flip, common))
        winsound.Beep(1200, 200)
    finally:
        try:
            dev.set_z(0); dev.set_bias(NEG)
        except Exception:
            pass
        port.close()
        print("end: Z 0, bias -0.5 V", flush=True)


if __name__ == "__main__":
    # Added 2026-09-19 after a --test run of a script WITHOUT a self-test went straight to its
    # hardware path (no port was connected, so nothing was sent). Unknown options now refuse.
    _bad = [a for a in sys.argv[1:] if a.startswith('-') and a not in []]
    if _bad:
        sys.exit('refusing unknown option(s) %s: this script drives the instrument%s'
                 % (_bad, '' if False else ' and has NO self-test'))
    main()
