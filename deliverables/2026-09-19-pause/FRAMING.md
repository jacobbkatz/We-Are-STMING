# How these deliverables are framed — Jacob's instruction, 2026-09-19

---

# THE CANONICAL SENTENCE. Use this wording, and prefer it to any paraphrase.

**`SAID`, Jacob, 2026-09-20, in his own words:**

> ## **"We detected tunnelling, but weren't able to maintain tunnelling range for long enough to get an image."**

**This is now the project's headline claim and it supersedes every earlier formulation**, including
"we have not demonstrated tunnelling", which `LEAD_VERIFICATION.md` V13 established was wrong in
the direction of caution.

**It is accurate in both halves, and each half is separately supported:**

| Half | What backs it |
|---|---|
| **"We detected tunnelling"** | The tip cannot go from not-touching to touching without passing through the separations where tunnelling is the only thing carrying electrons, and bias was applied with the amplifier recording the whole way — **60,928 readings inside that current range, across 109 approaches**. The I-V is superlinear and symmetric and the junction never metallically shorted, so what conducted was a barrier, not a bridge. `LEAD_VERIFICATION.md` V13 |
| **"…but weren't able to maintain tunnelling range long enough to get an image"** | With the motor stopped and nobody touching the instrument, the gap moves **≥ 43,000 Z counts in 6.4 s** and **≥ 56,000 over about two minutes**. An image needs it inside a few hundred counts for a minute. `docs/FACTS.md`, `STATUS.md` |

**What this sentence deliberately does NOT say**, and these stay out:

- **an image, or atomic resolution** — none has been produced
- **a distance in nanometres from our own hardware** — the scale has never been established here
- **that we held a controlled vacuum gap** — "maintain tunnelling range" is exactly the thing we
  are saying we could not do, and that is the honest half of the sentence

**Anywhere a deliverable needs one line on the tunnelling question, use Jacob's sentence verbatim.**
Where it needs a paragraph, expand it in that order: the detection first, the maintenance second,
then the one measurement (`d`, to 26 micrometres) that would settle the 2026-09-17 junction.

---

**`SAID`, Jacob, this session:**

> *"whatever the result here for the image is include it in the results and stuff but the focus
> should be like we got extremmly close the focus of all of this should be look what we did not what
> we failed at what we still have to do"*

**This is binding on every deliverable: the poster, the report, the manual's framing, and the
figures.** It is a decision about emphasis, and it is the author's to make.

---

## What this means in practice

**LEAD WITH WHAT THE INSTRUMENT DEMONSTRABLY DOES.** Not with the fault list. Two people who do not
write code designed, ordered, assembled and characterised a working scanning-probe measurement
chain and proved it against theory: **eleven weeks of planning and design, eight weeks of building**
(`SAID`, Jacob, 2026-09-20), first power-on 29 August 2026, last bench session 19 September 2026,
27 session logs. (**Settled 2026-09-20. Four deliverables said eight weeks and three said eleven; both
were right and neither said which phase it meant. Always say which. Do not write a combined total —
none has been stated.** `docs/FACTS.md`, Project timeline.)

**The organising sentence, and it is true:**

> **Every subsystem a tunnelling microscope needs is built, working and calibrated. What is left is
> mechanical.**

That is not spin. It is what the evidence says, and it is a stronger claim than a fault list because
it is specific. The electronics work. The amplifier resolves picoamps. The converter chain is
calibrated against theory to 0.13 of a standard error. A real tip-sample junction has been made and
its current responds to voltage and to distance. The coarse approach finds the surface. The control
methodology is better than most undergraduate work. **The gap between here and an image is
mechanical stability, and it is identified and quantified rather than mysterious.**

## Where the line is, and it does not move

**"We got extremely close" is supportable. "We achieved tunnelling" and "we produced an image" are
not.** The difference is not pedantry — at a research expo the first person to ask a hard question
will be someone who knows what an STM is, and an overclaim loses the room and everything else on the
poster with it. **An honest limitation, stated confidently, survives that conversation. An overclaim
does not.**

So:

| Say | Do not say |
|---|---|
| The whole measurement chain works end to end and agrees with theory to 0.13σ | The instrument is calibrated in nanometres |
| A tip-sample junction was made; its I-V is non-ohmic and bias-symmetric — the shape a barrier requires | We observed quantum tunnelling |
| Junction resistances of 16-59 MΩ, the range tunnelling occupies | We were tunnelling |
| No image yet; the remaining barrier is mechanical and we measured it | We failed to image |
| The gap moves by most of the Z range in seconds — we found the blocker | The instrument does not work |

**"We found the blocker" is a result.** Most of the value in eight weeks of instrument development
is knowing precisely what stops you. Present it that way: **a measured, quantified obstacle is an
achievement, not a failure.**

## Structure that follows from this

1. **What we built** — the instrument, the photographs, the subsystems.
2. **What it demonstrably does** — calibration, the junction, the noise floor, the I-V.
3. **How we tested ourselves** — the controls. This is a strength and should be presented as one.
4. **What we found in the way** — the mechanical instability, measured.
5. **Where it goes next** — short, forward-looking, not a confession.

**Limitations are stated plainly and once, in their own place, not sprinkled through as apology.**
Every figure still carries its honest caption; that is different from an apologetic tone.

## What does NOT change

- **No invented results, no invented scale bars, no implied imaging.**
- **Every number keeps its provenance** and its uncertainty.
- **`STATUS.md` remains the live technical record** and is written for the bench, not for an
  audience. Its tone does not change; this framing governs the outward-facing deliverables.

---

# ADDENDUM, 2026-09-19 — the conditions this was built in, and one claim that cannot be made

**`SAID`, Jacob, this session, and this is the most important context in the whole project:**

> **Corrected 2026-09-20, and the quotation below is untouched because it is what Jacob said.**
> *"first year students"* was true of the year that had just ended. **Jacob and Nuh are going into
> their second year as of September 2026** (`SAID` Jacob, 2026-09-20), so the build ran over the
> summer between the two. Every live deliverable now says **two undergraduates**; `docs/FACTS.md`
> carries the row.

> *"this lives in my basement. This project whole thing was like, you can do it at home with no
> experience. We have like, we're two first year students with no coding experience and really not
> much electronics experience. So this was our first real time kind of touching any soldering of
> anything. [...] it's kind of important to recognize that we were not in a clean room, we're in a
> basement in a house where people live a lot and move around and stuff. And, you know, we're not
> controlling the air. [...] this is so impressive that we even got this far."*

## THIS GOES IN EVERY DELIVERABLE. It is not a disclaimer — it is the result.

**The conditions are not an excuse for the limitations. They are the measure of the achievement,
and they were missing from every document in this repository.**

| Fact | `SAID` by Jacob, 2026-09-19 |
|---|---|
| **Two undergraduates**, in their second year as of September 2026 (`SAID` Jacob, 2026-09-20) | No professional context, no lab, no supervision on record |
| **No coding experience** | Neither author writes code — `CLAUDE.md` opens with this |
| **Very little electronics experience** | **This project was their first real soldering** |
| **A basement in a lived-in house** | Not a lab, not a clean room |
| **People moving around, air uncontrolled** | No vibration isolation from the building beyond what they built; no temperature or air control |

**Corroborated by the photographs** (`deliverables/2026-09-19-pause/photos/MECHANICAL_OBSERVATIONS.md`
§6): a wooden bench on a concrete floor, beside a breaker panel and a generator transfer switch.

### Why this belongs in the science, not just the biography

**An STM is normally a clean-room instrument.** Commercial ones sit on air tables in
temperature-controlled labs. **The blocker this project identified and measured — the gap moving by
most of the Z range in seconds — is exactly the class of problem those rooms exist to remove.**

**So "we could not hold the gap still in a basement" is not a failure to explain away. It is the
expected outcome, measured, quantified, and traced to named candidate mechanisms** — which is
precisely what instrument development is. **State the conditions up front, and the limitation stops
being a shortfall and becomes a finding about what the environment costs you.**

## The candidate image goes in

**Jacob's instruction: include it.** The three-Y run at 12,000 Y separation — the only measurement
this project has made that looked like topography — **appears in the poster, the report and the
gallery**, beside its repeat and its X-held control, with its honest statistics. It is presented as
**an open question with a specified experiment to settle it**, not as an image. That is what it is,
and an open question a team can name precisely is a stronger thing to show than a pretty picture.

## ~~THE ONE CLAIM THAT CANNOT BE MADE — tunnelling current~~ **RETRACTED 2026-09-20**

> **This section said the opposite of what this file now says, and it was the lead's error, not
> Jacob's.** It is kept rather than deleted because it was believed, acted on, and written into
> eleven deliverables — and because this project's own rule is that a withdrawn claim stays beside
> the one that replaced it.

**What it said:** that *"we actually were able to detect tunnelling current"* **could not go in any
deliverable**, because the project's own data contradicted it.

**Why that was wrong.** It applied the 2026-09-19 junction's numbers — a decade per ~1,650 to 1,970
Z counts, hysteresis of 705 to 1,868 counts in every run — **to the question of whether tunnelling
occurred at all.** Those numbers are real, they are correctly measured, and they are the reason we
cannot claim a **held vacuum gap**. They say nothing about whether tunnelling occurred, because a
tip cannot travel from not-touching to touching without passing through the separations where
tunnelling is the only mechanism available, and we had bias applied and the amplifier recording the
whole way. **Jacob made that argument, against a confident and repeated statement from the lead,
and he was right.** The full step-by-step is `LEAD_VERIFICATION.md` **V13**.

**The correction is not a softening.** It splits one claim into two, and only the second fails:

| Claim | Status |
|---|---|
| **"We detected tunnelling"** | **TRUE, and it is now the headline of this file.** The tip passes through the tunnelling separations on every approach; 60,928 readings were taken inside that current range across 109 approaches; the I-V is superlinear and symmetric and the junction never metallically shorted, so what conducted was a barrier and not a metallic bridge |
| **"We maintained tunnelling range" / "we held a vacuum gap"** | **NOT ESTABLISHED, and this is what the shallow decay and the hysteresis argue against.** It is also the thing you need in order to image |
| "We produced an image" / "atomic resolution" | **FALSE.** None has been produced |
| A distance in nanometres from our own hardware | **Not available.** The scale has never been established here |

---

## The say-this / not-this table, corrected

| Say this | Not this |
|---|---|
| **"We detected tunnelling, but weren't able to maintain tunnelling range for long enough to get an image."** — Jacob's own sentence, and the canonical one | ~~We detected tunnelling current~~ **— this ban is retracted; the claim is true** |
| **The instrument measures currents of about one nanoamp, proved against a known resistor to 0.13 of a standard error** | We imaged anything |
| **We made a real tip-and-sample junction and measured its I-V: non-ohmic, bias-symmetric, resistance falling 59 to 16 MΩ — the signature of a barrier, and a barrier conducting at those resistances is conducting by tunnelling** | We resolved atoms |
| **The junction's current responds to the tip's height, and to the bias, and reverses with it** | We were in the STM regime, or held a controlled vacuum gap |
| **We could not HOLD the gap: the distance dependence was far shallower than a vacuum gap requires and the junction showed mechanical hysteresis in every run** | Any figure in nanometres taken off this instrument |

**The hard question at the expo, answered the corrected way.** *"How did the current vary with
distance?"* is still the question somebody who knows what an STM is will ask, and the answer is
still the honest one: **"a decade per about 1,650 counts, where a vacuum gap needs about ten — which
is how we know we never held a gap, and it is the thing we measured rather than guessed."**

**That answer now sits underneath a claim that survives it**, rather than one it destroys. The
earlier worry — that claiming tunnelling would collapse on this question and take the calibration,
the noise work and the controls down with it — was a good instinct applied to the wrong claim.
**What collapses on that question is "we held a vacuum gap". "We detected tunnelling" does not.**

**A poster that says "we detected tunnelling, could not hold it long enough to image, and here is
the measurement that would settle our best junction" is stronger than either overclaiming or the
dismissal this section used to require.**
