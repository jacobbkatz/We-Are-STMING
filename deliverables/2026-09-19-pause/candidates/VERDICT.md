# Verdict on Jacob's hypothesis — did a real image survive, and did motion hide it?

**Subagent 2, 2026-09-19.** The hypothesis put to me, in Jacob's framing:

> Some scans may contain a real image of the sample, but swinging or motion of the instrument
> prevented repeatable imaging, and so potentially meaningful results were dismissed.

**It is two claims and one suspicion, and they get three different answers.** All three are
results.

> **Framing note.** `deliverables/2026-09-19-pause/FRAMING.md` carries Jacob's instruction about
> emphasis and it governs how this is written. **It changed no finding, no number, no uncertainty
> and no caveat in this file.** What it changed is that a measured obstacle and a ruled-out
> candidate are written down as what they are — results — rather than as apologies.

---

## The short answer

| The claim | The answer | Strength |
|---|---|---|
| **Motion prevented repeatable imaging** | **Confirmed, and quantified.** The gap moves by 396–1,722 Z counts over the five seconds an image takes; every candidate image's corrugation is 29–458 counts. **The blocker is found and measured** | Decisive |
| **A real image is sitting in the recordings underneath the motion** | **Not supported.** I searched all 51 recordings. The strongest candidate turns out to have an arithmetic explanation that predicts its size *and* predicts where it should be absent — and it is | Decisive for that candidate; one other stays open |
| **Meaningful results were dismissed** | **Partly right, and this is the most interesting finding in the file.** Two published dismissal arguments do not survive checking, both from the same silent bug. The conclusions happen to hold on other evidence — but they held for reasons other than the ones written down | Established, twice |

**The organising sentence, and it is what the evidence says:** *the measurement chain does
everything an imaging instrument needs it to do; what stands between this instrument and a picture
is mechanical stability, and this work measured it rather than guessing at it.*

**What is not supportable, and I will not write it:** that any scan in this project contains a
demonstrable image of the sample. It does not, and an overclaim here would be the one thing capable
of damaging the rest of the work.

---

## 1. The method is the headline result

**Before any candidate: the reason nobody in this project has fooled themselves is that every
imaging claim was run against a control designed to kill it.** That is worth stating as a finding
about method, because it is unusual and it did the work.

**An X-held control re-runs a scan with identical timing and identical loop behaviour while X never
moves.** It therefore contains **no sample structure at all, by construction**. Anything that shows
up in both a scan and its control is the instrument.

**It repeatedly beat the result it was controlling**, which is exactly what a control is for:

| Comparison | Real scans | Their X-held control |
|---|---|---|
| ±400 position-locking, 2026-09-17 (102 lines vs 8) | **−0.069 ± 0.049** | **+0.170 ± 0.118** |
| ±400 corrugation | 29–43 counts | **87 counts** |
| ±1500 position-locking, 2026-09-19 (44 lines vs 34) | −0.066 ± 0.137 | −0.053 ± 0.144 |
| three-Y place statistic, permutation p | run 2: 0.0036 | **an X-held control: 0.020** |

**Read the last row.** A control containing nothing scores p = 0.02 on the project's own
"is this the surface?" statistic. **That is the empirical false-positive rate of this measurement on
this instrument**, and knowing it is worth more than any single positive would have been.

**And the searching was budgeted.** 201 reproducibility tests have been run across this data
(`code/07_chance.py`). At that many, a 5% threshold is expected to throw up **about ten** apparent
findings from noise alone, so the honest threshold is Bonferroni's **p < 2.5 × 10⁻⁴**, about 3.7σ.
**Nothing in this body of data reaches it as evidence of a surface** — and the fact that the
threshold was computed before the candidates were judged is itself the point.

---

## 2. Motion is the blocker, and it is measured

**This is Jacob's hypothesis and the data back it without qualification.**

| Evidence | Where |
|---|---|
| The gap moves by **≥ 43,000 counts in 6.4 s** and **≥ 56,000 over ~2 min**, motor and hands still | `sessions/2026-09-19-morning.md` §3.9, already on record |
| Across five Z-test runs, the **onset Z scatter after removing steady drift**: **396, 637, 849, 1,358 and 1,722 counts** | measured here, `code/06_motion_and_timing.py`, from `sessions/data/2026-09-19-morning/ztest_*.csv` and `bias_*.csv` |
| Corrugation of every unclamped candidate scan, measured here | **29 to 458 counts** — 21 files, `work/inventory.csv` |
| A 21 × 11 image takes | **~5 s** — `cas9.log`: lock-in 03:48:10, scan 0 complete 03:48:15; the eight that follow are 4–9 s apart |

**The thing being measured is smaller than the way the gap moves while it is being measured.** That
single comparison explains the whole imaging record, and it is a number, not an impression.

**Nothing electronic is the limit.** That was established on 2026-09-17 with numbers — flat white
electrical noise at 8–14 counts, leakage under 0.06 nA to ±2 V, a loop holding current to 0.06 of a
decade at 2,000 pixels a second — and I found nothing to disturb any of it. **The instrument's
measurement chain is not what is missing.**

### A real instrument signal was found on the way

**In the wide ±15,000 images, trace and retrace are −0.85 to −0.92 correlated at zero shift and
+0.83 to +0.93 at a shift of about ten pixels, symmetric in sign.** That is a signal roughly
periodic over one pass, mirrored between the two scan directions. **The X-held controls, identical
timing, show nothing of the kind at any shift** (+0.24 → +0.32 and +0.15 → +0.18).

**So X motion is required to produce it.** That upgrades `sessions/2026-09-19-morning.md` §6's
"X motion is the likely but unproven cause" to a control-backed statement. It is a real,
characterisable property of this scanner and it was not known before this work.

**It is not an image.** A surface gives the same height at the same X whichever way the tip is
travelling; a mirrored signal is produced by the scan rather than found by it.

*(At the same night's measured pixel rate of ~10.8 ms this would be ~4–5 Hz, inside the 5–30 Hz band
the 2026-09-17 noise spectroscopy already blamed. **No timing was logged for the wide images, so
that rate is inherited from the `cas9` scans and the hertz figure rests on it. The periodicity in
pixels is measured directly and is what the argument uses.**)*

---

## 3. Candidate A: closed, with a mechanism — and that is a result

**The project's strongest candidate has been open since 2026-09-17.**
`sessions/2026-09-17-bench.md` §3.25:

> At ±15,000 there is a reproducible profile of about 636 counts, and whether it is the sample or
> the scanner's own bow is **UNDETERMINED**. The experiment that would settle it … **has not been
> run.**

`sessions/data/2026-09-17-bench/line_repeated_wide.csv`, 12 passes: consecutive-pass r **+0.647**,
split-half **+0.923**, averaged profile **636 counts**, and against 5,000 phase-randomised
surrogates **p < 2 × 10⁻⁴**. **All of that is true. It is genuinely reproducible and it is not
noise.** It is also not the sample, and the reason is arithmetic:

| | |
|---|---|
| tilt of the twelve passes | **−0.105 Z counts per X count** |
| X flyback between passes (the tool jumps X back to start the next one) | **30,000 counts** |
| **Z error the loop must therefore recover at each pass start** | **3,144 counts** |
| observed recovery in the first two pixels | **2,465 counts** |
| a mid-line step, for comparison | **−236 counts** |
| **consecutive-pass r after dropping two pixels** | **+0.647 → +0.048** |

**The same arithmetic predicts the transient's absence, twice.** The two 2D wide images of the same
night raster back and forth without lifting X, so there is no flyback — start-of-pass jumps **+78
and +37 counts**, an ordinary step. The 2026-09-19 three-Y runs **do** fly back but their tilt is
near zero (−0.0009, +0.0079), so the predicted recovery is **28 and 238 counts** — observed **−99
and +47**. **One piece of arithmetic, three data sets, right about the presence and right about the
absence.**

**A second, independent test agrees, and it closes a gap in the record.**
`scan_wide_25nm_1.csv` and `_2.csv` are **two complete 2D images of the same nine Y places on the
same X grid** — the ±15,000 place test §3.25 said had never been run, sitting in the same directory
the whole time. Same place r = **+0.216 ± 0.228** (n = 9), different place **+0.074 ± 0.063**
(n = 72), **permutation p = 0.24** forward and **0.28** backward.

> **Stated as a limit, not buried:** with nine same-place pairs that null can only exclude a
> difference bigger than about **+0.47**. A weak genuine surface signal is **not** excluded by it.
> **What closes this candidate is the flyback mechanism, not that null.**

> **Credit where it belongs.** `sessions/2026-09-17-bench.md` §3.22 killed an r of +0.75 on the same
> night with exactly this check, applied to the first *line* of an image. **Nobody had applied it to
> the first *pixels* of a line.** The idea was already in the repository; this work extended it one
> level down.

**`sessions/2026-09-17-bench.md` §3.25's "UNDETERMINED" can now be retired.** That is a change to a
recorded conclusion, flagged as the brief requires, and it moves toward *less* claim. **Closing an
open question with a mechanism is a result** — it is the difference between an unexplained
reproducible feature that would have gone on a poster and a characterised scanner artefact with a
one-line fix.

---

## 4. Candidate B: a well-posed open question, and the one worth bench time

`sessions/data/2026-09-19-bench/ycontrol_run2_ysep12000.csv` is **the only measurement in this
project that has ever looked like topography**: within-place +0.239, between-place −0.135,
difference **+0.374 ± 0.097**, reported on the night as 3.9σ.

**I verified all five three-Y runs from the raw CSVs with shapes checked first.** Every file is
3 places × 6 passes × 21 points — no short pass, no aborted run, **so the truncation defect in §5
does not touch this result** — and every published number reproduces exactly. **The
non-reproduction between run 2 (+0.374) and run 4 (+0.056) is real.**

**And the 3.9σ was never 3.9σ — in both directions.** That standard error treats 45 within-place
and 108 between-place pairwise correlations as independent when every pass appears in many of them.
Under 20,000 permutations of the place labels:

| Run | within − between | **permutation p** |
|---|---|---|
| **run 2, the positive** | +0.523 | **0.0036** — a factor of 14 short of the corrected threshold |
| run 4, the repeat | +0.059 | 0.26 |
| **an X-held control, y_sep 3000** | **+0.226** | **0.020** — with nothing to see |

**The honest position: this cannot be settled with the data that exist.** Run 2 and run 4 are half
an hour apart, and in between the gap demonstrably moved by most of the Z range. **"It did not
repeat" and "the surface moved out from under it" are not distinguishable here.** This is the
strongest form of Jacob's hypothesis and **I cannot refute it.**

**It is also a well-posed question with a four-image answer** — see §6.

---

## 5. How this project has evaluated its own data — a finding in its own right

**Twice now, a published dismissal statistic has been computed across truncated files.** Both were
found by replicating the numbers rather than reading them; the lead found the first and both of us
reached the second.

**(a) "The controls reproduce better than the scans, +0.37 against +0.04"** (`STATUS.md`,
`sessions/2026-09-19-bench.md` §3.14; lead's `LEAD_VERIFICATION.md` V4, confirmed independently
here). `sessions/data/2026-09-19-bench/scripts/analyze_scans.py` lines 50–51 truncate to the
shorter file with no shape check, and `cas9_xheld2.csv` is a single aborted line, so **two of the
three control correlations were computed over 21 points instead of 231**. Like for like, full
images only: **scans +0.04, controls +0.07. Indistinguishable.**

**(b) The wide images have the identical defect and it is worse** (`sessions/2026-09-19-bench.md`
§3.16; lead's V5, found independently here as `code/11_truncation_audit.py`).
**`img_scan_0.csv` is 1 line and `img_scan_1.csv` is 2 lines**, so both scan correlations were
computed over 21 and 42 points and **neither was an image-to-image correlation at all**. With only
one complete real wide image, **no like-for-like scan figure exists**. The controls' +0.56 over 231
points is the only sound number in that group — and it is a real result: **with X held, the
instrument repeats its own pattern strongly**, which is a measurement of the instrumental
signature.

**I audited the whole data set for the defect class** (`CLAUDE.md` §7 rule 1 — a defect is a class,
not an instance). Short files exist in three groups: `cas9` (one), `img_` (two), `tuned_s3k` (four).
**2026-09-17 is clean** — every set that session compared against itself is of uniform length, and
its other figures are per-file statistics no truncation can touch.

**Neither correction resurrects an image, and I want that unambiguous.** The real scans still do not
reproduce — +0.09, +0.18 and −0.15 over full images, scattering both sides of zero — and that
evidence needs no correction and carries the conclusion on its own.

> **So Jacob's suspicion about dismissal has something in it, precisely and narrowly.** Not that a
> picture was thrown away — I looked at all 51 recordings and there is none. But **the arguments
> used to dismiss were in two places weaker than the record claimed, and both times the conclusion
> was right for reasons other than the ones written down.** That matters because the next person
> inherits the reasons, not the conclusion. **This is what a project that checks itself looks like
> when it works**: the errors were found by replication, from inside, before anything went on a
> poster.

---

## 6. The open questions, and the experiment that settles each

**These are questions, not shortfalls. Each has a specific, cheap answer.** They go to the lead for
`docs/NEXT_SESSION_PLAN.md`; they are **not** bench instructions issued from here, and every one
comes **after** the plan's existing gates — reassembly, re-verification, the stillness recording, a
stiffer sample and a sharper tip. **None is worth doing until the gap holds still**, because all of
them measure reproducibility and the gap currently moves more than the signal.

### Q1 — Is candidate B real? *(the one I would spend bench time on)*

**Repeat the three-Y control at y_sep 12,000 and ±15,000 X, three times, with an X-held control
interleaved between them** — not run at the end.
`py Code/pc/stm_y_control.py 15000 1500 6 12000 1000 <out>.csv`.

- **The interleaved control is the point.** An X-held run scored p = 0.02 on this statistic on
  2026-09-19 with nothing to see. A positive cannot be read until a control has been run in the same
  conditions.
- **Analyse with the permutation test, not the printed sigma** — `code/07_chance.py` has it.
- **Decision rule, fixed in advance: the effect is real if all three real runs beat all interleaved
  controls.** One positive out of three is what 2026-09-19 produced and it means nothing.

### Q2 — What is the mirrored, line-periodic signal in the wide images? *(the most informative unrun experiment I found)*

**Run the wide ±15,000 image at two X speeds — the normal one and one four times slower — with an
X-held control at each speed.** Four images, and **all three possible answers are useful**:

| If the structure keeps the same period in… | …then it is |
|---|---|
| **pixels** | locked to the scan — the feedback loop hunting |
| **time** (half as many cycles per pass at quarter speed) | a ~4–5 Hz mechanical disturbance being sampled by the raster |
| **X**, with amplitude falling as speed falls | **the tip dragging a compliant sample** — which would be the first direct measurement of the gold leaf's compliance, and fits the record's "soft, pressed, sticky contact" and the gold "following the retracting tip in" |

### Q3 — Three fixes that cost nothing and remove known artefacts

1. **Discard the first three pixels of every pass, in the tool** (`--skip-lead 3` in
   `stm_y_control.py` and `stm_feedback_scan.py`, with the skipped points still written to file so
   nothing is lost). The flyback recovery is 3,144 counts on a −0.105 tilt and it produced the
   project's best-looking result.
2. **Make every image-to-image comparison refuse a shape mismatch rather than truncate.** If
   `analyze_scans.py` is ever promoted to `Code/pc/`, it must raise — and **the check must be shown
   red against a one-line file first** (`CLAUDE.md` §7 rule 2).
3. **Fly X back boustrophedon between passes as well as within a line.** The 2D images already do
   this and have no transient; the line-repeat tool does not, and that is the whole of candidate A.

### Q4 — The gate that makes any of the above worth doing

**Prove the onset Z holds within about 200 counts over sixty seconds before scanning anything.**
`docs/NEXT_SESSION_PLAN.md` already has this as step 4. **It is the gate.** Until it passes, every
imaging statistic is dominated by the gap and no amount of analysis will recover a picture.

---

## 7. What this work cannot resolve

**Stated plainly and once, because these are where "no image" is an assumption rather than a
measurement.**

1. **Candidate B.** Run 2 and run 4 are half an hour apart and the gap moved between them. Not
   distinguishable here (§4).
2. **The ±15,000 place test's power.** ±0.47 at 2σ with nine pairs. A weak genuine surface signal is
   not excluded by it (§3).
3. **Four files this work depends on are not listed in their own directory's `README.md`** —
   `scan_wide_25nm_1/2.csv`, `line_repeated_wide.csv` and `line_three_y_positions.csv` in
   `sessions/data/2026-09-17-bench/`. Between them they are the project's strongest candidate and
   the data that answers it. **That is the likeliest reason §3.25 believed the place test had never
   been run.** For the lead; `sessions/` is read-only to me.
4. **Whether the tip was ever over gold rather than copper.** `sessions/2026-09-17-bench.md` §3.27:
   *"oh ya I think your prooabbly over copper"* (`SAID`). Nothing electrical distinguishes them.
5. **The Z scale is inherited, not measured.** Every number here is in Z DAC counts and is
   scale-free. **I have made no conversion to nanometres.**
6. **The mechanism of the mirrored wide-image signal** — three candidates, none tested (Q2).
7. **No periodicity was found in the gap's motion**, so there is nothing to synchronise a scanner
   to — but the position records are too sparse to *exclude* one, exactly as
   `sessions/2026-09-19-morning.md` §6 says. My split-half coherence check adds three more records
   (`here_run1.csv` with a real junction, `touchrec_run1.csv`, `stamp.csv`) and finds **no coherent
   line in any of them**; the one line found is 63.6 Hz in a tip-clear control, which is electrical.

---

## 8. The answer, in the form Jacob asked the question

**Did some scans contain a real image of the sample?**
**No scan in this project contains a demonstrable image, and I looked at all 51 recordings.** The
one that came closest has an arithmetic explanation that also predicts where it should be absent,
and it is. **One candidate remains genuinely open and has a four-image test.**

**Did motion prevent repeatable imaging?**
**Yes, and by a wide margin — and we measured it.** The gap moves by 396–1,722 counts over the time
an image takes; the images' own corrugation is 29–458 counts. **This half of the hypothesis is
correct, it is the right thing to fix, and knowing precisely what stops you is most of the value in
eight weeks of instrument development.**

**Were potentially meaningful results dismissed?**
**Partly — for process reasons, not because a picture was thrown away.** Two published dismissal
arguments do not survive checking, both from the same silent truncation bug, and one real positive
was dismissed against a control that had not been run in the same conditions. **That one deserves a
second look at the bench, and it is the only one.**

---

*Everything here is reproducible from `code/`. Each script's docstring carries the one command that
runs it from the repository root; console output is in `work/NN_output.txt`; the figures are in
`gallery/`; the candidate-by-candidate reasoning, including the candidates that failed early, is in
`GALLERY.md`.*
