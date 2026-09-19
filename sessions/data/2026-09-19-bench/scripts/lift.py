"""Lift the tip off with single RETRACT motor steps and ask, after each, whether extending Z
brings the current back.

Per step: Z to 0; MTMV +1; then the current at Z 0 (64 reads), then an onset sweep 0..50000 in
200-count steps (threshold 300 counts on a median of 8, confirmed on 16), then, if an onset is
found, a short slope from onset-400 in 20-count steps, stopping at 5000. Stops after the
current at Z 0 is gone AND two consecutive steps find no onset anywhere, or after MAXSTEPS.
Watchdog: any read >= 20000 pulls Z to 0. Exit: Z 0, bias 0 V.
"""
import sys
import time
import statistics as st
import onset0 as o

MAXSTEPS = int(sys.argv[1]) if len(sys.argv) > 1 else 30
OUT = sys.argv[2] if len(sys.argv) > 2 else "lift.csv"


def main(rig, run, log):
    rig.bias(o.BNEG)
    rig.set_z(0)
    time.sleep(0.2)
    lost = 0
    table = []
    for k in range(MAXSTEPS + 1):
        if k > 0:
            rig.set_z(0)
            rig.motor(1)
            time.sleep(0.3)
        rig.set_z(0)
        v = run.reads(64, "z0_s%d" % k)
        i0 = st.mean(v)
        z = 0
        onset = None
        while z <= o.ZCAP:
            rig.set_z(z)
            a = run.reads(8, "sw_s%d" % k)
            if a and abs(st.median(a)) >= o.ONSET:
                b = run.reads(16, "sw_s%d" % k)
                if b and abs(st.median(b)) >= o.ONSET:
                    onset = z
                    break
            z += 200
        slope = []
        if onset is not None and onset > 0:
            zz = max(0, onset - 400)
            while zz <= min(o.ZCAP, onset + 800):
                rig.set_z(zz)
                m = st.mean(run.reads(16, "sl_s%d" % k))
                slope.append((zz, round(m)))
                if abs(m) >= o.STOPC:
                    break
                zz += 20
        rig.set_z(0)
        table.append((k, round(i0), onset, slope))
        log("step +%d: I at Z 0 = %.0f | onset %s | slope %s" % (
            k, i0, onset, " ".join("%d:%d" % p for p in slope[::3] + slope[-1:]) if slope else "-"))
        if abs(i0) < 150 and onset is None:
            lost += 1
            if lost >= 2:
                log("lifted beyond reach for 2 steps: stop")
                break
        else:
            lost = 0
    return table


if __name__ == "__main__":
    import serial
    sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
    from stm_approach import find_teensy

    class MRig(o.Rig):
        def motor(self, n):
            self.d.move_motor(n)

    port = serial.Serial(find_teensy(), 115200, timeout=0.2)
    rig = MRig(port)
    log = lambda s: print(time.strftime("%H:%M:%S", time.gmtime()), s, flush=True)
    run = o.Run(rig, log=log)
    try:
        main(rig, run, log)
    except o.Abort as e:
        log("ABORT: %s" % e)
    finally:
        rig.set_z(0)
        rig.bias(o.BZERO)
        port.close()
        with open(OUT, "w") as f:
            f.write("t,tag,z,bias,value\n")
            for r in run.rows:
                f.write("%s,%s,%s,%s,%s\n" % r)
        log("end: Z 0, bias 0 V; wrote %s" % OUT)
