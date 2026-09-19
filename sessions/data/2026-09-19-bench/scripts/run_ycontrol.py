import sys
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
import stm_feedback_scan as fs
fs.COUNTS_PER_DECADE = 100.0      # this tip's loop tuning (held the junction in catch_and_scan run 9)
import stm_y_control
sys.exit(stm_y_control.main(sys.argv[1:]))
