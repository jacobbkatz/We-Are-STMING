"""Let the creep do the approaching, and record it.

Motor still, Z parked at midscale. Every PERIOD s: sweep midscale -> ZLO and midscale -> ZHI in
STEP-count steps (16 reads, median), alternating which half goes first. The first point where
|I| >= THRESH is a TOUCH: record (time, Z, which half), return Z to midscale, MTMV +K (retract),
check midscale is clear (up to 5 more retracts of K), and carry on.
The intervals between touches x K = the creep rate; the half each touch lands in = the Z direction
(a slowly arriving surface meets the tip first where the tip reaches furthest).
Exit: Z midscale, bias 0 V.
"""
import sys, time, statistics as st

MID, ZLO, ZHI, STEP, THRESH = 32768, 2000, 63000, 1000, 1000


def cycle(dev, read_med, order):
    """Returns (z_hit, half) or (None, None). Z is left at midscale."""
    for half in order:
        end = ZLO if half == "low" else ZHI
        step = -STEP if half == "low" else STEP
        z = MID + step
        while (z >= end) if half == "low" else (z <= end):
            dev.set_z(z)
            if abs(read_med(16)) >= THRESH:
                dev.set_z(MID)
                return z, half
            z += step
        dev.set_z(MID)
    return None, None


def run(dev, read_med, now, sleep, secs, period, k, log):
    touches = []
    t0 = now()
    n = 0
    dev.set_bias(38229)
    dev.set_z(MID)
    while now() - t0 < secs:
        tc = now()
        order = ("low", "high") if n % 2 == 0 else ("high", "low")
        n += 1
        if abs(read_med(32)) >= THRESH:
            z, half = MID, "midscale"
        else:
            z, half = cycle(dev, read_med, order)
        if z is not None:
            t = now() - t0
            touches.append((round(t, 1), z, half))
            dev.set_z(MID)
            dev.motor(k)
            extra = 0
            while abs(read_med(32)) >= THRESH and extra < 5:
                dev.motor(k)
                extra += 1
            log("t=%6.1fs TOUCH at Z %d (%s half, sweep order %s) -> retracted +%d" % (
                t, z, half, "/".join(order), k * (1 + extra)))
            if extra >= 5:
                log("STILL IN CONTACT after %d retract steps: stopping" % (k * 6))
                break
        sleep(max(0.0, period - (now() - tc)))
    dev.set_z(MID)
    dev.set_bias(32768)
    return touches


if __name__ == "__main__":
    import serial
    sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
    from stm_approach import Device, find_teensy
    from stm_feedback_scan import read_averaged
    secs, period, k, out = float(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    port = serial.Serial(find_teensy(), 115200, timeout=0.2)
    d = Device(port)

    class Dev:
        def set_z(self, z): d._write(("DACZ %d\n" % z).encode()); time.sleep(0.002)
        def set_bias(self, c): d._write(("BIAS %d\n" % c).encode()); time.sleep(0.05)
        def motor(self, n): d.move_motor(n)

    def read_med(nr):
        v = [x for x in (read_averaged(d) for _ in range(nr)) if x is not None]
        return st.median(v) if v else 0

    log = lambda s: print(time.strftime("%H:%M:%S", time.gmtime()), s, flush=True)
    touches = []
    try:
        touches = run(Dev(), read_med, time.time, time.sleep, secs, period, k, log)
    finally:
        d._write(("DACZ %d\n" % MID).encode()); time.sleep(0.02); d._write(b"BIAS 32768\n"); time.sleep(0.05)
        port.close()
        with open(out, "w") as f:
            f.write("t,z,half\n")
            for r in touches: f.write("%s,%s,%s\n" % r)
        log("end: Z midscale, bias 0 V; %d touches" % len(touches))
