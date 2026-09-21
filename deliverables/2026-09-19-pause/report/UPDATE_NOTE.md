# Collaborator update — DRAFT, for Jacob to adapt and send

**Status: DRAFT. Nothing here has been sent to anybody, and no email address, affiliation or
relationship has been assumed.** Jacob said he will write the collaborator emails himself. This
file gives him **one recipient-neutral note to adapt**, a list of what to attach and why, and
**the questions he has to answer before any of the three can be personalized.**

**Three things this file deliberately does not do:** invent a name, invent a relationship, or
write three fake personalized emails. Section 3 says why, and section 4 records the one contact the
repository does turn out to name.

---

## 1. The note — recipient-neutral, about 920 words

> **Adapt freely.** The square brackets are the places where only Jacob knows the answer. **The
> technical sentences are the part not to loosen**: every figure in them is checked, and the two
> places where the note declines to claim something are deliberate.
>
> **It is longer than it was.** If it needs to come back down, **cut the AI-workflow paragraph or
> the calibration detail first** — not the tunneling paragraph, which is the part a technical
> reader will answer.

---

**Subject: We Are STMing — an update on the home-built STM, and where we have paused**

Dear [name],

[One line on how you know each other, and what they last heard about this.]

Over eleven weeks of planning and design and eight weeks of building, Nuh Shaheer and I — **two
undergraduates with no coding experience and very little electronics experience** — have built
a scanning tunneling microscope from 3D-printed parts. **This project was the first real soldering either of us has done**, and it was
built and run **in a basement in a house people live in**, with people moving around and no control
over the air or the temperature: a wooden bench on a concrete floor, a few meters from the breaker
panel. **It is not a clean room and it never was.** The mechanics, firmware and controller board
follow Mech Panda's open-source `red-panda-stm`; the scan head and transimpedance preamplifier
follow Dan Berard's home-built STM. Everything else — the electronics bring-up, the software, the
calibration and the fault isolation — we learned as we went.

**Where it stands: every subsystem a tunneling microscope needs is built, working and calibrated,
and what is left is mechanical.**

The measurement chain is calibrated end to end. With a precision 100 MΩ resistor clipped in where
the tip and sample go, the instrument reported −3,205 ± 37 counts per volt against −3,200 worked
out from Ohm's law before the measurement — 0.13 standard errors, R² 0.993, 53 readings at eight
bias settings. (The honest limit: that slope is the ratio of two nominally 100 MΩ resistors whose
tolerances we do not have.) The amplifier runs at about 4 pA of input current against a 1 nA
signal, the electronics are flat white noise at 8 to 14 counts across the band, and leakage is
under 0.06 nA from −2 V to +2 V. Stamping on the floor changes nothing, so the building is not
getting in electrically.

We have made a real tip-to-sample junction: current rising from 0.85 nA at 0.05 V to 31.7 nA at
0.5 V, superlinear as V^1.55, resistance falling from 59 to 16 MΩ, symmetric in both polarities to
about 10%, taken as eight rounds with the polarities interleaved and confirmed by a bias-flip test
on two separate nights. That is a barrier: not a metallic short and not an open circuit.

**We detected tunneling, but weren't able to maintain tunneling range for long enough to get an
image.** The tip cannot go from not-touching to touching without passing through the separations
where tunneling is what carries the electrons, and the bias was applied with the amplifier
recording the whole way — 60,928 readings inside that current range, across 109 approaches; the I-V
above is superlinear and symmetric and the junction never metallically shorted, so what conducted
was a barrier and not a metallic bridge. **What we could not do is hold it there.** A later
distance test, on a different tip and a different sample, gave a decade of current per about 1,650
Z counts where a held vacuum gap needs roughly ten, with mechanical hysteresis in every run, which
we read as a pressed contact. **We have not produced an image.**

**What stops us is mechanical, and we measured it rather than guessing.** With the motor stopped
and nobody touching the instrument, the gap moved by more than 43,000 Z counts in 6.4 seconds and
more than 56,000 within two minutes. Over the five seconds one image takes it drifts by 400 to
1,700 counts, and the structure in any candidate image is 30 to 460 counts. Every scan was run
against a control in which the tip never moved sideways — which cannot contain surface structure —
and the scans never beat their controls.

**That is where the basement stops being background and becomes the point.** An STM is normally a
clean-room instrument, and a gap moving on this timescale is precisely the class of problem those
rooms exist to remove. **The limitation is the expected outcome of the environment — measured,
quantified in the instrument's own units, and traced to five named candidate mechanisms.**

One more thing that is as much a result as the instrument. **Neither of us writes code, so the
second thing we built was the system that does**: a 575-line operating protocol for the AI model we
work through, one canonical register holding every number in the project with its provenance and
its date, 27 append-only session logs, and a 565-line checker that runs seven classes of test at
every session start and blocks a commit that fails. **The point of it is not that the model writes
well — it is that the model gets caught**: those checks made us withdraw a statistic computed
across truncated files, a reproducibility figure that turned out to be our own feedback loop rather
than the sample, and a detector's full-scale voltage we had recorded backwards in our own reference
document — and every retraction is still in the record beside the claim it replaced.

Work is paused: the instrument is disassembled and moved, and [reason and timescale]. When it comes
back: prove the gap holds still before scanning anything, move to a rigid sample and a sharper tip,
then one decisive experiment with interleaved controls and the decision rule fixed in advance.

**What would help most** is a view from someone who has fought this — sample mounting and approach
mechanics at this scale, cabling onto a suspended stage, and whether these numbers suggest
something we have missed. [Ask.]

Everything, including the mistakes, is at github.com/jacobbkatz/We-Are-STMING.

With thanks,
Jacob Katz
[contact details]

---

## 1b. ADD THIS PARAGRAPH — the open question, and it is the most interesting thing in the note

**Added 2026-09-19; the figures in it were corrected on 2026-09-20 — see the note under the
paragraph, because three of them were wrong.** The note above does not yet carry the project's
sharpest open result. **For a reader at a national lab this is the paragraph they will actually
respond to**, because it is a well-posed question with a cheap experiment attached rather than a
status report. Drop it in after the paragraphs about the junction:

> One junction we made on 17 September is still undecided, and we can say precisely why. Its
> current fell by a decade for about every 250 Z counts of piezo travel. Whether that was a gap we
> were holding open or a tip pressing through a contaminant film turns entirely on one distance
> inside the scan head: how far the tip sits from the line joining the two fixed screws, which sets
> the lever ratio between the coarse screw and the tip. At the design's 1.00 mm the decay is about
> 39 times too slow for a vacuum gap; at 0.5 mm, 19 times; at 0.13 mm, still 5 times. **Only about
> 26 micrometers works.** I measured that distance at the bench on 20 September and it is **under
> 0.5 mm** — which narrows the question without settling it, because 26 micrometers sits inside
> that bound, in the bottom 5% of it. Resolving it needs a loupe or a USB microscope with a scale
> in the frame rather than the straightedge that gave the half-millimeter bound, and it is the
> first thing we will do when the instrument is rebuilt.

> **What changed on 2026-09-20, recorded because this is the text most likely to reach an
> outsider.** The paragraph previously said the threshold was "around 0.13 mm", that the distance
> was "somewhere between 0 and 1 mm", and that "at 0.1 to 0.3 mm the same measurement lands near
> the textbook decade per 0.1 nm". **All three were wrong.** The decay threshold is about **26
> micrometers**; **0.13 mm is a different criterion** — whether the gap wobbles too much to hold at
> all — and on the decay test it is still 5 times too slow; and 0.1 to 0.3 mm does **not** land
> near the textbook figure, being 3.9 to 12 times too slow. **Jacob measured the distance at the
> bench on 2026-09-20 and it is under 0.5 mm** (`docs/FACTS.md`). The **250 Z counts per decade is
> correct for this junction** — it is the 2026-09-17 one; the 1,650 to 1,970 figure quoted earlier
> in the note belongs to the **2026-09-19** junction, which is a different tip and a different
> sample. Full arithmetic in `deliverables/2026-09-19-pause/LEAD_VERIFICATION.md` V11-V13 and
> `deliverables/2026-09-19-pause/JUNCTIONS.md`.

**Why this is worth sending rather than hiding.** It is honest, it is specific, and it shows a team
that knows which single measurement stands between them and an answer. **It is also the one place
where an experienced reader can help cheaply** — somebody who has built an STM will have an opinion
about that lever ratio, and may simply tell you.

**Do not soften it into "we think we saw a gap", and do not harden it either.** The whole value of
the paragraph is that it is undecided and that the deciding measurement is named.
`docs/OPEN_QUESTIONS.md` puts it as *"this one distance decides whether we are tunneling or
pressing through a soft contact."* **Note what is and is not open here.** That we detected
tunneling is settled and is stated in the note above; **what this paragraph leaves open is whether
that particular junction was a gap we were holding rather than a film we were pressing into** —
which is a question about the 2026-09-17 junction, not about the project's headline claim.

---

## 2. What to attach, and why each one earns its place

**Four attachments is a good maximum for a cold-ish email; six if they asked for detail.** All
paths are in this repository.

| Attach | File | Why this one |
|---|---|---|
| **1** | `deliverables/2026-09-19-pause/figures/png/fig01_calibration.png` | **The credibility figure.** The line is not fitted — it is what Ohm's law requires, worked out before the measurement. One glance says the chain works |
| **2** | `deliverables/2026-09-19-pause/figures/png/fig03_gap_motion.png` | **The ask, in one picture.** It is the measured blocker, and it is what any advice would be about |
| **3** | `deliverables/2026-09-19-pause/photos/prepared/04_instrument_full_height.jpg` | **What it physically is.** The best overview of the assembled instrument, with four parts named |
| **4** | `deliverables/2026-09-19-pause/figures/png/fig02_iv_curve.png` | **The junction.** Send it if the reader is technical; **the figure carries its own caveat that a barrier is not a tunneling gap**, which is exactly the caveat you want them to read in your words rather than infer |
| 5 | `deliverables/2026-09-19-pause/figures/png/fig04_control.png` | **The method.** If the reader is an experimentalist, this is the one that will earn their respect: the control that killed our own result |
| 6 | `deliverables/2026-09-19-pause/photos/prepared/13_poster_module_portrait.jpg` | **The human frame** — Jacob holding the complete scanning module. Good for a reader who is not going to read the numbers. **Contains a face; publication of a team photograph was confirmed for the poster, so extending it to an email is Jacob's call** |

**Two to consider instead of, not as well as:**

- `figures/png/fig06_noise.png` — the noise floor, still against stamping. Useful only if the
  conversation is about vibration or grounding.
- `photos/prepared/01_sample_plate_gold_window.jpg` — the sample as the tip actually sees it.
  **It shows honestly that the window is not all gold**, which is a point in your favor with
  anyone who has mounted a sample.

**Do not attach:** anything from `analysis/plots/`, which predates the corrections; any scan image,
because **no image in this project has a known scale and none should travel without its caption.**

---

## 3. THE THREE CONTACTS — for Jacob to fill in privately

**Jacob named three intended recipients: a contact at Brookhaven, a second person, and someone who
helped.** Two of the three are not identified anywhere in this repository, and **nothing here
guesses at them.**

**The questions that have to be answered before the draft above can be sent — who each person is,
how they know the project, what is being asked of them, and whether each is content to be named in
a public repository — were put to Jacob directly and are not reproduced here.**

> **Why they are not reproduced here.** This repository is public. Working through a named
> individual's identity, their relationship to the project, or whether they have agreed to be
> associated with it is a reasonable thing to do in private and **not a reasonable thing to publish
> about somebody**, particularly somebody who has not been asked. **Removed 2026-09-20**, when the
> repository was read through as an outside reader would read it.
>
> The acknowledgements themselves stay exactly as they are. They are Jacob and Nuh's own words,
> written into `README.md` on 2026-07-31, and they are not this work's to retract.

---

## 4. One of these three WAS already in the repository, and it should be said so

**`CLAUDE.md` §3b: before recording something as unknown, search for it — and if the answer was
already there, say where it was and credit whoever wrote it down.** The brief for this work stated
that none of the three contacts is named or contactable anywhere in the repository. **That is right
for two of them and wrong for the Brookhaven one.**

> **`README.md` line 121:** *"Thank you also to Dr. Percy Zahl (Brookhaven National Laboratory,
> CFN) for guidance on vibration isolation and scan head design."*
> The same sentence is in **`docs/progress.html`** §12, the credit section.

**Where it came from. Corrected 2026-09-20.** This said both were added on 2026-09-16 in commit
`55d8022`. **Only the progress page was.** The README credit is **six weeks older**: it is in
`de1cf22`, 2026-07-31, *"Revise README with detailed project information"* — the first detailed
README this project had, written by Jacob and Nuh before any of this work existed. **So it is
their own acknowledgement, made at the start, and it is not this work's to retract.** Checked
commit by commit rather than inferred.

**Why it was missed:** it is in an acknowledgments section, not in any bench document, and
**no session log records who supplied the name or how the guidance was given** — so it is invisible
to a search of the technical record. Credit for writing it down belongs to that session and to
whichever of Jacob and Nuh told it.

**What this does and does not settle.** It gives a name, an institution and a subject — **and
vibration isolation is precisely the open problem**. It does **not** settle that this is the person
Jacob means, it gives no contact details, and it records no consent. **Confirm with Jacob before
the name goes into any email.**

---

## 5. Two things to keep out of the outgoing note, whoever it goes to

1. **"We produced an image" and "we maintained tunnelling range" are both unsupported.**
   **"We detected tunnelling" is supported and the draft now says it** — corrected 2026-09-20; the
   earlier wording here said not to claim tunneling at all, and that was wrong in the direction of
   caution (`deliverables/2026-09-19-pause/LEAD_VERIFICATION.md` V13). **Use Jacob's sentence
   whole, both halves in one breath:** *"We detected tunneling, but weren't able to maintain
   tunnelling range for long enough to get an image."* **The first person to ask a hard question
   will be someone who knows what an STM is**, and their question will be *how did the current vary
   with distance?* — which the second half of that sentence answers before it is asked.
2. **No number taken off a photograph, and no scale bar.** Nothing in these deliverables carries
   one, because no image in this project has a known scale.
