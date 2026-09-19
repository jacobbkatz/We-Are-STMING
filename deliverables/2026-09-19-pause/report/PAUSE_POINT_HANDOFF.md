# Pause-point handoff — the state of the project on 2026-09-19

**Written to be picked up with no memory of any conversation**, weeks or months later, possibly on
a different computer, **with the instrument disassembled and moved.** If you are reading this and
you were not here, this file plus `STATUS.md` plus
[`docs/NEXT_SESSION_PLAN.md`](../../../docs/NEXT_SESSION_PLAN.md) is everything you need to start.

**Authority.** `STATUS.md` is the live state and wins over this file. **This file adds one thing
`docs/NEXT_SESSION_PLAN.md` does not have: a priority order with the reason each item is worth
doing, and a list of what in that plan is now superseded.** It does not replace the plan and it
issues no new bench procedure.

---

## The conditions this was built in — and why whoever picks this up needs to know

**`SAID`, Jacob, 2026-09-19.** **Two first-year students. No coding experience. Very little
electronics experience — this project was their first real soldering. Built in a basement in a
lived-in house, with people moving around and no control of the air or the temperature.** The
photographs corroborate it: a wooden bench standing on a concrete floor, a few metres from a
breaker panel and a standby-generator transfer switch.

**This matters operationally, not just biographically.** An STM is normally a clean-room
instrument, and **the blocker measured here — the gap moving by most of its range in seconds — is
exactly the class of problem those rooms exist to remove.** So:

- **Do not read the gap motion as a mysterious fault.** It is the expected result in this
  environment, it was measured rather than assumed, and five candidate mechanisms are named.
- **The move is an uncontrolled change to the single biggest variable in the experiment.** A
  different house, floor, bench and mains supply may make the gap behave differently, in either
  direction. **Record the new room in `docs/INVENTORY.md` before the first measurement** — the
  floor type, the bench, what else is running nearby — so that a change in the numbers can be
  attributed rather than puzzled over.
- **Whoever is at the bench may be doing something for the first time.** The procedures in
  `docs/` are written for that and should stay that way.

---

## 0. The first fifteen minutes, in order

1. `git pull --ff-only origin main`.
2. Read **`STATUS.md`**, top blocks first. **It has been corrected twice on the last day of work**
   — two statistics were withdrawn — so read the imaging row carefully rather than skimming it.
3. Read **every session log carrying the newest date in `sessions/`**. **There is often more than
   one file for a date** and neither supersedes the other.
4. Read **`docs/NEXT_SESSION_PLAN.md`**, the block headed START HERE.
5. Run `python3 Code/pc/check_facts.py` **as its own command and read its exit code.** If it
   reports anything, fix that before starting work: it means a number known to be wrong is sitting
   somewhere it will be believed.
6. Read **section 1 below before touching the hardware**, and ask the questions in section 1.3
   before unpacking anything.

---

## 1. Where the instrument physically is

### 1.1 What is known

**`SAID`, Jacob, about 14:19 UTC 2026-09-19:** *"We are now taking it apart and moving it to News
House as I'm flying to San Diego for college. We will probably continue a little bit less
frequently over the next few months."*

- **"News House" is read as Nuh's house.** That is an inference from speech-to-text, **not
  confirmed.**
- **Work is expected to be less frequent.** Plan for sessions that are weeks apart, and for the
  person at the bench not being the person who last touched it.

**What the photographs show, all `READ` and all from the morning of 2026-09-19** (camera-local
times; the teardown frames are from Nuh's camera, 10:05 to 10:16, and are catalogued in
`deliverables/2026-09-19-pause/photos/IMAGE_INVENTORY.md` §C3):

- Jumper leads unplugged and held; supply leads pulled; the electronics boxes open on the bench.
- The Teensy carrier and the stepper-driver board **out of their printed boxes**.
- **The suspended platform lifted off the frame in one piece**, with the scan head, the stepper
  and lead screw, the preamp box and the coin cups still mounted on it.
- **At least one spring eyebolt visibly empty**, so at least one spring came off.
- The copper Faraday enclosure **off** the instrument and in hand, in a different room.

### 1.2 What is UNKNOWN, and must not be assumed

| | |
|---|---|
| **How it was packed** | **No photograph shows anything going into a box.** The record stops at 10:16 |
| **Whether the three springs were kept, and where** | One eyebolt is empty in the last frames; nothing says what happened to the springs |
| **Whether the sample plate stayed on its rubber bands** | **Rubber perishes over weeks.** Assume nothing about their condition |
| **Whether the tip is still fitted, and whether it survived** | The tip fitted at about 03:00 on 2026-09-19 was already *"very blunt"* (`SAID`) and had been pressed into the gold with Z fully retracted for several minutes on four occasions that day. **It should be replaced regardless** |
| **The last parked state** | ~~Powered off, side screws backed off 2 full turns, covered~~ — **superseded by the move.** `STATUS.md` says so explicitly. **Nothing about the parked state can be assumed** |
| **Whether the gap back-off still means anything** | The two-turn back-off applied to **that** tip and **that** sample. Either may change |
| **Where each subassembly now is, and who has it** | Not recorded anywhere |
| **Whether anything was damaged in transit** | Not recorded anywhere |

### 1.3 Ask these before unpacking

**One question costs a sentence. A wrong assumption about what is in the room costs a purchase, a
rework or a part.** Whatever the answers are, **write them into
[`docs/INVENTORY.md`](../../../docs/INVENTORY.md) the same day** — that is the only file that
records physical reality, and facts that stay in a conversation are lost.

1. What came apart, and what is in which box now?
2. Were the three suspension springs taken off and kept?
3. Did the sample plate stay on its rubber bands, and is the gold sample still on it?
4. Is the tip still in the holder?
5. Did anything get dropped, crushed or bent?
6. Is the bench, the room and the mains supply the same as before, or is this a different place?
   **The room matters**: the last one was a basement utility room, a wooden bench on a concrete
   floor, a few metres from a breaker panel.

---

## 2. What works — do not spend bench time re-proving these

| | |
|---|---|
| **The measurement chain, end to end** | Calibrated against theory to 0.13 of a standard error, MEASURED 2026-09-16. See the findings report §3.1 |
| **The amplifier** | About 4 pA of input current in its box, MEASURED 2026-09-15 |
| **The electronics as a noise source** | Flat white at 8 to 14 counts, 2026-09-17; tip-clear scatter 41.8 counts and 60 Hz line content 10 counts, 2026-09-19. **Not the problem** |
| **Building vibration arriving electrically** | Eliminated: still against stamping, 41.8 against 42.3 counts, 2026-09-19 |
| **Motor direction** | **Negative approaches**, settled at the bench 2026-09-17 and confirmed on 2026-09-19. **Re-check after any change to the tip holder** — the lever's short arm is 1 mm |
| **Z direction for the tip that was fitted** | **HIGH Z extends toward the sample**, 4.2 standard deviations at a clean touch, and the loop held with that sign for eight runs. **This is a property of that tip's fitting, not of the instrument. Re-check it whenever the tip changes** |
| **Tools that worked on hardware** | The live back-off beeper, the chunked motor approach, and the Z test |
| **Tools that did NOT** | The tuned feedback loop never held on hardware on 2026-09-19 — every tuned image aborted at a clamp |
| **Two tip-destroying firmware faults** | Found and fixed, and each was tested by deliberately reproducing it first |

---

## 3. What is open

**Canonical home: [`docs/OPEN_QUESTIONS.md`](../../../docs/OPEN_QUESTIONS.md).** The science
summary is in [`FINDINGS_REPORT.md`](FINDINGS_REPORT.md) §8. The four that shape the plan below:

1. **What moves the gap.** Five candidates, none tested: the leaf on its backing paper; the plate
   on its rubber bands and three ball contacts; thermal motion of the printed parts; air currents;
   and post-move mechanical relaxation.
2. **The Z scale in nanometres**, which is inherited from another scanner and has never been
   measured on ours.
3. **Whether one three-Y measurement that looked like topography was real.** It cannot be settled
   with the data that exist.
4. **What the mirrored, line-periodic signal in the wide images is.** Three candidates, none
   tested.

---

## 4. What must be re-verified before power

**This is the order in `docs/NEXT_SESSION_PLAN.md`'s REASSEMBLY block, which is canonical.** It is
restated here only so that this file can be handed to someone on its own. **Every protective check
comes before the risky step it protects, and that ordering is deliberate.**

1. **`git pull` on whatever computer runs the session**, then install the Python requirements.
   **The 2026-09-19-morning scripts run only on Jacob's laptop** — absolute paths and a
   Windows-only sound module — so on another computer use the portable tools in `Code/pc/`, which
   find the Teensy by its USB vendor ID, or promote the scripts first. **On Windows type `py`, not
   `python`**: `python` and `python3` are Microsoft Store placeholders on Jacob's machine.
2. **Rewire from `docs/WIRING.md`, not from memory and not from photographs**, and **verify
   unpowered** with the plan's "unplug the DB9 and beep it" method. **Read its colour trap section
   first.**
3. **Bring up from cold** with `docs/soft_launch_test_procedure.md` stages 0 to 6 and
   `docs/DAC_BOOT_STATE.md`. **Supplies first, then USB.**
4. **Check LED1 to LED4 before anything is sent, and after every measurement.** There is no
   software substitute: the alert pins are not wired to the Teensy. **Any reading taken with one
   lit is void.** They are lit at every power-on; a reset clears them.
5. **Mechanics, by eye and meter:** the sample plate on all three balls; the motor screw's ball
   actually touching the plate (once found turning in free space); **fresh rubber bands**; the tip
   holder open to the brass piezo electrode when metered, which is the check owed before first
   imaging; the suspension hanging free; and **no cyanoacrylate anywhere near the preamp or in its
   enclosure**.
6. **Re-check the Z direction** before running any script that assumes one.
7. **Record what was reassembled, how, and by whom in `docs/INVENTORY.md`, the same day.**

**Standing prohibitions that have not been lifted** — they are `STATUS.md`'s numbered list, which
is the only citable one:

- **Do not run `APRH`** until the sign of the tunneling current is known. It was measured on
  2026-09-16 and **the rule was still not lifted**; that is Jacob and Nuh's decision to make.
- **Never send `CCON` with a tip in range**: engaging the loop snaps Z to midscale in the old
  firmware, and although the fix passed a bench test the rule is kept until they decide otherwise.
- **Keep every DAC argument between 0 and 65535.** An out-of-range value does not error; it
  silently jumps the axis to the opposite rail.
- **Never raise either serial clock above 1 MHz.** The ribbon cannot carry more.
- **A multimeter cannot clear a suspect leakage path in this project.** "OL" only proves more than
  about 60 MΩ, and the range that matters starts there.
- **No preamp measurement is valid while anyone is leaning over the board**, or within about a
  metre of it. **The old figure for how much a body injects is not established; the rule stands.**
- **A decision is owed on where to park Z before the motor moves.** The standing rule says
  midscale; every motor move on 2026-09-19 parked at the retracted end instead. **That is Jacob and
  Nuh's to amend or keep, not ours** — but it should be settled before the next motor move rather
  than discovered mid-session.

---

## 5. The priority list

**Ordered by value for effort, with the reason each is worth doing and what its outcome means.**
**Everything from P4 down is blocked by P4 itself:** while the gap moves more than the signal,
every imaging statistic measures the gap.

### P0 — Reassemble and re-verify. The gate on everything

Section 4. **Nothing else in this list is meaningful until it passes**, and it is also the point at
which the inventory questions in §1.3 get answered and written down.

### P1 — Three software fixes that cost nothing and can be done NOW, with the instrument still in its box

**These need no hardware.** They can be done on any computer, during the pause, by whoever has
time. **Between them they remove the artefact that produced this project's most convincing false
positive.**

1. **Discard the first three pixels of every pass, in the tool** — `--skip-lead 3` in
   `Code/pc/stm_y_control.py` and `Code/pc/stm_feedback_scan.py`, **writing the skipped points to
   the file anyway so nothing is lost.**
   **Why:** the loop begins each pass recovering from a 3,144-count step, and that recovery is the
   whole of the 636-count "image" that stood as the project's best candidate for two days.
2. **Make every image-to-image comparison refuse a shape mismatch instead of truncating to the
   shorter file.**
   **Why:** two published dismissal statistics were computed over 21 and 42 points instead of 231,
   because an aborted scan leaves a file that still parses. **And the check must be shown RED
   against a one-line file before it is believed** — a test that has never failed has not been run.
3. **Sweep X back and forth between passes as well as within a line.**
   **Why:** the 2D images already do this and have no start-of-pass transient; the line-repeat tool
   does not, and that is the entire mechanism behind item 1.

**Three more of the same kind, from the plan and from the analysis:**

4. **Write CSV rows as they are taken.** Four files were lost on 2026-09-19 because rows were
   written only on a clean exit and the processes were stopped.
5. **Promote the scratch tools** — the Z test, the chunked approach, the back-off beeper and the
   stillness logger — into `Code/pc/` with tests, **with the Z direction as a parameter rather than
   assumed**, and with no absolute paths. **The live back-off beeper is the method that actually
   worked for setting the gap by hand and it exists only on Jacob's laptop.**
6. **Add the four missing files to `sessions/data/2026-09-17-bench/README.md`.** They were missing
   from the only index of that directory, which is the likeliest reason a session spent a day
   believing an experiment had never been run when its data were sitting there.

### P2 — Two mechanical measurements that need no electronics, best done during reassembly

1. **The tip-to-pivot-line distance.** Plate off, lay a straightedge across the two side-by-side
   ball ends, and record which side of that line the tip stands on and by how much.
   **Why:** it sets the lever ratio and therefore **the Z scale in nanometres**, which is currently
   inherited from a different scanner and never measured on ours. `docs/OPEN_QUESTIONS.md` calls it
   the most valuable unmeasured number in the instrument. **At the design's 1.00 mm the measured
   current decay is thirty times too slow for vacuum tunnelling; at 0.1 to 0.3 mm the same
   measurement lands near the textbook figure.** One distance decides how every distance result is
   read. **It cannot be taken from a photograph** — three attempts differed by more than a factor
   of two.
2. **The suspension droop with a known added mass.** Measure the droop, add a known weight, measure
   again with the same ruler.
   **Why:** it gives the spring rate and the suspended mass together, and it settles whether the
   springs are carrying any load at all. The current arithmetic says **they are shut — below their
   initial tension, behaving as stiff wire** — which would mean the isolation is not engaged, and
   that **adding a few hundred grams may be the fix rather than the problem.** That reverses
   earlier advice and it deserves a measurement, not another calculation.

### P3 — The free test: is it air?

**Put a cardboard box over the whole instrument, standing on the bench and not on the platform, and
leave the room.** Then run the stillness test with the box on.
**Why:** it costs nothing and it tests one of the five candidate causes outright. **If the gap
holds still with the box and not without, that is the answer.**

### P4 — Prove the gap holds still. This is the gate on all imaging

Right after finding the surface, with the motor still, sweep for the surface repeatedly and log
where it is.

**Two acceptance thresholds are on record and they differ. Settle which before running it:**

| Source | Threshold |
|---|---|
| `docs/NEXT_SESSION_PLAN.md` | the onset stays within about **500 counts for 15 minutes** |
| `deliverables/2026-09-19-pause/candidates/VERDICT.md` §6 | the onset holds within about **200 counts over 60 seconds** |

**Any sweep that reports the surface out of reach voids the run** — on 2026-09-19 the logger read
"out of reach" throughout after a hand-set, and that cannot distinguish a still gap beyond reach
from a moving one.

**Why it is the gate:** the gap currently moves 396 to 1,722 counts over the five seconds an image
takes, and the structure in every candidate image is 29 to 458 counts. **Until that ratio inverts,
no analysis can recover a picture.**

### P5 — A stiffer sample and a sharper tip

**In the plan's order of preference for the sample:** a rigid gold surface (anything gold-plated
and flat that does not bend); HOPG, which is the standard hobby-STM sample and **is a purchase, so
decide only after P3**; or the leaf bonded all round with conductive adhesive under it and **no
paper**. **Check `docs/INVENTORY.md` and ask before assuming any of these is in the room.**

**Why:** the backing paper under the gold is roughly 50 to 100 µm of compressible cellulose
directly beneath the measurement surface, and the tip was blunt and had been pressed into the gold
repeatedly. **Neither is proven to be the cause and a rigid sample is the test.**

### P6 — Re-measure the junction, then run the one decisive imaging experiment

**First re-measure the Z test on the new tip and sample and put its own counts-per-decade into the
loop, immediately before scanning** — on 2026-09-19 that constant drifted about fivefold inside a
single run, so a value measured an hour earlier is not the value.

**Then the experiment that settles the one candidate this project could not close:**

> **Repeat the three-Y control at 12,000 Y separation and ±15,000 X, three times, with an X-held
> control INTERLEAVED between them — not run at the end.**
>
> - **The interleaved control is the point.** An X-held run, which cannot contain a surface, scored
>   p = 0.020 on this exact statistic on 2026-09-19. **A positive cannot be read until a control has
>   been run in the same conditions.**
> - **Analyse with the permutation test, not the printed sigma.** The code is in
>   `deliverables/2026-09-19-pause/candidates/code/07_chance.py`.
> - **Decision rule, fixed in advance and written down before the first run: the effect is real
>   only if all three real runs beat all interleaved controls.** One positive out of three is what
>   2026-09-19 produced and it means nothing.

**Why this one:** it is the only measurement in the project that has ever looked like topography,
its non-reproduction is real, and **"it did not repeat" and "the surface moved out from under it"
cannot be told apart in the existing data.** It is the strongest surviving form of the idea that a
real result was thrown away, and it has a four-run answer.

### P7 — Find out what the mirrored signal in the wide images is

**Run the wide ±15,000 image at two X speeds — the normal one and one four times slower — with an
X-held control at each speed.** Four images.

**Why: all three possible outcomes are informative**, which is rare.

| If the structure keeps the same period in… | …then it is |
|---|---|
| **pixels** | locked to the scan — the feedback loop hunting |
| **time** (half as many cycles per pass at quarter speed) | a mechanical disturbance around 4 to 5 Hz being sampled by the raster |
| **X**, with the amplitude falling as the speed falls | **the tip dragging a compliant sample** — which would be the first direct measurement of the gold's softness, and fits the "soft, pressed, sticky contact" reading on record |

### P8 — The documentation fixes, when there is a quiet hour

**Twenty-one of them are listed with file, line, evidence and a recommended fix in
`deliverables/2026-09-19-pause/manual/INCONSISTENCIES.md`, graded by severity.** The five graded A
can cost a bench session; the one that matters most is that `docs/COMMANDS.md` says the approach
tool "is planned but not yet written" **when it exists, has 40 passing tests, and is the only
approach route used since 2026-09-16** — a reader who believes it is left with no alternative to
the one command the project forbids.

---

## 6. What in `docs/NEXT_SESSION_PLAN.md` is now superseded

**Do not edit that file on the strength of this list — hand it to whoever owns it.** It remains the
canonical bench procedure and its REASSEMBLY block is sound.

| In the plan | What changed |
|---|---|
| *"How it was left before the move: side screws backed off 2 full turns, covered"* | **Superseded by the move**, and the same block already says nothing about the parked state can be assumed. **The two sentences contradict each other**; the second is the right one |
| Step 5, prove the gap holds still, *"within ~500 counts for 15 minutes"* | **A second threshold now exists** — about 200 counts over 60 seconds, from the pause-point verdict. **Pick one and write it into the plan** |
| The verdict's own text says the stillness test is *"step 4"* of the plan | **It is step 5.** A citation to fix, in the verdict rather than the plan |
| Step 6, *"scan with X-held controls"* | **Now needs the decision rule and the interleaving** from P6 above, and the permutation test rather than the printed sigma |
| Nothing in the plan mentions the start-of-pass transient | **P1's three tool fixes belong in it**, before any future scan |
| Nothing in the plan mentions the two withdrawn statistics | **`STATUS.md` now carries both withdrawals.** A reader who goes to the 2026-09-19 session logs for a reproducibility figure will find numbers that have been withdrawn, and the plan should say so |
| The plan's "software to do" list | Already carries "write CSV rows as they are taken", "promote the scratch tools" and "give every hardware script a self-test". **P1 adds the three scanning fixes and the missing index entries** |

---

## 7. Where everything is

| What | Where |
|---|---|
| **Live state, faults, the numbered safety rules** | `STATUS.md` |
| **The bench procedure** | `docs/NEXT_SESSION_PLAN.md` |
| **Every canonical number, with provenance and a retired list** | `docs/FACTS.md` |
| **Every open question** | `docs/OPEN_QUESTIONS.md` |
| **What is physically in the room** | `docs/INVENTORY.md` — **not `docs/BOM.md`, which is a specification** |
| **Pinouts, colours, LEDs, the power tree** | `docs/WIRING.md` |
| **Every firmware command** | `docs/COMMANDS.md` |
| **The consolidated manual, written at this pause point** | `deliverables/2026-09-19-pause/manual/MANUAL.md` |
| **The plain-language findings report** | `deliverables/2026-09-19-pause/report/FINDINGS_REPORT.md` |
| **The full data re-derivation** | `deliverables/2026-09-19-pause/analysis/` |
| **The imaging verdict and the candidate gallery** | `deliverables/2026-09-19-pause/candidates/` |
| **All 92 photographs, catalogued and marked** | `deliverables/2026-09-19-pause/photos/IMAGE_INVENTORY.md` |
| **The six finished figures** | `deliverables/2026-09-19-pause/figures/png/` |
| **Raw bench data, read-only** | `sessions/data/<session>/`, each with its own README |
