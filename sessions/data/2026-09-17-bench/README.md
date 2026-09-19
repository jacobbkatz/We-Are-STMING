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
| **`line_repeated_wide.csv`** | **Twelve passes of ONE line at +-15,000 X.** The source of the 636-count profile that `sessions/2026-09-17-bench.md` section 3.25 carried as UNDETERMINED. **Closed 2026-09-19: it is the feedback loop recovering from the 30,000-count X flyback between passes on a tilted surface** - predicted Z error 3,144 counts, and dropping two pixels of twenty-one collapses the consecutive-pass correlation to zero. `deliverables/2026-09-19-pause/candidates/VERDICT.md` |
| **`scan_wide_25nm_1.csv`, `scan_wide_25nm_2.csv`** | **Two COMPLETE images of the same nine Y places on the same X grid, at +-15,000.** **These are the +-15,000 place test that section 3.25 says 'has not been run'. It had been, and the data were in this directory the whole time** - same place +0.216 +- 0.228 against different place +0.074 +- 0.063, permutation p = 0.24 |
| `line_three_y_positions.csv` | One line at three Y positions |

> **Added 2026-09-19. These four files were in this directory but NOT in this table**, and the table is the
> only index of it. **That omission is the likeliest reason `sessions/2026-09-17-bench.md` section 3.25
> recorded the place test as never run while its data sat in the same folder** - the fifth time in this
> project that something recorded as unavailable was already here (`CLAUDE.md` section 3b keeps the tally).
> **An index that is missing entries is worse than no index, because it is believed.** When a file is added
> to a data directory, add its row the same session.

**None of them reproduces.** The analysis, and the spectrum that explains why,
are in `sessions/2026-09-17-bench.md` section 3.24.
