"""Are the reads alive, and does a big Z jump put a spike on the next reads? (sub-agent test 6)

2026-09-19 morning. Run ONLY with the gold out of reach of the whole Z range (fastwood_run1: nothing
in Z 0..62000 for 650 sweeps), so no current can flow at any Z used here.

At bias 0 V, then -0.5 V: jumps 0->28000, 28000->0, 0->60000, 60000->0, twice each, 30 ADCR
straight after each jump (reads 1-3 reported separately from 4-30). Then 200 ADCR at Z 0 at each of
0 / -0.5 / +0.5 V: mean and sd (a dead read path would give None or a frozen value).
"""
import sys, time, statistics as st
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")

JUMPS = [(0, 28000), (28000, 0), (0, 60000), (60000, 0)] * 2


def main():
    import serial
    from stm_approach import Device, find_teensy
    from stm_feedback_scan import read_averaged
    port = serial.Serial(find_teensy(), 115200, timeout=0.2)
    dev = Device(port)
    out = lambda s: print(time.strftime("%H:%M:%S", time.gmtime()), s, flush=True)
    try:
        dev._write(b"DACX 32768\n"); time.sleep(0.02)
        dev._write(b"DACY 32768\n"); time.sleep(0.02)
        for name, code in (("0 V", 32768), ("-0.5 V", 38229)):
            dev.set_bias(code); time.sleep(0.3)
            for a, b in JUMPS:
                dev._write(("DACZ %d\n" % a).encode()); time.sleep(0.3)
                dev._write(("DACZ %d\n" % b).encode())
                v = [read_averaged(dev) for _ in range(30)]
                good = [x for x in v if x is not None]
                first, rest = [x for x in v[:3] if x is not None], [x for x in v[3:] if x is not None]
                out("bias %-6s Z %5d->%5d: first3 %s | rest mean %6.1f sd %5.1f (None %d)"
                    % (name, a, b, first, st.mean(rest) if rest else float("nan"),
                       st.pstdev(rest) if len(rest) > 1 else float("nan"), 30 - len(good)))
        dev._write(b"DACZ 0\n"); time.sleep(0.3)
        for name, code in (("0 V", 32768), ("-0.5 V", 38229), ("+0.5 V", 27307)):
            dev.set_bias(code); time.sleep(0.3)
            v = [x for x in (read_averaged(dev) for _ in range(200)) if x is not None]
            out("Z 0, bias %-6s: mean %6.1f sd %5.1f n %d" % (name, st.mean(v), st.pstdev(v), len(v)))
        dev.set_bias(38229)
        out("end: Z 0, bias -0.5 V")
    finally:
        port.close()


if __name__ == "__main__":
    main()
