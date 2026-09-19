"""Constant-height current map at a FIXED Z: raster X (fwd and back) over Y lines, recording the
averaged current at each pixel. xheld=True keeps X still (the control). Also an I-V at the spot.
Needs only a junction, not Z control. Bias restored to -0.5 V afterwards."""
import time, statistics as st
MID = 32768

def cmap(dev_write, read, z, half=1500, step=150, nlines=11, reads=8, xheld=False):
    xs = list(range(MID - half, MID + half + 1, step))
    ys = [MID - half + round(i * 2.0 * half / (nlines - 1)) for i in range(nlines)]
    dev_write("DACZ %d\n" % z)
    rows = []
    for y in ys:
        dev_write("DACY %d\n" % y)
        line = {}
        for name, order in (("fwd", xs), ("back", xs[::-1])):
            vals = []
            for x in order:
                if not xheld:
                    dev_write("DACX %d\n" % x)
                v = [r for r in (read() for _ in range(reads)) if r is not None]
                vals.append(round(st.mean(v)) if v else 0)
            if name == "back":
                vals.reverse()
            line[name] = vals
        rows.append((y, line["fwd"], line["back"]))
    dev_write("DACX %d\n" % MID); dev_write("DACY %d\n" % MID)
    return xs, rows

def iv(dev_write, read, z, volts=(-0.8, -0.6, -0.4, -0.2, -0.1, 0.0, 0.1, 0.2, 0.4, 0.6, 0.8)):
    dev_write("DACZ %d\n" % z)
    out = {}
    order = list(volts[0::2]) + list(volts[1::2])
    for vv in order:
        code = int(round(32768 - vv * 5461 / 0.5))
        dev_write("BIAS %d\n" % code); time.sleep(0.02)
        v = [r for r in (read() for _ in range(64)) if r is not None]
        out[vv] = round(st.mean(v)) if v else 0
    dev_write("BIAS 38229\n")
    return [(vv, out[vv]) for vv in volts]
