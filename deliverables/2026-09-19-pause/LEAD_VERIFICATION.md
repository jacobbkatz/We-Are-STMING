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
