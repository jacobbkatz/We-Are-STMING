# Verdict on Jacob's hypothesis

**Subagent 2, 2026-09-19.** The hypothesis put to me, in Jacob's framing:

> Some scans may contain a real image of the sample, but swinging or motion of the instrument
> prevented repeatable imaging, and so potentially meaningful results were dismissed.

**It is two claims, and they do not get the same answer.**

---

## In one paragraph

**The second half of the hypothesis is right, and the first half is not supported.** Motion is the
blocker, and the numbers are not close: the gap's own unsteady motion over the five seconds an image
takes is 396 to 1,722 Z counts, while the corrugation of every unclamped candidate scan in the
project is 29 to 458 counts. **The thing being measured is smaller than the way the gap moves while it is being
measured.** But when I searched all 51 recordings for a surviving image, **nothing did.** The
project's strongest candidate — the 636-count profile at ±15,000 X that
`sessions/2026-09-17-bench.md` §3.25 has carried as **UNDETERMINED** since 2026-09-17 — turns out to
be the feedback loop recovering from a 30,000-count X flyback between passes, and I can predict its
size from the tilt and predict its absence in two other data sets. **One candidate survives as worth
a single further measurement, not as a result.** And separately: **two of the record's published
reasons for dismissing scans do not hold up**, which is the part of Jacob's hypothesis about
*dismissal* being partly vindicated even though no image is.

---

## 1. What the data support

**Motion prevented repeatable imaging. This is established, in numbers, and it is Jacob's point.**

| Evidence | Where |
|---|---|
| The gap moves by **≥ 43,000 counts in 6.4 s** and **≥ 56,000 over ~2 min** with the motor and hands still | `sessions/2026-09-19-morning.md` §3.9, already on record |
| Across five Z-test runs, the **scatter of the onset Z after removing steady drift** is **396 to 1,722 counts** | measured here, `code/06_motion_and_timing.py`, from `sessions/data/2026-09-19-morning/ztest_*.csv` and `bias_*.csv` |
| Corrugation of every unclamped candidate scan, measured here | **29 to 458 counts** — 21 files, `work/inventory.csv` |
| A 21 × 11 image takes | **~5 s** — `cas9.log`: lock-in 03:48:10, scan 0 complete 03:48:15; the eight that follow are 4–9 s apart |

**So an image could not have been stable even if the surface were perfect.** Nothing in the
electronics, the amplifier, the leakage, the feedback loop or the read noise is the limit; that was
established on 2026-09-17 with numbers and I found nothing to disturb it.

**There is also a real, X-motion-dependent signal in the wide images that is not noise.** In
`img_scan_1/2.csv` the trace/retrace correlation is −0.85 to −0.92 at zero shift and rises to +0.83
to +0.93 at a shift of about ten pixels, symmetric in sign — a signal roughly periodic over one pass
(~4–5 Hz, if the wide images ran at the same 10.8 ms per pixel as the same night's `cas9` scans —
no timing was logged for them, so that rate is inherited; **the periodicity in pixels is measured
directly and is what the argument uses**), mirrored between the two scan directions. **The X-held
controls, identical timing, show nothing like it at any shift.** That is a control-backed statement
that X motion is required, which upgrades `sessions/2026-09-19-morning.md` §6's "likely but
unproven". It is not an image — a surface gives the same height at the same X whichever way the tip
travels — but it is a real property of this instrument and worth characterising.

---

## 2. What the data contradict

**No image survives, and the strongest candidate has a mechanism.**

### Candidate A is closed

`sessions/data/2026-09-17-bench/line_repeated_wide.csv`, 12 passes at ±15,000 X: consecutive-pass
r +0.647, split-half +0.923, a 636-count averaged profile, overwhelmingly significant against
phase-randomised surrogates (p < 2 × 10⁻⁴). **All of that is true and none of it is the sample.**

| | |
|---|---|
| tilt of the twelve passes | **−0.105 Z counts per X count** |
| X flyback between passes (the tool jumps X back to start the next one) | **30,000 counts** |
| **Z error the loop must recover at each pass start** | **3,144 counts** |
| observed recovery in the first two pixels | **2,465 counts** |
| a mid-line step, for comparison | −236 counts |
| **consecutive-pass r after dropping two pixels** | **+0.647 → +0.048** |

**The same arithmetic predicts the transient's absence twice.** The two 2D wide images of the same
night raster back and forth without lifting X, so there is no flyback — start-of-pass jumps 37 and
78 counts. The 2026-09-19 three-Y runs do fly back but their tilt is near zero, so the predicted
recovery is 28 and 238 counts — observed −99 and +47. **One piece of arithmetic, three data sets,
right about the presence and right about the absence.**

**This check was already in the repository, one level up.** `sessions/2026-09-17-bench.md` §3.22
killed an r of +0.75 by dropping the first *line* of an image. **Nobody applied it to the first
*pixels* of a line.** Credit for the check belongs to whoever wrote §3.22.

**A second, independent test agrees.** `scan_wide_25nm_1.csv` and `_2.csv` are two complete images
of the same nine Y places on the same X grid — the ±15,000 place test §3.25 said had never been run,
sitting in the same directory the whole time. Same place r = +0.216 ± 0.228, different place
+0.074 ± 0.063, **permutation p = 0.24** (forward) and **0.28** (backward).

> **`sessions/2026-09-17-bench.md` §3.25's "UNDETERMINED" can be retired.** That is a change to a
> recorded conclusion, flagged here as the brief requires. It moves in the direction of *less*
> claim, not more.

### Nothing else clears the bar either

At **201 reproducibility tests** across this data (counted in `code/07_chance.py`), a Bonferroni
5% threshold is **p < 2.5 × 10⁻⁴**, about 3.7σ, and about ten p < 0.05 results are expected from
noise alone. **Nothing reaches it as evidence of a surface.**

---

## 3. Where the record was too strong — and Jacob is partly right about dismissal

**Two published dismissal arguments do not hold up. Neither resurrects an image.**

**(a) "The controls reproduce better than the scans, +0.37 against +0.04."** Found by the lead;
independently confirmed here. `sessions/data/2026-09-19-bench/scripts/analyze_scans.py` lines 50–51
truncate to the shorter file with no shape check, and `cas9_xheld2.csv` is a single aborted line, so
two of the three control correlations were computed over 21 points instead of 231. Like for like,
full images only: **scans +0.04, controls +0.07. Indistinguishable.**

**(b) The same defect contaminates a second conclusion, and worse — found here.**
`sessions/2026-09-19-bench.md` §3.16: *"Image to image +0.56 to +0.86, matched by the X-held
controls' +0.56."* **`img_scan_0.csv` is 1 line and `img_scan_1.csv` is 2 lines**, so **both** scan
pairs were computed over 21 and 42 points and **neither was an image-to-image correlation at all**.
There are only two full wide recordings and both are controls, so **no like-for-like scan figure
exists**. The comparison as published is between things of different kinds.

**I audited the whole data set for this defect class** (`code/11_truncation_audit.py`). Short files
exist in three groups — `cas9` (one), `img_` (two), `tuned_s3k` (four) — and **2026-09-17 is
clean**: every set that session compared against itself is of uniform length, and its other figures
(corrugation, trace/retrace) are per-file statistics that no truncation can touch.

**And the three-Y result is real but was over-stated.** I verified all five runs from the raw CSVs
with shapes checked first; every file is 3 × 6 × 21, no truncation, and every published number
reproduces exactly. **The non-reproduction between run 2 (+0.374) and run 4 (+0.056) is real.** But
the "3.9 sigma" is not: that standard error treats 45 within-place and 108 between-place pairwise
correlations as independent when every pass appears in many of them. Under a 20,000-fold permutation
of the place labels, **run 2 is p = 0.0036** — and **an X-held control, which contains no sample
structure by construction, scores p = 0.02 on the same statistic.**

> **So Jacob's instinct about dismissal has something in it.** Not "a real image was thrown away" —
> I looked hard and there is none. But **the arguments used to dismiss were in places weaker than
> the record claimed**, and in two cases rested on a silent bug. The conclusion happened to be right
> for reasons partly other than the ones written down. That is worth knowing, because the next
> person will inherit the reasons, not the conclusion.

---

## 4. What the data cannot resolve

**Stated plainly, because these are the places where "no image" is an assumption and not a
measurement.**

1. **The place test has limited power.** With nine same-place pairs, the 2026-09-17 ±15,000 test can
   only exclude a same-minus-other difference bigger than about **+0.47**. **A weak genuine surface
   signal is not excluded by it.** What closes candidate A is the flyback mechanism, not this null.

2. **Candidate B cannot be settled with the data that exist.** Run 2 at y_sep 12,000 gave
   within-place +0.239 against between-place −0.135 — the only measurement in this project that has
   ever looked like topography. Its repeat, half an hour later, gave +0.056. **In between, the gap
   demonstrably moved by most of the Z range.** "It did not repeat" and "the surface moved out from
   under it" are not distinguishable here. **This is the strongest form of Jacob's hypothesis and I
   cannot refute it.**

3. **Four of the files this work depends on are not listed in their own directory's `README.md`** —
   `scan_wide_25nm_1/2.csv`, `line_repeated_wide.csv` and `line_three_y_positions.csv` in
   `sessions/data/2026-09-17-bench/`. Between them they are the project's strongest candidate and
   the data that answers it. **That is the likeliest reason §3.25 believed the place test had never
   been run.** Flagged for the lead; `sessions/data/` is read-only to me.

4. **Whether the tip was ever over gold rather than copper.** `sessions/2026-09-17-bench.md` §3.27:
   *"oh ya I think your prooabbly over copper"* (`SAID`). Nothing electrical can tell them apart.

5. **The Z scale is inherited, not measured.** Every statement here in Z DAC counts is scale-free
   and unaffected. Any conversion to nanometres is not, and I have made none.

6. **What the mirrored, line-periodic signal in the wide images actually is.** Loop hunting, X-piezo
   coupling into Z, or **the tip ploughing a compliant sample** are all consistent. The third would
   be a real measurement of the gold's compliance and fits the record's "soft, pressed, sticky
   contact" and the gold "following the retracting tip in". **Untested.**

7. **No periodicity in the gap's motion could be found**, so there is nothing for a scanner to
   synchronise to — but the position records are too sparse to *exclude* one, exactly as
   `sessions/2026-09-19-morning.md` §6 says. My spectral check on four long fixed-point records
   adds three records to that conclusion and finds no coherent line in any of them.

---

## 5. What would settle it at the bench

**Written to be executed with no memory of this conversation.** These go to the lead for
`docs/NEXT_SESSION_PLAN.md`; they are **not** bench instructions issued from here, and every one of
them comes **after** the plan's existing gates — reassembly, re-verification, the stillness
recording, a stiffer sample and a sharper tip. **None of them is worth doing until the gap holds
still**, because all of them are measurements of reproducibility and the gap currently moves more
than the signal.

### The one measurement that would settle candidate B

**Repeat the three-Y control at y_sep 12,000 and ±15,000 X, three times in a row, with the gap
proven still first.** `py Code/pc/stm_y_control.py 15000 1500 6 12000 1000 <out>.csv`, three runs
back to back, plus **one X-held control run interleaved between them**, not at the end.

- **The X-held run is the point.** It scored p = 0.02 on this statistic on 2026-09-19 with nothing
  to see. Until a control is run *in the same conditions as the positive*, a positive cannot be
  read.
- **Analyse with a permutation test, not the printed sigma.** `code/07_chance.py` has it.
- **Decision rule, fixed in advance:** the effect is real if **all three** real runs beat **all**
  interleaved controls. One positive out of three is what 2026-09-19 already produced and it means
  nothing.

### Three cheap fixes that cost nothing and remove known artefacts

1. **Discard the first three pixels of every pass, in the tool.** The flyback recovery is
   3,144 counts on a −0.105 tilt and it is what produced the project's best-looking result. A
   `--skip-lead 3` in `stm_y_control.py` and `stm_feedback_scan.py`, with the skipped points still
   written to the file so nothing is lost.
2. **Make every image-to-image comparison refuse a shape mismatch.**
   `sessions/data/2026-09-19-bench/scripts/analyze_scans.py` lines 50–51 truncate silently and that
   defect reached two published conclusions. Any promoted version must raise rather than truncate.
   **Test it by feeding it a one-line file deliberately and confirming it goes red** — `CLAUDE.md`
   §7 rule 2.
3. **Scan X boustrophedon between passes as well as within a line.** The 2D images already do this
   and have no transient. The line-repeat tool does not, and that is the whole of candidate A.

### The measurement that would turn candidate D into physics

**Run the wide ±15,000 image at two X speeds — the normal one and one four times slower — with an
X-held control at each speed.** The mirrored, roughly line-periodic signal is currently consistent
with loop hunting, with X-piezo coupling into Z, and with the tip ploughing a compliant sample.

- If the structure **keeps the same period in pixels**, it is locked to the scan and it is the loop.
- If it **keeps the same period in time** (so half as many cycles per pass at a quarter speed), it
  is a ~4–5 Hz mechanical disturbance being sampled by the raster.
- If it **keeps the same period in X** and its amplitude falls with speed, it is the tip dragging
  the sample — which would be the first direct measurement of the gold's compliance and worth having
  in its own right.

**This is the single most informative unrun experiment I found**, because all three answers are
useful and the measurement is four images.

### And the one that would make any of it worth doing

**Prove the gap holds still for sixty seconds before scanning anything.** `docs/NEXT_SESSION_PLAN.md`
already has this as step 4. **It is the gate.** Until the onset Z holds within, say, 200 counts over
a minute, every imaging statistic above is dominated by the gap and no amount of analysis will
recover a picture from it.

---

## 6. The honest answer, in the form Jacob asked the question

**Did some scans contain a real image of the sample?**
**No scan in this project contains a demonstrable image, and I looked at all 51 recordings.** The
one that came closest has an arithmetic explanation that also predicts where it should be absent,
and it is.

**Did motion prevent repeatable imaging?**
**Yes, and by a wide margin.** The gap moves by 396–1,722 counts over the time an image takes, and
the images' own corrugation is 29–458 counts. **This half of the hypothesis is correct and is the
right thing to fix.**

**Were potentially meaningful results dismissed?**
**Partly — but for process reasons, not because a picture was thrown away.** Two published
dismissal arguments do not survive checking, one found by the lead and one found here, both from the
same silent truncation bug. And one positive result (the three-Y run at 12,000 apart) was dismissed
on a non-reproduction that is real but whose "3.9 sigma" was never 3.9 sigma — in **both**
directions: it was weaker than claimed *and* it was dismissed against a control that had not been
run in the same conditions. **That one deserves a second look at the bench, and it is the only one.**

---

*Everything in this verdict is reproducible from `code/`. Each script's docstring carries the one
command that runs it from the repository root; console output is in `work/NN_output.txt`; the
figures are in `gallery/`; the candidate-by-candidate reasoning is in `GALLERY.md`.*
