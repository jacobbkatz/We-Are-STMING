"""The three-Y control with X HELD at midscale: identical timing, no lateral motion. Every DACX
frame is rewritten to DACX 32768 before it reaches the wire. Gives tonight's noise floor."""
import sys
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
import stm_feedback_scan as fs
fs.COUNTS_PER_DECADE = 100.0
import stm_approach
_orig = stm_approach.Device._write
def _held(self, frame):
    if frame.startswith(b"DACX"):
        frame = b"DACX 32768\n"
    return _orig(self, frame)
stm_approach.Device._write = _held
import stm_y_control
sys.exit(stm_y_control.main(sys.argv[1:]))
