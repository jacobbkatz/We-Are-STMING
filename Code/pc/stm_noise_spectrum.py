#!/usr/bin/env python3
"""Noise spectrum of the ADC with the tip clear, and the comparison to every
previous run, printed for you.

WHY THIS FILE EXISTS. The 2026-09-18 bench session ran this measurement from
`sessions/data/2026-09-18-bench/scripts/spectrum.py`, which carries a
hardcoded path to Jacob's Desktop and a hardcoded COM3. **On any other
machine it fails on the first two lines**, and the 2026-09-19 plan is to
repeat the measurement on Nuh's computer. This is the same arithmetic with
the machine taken out of it: it finds the Teensy by its USB vendor ID, takes
`--port` if that fails, and writes the raw samples to CSV so the run can be
re-analysed without the instrument.

WHAT IT READS. `ADCR`, the firmware's averaged reading. **Not a raw single
conversion** -- 46 counts of noise against 188 for the same time, measured
2026-09-17. `Code/pc/adc_stats.py` reads single conversions on purpose, to
catch SPI bit-flips; this one wants the quietest honest reading.

IT ONLY READS. No DACZ, no motor, no bias. Nothing moves.

    py stm_noise_spectrum.py                 # 4 s, auto-find the Teensy
    py stm_noise_spectrum.py 10              # 10 s, quieter low-frequency bins
    py stm_noise_spectrum.py 10 --port COM7
    py stm_noise_spectrum.py --analyse run.csv        # no instrument needed
"""
import argparse
import cmath
import csv
import math
import os
import statistics as st
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Previous runs, for the comparison this tool prints. Session logs are history
# and keep their own numbers; these are copied here so the bench sees the
# comparison without opening anything.
BASELINES = [
    # label,           ADCR sd,  band means 2-10, 10-30, 30-100, 100-400, 400-1600
    ("2026-09-17",        47.0,  None),
    ("2026-09-18",       345.0,  {(2, 10): 9.3, (10, 30): 8.5, (30, 100): 10.0,
                                  (100, 400): 10.7, (400, 1600): 5.0}),
]
BANDS = [(2, 10), (10, 30), (30, 100), (100, 400), (400, 1600)]
# 2-100 Hz at 1 Hz, matching the 2026-09-18 run so the low bands are directly
# comparable, then a DENSE 400-1600 Hz control band.
#
# The control band started as 10 sparse lines, copied from the bench script.
# That is far too few: line POWER is exponentially distributed, so the mean of
# 10 has a 32% standard error, which is +/-16% on the floor -- and the floor is
# subtracted from every other band. The tests showed it turning a world where
# nothing had changed into a 1.3x rise. 61 lines takes that to about 6%.
FREQS = (list(range(2, 101))
         + [110, 120, 130, 150, 180, 200, 240, 300, 360]
         + list(range(400, 1601, 20)))


def find_teensy():
    """PJRC's vendor ID is 0x16C0. Same rule as adc_stats.py."""
    from serial.tools import list_ports
    for p in list_ports.comports():
        if p.vid == 0x16C0:
            return p.device
    ports = list_ports.comports()
    if len(ports) == 1:
        # A GUESS, not a match. Tested 2026-09-19 on a machine with no Teensy:
        # it silently picked /dev/ttyS0 and the only clue was 0 samples. Say so.
        sys.stderr.write("No device with the Teensy's vendor ID (0x16C0).\n")
        sys.stderr.write("GUESSING the only port present: %s  (%s)\n"
                         % (ports[0].device, ports[0].description))
        sys.stderr.write("If that is wrong, re-run with --port.\n")
        return ports[0].device
    if ports:
        sys.stderr.write("Could not identify the Teensy. Ports seen:\n")
        for p in ports:
            sys.stderr.write("    %s  %s\n" % (p.device, p.description))
        sys.stderr.write("Re-run with --port <one of those>.\n")
    else:
        sys.stderr.write("No serial ports at all. Is the USB lead in?\n")
    return None


def collect(port_name, secs):
    import serial
    from stm_approach import Device
    from stm_feedback_scan import read_averaged

    port = serial.Serial(port_name, 115200, timeout=0.2)
    try:
        dev = Device(port)
        ts, vs = [], []
        t0 = time.perf_counter()
        while time.perf_counter() - t0 < secs:
            v = read_averaged(dev)
            if v is not None:
                ts.append(time.perf_counter() - t0)
                vs.append(v)
    finally:
        port.close()
    return ts, vs


def spectrum(ts, vs):
    """Direct DFT on the real timestamps.

    The sample instants are not evenly spaced -- they are whatever the serial
    round trip gave -- so an FFT would need resampling and would smear the low
    bins. Evaluating the sum at each frequency costs more and needs no
    assumption about the clock.
    """
    m = st.mean(vs)
    x = [v - m for v in vs]
    n = len(x)

    def amp(f):
        s = sum(xi * cmath.exp(-2j * math.pi * f * ti) for xi, ti in zip(x, ts))
        return 2 * abs(s) / n

    return {f: amp(f) for f in FREQS}


def floor_of(sd, n):
    """Expected DFT line amplitude of white noise alone.

    For white Gaussian noise of standard deviation `sd` over `n` samples, the
    real and imaginary parts of the sum are each N(0, sd^2*n/2), so |S| is
    Rayleigh and E[2|S|/n] = sd*sqrt(pi/n).

    CHECKED AGAINST THE BENCH 2026-09-19: the 2026-09-18 run had sd 344 over
    n = 14041, which predicts 5.15 counts. Its measured 400-1600 Hz band mean
    was 5.0. **So that band was nothing but the white noise floor** -- there is
    no mechanical content up there at all, which is exactly why it makes a
    control.
    """
    return sd * math.sqrt(math.pi / n) if n else float("nan")


def report(ts, vs, a):
    """Print the run, and the comparison, and the one verdict that matters.

    THE TRAP THIS AVOIDS. Comparing raw band means between two runs is
    misleading whenever the broadband noise differs, because the white floor
    sits under every band and moves them all together. A run at sd 47 has a
    floor of 0.7 counts against sd 345's 5.2, so EVERY band would read
    "7x better" without any mechanical change at all.

    So each band is divided by its own run's floor. That number -- how far the
    band stands above white noise -- is comparable between runs. The
    400-1600 Hz band is the control: it should come out near 1.00 in any run,
    and if it does not, the model or the measurement is wrong.
    """
    secs = ts[-1] if ts else 0.0
    sd = st.pstdev(vs)
    n = len(vs)
    # THE FLOOR IS MEASURED, NOT PREDICTED. 400-1600 Hz carries no mechanical
    # content -- 2026-09-18's band mean there was 5.0 against the 5.15 that
    # white noise alone predicts -- so that band IS the floor for its own run.
    # Using it removes any dependence on the formula, on n, or on sampling
    # jitter. The predicted value is still printed as a cross-check: if the two
    # disagree badly, either there is real content up there or the run is short.
    # IN POWER, NOT AMPLITUDE. E[|signal + noise|^2] = A^2 + E[|noise|^2]
    # EXACTLY, so subtracting mean squares recovers the signal with no bias.
    # Subtracting mean AMPLITUDES in quadrature does not: at a signal-to-noise
    # around one it underestimates the content by roughly 7%, and it does so
    # MORE when the floor is large. That is the wrong direction -- 2026-09-18's
    # floor was 7x tonight's likely one, so its content would be underestimated
    # relative to tonight's and the tool would report a rise that is not there.
    # The tests caught exactly that.
    fl_pow = st.mean([a[f] ** 2 for f in FREQS if 400 <= f < 1600])
    fl = math.sqrt(fl_pow)
    fl_pred = floor_of(sd, n)
    print("n=%d over %.1f s, %.0f reads/s" % (n, secs, n / secs if secs else 0))
    print("ADCR sd %.0f counts  (%.2f nA at 320.5 counts/nA)" % (sd, sd / 320.5))
    print("floor from 400-1600 Hz: %.2f counts rms   (white noise alone predicts %.2f)"
          % (fl, fl_pred))
    if fl_pred and not (0.6 < fl / fl_pred < 1.7):
        print("  WARNING: those two disagree. Either there is real content above")
        print("  400 Hz or the run is too short. Treat the shape numbers with care.")
    print("")

    print("QUESTION 1 -- THE BROADBAND FLOOR. Is the 7x from 2026-09-18 still there?")
    print("  %-14s %-12s %s" % ("run", "ADCR sd", "vs tonight"))
    for label, base_sd, _ in BASELINES:
        r = sd / base_sd
        verdict = ("same" if 0.8 < r < 1.25 else
                   "%.1fx BETTER than that" % (1 / r) if r < 0.8 else
                   "%.1fx WORSE than that" % r)
        print("  %-14s %-12s %s" % (label, "%.0f" % base_sd, verdict))
    print("")

    means, exc = {}, {}
    for lo, hi in BANDS:
        vals = [a[f] for f in FREQS if lo <= f < hi]
        means[(lo, hi)] = st.mean(vals) if vals else float("nan")
        # THE MECHANICAL CONTENT ALONE, in counts. The white floor and the
        # mechanical signal are independent, so they add in QUADRATURE in the
        # line amplitude -- subtract the floor the same way and what is left is
        # the real content, independent of whatever the electrical noise did.
        #
        # This replaced a simple band/floor RATIO, which the tests showed is
        # wrong in a way that matters: if the 7x broadband noise is fixed and
        # the mechanical content is untouched, the ratio leaps and the tool
        # would report "the low frequencies got worse". They did not; the floor
        # under them moved. Only the absolute content answers the question.
        p = st.mean([a[f] ** 2 for f in FREQS if lo <= f < hi]) if vals else 0.0
        exc[(lo, hi)] = math.sqrt(p - fl_pow) if p > fl_pow else 0.0

    prev = BASELINES[-1][2]
    # The 2026-09-18 baseline survives only as band MEANS -- the raw samples
    # were not kept -- so its power is reconstructed from those. That costs a
    # little accuracy on the baseline side and nothing on tonight's.
    prev_fl = 5.0        # 2026-09-18's own 400-1600 Hz band mean
    prev_exc = {b: (math.sqrt(prev[b] ** 2 - prev_fl ** 2) if prev and prev[b] > prev_fl else 0.0)
                for b in BANDS} if prev else {}
    print("QUESTION 2 -- THE SHAPE. How far does each band stand above white noise?")
    print("  'mechanical' is the band with THIS RUN's own white floor taken out in")
    print("  quadrature -- the real content in counts, whatever the electrical noise")
    print("  did. 400-1600 Hz comes out at zero by construction; it IS the floor.")
    print("")
    print("  %-14s %-10s %-14s %-14s %s"
          % ("band", "counts", "mechanical", "09-18 mech", "change"))
    for b in BANDS:
        was = prev_exc.get(b)
        chg = "--"
        if was and was > 0.5:
            if exc[b] < 0.05 * was:
                chg = "GONE"          # 1/r would divide by zero
            else:
                r = exc[b] / was
                chg = ("%.1fx BETTER" % (1 / r) if r < 0.8 else
                       "%.1fx worse" % r if r > 1.25 else "same")
        print("  %-14s %-10s %-14s %-14s %s"
              % ("%d-%d Hz" % b, "%.1f" % means[b], "%.1f" % exc[b],
                 "%.1f" % was if was else "--", chg))
    print("")

    top = sorted(a.items(), key=lambda kv: -kv[1])[:8]
    print("strongest lines: " + ", ".join("%d Hz %.0f" % kv for kv in top))
    print("")

    if prev:
        low = st.mean([exc[(2, 10)], exc[(10, 30)]])
        low_was = st.mean([prev_exc[(2, 10)], prev_exc[(10, 30)]])
        rl = low / low_was if low_was else float("nan")
        if low < 0.05 * low_was:
            rl = 0.0
        # HOW FAR TO TRUST THIS. 2026-09-18's raw samples were not kept, so its
        # side of the comparison is reconstructed from published band means with
        # a different estimator from tonight's. On synthetic data where the truth
        # is 10.0 counts, this reads 7.4 at a floor of 6.0 and 9.7 at a floor of
        # 0.9 -- so when the two runs' floors differ a lot, the comparison is
        # biased toward "it got worse" by up to about 30%. That is not fixable
        # from here; it needs a baseline with raw samples. SAY SO rather than
        # print a confident number.
        ratio_fl = fl / prev_fl if prev_fl else float("nan")
        shaky = not (0.5 < ratio_fl < 2.0)
        print("THE VERDICT -- did the SUSPENSION do it?")
        print("  2-30 Hz mechanical content: %.1f counts tonight, %.1f on 09-18  (x%.2f)"
              % (low, low_was, rl))
        if shaky:
            print("")
            print("  *** THIS COMPARISON IS NOT RELIABLE. Tonight's floor is %.1fx" % ratio_fl)
            print("  *** 2026-09-18's, and that run's raw samples were never kept, so the")
            print("  *** two sides are estimated differently. The bias runs toward")
            print("  *** 'it got worse' by up to about 30%. Do NOT act on it alone.")
            print("  *** THE RELIABLE MEASUREMENT IS TWO RUNS THE SAME NIGHT:")
            print("  ***     py stm_noise_spectrum.py 10 --out still.csv")
            print("  ***     (someone stamps the floor a couple of metres away)")
            print("  ***     py stm_noise_spectrum.py 10 --out stamp.csv")
            print("  ***     py stm_noise_spectrum.py --compare still.csv stamp.csv")
            print("  *** Same floor, same gain, same everything. If the suspension works,")
            print("  *** stamping moves the low bands far less than it used to.")
        elif rl < 0.8:
            print("  => THE LOW-FREQUENCY CONTENT FELL, with the floor taken out.")
            print("     That is the suspension. Nothing else acts only down there.")
        elif rl > 1.25:
            print("  => THE LOW-FREQUENCY CONTENT ROSE. Check the platform hangs FREE")
            print("     and is not touching the magnets, the tower or a taut wire.")
        else:
            print("  => NO CHANGE in the low-frequency content. The suspension has not")
            print("     altered what reaches the tip, whatever the raw sd did.")


def load_csv(path):
    ts, vs = [], []
    with open(path) as fh:
        for row in csv.DictReader(fh):
            ts.append(float(row["t_s"]))
            vs.append(float(row["adcr"]))
    return ts, vs


def band_content(ts, vs):
    """(floor rms, {band: mechanical content in counts}) for one run."""
    a = spectrum(ts, vs)
    fl_pow = st.mean([a[f] ** 2 for f in FREQS if 400 <= f < 1600])
    out = {}
    for lo, hi in BANDS:
        p = st.mean([a[f] ** 2 for f in FREQS if lo <= f < hi])
        out[(lo, hi)] = math.sqrt(p - fl_pow) if p > fl_pow else 0.0
    return math.sqrt(fl_pow), out, st.pstdev(vs)


def compare(path_a, path_b):
    """Two runs from the SAME night, same settings. This is the honest one.

    Nothing is reconstructed and no estimator is mixed: both sides go through
    the identical code on raw samples. Use it for still-vs-stamping, or for
    before-and-after any single change.
    """
    fa, ca, sda = band_content(*load_csv(path_a))
    fb, cb, sdb = band_content(*load_csv(path_b))
    print("A  %-28s sd %6.0f   floor %.2f" % (os.path.basename(path_a), sda, fa))
    print("B  %-28s sd %6.0f   floor %.2f" % (os.path.basename(path_b), sdb, fb))
    print("")
    print("  %-14s %-12s %-12s %s" % ("band", "A mech", "B mech", "B vs A"))
    for b in BANDS:
        chg = "--"
        if ca[b] > 0.5:
            r = cb[b] / ca[b]
            chg = ("%.1fx LESS" % (1 / r) if r < 0.8 else
                   "%.1fx MORE" % r if r > 1.25 else "same")
        print("  %-14s %-12s %-12s %s"
              % ("%d-%d Hz" % b, "%.1f" % ca[b], "%.1f" % cb[b], chg))
    print("")
    lo_a = st.mean([ca[(2, 10)], ca[(10, 30)]])
    lo_b = st.mean([cb[(2, 10)], cb[(10, 30)]])
    print("2-30 Hz mechanical: A %.1f counts, B %.1f counts" % (lo_a, lo_b))
    if lo_a > 0.5:
        r = lo_b / lo_a
        print("B is %.2fx A down there." % r)
        print("")
        print("IF A WAS STILL AND B WAS SOMEONE STAMPING:")
        print("  B much bigger  -> the building IS getting in. The suspension is what")
        print("                    has to improve, and this is the number to watch.")
        print("  B about the same -> the floor is NOT the route. The 5-20 Hz is made")
        print("                    inside the instrument -- tip holder, sample plate,")
        print("                    the rubber bands -- and no suspension change helps.")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("secs", nargs="?", type=float, default=4.0,
                    help="seconds to sample (default 4; use 10 for cleaner low bins)")
    ap.add_argument("--port", help="serial port, if auto-detect picks wrong")
    ap.add_argument("--out", help="CSV to write the raw samples to")
    ap.add_argument("--analyse", help="re-analyse a CSV, no instrument needed")
    ap.add_argument("--compare", nargs=2, metavar=("A.csv", "B.csv"),
                    help="compare two runs from the SAME night -- the reliable comparison")
    args = ap.parse_args()

    if args.compare:
        return compare(*args.compare)

    if args.analyse:
        ts, vs = [], []
        with open(args.analyse) as fh:
            for row in csv.DictReader(fh):
                ts.append(float(row["t_s"]))
                vs.append(float(row["adcr"]))
        print("re-analysing %s" % args.analyse)
    else:
        port_name = args.port or find_teensy()
        if not port_name:
            return 2
        print("port %s, sampling %.0f s -- TIP MUST BE CLEAR AND NOBODY WITHIN A METRE"
              % (port_name, args.secs))
        ts, vs = collect(port_name, args.secs)
        if len(vs) < 50:
            sys.stderr.write("Only %d samples. Is the board powered and answering ADCR?\n"
                             % len(vs))
            return 1
        out = args.out or time.strftime("noise_%Y%m%d_%H%M%S.csv")
        with open(out, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["t_s", "adcr"])
            w.writerows(zip(ts, vs))
        print("raw samples -> %s" % out)

    print("")
    report(ts, vs, spectrum(ts, vs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
