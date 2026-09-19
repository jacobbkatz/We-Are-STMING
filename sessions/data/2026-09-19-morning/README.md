# 2026-09-19 morning bench data

Recorded by **`sessions/2026-09-19-morning.md`** — 2026-09-19, about 11:15-13:30 UTC, on Jacob's laptop
(COM3). Times are UTC. `ADCR` averaged reads throughout; 320.5 counts per nA; sample −0.5 V is
`BIAS 38229`, +0.5 V `27307`, −0.1 V `33860`, +0.1 V `31676`. **For this tip (fitted ~03:00 UTC
2026-09-19) HIGH Z extends toward the sample; Z 0 is fully retracted. NEGATIVE `MTMV` approaches.**

**Scripts are in `scripts/`: scratch kept as provenance, run only on Jacob's laptop (absolute paths,
`winsound`), all assuming HIGH Z = toward the sample.** Fourteen have a `--test` self-test on simulated
junctions; **six do not** (`live_backoff_z0.py`, `zjump.py`, `where.py`, `passive_z0.py`, `touchtest.py`,
`final.py`). **Every script refuses options it does not recognise** (added after a `--test` on a script
without one reached its hardware path; no port was connected). `.csv` files carry raw points; `.log` files
the console.

> **The approach sweeps in `apz_*`, `release_watch_*` and `where_*` ran in 1,000-count Z steps, not the
> 250 their scripts set**: `fastwood.sweep` bound its step as a default argument when defined, so the
> override was ignored. **Every onset they recorded is a multiple of 1,000.** Fixed after the session.

| File | What |
|---|---|
| `baseline_run1.log` | Power-up: `GSTS`, `ADCR` at 0/−0.5/+0.5/0 V with Z 0, then a gentle walk to midscale. Tip clear |
| `live_backoff_run1.log` | Hand-set 1, the 2026-09-19 live back-off at Z midscale: contact 11:24:40, clear 11:24:55 |
| `creep_watch_run1.log` | 8.0 minutes at Z midscale, nothing moving: no current. **Its CSV was lost** |
| `ztest_run1.log`, `ztest_1789817796.csv` | First Z test: nothing in Z 32768-62000 |
| `approach_run1.log` | `Code/pc/stm_approach.py`, single steps: 111 toward the sample, nothing (stopped by hand for hand-set 2) |
| `touch_and_hold_run1.log` | Hand-set 2 without a hand back-off: contact 11:44:36, railed at Z 0 |
| `backoff_motor_run1.log`, `_run2.log` | +80 and +300 single retract steps: still railed |
| `live_backoff_z0_run1.log` | Hand-set 3, the back-off with Z held at 0: clear 11:53:35 |
| `stairs_run1.log`, `stairs_1789818942.csv` | Two full finds 11:55:42-11:56:19: nothing in Z 0-62000 |
| `fastwood_run1.log`, `fastwood_1789819103.csv` | 650 single approach steps with a 1,000-count sweep: nothing |
| `zjump_run1.log` | **Read check and Z-jump transient**: 2 of 4 upward 0→28,000 jumps put 3,714 (0 V) and 1,026 (−0.5 V) counts on the next read |
| `nudge_run1.log` | Nudges judged with the hand off: 11 "IN" events at random Z, FAR within one or two sweeps |
| `touchtest_run1.log` | Touching the screw head without turning, bias flipping: no effect at all |
| `fastwood_run2_chunk20.log`, `fastwood_1789820034.csv` | 20-step chunks: found at Z 51,000 after 200 steps |
| `ztest_run2.log`, `ztest_1789820073.csv` | 30 s later: in contact even at Z 0 (STUCK) |
| `live_backoff_z0_run2.log` | Hand-set 4: clear 12:50:00 |
| `apz_run1.log`, `apz_approach_1789822231.csv`, `apz_ztest_1789822231.csv` | Chunks then the Z test with no gap: found at Z 17,000, then **the gold followed the retracting tip in**; the snap 28 → 16,777 in 4 counts is in the Z-test CSV at t 9.68 s. **Its Z-test figures are excluded from the results** |
| `release_watch_run1.log` | Released, then watched with the motor still: 19,000 → 42,000 → FAR → back at ~6,000-8,000. **No CSV** — stopped to start the Z test |
| **`ztest_run3.log`, `ztest_1789822585.csv`** | **THE Z TEST: 30 cycles at −0.5 V.** cpd in 1,650, out 3,442, hysteresis 1,162 (medians), 3 watchdog events (14 snap-phase rows), drift −74 counts/s |
| **`bias_series_run1.log`, `bias_m01V_1789822770.csv`, `bias_p05V_1789822770.csv`, `bias_p01V_1789822770.csv`, `bias_m05V_1789822770.csv`** | **The Z test at −0.1, +0.5, +0.1 and −0.5 V, 20 cycles each.** Re-analyse any Z-test CSV with `py scripts/ztest.py --analyse <file>` |
| `tuned_scans_run1.log`, `tuned_s3k_scan0-2.csv`, `tuned_s3k_xheld0-2.csv` | Scans with the loop constant set to 1,800: all six aborted — two at the top clamp, four at the bottom |
| `where_run1.log`, `where_run2.log` | Contact at Z 0, rising, 13:07-13:09 |
| `release_watch_run2.log`, `release_watch_1789823258.csv` | +1,200 retract steps in 20-step chunks: still railed (the CSV has no watch rows: the release never cleared) |
| `passive_z0_run1.log` | Z 0, nothing moving, railed until hand-set 5. **No CSV** — stopped for the hand-set |
| `live_backoff_z0_run3.log` | Hand-set 5: clear 13:12:01 |
| `swing_log_run1.log` | Full sweeps every 5 s with the motor still: FAR on every sweep for 11.8 minutes. **No CSV** — stopped for the shutdown |
| `storage_backoff_watch.log` | The watcher started for the storage back-off; it lost the port when the USB came out (a `SerialException`, expected). **The last record of the electrical state** |

**Four CSVs were lost the same way** (`creep_watch`, `release_watch` run 1, `passive_z0`, `swing_log`): the
scripts wrote their CSV only in `finally`, and stopping the task kills the process before that runs. **Write
rows as they are taken.** The `.log` files carry what was printed. `scripts/final.py` (the tip-clear baseline
and park for power-down) **was not run**: Jacob powered down first.

The Z-test CSV columns are `t, cycle, phase, z, adc` — phases `start`, `find`, `pre`, `in`, `out`, `out2`,
`snap`, `lost`. `cycle 0` is the find. **`snaps` in the analysis counts snap-phase ROWS, not events**: one
watchdog event writes one row per back-off step.
