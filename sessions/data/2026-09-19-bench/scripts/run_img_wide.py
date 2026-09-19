import sys
sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
sys.path.insert(0, r"C:\Users\jacob\AppData\Local\Temp\claude\C--Users-jacob-OneDrive-Desktop-CUsersyournameSTM\851972b6-d618-4bb1-ba1f-dc9b1865615d\scratchpad")
import stm_feedback_scan as fs
fs.Z_MAX_SAFE = 60000
import scan2
scan2.main(sys.argv[1:])
