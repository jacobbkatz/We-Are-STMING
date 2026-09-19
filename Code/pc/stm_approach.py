#!/usr/bin/env python3
"""
PC-side coarse approach, using the woodpecker method.

WHY THIS EXISTS INSTEAD OF THE FIRMWARE'S `APRH`
------------------------------------------------
The firmware's approach() tests `read_adc() > target` -- a SIGNED comparison
against a baseline that has been negative for this whole project. If tunneling
drives the reading more negative, that test never fires and the motor keeps
driving the tip into the sample. This script never sends APRH. It thresholds on
ABSOLUTE deviation from a measured baseline, so it works without knowing which
way tunneling moves the reading.

THE WOODPECKER METHOD
---------------------
Only the piezo ever closes the gap; the motor and the piezo never move at the
same time. Each cycle:

    1. park Z at the retracted end
    2. sweep Z toward the sample, watching the ADC at every point
    3. found it?  -> retract immediately and stop
       not found? -> retract, step the motor once, repeat

Because a motor step (~8 nm) is far smaller than the Z range (~700 nm), the
piezo always gets to search the whole gap before the motor closes any of it.

THIS SCRIPT WILL REFUSE TO RUN unless you tell it two things it cannot work out
for itself, because getting either backwards turns a safe approach into a drive
straight into the sample:

    --z-retracted          which end of the Z DAC range pulls AWAY from the sample
    --motor-toward-sample  which sign of MTMV advances TOWARD the sample

See docs/OPEN_QUESTIONS.md for both. As of 2026-09-16 the motor sign is
PROVISIONALLY "negative" (the sample moves toward the tip when the driven screw
pulls in) and the Z direction is still UNKNOWN. The usage lines below show the
syntax only; do not copy their values.

Usage:
    python stm_approach.py --z-retracted low --motor-toward-sample positive
    python stm_approach.py --z-retracted low --motor-toward-sample positive --dry-run
    python stm_approach.py --help
"""

import argparse
import sys
import time

# Z DAC window. The firmware's own constant-current loop clamps Z to this
# range, so staying inside it keeps us in territory the rest of the project
# already uses.
Z_MIN = 10000
Z_MAX = 50000
Z_PARK = 32768  # midscale, 0 V, safe whichever direction turns out to be which

# 16-bit signed ADC.
ADC_FULL_SCALE = 32767

# Refuse to approach if the resting reading is already this close to the rail.
# There is no headroom left to detect an increase, so a threshold could never
# be crossed. At the time of writing the preamp sits near 29873 counts, which
# trips this deliberately.
SATURATION_FRACTION = 0.80

# setSpeed(2) at 2048 steps/rev = 2 * 2048 / 60 steps per second.
STEPS_PER_SECOND = 2.0 * 2048 / 60.0

DEFAULT_Z_STEP = 200      # DAC counts per point during the sweep
DEFAULT_MOTOR_STEP = 1    # motor steps between sweeps
DEFAULT_MAX_STEPS = 200   # total motor steps allowed in one run
DEFAULT_BASELINE_N = 15   # samples used to characterise the resting reading

# Sample bias. Added after the 2026-09-19 bench session, where two approaches ran
# with the bias at 0 V because the previous script had zeroed it and this tool
# never set it. At 0 V no tunnelling current flows, so the only thing the
# threshold can catch is METAL-TO-METAL contact, carried by the DAC's few-mV
# offset: the tip is driven into the gold before anything trips. So the tool now
# sets the bias itself, and refuses to approach at (or within 0.05 V of) zero.
BIAS_DEFAULT = 38229      # sample -0.5 V (sessions/2026-09-17-bench.md)
BIAS_MIDSCALE = 32768     # 0 V
BIAS_MIN_OFFSET = 546     # counts, about 0.05 V at 5461 counts per 0.5 V


def z_sweep_points(z_from, z_to, step):
    """Inclusive list of Z codes from z_from to z_to, in increments of `step`.

    `step` is a positive magnitude; direction comes from the endpoints. The
    final point is always exactly z_to, so the sweep never overshoots the
    requested end and never stops short of it.
    """
    if step <= 0:
        raise ValueError("step must be positive, got %r" % step)
    points = []
    value = z_from
    if z_to >= z_from:
        while value < z_to:
            points.append(value)
            value += step
    else:
        while value > z_to:
            points.append(value)
            value -= step
    points.append(z_to)
    return points


def stats(values):
    """Mean and sample standard deviation."""
    n = len(values)
    mean = sum(values) / float(n)
    if n < 2:
        return mean, 0.0
    var = sum((v - mean) ** 2 for v in values) / float(n - 1)
    return mean, var ** 0.5


def adc_to_nanoamps(counts, full_scale_volts, feedback_ohms=100e6):
    """Counts to nA. Full scale is 10.24 V -- see docs/FACTS.md. It was
    recorded as 4.096 V until 2026-09-07; that figure is REFBUF, not the span."""
    volts = counts / float(ADC_FULL_SCALE) * full_scale_volts
    return volts / feedback_ohms * 1e9


class Device(object):
    """The firmware's 4-character serial protocol, and nothing else.

    Deliberately small so the approach loop can be exercised against a fake.
    """

    def __init__(self, port, dry_run=False):
        self._port = port
        self.dry_run = dry_run
        self.motor_steps_sent = 0
        self.commands_sent = []

    def _write(self, frame):
        self.commands_sent.append(frame)
        self._port.reset_input_buffer()
        self._port.write(frame)
        self._port.flush()

    def set_z(self, code):
        """DACZ. Silent command."""
        code = int(code)
        if not 0 <= code <= 65535:
            raise ValueError("Z code out of range: %r" % code)
        # Trailing newline: Serial.parseInt() consumes the terminating
        # non-digit, so it is eaten cleanly. Commands WITHOUT an argument must
        # not have one, or it sits in the buffer and corrupts the next command.
        self._write(("DACZ %d\n" % code).encode())
        time.sleep(0.01)

    def read_adc(self, timeout=3.0):
        """GSTS field 5 (index 4) -- a RAW single conversion, not an average.

        Returns None if the reply is malformed, so a glitched read is never
        mistaken for a signal.
        """
        self._write(b"GSTS")
        deadline = time.time() + timeout
        buf = b""
        while time.time() < deadline:
            # Read only what has arrived, or wait for ONE byte. Changed
            # 2026-09-16: read(256) waited out the full 0.2 s port timeout on
            # every call, because a GSTS reply is ~40 bytes, never 256. Measured
            # 0.208 s per read on the bench, which made a two-way Z search take
            # most of a minute per cycle.
            waiting = getattr(self._port, "in_waiting", 0)
            chunk = self._port.read(waiting if waiting else 1)
            if chunk:
                buf += chunk
                if buf.endswith(b"\n"):
                    break
            elif buf:
                break
        parts = buf.decode("ascii", "replace").strip().split(",")
        if len(parts) != 10:
            return None
        try:
            return int(parts[4])
        except ValueError:
            return None

    def set_bias(self, code):
        """BIAS. Silent command. Range-checked before anything reaches the wire:
        an out-of-range code would wrap modulo 65536 in the firmware."""
        code = int(code)
        if not 0 <= code <= 65535:
            raise ValueError("bias code out of range: %r" % code)
        self._write(("BIAS %d\n" % code).encode())
        time.sleep(0.05)

    def move_motor(self, steps):
        """MTMV. Silent AND blocking -- the firmware stops reading serial while
        it runs, so we must wait it out or the next command lands as garbage."""
        steps = int(steps)
        if steps == 0:
            return
        if self.dry_run:
            self.motor_steps_sent += steps
            return
        self._write(("MTMV %d\n" % steps).encode())
        self.motor_steps_sent += steps
        time.sleep(abs(steps) / STEPS_PER_SECOND + 0.5)


class Approach(object):
    """The woodpecker loop. Holds no serial knowledge; talks only to a Device.

    Two modes.

    KNOWN Z DIRECTION (z_retracted and z_extended given): Z parks at the
    retracted end for every motor step and sweeps the full range toward the
    sample. This is the original design.

    UNKNOWN Z DIRECTION (both None) -- added 2026-09-16, because which way our
    disc bends cannot be settled from the repository: it depends on the
    ceramic's poling, which is unknown for our unbranded disc, and on which face
    the improvised tip holder is on. Z parks at MIDSCALE for every motor step,
    and each cycle sweeps midscale -> Z_MIN, then midscale -> Z_MAX. The first
    contact is found on whichever half actually extends, which reveals the
    direction; Z then retracts to the OTHER end. Safe either way provided one
    motor step is much smaller than HALF the Z range: the extending half was
    searched with no contact before every step, so a step cannot carry the tip
    from out of range to a crash while Z sits at midscale. The cost is half the
    search depth per cycle.
    """

    def __init__(self, device, z_retracted, z_extended, motor_step,
                 z_step=DEFAULT_Z_STEP, max_steps=DEFAULT_MAX_STEPS,
                 log=print):
        if motor_step == 0:
            raise ValueError("motor_step must not be zero")
        if (z_retracted is None) != (z_extended is None):
            raise ValueError("give both Z ends, or neither for an unknown Z direction")
        self.dev = device
        self.direction_known = z_retracted is not None
        self.z_retracted = z_retracted
        self.z_extended = z_extended
        self.motor_step = motor_step
        self.z_step = z_step
        self.max_steps = max_steps
        self.log = log
        self.baseline = None
        self.threshold = None
        self.steps_taken = 0
        self.found = False
        self.found_at = None
        # Unknown mode only: 'low' or 'high' once contact shows which end of the
        # Z range moves the tip toward the sample. Stays None if contact was
        # already present at midscale, when the direction cannot be told.
        self.z_toward_sample = None

    @property
    def z_home(self):
        """Where Z waits during motor steps and baseline: the retracted end if
        known, midscale if not."""
        return self.z_retracted if self.z_retracted is not None else Z_PARK

    # -- baseline ---------------------------------------------------------

    def measure_baseline(self, n=DEFAULT_BASELINE_N):
        """Resting reading with Z at home. Returns (mean, stdev)."""
        self.dev.set_z(self.z_home)
        time.sleep(0.5)
        samples = []
        for _ in range(n):
            value = self.dev.read_adc()
            if value is not None:
                samples.append(value)
        if len(samples) < 3:
            raise RuntimeError(
                "Could not read the ADC. Got %d valid samples out of %d.\n"
                "Is the firmware running? Try: python stm_console.py GSTS"
                % (len(samples), n))
        mean, sd = stats(samples)
        self.baseline = mean
        return mean, sd

    def check_headroom(self):
        """Refuse to approach into a railed input. Returns (ok, message)."""
        limit = SATURATION_FRACTION * ADC_FULL_SCALE
        if abs(self.baseline) > limit:
            return False, (
                "Resting reading is %.0f counts, past %.0f%% of full scale.\n"
                "There is no headroom left to detect an increase, so an\n"
                "approach could never trigger and the motor would run to its\n"
                "limit. Fix the preamp offset first -- see STATUS.md."
                % (self.baseline, SATURATION_FRACTION * 100))
        return True, ""

    # -- the loop ---------------------------------------------------------

    def _is_contact(self, value):
        return value is not None and abs(value - self.baseline) >= self.threshold

    def _confirmed(self, first_value):
        """Two more reads at the same Z; contact only if at least 2 of the 3
        cross the threshold. Added 2026-09-16: the raw single conversions this
        tool reads have shown isolated spikes of ~1000 counts on the bench, and
        in unknown-direction mode one spike would be recorded as the Z
        direction. Costs two reads, a few milliseconds, at a real contact."""
        hits = 1 if self._is_contact(first_value) else 0
        for _ in range(2):
            if self._is_contact(self.dev.read_adc()):
                hits += 1
        return hits >= 2

    def _sweep_segment(self, z_from, z_to):
        """Step Z from z_from to z_to reading the ADC. Returns (z, value) at the
        first confirmed contact, or None. Does NOT retract: the caller does, at
        once."""
        for z in z_sweep_points(z_from, z_to, self.z_step):
            self.dev.set_z(z)
            value = self.dev.read_adc()
            if value is None:
                continue  # a malformed reply is not evidence of anything
            if self._is_contact(value) and self._confirmed(value):
                return z, value
        return None

    def _sweep_once(self):
        """One search cycle.

        Returns the Z code where the threshold was crossed, or None.
        Retracts immediately on a hit -- that retract happens here, not in the
        caller, so nothing can run between detection and pulling back.
        """
        if self.direction_known:
            hit = self._sweep_segment(self.z_retracted, self.z_extended)
            if hit is not None:
                self.dev.set_z(self.z_retracted)
                self.found = True
                self.found_at = hit
                return hit[0]
            return None

        # Unknown direction. First: is there already contact at midscale? That
        # should be impossible while a motor step is under half the Z range. If
        # it happens anyway, neither end can be trusted to retract, so stop with
        # Z left at midscale and say so.
        self.dev.set_z(Z_PARK)
        value = self.dev.read_adc()
        if self._is_contact(value) and self._confirmed(value):
            self.found = True
            self.found_at = (Z_PARK, value)
            return Z_PARK

        for end in (Z_MIN, Z_MAX):
            hit = self._sweep_segment(Z_PARK, end)
            if hit is not None and hit[0] == Z_PARK:
                # The hit is at the segment's FIRST point, which is midscale
                # itself: no Z motion produced it, so it says nothing about which
                # end extends. Found on the bench 2026-09-19: the LOW segment found
                # nothing, the sample crept in, and the HIGH segment's first read
                # was over threshold -- reported as "HIGH moves toward the sample"
                # from no evidence at all. Treat it as contact at midscale.
                self.found = True
                self.found_at = hit
                return Z_PARK
            if hit is not None:
                # Contact while moving toward `end`: that end extends toward the
                # sample, so the OTHER end retracts. Pull back there at once;
                # the path passes back through midscale, away from the sample.
                retract_end = Z_MAX if end == Z_MIN else Z_MIN
                self.dev.set_z(retract_end)
                self.z_retracted, self.z_extended = retract_end, end
                self.z_toward_sample = "low" if end == Z_MIN else "high"
                self.found = True
                self.found_at = hit
                return hit[0]
            self.dev.set_z(Z_PARK)
        return None

    def run(self):
        """Returns True if tunneling was found. Always leaves Z at home: the
        retracted end when the direction is known or has just been learned,
        midscale otherwise."""
        if self.baseline is None or self.threshold is None:
            raise RuntimeError("measure_baseline() and a threshold must be set first")
        try:
            while self.steps_taken < self.max_steps:
                hit = self._sweep_once()
                if hit is not None:
                    z, value = self.found_at
                    self.log("")
                    self.log("  TUNNELING at Z = %d after %d motor steps"
                             % (z, self.steps_taken))
                    self.log("  reading %d counts, baseline %.0f, deviation %.0f"
                             % (value, self.baseline, abs(value - self.baseline)))
                    if self.direction_known:
                        self.log("  Z retracted. Motor stopped.")
                        if z == self.z_retracted:
                            # 2026-09-19: contact at the sweep's first point, the
                            # retracted end. "Z retracted" then moves nothing, and
                            # the tip is still in contact.
                            self.log("  WARNING: contact was ALREADY there at the retracted end,")
                            self.log("  so the piezo cannot pull away from it. Back the MOTOR off")
                            self.log("  before anything else.")
                    elif self.z_toward_sample is not None:
                        self.log("  Z DIRECTION FOUND: the %s end of the Z range moves the"
                                 % self.z_toward_sample.upper())
                        self.log("  tip TOWARD the sample. Z retracted to %d. Motor stopped."
                                 % self.z_retracted)
                    else:
                        self.log("  CONTACT ALREADY PRESENT AT MIDSCALE. The Z direction")
                        self.log("  could not be told, so Z was left at %d. Motor stopped."
                                 % Z_PARK)
                        self.log("  Do not move Z or the motor. Power down, then back the")
                        self.log("  sample off by hand.")
                    return True

                # Clamp the last move so the step budget is never exceeded,
                # even when motor_step does not divide evenly into max_steps.
                remaining = self.max_steps - self.steps_taken
                magnitude = min(abs(self.motor_step), remaining)
                move = magnitude if self.motor_step > 0 else -magnitude
                self.dev.set_z(self.z_home)
                self.dev.move_motor(move)
                self.steps_taken += magnitude
                self.log("  %d/%d motor steps, no contact yet"
                         % (self.steps_taken, self.max_steps))
            self.log("")
            self.log("  Step limit reached (%d) with no contact." % self.max_steps)
            self.log("  Nothing is wrong -- this is the safe outcome. Re-run to")
            self.log("  continue, or raise --max-steps if you know the gap is large.")
            return False
        finally:
            # Runs on success, on failure, and on Ctrl-C. The tip must never be
            # left extended. In unknown-direction mode, before any contact, home
            # is midscale: the extending half from there was searched clear
            # before the last motor step, so midscale is out of contact.
            try:
                self.dev.set_z(self.z_home)
            except Exception:
                pass


def check_bias(code, allow_zero=False):
    """(ok, message). An approach needs a bias that can drive a tunnelling
    current; at or near 0 V the threshold can only ever catch metal contact."""
    if not 0 <= code <= 65535:
        return False, "--bias %d is outside 0..65535." % code
    if abs(code - BIAS_MIDSCALE) < BIAS_MIN_OFFSET and not allow_zero:
        return False, ("--bias %d is within 0.05 V of zero. At 0 V no tunnelling current\n"
                       "flows, so this tool could only detect METAL-TO-METAL contact --\n"
                       "the tip would be driven into the sample first. That happened twice\n"
                       "on 2026-09-19. Use the default (%d, sample -0.5 V), or pass\n"
                       "--allow-zero-bias if a zero-bias run is truly what you want."
                       % (code, BIAS_DEFAULT))
    return True, ""


def find_teensy():
    """PJRC vendor ID is 0x16C0."""
    from serial.tools import list_ports
    for p in list_ports.comports():
        if p.vid == 0x16C0:
            return p.device
    ports = list_ports.comports()
    return ports[0].device if len(ports) == 1 else None


def build_parser():
    ap = argparse.ArgumentParser(
        description="PC-side woodpecker coarse approach. Never sends APRH.",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--z-retracted", choices=["low", "high", "unknown"], required=True,
                    help="Which end of the Z DAC range pulls the tip AWAY from "
                         "the sample. 'low' means Z=%d is retracted, 'high' "
                         "means Z=%d is. GETTING THIS BACKWARDS DRIVES THE TIP "
                         "INTO THE SAMPLE. 'unknown' parks Z at midscale (%d) for "
                         "every motor step and searches both ways, which is safe "
                         "without the answer and reports it at first contact."
                         % (Z_MIN, Z_MAX, Z_PARK))
    ap.add_argument("--motor-toward-sample", choices=["positive", "negative"],
                    required=True,
                    help="Which sign of MTMV advances the tip TOWARD the "
                         "sample. Determine this with the tip removed.")
    ap.add_argument("--bias", type=int, default=BIAS_DEFAULT,
                    help="BIAS DAC code set before the baseline (default %d, sample "
                         "-0.5 V). Refused within 0.05 V of zero: a 0 V approach can "
                         "only detect metal contact." % BIAS_DEFAULT)
    ap.add_argument("--allow-zero-bias", action="store_true",
                    help="Permit --bias at or near 0 V. Almost never what you want.")
    ap.add_argument("--threshold", type=int, default=None,
                    help="ADC counts of absolute deviation from baseline that "
                         "count as contact. Default: 6 sigma of the measured "
                         "noise, floor 1500.")
    ap.add_argument("--z-step", type=int, default=DEFAULT_Z_STEP,
                    help="DAC counts per point during the sweep (default %d)"
                         % DEFAULT_Z_STEP)
    ap.add_argument("--motor-step", type=int, default=DEFAULT_MOTOR_STEP,
                    help="Motor steps between sweeps, magnitude only; direction "
                         "comes from --motor-toward-sample (default %d)"
                         % DEFAULT_MOTOR_STEP)
    ap.add_argument("--max-steps", type=int, default=DEFAULT_MAX_STEPS,
                    help="Total motor steps allowed in one run (default %d, "
                         "about %.1f um at 7.8 nm/step)"
                         % (DEFAULT_MAX_STEPS, DEFAULT_MAX_STEPS * 7.8 / 1000.0))
    ap.add_argument("--full-scale", type=float, default=10.24,
                    help="ADC full scale in volts, for reporting currents only. "
                         "ADC full scale in volts. RESOLVED 2026-09-07 from the "
                         "LTC2326-16 datasheet: it is 10.24 V. 4.096 V is REFBUF, "
                         "and the input span is 2.5x REFBUF. See docs/FACTS.md")
    ap.add_argument("-p", "--port")
    ap.add_argument("--dry-run", action="store_true",
                    help="Do everything except actually move the motor.")
    ap.add_argument("-y", "--yes", action="store_true",
                    help="Skip the confirmation prompt.")
    return ap


def main(argv=None):
    opts = build_parser().parse_args(argv)

    if opts.motor_step <= 0:
        print("--motor-step is a magnitude and must be positive.")
        print("Use --motor-toward-sample to choose the direction.")
        return 2
    if opts.z_step <= 0:
        print("--z-step must be positive.")
        return 2
    if opts.max_steps <= 0:
        print("--max-steps must be positive.")
        return 2
    ok, why = check_bias(opts.bias, opts.allow_zero_bias)
    if not ok:
        print(why)
        return 2

    if opts.z_retracted == "low":
        z_retracted, z_extended = Z_MIN, Z_MAX
    elif opts.z_retracted == "high":
        z_retracted, z_extended = Z_MAX, Z_MIN
    else:
        z_retracted, z_extended = None, None
    motor_step = (opts.motor_step if opts.motor_toward_sample == "positive"
                  else -opts.motor_step)

    portname = opts.port or find_teensy()
    if not portname:
        print("No Teensy found. Pass one with -p, or check the USB cable is a")
        print("DATA cable and not charge-only.")
        return 1

    print("=" * 68)
    print("  COARSE APPROACH -- this moves a real tip toward a real sample")
    print("=" * 68)
    print("  port              %s%s" % (portname, "   [DRY RUN]" if opts.dry_run else ""))
    if z_retracted is None:
        print("  Z direction       UNKNOWN: Z parks at %d for every motor step and"
              % Z_PARK)
        print("                    searches toward %d and toward %d each cycle"
              % (Z_MIN, Z_MAX))
    else:
        print("  Z retracted at    %d      extends toward sample to %d"
              % (z_retracted, z_extended))
    print("  sample bias       code %d (%+.2f V at the sample)"
          % (opts.bias, -(opts.bias - BIAS_MIDSCALE) * 0.5 / 5461.0))
    print("  motor step        %+d per cycle, up to %d steps (~%.1f um)"
          % (motor_step, opts.max_steps, opts.max_steps * 7.8 / 1000.0))
    print("")
    print("  BEFORE YOU CONTINUE:")
    print("   - LED1 to LED4 must be DARK. If any is lit the DACs have lost")
    print("     configuration, every Z command below does nothing, and the")
    print("     motor would advance with no piezo protection at all.")
    print("   - Nobody within a metre of the preamp.")
    if z_retracted is None:
        print("   - Ctrl-C stops at any time and sends Z to midscale.")
    else:
        print("   - Ctrl-C stops at any time and retracts Z.")
    print("")

    if not opts.yes:
        try:
            if input("  Type 'go' to start: ").strip().lower() != "go":
                print("  Cancelled.")
                return 0
        except (EOFError, KeyboardInterrupt):
            print("\n  Cancelled.")
            return 0

    import serial
    try:
        port = serial.Serial(portname, 115200, timeout=0.2)
    except serial.SerialException as e:
        print("Could not open %s: %s" % (portname, e))
        print("Something else has the port open -- close the GUI or console.")
        return 1

    with port:
        time.sleep(1.0)
        dev = Device(port, dry_run=opts.dry_run)
        # Set the bias HERE, every run: never inherit whatever the last script left.
        dev.set_bias(opts.bias)
        app = Approach(dev, z_retracted, z_extended, motor_step,
                       z_step=opts.z_step, max_steps=opts.max_steps)

        if z_retracted is None:
            print("\n  Measuring baseline with Z at midscale...")
        else:
            print("\n  Measuring baseline with Z retracted...")
        try:
            mean, sd = app.measure_baseline()
        except RuntimeError as e:
            print("  %s" % e)
            return 1
        print("  baseline %.0f counts, noise %.0f counts RMS (%.2f nA)"
              % (mean, sd, adc_to_nanoamps(sd, opts.full_scale)))

        ok, why = app.check_headroom()
        if not ok:
            print("")
            print("  REFUSING TO APPROACH.")
            for line in why.splitlines():
                print("  " + line)
            return 1

        if opts.threshold is not None:
            app.threshold = opts.threshold
        else:
            app.threshold = max(int(6 * sd), 1500)
        print("  threshold %d counts (%.2f nA) of deviation either way"
              % (app.threshold, adc_to_nanoamps(app.threshold, opts.full_scale)))
        print("  A high threshold costs almost no depth: tunneling current rises")
        print("  about 10x per Angstrom, so 6 nA is under an Angstrom past 1 nA.")
        print("")

        try:
            found = app.run()
        except KeyboardInterrupt:
            # Approach.run()'s finally clause has already sent Z home: the
            # retracted end if known, midscale if not.
            print("\n  Stopped by user. Z sent to %d, motor stopped." % app.z_home)
            print("  %d motor steps were taken." % app.steps_taken)
            return 130

        if app.z_toward_sample is not None:
            other = "high" if app.z_toward_sample == "low" else "low"
            print("")
            print("  RECORD THIS: Z toward the sample is the %s end, so next time"
                  % app.z_toward_sample.upper())
            print("  use --z-retracted %s. Write it into docs/OPEN_QUESTIONS.md." % other)

        if opts.dry_run:
            print("")
            print("  DRY RUN: %d motor steps would have been sent, none were."
                  % dev.motor_steps_sent)
        return 0 if found else 1


if __name__ == "__main__":
    sys.exit(main())
