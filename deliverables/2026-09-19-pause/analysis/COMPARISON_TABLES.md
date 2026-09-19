# Cross-session comparison tables

**Written 2026-09-19 for the pause-point deliverables, from the raw files in
`sessions/data/`.** Every number here is either re-derived by a script in
[`code/`](code/) — those are marked **RE-DERIVED** and the script is named — or quoted from the
session log that measured it, in which case the log is named. Nothing is inferred.

The point of this document is the thing that is easiest to get wrong in this project: **four
bench sessions look like four repeats of one experiment and they are not.** The tip changed
twice, the sample changed, the tip holder was rebuilt, the electronics had one unexplained noisy
night, the feedback loop was retuned by a factor of eighteen, and two of the analysis tools
carried bugs that changed what the files contain. This document lists every one of those
differences so that nobody pools two rows that must not be pooled.

---

## 1. What changed between the sessions

| | `2026-09-17-bench` | `2026-09-18-bench` | `2026-09-19-bench` | `2026-09-19-morning` |
|---|---|---|---|---|
| **When (UTC)** | evening 2026-09-17 | 01:00–02:40, 2026-09-18 | 00:54–04:00, 2026-09-19 | 11:15–13:30, 2026-09-19 |
| **Tip** | blunt placeholder | **same** placeholder | **TWO**: the same one until ~03:00, then a new "very blunt" one | the new blunt one, unchanged |
| **Was the tip bent?** | not known at the time | not known at the time | **Jacob said the first tip was BENT, ~02:57** | the replacement, never assessed |
| **Sample** | crumpled gold leaf; `SAID` at the end the junction was probably **on the copper beside it** | **all-gold plate**, continuity to bias confirmed | the **2026-09-19 copper-framed leaf-on-paper stack** | same as the night before |
| **Tip holder** | original | **REBUILT** — left the tip ~2.2 mm further back | as rebuilt | as rebuilt |
| **ADC scatter, tip clear** | 46 counts | **341–350 counts** | 40–42, then 34–36 after the tip change | 33.5–37.1 |
| **Feedback loop constant** | 250 counts/decade | loop not used for imaging | **100** counts/decade | **1,800** counts/decade |
| **Z clamps** | 12,000–48,000 | — | 12,000–48,000, raised to **60,000** at the top for the wide runs | 12,000–48,000 |
| **Z direction in force** | HIGH toward the sample | HIGH toward (inherited) | **UNRESOLVED** for the bent tip; settled **HIGH toward** at 03:48 for the new one | HIGH toward; Z 0 fully retracted |
| **Scripts kept** | **none** | 25 | 37 | 20 |
| **Known tool defect affecting the data** | `stm_feedback_scan.py` ignored its bias argument and wrote `BIAS 38229` regardless; the loop steered on a **single conversion** (188 counts of noise) until 21:35 | `stm_approach.py` set no bias | **two approaches ran at 0 V bias**; `zdir.py` had no watchdog | the approach sweep ran at **1,000-count Z steps, not 250** |

**Sources.** Each session's own `sessions/data/<session>/README.md` header and the session log it
names; the tip and sample statements are `SAID` by Jacob and are marked as such in those logs.

---

## 2. The five comparisons that are SAFE, and the five that are NOT

| Comparison | Safe? | Why |
|---|---|---|
| ADC scatter with the tip clear, 2026-09-17 (46) against 2026-09-18 (341–350) against 2026-09-19 (40–42) | **SAFE** | same measurement, same command (`ADCR`), same condition (tip clear). The 2026-09-18 excursion is about **eight times** the other two and it went away |
| `still.csv` against `stamp.csv` | **SAFE — the best controlled A/B in the record** | 36 seconds apart, one tip, one night, one tool, one setting. Nothing else in the noise record is this clean |
| The five Z-test runs of 2026-09-19 morning against each other | **SAFE** | one tip, one sample, one script, back to back over nine minutes |
| The four `cas9` scans against their four X-held controls | **SAFE, but only over COMPLETE images** | interleaved, same tip, same loop tuning, same night — **and `cas9_xheld2.csv` is a single line, so any pair involving it is 21 pixels against 231.** See §5 |
| Motor-retract outcomes across sessions | **SAFE as a count, not as a rate** | eight independent episodes; three cleared. The count is comparable, the step size is not |
| ADC scatter with the tip clear against the 46 counts of the 2026-09-19 morning touch test | **NOT SAFE** | the touch test had a **junction at Z 20,000**. A junction is a current source; the tip-clear figure is the instrument's own floor |
| 2026-09-17's height-channel wobble (287–419 counts) against 2026-09-19's (9–19 counts) | **NOT SAFE as a like-for-like improvement** | different tip, different sample, different loop constant, and the 9–19 figure is an **X-held** control while the 287–419 is a loop holding at one point. The tools still print the 2026-09-17 figure |
| 2026-09-17's 250 counts per decade against 2026-09-19 morning's ~1,800 | **NOT SAFE** | different tip, different sample, and **the 2026-09-19 bench junction was never Z-tested**, so the middle term is missing |
| Any 2026-09-19 bench result before 03:00 against anything after | **NOT SAFE** | different tip, and the first was bent |
| The trace/retrace figures of the wide images against those of the narrow scans | **NOT SAFE** | the wide runs had their top Z clamp raised to 60,000 and two of the three aborted after one and two lines |

---

## 3. Noise, session by session

All figures are the standard deviation of `ADCR`, the firmware's five-sample averaged read
(`docs/FACTS.md`, "ADC averaging"). **320.5 counts is 1 nA** (`docs/FACTS.md`, "Counts per nA").

| When | sd, counts | sd, nA | Tip | Junction? | Source |
|---|---|---|---|---|---|
| 2026-09-17, room empty | 46 | 0.14 | blunt placeholder | clear | `sessions/2026-09-17-bench.md` §3.25 |
| 2026-09-18 01:47, `ADCR` only | 341 | 1.06 | same, holder rebuilt | clear | `sessions/2026-09-18-bench.md` §3.5 |
| 2026-09-18 01:47–01:59 | 343–350 | 1.07–1.09 | same | clear | same, and **no decay over 12 minutes** |
| 2026-09-19 bench 01:01 | 40–41 | 0.12–0.13 | the bent tip | clear | `sessions/2026-09-19-bench.md` §3.2 |
| 2026-09-19 bench 01:08 `still.csv` | **41.8 RE-DERIVED** (log says 42) | 0.130 | the bent tip | clear | `code/noise_analysis.py` |
| 2026-09-19 bench 01:08 `stamp.csv` | **42.3 RE-DERIVED** (log says 42) | 0.132 | the bent tip | clear | `code/noise_analysis.py` |
| 2026-09-19 bench 03:05, new tip | 34–36 | 0.11 | the very blunt tip | clear | `sessions/2026-09-19-bench.md` §3.13 |
| 2026-09-19 morning 11:22 | 33.5–37.1 | 0.10–0.12 | the very blunt tip | clear | `sessions/2026-09-19-morning.md` §3.1 |
| 2026-09-19 morning 12:11 touch test | 46.3–46.5 | 0.144 | the very blunt tip | **junction at Z 20,000** | `sessions/2026-09-19-morning.md` §3.6 |

**The 2026-09-18 night is the outlier and its cause was never found.** It was ruled out as the
operator (identical at 76 cm and with the room empty) and it showed no decay over 16 minutes.
The candidates the log leaves open are the rebuilt holder and the new whole-plate gold, which puts
a much larger electrode opposite the input node. Neither was tested.

### The separate quantity that is easily confused with these

| When | Height-channel wobble | Conditions | Source |
|---|---|---|---|
| 2026-09-17 | **287–419 counts RMS** | the loop holding a fixed current at ONE fixed point, no scanning, at every setpoint from 1.6 to 47 nA | `sessions/2026-09-17-bench.md` §3.25 |
| 2026-09-19 bench | **9–19 counts RMS** | the three-Y control **with X held** | `sessions/2026-09-19-bench.md` §3.15 |

These are **Z DAC counts the feedback loop needed**, not ADC counts. They are not the same
measurement as the rows above and they are not the same measurement as each other.
`Code/pc/stm_y_control.py` still prints the 2026-09-17 figure as its comparison, and
`sessions/data/2026-09-19-bench/README.md` says so explicitly.

---

## 4. Scans and their controls, every group in the repository

**RE-DERIVED by `code/scans_and_controls.py`.** "Image to image" is the correlation of one
detrended forward image with the next; "trace/retrace" is forward against backward, line by line.
**Every image-to-image figure below is over COMPLETE IMAGES ONLY** — see §5 for why, and for the
four groups where the published figure was not.

| Group | Session | Scans | Controls | Scan image-to-image | Control image-to-image | Verdict |
|---|---|---|---|---|---|---|
| 4 fast narrow images | 09-17 | 4 | — | +0.70 → **−0.08 with the first two lines dropped** | — | the agreement was the loop settling |
| 2 slow narrow images | 09-17 | 2 | — | +0.75 → **+0.04 with two lines dropped** | — | the same trap, and the log caught it at the time |
| 250 corrections per pixel | 09-17 | 2 | — | +0.62 → **−0.29** | — | same |
| 15 corrections, with an X-HELD control | 09-17 | 2 | 1 | +0.71 → **−0.45** | — | the control's corrugation (87 counts) sits between the two scans' (133 and 57) |
| wide ±4,000 X | 09-17 | 2 | — | +0.38 → **−0.26** | — | same |
| wide ±15,000 X | 09-17 | 2 | — | +0.31 → +0.44 | — | the one 2026-09-17 group that survives the line drop; see §5 |
| `cas8` constant-height maps | 09-19 bench | 6 | 3 | — | — | **every pixel at the ADC rail. No information** |
| `cas9` feedback scans | 09-19 bench | 4 | 4 | **+0.039** (3 pairs) | **+0.068** (2 pairs) | **neither reproduces; the two are indistinguishable** — see §5 |
| wide images | 09-19 bench | 3 | 2 | **no complete pair** | +0.56 (1 pair) | two of three scans aborted after 1 and 2 lines — see §5 |
| tuned scans, loop 1,800 | 09-19 morning | 3 | 3 | **no complete pair** | **no complete pair** | all six aborted at a clamp |

### Corrugation, the same groups

| Group | Scans (counts RMS) | Controls (counts RMS) |
|---|---|---|
| `cas9` | 82, 126, 147, 101 | 82, 41, **237 (one aborted line)**, 59 |
| 09-17 diagnostic | 133, 57 | 87 |
| wide images, 09-19 | 382, 438, 416 | 181, 133 |
| tuned scans | 1,885, 1,183, 1,310 | 1,373, 921, 970 |

---

## 5. The truncation defect — a class in four groups, and the one number it changes

`sessions/data/2026-09-19-bench/scripts/analyze_scans.py` lines 50–51 **truncate each image pair to
the shorter file with no shape check.** Where one file of a pair aborted, the resulting
"image-to-image correlation" is computed over one or two **lines** while a complete pair is computed
over eleven. The short one is dominated by the first line, which is the line guaranteed to agree
because it carries the loop's settling transient (§4's drop-line column).

**Four groups are affected, on both the scan side and the control side.**

| Group | Side | As published (truncating) | Complete images only | Why it truncated |
|---|---|---|---|---|
| `cas9` | controls | +0.20, +0.21, +0.70 → **+0.37** | +0.20, −0.06 → **+0.068** | `cas9_xheld2.csv` is **one line** of eleven |
| wide images | scans | +0.86, +0.56 → **+0.71** | **no complete pair exists** | `img_scan_0` 1 line, `img_scan_1` 2 lines |
| tuned scans | scans | −0.75, +0.26 → **−0.25** | **no complete pair exists** | `tuned_s3k_scan0` 1 line of nine |
| tuned scans | controls | +0.22, −0.15 → **+0.03** | **no complete pair exists** | `tuned_s3k_xheld0` 2 lines of nine |

### The one published conclusion this changes

**"The controls reproduce better than the scans" is WITHDRAWN.** Like for like, complete images
only:

| | n pairs | Values | Mean |
|---|---|---|---|
| Real scans (X moving across the surface) | 3 | +0.09, +0.18, −0.15 | **+0.039** |
| X-held controls (tip never moved across it) | 2 | +0.20, −0.06 | **+0.068** |

Standard error of each correlation at 231 pixels: **0.066**, and that is optimistic — it treats the
21 pixels of a line as independent, which the Z ramp along a line makes false. **Difference −0.030
against 0.066: indistinguishable, and neither mean differs from zero.**

**The correct statement: neither the scans nor the controls reproduce, and the scans show no more
repeatable structure than a control in which the tip never moved across the surface.** The imaging
conclusion is unchanged and needs no rescuing — it rests on the real scans not reproducing.

**Found by the lead's independent review** (`LEAD_VERIFICATION.md` V4); `STATUS.md` is already
corrected.

### The wide images, which I previously called "the one group where the scans win"

**There is no pair of complete wide images to compare.** Only `img_scan_2` ran to the end. The
+0.71 came entirely from a single shared line. Two things stand against those scans independently
of any correlation:

- **Trace and retrace are anti-correlated in all three** (−0.94, −0.91, −0.75) and not in the
  controls (+0.14, +0.13). A surface gives a **positive** trace/retrace.
- **There is no `.log` file** for these runs, so the "14.5 % saturation" in the session log came
  from console output that was not saved and cannot be checked. `cas9.log` does carry the loop's
  own saturated and clamped counters.

---

## 6. The three-Y control, all five runs

**RE-DERIVED by `code/scans_and_controls.py`; every one of the five reproduces the published
figure to the third decimal.** The test asks whether one place on the sample looks more like
itself than like a place 3,000 or 12,000 Y counts away.

| Run | Y separation | X moving? | Within a place | Between places | Difference | Verdict |
|---|---|---|---|---|---|---|
| `ycontrol_run1` | ±3,000 | yes | +0.713 | +0.680 | **+0.032 ± 0.035** | nothing |
| `ycontrol_xheld_run1` | ±3,000 | **NO** | +0.278 | +0.114 | **+0.164 ± 0.082** | "positive" — **in a run with no lateral motion** |
| `ycontrol_run2_ysep12000` | ±12,000 | yes | +0.239 | −0.135 | **+0.374 ± 0.096** | "positive" |
| `ycontrol_run3_ysep12000_xheld` | ±12,000 | **NO** | +0.116 | +0.046 | +0.070 ± 0.083 | nothing |
| `ycontrol_run4_ysep12000_repeat` | ±12,000 | yes | +0.149 | +0.093 | **+0.056 ± 0.093** | **run 2 did not reproduce** |

**Five tests, two positives, and one of the two is an X-HELD CONTROL in which X never moved and
there is therefore no surface to see.** A statistic that fires on a run with no lateral motion is
biased in this data, and the same bias is available to the run that fired with X moving. The
2026-09-19 bench log reaches the same conclusion from the split-half statistic. Run 2's +0.374 and
its repeat run 4's +0.056 are the same measurement, taken a few minutes apart.

**How many minutes is NOT recorded, and two guesses have already been wrong.** Neither `ycontrol`
log carries a timestamp. What the record bounds: `sessions/2026-09-19-bench.md` is chronological,
§3.14 is timestamped **03:48**, §3.16 is timestamped **03:53**, and §3.15 — **all five** runs — sits
between them. **All five fit inside about five minutes.** An earlier version of this file said
"nine minutes" and subagent 2 said "half an hour"; both were guesses and both were too long. Found
by the lead's independent review.

### The onset Z of each run — a measurement that was in the logs and unused

The first line of every `ycontrol_run*.log` gives the Z at which the loop found the surface before
that run started. It is the only series of gap positions taken inside one short window.

| Run | Y separation | X moving? | **Onset Z** |
|---|---|---|---|
| `ycontrol_run1` | ±3,000 | yes | 44,200 |
| `ycontrol_xheld_run1` | ±3,000 | no | 47,000 |
| `ycontrol_run2` | ±12,000 | yes | **48,600** |
| `ycontrol_run3` | ±12,000 | no | 52,000 |
| `ycontrol_run4` (repeat of run 2) | ±12,000 | yes | **50,800** |

**Across all five the onset moved 7,800 counts. Between run 2 and run 4 it moved +2,200** — **3.4 %**
of the 65,536-count Z range, **4.6 %** of the 12,000–60,000 window these runs used.

**This weakens the "the surface moved out from under it" explanation for run 2 not reproducing**,
because across exactly that interval the gap moved a few per cent of the range, not most of it.

**It does not close it.** Onset Z measures the **gap**, not **lateral position**. A sideways drift
would carry the tip to a different patch of gold while barely changing the Z at which it finds the
surface. **Lateral drift has never been measured in this project**, and nothing in `sessions/data/`
can measure it.

**Rate, bounded not measured:** 2,200 counts over at most the ~5 minutes holding all five runs, so
a mean of **at least 7 counts/s** — the quiet end of the range in §9.

---

## 7. Z-test results, all five runs, side by side

**RE-DERIVED by `code/ztest_analysis.py` from the CSVs, with an independent implementation of the
definitions in `sessions/data/2026-09-19-morning/scripts/ztest.py`. All twenty-five published
numbers reproduce exactly.** One tip, one sample, nine minutes, so these five ARE comparable with
each other.

| Sample bias | Cycles | Counts/decade IN | Counts/decade OUT | Hysteresis (counts) | Watchdog events | Onset drift (counts/s) |
|---|---|---|---|---|---|---|
| −0.5 V (run 1) | 30 | 1,650 | 3,442 | **+1,162** | 3 | −74 |
| −0.1 V | 20 | 808 | 4,839 | **+1,653** | 0 | +29 |
| +0.5 V | 20 | 2,243 | 4,975 | **+1,868** | 1 | +22 |
| +0.1 V | 20 | 4,639 | 12,595 | **+1,474** | 0 | +7 |
| −0.5 V (repeat) | 20 | 1,967 | 3,834 | **+705** | 0 | +83 |

For comparison, tunnelling through vacuum on the inherited — and **unmeasured** — Z scale would be
**6–13 counts per decade** (`docs/FACTS.md`, "Tunnelling for comparison"). The hysteresis result
does not depend on that scale; the counts-per-decade comparison does.

**Two runs at the same bias, nine minutes apart:** 1,650 against 1,967 counts per decade going in
(agreement to ~20 %) but 1,162 against 705 counts of hysteresis (a factor of 1.6). The junction was
not the same junction twice.

---

## 8. What an onset costs, session by session — the coarse stage

| Session | Evidence | What one motor step did |
|---|---|---|
| 2026-09-17 | staircase after a reversal | "250 Z counts per motor step" — **declared SUSPECT the next night**: it ran inside its own 100–250 steps of measured slack |
| 2026-09-18 | `zcal3_run1`, three passes | 0–23 steps: nothing anywhere. Step 24: a clean onset at Z 28,500. Step 25: full scale at Z 9,250. Step 26: full scale at Z 0. Where a step changed anything it moved the onset **14,000–29,000 counts** |
| 2026-09-18 | `track_run1`, motor STILL | **RE-DERIVED**: 249 onsets in 276 searches over 90 s, mean 24,067, sd 7,563, range 7,250–44,250. **This is the control**: the gold moves over most of the Z range with nothing driving it |
| 2026-09-19 bench | one step at a time after a 5-step approach | **pinned for 23 retract steps, clear on the 24th, no moderate current in between** |
| 2026-09-19 morning | 650 single steps | nothing at all |
| 2026-09-19 morning | 20-step chunks | found twice, at 200 and 180 steps — **but 11 hand nudges came in between, so chunks against singles is confounded** |

**The conclusion that survives all of it, and does not depend on the unmeasured Z scale: the motor
cannot park the tip at a moderate current.** Between "nothing anywhere" and "metal contact" there
is no motor setting.

Motor retract against a hard contact, eight independent episodes across three sessions and two
tips: **three cleared, five did not.** The hand on the side screws released three of the four hard
contacts on 2026-09-19 morning; the fourth released on its own or after +20 steps.

---

## 9. Gap motion — three records that are not the same measurement

| Record | What it measures | Rate | n |
|---|---|---|---|
| `release_watch_run1.log`, 12:54–12:56 | where the contact is, motor and hands still, piezo sweeping only | **≥ 43,000 counts in 6.3 s**, then **≥ 56,000 counts back over 111 s** | **1 episode**, 9 sweeps |
| The five Z-test runs | onset Z per cycle, tip touching most of the time | **−74 to +83 counts/s** | **5 independent runs** |
| `track_run1.csv`, 2026-09-18 | onset Z with the motor still, different tip and sample | range **37,000 counts** in 90 s, sd 7,563 | **1 run**, 276 searches |
| The five `ycontrol_run*.log` onsets, 2026-09-19 bench | onset Z before each three-Y run, all inside one ~5-minute window | **7,800 counts across five runs**; +2,200 between run 2 and run 4, so **≥ 7 counts/s** as a mean | **5 points**, one window |

These differ by two orders of magnitude in rate and they are **not in conflict**: in a Z test the
tip is in or near contact for most of the run, and the log's reading is that the gold sticks to and
follows the tip. In the release-watch the tip had just been released and was clear. The `ycontrol`
series sits at the quiet end, with a junction held throughout — consistent with that reading.

**All four measure the GAP. None of them measures LATERAL position**, and lateral drift has never
been measured in this project. That gap in the record is what stops the `ycontrol` series from
closing the question in §6.

**No period is evident in any of them, and none of them can exclude one.** The fastest record of a
live junction (`here_run1.csv`, 10.3 s at about 3,400 readings per second) resolves down to about
0.1 Hz and shows nothing steady between its halves except mains; the position records are one
sweep per 3 s at best. The timescale on which the gap actually moves — tens of seconds to minutes —
is covered by nothing.

---

## 10. Every difference that makes a cross-session comparison unsafe, in one list

The brief flagged four of these. These are all of them found in the raw record. Nineteen in total.

1. **Two different tips within `2026-09-19-bench`**, changed at ~03:00 UTC, and the first was bent.
2. **A third tip** across the earlier sessions (the placeholder of 2026-09-17 and 2026-09-18).
3. **Three different samples**: crumpled leaf (2026-09-17, probably contacted on the copper),
   all-gold plate (2026-09-18), leaf-on-paper stack (2026-09-19).
4. **The tip holder was rebuilt** between 2026-09-17 and 2026-09-18, moving the tip ~2.2 mm back.
5. **The noise floor was eight times higher on 2026-09-18** than on either side, cause unknown.
6. **The feedback loop constant changed by a factor of 18**: 250 → 100 → 1,800 counts per decade.
7. **The upper Z clamp was raised from 48,000 to 60,000** for the 2026-09-19 wide runs only.
8. **The loop steered on a single conversion (188 counts of noise) until 21:35 on 2026-09-17** and
   on the averaged read after. Every earlier image ran on the noisy path.
9. **`stm_feedback_scan.py` ignored its bias argument until after 2026-09-17**, so every scan that
   night ran at −0.5 V whatever was typed.
10. **`stm_approach.py` set no bias until 2026-09-19**, and two 2026-09-19 approaches ran at 0 V,
    where only metal contact could trip the threshold.
11. **The 2026-09-19 morning approach sweeps ran in 1,000-count Z steps, not 250**, so every onset
    they record is a multiple of 1,000 and every rate derived from them is quantised.
12. **Two 2026-09-17 line files store the forward pass twice**, so no trace-versus-retrace figure
    from them means anything.
13. **`line_repeated_wide.csv` flies X back 30,000 counts between passes and the 2D wide images do
    not**, so their start-of-pass transients are not comparable: 3,144 Z counts predicted for the
    first, 37 and 78 observed for the second (subagent 2, carried into `STATUS.md`). This is what
    closes that file's 636-count profile.
14. **`Code/pc/stm_y_control.py` still prints 2026-09-17's 287–419 count floor** as its
    comparison, which belongs to a different tip and a different junction.
15. **No scripts were kept for 2026-09-17**, so the diagnostics that produced its files cannot be
    inspected.
16. **The `cas8` constant-height maps are entirely at the ADC rail** and carry no information.
17. **Four CSVs of 2026-09-19 morning were lost** (`creep_watch`, `release_watch` run 1,
    `passive_z0`, `swing_log`) because the scripts wrote them only on a clean exit. The headline
    gap-motion measurement survives only as a `.log`.
18. **`scripts/final.py` was never run**, so there is no tip-clear baseline at power-down.
19. **Six 2026-09-19 morning scripts have no self-test** and four of them produced committed data.

---

## 11. Where each of these numbers can be checked

| Table | Regenerate with |
|---|---|
| §3 noise | `python3 deliverables/2026-09-19-pause/analysis/code/noise_analysis.py` |
| §4, §5, §6 scans and controls | `python3 deliverables/2026-09-19-pause/analysis/code/scans_and_controls.py` |
| §7 Z tests | `python3 deliverables/2026-09-19-pause/analysis/code/ztest_analysis.py` |
| §8 motor | `python3 deliverables/2026-09-19-pause/analysis/code/approach_and_motor.py` |
| §9 gap motion | `python3 deliverables/2026-09-19-pause/analysis/code/gap_stability.py` |
| §1, §2, §10 file-level facts | `python3 deliverables/2026-09-19-pause/analysis/code/build_inventory.py` |

Each script runs from the repository root, reads only `sessions/data/`, and writes only into this
directory.
