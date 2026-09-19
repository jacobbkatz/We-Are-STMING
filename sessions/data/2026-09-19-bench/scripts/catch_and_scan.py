"""Wait for the creeping gold to come into reach, learn the Z direction there, and scan at once.

Motor still, Z parked at MIDSCALE, sample -0.5 V. Every PERIOD s: sweep midscale -> ZLO and
midscale -> ZHI in STEP counts (median of 16), alternating the order. At the FIRST touch:
  1. lock-in at the touch Z (creeptrack2.lockin): Z toggled +-500, 40 times -> the direction,
     accepted only if |diff| > 3 standard errors. Otherwise: back to midscale, wait for the next
     touch (the lock-in is repeated at every touch until it decides).
  2. With the direction decided: scan2.scan() REPS times (constant current, the tested Loop with
     the sign), then the SAME timing with X held still (the control), alternating, while each
     scan finds the surface and does not abort.
  3. Retract Z to the retracted end for that direction and set the bias to 0 V. The script then
     ends; it never moves the motor.
Exit: Z at the retracted end if the direction is known, else midscale; bias 0 V.
"""
import sys, time, math, statistics as st

MID, ZLO, ZHI, STEP, THRESH = 32768, 2000, 63000, 1000, 1000
BIAS = 38229


def sweep(dev, med, order):
    for half in order:
        end, step = (ZLO, -STEP) if half == "low" else (ZHI, STEP)
        z = MID + step
        while (z >= end) if half == "low" else (z <= end):
            dev.set_z(z)
            if abs(med(16)) >= THRESH:
                return z, half
            z += step
        dev.set_z(MID)
    return None, None


def run(dev, med, lockin, scan_fn, now, sleep, log, secs=1800, period=3, reps=4, ret=200, chmap_fn=None):
    dev.set_bias(BIAS); dev.set_z(MID)
    t0 = now(); n = 0; toward = None; scans = []; undecided = 0
    while now() - t0 < secs and toward is None:
        tc = now()
        order = ("low", "high") if n % 2 == 0 else ("high", "low"); n += 1
        if abs(med(32)) >= THRESH:
            z, half = MID, "midscale"
        else:
            z, half = sweep(dev, med, order)
        if z is not None:
            lo, hi, diff, se = lockin(dev, med, z)
            call = +1 if diff > 3 * se else (-1 if diff < -3 * se else 0)
            if call == 0 and hasattr(lockin, "__module__"):
                # Undecided at +-500: the Z response may just be weak. Retry once at +-2000.
                import creeptrack2 as _ct
                saved = _ct.LI_D; _ct.LI_D = 2000
                try:
                    lo, hi, diff, se = lockin(dev, med, z)
                finally:
                    _ct.LI_D = saved
                call = +1 if diff > 3 * se else (-1 if diff < -3 * se else 0)
                log("   retry at +-2000: I(-)%.0f I(+)%.0f diff %+.0f se %.0f" % (lo, hi, diff, se))
            log("t=%6.1fs TOUCH Z %d (%s) lock-in I(-)%.0f I(+)%.0f diff %+.0f se %.0f -> %s" % (
                now() - t0, z, half, lo, hi, diff, se, {1: "HIGH toward", -1: "LOW toward", 0: "undecided"}[call]))
            dev.set_z(MID)
            if call != 0:
                toward = call
                break
            # No Z control at this touch: take the data that does not need it, at the touch Z.
            if chmap_fn is not None:
                undecided += 1
                if undecided <= 3:
                    chmap_fn(z, undecided)
        sleep(max(0.0, period - (now() - tc)))
    if toward is None:
        log("no decided touch in %.0f s" % (now() - t0))
        dev.set_z(MID); dev.set_bias(32768)
        return None, scans
    zr = 10000 if toward > 0 else 55000
    t_s = now(); r = 0; waited = 0
    while r < reps and now() - t_s < 180:
        rows, loop = scan_fn(dev, toward, False)
        if rows is None:
            # The creeping surface first comes into reach at the far end of the Z range, outside the
            # loop's safe window: pull back and try again as the creep brings it into the window.
            dev.set_z(zr); waited += 1
            sleep(1.0)
            continue
        zs = [v for _, f, b in rows for v in f + b]
        log("scan %d (after %d retries): %d lines, Z %d..%d, saturated %d, clamped %d" % (
            r, waited, len(rows), min(zs), max(zs), loop.saturated, loop.clamped))
        scans.append((r, False, rows, loop.saturated, loop.clamped))
        rows2, loop2 = scan_fn(dev, toward, True)
        if rows2 is not None:
            zs2 = [v for _, f, b in rows2 for v in f + b]
            log("X-HELD control %d: %d lines, Z %d..%d, saturated %d, clamped %d" % (
                r, len(rows2), min(zs2), max(zs2), loop2.saturated, loop2.clamped))
            scans.append((r, True, rows2, loop2.saturated, loop2.clamped))
        r += 1
        if len(rows) < 3:
            log("scan aborted early: stopping")
            break
    if not scans:
        log("the surface never came into the loop's window in %.0f s" % (now() - t_s))
    zr = 10000 if toward > 0 else 55000
    dev.set_z(zr)
    dev.set_bias(32768)
    return toward, scans


if __name__ == "__main__":
    import serial
    sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
    sys.path.insert(0, r"C:\Users\jacob\AppData\Local\Temp\claude\C--Users-jacob-OneDrive-Desktop-CUsersyournameSTM\851972b6-d618-4bb1-ba1f-dc9b1865615d\scratchpad")
    import stm_feedback_scan as fs
    import scan2, creeptrack2
    from stm_approach import Device, find_teensy
    from stm_feedback_scan import read_averaged
    secs, reps, prefix = float(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    half, step, nlines, setpoint, cpd = 1500, 150, 11, 1000.0, 100.0
    fs.COUNTS_PER_DECADE = cpd
    port = serial.Serial(find_teensy(), 115200, timeout=0.2)
    d = Device(port)

    class Dev:
        def set_z(self, z): d._write(("DACZ %d\n" % int(z)).encode()); time.sleep(0.002)
        def set_bias(self, c): d._write(("BIAS %d\n" % c).encode()); time.sleep(0.05)
        def motor(self, n): d.move_motor(n)

    def med(nr):
        v = [x for x in (read_averaged(d) for _ in range(nr)) if x is not None]
        return st.median(v) if v else 0

    log = lambda s: print(time.strftime("%H:%M:%S", time.gmtime()), s, flush=True)
    toward, scans = None, []
    try:
        import chmap

        def chmap_fn(z, k):
            wr = lambda s_: (d._write(s_.encode()), time.sleep(0.002))
            rd = lambda: read_averaged(d)
            for xh in (False, True, False):
                t_ = time.time()
                xs_, rows_ = chmap.cmap(wr, rd, z, xheld=xh)
                tag = "chmap_t%d_%s" % (k, "xheld" if xh else "scan")
                fn = "%s_%s_%d.csv" % (prefix, tag, int(t_))
                with open(fn, "w") as f:
                    f.write("y,dir," + ",".join(str(x) for x in xs_) + chr(10))
                    for y, fw, bk in rows_:
                        f.write("%d,fwd,%s" % (y, ",".join(map(str, fw))) + chr(10))
                        f.write("%d,back,%s" % (y, ",".join(map(str, bk))) + chr(10))
                allv = [v for _, fw, bk in rows_ for v in fw + bk]
                log("   constant-height map (%s) at Z %d in %.1f s: current %d..%d, mean %.0f -> %s" % (
                    "X HELD" if xh else "X moving", z, time.time() - t_, min(allv), max(allv), sum(allv) / len(allv), fn))
            curve = chmap.iv(wr, rd, z)
            log("   I-V at Z %d (V:counts): %s" % (z, " ".join("%+.1f:%d" % p for p in curve)))
            wr("DACZ %d" % MID + chr(10))

        toward, scans = run(Dev(), med, creeptrack2.lockin,
                            lambda dev, tw, xh: scan2.scan(d, tw, half, step, nlines, setpoint, xheld=xh, log=log),
                            time.time, time.sleep, log, secs=secs, reps=reps, chmap_fn=chmap_fn)
    finally:
        zr = MID if toward is None else (10000 if toward > 0 else 55000)
        d._write(("DACZ %d\n" % zr).encode()); time.sleep(0.02)
        d._write(("DACX %d\n" % MID).encode()); d._write(("DACY %d\n" % MID).encode())
        d._write(b"BIAS 32768\n"); time.sleep(0.05)
        port.close()
        xs = list(range(MID - half, MID + half + 1, step))
        for r, xheld, rows, sat, cl in scans:
            out = "%s_%s%d.csv" % (prefix, "xheld" if xheld else "scan", r)
            with open(out, "w") as f:
                f.write("y,dir," + ",".join(str(x) for x in xs) + "\n")
                for y, fwd, back in rows:
                    f.write("%d,fwd,%s\n" % (y, ",".join(str(v) for v in fwd)))
                    f.write("%d,back,%s\n" % (y, ",".join(str(v) for v in back)))
        log("end: toward %s, %d scans saved, Z %d, bias 0 V" % (toward, len(scans), zr))
