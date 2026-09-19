# Handoff — Subagent 1, data inventory and comprehensive analysis

**Written 2026-09-19.** Everything below is in `deliverables/2026-09-19-pause/analysis/`.
Nothing outside that directory was modified. `python3 Code/pc/check_facts.py` exits 0.

---

## 1. Files reviewed

**Read in full:** `CLAUDE.md`; `deliverables/2026-09-19-pause/BRIEF.md`;
`deliverables/2026-09-19-pause/SOURCE_INVENTORY.md`; all four
`sessions/data/*/README.md`; `docs/FACTS.md` (all 236 lines, including the RETIRED table);
`STATUS.md` (top 180 lines, then searched); `sessions/2026-09-19-morning.md` (all);
`sessions/2026-09-19-bench.md` (§1–4); `sessions/2026-09-18-bench.md` (§1–3.8);
`sessions/2026-09-17-bench.md` (§3.19–3.27 and the code-changes section);
`sessions/2026-09-16-bench.md` §3.4 (the calibration table).

**Data:** all **163** raw files in the four `sessions/data/` directories were opened and
characterised mechanically; **~70** were read in detail and computed on.

**Scripts:** `sessions/data/*/scripts/` (82 files) — `ztest.py`, `chmap.py`, `scan2.py`,
`analyze_scans.py`, `live_backoff.py`, `live_backoff_z0.py`, `fastwood.py`, `zcal3.py`,
`track.py`, `ft_run.py`, `ft_long.py`, `lash.py`, `creeptrack.py`, `slowscan.py`,
`touchrec.py`, `wander.py`, `zdir2.py`, `run_img_wide.py`, `run_ycontrol_wide.py` read in
detail for provenance and settings; the rest surveyed.

**Tools:** `Code/pc/stm_feedback_scan.py`, `Code/pc/stm_noise_spectrum.py`,
`Code/pc/stm_approach.py` (clamps, bias handling, the fixed bias bug).

---

## 2. Work completed

- **Inventoried all 163 raw data files** (plus 2 transcribed console notes), with what
  produced each, its format, row count, the bias and Z parking it was taken under, the
  run settings, and the session-log passage that describes it.
- **Re-derived the 100 MΩ dummy-junction calibration** from the 53 raw readings.
- **Re-derived all five Z-test runs** with an independent implementation.
- **Quantified gap drift** from three independent records and tested for periodicity.
- **Re-derived the still/stamp noise comparison** from the raw samples and assembled the
  cross-session noise table with each figure's tip and junction state attached.
- **Re-derived the I-V, the bias flip and the Z sweep** with the railed points excluded.
- **Re-derived every scan-versus-control statistic** in the repository, including the
  first-line-transient check and the three-Y control.
- **Re-derived the motor and approach statistics**, against the still-motor control.
- **Produced 17 publication-quality figures** at 200 dpi.

---

## 3. Outputs, and the exact command that reproduces each

All commands run **from the repository root**.

| Output | Command |
|---|---|
| `analysis/DATA_INVENTORY.md`, `analysis/data_inventory.csv` | `python3 deliverables/2026-09-19-pause/analysis/code/build_inventory.py` |
| `plots/fig01_calibration.png`, `fig02_calibration_residuals.png` | `python3 deliverables/2026-09-19-pause/analysis/code/calibration.py` |
| `plots/fig03_ztest_curves.png`, `fig04_ztest_hysteresis.png`, `fig05_ztest_cpd_by_bias.png`, `fig06_ztest_drift.png` | `python3 deliverables/2026-09-19-pause/analysis/code/ztest_analysis.py` |
| `plots/fig07_gap_motion.png`, `fig08_junction_timeseries.png`, `fig09_junction_spectrum.png` | `python3 deliverables/2026-09-19-pause/analysis/code/gap_stability.py` |
| `plots/fig10_noise_spectra.png`, `fig11_noise_by_session.png` | `python3 deliverables/2026-09-19-pause/analysis/code/noise_analysis.py` |
| `plots/fig12_iv_curve.png`, `fig13_bias_flip.png` | `python3 deliverables/2026-09-19-pause/analysis/code/iv_barrier.py` |
| `plots/fig14_scan_vs_control.png`, `fig15_scan_examples.png`, `analysis/scan_stats.csv` | `python3 deliverables/2026-09-19-pause/analysis/code/scans_and_controls.py` |
| `plots/fig16_motor_steps.png`, `fig17_still_vs_stepping.png` | `python3 deliverables/2026-09-19-pause/analysis/code/approach_and_motor.py` |
| `analysis/FINDINGS.md`, `analysis/COMPARISON_TABLES.md` | written by hand from those outputs; every number in them is printed by the script named beside it |

Each script prints every number it computes **beside the published figure it is
checking**, so a reader can audit it without reading the code. Requirements: `python3`
with `numpy`, `scipy`, `matplotlib`. `scipy` is used for two optional significance tests
and each is skipped with a printed note if absent. No absolute path outside the
repository appears in any script; paths are derived from the file's own location.

---

## 4. Evidence behind each finding

| Finding | Evidence: file + rows | Number |
|---|---|---|
| Calibration reproduces | `sessions/2026-09-16-bench.md` §3.4 table, 53 readings in 8 steps | slope −3,205.0 ± 36.5 counts/V, R² 0.9934, intercept +58.1, residual sd 320.3; 0.14 s.e. from the −3,200 prediction |
| Z-test numbers reproduce | `ztest_1789822585.csv` (24,379 rows), `bias_m01V_…` (14,893), `bias_p05V_…` (15,559), `bias_p01V_…` (28,485), `bias_m05V_…` (11,825) | all 25 published figures match exactly |
| Not a tunnelling gap | same five files, 110 cycles | 808–4,639 counts per decade in, against 6–13 expected |
| Hysteresis in every run | same five files, 109 cycles with a value | medians +705 to +1,868; 99 of 109 cycles positive |
| Hysteresis does not shrink at ±0.1 V | ±0.1 V: `bias_m01V_…`, `bias_p01V_…` (2 runs, 40 cycles); ±0.5 V: 3 runs, 69 cycles | means 1,564 against 1,245; ratio 1.26 where V² predicts 0.04 |
| 1 of 110 onsets was a one-step snap | `ztest_1789822585.csv`, cycle 1 at t 9.28 s | Z 41,260 → 41,264, 10.4 → 9,116 counts |
| Gap moves by most of the Z range | `release_watch_run1.log`, 9 sweep lines | +23,000 counts in 3.1 s measured; ≥ 43,000 in 6.3 s and ≥ 56,000 over 111 s as bounds |
| A second record of the same size | `track_run1.csv`, 276 rows, 249 with an onset | mean 24,067, sd 7,563, range 7,250–44,250 in 90 s, motor still |
| Stamping changed nothing | `still.csv` 34,746 rows, `stamp.csv` 36,071 rows | sd 41.80 against 42.35; no band above the floor; control band at zero |
| The junction is real | `here_run1.csv`, `flip` rows, 4 × 256 readings | −0.5 V +1,156, +0.5 V −811, 0 V −1.4, −0.5 V +1,033 counts |
| Superlinear and asymmetric I-V | `here_run1.csv`, `iv` rows, 17 of 21 bias points kept | p = 1.98 ± 0.25 and 1.48 ± 0.15; 3.6× asymmetry at 0.8 V; 181 and 193 MΩ at ±0.1 V |
| Controls reproduce better than scans | `cas9_scan0-3.csv`, `cas9_xheld0-3.csv`, 11 lines × 21 pixels each | image-to-image +0.04 against +0.37 |
| The first-line trap | 12 CSVs in `2026-09-17-bench` | +0.70 → −0.08, +0.75 → +0.04, +0.62 → −0.29, +0.71 → −0.45, +0.38 → −0.26 |
| The three-Y statistic fires on a control | 5 y-control CSVs, 18 rows each | X-held run: +0.164 ± 0.082 with X never moving |
| The motor cannot park at a moderate current | `zcal3_run1.csv` 44 rows, `lash_run1.log` 177 medians, `2026-09-19-bench.md` §3.13 | 23 steps pinned then clear on the 24th; 650 single steps found nothing |
| Motor release rate | 8 episodes across 3 session logs | 3 of 8 cleared |

---

## 5. Two corrections owed to live documents — for the lead, not for me

1. **`docs/FACTS.md`, "Current against Z, going in — sample −0.5 V"** states the
   per-cycle counts-per-decade range across all runs as **233–22,990**. The true minimum
   is **208.3** (cycle 1 of the −0.5 V repeat run, `bias_m05V_1789822770.csv`). The
   maximum is right. Reproduce with
   `python3 deliverables/2026-09-19-pause/analysis/code/ztest_analysis.py`, section 6.
2. **`sessions/2026-09-19-morning.md` §3.11** reads *"10 of 109 cycles at +0.5 V were
   negative"*. 10 of 109 cycles **across all five runs** are negative; only **1** is at
   +0.5 V. Session logs are history and must not be rewritten — this is recorded so the
   sentence is not quoted as written.

Neither changes a conclusion.

---

## 6. Metadata gaps, and what closed them

**Not one data file is missing its bias or Z parking**, but for 38 of 165 the setting is
not where a reader would look:

| Where the bias had to be read from | Files |
|---|---|
| The session data README or session log | 127 |
| **The producing script's own source**, in that session's `scripts/` | 18 |
| **The session log's code-changes section**, not the scan record | 18 |
| **The data file's own printed banner** | 1 |
| **Not recorded anywhere** | 1 |

- **The 18 "code-changes" files are the 2026-09-17 scans.** Their bias appears nowhere
  beside them. `sessions/2026-09-17-bench.md` records that `stm_feedback_scan.py` *"read
  a bias argument, printed it in its banner, and then ignored it — it wrote `BIAS 38229`
  unconditionally… Every scan before that ran at −0.5 V whatever was typed"*, and the fix
  is commented at `Code/pc/stm_feedback_scan.py:206-211`. **Credit for finding it goes to
  the 2026-09-17 review team**, who are named in that log; I only looked it up.
- **The one genuine gap** is `sessions/data/2026-09-18-bench/approach3.log`.
  `stm_approach.py` did not set a bias at that date, so the sample sat at whatever the
  previous command left, and nothing records what that was. **UNKNOWN.**
- **`approach5_unknown.log` is the only data file no prose document mentions.** Its own
  printed banner gives bias 38229, Z parking 32768, motor step −1 up to 700, baseline 73
  counts, noise 170 RMS, threshold 1,500 — and it records contact **already present at
  midscale after 2 steps**, 32,767 counts.

---

## 7. Uncertainties and blockers

1. **The gap's motion is one episode.** `release_watch_run1.log` is nine sweeps, n = 1
   for the recession and n = 1 for the return, quantised to 1,000 Z counts by a
   default-argument bug. Do not quote it as a repeatable rate.
2. **Periodicity cannot be tested at the timescale that matters.** The fastest junction
   record is 10.3 s (lowest resolved frequency ≈ 0.1 Hz); the gap moves over tens of
   seconds to minutes. Nothing here can find or exclude a period. Four CSVs that would
   have helped were lost.
3. **The Z scale is inherited and unmeasured.** Every nanometre statement is conditional
   on 0.016 nm per count, from Berard's disc. **The hysteresis result does not depend on
   it; the counts-per-decade comparison does.**
4. **The tungsten-gold contact potential is unmeasured**, so §2.4 of `FINDINGS.md` cannot
   fully close the electrostatic hypothesis. `STATUS.md` says the same.
5. **The wide-image saturation figure cannot be checked** — no `.log` was kept for the
   `img_scan_*` / `img_xheld_*` runs.
6. **The 2026-09-18 noise excursion cannot be diagnosed** — no raw samples were kept.
7. **The 2026-09-17 diagnostics cannot be inspected** — no scripts kept for that session.
8. **Statistical caveat that applies throughout:** readings and cycles inside a run are
   repeated measurements, not independent samples. Every standard error printed by these
   scripts assumes independence and is therefore optimistic. The n for *independent*
   observations is stated beside every claim in `FINDINGS.md`.

**Alignment with subagent 2, whose results landed while this was being written.** Three of their
findings are now carried in this analysis, with credit, because they change how three of my files
should be read:

- **`line_repeated_wide.csv`'s 636-count profile is CLOSED** — the loop recovering from a
  30,000-count X flyback on a tilted surface; 3,144 counts predicted, +0.65 → +0.05 on dropping two
  pixels of twenty-one. `FINDINGS.md` §6.5, `DATA_INVENTORY.md` and `COMPARISON_TABLES.md` §10
  item 13 all say so now.
- **`scan_wide_25nm_1/2.csv` ARE the ±15,000 three-place test** that
  `sessions/2026-09-17-bench.md` §3.25 records as never run, permutation p = 0.24. Their inventory
  entries now say so; this is the fifth `CLAUDE.md` §3b case and the reason it happened is that
  those two files were missing from that directory's `README.md` table.
- **The three-Y "3.9σ" is overstated.** Subagent 2's 20,000-fold permutation gives run 2
  p = 0.0036 and **an X-held control p = 0.020 on the same statistic**. That is the empirical
  false-positive rate of this measurement, and it is a much better number than my "two of five
  tests fired, one of them on a control". `FINDINGS.md` §6.4 now carries it.

**For agents 5 and 6 specifically:**

- **The `cas9` set is the strongest evidence for "no image"**: +0.04 against +0.37, four
  scans each with its own interleaved control, one tip, one night. Use that, not the
  wide images.
- **The one result that points the other way** (wide images, scans +0.71 against controls
  +0.56) is examined in `FINDINGS.md` §6.3 and `COMPARISON_TABLES.md` §5. It rests on
  21 and 42 pixels against the control's 231, on the single line that is guaranteed to
  agree, and it comes with trace/retrace of −0.75 to −0.94. **It does not survive, but it
  should be shown rather than omitted.**
- **The "no image" conclusion is neither weakened nor strengthened by this work.**

---

## 8. What is left undone

- No analysis of `Images/` — that is agent 3's.
- `console_outputs.md` and `claude_running_notes.md` are inventoried as prose but their
  numbers were not extracted into a table; the session logs already carry the ones that
  matter.
- The eight 2026-09-18 `console_outputs.md` static scans and Z probes were not
  re-analysed (they are transcriptions, not machine-readable).
- `ft_run1.json` and `ft_long1.json` (1,900 and 30 entries) were characterised but their
  wobble spectra were not recomputed, because the data README marks every statistic from
  them as provisional — they locate snap-in events, not tunnelling onsets.
- No attempt was made to re-analyse the 2026-09-17 `line_three_y_positions.csv` as a
  discriminating control: the 2026-09-17 log's own correction records that it was run at
  ±8,000 X against the wide scans' ±15,000 and had no power to discriminate.
