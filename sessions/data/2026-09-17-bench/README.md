# Raw scan data, 2026-09-17 bench session

Every file is a constant-current scan taken with `Code/pc/stm_feedback_scan.py`
or a diagnostic variant of it. **The value in each cell is the Z DAC code the
feedback loop needed to hold the setpoint current at that pixel** — the height
map. Each line appears twice, `fwd` and `back`, which is the trace-and-retrace
pair.

Column header is the X DAC code; the first column is the Y DAC code.

| File | What it is |
|---|---|
| `scan_slow_1/2.csv` | The first two images, before the read timeout was fixed. 38-60 s each |
| `scan_fast_1..4.csv` | Four images of the same patch, 4.5-6.2 s each |
| `diag_scan_normal_1/2.csv` | 15 loop corrections per pixel |
| **`diag_scan_x_held.csv`** | **The control: identical timing, X never moved.** Shows as much apparent structure as a real scan |
| `diag_line_repeated.csv` | One line scanned ten times. Consecutive lines correlate at +0.11 |
| `scan_slow_dwell_1/2.csv` | 250 corrections per pixel, 60-88 s per image |
| `scan_wide_slow_1/2.csv` | +-4000 X counts, slow loop |

**None of them reproduces.** The analysis, and the spectrum that explains why,
are in `sessions/2026-09-17-bench.md` section 3.24.
