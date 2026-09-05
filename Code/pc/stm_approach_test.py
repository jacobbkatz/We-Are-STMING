#!/usr/bin/env python3
"""
Tests for stm_approach.py, run against a simulated microscope.

Neither of us can read code, so this exists to prove the approach logic behaves
before it is ever pointed at real hardware. Run it any time the script changes:

    python Code/pc/stm_approach_test.py

Every test must pass. A failure means DO NOT use stm_approach.py until it is
fixed.

The simulated microscope models a tip closing on a sample: motor steps and
piezo extension both shrink the gap, and the tunneling current appears when the
gap closes. It deliberately also covers the case the firmware gets wrong --
tunneling that drives the ADC reading NEGATIVE.
"""

import contextlib
import io
import sys
import unittest

import stm_approach as A


@contextlib.contextmanager
def _quiet_stderr():
    """argparse prints usage to stderr when it rejects arguments. That is the
    behaviour under test, so hide it -- a passing run should look clean."""
    saved, sys.stderr = sys.stderr, io.StringIO()
    try:
        yield
    finally:
        sys.stderr = saved


class FakeScope(object):
    """A microscope on the bench, in software.

    gap_counts shrinks as the motor advances and as the piezo extends. When it
    reaches zero the tunneling current appears, with a sign we can choose.
    """

    def __init__(self, gap=30000, baseline=-400, tunnel_delta=-9000,
                 noise=0, z_retracted=A.Z_MIN, z_per_count=1.0,
                 counts_per_motor_step=2500, dead_dacs=False,
                 malformed_every=0):
        self.gap = gap
        self.baseline = baseline
        self.tunnel_delta = tunnel_delta      # negative = current drives reading down
        self.noise = noise
        self.z_retracted = z_retracted
        self.z_per_count = z_per_count
        self.counts_per_motor_step = counts_per_motor_step
        self.dead_dacs = dead_dacs            # DACs lost config: Z commands do nothing
        self.malformed_every = malformed_every

        self.z = z_retracted
        self.motor_advance = 0.0
        self.motor_steps_sent = 0
        self.commands = []
        self._reads = 0
        self.max_penetration = 0.0            # how far past contact we ever got

    # -- Device interface --------------------------------------------------

    def set_z(self, code):
        self.commands.append(("DACZ", code))
        if not self.dead_dacs:
            self.z = code

    def move_motor(self, steps):
        self.commands.append(("MTMV", steps))
        self.motor_steps_sent += steps
        self.motor_advance += abs(steps) * self.counts_per_motor_step

    def read_adc(self):
        self._reads += 1
        if self.malformed_every and self._reads % self.malformed_every == 0:
            return None
        z_advance = abs(self.z - self.z_retracted) * self.z_per_count
        remaining = self.gap - self.motor_advance - z_advance
        if remaining < 0:
            self.max_penetration = max(self.max_penetration, -remaining)
        value = self.baseline
        if remaining <= 0:
            value += self.tunnel_delta
        return int(value)


def make_approach(scope, **kw):
    kw.setdefault("z_retracted", A.Z_MIN)
    kw.setdefault("z_extended", A.Z_MAX)
    kw.setdefault("motor_step", 1)
    kw.setdefault("max_steps", 50)
    kw.setdefault("log", lambda *a, **k: None)
    return A.Approach(scope, **kw)


class TestSweepPoints(unittest.TestCase):
    """The Z sweep must cover the range exactly, in either direction."""

    def test_ascending_hits_both_ends(self):
        pts = A.z_sweep_points(10000, 50000, 10000)
        self.assertEqual(pts, [10000, 20000, 30000, 40000, 50000])

    def test_descending_hits_both_ends(self):
        pts = A.z_sweep_points(50000, 10000, 10000)
        self.assertEqual(pts, [50000, 40000, 30000, 20000, 10000])

    def test_uneven_step_still_ends_exactly_on_target(self):
        pts = A.z_sweep_points(10000, 50000, 30000)
        self.assertEqual(pts, [10000, 40000, 50000])
        self.assertEqual(pts[-1], 50000, "sweep must end exactly at the target")

    def test_uneven_step_descending_ends_exactly(self):
        pts = A.z_sweep_points(50000, 10000, 30000)
        self.assertEqual(pts, [50000, 20000, 10000])

    def test_step_larger_than_range(self):
        self.assertEqual(A.z_sweep_points(10000, 50000, 99999), [10000, 50000])

    def test_never_overshoots_the_endpoint(self):
        for step in (1, 7, 199, 200, 4001, 39999, 40000, 40001):
            for a, b in ((10000, 50000), (50000, 10000)):
                pts = A.z_sweep_points(a, b, step)
                lo, hi = min(a, b), max(a, b)
                self.assertTrue(all(lo <= p <= hi for p in pts),
                                "step=%d %d->%d left the range" % (step, a, b))
                self.assertEqual(pts[0], a)
                self.assertEqual(pts[-1], b)

    def test_zero_or_negative_step_rejected(self):
        for bad in (0, -1, -200):
            with self.assertRaises(ValueError):
                A.z_sweep_points(10000, 50000, bad)


class TestStats(unittest.TestCase):
    def test_mean_and_stdev(self):
        mean, sd = A.stats([2, 4, 4, 4, 5, 5, 7, 9])
        self.assertAlmostEqual(mean, 5.0)
        self.assertAlmostEqual(sd, 2.13809, places=4)

    def test_single_sample_has_zero_stdev(self):
        mean, sd = A.stats([42])
        self.assertEqual((mean, sd), (42.0, 0.0))


class TestFindsTunneling(unittest.TestCase):

    def test_finds_negative_going_current(self):
        """THE case the firmware's signed `>` comparison misses entirely."""
        scope = FakeScope(gap=30000, baseline=-400, tunnel_delta=-9000)
        app = make_approach(scope)
        app.measure_baseline(n=5)
        app.threshold = 2000
        self.assertTrue(app.run(), "must detect current that drives the ADC DOWN")
        self.assertTrue(app.found)

    def test_finds_positive_going_current(self):
        scope = FakeScope(gap=30000, baseline=-400, tunnel_delta=+9000)
        app = make_approach(scope)
        app.measure_baseline(n=5)
        app.threshold = 2000
        self.assertTrue(app.run())

    def test_retracts_z_immediately_after_finding(self):
        scope = FakeScope(gap=30000)
        app = make_approach(scope)
        app.measure_baseline(n=5)
        app.threshold = 2000
        self.assertTrue(app.run())
        self.assertEqual(scope.commands[-1], ("DACZ", A.Z_MIN),
                         "the last thing sent must be a retract")
        self.assertEqual(scope.z, A.Z_MIN)

    def test_motor_only_ever_moves_while_z_is_retracted(self):
        """THE woodpecker invariant. If this fails the design is unsafe.

        Replays the whole command stream and checks that at the moment of every
        single MTMV, Z was parked at the retracted end. This is what stops the
        motor closing a gap the piezo is already holding open.
        """
        for gap in (5000, 30000, 90000, 250000):
            for z_ret, z_ext in ((A.Z_MIN, A.Z_MAX), (A.Z_MAX, A.Z_MIN)):
                scope = FakeScope(gap=gap, z_retracted=z_ret)
                app = make_approach(scope, z_retracted=z_ret, z_extended=z_ext,
                                    max_steps=60)
                app.measure_baseline(n=5)
                app.threshold = 2000
                app.run()
                z_now = None
                for kind, value in scope.commands:
                    if kind == "DACZ":
                        z_now = value
                    elif kind == "MTMV":
                        self.assertEqual(
                            z_now, z_ret,
                            "motor moved with Z at %r, not retracted (%r), "
                            "gap=%d" % (z_now, z_ret, gap))

    def test_no_motor_movement_after_contact(self):
        """Nothing may drive the motor once tunneling has been seen.

        Gap is deliberately wider than the piezo alone can close, so motor
        steps definitely happen before contact.
        """
        scope = FakeScope(gap=90000)
        app = make_approach(scope)
        app.measure_baseline(n=5)
        app.threshold = 2000
        self.assertTrue(app.run())
        kinds = [c[0] for c in scope.commands]
        last_motor = len(kinds) - 1 - kinds[::-1].index("MTMV")
        # every command after the final motor move must be a Z command
        self.assertTrue(all(k == "DACZ" for k in kinds[last_motor + 1:]),
                        "something other than a retract followed the last move")

    def test_contact_reachable_by_piezo_alone_needs_no_motor(self):
        scope = FakeScope(gap=5000, counts_per_motor_step=2500)
        app = make_approach(scope)
        app.measure_baseline(n=5)
        app.threshold = 2000
        self.assertTrue(app.run())
        self.assertEqual(scope.motor_steps_sent, 0,
                         "piezo could reach it; the motor should never have moved")


class TestSafety(unittest.TestCase):

    def test_never_sends_APRH(self):
        scope = FakeScope(gap=10**9)  # never reachable
        app = make_approach(scope, max_steps=5)
        app.measure_baseline(n=5)
        app.threshold = 2000
        app.run()
        sent = set(c[0] for c in scope.commands)
        self.assertNotIn("APRH", sent)
        self.assertTrue(sent <= {"DACZ", "MTMV"}, "unexpected command: %r" % sent)

    def test_respects_max_steps(self):
        scope = FakeScope(gap=10**9)
        app = make_approach(scope, max_steps=7)
        app.measure_baseline(n=5)
        app.threshold = 2000
        self.assertFalse(app.run())
        self.assertEqual(abs(scope.motor_steps_sent), 7)

    def test_max_steps_respected_with_multi_step_moves(self):
        scope = FakeScope(gap=10**9)
        app = make_approach(scope, motor_step=3, max_steps=7)
        app.measure_baseline(n=5)
        app.threshold = 2000
        app.run()
        self.assertEqual(abs(scope.motor_steps_sent), 7,
                         "step budget must be exact, not rounded up to 9")
        self.assertEqual(app.steps_taken, 7)

    def test_z_retracted_when_step_limit_reached(self):
        scope = FakeScope(gap=10**9)
        app = make_approach(scope, max_steps=3)
        app.measure_baseline(n=5)
        app.threshold = 2000
        app.run()
        self.assertEqual(scope.z, A.Z_MIN)

    def test_z_retracted_even_if_something_throws(self):
        """The finally clause must pull the tip back on any failure path."""
        scope = FakeScope(gap=10**9)

        calls = {"n": 0}
        real_read = scope.read_adc

        def exploding_read():
            calls["n"] += 1
            if calls["n"] > 12:
                raise RuntimeError("simulated USB unplug")
            return real_read()

        app = make_approach(scope, max_steps=50)
        app.measure_baseline(n=5)
        app.threshold = 2000
        scope.read_adc = exploding_read
        with self.assertRaises(RuntimeError):
            app.run()
        self.assertEqual(scope.z, A.Z_MIN, "tip left extended after a crash")

    def test_z_retracted_on_keyboard_interrupt(self):
        scope = FakeScope(gap=10**9)
        calls = {"n": 0}
        real_read = scope.read_adc

        def interrupting_read():
            calls["n"] += 1
            if calls["n"] > 12:
                raise KeyboardInterrupt()
            return real_read()

        app = make_approach(scope, max_steps=50)
        app.measure_baseline(n=5)
        app.threshold = 2000
        scope.read_adc = interrupting_read
        with self.assertRaises(KeyboardInterrupt):
            app.run()
        self.assertEqual(scope.z, A.Z_MIN, "Ctrl-C left the tip extended")

    def test_refuses_when_input_is_railed(self):
        """The preamp's present state: ~29873 counts, no headroom."""
        scope = FakeScope(gap=30000, baseline=29873, tunnel_delta=0)
        app = make_approach(scope)
        app.measure_baseline(n=5)
        ok, why = app.check_headroom()
        self.assertFalse(ok)
        self.assertIn("headroom", why)

    def test_allows_a_healthy_baseline(self):
        scope = FakeScope(gap=30000, baseline=-400)
        app = make_approach(scope)
        app.measure_baseline(n=5)
        ok, _ = app.check_headroom()
        self.assertTrue(ok)

    def test_railed_negative_also_refused(self):
        scope = FakeScope(gap=30000, baseline=-29873, tunnel_delta=0)
        app = make_approach(scope)
        app.measure_baseline(n=5)
        ok, _ = app.check_headroom()
        self.assertFalse(ok, "a negative rail is just as saturated")

    def test_malformed_replies_never_trigger_a_false_positive(self):
        scope = FakeScope(gap=10**9, malformed_every=3)
        app = make_approach(scope, max_steps=4)
        app.measure_baseline(n=8)
        app.threshold = 2000
        self.assertFalse(app.run(), "a dropped reply was read as contact")

    def test_zero_motor_step_rejected(self):
        scope = FakeScope()
        with self.assertRaises(ValueError):
            make_approach(scope, motor_step=0)

    def test_run_refuses_without_a_threshold(self):
        scope = FakeScope()
        app = make_approach(scope)
        with self.assertRaises(RuntimeError):
            app.run()

    def test_baseline_refuses_when_adc_is_unreadable(self):
        scope = FakeScope(malformed_every=1)  # every read fails
        app = make_approach(scope)
        with self.assertRaises(RuntimeError):
            app.measure_baseline(n=5)


class TestDirectionHandling(unittest.TestCase):
    """Both Z orientations must work, since which is which is still unknown."""

    def test_z_retracted_high(self):
        scope = FakeScope(gap=30000, z_retracted=A.Z_MAX)
        app = make_approach(scope, z_retracted=A.Z_MAX, z_extended=A.Z_MIN)
        app.measure_baseline(n=5)
        app.threshold = 2000
        self.assertTrue(app.run())
        self.assertEqual(scope.z, A.Z_MAX, "must retract to the HIGH end here")

    def test_negative_motor_direction(self):
        scope = FakeScope(gap=10**9)
        app = make_approach(scope, motor_step=-1, max_steps=5)
        app.measure_baseline(n=5)
        app.threshold = 2000
        app.run()
        self.assertEqual(scope.motor_steps_sent, -5)
        self.assertEqual(app.steps_taken, 5, "step budget counts magnitude")


class TestArgumentParsing(unittest.TestCase):
    """The two direction arguments must be impossible to forget."""

    def test_directions_are_required(self):
        parser = A.build_parser()
        for argv in ([], ["--z-retracted", "low"],
                     ["--motor-toward-sample", "positive"]):
            with self.assertRaises(SystemExit), _quiet_stderr():
                parser.parse_args(argv)

    def test_valid_arguments_accepted(self):
        opts = A.build_parser().parse_args(
            ["--z-retracted", "low", "--motor-toward-sample", "positive"])
        self.assertEqual(opts.z_retracted, "low")
        self.assertEqual(opts.max_steps, A.DEFAULT_MAX_STEPS)

    def test_bad_direction_value_rejected(self):
        with self.assertRaises(SystemExit), _quiet_stderr():
            A.build_parser().parse_args(
                ["--z-retracted", "sideways", "--motor-toward-sample", "positive"])


class TestDeviceFraming(unittest.TestCase):
    """The firmware reads 4 bytes as soon as one arrives, so framing matters."""

    class FakePort(object):
        def __init__(self):
            self.writes = []

        def reset_input_buffer(self):
            pass

        def write(self, b):
            self.writes.append(b)

        def flush(self):
            pass

        def read(self, n):
            return b""

    def test_dacz_frame_has_command_arg_and_newline(self):
        port = self.FakePort()
        A.Device(port).set_z(32768)
        self.assertEqual(port.writes, [b"DACZ 32768\n"])

    def test_gsts_frame_has_no_newline(self):
        """A no-argument command must not send a newline; parseInt is never
        called, so it would sit in the buffer and corrupt the next command."""
        port = self.FakePort()
        A.Device(port).read_adc(timeout=0.01)
        self.assertEqual(port.writes, [b"GSTS"])

    def test_out_of_range_z_rejected(self):
        port = self.FakePort()
        dev = A.Device(port)
        for bad in (-1, 65536, 100000):
            with self.assertRaises(ValueError):
                dev.set_z(bad)
        self.assertEqual(port.writes, [], "a bad code must never reach the wire")

    def test_dry_run_sends_no_motor_command(self):
        port = self.FakePort()
        dev = A.Device(port, dry_run=True)
        dev.move_motor(5)
        self.assertEqual(port.writes, [])
        self.assertEqual(dev.motor_steps_sent, 5)

    def test_zero_step_move_is_a_noop(self):
        port = self.FakePort()
        dev = A.Device(port)
        dev.move_motor(0)
        self.assertEqual(port.writes, [])

    def test_read_adc_parses_field_five(self):
        class Replying(TestDeviceFraming.FakePort):
            def read(self, n):
                out = self._buf
                self._buf = b""
                return out
        port = Replying()
        # bias,dac_z,dac_x,dac_y,adc,steps,appr,cc,scan,millis
        port._buf = b"0,32768,0,0,-1234,10,0,0,0,5000\n"
        self.assertEqual(A.Device(port).read_adc(timeout=0.5), -1234)

    def test_read_adc_returns_none_on_short_reply(self):
        class Replying(TestDeviceFraming.FakePort):
            def read(self, n):
                out = self._buf
                self._buf = b""
                return out
        port = Replying()
        port._buf = b"0,32768,0\n"
        self.assertIsNone(A.Device(port).read_adc(timeout=0.5))


if __name__ == "__main__":
    unittest.main(verbosity=2)
