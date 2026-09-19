# 2026-09-19 bench data

Recorded by **`sessions/2026-09-19-bench.md`** — the evening of 2026-09-18 local, 00:54-02:25 UTC,
on Jacob's laptop (COM3). Times are UTC. `ADCR` averaged reads throughout; 320.5 counts per nA;
sample −0.5 V is `BIAS 38229`, +0.5 V is `27307`.

> **This file replaces a placeholder written before the run** ("Empty until the run happens"),
> which listed `still.csv`, `stamp.csv` and a console paste. Those two CSVs are here as planned;
> the tool's printed output is in the session log §3.3 rather than a separate `console.md`.

## The planned noise run (tip clear)

| File | What |
|---|---|
| `still.csv` | `stm_noise_spectrum.py 10`, room still, tip clear. `ADCR` sd 42 |
| `stamp.csv` | the same while someone stamped ~2 m away. sd 42, no difference. **With the tip clear this tests electrical pickup only** |

## Everything after, in order

| File | What |
|---|---|
| `live_touch.log` | The laptop nano-amp beeper during the hand-set. Contact at 01:19:49, 4082 counts |
| `onset0_run1.csv/.log` | Piezo-only onset search: no current anywhere after the hand was released |
| `approach1_zero_bias.log` | **Approach at 0 V bias — see the session log §4.** Contact at the first point after 88 steps |
| `here_run1.csv/.log` | **The steady junction: 10 s at Z 0 (3.3 nA ± 0.3)**, the bias flip, the I-V, Z 0-3000 |
| `lift_run1.csv/.log`, `backoff2_0919.log` | Retract steps pushing the gold in, then 80 steps not clearing it |
| `zdir_run1.csv/.log` | Z sweeps at −0.14 V; ended with Z parked in contact (the session log §4) |
| `approach2_unknown_zero_bias.log` | Direction-finding approach, **also at 0 V bias**. Contact at midscale after 166 steps |
| `approach3_unknown.log` | Direction-finding at −0.5 V: "LOW", from a baseline already at 6087 |
| `approach4_unknown_tool_bias.log` | Direction-finding with the tool setting the bias: "HIGH" — **invalid**, the hit was midscale itself |
| `zdir2_run1.csv/.log` | Four sweeps 50000 → 0 → 50000: nothing |
| `wander_run1.log` | Sweeps from 50000: current at 50000 itself on 88 of 92. Stopped; no CSV |
| `lockin_run1.csv/.log` | Survey and the Z-toggle lock-in at Z 22000 |
| `touchrec_run1.csv/.log` | Fixed Z 2000: pinned for 5 s, watchdog fired |
| `slowscan_run1.csv/.log` | Three slow sweeps 50000 → 0 → 50000: nothing over 100 counts |
| `wander2_run1.log` | A sweep every 15 s, four minutes. Stopped by hand; **no CSV was written**, the 2-minute summaries are the record |
| `wander2_run2.log` | The same, nothing else moving; the gold came back into hard contact after ~10 minutes. Stopped by hand, so **no CSV** |
| `claude_running_notes.md` | Claude's timeline written during the session, including console output not saved elsewhere |
| `scripts/` | **Scratch scripts, kept as provenance, not tools.** Hardcoded to this laptop. `live_touch_test.py`, `onset0_test.py` and `lift_test.py` are their simulated-junction tests |

## Second half (02:10-03:55): hand-sets, the new tip, direction, scans

| File | What |
|---|---|
| `creeptrack_run1.log` | Motor still, both halves of Z swept every 5 s, +100 retract at each touch. Touches in both halves within seconds; stopped as a runaway |
| `live_touch2_run1.log` | Beeper hand-set, 02:21-02:23: the smooth rise 104 → 262 → 566 → 1314 counts, clear after the back-off |
| `live_touch2_run2.log` | Beeper hand-set, 02:42-02:44 ("the tiniest hair") |
| `cas2.log` (= `catch_and_scan_run2.log`) | The gold arrived 02:50:21 by creep; ten ±500 lock-ins undecided — the BENT tip |
| `bigswing_run1.csv` | Z ±2000/±8000/±20000 and X ±5000/±15000 toggles at 02:51; the junction faded during it |
| `cas3.log`-`cas7.log` | Catch-and-scan runs waiting after the new-tip hand-sets; no touch (runs 5-6 stopped for re-sets) |
| `live_touch4.log`, `live_touch5.log` | New-tip beeper hand-sets, 03:06 and 03:21, three hair back-offs each |
| `approach_newtip.log` | 1-step motor approach, 78 steps, nothing (stopped) |
| `live_backoff1.log`, `live_backoff2.log` | **The live back-off**, 03:39 and 03:41: ticks while touching, clear on silence |
| `approach_big.log`, `cas8.log`, `cas8_chmap_*.csv` | 5-step motor approach: hard contact at midscale after 60 steps; the constant-height maps and I-V taken there are **saturated** |
| `cas9.log`, `cas9_scan0-3.csv`, `cas9_xheld0-3.csv` | **Direction settled (HIGH, 4.2σ) and 4 feedback scans + 4 X-held controls.** No image |
| `ycontrol_run1.csv/.log` | **Three-Y control, ±3000 Y**: the same shape at every place |
| `ycontrol_xheld_run1.csv/.log` | The same with X held: floor 9-19 counts |
| `ycontrol_run2_ysep12000.csv`, `ycontrol_run2.log` | ±12000 Y: +0.374 ± 0.097 |
| `ycontrol_run3_ysep12000_xheld.csv`, `ycontrol_run3.log` | ±12000 Y with X held |
| `ycontrol_run4_ysep12000_repeat.csv`, `ycontrol_run4.log` | ±12000 Y repeated: +0.056 ± 0.094 — **run 2 did not reproduce** |
| `approach_known1.log` | `--z-retracted low` approach: tunnelling at Z 45200 after 0 steps |
| `img_scan_0-2.csv`, `img_xheld_0-1.csv` | Wide 2D constant-current images and X-held controls. Trace/retrace −0.75 to −0.94 |

The y-control CSVs are written by `Code/pc/stm_y_control.py` and re-analyse with
`py Code/pc/stm_y_control.py --analyse <file>` — **its "287-419 count wobble" line is 2026-09-17's
floor, not tonight's.** The feedback-scan CSVs re-analyse with `scripts/analyze_scans.py <prefix>`.
