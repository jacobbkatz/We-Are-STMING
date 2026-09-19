"""Power-up baseline, then a GENTLE walk of Z to midscale before the hand-set.

2026-09-19 morning. Jacob turned the side screws IN by an unknown amount before power-up, so
the gold may already be inside the piezo's reach. live_backoff.py jumps Z straight to midscale;
this walks it there in small steps first and stops at the first current.

For the tip fitted ~03:00 UTC 2026-09-19, HIGH Z extends toward the sample
(sessions/2026-09-19-bench.md 3.14), so code 0 is fully retracted and walking up is toward the gold.

1. GSTS, raw.
2. X, Y midscale. Z held at 0 (fully retracted for this tip).
3. ADCR at bias 0, -0.5, +0.5, 0 V: a current that follows the bias sign = contact.
4. At -0.5 V, Z 0 -> 32768 in STEP-count steps. At the first averaged reading >= STOP counts,
   Z goes straight back to 0 and the script says so. Otherwise Z is left at 32768, bias -0.5 V,
   ready for live_backoff.py (which will then not jump).
"""
import sys, time, statistics as st

BIAS_0, BIAS_NEG, BIAS_POS = 32768, 38229, 27307    # 0 V, sample -0.5 V, sample +0.5 V
MID, STEP, STOP = 32768, 64, 1000


def walk(set_z, read, out, z_from=0, z_to=MID, step=STEP, stop=STOP):
    """Walk Z up. Returns ('contact', z) with Z back at z_from, or ('clear', z_to)."""
    z = z_from
    while z < z_to:
        z = min(z + step, z_to)
        set_z(z)
        v = read()
        if v is not None and abs(v) >= stop:
            set_z(z_from)
            out("CONTACT at Z %d: %d counts. Z back to %d." % (z, v, z_from))
            return "contact", z
    out("clear all the way to Z %d" % z_to)
    return "clear", z_to


def self_test():
    """Simulated junction. Contact at Z >= 20000; and a no-contact world."""
    class Fake:
        def __init__(self, zc):
            self.z, self.zc, self.log = 0, zc, []
        def set_z(self, z):
            assert 0 <= z <= 65535
            self.z = z; self.log.append(z)
        def read(self):
            return 5000 if (self.zc is not None and self.z >= self.zc) else 5
    f = Fake(20000)
    res, z = walk(f.set_z, f.read, lambda s: None)
    assert res == "contact" and 20000 <= z < 20000 + STEP, (res, z)
    assert f.z == 0, "must end retracted"
    assert max(f.log) < 20000 + STEP, "must not pass the contact"
    f = Fake(None)
    res, z = walk(f.set_z, f.read, lambda s: None)
    assert res == "clear" and f.z == MID, (res, f.z)
    # A deliberately broken walk (ignores contact) must FAIL the same check.
    def broken(set_z, read, out):
        for z in range(STEP, MID + 1, STEP):
            set_z(z); read()
        return "clear", MID
    f = Fake(20000)
    broken(f.set_z, f.read, lambda s: None)
    assert f.z != 0, "the check must catch a walk that ignores contact"
    print("self-test: pass (contact stops and retracts; clear ends at midscale; broken walk caught)")


if __name__ == "__main__":
    if "--test" in sys.argv:
        self_test(); sys.exit(0)
    import serial
    sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
    from stm_approach import Device, find_teensy
    from stm_feedback_scan import read_averaged
    stamp = lambda: time.strftime("%H:%M:%S", time.gmtime())
    out = lambda s: print(stamp(), s, flush=True)
    port = serial.Serial(find_teensy(), 115200, timeout=0.2)
    dev = Device(port)
    try:
        dev._write(b"GSTS")
        time.sleep(0.3)
        out("GSTS: " + port.read(port.in_waiting or 1).decode("ascii", "replace").strip())
        dev._write(b"DACX 32768\n"); time.sleep(0.02)
        dev._write(b"DACY 32768\n"); time.sleep(0.02)
        dev.set_z(0)
        for name, code in (("0 V", BIAS_0), ("-0.5 V", BIAS_NEG), ("+0.5 V", BIAS_POS), ("0 V", BIAS_0)):
            dev.set_bias(code); time.sleep(0.2)
            v = [x for x in (read_averaged(dev) for _ in range(200)) if x is not None]
            out("Z 0, bias %-6s: mean %7.1f  sd %6.1f  (n %d)" % (name, st.mean(v), st.pstdev(v), len(v)))
        dev.set_bias(BIAS_NEG); time.sleep(0.2)
        def rd():
            v = [x for x in (read_averaged(dev) for _ in range(5)) if x is not None]
            return st.mean(v) if v else None
        res, z = walk(dev.set_z, rd, out)
        out("RESULT: %s at Z %d; bias left at -0.5 V" % (res, z))
    finally:
        port.close()
