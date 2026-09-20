# Questions you will be asked, and honest answers

**For Jacob and Nuh, 2026-09-19.** Written against the poster's six panels:

| | |
|---|---|
| **01** | We built the whole thing |
| **02** | The measurement chain agrees with theory |
| **03** | A real junction, with a barrier's signature |
| **04** | We found the limit, and measured it |
| **05** | We built controls designed to kill our own results |
| **06** | One junction is still undecided - and we know the measurement |

**Every answer here traces to `docs/FACTS.md`, to
`deliverables/2026-09-19-pause/LEAD_VERIFICATION.md`, or to the session log named beside it.** The
source is given so you can check it, and so you can say where it came from if somebody pushes.

**Two rules that cover everything below.**

1. **Never claim tunnelling, and never claim an image.** Not as a slip, not as a "well, basically".
   The honest answers here are stronger, and they survive the follow-up question. An overclaim does
   not, and it would take the calibration, the noise work and the controls down with it.
2. **"We have not measured that" is a complete answer.** It is a normal sentence at a research
   event and everybody there says it about something. **What is not acceptable is inventing a
   number on your feet** - section 5 lists the questions where that is the temptation.

---

## 1. The hard ones, from people who know what an STM is

### "How did the current change with distance?"

**This is the question. It decides whether they believe the rest of the poster. Panel 06.**

> On the junction we tested on 19 September, it took about **1,650 to 1,970 Z counts** for the
> current to change ten-fold. A tunnelling gap, on the Z scale we inherited, would need about
> **6 to 13**. **So that one was a pressed contact, and we say so on the poster.** Every run also
> showed **705 to 1,868 counts of hysteresis** between going in and coming out - the current
> lingers on the way out - which is mechanical, and which does not depend on any distance scale.
>
> Our best junction, two nights earlier, was about **seven times steeper**: roughly 250 counts per
> decade. **Whether that one was a vacuum gap is still undecided, and panel 06 is about exactly
> that.**

**Source:** `docs/FACTS.md`, "the junction and the gap"; `LEAD_VERIFICATION.md` V10-V12;
`sessions/2026-09-19-morning.md` 3.10-3.11.

### "So were you tunnelling, or not?"

**Do not answer yes. Do not answer no either - the honest answer is the interesting one, and it is
what panel 06 says.**

> **On 19 September, no: that junction was a pressed contact, measured.** Our best junction, on the
> 17th, was a real barrier, and we wanted it to be tunnelling - so we worked out what that would
> require instead of guessing.
>
> One motor step moves the fine screw **155 nm**. A vacuum gap changes the current ten-fold per
> **0.1 nm**, and that junction changed by about a decade per motor step. **So the lever ratio
> between the motor and the tip would have to be about 1,550, which puts the tip within about
> 26 micrometres of the line joining the two ball supports.** At the 1 mm the design puts it at, we
> are **39 times too slow**.
>
> **Jacob measured that distance as well as a straightedge and an eye can: under half a
> millimetre.** That does not resolve 26 micrometres, so **we cannot say, and we do not.** What
> closes it is an eyepiece or an optical comparator, with the power off, in minutes - and the same
> measurement gives us our first height scale.

**Source:** `LEAD_VERIFICATION.md` V11 and V12; `sessions/2026-09-17-bench.md` 3.19, which called
the 26 um requirement *"possible but implausibly exact"* on the night; **`docs/FACTS.md` lists `d`
itself as CONTESTED - do not use.**

**If they push: "but what do you think?"** - *"The arithmetic does not favour it. At anything but
the very bottom of the range we could measure, it is a tip pressing through a thin film. We would
rather say that than claim something we cannot defend."*

### "Isn't 26 micrometres a strange threshold? Where does 0.13 mm come from?"

**Somebody who has read the repository may ask this. There are two different criteria and they got
conflated for two days.**

> **26 micrometres is the decay criterion** - what it takes for one motor step to move the tip
> 0.1 nm. **0.13 mm is a different one**: whether the height wobble is small enough to hold a gap
> at all. **Both have to be met, and the decay one is far stricter.** We had them mixed up in our
> own notes and caught it during a self-audit.

**Source:** `LEAD_VERIFICATION.md` V11, which corrects `docs/NEXT_SESSION_PLAN.md` and an earlier
verification entry of our own.

### "Sixteen to fifty-nine megohms is low for a tunnelling junction."

**Yes, and they are right. Do not argue.**

> It is at the low end - tunnelling junctions usually start around a hundred megohms and go up.
> It is still about a thousand times above the conductance quantum, so it is not a point contact
> either. **What panel 03 claims is a barrier, not a vacuum gap**, and we are careful about the
> difference.

**Source:** `LEAD_VERIFICATION.md` V3.

### "Couldn't that curve just be a dirty contact, or an oxide?"

> **Yes. It could.** A contaminant film, a thin oxide or a dirty near-contact are all superlinear
> too. That is exactly why panel 03 says barrier and not tunnelling. **Tunnelling implies a
> barrier; a barrier does not imply tunnelling.**

### "How do you know it isn't noise, or a short?"

> Four ways. **A short would be ohmic**, and our resistance falls by a factor of 3.7 across the
> sweep - 59 megohms down to 16. **An open circuit gives nothing**, and we had tens of nanoamps.
> **Drift cannot have made it**: the sweep was taken as eight rounds with the polarity interleaved.
> And **it reverses when the bias reverses**, on two separate nights. Noise does not do that - and
> that same bias-flip test rejected two false contacts, so it is a test that has said no.

**Source:** `sessions/2026-09-17-bench.md` 3.15; `LEAD_VERIFICATION.md` V2.

### "Your error bars look small for 53 readings."

**Concede it immediately - it is written on our own figure.**

> They are not 53 independent observations. They are repeated reads at **eight** bias settings,
> about 1.4 seconds apart, and three of the eight are the same zero-volt point revisited. **The
> independent unit is the setting, so n is 8.**
>
> There is a second limit, also on the figure: **the slope is really the ratio of two nominally
> 100 megohm resistors whose tolerances we never recorded.** So it confirms the scale to within
> those tolerances rather than independently of them. **What it does prove regardless is that the
> whole current path works end to end** - twelve stages, and a fault anywhere would have shown as
> points off the line.

**Source:** `LEAD_VERIFICATION.md` V1.

### "Isn't p = 0.0036 significant? That looks like a real result."

**This is the sharpest question on the poster, and the answer is the best thing on it. Panel 06.**

> On its own it would be. But we ran **209 reproducibility tests** across this data, and at that
> many, a one-in-twenty threshold throws up about ten apparent findings from nothing at all. **So
> the honest threshold is about p < 2.4 x 10^-4** - and we fixed that before we judged the
> candidates, not after. Our best run falls a factor of fourteen short of it.
>
> And the part that settles it for us: **an X-held control, which cannot contain a surface because
> the tip never moved sideways, scored p = 0.020 on the same statistic.** That is this instrument's
> own false-positive rate, and knowing it is worth more than any single positive would have been.
>
> We also ran the test that compares the same place across the two runs. **The same place agreed no
> better than a different place** - very slightly worse, p = 0.70.

**Source:** `deliverables/2026-09-19-pause/candidates/VERDICT.md` 1 and 4.

### "This isn't really a working STM, then."

**Do not get defensive. The true answer is better.**

> It is a working scanning-probe measurement chain that has not yet imaged. Every subsystem is
> built, working and calibrated: the converters, the amplifier, the current measurement, the coarse
> approach, the feedback loop and the analysis. **What is missing is mechanical stability, and we
> measured it rather than guessing.** Knowing precisely what stops you is most of the value in
> instrument development.

---

## 2. The common ones

### "What actually is a scanning tunnelling microscope?"

> You hold a sharp metal tip about a nanometre above a conducting surface - close enough that
> electrons cross the gap without the two touching - and you measure that current, which is around
> a billionth of an amp. The current changes enormously with distance, so if you sweep the tip
> across and keep the current constant, the height you needed is a map of the surface. That is how
> people get pictures of individual atoms.

### "Why is it in a basement?"

> Because that was the point: it is an open design, and the idea is that you can do this at home
> with no experience. **And the basement turned out to be part of the science.** An STM is normally
> a clean-room instrument, and the thing that stopped us is exactly the class of problem those
> rooms exist to remove. We measured what the room costs you, in the instrument's own units.

### "What did you build, and what did you copy?"

**Say this without being asked. Panel 01.**

> The mechanics, the controller board and the firmware follow Mech Panda's open-source
> `red-panda-stm`. The scan head, the tip preparation and the transimpedance preamplifier follow
> Dan Berard's home-built STM. **Ours is the electronics bring-up, all the control and analysis
> software, the calibration, the controls and the fault isolation.**

### "What was the hardest part?"

> A fabrication fault we could not see. **The preamplifier boards came back from the board house
> missing a ground pour that the original design has**, so the amplifier's own reference pin was
> connected to nothing - on both boards. **Every amplifier measurement we took before 14 September
> was referenced to a floating node and was meaningless.** The repair was four wires on a board
> 20 mm long. Finding it took two weeks.

**Source:** `STATUS.md` fault 0d.

### "How do you know you are not fooling yourselves?"

**Panel 05, and it is the panel to be proud of.**

> The control. **Every scan was immediately re-run with the sideways sweep switched off** - same
> timing, same loop, same number of points, but the tip never travels across the surface. **A
> control like that cannot contain surface structure by construction**, so anything that turns up
> in both is us, not the sample. Our scans repeat no better than those controls do: +0.04 against
> +0.07, and neither differs from zero.
>
> And at this pause point we re-derived our own published numbers from the raw files and **found
> six of them wrong**, including two statistics we had used to dismiss our own results. **Every
> conclusion survived; two of the arguments for them did not, and we published the withdrawals.**

**Source:** `LEAD_VERIFICATION.md` V4 and V5; `report/FINDINGS_REPORT.md` 7.

### "Is the electronics noise not the problem?"

> No, and that is measured rather than assumed. **With no junction the chain is flat white noise at
> 8 to 14 counts** from 2 Hz to 1.2 kHz. **With a junction live it is 9 to 19 counts.** Leakage
> through the tip lead and holder is under 0.06 nA across plus and minus 2 V, which is more than
> 8 gigohms. And **somebody stamping on the floor two metres away moves a single reading's spread
> from 131 to 132 picoamps** - so the building is not getting in electrically either.

**Source:** `sessions/2026-09-17-bench.md`; `sessions/2026-09-19-bench.md` 3.3; `docs/FACTS.md`.

### "Is the gold real?"

> Yes - settled with a flame test. Imitation leaf is brass and blackens instantly; gold does not.
> **What we do not know is whether the tip was ever over gold rather than copper**: the window in
> our sample plate is not all gold, there is exposed copper tape to one side, and nothing
> electrical distinguishes them. It is on our open list.

### "Why not put it on an air table, or in a vacuum?"

> Those are the right answers if you have them. We do not, and part of the point was to find out
> how far you get without. **The cheapest test we have not yet run is a cardboard box over the
> instrument** - that removes air currents for nothing, and it is first on the list.

### "What is next?"

> Four things, in order. **Measure `d` properly** - optically, because a straightedge cannot
> resolve it - which settles panel 06 and gives us a height scale. **Prove the gap holds still
> before scanning anything**: a box over it, a fifteen-minute recording, and a gate of about 200
> counts over sixty seconds. **A stiffer sample than gold leaf on paper, and a sharper tip.** And
> three software fixes that cost nothing and remove the artefact behind our most convincing false
> positive.

### "Can I see the code and the data?"

> All of it, including the mistakes: `github.com/jacobbkatz/We-Are-STMING`. Every session log, every
> raw data file, every analysis script.

**Check the repository is actually public before you say this.** If it is not, say "I can send it
to you" and take their email.

---

## 3. If they ask about a specific number on the poster

| They point at | The honest sentence |
|---|---|
| **0.13 sigma** | Measured gain against what Ohm's law required, worked out before the run: -3,204.8 +/- 36.5 counts per volt against -3,200 predicted, R-squared 0.9934. Panel 02. |
| **4 pA** | The amplifier's own input current, measured on the repaired board on 15 September - about 250 times smaller than the 1 nA signal it has to find. |
| **16-59 megohms** | The junction's resistance across our I-V sweep. It falls as the voltage rises, which is the point: a resistor would not. |
| **9-19 counts** | The noise with a junction live, 19 September. With the tip clear it is 8 to 14. |
| **8 weeks** | Boards ordered to a working junction. First power-on 29 August, last bench session 19 September. |
| **43,000 counts in 6.4 s** | How far the surface moved with the motor stopped and nobody touching the instrument. It then went out of reach for 105 seconds. Panel 04. |
| **+0.04 against +0.07** | How well our scans repeat, against how well a control with nothing in it repeats. Panel 05. |

---

## 4. Questions with no answer in the repository

**Do not improvise these. The correct answer is that we have not measured it.**

| Question | What to say |
|---|---|
| **"What did it cost?"** | **We have never totalled it.** `docs/BOM.md` lists every part, but no total is recorded anywhere, so any number said on the day would be invented. Say: *"I have never added it up - the full parts list is in the repository."* **If Jacob knows the figure, write it into `docs/INVENTORY.md` and then it can be quoted.** |
| **"How big an area can you scan?"** | In counts only: the wide runs on the poster sweep 15,000 counts either side of centre, the close ones 1,500. **In nanometres we cannot say**, for the same reason there is no scale bar. |
| **"What is your resolution?"** | **We have not established one, and it has to be that way** - resolution is a distance, and we have no measured distance scale. What we can quote is current: one converter count is 3.125 picoamps. |
| **"How far does one Z count move the tip?"** | **Unknown for this instrument.** The 0.016 nm per count in circulation is inherited from another builder's scanner. We can derive about 0.0155 nm from our own geometry, and the two agree to 3% - **but that derivation divides by a counts-per-motor-step figure our own record marks SUSPECT, and it needs `d`, which is CONTESTED.** So: a first estimate, not a calibration. |
| **"How fast can it scan?"** | The loop holds current to about 0.06 of a decade at 2,000 pixels per second, measured 17 September. **Whether that is fast enough for an image is not known**, because the gap moves first. |
| **"Is the shield continuous?"** | **We have never metered it.** It is on the open list; it takes two minutes with a meter and we have not done it. |
| **"What is moving the gap?"** | **Unknown - five candidates, none tested:** the leaf on its backing paper, the plate on its rubber bands and three balls, thermal motion of the printed parts, air currents, and relaxation after a motor move. |

---

## 5. If somebody offers advice, take it and write it down

**This is the most valuable thing that can happen at the event.** People who have fought sample
mounting, approach mechanics and cabling on a suspended stage know things that are in nobody's
documentation.

**Ask specifically:**

- **"How do you mount a sample so it does not move?"** Ours is gold leaf on backing paper, held by
  two twisted rubber bands, and it is one of five suspects for the gap wandering.
- **"How do you get cables onto a suspended stage without spoiling the isolation?"** Our own
  photographs show an orange lead and a four-way bundle crossing from the suspended platform to the
  fixed bench, with no strain relief visible in any frame.
- **"Does any of this look like something you have seen before?"** Then be quiet and listen.

**Write down what they say, with their name, on the day.** It goes into `docs/INVENTORY.md` or
`docs/OPEN_QUESTIONS.md` in the same session - otherwise it is lost, which is exactly how this
project has lost things before.
