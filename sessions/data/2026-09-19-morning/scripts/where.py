"""Where is the gold now? N full sweeps (fastwood.sweep, DETECT 200; 250-count steps intended, but
the 2026-09-19 runs swept in 1,000-count steps because of the fastwood.sweep default bug, fixed after), PERIOD s apart.
Read-and-Z only: no motor. Z ends at 0, bias -0.5 V. 2026-09-19 morning."""
import sys, time, statistics as st
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\sessions\data\2026-09-19-morning\scripts")
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
import fastwood
fastwood.ZSTEP, fastwood.DETECT = 250, 200

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
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    period = float(sys.argv[2]) if len(sys.argv) > 2 else 2.0
    port = serial.Serial(find_teensy(), 115200, timeout=0.2)
    dev = Device(port)
    try:
        dev._write(b"DACX 32768\n"); dev._write(b"DACY 32768\n")
        dev.set_z(0); dev.set_bias(38229); time.sleep(0.2)
        def set_z(z): dev._write(("DACZ %d\n" % z).encode()); time.sleep(0.001)
        def rd():
            v = [x for x in (read_averaged(dev) for _ in range(2)) if x is not None]
            return st.mean(v) if v else None
        for i in range(n):
            set_z(0); v0 = rd()
            z, v = fastwood.sweep(set_z, rd)
            print(time.strftime("%H:%M:%S", time.gmtime()), "sweep %d: at Z 0 %s counts; onset %s (%s counts)"
                  % (i, "%.0f" % v0 if v0 is not None else "None", z, "%.0f" % v if v is not None else "-"), flush=True)
            time.sleep(period)
        set_z(0)
    finally:
        port.close()
