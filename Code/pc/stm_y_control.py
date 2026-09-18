#!/usr/bin/env python3
"""The control that decides whether a reproducible scan profile is the SAMPLE
or the SCANNER'S OWN BOW.

Why this exists
---------------
On 2026-09-17 twelve passes of one line at +-15,000 X counts reproduced:
consecutive passes r +0.515, odd-pass average against even-pass average +0.923,
and a surviving profile of 636 Z counts against a fixed-point height wobble of
287-419. That looks like topography.

It is only topography if it is a property of the PLACE. A fixed bow in the
scanner -- traced identically wherever the instrument points -- reproduces just
as well and means nothing.

    Different places give DIFFERENT shapes  ->  the profile is the surface.
    Different places give the SAME shape    ->  the profile is the scanner.

The control run on the night got this backwards, in two ways that are both
baked out of this tool:

  1. **It compared unlike things.** "Between places" was computed from
     five-pass AVERAGES while "within a place" was computed from SINGLE passes.
     Averaging raises a correlation on its own, so the comparison was decided
     before any physics entered. **Here both sides always use the same
     averaging depth**, and two statistics are reported so neither can hide a
     problem in the other.
  2. **It ran at the wrong width.** The control swept +-8,000 X counts while
     the result it was testing ran at +-15,000 -- a width at which nothing
     reproduces anywhere, so it had no power to discriminate. **Run this at the
     SAME half-width as the result you are testing**, and the tool records that
     width in the file so the two can never drift apart again.

A third trap, found 2026-09-18 while re-deriving the night's numbers from the
committed files: **none of these correlations mean anything until the tilt is
removed from each pass.** There is a fixed -0.1 to -0.2 counts-of-Z per count-
of-X tilt between tip and sample. Undetrended, it dominates every pass and
makes everything correlate with everything -- the same data gives +0.741 and
+0.880 and looks like a triumph. Every pass is detrended here before any
correlation is taken.

Safety
------
The feedback loop is `stm_feedback_scan.Loop`, unchanged: Z is clamped to
[Z_MIN_SAFE, Z_MAX_SAFE], one pixel moves Z by at most MAX_STEP counts, and
saturated and clamped pixels are counted. Z is retracted and X/Y re-centred on
every exit path, including Ctrl-C and an exception.

Usage
-----
    py stm_y_control.py <half> <step> <passes> <y_sep> <setpoint> <out.csv> [bias]

    py stm_y_control.py 15000 1500 6 3000 3000 control.csv

        half      X half-width in DAC counts. USE THE SAME WIDTH as the result
                  you are testing. 15000 for the 2026-09-17 profile.
        step      X step in counts. 1500 gives 21 points, as the night's files.
        passes    passes per place. 6 is the plan's figure; must be even, so
                  the split-half statistic has equal halves.
        y_sep     Y separation between places, in counts. Three places are run,
                  at -y_sep, 0 and +y_sep. 3000 is the plan's figure.
                  Keep it modest: +-12,000 drove 59-83% of pixels into a clamp
                  on 2026-09-17, because Y moves the gap as much as X does.
        setpoint  target current in ADC counts. 3000 counts is about 9.4 nA.
        bias      optional bias DAC code. 38229 is -0.5 V at the sample.

To re-analyse a file that already exists, with no instrument attached:

    py stm_y_control.py --analyse sessions/data/2026-09-17-bench/line_three_y_positions.csv

Tested by `stm_y_control_test.py` against a simulated junction carrying real
topography, a pure scanner bow, and noise -- and against the 2026-09-17 bug
re-injected, which must report the wrong answer.
"""
import sys
import os
import csv
import math

# The analysis half is deliberately pure-stdlib and imports nothing from the
# instrument tools, so it runs on any machine, with no serial port and no
# pyserial. The bench half imports lazily inside main().


# ----------------------------------------------------------------- statistics

def detrend(ys):
    """Remove the straight-line tilt from one pass.

    MEASURED 2026-09-17: holding the current while X moves needs about -0.17
    counts of Z per count of X. That tilt is instrumental -- it is the fixed
    angle between tip and sample -- and it is present in every pass at every
    place. Left in, it correlates with itself and swamps everything.
    """
    n = len(ys)
    if n < 3:
        return list(ys)
    mx = (n - 1) / 2.0
    my = sum(ys) / float(n)
    sxx = sum((i - mx) ** 2 for i in range(n))
    sxy = sum((i - mx) * (v - my) for i, v in enumerate(ys))
    slope = sxy / sxx if sxx else 0.0
    return [v - (my + slope * (i - mx)) for i, v in enumerate(ys)]


def corr(a, b):
    """Pearson r. Returns None when either side is flat, rather than 0.

    A flat pass is a clamped or dead run, not a run that disagrees, and
    scoring it as 0 would quietly drag an average toward "no effect".
    """
    n = len(a)
    if n != len(b) or n < 3:
        return None
    ma = sum(a) / float(n)
    mb = sum(b) / float(n)
    sa = math.sqrt(sum((x - ma) ** 2 for x in a))
    sb = math.sqrt(sum((x - mb) ** 2 for x in b))
    if sa == 0 or sb == 0:
        return None
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / (sa * sb)


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / float(len(xs)) if xs else None


def stdev(xs):
    xs = [x for x in xs if x is not None]
    if len(xs) < 2:
        return None
    m = sum(xs) / float(len(xs))
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def rms(xs):
    m = sum(xs) / float(len(xs))
    return math.sqrt(sum((x - m) ** 2 for x in xs) / float(len(xs)))


def average_passes(passes):
    """Elementwise mean of a list of equal-length passes."""
    n = len(passes)
    return [sum(p[i] for p in passes) / float(n) for i in range(len(passes[0]))]


# ------------------------------------------------------------------- analysis

def analyse(places, detrend_passes=True, fair=True):
    """The control's verdict.

    `places` maps a y_offset to its list of passes, each pass a list of Z.

    Two statistics, both computed the SAME WAY on both sides of the comparison:

      single   every pairwise correlation between two individual passes --
               within a place, and between places.
      split    odd-pass average against even-pass average within a place, and
               odd-pass average against odd-pass average between places. Both
               sides are averages of the same number of passes.

    `fair=False` re-injects the 2026-09-17 bug: between-place uses ALL-pass
    averages while within-place stays on single passes. It exists so the test
    suite can prove the honest statistic is doing the work.
    """
    keys = sorted(places)
    prep = {}
    for k in keys:
        prep[k] = [detrend(p) if detrend_passes else list(p) for p in places[k]]

    # --- single pass against single pass, both sides
    within_single = []
    for k in keys:
        ps = prep[k]
        for i in range(len(ps)):
            for j in range(i + 1, len(ps)):
                within_single.append(corr(ps[i], ps[j]))
    between_single = []
    for a in range(len(keys)):
        for b in range(a + 1, len(keys)):
            for pa in prep[keys[a]]:
                for pb in prep[keys[b]]:
                    between_single.append(corr(pa, pb))

    # --- split-half averages, equal depth on both sides
    within_split, between_split = [], []
    halves = {}
    for k in keys:
        ps = prep[k]
        odd, even = ps[0::2], ps[1::2]
        if odd and even:
            halves[k] = (average_passes(odd), average_passes(even))
            within_split.append(corr(halves[k][0], halves[k][1]))
    for a in range(len(keys)):
        for b in range(a + 1, len(keys)):
            ka, kb = keys[a], keys[b]
            if ka in halves and kb in halves:
                # odd-vs-odd and even-vs-even: same averaging depth as within.
                between_split.append(corr(halves[ka][0], halves[kb][0]))
                between_split.append(corr(halves[ka][1], halves[kb][1]))

    if not fair:
        # THE 2026-09-17 BUG, on purpose: all-pass averages between places
        # against single passes within one. Never use this for a real answer.
        between_single = []
        full = {k: average_passes(prep[k]) for k in keys}
        for a in range(len(keys)):
            for b in range(a + 1, len(keys)):
                between_single.append(corr(full[keys[a]], full[keys[b]]))

    # --- how much profile is there to argue about at all
    amps = {k: rms(average_passes(prep[k])) for k in keys}

    return {
        "places": keys,
        "n_passes": {k: len(prep[k]) for k in keys},
        "within_single": mean(within_single),
        "between_single": mean(between_single),
        "within_single_sd": stdev(within_single),
        "between_single_sd": stdev(between_single),
        "n_within_single": len([x for x in within_single if x is not None]),
        "n_between_single": len([x for x in between_single if x is not None]),
        "within_split": mean(within_split),
        "between_split": mean(between_split),
        "amplitudes": amps,
    }


# The fixed-point height wobble the profile has to beat, MEASURED 2026-09-17
# with the loop holding a fixed current at ONE point and nothing scanning.
WOBBLE_LO, WOBBLE_HI = 287.0, 419.0


def report(r):
    """Print the verdict. Returns a short verdict string."""
    print("")
    print("  places: %s   passes each: %s"
          % (r["places"], [r["n_passes"][k] for k in r["places"]]))
    print("")
    print("  profile amplitude, per place (Z counts RMS, tilt removed):")
    for k in r["places"]:
        a = r["amplitudes"][k]
        flag = "" if a >= WOBBLE_LO else "   <-- under the %d-count wobble floor" % WOBBLE_LO
        print("      y %+7d : %7.0f%s" % (k, a, flag))
    biggest = max(r["amplitudes"].values())

    print("")
    print("  %-34s %8s %8s %10s" % ("statistic", "within", "between", "within-between"))
    rows = [("single pass vs single pass", r["within_single"], r["between_single"]),
            ("split-half avg vs split-half avg", r["within_split"], r["between_split"])]
    for name, w, b in rows:
        if w is None or b is None:
            print("  %-34s %8s %8s %10s" % (name, "--", "--", "--"))
        else:
            print("  %-34s %+8.3f %+8.3f %+10.3f" % (name, w, b, w - b))

    # Standard error of the single-pass difference, for an honest "no effect".
    se = None
    if (r["within_single_sd"] is not None and r["between_single_sd"] is not None
            and r["n_within_single"] and r["n_between_single"]):
        se = math.sqrt(r["within_single_sd"] ** 2 / r["n_within_single"]
                       + r["between_single_sd"] ** 2 / r["n_between_single"])
        print("")
        print("  single-pass difference = %+.3f +- %.3f (1 s.e.)"
              % (r["within_single"] - r["between_single"], se))

    print("")
    if biggest < WOBBLE_LO:
        v = "NO PROFILE TO TEST"
        print("  VERDICT: %s. The biggest profile here is %.0f counts, under the"
              % (v, biggest))
        print("           %.0f-%.0f count wobble the height channel shows with"
              % (WOBBLE_LO, WOBBLE_HI))
        print("           nothing scanning. Widen the scan or raise the current")
        print("           before running this control -- it cannot answer a")
        print("           question about a signal that is not there.")
        return v

    d = r["within_single"] - r["between_single"]
    if se is not None and abs(d) < 2 * se:
        v = "NO EFFECT -- CANNOT DISCRIMINATE"
        print("  VERDICT: %s. Within and between agree to" % v)
        print("           within 2 standard errors, so this run does not")
        print("           separate the sample from the scanner. That is NOT the")
        print("           same as proving it is the scanner. More passes, or a")
        print("           wider Y separation, would give it more power.")
    elif d > 0:
        v = "THE PROFILE IS THE SURFACE"
        print("  VERDICT: %s." % v)
        print("           One place agrees with itself better than two places")
        print("           agree with each other. A fixed instrumental shape")
        print("           cannot do that. This is topography.")
    else:
        v = "THE PROFILE IS THE SCANNER"
        print("  VERDICT: %s." % v)
        print("           Different places trace the same shape better than one")
        print("           place repeats itself. That is a bow in the scanner,")
        print("           traced wherever it points. Not an image.")
    print("")
    return v


def load(path):
    """Read a control CSV. Returns (x_codes, {y_offset: [pass, ...]})."""
    with open(path, "r") as fh:
        rows = list(csv.reader(fh))
    xs = [int(v) for v in rows[0][2:]]
    places = {}
    for row in rows[1:]:
        if not row or not row[0].strip():
            continue
        y = int(row[0])
        places.setdefault(y, []).append([int(v) for v in row[2:]])
    return xs, places


def analyse_file(path, fair=True, detrend_passes=True):
    xs, places = load(path)
    half = (max(xs) - min(xs)) // 2
    print("%s" % path)
    print("  %d X points spanning +-%d counts, %d places"
          % (len(xs), half, len(places)))
    if half < 10000:
        print("  WARNING: this ran at +-%d. The 2026-09-17 profile under test"
              % half)
        print("           was at +-15,000, and at narrower widths nothing")
        print("           reproduces anywhere -- so a 'no effect' here may mean")
        print("           only that the control had no power. See the docstring.")
    r = analyse(places, detrend_passes=detrend_passes, fair=fair)
    return report(r), r


# ---------------------------------------------------------------- bench half

def reacquire(fs, loop, dev, x_start, setpoint):
    """Re-find the junction after a Y move.

    Y moves the gap as much as X does, so a place change can put the surface
    outside what one bounded pixel step can follow. Settle hard at the start of
    the line first, and if the loop ends up against a clamp, sweep Z from the
    retracted end and start again. Returns True if the junction was found.
    """
    dev._write(("DACX %d\n" % x_start).encode())
    before = loop.clamped
    for _ in range(8):
        z, v = loop.settle()
        if v and abs(v) > setpoint * 0.3 and abs(v) < fs.SAT:
            if loop.clamped == before:
                return True
        before = loop.clamped
    onset = fs.locate(dev, setpoint)
    if onset is None:
        return False
    loop.set_z(onset)
    loop.settle()
    return True


def sweep(fs, loop, dev, xs):
    """One forward pass. Returns the Z at each X."""
    zs = []
    for x in xs:
        dev._write(("DACX %d\n" % x).encode())
        z, _ = loop.settle()
        zs.append(z)
    return zs


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]

    if argv and argv[0] == "--analyse":
        if len(argv) < 2:
            print(__doc__)
            return 2
        analyse_file(argv[1])
        return 0

    if len(argv) < 6:
        print(__doc__)
        return 2

    half, step = int(argv[0]), int(argv[1])
    n_passes, y_sep = int(argv[2]), int(argv[3])
    setpoint, out = float(argv[4]), argv[5]
    bias_code = int(argv[6]) if len(argv) > 6 else 38229

    if n_passes % 2:
        print("passes must be EVEN, so the split-half statistic has equal "
              "halves. You gave %d." % n_passes)
        return 2
    if half < 10000:
        print("WARNING: +-%d is narrower than the +-15,000 the profile under "
              "test was measured at." % half)
        print("         At narrow widths nothing reproduces anywhere, so this "
              "run may return")
        print("         'no effect' whatever the truth is. That is exactly how "
              "the 2026-09-17")
        print("         control failed. Continuing anyway.")

    import serial
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import stm_feedback_scan as fs
    from stm_approach import Device, find_teensy

    xs = list(range(fs.MID - half, fs.MID + half + 1, step))
    places = [fs.MID - y_sep, fs.MID, fs.MID + y_sep]

    portname = find_teensy()
    if not portname:
        print("No Teensy found.")
        return 1

    port = serial.Serial(portname, 115200, timeout=0.2)
    rows = []
    with port:
        import time
        time.sleep(1.0)
        dev = Device(port)
        loop = None
        try:
            dev.set_z(fs.Z_LOCATE_START)
            dev._write(("DACX %d\n" % fs.MID).encode())
            dev._write(("DACY %d\n" % fs.MID).encode())
            dev._write(("BIAS %d\n" % bias_code).encode())
            time.sleep(0.1)

            onset = fs.locate(dev, setpoint)
            if onset is None:
                print("No junction in the Z range. Approach with the motor "
                      "first:")
                print("  py stm_approach.py --z-retracted low "
                      "--motor-toward-sample negative")
                return 1

            loop = fs.Loop(dev, setpoint)
            loop.set_z(onset)
            print("onset Z=%d, setpoint %d counts (%.2f nA), bias %d"
                  % (onset, setpoint, setpoint / fs.COUNTS_PER_NANOAMP,
                     bias_code))
            print("%d X points at +-%d, %d places %d apart, %d passes each"
                  % (len(xs), half, len(places), y_sep, n_passes))

            t0 = time.time()
            for p in range(n_passes):
                # Interleaved: every place gets pass p before any place gets
                # pass p+1, so a slow drift cannot masquerade as a difference
                # between places.
                for y in places:
                    dev._write(("DACY %d\n" % y).encode())
                    if not reacquire(fs, loop, dev, xs[0], setpoint):
                        print("  lost the junction at y=%d, pass %d -- stopping"
                              % (y, p))
                        raise KeyboardInterrupt
                    # A throwaway sweep. MEASURED 2026-09-17: the loop's
                    # settling transient on the FIRST line of an image was
                    # +712, +521 and +330 counts and produced a spurious
                    # r = +0.75 between two images, because the procedure is
                    # identical rather than the sample. Never record it.
                    sweep(fs, loop, dev, xs)
                    zs = sweep(fs, loop, dev, xs)
                    rows.append((y - fs.MID, p, zs))
                    print("  pass %d, y %+6d : done" % (p, y - fs.MID))
            print("  %d lines in %.1f s, saturated %d, clamped %d, lost %d"
                  % (len(rows), time.time() - t0, loop.saturated,
                     loop.clamped, loop.lost))
        except KeyboardInterrupt:
            print("\ninterrupted")
        finally:
            # Every exit path retracts and re-centres.
            dev._write(("DACZ %d\n" % fs.Z_LOCATE_START).encode())
            dev._write(("DACX %d\n" % fs.MID).encode())
            dev._write(("DACY %d\n" % fs.MID).encode())
            dev._write(b"BIAS 32768\n")
            print("Z retracted to %d, X/Y centred, bias 0 V."
                  % fs.Z_LOCATE_START)

    if not rows:
        print("Nothing recorded.")
        return 1

    with open(out, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["y_offset", "pass"] + xs)
        for y, p, zs in rows:
            w.writerow([y, p] + zs)
    print("wrote %s" % out)

    analyse_file(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
