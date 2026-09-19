# What we built, what it measures, and what we found in the way

**The pause-point report, 2026-09-19.** Written for Jacob and Nuh, in plain language, by the
report agent of the pause-point work. **Every number here carries where it came from and how
sure it is.**

> **The one-sentence version, and it is what the evidence says:**
> **Every subsystem a tunnelling microscope needs is built, working and calibrated. What is left
> is mechanical — and we measured it rather than guessed at it.**

**`STATUS.md` is the live technical record. This report has no independent authority over it.**
Where this report and `STATUS.md` disagree, `STATUS.md` wins and this file is the one to fix.
Canonical numbers live in [`docs/FACTS.md`](../../../docs/FACTS.md); open questions live in
[`docs/OPEN_QUESTIONS.md`](../../../docs/OPEN_QUESTIONS.md). This report cites those figures inside
its arguments, as the project's rules allow, and **is not a second register of constants.**

### How to read the marks

| Mark | Means |
|---|---|
| **MEASURED** | a number that came off our instrument, with the date it was taken |
| **DERIVED** | arithmetic on measured numbers; the arithmetic is shown or named |
| **ASSUMED** | taken from somewhere else and not checked on our hardware |
| `SAID` | Jacob or Nuh told us, with the date |
| `READ` | a reading of a photograph or a file by Claude — plausible, **not confirmed** |

**Two words that are not the same and are kept apart throughout: a *barrier* is two conductors
separated by something electrons have to cross. *Tunnelling* is one particular kind of barrier —
a clean vacuum gap. We have evidence of the first. We have not demonstrated the second, and we
have never produced an image.**

### The figures

**Six finished figures are in `deliverables/2026-09-19-pause/figures/png/`**, with print versions
beside them and their full captions in that directory. **They supersede the working plots in
`deliverables/2026-09-19-pause/analysis/plots/`**, which were made before today's corrections.

| | |
|---|---|
| `fig01_calibration.png` | the measurement chain against Ohm's law |
| `fig02_iv_curve.png` | the 2026-09-17 junction's current against voltage, at V^1.55, with the barrier-is-not-a-tunnelling-gap caveat on the figure itself |
| `fig03_gap_motion.png` | the blocker, measured |
| `fig04_control.png` | the control, and what it settled |
| `fig05_ztest.png` | the distance test, 110 cycles at four biases — **no distance scale, because we have never established one** |
| `fig06_noise.png` | the noise floor, still against stamping |

---

## 1. The short version

1. **The whole measurement chain works end to end and agrees with theory to 0.13 of a standard
   error.** A known resistance in place of the tip gave −3,205 ± 37 counts per volt against
   −3,200 predicted before the measurement was taken. MEASURED 2026-09-16.
2. **The amplifier resolves picoamps.** About 4 pA of its own input current, against a tunnelling
   signal of about 1 nA — roughly 250 times smaller than the thing it has to find. MEASURED
   2026-09-15.
3. **The electronics are not the limit, and that was established with numbers rather than
   opinion.** Flat white noise at 8 to 14 counts across the whole band, no mains peak, leakage
   under 0.06 nA from −2 V to +2 V. MEASURED 2026-09-17.
4. **A real tip-to-sample junction was made, and its current responds to voltage and to
   distance.** Its current-voltage curve has the non-ohmic, bias-symmetric shape a barrier
   requires, and rules out both a metallic short and an open circuit. MEASURED 2026-09-17.
5. **It is a barrier. It is not established as a clean tunnelling gap.** A separate distance test
   two nights later, on a **different tip and a different sample**, found a junction that behaves
   like a soft, pressed contact rather than a vacuum gap. MEASURED 2026-09-19. Both results stand;
   they are different junctions.
6. **We found the blocker and put a number on it.** With the motor stopped and nobody touching
   the instrument, the gap moved by more than 43,000 Z counts in 6.4 seconds and more than 56,000
   within two minutes — most of the Z range. The structure an image would have to show is 29 to
   458 counts. MEASURED 2026-09-19.
7. **No image has been produced, and we know that because of our own controls**, not because
   nothing turned up. Every imaging test was run against a control in which the tip never moved
   sideways — which cannot contain surface structure by construction.
8. **At this pause point we found and fixed six errors in our own record**, including two
   statistics that had been used to dismiss results. Every conclusion survived; two of the
   arguments for them did not. That is written up in section 7, because a project that catches its
   own mistakes from the inside is demonstrating method, and the method is a result.

---

## 2. What was built

There was no kit. Two people who do not write code designed, ordered, printed, assembled,
wired and characterised a complete scanning-probe measurement chain.

- **Mechanics, firmware and controller board** follow Mech Panda's open-source `red-panda-stm`.
  **The scan head, tip preparation and the transimpedance preamplifier** follow Dan Berard's
  home-built STM. What is ours is the electronics bring-up, the control and analysis software,
  the calibration, and the fault isolation described here.
- **The instrument**: a Teensy 4.1 microcontroller driving four 16-bit digital-to-analog
  converters (X, Y and sample bias at ±3 V, Z at ±10 V) over one serial bus, and a 16-bit
  LTC2326-16 converter reading the current back on another. A 26-way ribbon connects the
  controller to the Teensy. An OPA627 transimpedance amplifier with a 100 MΩ feedback resistor
  sits at the scan head, inside a hand-folded copper box, as close to the tip as it physically
  can. A 28BYJ-48 stepper through a ULN2003 drives the coarse approach, wired directly to the
  Teensy.
- **The frame, scan head, isolation stack and enclosures** are 3D-printed in carbon-filled PETG.
  The suspended platform is a Ø200 mm printed disc hung on three springs over an eddy-current
  damping stack.
- **The record**: 26 session logs, 163 raw data files in four bench-session directories, 92
  photographs of our own hardware, and every analysis script committed beside the data it reads.

**Dates.** The earliest dated file in the repository is 3 July 2026. **The first volt went through
any of it on 29 August.** The last bench session was the morning of 19 September. So: about
eleven weeks of building, and three weeks of powered bring-up.

---

## 3. What the instrument demonstrably does

### 3.1 The measurement chain is calibrated end to end — the strongest single result

**What was done.** A precision 100 MΩ resistor was clipped in where the tip and the sample would
be, making a junction of exactly known resistance. The bias was stepped through eight settings and
the converter read several times at each. If every stage works, the reading must be proportional
to the voltage, with a slope fixed by the two resistors and the converter's scale — a number that
can be worked out before the measurement.

**The result. MEASURED 2026-09-16** (`sessions/2026-09-16-bench.md` §3.4):

| | |
|---|---|
| Predicted, before the measurement | **−3,200 counts per volt** |
| Measured | **−3,205 ± 37 counts per volt** |
| Agreement | **0.13 standard errors** |
| Fit quality | **R² 0.993** |
| Readings | **53**, at 8 bias settings |

**Re-derived twice at this pause point, independently, from the 53 individual readings**: slope
−3,204.8 ± 36.5, intercept +58.0 ± 45.3, R² 0.9934, residual scatter 320 counts per reading. Both
re-derivations match the session log digit for digit
(`deliverables/2026-09-19-pause/LEAD_VERIFICATION.md` V1;
`deliverables/2026-09-19-pause/analysis/FINDINGS.md` §1).

**What that proves.** Fifteen things had to be right at once for those readings to land on that
line: the bias converter, the buffer, the wire, the known resistance, the tip holder, the tip
lead, the standoff, the amplifier, the cable, the converter, the firmware and the PC tools. **A
fault anywhere would have shown as points off the line.** It also settles the sign — a positive
voltage on the sample gives negative counts — which matters, because a current that drove the
reading the unexpected way would make an automatic approach drive the tip into the sample.

**Three limits on it, all of which must travel with the claim:**

1. **The slope is really a ratio of two resistors**, the dummy and the feedback resistor, both
   nominally 100 MΩ. **Neither tolerance is recorded.** So the agreement confirms the scale *to
   within those two tolerances*. If both are 5% out in the same direction the agreement is
   preserved and the absolute current scale is 5% out. **It is substantially a measurement that
   the two resistors match each other.** The qualitative result — that the whole current path
   works end to end — is unaffected by that.
2. **53 readings are not 53 independent tests.** They are repeated reads at eight settings, about
   1.4 s apart. **The independent unit is the setting, n = 8** (three of which are the same 0 V
   point revisited). Nobody should quote "53 measurements" as 53 independent confirmations.
3. **The 320-count scatter per reading is not a noise figure.** It was taken with the shield open
   and crocodile clips on the input node. It is about 25 times the quietest capture of the same
   session.

**Figure:** `deliverables/2026-09-19-pause/figures/png/fig01_calibration.png`. The straight line on
it is not fitted — it is what Ohm's law through 100 MΩ requires.

### 3.2 The amplifier resolves picoamps

**MEASURED 2026-09-15.** In its assembled copper box, on its screws, at ±15 V, the output sat at
−0.4 mV against ground, which through the 100 MΩ feedback resistor is **about 4 pA of input
current** — 250 times inside the limit the project set itself. Part of that 0.4 mV is the
amplifier's own input offset *voltage*, which does not divide by 100 MΩ, **so the true input
current is at or below 4 pA.** The reading was identical at 20 and at 45 minutes.

**This is the part that blocked the project for two weeks, and the reason is worth keeping.** The
fabricated boards were missing a ground pour that the original design has, so the amplifier's own
reference pin was connected to nothing on both boards. **Every amplifier measurement taken before
14 September was referenced to a floating node and was therefore meaningless.** The repair was four
wires onto a board 20 mm long. **The older "119 nA offset" figure is not a valid current** and is
recorded that way in `docs/FACTS.md`: the voltage was real, the current was never measured.

### 3.3 The electronics noise floor, and what it excludes

**Every noise number in this project belongs to a night and a tip. They are not interchangeable,
and mixing them has already caused confusion.** Each figure below therefore carries its date and
its conditions.

**MEASURED 2026-09-17, tip clear and with a junction** (`sessions/2026-09-17-bench.md`, the noise
spectroscopy that redirected the project):

- **With no junction, the chain is flat white noise at 8 to 14 counts** from 2 Hz to 1.2 kHz —
  the signature of a clean measurement path.
- **Bring a junction into existence and about 350 counts appear at 5 Hz**, falling away by 60 Hz.
- **There was no peak at 60 or 120 Hz that night**, and nothing at 1.2 kHz, so it was neither
  mains pickup nor the digital side.

**Noise that lives between 5 and 20 Hz and exists only when something is nearly touching is
mechanical.** That single chart redirected the whole project, away from the electronics and toward
the mechanics.

**MEASURED 2026-09-19, tip clear, on the tip fitted at about 03:00 that morning**
(`sessions/data/2026-09-19-bench/still.csv`, 34,746 readings over 10 s; recomputed for figure 6):

| | |
|---|---|
| Reading scatter, room still | **41.8 counts** (about 131 pA) |
| Reading scatter, someone stamping on the floor about two metres away | **42.3 counts** |
| What is left in the spectrum | **sharp lines at 60 Hz and its odd harmonics** — 5.2, 2.9 and 2.6 counts per root hertz at 60, 180 and 300 Hz still; 6.0, 2.5 and 2.5 while stamping |
| With a junction and X held (three-Y control, same night) | **9 to 19 counts** |

**Two findings come out of that pair, and both are worth stating outright.**

1. **The building is not getting into the measurement electrically. The still and stamping records
   are indistinguishable** — 41.8 against 42.3 counts, with the spectra lying on top of each other.
   **That is a clean negative result and it narrows the search** for what moves the gap: footsteps
   are not arriving through the mains, the cabling or the ground.
2. **What noise remains is mains pickup on a few sharp lines, not a limit of the amplifier.** Sixty
   hertz and its odd harmonics are the signature of pickup — a wiring and grounding problem, which
   is a class of fault with known remedies. **DERIVED from the line structure; no fix has been
   tried or measured here**, so that is a route, not a result.

> **The scope limit on both, stated because the page-facing version of this has omitted it.**
> **A tip-clear measurement has no junction in it.** Nothing mechanical can reach the amplifier
> through a gap that does not exist. So this pair tests **electrical pickup only.** It says nothing
> about whether footsteps move the gap — which is a different question, and the one that actually
> blocks imaging. **The stamp test that would answer that needs a junction, and it has not been
> run.**

**The 341 to 350 counts measured on 2026-09-18 belong to that night and that tip**, and are stale
for any later one. Several PC tools still quote older figures; updating them is on the fix list.

**Figure:** `deliverables/2026-09-19-pause/figures/png/fig06_noise.png`.

### 3.4 A real junction, and what its current-voltage curve does and does not establish

**MEASURED 2026-09-17** (`sessions/2026-09-17-bench.md` §3.15), taken as **eight rounds with the
bias polarity interleaved**, so that slow drift could not manufacture a slope:

| | |
|---|---|
| Current at 0.05 V | **0.85 nA** |
| Current at 0.5 V | **31.7 nA** |
| Effective resistance | **59 MΩ falling to 16 MΩ** as the voltage rose |
| Current ratio over a 10× voltage ratio | **37.3×** — ohmic would be 10× |
| Shape | **superlinear, and symmetric in both polarities to about 10%** |

**Confirmed independently by a bias-flip test on two separate nights**: reverse the voltage on the
sample and the reading reverses sign at about the same size. **Noise does not do that**, and the
test rejected two false contacts and confirmed the real one.

**A correction made at this pause point.** `sessions/2026-09-17-bench.md` reads the shape as
"roughly V²". **Refitting the six tabulated points gives V^1.55** (log-log R² 0.985). A pure
square law predicts 85 nA at 0.5 V where 31.7 nA was measured — a factor of 2.7, not a rounding
difference. **The error never propagated**: every live document says only "superlinear", which is
right. **Use V^1.55, or say "superlinear" and stop.**

**What this curve establishes, robustly:**

- **It is not a metallic short.** A short is ohmic; the resistance here falls by 3.7× across the
  sweep.
- **It is not an open circuit.** There are tens of nanoamps.
- **Drift cannot have made it**, because the polarities were interleaved.
- **It reverses with the bias**, on two separate nights.

**What it does NOT establish, stated plainly and once:**

- **That the gap is vacuum.** A contaminant film, a thin oxide or a dirty near-contact are all
  superlinear too. Tunnelling implies a barrier; a barrier does not imply tunnelling.
- **16 to 59 MΩ is at the LOW end for STM tunnelling**, which usually sits from about 100 MΩ up.
  It is still roughly a thousand times above the conductance quantum, so it is not a point contact
  either — but it is nearer contact than a textbook tunnelling junction.
- **At these biases an ideal vacuum junction should be closer to ohmic than this.** Measured
  superlinearity of V^1.55 is stronger than the near-linear behaviour a clean vacuum barrier gives
  well below the barrier height, which points at a barrier that is not clean vacuum.

**Figure:** `deliverables/2026-09-19-pause/figures/png/fig02_iv_curve.png`.

### 3.5 The distance test, on a different tip and a different sample

**MEASURED 2026-09-19 morning** (`sessions/2026-09-19-morning.md` §3.10–3.11; 110 cycles at four
bias settings, in nine minutes, on the tip fitted at about 03:00 that morning after the previous
one was found bent, and on the leaf-on-paper gold):

| | |
|---|---|
| Distance for the current to change tenfold, going in, sample −0.5 V | **a decade per about 1,650 and 1,970 Z counts** (per-run medians, 30 and 20 cycles) |
| At the other biases | **808 to 4,639 counts per decade** |
| What a vacuum tunnelling gap would need | **about 6 to 13 counts** — and **that comparison rests on an ASSUMED Z scale**, inherited from a similar disc, never measured on ours |
| In/out hysteresis | **705 to 1,868 counts** (per-run medians), in **every** run; 99 of 109 cycles positive. **This does not depend on the Z scale** |
| Onset shape | **gradual in 109 of 110 cycles**; one single-step snap |

**The hysteresis does not shrink at low bias.** At ±0.1 V the run medians are 1,653 and 1,474
against 1,162, 1,868 and 705 at ±0.5 V. **An electrostatic pull-in would scale as the square of
the voltage and predict about 25 times less.** It did not happen.

**The interpretation on record is "a soft, pressed, sticky contact" — and it is marked as
interpretation, not proof.** The contact potential between our tungsten tip and gold has never
been measured, so an electrostatic explanation is not excluded.

**Figure:** `deliverables/2026-09-19-pause/figures/png/fig05_ztest.png`. **It carries no distance
scale, because this instrument has never established one from its own hardware.**

**This does not contradict section 3.4.** Different tip, different sample, different night.
`docs/FACTS.md` says so in the section heading itself: *for this tip and this sample only*.

**So the honest statement, which is the one to use everywhere:**

> An I-V curve taken on the 2026-09-17 junction has the non-ohmic, bias-symmetric shape a
> tunnelling barrier requires, and rules out both a short and an open. A separate Z-distance test
> on a **different** tip and sample two nights later did **not** show the steep response a clean
> tunnelling gap requires, and was interpreted as a pressed contact. **The project has evidence of
> a barrier junction; it has not demonstrated a stable vacuum tunnelling gap, and it has never
> produced an image.**

### 3.6 The rest of the chain

- **Coarse approach finds the surface.** The motor, driven in 20-step chunks, found the gold twice
  on 2026-09-19 (at 200 and 180 steps). **Neither find gave a usable gap** — see section 5.
  Direction was settled at the bench on 2026-09-17: negative approaches.
- **The feedback loop works, within its limits.** It holds current to about 0.06 of a decade at
  2,000 pixels per second, and 5, 15 and 250 corrections per pixel all agree (MEASURED
  2026-09-17). **The loop tuned for the 2026-09-19 junction never held on hardware that day** —
  every tuned image aborted at a clamp — which is consistent with a junction whose constant drifted
  about fivefold inside a single run.
- **Two ways to destroy a tip were found in the software before any tip was fitted**, both
  inherited from the original design, both fixed and both tested by deliberately reproducing them
  first.

---

## 4. How we tested ourselves — and this is a result, not a formality

**The reason nobody in this project has fooled themselves is that every imaging claim was run
against a control designed to kill it.**

**What an X-held control is.** Re-run a scan with identical timing, identical loop behaviour and
identical numbers of points — but **X never moves**. The tip does not travel across the surface.
**A control therefore contains no sample structure at all, by construction.** Anything that turns
up in both a scan and its control is the instrument talking to itself.

**It repeatedly beat the result it was controlling, which is exactly what a control is for:**

| Comparison | Real scans | Their X-held control |
|---|---|---|
| ±400 line-position agreement, 2026-09-17 (102 lines against 8) | **−0.069 ± 0.049** | **+0.170 ± 0.118** |
| ±400 corrugation (the size of the "structure") | 29 to 43 counts | **87 counts** |
| ±1,500 line-position agreement, 2026-09-19 (44 lines against 34) | −0.066 ± 0.137 | −0.053 ± 0.144 |
| The three-Y "is this the surface?" statistic, permutation test | best real run: **p = 0.0036** | **an X-held control: p = 0.020** |

**Read the last row.** A measurement containing nothing scored p = 0.02 on the project's own
"is this the surface?" statistic. **That is the empirical false-positive rate of this measurement
on this instrument**, and knowing it is worth more than any single positive would have been.

**And the searching was budgeted.** 201 reproducibility tests have been run across this data. At
that many, a 5% threshold is expected to throw up about ten apparent findings from noise alone, so
the honest threshold is **p < 2.5 × 10⁻⁴**, about 3.7 standard deviations. **Nothing in this body
of data reaches it as evidence of a surface** — and the threshold was computed before the
candidates were judged.

**Two traps this project found and then generalised:**

1. **The first-line trap.** A promising agreement of +0.75 between two images was the feedback
   loop's settling transient on the first line of each — the same *procedure*, not the same
   sample. Dropping that line took it to +0.04. Reproduced on five separate 2026-09-17 groups at
   this pause point: +0.70 → −0.08, +0.75 → +0.04, +0.62 → −0.29, +0.71 → −0.45, +0.38 → −0.26.
2. **The first-*pixels* trap, found at this pause point.** The same idea, one level down — see
   section 7.

**Figure:** `deliverables/2026-09-19-pause/figures/png/fig04_control.png`.

**What the imaging record says, stated once and plainly.** Fifty-one recordings were examined at
this pause point — every raster scan, line repeat, three-Y run and control in the project.
**No scan contains a demonstrable image of the sample.** The cleanest comparison, four feedback
scans each with its own control taken on the same night with the same tip, gives, like for like
over full images: **scans +0.09, +0.18, −0.15 (mean +0.04); controls +0.20, −0.06 (mean +0.07).
Neither group reproduces, and neither differs from zero.** The scans show no more reproducible
structure than a control in which the tip never moved across the surface.

---

## 5. What we found in the way — measured, not guessed

**This is the project's central negative result, and it is the most useful thing in it.**

**MEASURED 2026-09-19 morning**, with the motor stopped, nobody touching the instrument, and only
the Z piezo sweeping to look for the surface (`release_watch_run1.log`, nine sweep events, the
whole record — the CSV was lost because the script wrote its rows only on a clean exit):

| | |
|---|---|
| Gap movement in 6.4 seconds | **more than 43,000 Z counts** |
| Gap movement over about two minutes | **more than 56,000 counts** — most of the Z range |
| During scans, with X, Y and Z being driven | **more than 48,000 counts in 33 seconds** |
| Resolution of these onsets | 1,000 counts — irrelevant at this size, but it limits any fine claim from the same files |
| Independent record, different tip and night | onsets ranged 7,250 to 44,250 counts over 90 seconds, motor still (mean 24,067, sd 7,563, 249 onsets) |

**The honest caveat, which is not in the original write-up and should be.** The 6.4-second
excursion begins 0.1 s after a 60-step motor move finished, so **post-move mechanical relaxation
cannot be excluded for that one event.** It does not carry the result: **the motion reverses
direction and overshoots its own starting point** — settling and creep decay one way — and the
two-minute figure is measured from 6.4 s to 111 s, well clear of any fast transient. **Post-move
relaxation should be a fifth candidate cause** alongside the four already on record: the leaf on
its backing paper, the plate on its rubber bands and ball contacts, thermal motion of the printed
parts, and air currents.

**Why this ends the imaging question, in one comparison:**

| | |
|---|---|
| How much the gap drifts over the time one image takes (about 5 s) | **396 to 1,722 counts** (scatter across five runs after removing steady drift) |
| How big the "structure" in every candidate image is | **29 to 458 counts** (21 files) |

**The thing being measured is smaller than the way the gap moves while it is being measured.**
That single comparison explains the entire imaging record, and it is a number, not an impression.

**A real property of the scanner was found on the way.** In the wide images, the forward and
backward sweeps of each line are −0.85 to −0.92 correlated at zero offset and +0.83 to +0.93 at an
offset of about ten pixels — a signal roughly periodic over one pass and mirrored between the two
scan directions. **The X-held controls, identical timing, show nothing of the kind at any offset.**
So **X motion is required to produce it**, which upgrades "X motion is the likely but unproven
cause" to a control-backed statement. **It is not an image**: a surface gives the same height at
the same place whichever way the tip is travelling. Three explanations are consistent with it and
none has been tested — the loop hunting, the X drive coupling into Z, or **the tip dragging a
compliant sample**, which would be the first direct measurement of the gold leaf's softness.

**Figure:** `deliverables/2026-09-19-pause/figures/png/fig03_gap_motion.png`.

---

## 6. What was ruled out, and by what number

**The false trails in this project have been as valuable as the results.** Recording what was
eliminated, with the measurement that eliminated it:

| Suspect | Verdict | The number that decided it |
|---|---|---|
| Amplifier and electronics noise | **Eliminated** | Flat white, 8 to 14 counts across the band, 2026-09-17 |
| Leakage through the tip lead or holder | **Eliminated** | Under 0.06 nA from −2 V to +2 V with the tip retracted — more than 8 GΩ, 2026-09-17 |
| Mains hum at 60 or 120 Hz | **Eliminated** | No peak at either frequency with a junction present, 2026-09-17; line content 10 counts on 2026-09-19 |
| The feedback loop mistracking | **Eliminated** | Holds current to about 0.06 of a decade at 2,000 pixels a second, 2026-09-17 |
| The operator sitting at the bench | **Eliminated** | Under 1% of the noise, 2026-09-17. **Leaning over the board is a different matter and the rule stands** |
| The sample-plate magnets moving the gold | **Eliminated by arithmetic** | Gold is diamagnetic; even at 0.5 T and 1,000 T/m the force reaches 7% of the leaf's own weight |
| The sample-plate magnets making the noise | **Eliminated by arithmetic** | A vibrating input loop in that gradient gives about 0.0063 pA against a 1,000 pA signal |
| Building vibration arriving **electrically** | **Eliminated, cleanly** | Still 41.8 counts against stamping 42.3, spectra lying on top of each other, 2026-09-19. **A real negative result: footsteps are not coming in through the mains, the cabling or the ground** |
| Building vibration **moving the gap** | **Untested** | The same pair had the tip clear, so there was **no junction** for vibration to act on. **The test that would answer it needs a junction and has not been run** |
| A periodic disturbance a scanner could be synchronised to | **None found, and none excluded** | No coherent spectral line in four long fixed-point records; the one line found, 63.6 Hz, is in a tip-clear control and is electrical. **The timescale on which the gap actually moves is covered by no record we have** |
| The reproducible 636-count profile — the project's best candidate image | **Closed, with a mechanism** | See section 7 |

---

## 7. What we corrected in our own record at this pause point

**Six things. Every conclusion survived. Two of the arguments for them did not.** This section is
here because it is a result: **the errors were found from the inside, by replicating the numbers
rather than reading them, before anything went on a poster.**

### 7.1 Two dismissal statistics were withdrawn — both from the same silent bug

**A scan that aborts leaves a file that still parses.** It has a header, valid rows and plausible
numbers; it is simply short. The comparison script truncated both images to the shorter one, with
no shape check and no warning.

**(a) "The controls reproduce better than the scans, +0.37 against +0.04" is WITHDRAWN.** One of
the four control files is **a single scan line**, not an image — the run aborted after line one,
where the other seven files carry eleven. **Two of the three control correlations were therefore
computed over 21 points instead of 231**, comparing one line against another image's first line.
**Like for like, full images only: scans +0.04, controls +0.07. Indistinguishable, and neither
differs from zero.**

**(b) The wide images' "+0.56 to +0.86 image to image" is WITHDRAWN, and it is worse.** Two of the
three wide scans aborted — one holds a single line, one holds two — so those figures are 21- and
42-point fragment correlations and **neither was an image-to-image correlation at all.** With only
one complete real wide image, **there is no valid reproducibility figure for the wide scans.** The
controls' +0.56 over 231 points **is** sound, and is a real result: **with X held, the instrument
repeats its own pattern strongly**, which is a measurement of the instrumental signature.

**Neither correction resurrects an image, and that should be unambiguous.** The real scans still do
not reproduce, over full images, with no correction needed. **The right statement is simpler and
needs no repair to be believed:** neither the scans nor the controls reproduce.

**The general lesson, worth more than either instance:** every comparison in this project flattens
an image and correlates it, and **flattening destroys the shape information that would have caught
this.** The fix is one line — refuse to compare two images of different shape — and it is in the
priority list in `PAUSE_POINT_HANDOFF.md`.

### 7.2 The project's best candidate image is closed, with a mechanism

**Open since 2026-09-17 as UNDETERMINED**: twelve passes of one line at ±15,000 X gave a
reproducible 636-count profile — consecutive-pass agreement about +0.5 to +0.65, split-half +0.92,
and p < 2 × 10⁻⁴ against phase-randomised surrogates. **All of that is true. It is genuinely
reproducible and it is not noise. It is also not the sample.**

**The arithmetic:**

| | |
|---|---|
| Tilt of the twelve passes | **−0.105 Z counts per X count** |
| X jump back to the start of each pass | **30,000 counts** |
| **Z error the loop must therefore recover at every pass start** | **3,144 counts** |
| Observed recovery over the first two pixels | **about 2,470** |
| **Agreement between passes after dropping two pixels of twenty-one** | **+0.65 → +0.05** |

**The same arithmetic predicts the effect's ABSENCE, twice.** The two 2D wide images of the same
night sweep back and forth without lifting X, so there is no jump: predicted small, observed 37 and
78 counts. The 2026-09-19 three-Y runs do jump back but are nearly level: predicted 28 and 238
counts, observed −99 and +47. **One piece of arithmetic, three data sets, right about the presence
and right about both absences. That is a falsification, not a null.**

**And the check already existed in this repository, one level up.** The 2026-09-17 session killed
an agreement of +0.75 by dropping the first *line* of an image. **Nobody had applied it to the
first *pixels* of a line.** The credit belongs to whoever wrote that section; what was missing was
one step of generalisation.

### 7.3 The "3.9 sigma" on the three-Y result was overstated — in both directions

The measurement that has come closest to looking like topography — one place on the sample looking
more like itself than like a place 12,000 Y counts away — was reported on the night as 3.9 standard
deviations. **The data are sound: every file is 3 places × 6 passes × 21 points, no truncation, and
all five published numbers reproduce exactly.** But that sigma treats 45 within-place and 108
between-place comparisons as independent when every pass appears in many of them.

**Under 20,000 permutations of the place labels: the positive run is p = 0.0036** — a factor of 14
short of the corrected threshold — **its repeat half an hour later is p = 0.26, and an X-held
control, which cannot contain a surface, scores p = 0.020 on the same statistic.**

**This one cannot be settled with the data that exist**, and that is stated as a limit rather than
buried: the two runs are half an hour apart, and in between the gap demonstrably moved by most of
the Z range. **"It did not repeat" and "the surface moved out from under it" are not
distinguishable here.** It is the strongest form of the hypothesis that a real image was dismissed,
and **it is not refuted.** It has a four-image test, which is the top scientific priority in
`PAUSE_POINT_HANDOFF.md`.

### 7.4 A question recorded as never answered had in fact been answered — by our own data

The 2026-09-17 log records that the experiment which would settle its best candidate **had not been
run**. It had been: two complete images of the same nine places on the same grid were sitting in
the same directory the whole time. **They were missing from that directory's index file, which is
the only listing of it**, and that is the likeliest reason nobody knew. (Result: same place
+0.216 ± 0.228, different place +0.074 ± 0.063, permutation p = 0.24 — **and with nine pairs that
test can only exclude a difference bigger than about +0.47, so a weak genuine signal is not
excluded by it.** What closes that candidate is the mechanism in 7.2, not this null.)

**This is the fifth time in this project that something recorded as unknown was already answered by
a file in the repository.** Four files were missing from one index. That is a cheap fix and it is in
the handoff.

### 7.5 The conflict register had the project's most expensive error recorded backwards

`docs/ENGINEERING_REFERENCE.md` §11 is the one place in the project whose job is to say which of two
conflicting sources won. Its row on the converter's input span said **"Resolved: 4.096"** and that
the PC tools had not yet been changed. **Both halves were wrong: the span is 10.24 V** — 4.096 V is
the reference buffer and the span is 2.5 times it — **and the PC tools had already been changed**,
with the reason written in the code. Corrected in place, old text struck through.

**This is the correction that `docs/FACTS.md` exists because of**, and **one of the stale copies was
the conflict register itself.** The automatic checker could not see it, for a reason worth knowing:
it suppresses a hit when the corrected value appears on the same line, and **a conflict row names
both values by construction** — so it is blind in exactly the document type where a wrong
resolution does most damage. That is now recorded as a known limit rather than patched, because
tightening it risks a checker that cries wolf, and **a checker that fires on correct lines gets
switched off.**

### 7.6 The V² reading of the I-V curve was wrong; it is V^1.55

Covered in section 3.4. **It never propagated** — every live document says only "superlinear".

### 7.7 Two checker over-firings were found and fixed

Both were the same class: **a retired value that is also a substring of innocent text.** One was an
English phrase matching a sentence about a power supply; one was a number matching inside a larger
number. Both fixed at the source during this work. **The rule they demonstrate is now commented at
both sites in the checker**: when a value is retired, check whether its text is a substring of
ordinary English or of a bigger number, **and then confirm the check actually fires** against a
deliberately reintroduced stale line.

---

## 8. What is still open

**Canonical home: [`docs/OPEN_QUESTIONS.md`](../../../docs/OPEN_QUESTIONS.md).** This is a summary
of the ones that matter most to the science, not a second list.

1. **What moves the gap.** Five candidates, none tested: the leaf on its backing paper; the plate
   on its rubber bands and three ball contacts; thermal motion of the printed parts; air currents;
   and post-move mechanical relaxation. **A cardboard box over the instrument is the free first
   test.**
2. **The Z scale in nanometres is ASSUMED, not measured.** Every distance statement in counts is
   scale-free and safe; every statement in nanometres inherits a figure from a similar disc. **The
   hysteresis result does not depend on it. The "counts per decade" comparison does.**
3. **The tip-to-pivot-line distance**, which sets the lever ratio and therefore the Z scale, has
   never been measured. `docs/OPEN_QUESTIONS.md` calls it *the most valuable unmeasured number in
   the instrument*, and it needs a straightedge, not electronics. **It cannot be measured from
   photographs** — three attempts gave answers more than a factor of two apart.
4. **Whether the tip was ever over gold rather than copper.** The sample's window is not all gold;
   copper is exposed to the gold's left and below it in the photograph of the plate. Nothing
   electrical distinguishes them.
5. **The three-Y candidate** (section 7.3), which has a specific four-image test.
6. **The mechanism of the mirrored signal in the wide images** (section 5), which has a specific
   two-speed test.
7. **Whether the rebuilt preamp box shield is continuous.** The repository contradicts itself and
   no shield in this project has ever been metered end to end. **Two minutes with a meter settles
   it.**
8. **What was taken apart in the move and how it was packed.** The photographs show the teardown up
   to 10:16 — leads off, boxes open, **the platform lifted off the frame as one piece with the head,
   motor and preamp still on it.** **No frame shows anything going into a box.**

---

## 9. Where this goes next

**The full ordered plan, written to be executed with no memory of any conversation, is
[`PAUSE_POINT_HANDOFF.md`](PAUSE_POINT_HANDOFF.md) in this directory, and the canonical bench
procedure remains [`docs/NEXT_SESSION_PLAN.md`](../../../docs/NEXT_SESSION_PLAN.md).**

In one paragraph: **reassemble and re-verify before any power; then prove the gap holds still, for
free, before spending any effort on imaging.** Three software fixes cost nothing and can be done
while the instrument is still in its box — they remove the artefact that produced this project's
most convincing false positive. **Everything else waits on the gap holding still, because every
imaging statistic is currently dominated by the gap moving more than the signal.**

---

## 10. What this report does not claim

- **No tunnelling.** We have a barrier junction. We have not demonstrated a stable vacuum
  tunnelling gap.
- **No image.** Fifty-one recordings, no demonstrable image of the sample, and we know that from
  our own controls.
- **No atomic resolution**, and no scale bar anywhere in these deliverables, because no image in
  this project has a known scale.
- **No number taken off a photograph.** Every photographic caption in these deliverables is marked
  `SAID` or `READ`, and no dimension has been measured from any frame.

**"We got extremely close" is what the evidence supports. An honest limitation, stated
confidently, survives the first hard question from someone who knows what an STM is. An overclaim
does not, and it would take the rest of the work down with it.**
