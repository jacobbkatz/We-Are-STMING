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

Both are recorded as UNKNOWN in docs/OPEN_QUESTIONS.md. Determine them before
using this, with the tip removed or far away.

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
    """Counts to nA. full_scale_volts is the unresolved 4.096 vs 10.24 question."""
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
            chunk = self._port.read(256)
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
    """The woodpecker loop. Holds no serial knowledge; talks only to a Device."""

    def __init__(self, device, z_retracted, z_extended, motor_step,
                 z_step=DEFAULT_Z_STEP, max_steps=DEFAULT_MAX_STEPS,
                 log=print):
        if motor_step == 0:
            raise ValueError("motor_step must not be zero")
        self.dev = device
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

    # -- baseline ---------------------------------------------------------

    def measure_baseline(self, n=DEFAULT_BASELINE_N):
        """Resting reading with Z fully retracted. Returns (mean, stdev)."""
        self.dev.set_z(self.z_retracted)
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

    def _sweep_once(self):
        """One Z sweep from retracted toward the sample.

        Returns the Z code where the threshold was crossed, or None.
        Retracts immediately on a hit -- that retract happens here, not in the
        caller, so nothing can run between detection and pulling back.
        """
        for z in z_sweep_points(self.z_retracted, self.z_extended, self.z_step):
            self.dev.set_z(z)
            value = self.dev.read_adc()
            if value is None:
                continue  # a malformed reply is not evidence of anything
            if abs(value - self.baseline) >= self.threshold:
                self.dev.set_z(self.z_retracted)
                self.found = True
                self.found_at = (z, value)
                return z
        return None

    def run(self):
        """Returns True if tunneling was found. Always leaves Z retracted."""
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
                    self.log("  Z retracted. Motor stopped.")
                    return True

                # Clamp the last move so the step budget is never exceeded,
                # even when motor_step does not divide evenly into max_steps.
                remaining = self.max_steps - self.steps_taken
                magnitude = min(abs(self.motor_step), remaining)
                move = magnitude if self.motor_step > 0 else -magnitude
                self.dev.set_z(self.z_retracted)
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
            # left extended.
            try:
                self.dev.set_z(self.z_retracted)
            except Exception:
                pass


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
    ap.add_argument("--z-retracted", choices=["low", "high"], required=True,
                    help="Which end of the Z DAC range pulls the tip AWAY from "
                         "the sample. 'low' means Z=%d is retracted, 'high' "
                         "means Z=%d is. GETTING THIS BACKWARDS DRIVES THE TIP "
                         "INTO THE SAMPLE." % (Z_MIN, Z_MAX))
    ap.add_argument("--motor-toward-sample", choices=["positive", "negative"],
                    required=True,
                    help="Which sign of MTMV advances the tip TOWARD the "
                         "sample. Determine this with the tip removed.")
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
    ap.add_argument("--full-scale", type=float, default=4.096,
                    help="ADC full scale in volts, for reporting currents only. "
                         "4.096 vs 10.24 is unresolved -- see OPEN_QUESTIONS.md")
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

    if opts.z_retracted == "low":
        z_retracted, z_extended = Z_MIN, Z_MAX
    else:
        z_retracted, z_extended = Z_MAX, Z_MIN
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
    print("  Z retracted at    %d      extends toward sample to %d"
          % (z_retracted, z_extended))
    print("  motor step        %+d per cycle, up to %d steps (~%.1f um)"
          % (motor_step, opts.max_steps, opts.max_steps * 7.8 / 1000.0))
    print("")
    print("  BEFORE YOU CONTINUE:")
    print("   - LED1 to LED4 must be DARK. If any is lit the DACs have lost")
    print("     configuration, every Z command below does nothing, and the")
    print("     motor would advance with no piezo protection at all.")
    print("   - Nobody within a metre of the preamp.")
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
        app = Approach(dev, z_retracted, z_extended, motor_step,
                       z_step=opts.z_step, max_steps=opts.max_steps)

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
            # Approach.run()'s finally clause has already retracted Z.
            print("\n  Stopped by user. Z retracted, motor stopped.")
            print("  %d motor steps were taken." % app.steps_taken)
            return 130

        if opts.dry_run:
            print("")
            print("  DRY RUN: %d motor steps would have been sent, none were."
                  % dev.motor_steps_sent)
        return 0 if found else 1


if __name__ == "__main__":
    sys.exit(main())
