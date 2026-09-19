"""stm_y_control with this tip's loop tuning and a Z window widened to 60000 at the top.
Direction confirmed HIGH-toward for this tip (lock-in 4.2 sigma; the loop held with that sign)."""
import sys
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
import stm_feedback_scan as fs
fs.COUNTS_PER_DECADE = 100.0
fs.Z_MAX_SAFE = 60000
fs.Z_LOCATE_END = 60000
xheld = "--xheld" in sys.argv
args = [a for a in sys.argv[1:] if a != "--xheld"]
if xheld:
    import stm_approach
    _orig = stm_approach.Device._write
    def _held(self, frame):
        if frame.startswith(b"DACX"):
            frame = b"DACX 32768\n"
        return _orig(self, frame)
    stm_approach.Device._write = _held
import stm_y_control
sys.exit(stm_y_control.main(args))
