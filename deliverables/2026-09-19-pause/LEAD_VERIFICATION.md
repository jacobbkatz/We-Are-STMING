# Lead verification log

**The lead's own checks, run independently of the subagents.** Nothing here is taken from an
agent's summary. Where an agent later reports the same quantity, this file is what its number is
checked against, not the other way round.

Each entry says what was checked, how, what came out, and whether the project's existing claim
survives.

---

## V1. The end-to-end calibration — the project's strongest single result. **VERIFIED**

**The claim, from `docs/FACTS.md` and `sessions/2026-09-16-bench.md` §3.4:** a 100 MΩ dummy junction
clipped between the bias wire and the tip holder gives **−3,205 ± 37 counts per volt against −3,200
predicted**, **320.5 counts per nA**, **R² 0.993**, across 53 readings.

**How I checked it.** There is **no CSV for 2026-09-16** — `sessions/data/` starts at 2026-09-17 —
so the eight-row table in the session log is the primary record. I transcribed all 53 individual
readings out of that table by hand and refit them from scratch, with my own least-squares code, in
the lead scratchpad. This was done before Subagent 1 reported anything.

| Quantity | Session log | My independent refit | Agrees |
|---|---|---|---|
| Slope, counts per volt on the bias wire | −3,205 ± 37 | **−3,204.8 ± 36.5** | yes |
| Counts per nA | 320.5 | **320.5** | yes |
| Intercept | +58, about 1.3 standard errors from zero | **+58.0 ± 45.3, 1.28 SE** | yes |
| R² | 0.993 | **0.9934** | yes |
| Residual scatter per reading | 320 counts | **320 counts** | yes |
| Ratio to the predicted −3,200 | 1.0016 | **1.0015** | yes |
| Every group mean within | 1.4 standard errors | **worst is 1.29 SE**, at +0.711 V | yes |

**n = 53, and they are NOT 53 independent observations.** They are repeated `ADCR` reads at eight
bias settings — five to ten reads per setting, about 1.4 s apart. The independent unit here is the
**bias setting, n = 8** (of which three are the same 0 V point revisited). The slope's standard
error is computed from the scatter of individual reads, which is the right thing for the fit, but
nobody should quote "53 measurements" as 53 independent tests of the chain.

**The 0.13 sigma figure on `docs/showcase.html` is also correct.** (−3,204.8 − (−3,200)) / 36.5 =
**0.13**. That claim survives.

### What this does NOT establish, and the session log already said so

**The slope is the ratio of the feedback resistor to the dummy resistor**, both nominal 100 MΩ,
divided by the volts per count. **Neither resistor's tolerance is recorded.** So the agreement to
0.16% confirms the scale *to within those two tolerances* — it is substantially a measurement that
the two resistors match each other, not an independent confirmation of 320 counts per nA. A pair of
5% resistors that happen to be cut from the same reel would produce exactly this result.

**This is a real limit on the headline claim and it must appear wherever the claim does** — poster,
report and showcase alike. It does not weaken the qualitative result, which is that **the entire
current path works end to end**: bias DAC, buffer, wire, a known resistance, tip holder, tip lead,
standoff, preamp, cable, converter, firmware and PC tools. That is unaffected by resistor tolerance.

**The 320-count residual scatter is not a noise figure.** Cover off, clips and a jumper on the input
node. It is about 25× the quietest capture of that session.

**Reproduce:** the transcription and fit are in
`deliverables/2026-09-19-pause/analysis/` only if Subagent 1 also did it; my own copy is a
scratchpad script, and the 53 numbers themselves are in `sessions/2026-09-16-bench.md` §3.4, which
is the durable record. Anyone can redo this from that table in ten minutes.

---

## V2. The I-V curve: **the "roughly V²" reading is wrong. It is V^1.55.** Everything else holds

**The claim, `sessions/2026-09-17-bench.md` §3.15, round 7 of eight interleaved-polarity rounds:**
six points from 0.85 nA at 0.05 V to 31.7 nA at 0.5 V, junction resistance falling 59 to 16 MΩ,
*"symmetric in both polarities to about 10%, and superlinear: the current goes as roughly V^2."*

**I refit the six tabulated points** (transcribed by hand; no CSV for this measurement exists in
`sessions/data/`, so the log table is the primary record).

| Quantity | Session log | My refit | Verdict |
|---|---|---|---|
| Power-law exponent | *"roughly V^2"* | **V^1.55**, log-log R² 0.985 | **the log is wrong** |
| Resistance range | 59 to 16 MΩ | **58.8 to 15.8 MΩ** | holds |
| Current ratio over a 10x voltage ratio | — | **37.3x** (ohmic would be 10x) | holds |
| Showcase's *"about four times faster than Ohm's law"* | — | **3.73x** | **correct** |

**How far out V² is: a pure V² law predicts 85 nA at 0.5 V against the 31.7 nA measured** — a factor
of 2.7. This is not a rounding difference. **V^1.5 predicts 26.9 nA, which is close.**

**The error did NOT propagate, and I checked.** `grep` across every live document finds "V^2" only
in `sessions/2026-09-17-bench.md` (lines 368 and 741). `STATUS.md`, `docs/NEXT_SESSION_PLAN.md` and
`docs/showcase.html` all say only **"superlinear"**, which is right. **Session logs are history and
`CLAUDE.md` §3bb forbids rewriting a past measurement, so the log stays as written** — but nothing
downstream may reach into it for "V²", and the poster and report must use **V^1.55** or say
"superlinear" and stop.

---

## V3. Does the I-V curve establish a tunnelling gap? **It establishes a barrier. That is not the same claim**

This is the conclusion most likely to be overstated on a poster, so it gets stated carefully.

**What the curve does establish, robustly:**

- **It is not a metallic short.** A short is ohmic; resistance here falls by 3.7x across the sweep.
- **It is not an open circuit.** There are tens of nanoamps.
- **Drift cannot have manufactured it.** Eight rounds with the polarities interleaved.
- **It reverses with the bias**, confirmed by a bias-flip test on two separate nights. Noise does
  not do that.

**What it does NOT establish:**

- **That the gap is vacuum.** A barrier can be a contaminant film, a thin oxide, or a dirty
  near-contact, and all of those are superlinear too. "A barrier junction is what tunnelling is",
  as the session log puts it, is a step too far: tunnelling implies a barrier, not the reverse.
- **16 to 59 MΩ is at the LOW end for STM tunnelling**, which usually sits from about 100 MΩ up.
  It is still roughly a thousand times above the conductance quantum, so it is not a point contact
  either — but it is nearer contact than a textbook tunnelling junction.
- **At these biases an ideal vacuum junction should be closer to ohmic than this.** Simmons' model
  gives I proportional to V plus a small cubic term for V well below the barrier height. Measured
  superlinearity of V^1.55 is stronger than that, which points at a barrier that is not clean
  vacuum.

### The tension that the poster and the report MUST handle explicitly

**`docs/showcase.html` answers "Is there really a quantum junction at the tip?" with "Yes".** That
was written from the **2026-09-17 junction**. The **2026-09-19 morning Z test concluded the
opposite** — *"not a clean tunnelling gap"*, a decade of current per ~1,650 to 1,970 Z counts where
tunnelling would need ~6 to 13, with the interpretation *"a soft, pressed, sticky contact"*.

**These are not a contradiction, and neither supersedes the other, because they are different
junctions.** Different tip (the 2026-09-19 tip was fitted at ~03:00 that morning, after the previous
one was found bent), different sample (the leaf-on-paper gold), different night.
**`docs/FACTS.md` says so in the section heading itself: "For this tip and this sample only."**

**So the honest statement, which is what the deliverables must carry:**

> An I-V curve taken on the 2026-09-17 junction has the non-ohmic, bias-symmetric shape a tunnelling
> barrier requires, and rules out both a short and an open. A separate Z-distance test on a
> **different** tip and sample two nights later did **not** show the steep exponential a clean
> tunnelling gap requires, and was interpreted as a pressed contact. **The project has evidence of a
> barrier junction; it has not demonstrated a stable vacuum tunnelling gap, and it has never
> produced an image.**

**Nothing in the deliverables may say "tunnelling achieved" or "atomic resolution".** The
qualitative claim that survives everything is the one worth leading with: **the complete measurement
chain works, end to end, and is calibrated against theory.**

---

## V4. **"The controls reproduce better than the scans" rests on a truncated file.** The conclusion survives; this argument for it does not

**This is the most consequential thing I found, and it was found by replicating the numbers rather
than reading them.**

**The claim,** in `STATUS.md`'s top block and `sessions/2026-09-19-bench.md` §3.14:

> 4 feedback scans + 4 X-held controls: **the controls reproduce better** (image to image **+0.37**
> against **+0.04**).

An X-held control has no sample structure in it by construction — X never moves, so every apparent
feature is the instrument. If the controls reproduce *better* than the real scans, the real scans
contain nothing the instrument did not make. It is the strongest single argument in the imaging
case, and it would have gone on the poster.

### I reproduced both numbers exactly, and then found what makes them differ

| Group | Published | My replication | Points per correlation |
|---|---|---|---|
| Real scans | +0.09, +0.18, −0.15 (mean **+0.04**) | **+0.09, +0.18, −0.15** | **231, 231, 231** |
| X-held controls | +0.20, +0.21, +0.70 (mean **+0.37**) | **+0.20, +0.21, +0.70** | **231, 21, 21** |

**`sessions/data/2026-09-19-bench/cas9_xheld2.csv` is not an image. It is a single scan line** —
one `y` value, `fwd` and `back`, where the other seven files carry eleven. The run aborted after
the first line.

**Two of the three control correlations are therefore computed over 21 points, not 231**, because
the comparison silently truncates both images to the shorter one. They are not image-to-image
correlations at all: they compare one line against the first line of another image.

**The mechanism is in committed code**, `sessions/data/2026-09-19-bench/scripts/analyze_scans.py`
lines 50-51:

```python
n = min(len(fa), len(fb))
c = corr(fa[:n], fb[:n])
```

**No shape check, no warning, and the group mean folds 231-point and 21-point correlations
together.** The per-file line count *is* printed above the summary, so a one-line file was visible
on screen; the summary line is what nobody could have checked by eye.

### The like-for-like comparison

Dropping the one-line file and using only full images:

| Group | Correlations over 231 points each | Mean |
|---|---|---|
| Real scans | +0.09, +0.18, −0.15 | **+0.04** |
| X-held controls | +0.20, −0.06 | **+0.07** |

**+0.07 against +0.04. Indistinguishable.** With three and two pairs respectively, and individual
standard errors around 0.07, neither mean is distinguishable from zero or from the other. **The
comparison was never powered to support "better".**

### What changes, and what does not

**THE CONCLUSION "NO IMAGE" STANDS, and it does not need this argument.** The direct evidence is
that the real scans do not reproduce: +0.09, +0.18 and −0.15 scatter both sides of zero, over full
images, with no correction needed. That is sufficient on its own.

**What must change is the sentence.** "The controls reproduce better than the scans" is not
supported. The supported statement is stronger for being simpler:

> **Neither the feedback scans nor the X-held controls reproduce from image to image. The scans
> show no more reproducible structure than a control in which the tip never moved across the
> surface.**

**This does not resurrect an image**, and nobody should read it as doing so. It removes one
overstated argument and leaves the conclusion resting on the evidence that actually carries it.

**It does mean one stated reason for dismissing the scans was weaker than the record says** — which
is directly relevant to the hypothesis Subagent 2 is testing, and is why it is written down here in
full rather than quietly fixed.

### Actions taken

- `STATUS.md` corrected — the live document is what the next session reads first.
- Subagent 2 (candidate images) told, because this is central to its question.
- Subagent 7 (figures) told, because I had commissioned a figure built on "+0.04 against +0.37".
- The scratch script is **not** rewritten: `sessions/data/**/scripts/` is provenance, not a tool,
  and `CLAUDE.md` keeps session history as written. The defect is recorded here and in `STATUS.md`
  instead.

---

## V5. The same truncation reaches the WIDE images. I checked every data file's shape

Having found V4, I checked whether the min-length truncation is a class rather than one instance. It
is. **I listed the row count of every CSV in all four data directories.**

### Where it bites

**`sessions/2026-09-19-bench.md` §3.16, the wide constant-current images:**

> ±15000 X and Y, 21 × 11, three images and two X-held controls: **two of the three aborted on
> saturation** [...] Image to image **+0.56 to +0.86**, **matched by the X-held controls' +0.56**.

**The log states the aborts, but not that the correlations are computed across them.** The shapes:

| File | Shape | |
|---|---|---|
| `img_scan_0.csv` | **(1, 21)** | a single line |
| `img_scan_1.csv` | **(2, 21)** | two lines |
| `img_scan_2.csv` | (11, 21) | the only complete real image |
| `img_xheld_0.csv` | (11, 21) | complete |
| `img_xheld_1.csv` | (11, 21) | complete |

**My replication of the published figures:**

| Pair | r | Points | Like for like |
|---|---|---|---|
| `img_scan_0` vs `img_scan_1` | **+0.86** | **21** | no — 1 line against 2 |
| `img_scan_1` vs `img_scan_2` | **+0.56** | **42** | no — 2 lines against 11 |
| `img_xheld_0` vs `img_xheld_1` | **+0.56** | **231** | **yes** |

**So "+0.56 to +0.86" for the real wide images is two fragment correlations over 21 and 42 points.**
With only one complete real wide image, **there is no valid image-to-image reproducibility figure for
the wide scans at all.** The control figure, +0.56 over 231 points, is the only sound number in that
group — and it is a real result worth keeping: **with X held, the instrument repeats its own pattern
strongly.** That is a measurement of the instrumental signature, and it is good evidence.

### Where it does NOT bite — checked, not assumed

- **Three-Y controls**: `ycontrol_run1`, `run2_ysep12000`, `run3_..._xheld`, `run4_..._repeat`,
  `xheld_run1` — **all 18 rows × 23 columns.** Uniform. The +0.374 ± 0.097 and the +0.056 ± 0.094
  repeat are **not** affected by shape mismatch.
- **2026-09-17 bench**: files of the same kind match each other — `scan_fast_1..4` all 24 rows,
  `scan_slow_1/2` both 24, `diag_scan_normal_1/2` and `diag_scan_x_held` all 16. **That night's
  scan-versus-control comparison is like for like.**
- **2026-09-19 morning tuned scans** are ragged (`scan0` 1 line, `scan1` 8, `scan2` 9; `xheld0` 2,
  `xheld1` 8, `xheld2` 9) — **but the morning log reports them only qualitatively** ("the loop never
  held", clamped, climbing blind) **and quotes no correlation from them.** Nothing to withdraw.
- **Trace/retrace figures are unaffected everywhere**, because `fwd` and `back` live in the same
  file and always have the same shape.

### Propagation check

**"+0.56 to +0.86" appears only in `sessions/2026-09-19-bench.md`.** It is in no live document —
not `STATUS.md`, not `docs/`, not the showcase. So nothing downstream is wrong today. **The risk is
forward-looking**: a poster or paper would go to the session log for that number. Hence the pointer
now added to `STATUS.md`'s imaging row.

### The general lesson, which is worth more than either instance

**A scan that aborts leaves a file that still parses.** It has a header, valid rows and plausible
numbers; it is simply short. Every comparison in this project flattens images and correlates, and
**flattening destroys the shape information that would have caught it.** The fix for any future tool
is one line — refuse to compare two images of different shape, or state the shape beside every
correlation — and it is recorded in `deliverables/2026-09-19-pause/manual/` recommendations rather
than applied to the scratch scripts, which are provenance.

---

## V6. The gap motion — **the number is right; one alternative cause is missing from the list**

**The claim** (`STATUS.md`, `docs/FACTS.md`, `sessions/2026-09-19-morning.md` §3.9): with the motor
and hands still and only the piezo sweeping, the gap moved **≥ 43,000 Z counts in 6.4 s** and
**≥ 56,000 over about 2 minutes**. This is the central negative result and the poster's most
important figure.

**Verified from `release_watch_run1.log` line by line.** There is **no CSV** — it was lost because
the script wrote its rows only in `finally` and the task was killed (`sessions/data/2026-09-19-morning/README.md`
records this, and that four CSVs went the same way). The log is the whole record:

```
12:54:10 RELEASE: clear after 3 chunks (+60 steps)
12:54:10    0.1s FOUND onset Z 19000
12:54:13    3.2s FOUND onset Z 42000
12:54:16    6.4s FAR
12:56:01  111.1s FOUND onset Z 6000
```

**The arithmetic holds.** 19,000 → 42,000 → beyond the sweep top (62,000) is **> 43,000 counts in
6.3 s**. Beyond 62,000 → 6,000 at 111 s is **> 56,000 counts**. The "≥" is right, because FAR is a
lower bound: the onset was outside the sweep, not measured.

**Resolution is 1,000 counts, not 250.** `fastwood.sweep` bound its step as a default argument, so
every onset in these files is a multiple of 1,000. **Irrelevant at this size** — 43,000 against a
1,000-count quantisation — but it would matter for any fine claim from the same files.

### The caveat that is NOT in the record

**The 6.4 s excursion begins 0.1 s after a motor move ends.** The same log shows three release
chunks totalling **+60 motor steps** at 12:54:08-12:54:10, and the first onset is at 12:54:10.
`STATUS.md` says "with the motor and hands still", which is true *during* the window — but the
window opens immediately after the motor stopped.

**Post-move mechanical relaxation is the standard explanation for large drift in the first seconds
after a stepper move**, and it is **not among the four candidate causes on record** (the leaf on its
paper, the plate on its bands and balls, thermal motion, air currents). **It should be a fifth.**

### Why it does not sink the claim — and this is the interesting part

**The motion is not monotonic.** The onset goes **up** by more than 43,000 counts, then comes back
**down past where it started**, to 6,000 against the initial 19,000. **Settling and creep after a
move decay in one direction.** An excursion that reverses and overshoots its own starting point is
not that shape.

**And the ≥ 56,000 figure is measured from 6.4 s to 111 s**, which is well clear of any fast
post-move transient.

**So the honest form of the claim, which is what the deliverables should carry:**

> With the motor stopped and nobody touching the instrument, the gap moved by more than 43,000 Z
> counts within 6.4 seconds and by more than 56,000 within two minutes — most of the Z range. The
> fast excursion began seconds after a motor move, so post-move relaxation cannot be excluded for
> that event; but the motion reversed direction and overshot its starting point, which relaxation
> does not do, and the two-minute figure is measured long after any settling transient.

### The supporting evidence is weaker than it reads, and the log already says so

`swing_log_run1.log` is cited for "FAR on every sweep for 11.8 minutes with the motor still".
**The file contains ONE line** — `13:14:21 0.0s FAR`. §3.14 states this plainly and flags its own
caveat: the tool prints only changes of state, so one line is the whole record, and *"a sweep in
which every read failed would also score FAR."* **That is exemplary reporting and I am not
criticising it** — but it means the 11.8-minute figure is an absence of recorded state changes, not
11.8 minutes of measurements, and a poster must not present it as the latter.

**The strongest single piece of gap-motion evidence remains `release_watch_run1.log`**, with the
motor caveat above attached.

---

## V7. **`docs/ENGINEERING_REFERENCE.md` recorded this project's most expensive error backwards.** Corrected

**Found by Subagent 4 during its consistency pass, verified independently by me before acting.**

`docs/ENGINEERING_REFERENCE.md` §11 is, by `CLAUDE.md` §6, **the canonical home for documented
conflicts between sources.** Its row read:

> | ADC full scale 10.24 vs 4.096 | PC tools vs firmware driver and schematic | **Resolved: 4.096.**
> PC tools not yet changed |

**Both halves are wrong.**

1. **The full scale is 10.24 V, not 4.096 V.** 4.096 V is REFBUF; the LTC2326-16's span is
   2.5 × REFBUF. `docs/FACTS.md` has said so since 2026-09-07 and lists `4.096` as a RETIRED value
   for exactly this.
2. **The PC tools HAD already been changed.** `Code/pc/stm_approach.py:118-119` and `:501-504` use
   10.24 V and explain in the code why. I checked the source rather than trusting either document.

**This is the correction that `docs/FACTS.md` exists because of.** `Code/pc/check_facts.py`'s own
header says so: *"on 2026-09-07 the ADC full scale was corrected from 4.096 V to 10.24 V [...]
correcting the ones anybody thought of still left stale copies in six files."* **One of the
survivors was the conflict register itself** — the document whose entire job is to say which of two
conflicting sources won.

### Why the checker could not see it, and this is a genuine blind spot

`check_facts.py` suppresses a hit when the corrected value appears on the same line:

```python
num = re.search(r'\d[\d.]*', replacement)   # replacement is "10.24 V"
if num and num.group(0).rstrip('.') in line:
    continue                                 # "a correction table or a sentence saying X, not Y"
```

**A conflict row names both values by construction** — "ADC full scale 10.24 vs 4.096" — so "10.24"
is on the line and the hit is suppressed, **whichever value the row then declares the winner.**

**The suppression is right in general** and should stay: correction tables genuinely do carry both
numbers. **But it is blind in precisely the document type where a wrong resolution is most
damaging.** I have not changed the heuristic, because a targeted patch here risks suppressing less
and crying wolf more — and today has already produced three false positives from over-firing.
**Recorded instead as a known limit**, in this file and in the corrected row itself, with the manual
agent's `INCONSISTENCIES.md` carrying the full list of what a human still has to read for.

**Corrected in place**, with the old text struck through rather than deleted, per the project's
habit of keeping withdrawn claims in the record.

---

## V8. **The project's best-looking result is the feedback loop recovering from an X flyback.** Independently confirmed

**Subagent 2's central finding, re-derived by me from the raw file before I accepted it.**

`sessions/data/2026-09-17-bench/line_repeated_wide.csv` — twelve passes of one line at ±15,000 X —
produced a 636-count averaged profile with consecutive-pass correlation around +0.5 to +0.65 and a
split-half of +0.92. **`sessions/2026-09-17-bench.md` §3.25 has carried it as UNDETERMINED since
2026-09-17. It is the strongest candidate image this project has ever had.**

**The mechanism: the tool jumps X back to the start of each pass, and the surface is tilted, so the
loop begins every pass with a large Z error and spends the first pixels recovering.**

| Quantity | Subagent 2 | **My independent re-derivation** | |
|---|---|---|---|
| Tilt of the passes | −0.105 Z counts per X count | **−0.1048** | matches |
| X flyback between passes | 30,000 counts | **30,000** (17,768 to 47,768) | matches |
| **Predicted Z error at each pass start** | 3,144 counts | **3,144** | **exact** |
| Observed excursion over the first two pixels | 2,465 counts | **2,489** | matches |
| Consecutive-pass r, all pixels | +0.647 | **+0.515** | differs, see below |
| **Consecutive-pass r, first two pixels dropped** | **+0.048** | **+0.025** | **both are zero** |

**The result that matters reproduces: dropping two pixels out of twenty-one collapses the
correlation to nothing.** The apparent reproducible profile lives entirely in the first two pixels
of each pass, which is exactly where a loop recovering from a 3,144-count step would put it.

**One discrepancy, and it does not affect the conclusion.** My all-pixel correlation is +0.515
against their +0.647, and my mid-line step is 385 counts against their 236 — different averaging
conventions (Fisher-z against arithmetic mean, and a different definition of "mid-line"). **Both
numbers move the same way and both collapse to zero on dropping two pixels.** Worth reconciling in
the final figures so one number is quoted, not two.

### Why this is a strong result rather than a disappointing one

**A null result says "we could not see it". A mechanism says "here is what it was, and here is where
it will and will not appear."** Subagent 2's arithmetic predicts the transient's **absence** twice:

- the two 2D wide images of the same night raster back and forth without lifting X, so no flyback —
  predicted small, observed 37 and 78 counts;
- the 2026-09-19 three-Y runs do fly back but are nearly level, so predicted 28 and 238 counts —
  observed −99 and +47.

**One piece of arithmetic, three data sets, right about the presence and right about both absences.**
That is a falsification, not a null.

**And the check already existed in the repository one level up.** `sessions/2026-09-17-bench.md`
§3.22 killed a correlation of +0.75 by dropping the first *line* of an image. **Nobody applied the
same idea to the first *pixels* of a line.** The credit belongs to whoever wrote §3.22; what was
missing was one step of generalisation.

### The consequence for the bench, which is cheap and concrete

**Discard the first three pixels of every pass, in the tool** — writing them to the file so nothing
is lost — **and scan X boustrophedon between passes as well as within a line**, which the 2D images
already do and which is why they have no transient. Both are small changes to
`Code/pc/stm_y_control.py` and `Code/pc/stm_feedback_scan.py`, and between them they remove the
artefact that produced this project's most convincing false positive.

---

## V9. **The three-Y runs are MINUTES apart, not thirty. And the logs record the gap position nobody used**

**Both subagents, and I repeating one of them to Jacob, stated an interval that the data do not
support.** Subagent 2's `VERDICT.md` says run 4 came "half an hour later"; Subagent 1's `FINDINGS.md`
says "nine minutes later". **Neither is evidenced, and both are almost certainly too long.**

**What the record actually fixes.** `sessions/2026-09-19-bench.md` is chronological. §3.14 is
timestamped **03:48**, §3.16 is timestamped **03:53**, and §3.15 — all four three-Y runs — sits
between them. **All four runs fit inside about five minutes**, which is consistent with the work:
each run is 3 places × 6 passes × 21 points, and a 21 × 11 image on the same night took about 5 s.
**So run 2 to run 4 is a couple of minutes.** Neither log carries its own timestamp, which is why
this was guessable in the first place.

### The measurement nobody used

**Every `ycontrol_run*.log` records the onset Z at which the loop found the surface, on its first
line.** That is a direct measurement of gap position at the start of each run:

| Run | Onset Z | |
|---|---|---|
| 1 | 44,200 | ±3,000 places |
| **2** | **48,600** | the run that looked like a surface |
| 3 | 52,000 | X-held control |
| **4** | **50,800** | the repeat that did not reproduce |

**Between run 2 and run 4 the onset moved 2,200 counts — about 3% of the 65,536-count Z range.**

### Why this matters, and it does not go the way anyone expected

**The claim on record — mine included — is that "between run 2 and run 4 the gap moved by most of
the Z range", which is why "it did not repeat" and "the surface moved out from under it" cannot be
separated.** For this pair of runs **that premise is not supported by the instrument's own record.**
The gap was comparatively steady across exactly the interval in question.

**That weakens the candidate rather than strengthening it.** If the surface did not move much, then
"the surface moved out from under it" is a weaker explanation for the non-reproduction, and genuine
non-reproduction — i.e. there was no surface signal — becomes the better-supported reading.

**But it does not close it, for a reason that is specific and worth stating.** **Onset Z measures
the GAP, not lateral position.** A lateral drift in X or Y would carry the tip onto a different
patch of gold while barely changing the Z at which it finds the surface. **Nothing in this data set
measures lateral drift**, and the project has never measured it. So the candidate stays open — but
on the grounds that *lateral* position is unmeasured, not on the grounds that the gap moved wildly.

**This is a sharper open question than the one it replaces**, and it changes what the settling
experiment must include: **the interleaved-control repeat must also record onset Z at every run**,
so that gap motion is separated from whatever else is happening.

**Corrections owed:** `deliverables/2026-09-19-pause/candidates/VERDICT.md` ("half an hour later"),
`deliverables/2026-09-19-pause/analysis/FINDINGS.md` ("nine minutes later"), and I told Jacob "half
an hour" in conversation and have corrected it to him directly.

---

## V5b. The truncation class is WIDER than V5 found. Subagent 1's sweep, verified

**V5 checked the groups I suspected. Subagent 1 swept all of them, which is what `CLAUDE.md` §7.1
asks for and what I should have done.** Four groups are affected, on both sides of the comparison:

| Group | Side | As published / as naively computed | Complete images only |
|---|---|---|---|
| `cas9` | controls | +0.37 | **+0.068** |
| wide images | scans | +0.71 | **no complete pair exists** |
| tuned scans | scans | −0.25 | **no complete pair exists** |
| tuned scans | controls | +0.03 | **no complete pair exists** |

**Two corrections to my own V5:**

1. **The wide-image answer is stronger than I wrote.** I said "with one complete real wide image
   there is no valid reproducibility figure". That is right, and the consequence is that **the
   published +0.56 to +0.86 came entirely from lines the two fragments share** — there is no pair to
   compare at all, in either direction.
2. **The tuned scans belong in the table**, which V5 left out. **My statement there still stands and
   I re-checked it: no correlation for the tuned scans is published in `sessions/2026-09-19-morning.md`**
   — I grepped it again. So **no session-log conclusion is affected by that row**; what it affects is
   any analysis that recomputes those files naively, which is exactly what a future session would do.

**What still stands against the wide scans, and it is untouched by any of this:** trace/retrace of
**−0.94, −0.91 and −0.75**, against the controls' **+0.14 and +0.13**. Trace and retrace live in the
same file and always share a shape, so no truncation can reach them.

**The defect can no longer recur silently in that tool.** `image_to_image()` now drops any file
short of its group's modal line count, prints the truncating version beside the corrected one, and
names every pair it dropped.

### The onset-Z series, complete

All five `ycontrol` logs, verified by me directly from the files:

| File | Onset Z |
|---|---|
| `ycontrol_run1.log` (±3,000) | 44,200 |
| `ycontrol_xheld_run1.log` (±3,000, X held) | 47,000 |
| **`ycontrol_run2.log` (±12,000)** | **48,600** |
| `ycontrol_run3.log` (±12,000, X held) | 52,000 |
| **`ycontrol_run4.log` (±12,000, repeat)** | **50,800** |

**7,800 counts across all five; 2,200 between run 2 and run 4.** The series rises steadily and then
falls slightly — the shape of a slow drift, not of the violent excursions measured that morning.

**And Subagent 1's phrasing of the interval is better than mine.** I inferred "a couple of minutes"
from the surrounding timestamps. The correct statement is that **neither `ycontrol` log carries a
timestamp**, so **the interval between any two of them is UNKNOWN**, bounded only by the ~5 minutes
between §3.14 at 03:48 and §3.16 at 03:53. **"UNKNOWN, bounded by five minutes" is what the record
supports; "a couple of minutes" was an inference I should have marked as one.**

---

## V10. **I WAS WRONG, AND JACOB CAUGHT IT.** Tunnelling is NOT excluded for the 2026-09-17 junction

**I told Jacob that "we detected tunnelling current" is contradicted by his own data, and cited the
Z test: a decade per ~1,650 Z counts where tunnelling needs ~6-13. He replied that the project had
told them there was tunnelling in at least one case, and asked me to find it. He was right and I
was wrong.**

**I made exactly the error I wrote V3 to warn against: I applied evidence from one junction to a
different one.**

### The two junctions are not the same measurement

| | **2026-09-17 junction** | **2026-09-19 junction** |
|---|---|---|
| Tip | the 2026-09-17 tip | fitted ~03:00 on 2026-09-19, after the previous one was found **bent** |
| Sample | the 2026-09-17 gold | the leaf-on-paper gold |
| **Current per decade of Z** | **~250 counts** (median of 4 runs: 125, 236, 340, 433) | **~1,650-1,970 counts** |
| In/out hysteresis | not measured this way | **705-1,868 counts, every run** |
| Verdict on record | **OPEN** | **"a soft, pressed, sticky contact"** |

**The 2026-09-19 figure I quoted is about seven times shallower than the 2026-09-17 one, and it
belongs to a different tip on a different sample.** `docs/FACTS.md` says so in the section heading
itself — *"For this tip and this sample only."* **I read past it.**

### What the project's own record actually says about 2026-09-17

**`docs/OPEN_QUESTIONS.md`, the canonical register of open questions, line 47** — on the tip's
distance `d` from the pivot line, which it calls *"the most valuable unmeasured number in the
instrument"*:

> At the design's 1.00 mm the ratio is 40 [...] and the measured current decay of a decade per 200 Z
> counts works out at a decade per 3 nm, **thirty times too slow for vacuum tunnelling**. At
> 0.1-0.3 mm the ratio is 130-400 and the same measurement **lands near the textbook decade per
> 0.1 nm**. **So this one distance decides whether we are tunnelling or pressing through a soft
> contact.**

**`sessions/2026-09-17-bench.md` §3.19**, stated carefully at the time:

> For this junction to be vacuum tunnelling the lever ratio would have to be about **1,550** — the
> tip within **26 um** of the pivot line. **That is possible but implausibly exact.** The
> alternative fits everything measured [...] **Neither is proven. The straightedge measurement
> decides it.**

**`docs/NEXT_SESSION_PLAN.md`** puts a number on the threshold: **`d` under about 0.13 mm and
2026-09-17 was tunnelling; at `d` = 1 mm the tip was resting on something.**

**And `d` has never been measured.** `SAID`, Jacob, 2026-09-18: *"its between 1mm and 0mm its really
hard to measure"*, later *"1ish mm"*. **The threshold sits inside the range.** Three attempts to get
it from photographs gave answers a factor of two apart, which is why `Images/ours/README.md` forbids
trying again.

### The corrected position, which is what the deliverables must carry

> **The 2026-09-19 junction was a pressed contact — measured, and not in doubt.**
>
> **Whether the 2026-09-17 junction was tunnelling is an OPEN QUESTION that this project has never
> closed, and it turns on a single unmeasured distance.** The instrument's own record identifies the
> measurement, states the threshold, and says it needs no electronics: **lay a straightedge across
> the two ball ends, with the plate off, and see which side of it the tip stands on and by how
> much.** Below about **0.13 mm**, the 2026-09-17 measurement is tunnelling.

**"We have not demonstrated tunnelling" remains true and must stay. "Our data rule it out" is FALSE
and I should not have said it.** The distinction is the difference between an honest limitation and
a wrong claim, and I made the wrong claim in the direction of caution — which is still a wrong
claim.

### What this changes downstream

- **`FRAMING.md`'s say/do-not-say table is corrected.** "We were in the tunnelling regime" stays out
  as a *claim*; "whether our best junction was tunnelling is undecided, and one ruler measurement
  decides it" goes in as a *result*, because it is one.
- **This is a better poster panel than either overclaiming or dismissing.** A team that can name the
  single measurement standing between them and the answer is showing they understand their
  instrument.
- **It raises the priority of measuring `d`** to the top of the bench list. It needs a straightedge
  and no power, and it retroactively settles the project's best junction.

**Credit where it is due: Jacob caught this, against a confident and wrong statement from me,
because he remembered the record better than my reading of it.**

---

## V11. **The case for tunnelling is WEAKER than the repository's own optimistic passages say — and my V10 repeated their error**

**Jacob asked me to write "we achieved tunnelling" and to elaborate on it. Before writing anything I
re-derived the requirement from first principles. It goes the other way, and it also corrects V10.**

### The arithmetic, with every input from the repository

| Input | Value | Source |
|---|---|---|
| Fine screw | 0.31750 mm/turn | `docs/FACTS.md` |
| Motor steps per turn | 2,048 | 28BYJ-48 through its gearbox |
| **Screw travel per motor step** | **155 nm** | matches `sessions/2026-09-17-bench.md` §3.19 exactly |
| Cross-check at ratio 40 | **3.88 nm/step** | matches `docs/FACTS.md` exactly |
| Pivot line to motor screw | 40 mm | `PiezoPlate.stl`, Y 135.28 against Y 95.28 |

**Measured on 2026-09-17: about 250 Z counts per decade of current, and about 250 Z counts per motor
step. So one motor step changed the current roughly tenfold.**

**A vacuum tunnel gap changes tenfold per 0.1 nm.** For one motor step to move the tip 0.1 nm:

**required lever ratio = 155 / 0.1 = 1,550, so d = 40 mm / 1,550 = 26 um.**

### What the tip actually moves, at each candidate `d`

| `d` | Lever ratio | nm per decade | How far from tunnelling |
|---|---|---|---|
| **1.00 mm** (design) | 40 | 3.88 | **39x too slow** |
| 0.30 mm | 133 | 1.16 | **12x too slow** |
| **0.13 mm** (the threshold quoted in the plan) | 308 | 0.50 | **5x too slow** |
| 0.10 mm | 400 | 0.39 | **3.9x too slow** |
| **0.026 mm** | 1,538 | 0.10 | **this is the only value that works** |

### Two live documents are wrong, and so was my V10

1. **`docs/OPEN_QUESTIONS.md`** says *"At 0.1-0.3 mm the ratio is 130-400 and the same measurement
   **lands near the textbook decade per 0.1 nm**."* **It does not.** At 0.1 mm it is 3.9x too slow;
   at 0.3 mm, 12x. **That sentence overstates the case for tunnelling by roughly four to twelve
   times.**
2. **`docs/NEXT_SESSION_PLAN.md`** says *"d under about 0.13 mm and 2026-09-17 was tunnelling"*.
   **On the decay criterion it was not — 0.13 mm is still 5x too slow.** The 0.13 mm figure is a
   **different** criterion, about whether the height wobble is small enough to hold a gap at all.
   **Both criteria have to be met; the decay one is far stricter, and the two were conflated.**
3. **My own V10 repeated the plan's 0.13 mm uncritically** and told Jacob that below it the
   measurement "is tunnelling". **That was wrong in his favour, which is still wrong.**

**`sessions/2026-09-17-bench.md` §3.19 had it right all along**, and is the only passage in the
repository that does: *"the lever ratio would have to be about 1,550 — the tip within 26 um of the
pivot line. That is possible but implausibly exact."*

### So: can the deliverables say "we achieved tunnelling"?

**No, and this pass makes the answer firmer rather than softer.** It would require the tip to sit
within **26 micrometres** of the pivot line — a 2.6% sliver at the very bottom of the 0-1 mm range
Jacob measured by eye, on a hand-built holder soldered to a superglued stake. **Nothing was built to
that tolerance and nothing has measured it.**

**What remains true, and is still worth a panel:** the 2026-09-17 junction is a real barrier
junction whose tunnelling status is **not settled by the data that exist** — but the honest reading
of the decay arithmetic is that **a pressed contact through a thin film is much the better
explanation**, exactly as §3.19 concluded on the night. **The straightedge measurement is still
worth doing**, because it converts an argument into a number, and because `d` sets the Z scale for
every future measurement. **It is no longer fair to present it as a coin-flip.**
