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
