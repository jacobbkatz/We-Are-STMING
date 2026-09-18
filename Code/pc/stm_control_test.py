"""Tests for stm_control.py, the GUI's serial layer.

THIS FILE HAS NEVER PASSED. It went in with the repository's first commit
(`aa564e4`, "First itteration of all files uploaded") calling `open()` with no
argument against an `open(self, device)`, so every run has ended in

    TypeError: STM.open() missing 1 required positional argument: 'device'

Found 2026-09-19 by running the whole suite as a suite for the first time.
`CLAUDE.md` section 7 says a test that has never FAILED has not been run; this
is the mirror image -- a test that has never PASSED, sitting in the tree
looking like coverage.

It cannot be made to pass unattended either: `open()` calls `serial.Serial`
on a real port and then `set_buffer_size`, which is **pySerial's Windows-only
method** and raises on Linux and macOS. So this is an INTEGRATION test that
needs the instrument plugged in.

It now says so, and SKIPS instead of erroring, so a red suite means something.

    py stm_control_test.py                 # skips, no hardware needed
    STM_PORT=COM3 py stm_control_test.py   # actually talks to the board
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import stm_control

PORT = os.environ.get("STM_PORT")


@unittest.skipUnless(PORT, "set STM_PORT (e.g. COM3) to run against the real board")
class TestStm(unittest.TestCase):
    """Live test. `stm_control` is the GUI's layer -- `stm_app.py` imports it.

    Nothing else in the repository does, and the bench tools
    (`stm_console.py`, `stm_approach.py`, `stm_feedback_scan.py`,
    `stm_noise_spectrum.py`) use their own `Device` instead.
    """

    def setUp(self):
        self.stm = stm_control.STM()
        self.stm.open(PORT)
        self.addCleanup(self._close)

    def _close(self):
        port = getattr(self.stm, "stm_serial", None)
        if port is not None and getattr(port, "is_open", False):
            port.close()

    def test_get_status(self):
        status = self.stm.get_status()
        print(status)
        self.assertIsNotNone(status, "GSTS returned nothing -- is the board powered?")


class TestImportable(unittest.TestCase):
    """Runs everywhere. Catches the thing that actually broke: a signature
    change in stm_control that its only caller would not survive."""

    def test_open_takes_a_device(self):
        import inspect
        params = list(inspect.signature(stm_control.STM.open).parameters)
        self.assertEqual(params, ["self", "device"],
                         "stm_control.STM.open changed shape; stm_app.py calls it")


if __name__ == "__main__":
    unittest.main(verbosity=2)
