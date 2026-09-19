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
| `wander2_run2.csv/.log` | The same, fifteen minutes, nothing else moving |
| `claude_running_notes.md` | Claude's timeline written during the session, including console output not saved elsewhere |
| `scripts/` | **Scratch scripts, kept as provenance, not tools.** Hardcoded to this laptop. `live_touch_test.py`, `onset0_test.py` and `lift_test.py` are their simulated-junction tests |
