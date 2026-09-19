"""Is there an image? The tests the project already uses, applied to catch_and_scan's files.

For each file: every line detrended (the tilt removed), then
  corrugation   RMS of the detrended forward lines, averaged over lines
  trace/retrace mean correlation of forward against backward, line by line
and between consecutive REAL scans: image-to-image correlation of the detrended forward images.
The X-held controls get the same numbers: they are what the loop and the junction do with NO
lateral motion. A real image needs trace/retrace and image-to-image well above the controls'.
"""
import sys, glob, os
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
from stm_y_control import detrend, corr, rms


def load(path):
    fwd, back = {}, {}
    with open(path) as f:
        f.readline()
        for line in f:
            p = line.strip().split(",")
            y, d, vals = int(p[0]), p[1], [float(v) for v in p[2:]]
            (fwd if d == "fwd" else back)[y] = vals
    ys = sorted(fwd)
    return ys, [fwd[y] for y in ys], [back.get(y) for y in ys]


def stats(path):
    ys, F, B = load(path)
    cor = [rms(detrend(f)) for f in F]
    tr = [corr(detrend(f), detrend(b)) for f, b in zip(F, B) if b]
    tr = [t for t in tr if t is not None]
    return {"lines": len(ys), "corrugation": sum(cor) / len(cor),
            "trace_retrace": sum(tr) / len(tr) if tr else None,
            "flat": [v for f in F for v in detrend(f)], "nlines": len(F)}


def main(prefix):
    scans = sorted(glob.glob(prefix + "_scan*.csv"))
    ctrls = sorted(glob.glob(prefix + "_xheld*.csv"))
    res = {}
    for p in scans + ctrls:
        s = stats(p); res[p] = s
        print("%-22s lines %2d  corrugation %6.0f  trace/retrace %s" % (
            os.path.basename(p), s["lines"], s["corrugation"],
            "%+.2f" % s["trace_retrace"] if s["trace_retrace"] is not None else "-"))
    for group, name in ((scans, "real scans"), (ctrls, "X-held controls")):
        pairs = []
        for a, b in zip(group, group[1:]):
            fa, fb = res[a]["flat"], res[b]["flat"]
            n = min(len(fa), len(fb))
            c = corr(fa[:n], fb[:n])
            if c is not None:
                pairs.append(c)
        if pairs:
            print("%s: image-to-image r %s (mean %+.2f)" % (name, " ".join("%+.2f" % c for c in pairs), sum(pairs) / len(pairs)))


if __name__ == "__main__":
    main(sys.argv[1])
