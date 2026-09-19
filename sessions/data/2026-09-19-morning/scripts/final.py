"""Final state before the break: tip-clear noise baseline, then park for power-down.

2026-09-19 morning, after the storage back-off of the side screws. Z 0 (fully retracted for the tip
fitted ~03:00 UTC 2026-09-19), X/Y midscale, 200 ADCR at 0 / -0.5 / +0.5 / 0 V, then bias 0 V
(`BIAS 32768`) and Z 0 left set for the power-down. Nothing but Z 0 and the bias is written.
"""
import sys, time, statistics as st
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")

if __name__ == "__main__":
    # Added 2026-09-19 after a --test run of a script WITHOUT a self-test went straight to its
    # hardware path (no port was connected, so nothing was sent). Unknown options now refuse.
    _bad = [a for a in sys.argv[1:] if a.startswith('-') and a not in []]
    if _bad:
        sys.exit('refusing unknown option(s) %s: this script drives the instrument%s'
                 % (_bad, '' if False else ' and has NO self-test'))
    import serial
    from stm_approach import Device, find_teensy
    from stm_feedback_scan import read_averaged
    port = serial.Serial(find_teensy(), 115200, timeout=0.2)
    dev = Device(port)
    out = lambda s: print(time.strftime("%H:%M:%S", time.gmtime()), s, flush=True)
    try:
        dev._write(b"GSTS"); time.sleep(0.3)
        out("GSTS: " + port.read(port.in_waiting or 1).decode("ascii", "replace").strip())
        dev._write(b"DACX 32768\n"); time.sleep(0.02)
        dev._write(b"DACY 32768\n"); time.sleep(0.02)
        dev.set_z(0)
        for name, code in (("0 V", 32768), ("-0.5 V", 38229), ("+0.5 V", 27307), ("0 V", 32768)):
            dev.set_bias(code); time.sleep(0.3)
            v = [x for x in (read_averaged(dev) for _ in range(200)) if x is not None]
            out("Z 0, bias %-6s: mean %7.1f  sd %6.1f  (n %d)" % (name, st.mean(v), st.pstdev(v), len(v)))
        dev.set_bias(32768); dev.set_z(0)
        out("PARKED: Z 0, X/Y 32768, bias 0 V. Ready for USB out, then supplies off.")
    finally:
        port.close()
