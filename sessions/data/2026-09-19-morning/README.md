# 2026-09-19 morning bench data

Recorded by **`sessions/2026-09-19-morning.md`** — 2026-09-19, about 11:15-13:40 UTC, on Jacob's laptop
(COM3). Times are UTC. `ADCR` averaged reads throughout; 320.5 counts per nA; sample −0.5 V is
`BIAS 38229`, +0.5 V `27307`, −0.1 V `33860`, +0.1 V `31676`. **For this tip (fitted ~03:00 UTC
2026-09-19) HIGH Z extends toward the sample; Z 0 is fully retracted. NEGATIVE `MTMV` approaches.**

**Scripts are in `scripts/`: scratch kept as provenance, hardcoded to this laptop, each with a
`--test` self-test on simulated junctions.** `CSV` files carry the raw points; `.log` files the console.

| File | What |
|---|---|
| `baseline_run1.log` | Power-up: `GSTS`, `ADCR` at 0/−0.5/+0.5/0 V with Z 0, then a gentle walk to midscale. Tip clear |
| `live_backoff_run1.log` | Hand-set 1, the 2026-09-19 live back-off at Z midscale: contact 11:24:40, clear 11:24:55 |
| `creep_watch_run1.log` | 8 minutes at Z midscale, nothing moving: no current. **Its CSV was lost** — the process was stopped before it wrote |
| `ztest_run1.log`, `ztest_1789817796.csv` | First Z test: nothing in Z 32768-62000 |
| `approach_run1.log` | `Code/pc/stm_approach.py`, single steps: 111 toward the sample, nothing (stopped by hand for hand-set 2) |
| `touch_and_hold_run1.log` | Hand-set 2 without a hand back-off: contact 11:44:36, railed at Z 0 |
| `backoff_motor_run1.log`, `_run2.log` | +80 and +300 single retract steps: still railed |
| `live_backoff_z0_run1.log` | Hand-set 3, the back-off with Z held at 0: clear 11:53:35 |
| `stairs_run1.log`, `stairs_*.csv` | Two full finds after hand-set 3: nothing in Z 0-62000 |
| `fastwood_run1.log`, `fastwood_*.csv` | 650 single approach steps with a coarse sweep: nothing |
| `zjump_run1.log` | **Read check and Z-jump transient**: a 0→28,000 jump put 3,714 (0 V) and 1,026 (−0.5 V) counts on the next read |
| `nudge_run1.log` | Nudges judged with the hand off: 11 one-sweep "IN" blips at random Z, FAR on release |
| `touchtest_run1.log` | Touching the screw head without turning, bias flipping: no effect at all |
| `fastwood_run2_chunk20.log` | 20-step chunks: found at Z 51,000 after 200 steps |
| `ztest_run2.log`, `ztest_1789820073.csv` | 30 s later: in contact even at Z 0 (STUCK) |
| `live_backoff_z0_run2.log` | Hand-set 4: clear 12:50:00 |
| `apz_run1.log`, `apz_approach_*.csv`, `apz_ztest_*.csv` | Chunks then the Z test with no gap: found at Z 17,000, then **the gold rushed in ~15,000 counts/s**; the snap 28 → 16,777 in 4 counts is in the Z-test CSV at t 9.68 s |
| `release_watch_run1.log` | Released, then watched with nothing moving: 19,000 → 42,000 → FAR → back at ~6,000-8,000. **No CSV** — stopped to start the Z test, before it wrote |
| **`ztest_run3.log`, `ztest_1789822585.csv`** | **THE Z TEST: 30 cycles at −0.5 V.** cpd in 1,650, out 3,442, hysteresis 1,162, 14 snaps, drift −74 counts/s |
| **`bias_series_run1.log`, `bias_m01V_*.csv`, `bias_p05V_*.csv`, `bias_p01V_*.csv`, `bias_m05V_*.csv`** | **The Z test at −0.1, +0.5, +0.1 and −0.5 V, 20 cycles each.** Re-analyse any of them with `py scripts/ztest.py --analyse <file>` |
| `tuned_scans_run1.log`, `tuned_s3k_*.csv` | Scans with the loop constant set to 1,800: clamped top, then bottom — the gold swung |
| `where_run1.log`, `where_run2.log` | Contact at Z 0, rising, 13:07-13:09 |
| `release_watch_run2.log`, `release_watch_1789823258.csv` | +1,200 retract steps in 20-step chunks: still railed (the CSV is empty of watch rows: the release never cleared) |
| `passive_z0_run1.log` | Z 0, nothing moving, railed until hand-set 5. **No CSV** — stopped for the hand-set |

**Three CSVs were lost the same way** (`creep_watch`, `release_watch` run 1, `passive_z0`): the scripts
wrote their CSV only in `finally`, and stopping the task kills the process before that runs. **Write rows
as they are taken.** The `.log` files carry what was printed.
| `live_backoff_z0_run3.log` | Hand-set 5: clear 13:12:01 |
| `swing_log_run1.log`, `swing_log_*.csv` | 15 minutes of full sweeps every 5 s, nothing moving |

The `ztest` CSV columns are `t, cycle, phase, z, adc` — phases `start`, `find`, `pre`, `in`, `out`, `out2`,
`snap`, `lost`. `cycle 0` is the find.
