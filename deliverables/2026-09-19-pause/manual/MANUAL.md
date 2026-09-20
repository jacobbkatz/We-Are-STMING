# The We-Are-STMING instrument manual

**A single consolidated operating manual for the 3D-printed scanning tunnelling microscope built
by Jacob Katz and Nuh Shaheer.**

**Written 2026-09-19**, at the pause point, for two people who do not write code, who will come
back to this after weeks or months, possibly on a different computer, **with the instrument taken
apart and moved.**

---

## Read this before you read anything else

**This manual has no independent authority.** It is a consolidated, current reading of documents
that already exist in this repository. Where it disagrees with any of the files below, **they win
and this file is the one to fix.**

| If you want | Go to |
|---|---|
| Where the build actually is, the open faults, and the **numbered safety rules** | `STATUS.md` |
| The canonical value of any number | `docs/FACTS.md` |
| What to do next at the bench | `docs/NEXT_SESSION_PLAN.md` |
| Verified pinouts and cable colours | `docs/WIRING.md` |
| Every firmware command in detail | `docs/COMMANDS.md` |
| What is physically in the room | `docs/INVENTORY.md` |
| Every open question, UNKNOWN and VERIFY | `docs/OPEN_QUESTIONS.md` |

**Safety rule numbers in this manual always mean `STATUS.md`'s numbered list.** That is the only
citable numbering in the project. `CLAUDE.md` section 4 has a deliberately unnumbered summary;
never cite a number against it.

**Three marks are used throughout, the same ones the repository uses:**

- **MEASURED** — someone read it off our own hardware, with a date.
- **SAID** — Jacob or Nuh told us. Good, but it is a statement, not a measurement.
- **UNKNOWN / VERIFY** — nobody has established it. **These are not oversights.** A confident
  wrong number costs hardware here.

**A photograph is not a measurement of our hardware.** Nothing in this manual takes a dimension,
a part marking or a colour off a photograph.

**How these rules are enforced, rather than merely stated, is section 1.4.** It describes the
framework the project runs inside — the single canonical register of numbers, the provenance tags
above, the append-only session logs and the seven automated checks. **Read it if you want to know
how much to trust the rest of this document.**

---

## Table of contents

1. [What the instrument is](#1-what-the-instrument-is)
   - [1.4 The second instrument: the system that runs the science](#14-the-second-instrument-the-system-that-runs-the-science)
2. [Which revision you are holding](#2-which-revision-you-are-holding)
3. [Assembly and connections](#3-assembly-and-connections)
4. [Sample and tip](#4-sample-and-tip)
5. [Startup and shutdown](#5-startup-and-shutdown)
6. [Operation: every command](#6-operation-every-command)
7. [Data collection](#7-data-collection)
8. [Analysis](#8-analysis)
9. [File organisation: which document owns what](#9-file-organisation-which-document-owns-what)
10. [Troubleshooting](#10-troubleshooting)
11. [How to resume the project after the move](#11-how-to-resume-the-project-after-the-move)
12. [What is still unknown, and what is untested](#12-what-is-still-unknown-and-what-is-untested)
- [Appendix A: glossary](#appendix-a-glossary)
- [Appendix B: figures](#appendix-b-figures)

---

# 1. What the instrument is

## 1.1 In one paragraph

A scanning tunnelling microscope holds a sharp metal tip about a nanometre above a conducting
surface, puts a small voltage between them, and measures the tiny current that quantum-mechanically
tunnels across the gap. That current changes about tenfold for every 0.1 nm of gap change, which is
what makes the instrument sensitive enough to see atoms. **Ours is built from 3D-printed parts**,
following **Mech Panda's `red-panda-stm`** for the mechanics, firmware and controller board, and
**Dan Berard's home-built STM** for the scan head and the transimpedance preamplifier.

**Where the project stands, in Jacob's words and in one sentence:**

> ## **"We detected tunnelling, but weren't able to maintain tunnelling range for long enough to get an image."**

**Both halves are separately supported, and the order matters.** We detected tunnelling: the tip
cannot go from not touching to touching without passing through the separations where tunnelling is
the only thing carrying electrons, and the bias was on with the amplifier recording the whole way —
**60,928 readings inside that current range, across 109 approaches**. We could not maintain
tunnelling range: with the motor stopped and nobody touching the instrument the gap moves **at
least 43,000 Z counts in 6.4 s** and **at least 56,000 over about two minutes**, where an image
needs it inside a few hundred counts for a minute. **And one measurement would settle our best
junction retroactively** — `d`, the tip's distance from the pivot line, resolved to 26 micrometres
rather than bounded under 0.5 mm. It needs a loupe and no power.
[`../FRAMING.md`](../FRAMING.md); [`../LEAD_VERIFICATION.md`](../LEAD_VERIFICATION.md) V13.

**What it demonstrably does today** (all MEASURED, all in `docs/FACTS.md` and the session logs):

- **The measurement chain works end to end and is calibrated.** A 100 MOhm dummy junction gave
  −3,205 +/− 37 counts per volt against −3,200 predicted, 53 readings, R-squared 0.993. That is
  the project's strongest single result.
- **A real tip-to-gold junction has been made**, repeatedly, and its current responds to Z and to
  the sign of the bias.
- **That junction was a tunnel junction, and the current tunnelling through it was measured.** The
  tip starts with no measurable current and ends in saturating contact, so on every approach the
  separation passes through the range where tunnelling is the only mechanism that carries
  electrons; the bias was on and the amplifier recording throughout, **60,928 readings inside that
  current range across 109 approaches**. The junction never metallically shorted — resistance never
  fell below about 5 MOhm even at saturation — the I-V is superlinear and symmetric, and 109 of 110
  onsets were gradual. **So it was a barrier, conducting by tunnelling, and not a metallic bridge.**
- **The electronics are quiet enough.** Tip clear, the reading's standard deviation was 40–42
  counts on 2026-09-19; with a junction and X held it was 9–19 counts. A tunnelling current is
  about 1 nA, which is about 320 counts.

**What it has not done:**

- **No image has been produced.** Every feedback scan is matched or beaten by its own X-held
  control, so nothing in them is established as surface structure. No atomic resolution, and no
  distance in nanometres from our own hardware.
- **No controlled vacuum gap has been held** — the STM regime you need in order to scan. That is a
  different claim from the bullet above, and it is the one our data does not support: on 2026-09-19
  the current changed by a factor of ten per roughly 1,650–1,970 Z counts going in, where tunnelling
  on the inherited (and unmeasured) Z scale would be about 6–13 counts, and every run showed
  705–1,868 counts of in/out hysteresis. The interpretation on record is **"a soft, pressed, sticky
  contact"** — marked as interpretation, not proof. **Tunnelling through a pressed film is still
  tunnelling; it is not a gap you can command, sweep and image with.**
- **The gap does not hold still.** With the motor and hands still, it moved by most of the Z range
  within seconds to minutes. **What moves it is UNKNOWN**; `STATUS.md` carries **seven untested
  candidates** — the gold leaf on its backing paper, the sample plate on its rubber bands and ball
  contacts, thermal motion of the printed head, air currents, the undressed cables crossing from the
  suspended platform to the fixed bench, the coin mass standing tall and unrestrained, and the
  spring-hook-in-eyebolt joints. **The last three came from the photograph review and are not
  evidence** — a photograph shows what is touching what, never what moved.

**So the blocker is mechanical, not electrical.** That is the single most useful sentence in this
manual, because it tells you where not to spend time.

> **The five mechanical blockers are ranked, with a cost-to-fix table, in
> [`../WHAT_HELD_US_BACK.md`](../WHAT_HELD_US_BACK.md).** It opens with what was **not** the
> problem — the electronics — and then ranks the gap not holding still, the soft unbonded sample,
> the blunt tips, having no distance scale of our own, and an approach too coarse to park inside
> the 0.17 nm window. **None of the five needs a purchase and none needs a laboratory.** This
> manual does not restate them; go there.

## 1.2 The subsystems, and what each one does

### The frame and the vibration isolation

A printed tower — `new_body` at the bottom, `new_topframe` at the top, joined by **three M8
threaded rods** — carries a **Ø200 mm printed platform disc** hanging on **three extension
springs**. Under the platform sits an **aluminium plate moving between fixed magnets**: eddy-current
damping, with no contact.

The springs are identified from Jacob's own order record: **FOCMKEAS, 304 stainless, wire
Ø0.50 mm, OD Ø3.00 mm, 300 mm free length, double hook**, ordered 2026-06-21. Their rate is
calculated at about 58 N/m each, 173 N/m for three, with an initial tension of roughly 2.0 to 3.0 N
each — meaning **610 to 910 g of total load has to hang on them before they stretch at all**
(`docs/FACTS.md`, CALC 2026-09-19).

**The state as of 2026-09-19: mass has been added and the springs have almost certainly opened.**
356.2 g of coin is on the platform — 10 US nickels in the printed cups plus three paper wrapper
tubes of 18 quarters each — and Jacob had to raise the platform with the printed height adjusters
afterwards, which is the evidence that it sagged. **The adjusters are now at maximum**, so there is
no headroom to correct another sag. **Do not add more mass.**

> **Two things about this subsystem are still UNKNOWN and one of them decides whether it works at
> all:** the platform-to-tower clearance has never been measured (Jacob: *"its not sitting on the
> tower is just about its a perfect fit"*), and the damping gap between the aluminium plate and the
> magnets has never been measured. Reaching the calculated 2 Hz needs room below the platform to
> droop into, and nobody knows how much room there is.

### The scan head

Three printed plates bolted to a base:

- **`BasePlate`**, 100 x 70 x 10 mm, sits on the platform.
- **`PiezoPlate`**, 55 x 70 x 15 mm, carries the piezo disc in a Ø20.500 mm seat over a Ø18.000 mm
  free-flex bore, and carries **three 1/4"-80 fine-adjust screws** in brass inserts.
- **`SamplePlate`**, 12 x 70 x 49 mm, holds the sample and is pressed against the ball ends of
  those three screws by **rubber bands**.

**The lever.** Two of the three screws sit side by side, 35.000 mm apart, and act as the pivot
line. The third screw, 40.000 mm away, is the one the motor turns. **The piezo pocket centre sits
1.000 mm from the pivot line, on the motor screw's side** (measured from the mesh). So turning the
motor screw moves the sample under the tip in the same direction, about 40 times less.

> **The lever ratio is the most valuable unmeasured number in the instrument.** The design geometry
> gives 40, but that assumes the tip sits at the disc centre. **The current bound is `d` under
> 0.5 mm** — `SAID`, Jacob, at the bench on 2026-09-20, *"I obviously can't measure 26 micrometers
> but it's less than 0.5 mm"*, superseding his 2026-09-18 estimate of *"between 1mm and 0mm its
> really hard to measure"*. **A straightedge takes it no further; an eyepiece or an optical
> comparator does.** It decides the Z scale in nanometres, and therefore whether the measured
> current-versus-Z slope is a held gap or a press. **`docs/FACTS.md` is the canonical home for it**;
> see also `docs/OPEN_QUESTIONS.md`.

### The coarse approach

A **28BYJ-48 geared stepper** through a **ULN2003 driver module**, wired **directly to the Teensy**
— not through the ribbon, and there is no motor circuitry anywhere on the controller board. It
turns the rear 1/4"-80 screw through a printed `ThreadAdaptor` and `MotorSupport`.

2048 steps per revolution, 0.3175 mm of screw travel per turn, so **155 nm per step at the screw**
and, divided by the lever, a few nanometres at the tip. **Direction: negative `MTMV` approaches,
positive retracts** — settled at the bench 2026-09-17 and confirmed by every motor approach since
that found the gold.

**The motor does not behave as a ruler.** On 2026-09-18 single steps shifted the surface by 14,000
to 29,000 Z counts when they shifted it at all, while runs of 20 to 40 steps did nothing, and
retract steps twice brought the gold into contact. Expect **100 to 250 steps of backlash after any
reversal**.

### The piezo scanner

An unbranded piezoelectric disc actuator — **Jessinie SKU `91410_30_JE`** (`SAID` 2026-09-17,
Jacob) — bonded into the `PiezoPlate` pocket, with four quadrant electrodes. The controller drives
it with **−(Z ± X)** and **−(Z ± Y)**, so one disc does all three axes.

> **Nothing about our own scanner's displacement has ever been measured.** The figures of about
> 34 nm/V in Z and 83 nm/V in X and Y come from **Berard's calibration of a different disc** and
> are marked INFER in `docs/FACTS.md`. **Our disc is not his disc.** Every nanometre figure for
> this instrument should be read as unsupported until our own scanner is calibrated.

**The four quadrant wires are identical bare enamelled copper with no colour code.** There is no
way to recover which quadrant is +X from any file or photograph. If the first image comes out
rotated or mirrored, that is why, and it is fixed in software.

### The tip and its holder

A **tungsten** tip (`SAID` 2026-09-18), cut from 0.25 mm wire, held in a socket soldered to a metal
stake which is **superglued to the underside of the piezo disc**, insulated from it. Tips push into
the socket, so they are swappable without rebuilding the scanner.

**The tip holder is part of the preamplifier's input node.** That has two consequences that matter
every time it is touched:

1. **`STATUS.md` safety rule 7 must be re-checked after any rebuild** — the tip holder must meter
   OPEN against the brass piezo electrode. A bridge there is a shunt straight across the amplifier
   input.
2. **What the "metal stake" is made of has never been written down.** If it is ferromagnetic, the
   four magnets sitting a millimetre or two behind the sample exert a pull that rises steeply as
   the gap closes — a second snap mechanism. **A spare magnet held near it settles this in ten
   seconds.**

### The sample

**Real gold leaf** — flame-tested (`SAID` 2026-09-17, Jacob) — about 100 nm thick, mounted on the
`SamplePlate`. The plate's face is covered in aluminium tape with a square window cut in it; the
gold assembly sits in that window and is joined to the bias wire.

**The four disc magnets in the sample plate do nothing useful now.** They were put there to hold a
magnetic sample puck, as Mech Panda's HOPG came on. We put gold straight onto the plate instead.
They cannot move the gold (gold is diamagnetic; the force reaches about 7% of the leaf's own weight
even at 0.5 T) and they cannot make the noise (about 0.0063 pA against a 1 nA signal) — both ruled
out by arithmetic on 2026-09-18. **They might still stick the plate to its three steel ball screws,
and that is untested.**

### The preamplifier

An **OPA627 transimpedance amplifier with a 100 MOhm feedback resistor**, on a 20.625 x 15.23 mm
board, in a small printed box wrapped in copper tape and grounded, mounted at the centre of the
scanning module — right next to the tip, which is the whole point. **It converts tip current to
voltage: 1 nA becomes 0.1 V.**

The feedback resistor, the tip wire and the link to the op-amp's inverting input all meet **in the
air on a PTFE standoff**, because copper on a board surface would leak more than the signal.

**The board now in service is the repaired spare**, and it measures **about 4 pA of input current**
in its box (MEASURED 2026-09-15). That is 250 times inside the gate `STATUS.md` safety rule 14 set,
and it is why the preamplifier is no longer the blocker.

### The controller board

A 103 x 88 mm board carrying:

- **Four AD5761 16-bit DACs** — U1 (X), U2 (Y), U3 (Z), U4 (sample bias) — on one SPI bus.
- **Inverting summing amplifiers** U9 and U10, gain exactly −1 per input, which build the
  −(Z ± X) and −(Z ± Y) quadrant drives.
- **U13**, an OPA2227P, buffering the bias out to the sample.
- **An LTC2326-16 16-bit ADC**, U15, on a second SPI bus, reading the preamplifier through
  unity-gain buffers and a 103 kHz filter.
- **Its own regulators**: you feed it roughly ±18 V and it makes ±15 V, 5 V and 3.3 V.

### The Teensy and the PC

A **Teensy 4.1** runs the firmware, takes four-character commands over USB serial at 115200 baud,
and drives everything. **Python tools in `Code/pc/` talk to it.** `Code/pc/stm_console.py` is the
one to start with; it finds the board by USB vendor ID, so you never have to name a port.

## 1.3 The signal chain, end to end

```
   you type            Teensy 4.1           controller board            scan head
   --------            ----------           ----------------            ---------
 stm_console.py  USB  +-----------+ 26-way +----------------+  DSUB1  +-----------+
  "DACZ 50000"  ----> | 4-char    | ribbon | U1 X  --+      | ------> | piezo,    |
                      | commands  | -----> | U2 Y  --+ U9   |4 wires  | 4 quadrant|
                      |           |        | U3 Z  --+ U10  |         | electrodes|
                      |           |        | U4 bias-- U13  |         |           |
                      |           |        +----------------+         | tip ------+--+
                      |           |                    | DSUB2        +-----------+  |
                      |           | <---- U15 ADC <-- U21 <-- PREAMP+ <---------------+
                      +-----------+ SPI1  (LTC2326-16)        (OPA627, 100 MOhm)

   power:  bench supply, two channels, about +/-18 V --> U19 (3-pin JST) --> on-board
           regulators --> +15 V, -15 V, 5 V, 3.3 V, and +/-15 V out to the preamp
```

**Reading the current, in three steps:** the tip current times 100 MOhm gives volts; volts divided
by 0.3125 mV gives ADC counts. So **1 nA = 0.1 V = 320 counts**, and the ceiling the instrument can
measure at all is 102.4 nA. **MEASURED end to end on 2026-09-16 as 320.5 counts per nA.**

**The sign, and it matters:** a **positive voltage on the sample gives negative counts.** Current
flowing into the tip reads negative. `BIAS` codes above 32768 put a negative voltage on the sample.

## 1.4 The second instrument: the system that runs the science

**This section is here, near the front, because it is what tells you how far to trust the rest of
this manual.**

**Neither of us writes code. So the second thing we built was the system that does.** This
instrument was designed, assembled, characterised and documented by two undergraduates
directing an AI model, working inside a framework we built for it. **The model is off the shelf. The
framework is ours.**

### What the problem was

Two people, no prior programming and no prior electronics experience, working from two different
computers, days apart, in between other commitments. **The failure mode is not that the work is
hard. It is that a number gets corrected in one document and left standing in the eleven others
that quote it**, and six weeks later somebody builds on the stale copy.

That is not hypothetical here. **On 2026-09-07 two constants changed**, both had already been
written into more than a dozen documents, and correcting every copy anyone could think of **still
left stale values in six files.**

### What we built

| Component | What it is | Size |
|---|---|---|
| **The protocol** (`CLAUDE.md`) | The operating instructions the model must read before doing anything: which document outranks which, what to search before recording something as unknown, what to compute before giving an instruction that touches hardware, and what to do at the start and end of every session | **575 lines** |
| **The register** (`docs/FACTS.md`) | One canonical value for every number that matters, each with units, provenance and a date, plus a RETIRED table of every value that has ever been replaced | **164 rows** (2026-09-20; count table lines that are neither a separator nor a continuation) |
| **The checker** (`Code/pc/check_facts.py`) | Seven classes of automated test, run at session start and before every commit | **565 lines** |
| **The session record** (`sessions/`) | One append-only log per working session. Past measurements are never rewritten | **27 logs** |
| **The reference set** (`docs/`) | Wiring, commands, components, open questions, engineering cross-references, and an index of what is inside every binary and archive | **18 documents** |
| **The bench tools** (`Code/pc/`) | Python programs that talk to the instrument, analyse its output, and measure the printed parts straight out of the CAD meshes | **15 tools** |
| **The session hook** (`.claude/session-start.sh`) | Runs automatically: syncs both computers, reports the state, names every session log carrying the newest date, and runs the checker | — |

### The seven checks

Run `python3 Code/pc/check_facts.py` and it verifies:

1. No value the register lists as RETIRED is still sitting in a live document.
2. Every file path cited in prose actually exists.
3. No archived, superseded document is cited as if it were current.
4. Every "safety rule N" citation resolves, **and points at the rule it claims to**.
5. Every session log is indexed in `sessions/README.md`.
6. Every RETIRED entry's qualifying wording still matches the real text.
7. The next-session plan is not older than the newest session log.

**Checks 4 and 6 exist because both failure modes happened.** Rule numbering drifted between two
files until the same number meant different rules in each, and a retirement was written with a
qualifier that no longer matched the document it was guarding.

### Every fact carries where it came from

No number is stated without a tag saying how it is known:

**`MEASURED`** at the bench · **`CALC`** derived, with the inputs shown · **`DS`** from a
manufacturer datasheet · **`MESH`** measured out of the CAD file · **`ORDER`** from an order
confirmation · **`SAID`** stated by Jacob or Nuh · **`READ`** the model's reading of a photograph,
plausible and unconfirmed

**`SAID` and `READ` are deliberately the weakest tags, and they are the ones that have been wrong
most often.** One `READ` of a part marking off a shared photograph put a wrong component into five
documents before anybody asked whose board it was. It was not our board. Every edit was reversed,
and the rule that came out of it — *a photograph is not a measurement of our hardware* — is now in
the protocol, and at the top of this manual.

### What proves it works

**The system's output is not the documents. It is the retractions.**

| What was published | What the system did |
|---|---|
| "The controls reproduce better than the scans, +0.37 against +0.04" | Traced to a control file that was a single line long. **Withdrawn**, and the same defect was then swept across every other comparison in the project |
| A reproducible feature in the scan data, at 3.9 sigma | Found to be the feedback loop recovering from a horizontal flyback, predicted to the exact count. **Withdrawn** |
| The detector's full-scale voltage, in a live engineering reference | **Recorded backwards** — the corrected value listed as the retired one. Caught and fixed |
| A single commit's session log | **Eleven wrong numbers**, found by a verification pass and corrected before the second push |
| "d is 1.000 mm, and that settles the tunnelling question" | Wrong reading of what Jacob said. **Re-opened**, twice, and it is open now |

**Four of those five were the model's own errors, found by the framework the model was made to work
inside.** The fifth was found by Jacob, against a confident and wrong statement from the model.

### The honest boundary

**We did not train a model.** What we built is the scaffolding that makes a general-purpose model
usable as a laboratory assistant: the protocol, the single-source register, the provenance tags, the
append-only logs and the automated checks. **The model is off the shelf. The discipline is ours** —
and without it the same model produces confident, unverifiable, quietly-drifting prose, which is
what it did here before the framework existed.

**An AI that produces confident prose is not hard to get. An AI workflow that produces a retraction
is, and that is the part we built.**

### How to check any of this

```bash
wc -l CLAUDE.md Code/pc/check_facts.py   # the protocol and the checker
ls sessions/*.md | wc -l                 # the session logs
python3 Code/pc/check_facts.py           # the seven checks, run on the live repository
cat .githooks/pre-commit                 # what blocks a failing commit
```

---

# 2. Which revision you are holding

**This project has rebuilt the same three things several times, and older documents describe older
versions.** This section says what was fitted when the instrument was taken apart on 2026-09-19, and
what came before it, so that a sentence written in August is not read as describing today's
hardware.

> **Everything below describes the instrument as it was BEFORE it was taken apart and moved.**
> `SAID`, Jacob, about 14:19 UTC on 2026-09-19: *"We are now taking it apart and moving it to News
> House as I'm flying to San Diego for college."* **"News House" is read as Nuh's house and is an
> inference, not confirmed.** **What was taken apart, and how it was packed, is UNKNOWN.**
> **Re-confirm every row at reassembly and write what you find into `docs/INVENTORY.md` the same
> day.**

## 2.1 The preamplifier

| | |
|---|---|
| **In service** | **The repaired spare board**, since 2026-09-16. About 4 pA input current in its box |
| Previously | The original board, glued into a cyanoacrylate-contaminated box, with the tip coax cut. **It is retired.** Its famous offset reading was taken with the amplifier's own 0 V reference floating, so it was never a valid current at all |
| **Why they differ** | **The fabricated boards have no ground pour.** Berard's Eagle source has a bottom-layer ground polygon; the gerbers JLCPCB built from have none. Six points that should be ground each end at a dead via, including IC1 pin 3, the amplifier's reference input. **The spare was repaired with four 40 AWG wires to JP1 hole 1.** The old board was never repaired |
| **Consequence for old documents** | **Any preamp number dated before 2026-09-13 was measured on an amplifier whose reference floated.** Noise figures, warm-up drift, the body-proximity figure and three null sweeps are all in that category |
| **The box** | The **new** printed box, wrapped in copper and grounded. The original is out of the instrument and stays out |
| **C2** | **Still the reused tantalum**, desoldered and refitted with two irons, then rotated the right way round. Replacing it was Jacob's explicit decision not to do: *"we will not be replacing C2, executive decision."* The replacement part is not in the room |
| **The PTFE standoff** | A **Keystone 11301**. It **does not enter the board's Ø2.108 mm hole** — offered up at the bench 2026-09-15 and it would not go. The node was built with the standoff **resting on the board surface**, held by the 100 MOhm's own lead in tension. **Nothing was glued, drilled or forced** |

## 2.2 The tip

**Three tips have been fitted. Documents from different days mean different tips.**

| Era | What it was | What to know |
|---|---|---|
| 2026-09-16 to 2026-09-18 | The original placeholder: *"horribly probably extremly blunt and bent downwards"*, sticking out about 1.8 cm from the plate face | Every 2026-09-17 and 2026-09-18 measurement is this tip |
| Early 2026-09-19 | *"a lot shorter and a lot thinner"* | **It was BENT.** It explains that session's chattering contact and Z-proof behaviour |
| **From ~03:00 UTC 2026-09-19** | **The tip fitted when the instrument was packed.** *"new tip its gonna be very blunt but that what we have for today"* | **With this tip, HIGH Z extends toward the sample** — measured at a clean touch, +6,305 +/− 1,484 counts over +/−2,000 Z, 4.2 sigma, and the feedback loop held with that sign for eight runs |
| | | **It was then pressed into the gold with Z fully retracted for about 9, about 35, under 3.4 and about 5 minutes on 2026-09-19 morning.** Expect it blunter still. **Replace it before the next imaging attempt** |

> **The Z direction belongs to the tip, not to the instrument.** `--z-retracted low` is right for
> the tip that was fitted. **Re-check the direction whenever the tip changes**, with a +/−2,000 Z
> lock-in at a touch or with `Code/pc/stm_approach.py --z-retracted unknown`.

> **Changing the tip length changes the gap.** A shorter tip means the three ball ends stand
> further beyond it, and the sample plate can rest on the balls and never reach the tip. **Re-do
> the hand-set beep test after every tip change.** Do not assume the screws are where they were.

## 2.3 The sample plate and the gold

**Four gold builds. Only the last one matters for what is in the room, but the differences explain
the results.**

| Build | Method | What happened |
|---|---|---|
| 2026-09-16, attempt 1 | Not recorded | **Removed.** It was never reported at the time and only came to light on 2026-09-18 |
| 2026-09-17 | Leaf pressed onto **copper tape with the adhesive under it**, in a window cut in aluminium tape | **It held.** It did not move when blown on. That night gave an eight-round I-V curve, a 90-pass drift series and four scans |
| 2026-09-18 | A second sheet laid over the **whole plate face** | **It was loose** — *"it was moveing a bit if i blew on it"*. This is the leading explanation for everything erratic that night: an unadhered 100 nm sheet weighs about 0.019 Pa, and the bias pulls on it at about 1.1 Pa across a 1 micron gap, rising as one over gap squared. That is a pull-in instability, which is a snap |
| **2026-09-19, the one that was fitted** | **A copper/paper/gold/copper sandwich.** Copper tape sticky side up; the gold, still on its backing paper, laid onto that adhesive; a second copper tape pressed sticky-side-down onto the gold and stuck to the first; the whole thing onto a rolled copper ring on the plate | **Continuity gold to the orange bias wire: good** (`SAID`). **The second tape touches only the EDGE of the leaf, so the tip lands on gold** (`SAID`, Jacob: *"more like one strip of copper touches the side of the gold so framed a tiny section of it"*) |

**Two things to watch about the fitted build, both untested:**

1. **The leaf is anchored along one strip, not all round.** The far side is still free to lift, and
   the electrostatic pull rises as one over gap squared. If the snap comes back, anchoring more of
   the perimeter is the next move.
2. **The backing paper is still in the stack, directly under the gold** — roughly 50 to 100 microns
   of compressible cellulose immediately beneath a surface that needs sub-nanometre stability.
   **Jacob's own fallback removes it:** *"just putting the gold straight onto the sticky side of the
   copper."*

**The stack is also thicker than the previous one, on the same day the tip got shorter.** Those
move the gap in opposite directions by unmeasured amounts. **The net change is UNKNOWN. Re-set the
gap with the beep test; do not assume they cancel.**

## 2.4 The suspension

| | |
|---|---|
| **Fitted** | Three FOCMKEAS springs, identified 2026-09-19 from Jacob's order listing |
| **Loaded** | **356.2 g of coin** — 10 nickels in the printed cups (50.0 g) plus three paper wrapper tubes of 18 quarters (306.2 g). The nickels went on first |
| **State** | **The springs have almost certainly OPENED**, because the platform sagged when the coin went on and had to be raised again. **NOT YET CONFIRMED** — the bounce test confirms it in thirty seconds |
| **Height adjusters** | **At maximum.** There is no headroom left to correct another sag |
| **Eddy damping** | **Engaged** (`SAID` 2026-09-19). The magnet holder's height is not adjustable, so the damping gap is set by the platform alone |

> **This reverses advice that stood for one day.** An earlier calculation said the springs were far
> too stiff and that adding mass would make the 5 Hz noise worse. **Both were wrong**, from
> assuming a linear spring through the origin. These springs have initial tension, so the 2 mm
> droop was never a spring extension and every number built on it is retired (`docs/FACTS.md`).
> **Do not buy springs. Do not add more mass.**

**The quarters do not fit the printed cups and cannot be made to.** A US quarter is Ø24.26 mm;
the cups are Ø24.00 mm on the outside. The cups were designed around US nickels and hold five
each, fifteen in all, 75 g. That is their ceiling. **Any other mass has to be fastened to the
platform some other way — and fastened, not standing loose**, because a tube that can slide is a
stick-slip source on the one stage whose stability is the problem.

## 2.5 Firmware

**The Teensy is running the 2026-09-16 firmware**, uploaded and bench-tested that evening. Two
faults were fixed in it, both of which used to be tip hazards:

- **`CCON` no longer jumps Z to midscale on engage.** The loop now starts from the current Z, and
  it refuses to engage at all if Z is outside 10000–50000. **Tested red then green**: the old
  firmware jumped from 20000 to 32768; the new one held 20000.
- **The stepper coils switch off after every move**, about 20 ms later. **Dark driver LEDs between
  moves are now correct.** The old firmware left them powered, which heated the scan head.

---

# 3. Assembly and connections

> **`docs/WIRING.md` is canonical for everything in this section.** The tables below are a working
> copy so that the bench does not need two documents open. **If they differ, `docs/WIRING.md` wins
> and this file is the one to fix.**

> ## Use these colours. Do not read colours off a photograph
>
> Jacob and Nuh prefer wire colours to pin numbers and translate them to their own jumper leads
> themselves. **The colours below are the J1 / J2 cable colours from `docs/WIRING.md`.**
>
> **The jumper leads at the preamp board end are different colours from these.** Quoting a colour
> read off a photograph of the bench is exactly what would cause a mistake. Say "the DSUB2 −15 V
> wire" using the documented colour and let them translate.

## 3.1 Connector names — read this first

The documents, the silkscreen and ordinary conversation use different names for the same
connectors, and this has caused repeated confusion.

| Called | Silkscreen | Board | What it is | Where |
|---|---|---|---|---|
| J1 | **DSUB1** | Controller | DB9 to the scan head / piezo | bottom **left** |
| J2 | **DSUB2** | Controller | DB9 to the preamp | bottom **right** |
| JP1 | JP1 | **Preamp board** | 5-pin header: ±15 V in, signal out | a separate small PCB |
| — | **H1** | Controller | 26-pin ribbon to the Teensy | top **left** |
| — | **U19** | Controller | 3-pin JST XH, **power INPUT** | **right edge** |
| JP2 | — | — | **Does not exist anywhere in this project** | — |

## 3.2 Power — the two things that destroy hardware

**1. Power goes IN at U19, the little 3-pin JST XH on the right edge.** Pin 1 is V−−, pin 2 is
ground, pin 3 is V++.

**2. The ±15 V pins on DSUB2 are OUTPUTS to the preamplifier.** They look like the obvious place
for a bench supply and they are not. Feeding a supply in there pushes voltage backwards into
regulator outputs.

**Feed roughly ±18 V, not ±15 V.** The on-board regulators need headroom above their ±15 V output;
at ±15 V in they drop out and give low unstable rails that look like a dozen other problems.

**You need two independently adjustable supply channels**, or two supplies stacked in series with
their junction called ground. A single-output supply physically cannot straddle ground.

> **The 18 V figure is the CONTROLLER's. It is the wrong number for the preamp board.** If the
> preamp board is ever powered directly from a bench supply, **use 15.0 V**, because ±18 V is
> exactly its stated limit with no margin and bench supplies can overshoot at switch-on. This was
> caught before the outputs went on, on 2026-09-15, and nothing was damaged.

**Current limits.** Set a few hundred mA. On 2026-09-16 one channel was still on the preamp-only
20 mA setting and went into constant-current mode at about 2 V; at 200 mA it worked, drawing
about 40 mA. **A channel still in constant-current mode at 200 mA is a real fault — do not retry,
prove the wiring at the plug first.** Measured supply currents after a park on 2026-09-16 were
60 mA on V++ and 47 mA on V−−.

**LED5 and LED6 are the rail indicators.** LED5 means V++ is present, LED6 means V−− is present.

| LED5 | LED6 | Reading |
|---|---|---|
| on | on | Both rails up. This is what you want |
| on | off | **STOP.** V++ present, V−− missing — a half-powered bipolar supply |
| off | off | Neither rail. Supply off, not connected, or not delivering |

> **One expected exception, so it is not misread as a fault:** with the bench supply **off** but
> USB connected, LED1 to LED5 light and LED6 stays dark. That is the Teensy backfeeding through the
> SPI lines' protection diodes into the 3.3 V rail and on into V++. Confirmed by test. The
> LED5-on/LED6-off pattern only means a fault **when the bench supply is switched on**.

## 3.3 The 26-way ribbon, Teensy to controller (H1)

| Teensy pin | H1 pin | Signal | Purpose |
|---|---|---|---|
| 19 | 2 | ADC_CNV | start a conversion |
| 18 | 4 | ADC_BUSY | conversion status |
| 38 | **6** | ADC_SDI | the LTC2326's **RDL read-enable** |
| 27 | 8 | ADC_SCK | second SPI bus clock |
| 39 | 10 | ADC_SDO | second SPI bus data in |
| 13 | 12 | SCLK | SPI clock, all four DACs |
| 11 | 14 | SDI | SPI data, all four DACs |
| 10 | 16 | SYNC4 | U4, bias |
| 9 | 18 | SYNC2 | U2, Y |
| 8 | 20 | SYNC3 | U3, Z |
| 7 | 22 | SYNC1 | U1, X |
| — | all 13 odd pins | AGND | ground |
| — | **24, 26** | — | **unconnected by design.** Leave them alone |

**The rule that avoids counting pins: on H1 the odd pins are all ground and the even pins are
signals.**

**Pin 6 does get connected.** It is labelled ADC_SDI, which sounds like a data input a read-only
converter would not need. On this chip it is RDL, a read-enable — effectively the chip select. It
was left disconnected at first and that was a mistake.

**Teensy pins 8 and 9 are deliberately "swapped" relative to axis order — pin 8 is Z and pin 9 is
Y. That is correct. Do not fix it.**

> **There is no data-return line for the DACs.** Teensy pin 12 is not on the ribbon, so **the DACs
> can never be read back.** This is why a DAC that has lost its configuration is invisible to
> software, and why LED1 to LED4 are the only indicator you have.

## 3.4 DSUB1 — the scan head cable

| Colour | DB9 pin | Function |
|---|---|---|
| Black, Brown, Red, Orange, Yellow | 1–5 | AGND |
| **Green** | 6 | **Z−Y** |
| **Blue** | 7 | **Z+Y** |
| **Grey** | 8 | **Z−X** |
| **White** | 9 | **Z+X** |

**Row rule: on DSUB1 the row of five is all ground and the row of four carries signal.**

## 3.5 DSUB2 — the preamplifier cable

| Colour | DB9 pin | Function |
|---|---|---|
| **Black** | 1 | **BIAS**, out to the sample holder |
| **Brown** | 2 | **PREAMP−**, the ADC's negative reference |
| **Red** | 3 | **PREAMP+**, the signal |
| **Orange** | 4 | **−15 V** |
| **Yellow** | 5 | **+15 V** |
| Green, Blue, Grey, White | 6–9 | AGND |

**Row rule: on DSUB2 it is the opposite way round — the row of five carries signal and the row of
four is all ground.**

> **The same colour means different things on the two cables.** Orange is −15 V on the preamp cable
> and plain ground on the scan head cable. **Check which cable you are holding.**

### Why brown must land on the preamplifier's own ground

**`PREAMP−` is the converter's negative input, not a spare ground.** The LTC2326-16 measures
`PREAMP+` relative to `PREAMP−`. That input is high impedance, so **brown carries no current at
all** — it is a sense wire, and a wire carrying no current has no voltage drop along it, so it
reports the preamplifier's local ground faithfully back to the converter. That is what cancels the
ground drop along the cable.

**And white has to meet an AGND wire anyway**, or the ±15 V supply has no return path and the
preamplifier does not run. Brown alone cannot carry it. **So the three-way joint is the minimum,
not a convenience: white plus one AGND plus brown.** Solder brown and green onto the white lead
one at a time rather than twisting three together.

## 3.6 JP1, the preamplifier board's 5-pin header

| Pin | Net | Position along the row |
|---|---|---|
| 1 | **GND** | one end |
| 2 | **+ supply** (our +15 V) | second in from that end |
| 3 | **OUTPUT** | **the middle** |
| 4 | GND | |
| 5 | **− supply** (our −15 V) | **the far end** |

**How to tell which end is pin 1 with a meter and no ambiguity:** the layout is asymmetric. **The
negative supply is at the very END of the row; the positive supply is one in from the other end.**
So find the two supply pins; the one at an end is pin 5. **The middle pin is always pin 3, the
output**, whichever way round the board sits.

**On the board in service, hole 4 is left empty and a single ground lead goes in hole 1**, because
pin 4 has no copper on it at all. At the DSUB2 splice, **green (AGND) and brown (`PREAMP−`) both
join that ground lead.**

**The board's own jumper-lead colours, recorded at the bench 2026-09-14** — these are NOT the
J1/J2 colours and are only for the preamp board's own leads:

| Hole | Function | Lead colour |
|---|---|---|
| 1 | GND | **white** |
| 2 | +15 V | **grey** |
| 3 | OUT | **orange** |
| 4 | — | **empty** |
| 5 | −15 V | **tan** |

### The orange trap — read this before the preamp meets the controller

**`orange` means two different things at the two ends of this connection.**

| | Orange means |
|---|---|
| At the preamp board | **the amplifier's OUTPUT**, JP1 hole 3 |
| On the DSUB2 cable | **−15 V**, pin 4 |

**Joining orange to orange puts −15 V onto the amplifier's output through a 220 Ohm resistor.**
That is roughly 68 mA into an output stage that limits in the tens of mA, and **it would very
likely destroy IC1.**

**Go by function, never by colour, on this splice.** The verified mapping, made and checked on
2026-09-15: **white to brown AND green, grey to yellow, orange to RED, tan to ORANGE.** The splice
row as built, left to right, is: nothing, white, orange, tan, grey — which is BIAS, `PREAMP−`,
`PREAMP+`, −15 V, +15 V.

> **An expected reading written for that check was wrong, and a correct splice looked like a
> fault.** It said white should beep to all four ground pins. **With the connector unplugged it
> beeps to exactly one**, because the four AGND pins are tied together only inside the controller.
> Jacob reported what he saw instead of what he had been told to expect, which is the only reason
> it was caught. **Report what you see.**

## 3.7 The motor

**Wire it straight across: Teensy 33 to IN1, 34 to IN2, 35 to IN3, 36 to IN4.**

Sources online will tell you a 28BYJ-48 needs its coils driven in the order 1-3-2-4. That is true,
**and the firmware already does it** — it declares the motor as `EfficientStepper(steps, IN1, IN3,
IN2, IN4)`, performing the swap in software. **Swap the wires too and the two swaps cancel: the
motor buzzes instead of turning.**

**The motor driver does not go through the ribbon.** There is no motor circuitry anywhere on the
controller PCB.

**Powering the driver.** The Teensy pin labelled 5V is VIN and sits near 5 V when USB-powered, so
the driver can run off it — which is what Mech Panda appears to do. The catch is that the motor's
current spikes then ride on the same rail as the microcontroller and can reset it mid-scan. **A
separate 5 V supply avoids that.**

## 3.8 Shields and grounding

**The rule, and it has bitten this project once already:**

1. **Copper tape only** on the preamp box and the scan head shield cover.
2. **Buy conductive-adhesive copper tape.** Non-conductive adhesive means the overlaps do not
   connect.
3. **Solder the seams.** Do not trust overlap alone.
4. **Bond to circuit ground at ONE point.** More than one makes a ground loop.
5. **Then meter it** — every point on the shield must beep to the ground wire: near the wire, the
   far corner, and across every seam. **A shield you have not metered is not a shield you can
   reason about.**
6. **Never put copper and aluminium in contact** anywhere in the assembly.

**Why not aluminium:** it cannot be soldered because of its oxide, its adhesive usually does not
conduct so overlapping strips may not connect to each other at all, and against copper in humid
air it forms a galvanic cell — a few hundred millivolts of DC sitting on your shield, millimetres
from a 100 MOhm input. **On 2026-09-06 the preamp box was found wrapped in both and metered as
discontinuous and only partly grounded.** It was stripped and rebuilt in copper with soldered
seams.

**Two places on the instrument are aluminium by Jacob's decision, and that is recorded rather than
argued with:** the motor mount extenders (aluminium with copper over it — the one place the
galvanic rule still applies, slow-acting, watch it) and the piezo holding block (aluminium only,
which matches Mech Panda's build). **Neither is the scan head shield cover.**

**Where the ground bonds land:** both shields go to what Jacob calls "universal ground", which is
**the junction of the two supply channels — that is AGND**, the controller's single ground net.
One bond each, and the two shields do not touch. There is no separate chassis or mains-earth ground
in this design.

> **Both DB9 backshells float by design.** Their shell pins each sit alone on their own net; there
> is no ground path from a metal hood to the board. If you use metal hoods, their shields float,
> and a hood touching anything earthed creates a path the netlist cannot show you.

## 3.9 Figures for this section

**All figures are in `deliverables/2026-09-19-pause/photos/prepared/`, prepared by the photograph
review that ran alongside this manual.** Each carries its own caption bar naming the source frame,
its capture time and whether the reading is `SAID` or `READ`. **Every one below has been opened.**

> ### Figure 3.1 — `04_instrument_full_height.jpg`
> **The instrument as it stood on the morning of the move.** The printed frame; a top plate on
> three threaded columns; three long fine springs running down to eyebolts on the circular
> suspended platform; the copper-taped scan head on a copper-covered base plate; **three paper
> quarter wrappers standing on the platform as added mass.**
> **`READ`**, except the coin mass, which `docs/INVENTORY.md` records as `SAID` by Jacob.
> Source frame `IMG_8647`, 2026-09-19 09:41:02 camera-local.

> ### Figure 3.2 — `05_scan_module_in_hand.jpg`
> **The whole scanning module, lifted off the frame during the move — the best single view of how
> the subsystems sit relative to each other.** The suspended platform carrying the copper-covered
> base plate, the head held by **two rubber bands**, the coarse-approach stepper on its lead screw,
> **the copper-taped preamplifier box above the head**, an empty spring eyebolt, and two printed
> coin cups. **`READ`. Whose hand this is has not been established.**
> Source frame `IMG_4918`, 2026-09-19 10:15:53 camera-local, Nuh's camera.

> ### Figure 3.3 — `07_teensy_carrier_and_ribbon.jpg`
> **The control electronics.** The Teensy on a hand-wired protoboard carrier in its own printed
> box, with the yellow 26-way ribbon running down to the controller board in the box below.
> **No connection has been read off this photograph and none should be — `docs/WIRING.md` is the
> pinout reference.** `READ`. Source frame `IMG_4904`, 2026-09-19 09:41:09 camera-local.

> ### Figure 3.4 — `08_bench_power_supplies.jpg`
> **The two bench supplies, model numbers legible from the front panels:** a **JESVERTY SPS-3010**
> and a **LONGWEI LW-K3010D**. **Two supplies, not one dual-channel supply** — which matches
> section 3.2's requirement that a single-output supply physically cannot straddle ground.
> **How they are connected to each other has NOT been read off this frame and must not be.**
> `READ`. Source frame `IMG_4899`, 2026-09-19 09:40:51 camera-local.

> ### Figure 3.5 — `06_stepper_28byj48_label.jpg`
> **The coarse-approach motor with its own label legible: "STEP MOTOR 28BYJ-48 5V DC".** This is
> the first photograph of our hardware in which the stepper's label can be read, and it agrees with
> `docs/BOM.md` and `docs/WIRING.md`. `READ`. Source frame `IMG_4917`, 2026-09-19 10:15:42
> camera-local.

> ### Figure 3.6 — `09_faraday_enclosure.jpg`
> **The scan head's shield, off the instrument:** a printed box wrapped in copper tape, with two
> rectangular openings in one face and a small round hole in the top. `READ`.
> Source frame `IMG_4898`, 2026-09-19 09:33:31 camera-local.
>
> **Its continuity is the check that keeps being owed.** See `INCONSISTENCIES.md` item B8 — the
> repository contradicts itself about whether any shield in this project has ever been metered end
> to end.

# 4. Sample and tip

**All of this is unpowered work, with the sample plate off the instrument.** Nothing in this
section can damage the electronics. The two things you can lose are the gold leaf and the tip, and
both are protected by working on the bench rather than on the microscope.

> **Two hard rules for every job in this section.**
>
> **No cyanoacrylate. None.** Not near the plate, not in the same room as an open amplifier. The
> vapour travels and settles on the amplifier's input node, and that is the fault that cost this
> project two weeks. `STATUS.md` safety rule 5 forbids it anywhere near the preamp.
>
> **Loose gold flakes are conductive dust.** A flake landing on the tip holder or in the amplifier
> shorts across the input. Work away from the scan head, on a sheet of paper you can fold up and
> bin afterwards.

## 4.1 The tip

**Material: tungsten, 0.25 mm wire**, cut at about 45 degrees. Tungsten and platinum-iridium are
the two standard STM tip materials and both are effectively non-magnetic, which removes a whole
class of problem for free given the magnets sitting behind the sample. **Do not use steel.**

**Tips push into a socket** soldered to the metal stake on the piezo, so changing one does not mean
rebuilding the scanner.

**After fitting any tip, in this order:**

1. **Meter the tip holder against the brass piezo electrode. It must read OPEN.** This is
   `STATUS.md` safety rule 7 — a glue bridge or a solder whisker there is a shunt across the
   amplifier input, and it costs signal and adds noise.
2. **Re-do the hand-set** (section 4.4). A shorter tip means the three ball ends stand further
   beyond it, and the sample plate can rest on the balls and never reach the tip.
3. **Re-check the Z direction** before running anything that assumes one.

> **A meter's "OL" does not clear a leakage path in this project.** `STATUS.md` safety rule 12: what
> matters here is 100 MOhm to 10 GOhm, and a typical multimeter tops out near 60 MOhm, so OL only
> proves "more than 60 MOhm". **Never read OL as "ruled out."** Rule 7's check is different — it is
> looking for a hard short, which a meter does resolve.

## 4.2 Is the leaf actually gold?

**Ours is** — flame-tested on 2026-09-17 (`SAID`, Jacob). Keep the test, because it matters for any
new leaf: imitation leaf (Dutch metal, composition leaf, schlagmetal) is brass, and **brass grows
an insulating tarnish within days.** You would be trying to tunnel through a film that does not
conduct, on a surface that keeps changing.

**The flame test, two seconds, no chemicals.** Hold a 2–3 mm torn scrap in steel tweezers over a
ceramic tile, away from the leaf book and away from the instrument, and pass a lighter flame over
it for a second.

| What you see | Answer |
|---|---|
| Stays bright yellow, may shrink or ball up, does not darken | **Real gold** |
| Goes black or brown within a second, maybe a green flash and white smoke | **Brass** |

**Never make aqua regia.** It dissolves gold, so it cannot distinguish anything, and it releases
chlorine and nitrosyl chloride while it does it. **Do any chemical test in a different room from the
microscope** — acid mist and metal salts are exactly the contamination that makes an amplifier
input leak.

## 4.3 Mounting the gold

**The full bench card is `docs/gold_leaf_procedure.html`.** Read it before doing this job; what
follows is the summary and the difference between what the card says and what is actually fitted.

### The gate that comes first

**The gold must be electrically joined to the bias wire, or no tunnelling current can exist at
all.** The weak link is the copper tape's adhesive.

**Ours conducts** — `SAID` 2026-09-17, Jacob: *"the glue is conductive"*, checked on a scrap of
tape. **That was checked on a scrap, not on the tape already fitted to the box or the head**, which
may be from the same roll but that has not been confirmed.

**The five-minute test, if you ever open a new roll:** stick one scrap of copper tape down glue
side down, stick a second scrap on top overlapping by half so the second one's glue presses onto
the first one's copper, rub it hard, and meter across the join. **Beeps means the glue conducts.
Silent means you must make the connection metal to metal** — either fold the tape around the plate
edge so copper touches copper, or put one small solder blob on it with the plate off the instrument.

### The method the card describes

Copper tape onto the plate, rubbed flat; then the gold transferred onto that copper by the flip:
keep the leaf between paper, peel the top sheet off, turn the bottom sheet over onto the copper,
rub the back of the paper in small circles for about twenty seconds, then peel the paper off
slowly from one corner. **The gold stays on the copper because gold grips clean metal and paper
has nothing to grip with.**

**Then burnish it** — press and smooth the gold itself very lightly with a clean cotton ball. **It
goes from dull and loose-looking to bright and flat, and that change is how you know it has taken.**
Then pin the far edge with a small tab of copper tape, well clear of where the tip will land.

**Never cut free-floating leaf.** Unsupported leaf has no strength; scissors crumple it and tweezers
tear it. Cut it inside a paper sandwich, or stick it to oversized copper tape first and cut the
result down.

**You are not short of gold.** Four one-inch squares cut into roughly a hundred usable 5 mm pieces,
and the scanner's whole range is about half a micrometre — a 5 mm piece is ten thousand times wider
than anything the tip will ever look at.

### The method actually fitted, 2026-09-19

**Jacob could not get leaf to transfer onto copper tape by pressure** — *"I was pushing down super
hard and it just stuck to the paper."* What he built instead, in his own words: copper tape **sticky
side up**; the gold, **still on its backing paper**, laid onto that adhesive; then a **second copper
tape pressed sticky-side-down onto the gold** and stuck to the first; then a piece of copper tape
rolled into a ring to make it double-sided, stuck to the plate, and the whole assembly onto that.

**This keeps what the 2026-09-18 whole-plate sheet won — no copper oxide in front of the tip — and
adds what it lacked: the leaf is held down by adhesive instead of lying loose.** Leaf that is stuck
to adhesive cannot lift electrostatically, and that lifting was the leading explanation for the
snap.

**Its two known weaknesses are in section 2.3: the leaf is anchored along one strip only, and the
backing paper is still under the gold.**

### The three readings that decide whether it goes back on

Power off, plate off the instrument for the first one. **Take the gold reading at a corner, gently
— a meter probe dents gold leaf.**

| Probe from | Probe to | Expect |
|---|---|---|
| The gold surface, at a corner | The sample-plate wire | **Beeps** |
| The gold surface | The instrument's ground or frame | **Silent** |
| The gold surface | The tip holder | **Silent** |

**Stop and ask if:** gold to the sample-plate wire is silent after the tab is on; **gold to the tip
holder beeps once the plate is refitted** (that means the tip is touching the gold — back the plate
off immediately and do not power anything up); or the leaf will not lie flat after two attempts.

> **Which wire is the sample-plate wire?** It is the local jumper that lands on the plate at the
> scan head, recorded in our own bench logs as **orange at that end**. **Do not confuse it with the
> orange wire in the DSUB2 cable, which is −15 V.** The bias conductor inside DSUB2 is **black**. If
> there is any doubt about which physical wire you are holding, stop and ask.

## 4.4 Fitting the plate and setting the gap by hand

**The sample plate is held against the ball ends of the three fine screws by rubber bands.** There
is no other retention.

1. **Photograph the plate in place before removing it**, front and one side, with the rubber bands
   and which screws it sits on in the frame. You have to put it back the same way round.
2. **Lift it straight back and away from the tip**, never sideways past it.
3. **Bring it back in straight from behind**, not swinging past the tip.
4. **Confirm it sits on all three ball ends.** On 2026-09-17 both rubber bands pulled in line with
   the two side-by-side balls — the line the plate tips about — so nothing held the motor end down
   and **the motor screw was turning in free space.** One more band fixed it, and it was verified
   under motor drive over 400 steps out and back. **Check the motor-screw ball is actually touching
   the plate.**
5. **Replace any rubber band that is cracked or slack.** Rubber perishes over weeks, and the
   instrument has been in storage.

**Then close the gap by hand**, which is the step that decides whether a motor approach can find
anything at all. The motor's whole reach at the tip is only about ±75 microns, **so the sample has
to be set by hand to within about a tenth of a millimetre before any motor approach.**

**Two documented ways to do it. They differ and both are on record:**

| Method | What it says |
|---|---|
| The gold card, 2026-09-17 | Turn the two side-by-side screws in **tiny equal amounts** until a meter beeps tip-to-gold, then **back both off 1/16 of a turn**, which is about 20 microns |
| **The live back-off, 2026-09-19 — the one that worked** | Run the laptop beeper script with Z parked. **Turn in until it beeps, then back off in the tiniest nudges while it ticks, and stop at the silence.** The laptop ticks while the tip is touching and goes quiet when it is clear |

**The live back-off is the one to use**, because it watches the actual current rather than a meter,
and because on 2026-09-19 it was the only method that reliably left the gold within reach. **Its
script is scratch code on Jacob's laptop** (`sessions/data/2026-09-19-morning/scripts/`) and has not
been promoted into `Code/pc/`. See section 11.

> **One motor step spans nothing to metal contact.** The motor cannot park the tip at a moderate
> current. This is measured, not suspected, and it is why the hand-set matters so much.

## 4.5 Figures for this section

> ### Figure 4.1 — `01_sample_plate_gold_window.jpg`
> **The window in the sample plate is NOT all gold.** Aluminium tape over the plate face
> (`SAID`), a square window framed in dark tape, and inside it **a bright smooth gold patch over
> roughly the centre and right of the opening with duller crinkled copper tape exposed to its left
> and below** (`READ`). The orange bias wire enters under the tape at the top.
>
> **This is what the manual means by "the tip lands on gold only if it lands on the gold part."**
> Source frame `IMG_8619`, 2026-09-18 18:08:45 camera-local — the evening before the 2026-09-19
> bench session, so **this is the plate as rebuilt for that session.** `READ` from the frame, and it
> confirms the reading the 2026-09-18 23:13 session made independently.

> ### Figure 4.2 — `03_sample_plate_rubber_bands.jpg`
> **What actually holds the sample plate on: two twisted rubber bands**, each doubled and twisted,
> hooked over a screw head on either side. The orange bias wire runs down past the plate.
>
> **This is the first photograph in the repository that shows the mounting**, and `STATUS.md`
> already lists "the plate on its bands and balls" as one of four untested causes of the gap
> drifting. **`READ`. Nothing about band tension, age or creep can be taken from a photograph.**
> Source frame `IMG_8653`, 2026-09-19 09:41:26 camera-local.

> ### Figure 4.3 — `Images/ours/2026-09-18_scanhead_face_1.jpg`
> **The scan head face, straight on.** The piezo disc recessed in its bore with a small soldered
> structure at the disc centre, the fine tip lead crossing the face from above, and **three
> ball-end screws** — one top, one bottom and one at the right. `Images/ours/README.md` records
> Jacob's confirmation that **the top and bottom balls are the side-by-side pivot pair and the
> motor screw is the one on the right**, so the pivot line runs vertically in this view.
>
> **NO DIMENSION MAY BE TAKEN OFF THIS FRAME.** Three attempts to measure the tip-to-pivot-line
> distance from these photographs gave answers more than a factor of two apart, and
> `Images/ours/README.md` records four separate reasons the measurement cannot work. **A
> straightedge on the real part is the only route.**

**Still wanted, and not available:**

> **TODO-PHOTO A — the DSUB2 splice at the preamp end**, showing the five-way row. No frame in
> either new batch shows it. **Any caption must not quote colours read off the frame** — see the
> rule at the top of section 3.

> **TODO-PHOTO B — the tip itself, close enough to judge sharpness.** The closest existing frames
> are `Images/ours/2026-09-16_tip_protrusion_measurement_1.jpg` and `_2.jpg`, which show a tape
> measure against the head face and are the provenance for the 1.8 cm protrusion figure, but they
> are of a tip that has since been replaced twice.

# 5. Startup and shutdown

## 5.1 Before anything is switched on

**Do these unpowered. None takes more than a couple of minutes and two of them are gates.**

| Check | Why | Pass |
|---|---|---|
| **Tip out, or the sample well clear** | **The DACs power up at zero scale, not at 0 V.** The instant the analog rails come up, Z sits at one extreme of its range with no command from you. **This is a Stage 3 precaution, not a Stage 5 one** | — |
| **Tip holder to the brass piezo electrode** | `STATUS.md` safety rule 7 — a bridge there shunts the amplifier input | **OPEN** |
| **Gold to the sample-plate bias wire** | If the gold is not on the bias, no tunnelling current can exist | **Beeps** |
| **Gold to the tip holder** | If it beeps, the tip is already touching the sample | **Silent** |
| **Nothing is touching the suspended platform** | A cable, rod or tie across the suspension is a rigid bypass and no spring change works around it. **Check every wire has slack**: the coax to the preamp, the loom, the stepper leads | Only wires, all slack |
| **The plate sits on all three balls, and the motor-screw ball touches it** | On 2026-09-17 the motor screw was found turning in free space | — |
| **The rubber bands** | Rubber perishes in storage | No cracks, not slack |
| **No cyanoacrylate anywhere near the preamp** | `STATUS.md` safety rule 5 | — |

## 5.2 Power-on, in order

**The order matters, and it is the fix for the DAC configuration fault.**

1. **Bench supply set to about ±18 V, current limit a few hundred mA, polarity checked against your
   labels, THEN connected** to U19 — the 3-pin JST on the right edge, never DSUB2.
2. **Switch the supply on. Watch and smell for several seconds.** No smoke, no burning smell,
   nothing hot. Check the current draw is modest and stable, not pegged.
3. **Check LED5 and LED6.** Both must be lit. See section 3.2 for what each pattern means.
4. **Wait, then plug in the USB.** The Teensy boots in milliseconds and immediately writes the DAC
   configuration; if it does that before the DACs' 3.3 V supply is up, the writes go nowhere.
   Powering the analog side first is the free fix for that.
5. **Wait about a second before the first command.** The boot reset does four software resets with
   a 100 ms wait each, so the board takes roughly half a second before it answers anything. If
   your first command gets no reply, wait and retry.
6. **Check LED1 to LED4.** See below.
7. **Park every axis** (section 5.4).
8. **Allow about two minutes to settle** before taking any preamp measurement.

> **The 45-minute warm-up rule is RETIRED.** `STATUS.md` safety rule 0 was retired on 2026-09-15:
> the repaired board settled within about two minutes and then did not move, twice, and showed
> **zero change between 20 and 45 minutes.** The old climb was the previous board's floating
> reference charging, not the amplifier. **Allow about two minutes.** Note the minutes since
> power-on alongside any noise figure anyway, so that runs compare like with like.

## 5.3 The LED check — do this before and after every measurement

**LED1 to LED4 are the four DACs' ALERT pins.**

| | |
|---|---|
| **Dark** | The DACs are configured and working |
| **Lit** | **That DAC is dead. Any reading taken with one lit is void** |

**They are lit at every power-on, before any command is sent, without exception.** That is power
sequencing, not a random fault — `STATUS.md` fault 4. **`RSET` clears them.**

**There is no software substitute for looking.** The ALERT pins go to the LEDs and nowhere else;
they are not wired to the Teensy. There is no DAC readback, because the ribbon carries no data
return line for the DAC bus. **`GSTS` will happily report `dac_z = 65535` while the chip outputs
nothing** — its fields are firmware bookkeeping, not measurements.

**If any is lit: send `RSET`, then re-park Z immediately**, because `RSET` slams Z to a rail.

## 5.4 Parking the axes

**After power-on, after `RSET`, and after `TEST`, every axis has to be put somewhere sane by hand.**

```
DACZ 32768
DACX 32768
DACY 32768
BIAS 32768
```

Then `GSTS` and confirm the fields read back 32768.

> **32768 is 0 V on every axis.** Codes run 0 to 65535. Z is ±10 V, X, Y and bias are ±3 V.

> **Where to park Z is a live disagreement in the repository, and it is Jacob and Nuh's to
> settle.** `STATUS.md` safety rule 6 says park Z at midscale before the motor moves. **Every motor
> move on 2026-09-19 parked Z at the retracted end (code 0) instead**, which is what
> `Code/pc/stm_approach.py`'s known-direction mode does and what the 2026-09-18 plan says.
> **Midscale leaves the tip half extended during a motor step; the retracted end does not — but
> "retracted" is only code 0 while HIGH Z extends toward the sample, which is a property of the
> fitted tip.** **Settle this before the next motor move** and write the decision into `STATUS.md`.

## 5.5 Shutdown

**In this order:**

1. **Park.** Z to the retracted end, X and Y to midscale, bias to 32768 (0 V).
2. **Back the sample off.** On 2026-09-19 the side screws were backed off **two full turns** before
   the move; at the end of the previous session it was about a quarter turn. **Either is fine as
   long as it is written down**, because the next session has to know how far it is starting from.
3. **Unplug the USB.**
4. **Switch the supplies off.**
5. **Write down the coarse screw's step count.** The firmware counter resets at restart, so **that
   number exists only in `STATUS.md` and the session log.** If it is not written down it is lost.
6. **Cover the instrument.**

**Then do the five session-closing steps in `CLAUDE.md` section 5** — the session log, `STATUS.md`,
`docs/NEXT_SESSION_PLAN.md`, commit, push. **Work that is not pushed does not exist as far as the
other computer is concerned.**

---

# 6. Operation: every command

## 6.1 How to talk to the board

```
python Code/pc/stm_console.py GSTS          # one command, then exit
python Code/pc/stm_console.py DACZ 32768
python Code/pc/stm_console.py               # interactive
```

**On Windows type `py`, not `python` or `python3`.** On Jacob's machine `python` and `python3` are
Microsoft Store placeholders that print *"Python was not found"* even though Python is installed.
**`py` is the Python launcher and it works either way.**

**Use `stm_console.py`, not a generic serial monitor.** The firmware starts reading as soon as one
byte arrives and then immediately reads four. Anything that sends per-keystroke — PuTTY, screen,
minicom, the PlatformIO monitor — loses that race, and **the command is silently discarded.**
`stm_console.py` sends each command as a single write.

**Every command is exactly four characters.** Arguments follow after a space.

**In interactive mode, type `free` to release the serial port** before flashing firmware, otherwise
the Teensy Loader asks for the PROGRAM button on every upload.

> **The firmware also leaves the line terminator in the buffer after an argument-less command.**
> `stm_console.py` works around this by sending a newline only when there is an argument. Anything
> else desynchronises: after `RSET` or `ADCR` the stray newline eats the first character of your
> next command.

## 6.2 The commands

### Reading

| Command | Arguments | Replies | What it does |
|---|---|---|---|
| `GSTS` | — | **yes** | Ten comma-separated fields, see below |
| `ADCR` | — | **yes** | One ADC reading, as a **5-sample rolling average** |
| `IVGE` | — | **yes** | Dumps the last I-V curve |

**`GSTS` returns, in order:** `bias, dac_z, dac_x, dac_y, adc, steps, is_approaching,
is_const_current, is_scanning, time_millis`.

> **Field 5 is a RAW single conversion. `ADCR` is an average.** Use `GSTS` for noise work, because
> averaging hides exactly the isolated bit-flips a marginal SPI link produces. Use `ADCR` for a
> settled value.
>
> **The other fields are firmware bookkeeping, not measurements.** `time_millis` climbing between
> calls is the sign the board is alive and not resetting.

### Setting outputs — all four are silent

| Command | Range | Notes |
|---|---|---|
| `DACX` | 0–65535, 32768 = 0 V | X piezo, **±3 V** |
| `DACY` | 0–65535, 32768 = 0 V | Y piezo, **±3 V** |
| `DACZ` | 0–65535, 32768 = 0 V | Z piezo, **±10 V** |
| `BIAS` | 0–65535, 32768 = 0 V | Sample bias, **±3 V**. It **inverts**: 65535 gives −3 V at the holder |

> **The firmware's own source comments say X and Y are minus five to plus five volts and they are
> wrong** — that figure is retired. X, Y and bias use identical range bits, so they cannot differ,
> and bias measures ±3 V. **Trust the range bits and the measurement, not the comment.**

### Motor

| Command | Arguments | Notes |
|---|---|---|
| `MTMV` | steps | **Blocks while moving**, at about 68.3 steps per second, so 512 steps takes about 7.5 s. **Negative approaches, positive retracts** |

**A move cannot be stopped by any command.** The firmware reads nothing until it finishes. The only
stop is unplugging USB, or opening the port at 134 baud, which drops the Teensy into its bootloader.
**So keep single moves short — a few hundred steps at most.**

**Since the 2026-09-16 firmware the coils switch off about 20 ms after a move**, so the driver LEDs
go dark between moves. **That is correct, not a fault.** `MTMV 0` just makes sure they are off.

### Reset and the piezo tests

| Command | Blocks for | Notes |
|---|---|---|
| `RSET` | — | Full reset: all four DACs, the stepper counter and the status struct |
| `TEST` | about 3.5 s | 1 kHz square wave on Z, then X, then Y. **Leaves each axis at a rail** |
| `TONE` | the requested duration | Square wave on Z, symmetric about midscale, **parks Z at 0 V on exit** |

> **`RSET` and `TEST` both slam Z to a rail.** `RSET` sends a software full reset, which is zero
> scale, and also zeroes the bias, the step counter and every setpoint. **Re-park Z at 32768 after
> either.** `STATUS.md` safety rule 6.

> **`RSET` does not de-energise the motor.** It only zeroes the step count.

**Prefer `TONE` over `TEST`**, because it parks Z at 0 V instead of leaving it at a rail.

> **There is no usable resonance to hunt for, and you cannot judge the piezo by ear.** A sweep from
> 1 kHz to 11 kHz on 2026-08-31 found no loudness peak anywhere once the disc is mounted — clamping
> at the rim and mass-loading by the tip holder damp it out of existence. **The old advice to use a
> tone near 8.6 kHz as a standard check is retired**, and the firmware's own source comment still
> repeats it. **Judge the piezo with a meter:** `DACZ 65535` should give −10 V at the scan head end
> of the DSUB1 cable, on the row-of-four signal wires.

### Feedback, scanning and I-V

| Command | Arguments | Notes |
|---|---|---|
| `CCON` | adc_target | Turn constant-current mode on. **Silent** |
| `CCOF` | — | Turn it off |
| `PIDS` | Kp Ki Kd | Set the PID gains. **They boot at 0.0, so constant-current mode does nothing until you send this** |
| `SCST` | x_start x_end x_res y_start y_end y_res samples_per_pixel | Start a scan. **Blocks for minutes** |
| `IVME` | bias_start bias_end bias_step | Sweep bias and record an I-V curve, up to 1000 points. Blocks up to about 60 s |
| `STOP` | — | Clears the approaching, constant-current and scanning flags |

`SCST` streams each line back as `A,<row>,<values...>` for the ADC and `Z,<row>,<values...>` for the
Z heights, then prints `D` when it is done.

### The one you must not run

| Command | Notes |
|---|---|
| `APRH` | **Do not use it.** `STATUS.md` safety rule 2 |

**Two reasons, both in the source.** `approach()` tests `read_adc() > target`, a **signed**
comparison, against a baseline that has been negative for most of this project — **so if tunnelling
drives the reading more negative it never triggers and the motor keeps driving the tip into the
sample.** And the second argument is the step *interval*, not a step count; maximum travel is
hardcoded at 10000 steps.

**Measured 2026-09-16: a positive sample voltage gives negative counts.** So under positive sample
bias this failure case is exactly what happens. **Use `Code/pc/stm_approach.py`, which never sends
`APRH`** and thresholds on absolute deviation from a measured baseline, so it works without knowing
which way tunnelling moves the reading.

## 6.3 Which commands block, and which reply

**The firmware is single-threaded.** While a blocking command runs, it never reads the serial port,
so anything you send lands in the buffer and gets misread as garbage. `stm_console.py` waits these
out for you.

| Command | Blocks for |
|---|---|
| `TEST` | about 3.5 s |
| `TONE` | the requested duration |
| `MTMV` | steps divided by 68.3, in seconds |
| `APRH` | up to about 120 s |
| `IVME` | up to about 60 s |
| `SCST` | minutes |

**Only `GSTS`, `ADCR` and `IVGE` reply with anything.** Everything else is silent, so waiting for a
response from them just burns the timeout.

## 6.4 The dangerous commands, in one place

| | Why |
|---|---|
| **`APRH`** | `STATUS.md` safety rule 2. It can drive the tip into the sample without ever triggering |
| **`CCON` with a tip in range** | `STATUS.md` safety rule 8. **The firmware jump was fixed and bench-tested on 2026-09-16**, and the rule is kept anyway until Jacob and Nuh decide otherwise, because with non-zero gains the loop's first step still applies a normal correction and no tip has ever been near a sample. **Keep the target within ±32768** — a larger one reads past the end of the firmware's log table |
| **Any out-of-range DAC value** | `STATUS.md` safety rule 13. **An out-of-range value does not error — it silently jumps the axis to the opposite rail** |
| **`RSET` or `TEST` with a tip near the sample** | Both leave Z at a rail |
| **`SCST` with y_resolution above 2048** | The firmware parses seven integers straight from serial with no bounds check, and writes past the end of two arrays. **Keep y_resolution at 2048 or below.** `samples_per_pixel` of 0 divides by zero |
| **A big upward Z jump followed immediately by a read** | Measured 2026-09-19: two of four jumps from 0 to 28,000 put 3,714 and 1,026 counts on the very next reading. **Ramp Z, or wait, before trusting the first read after a large upward jump** |

**What an out-of-range DAC value actually does**, because this is a tip hazard and not a typo:

| You type | The firmware sends | The DAC outputs |
|---|---|---|
| `DACZ 65535` | 65535 | +10 V, as expected |
| **`DACZ 70000`** | **4464** | **−8.6 V.** You asked for the top rail and got most of the way to the bottom one |
| **`DACZ -1`** | **65535** | **+10 V.** You asked for below zero and got the top rail |
| **`DACZ` with no number** | **0** | **−10 V** |

**From midscale each of those is a jump of roughly 8 to 10 V — hundreds of nanometres, far more
than a tunnelling gap.** There is no clamp anywhere in the path. **Keep every DAC argument between
0 and 65535, and never send a bare `DACZ`, `DACX` or `DACY`.**

## 6.5 Before every measurement

1. **Look at LED1 to LED4.** If any is lit, the reading is void. Send `RSET`, then re-park Z.
2. **Nobody within a metre of the preamplifier.** A person nearby injects current into a 100 MOhm
   input node; a tunnelling current is about 1 nA. **`STATUS.md` safety rule 9 keeps this rule but
   flags its number as not established**, because the figure came from the old board whose
   reference floated.
3. **Soldering iron off.** Measured 2026-09-16: a hot iron adds about 17 counts. Small, but real.
4. **Look at LED1 to LED4 again afterwards.** The configuration can drop during a measurement.

---

# 7. Data collection

## 7.1 The tools, what they do and what they write

**Everything lives in `Code/pc/` and is run from the repository root.** They find the Teensy by
PJRC's USB vendor ID, so you never have to name a port. `pyserial` alone is enough for the console;
`numpy` and `matplotlib` are only needed by `adc_stats.py` and the unused GUI.

| Tool | What it does | What it writes |
|---|---|---|
| **`Code/pc/stm_console.py`** | **Start here.** Sends any firmware command, one-shot or interactive | Prints to the terminal only |
| **`Code/pc/adc_stats.py`** | Samples the ADC over time and reports mean, standard deviation, minimum, maximum and range. **Reads `GSTS` field 5, a raw single conversion**, on purpose — `ADCR` averages and would hide the isolated bit-flips a marginal SPI link produces | Prints to the terminal |
| **`Code/pc/stm_noise_spectrum.py`** | Noise spectrum of the ADC, with a comparison against every previous run printed for you. **It only reads** — no Z, no motor, no bias, nothing moves | A CSV of raw samples, so the run can be re-analysed with no instrument |
| **`Code/pc/stm_approach.py`** | PC-side coarse approach by the woodpecker method: only the piezo ever closes the gap, and the motor only moves while Z is retracted. **It never sends `APRH`** | A log; CSVs in some modes |
| **`Code/pc/stm_feedback_scan.py`** | Constant-current imaging with the feedback loop running on this computer. Each pixel records the Z that holds the setpoint current — the height map. **Every line is scanned forward then backward** | A CSV per scan: first column the Y DAC code, header row the X DAC codes, each line appearing twice as `fwd` and `back` |
| **`Code/pc/stm_y_control.py`** | **The control that decides whether a reproducible profile is the sample or the scanner's own bow.** Runs the same line at three Y positions | A CSV, with the half-width recorded inside it |
| `Code/pc/stm_control.py` | A library the GUI is built on, not a program. **Four verified bugs, all upstream, none fixed** | — |
| **`Code/pc/stm_app.py`** | **Do not use.** Its Approach button sends `APRH` and its motor control is broken | — |
| `Code/pc/stl_features.py` | Measures the printed parts straight out of the STL meshes. **Run this instead of guessing a hole size** | Prints a table, with a fit-error column |
| `Code/pc/check_facts.py` | Reports anywhere a value `docs/FACTS.md` lists as retired still sits in a live document, plus broken links and miscited safety rules. **Runs automatically at session start** | Exit code and a report |

**Every instrument tool has a matching `*_test.py`** that runs it against a simulated junction with
no hardware attached. **Run the test first.** If any assertion fails, do not use the tool.

```
py Code/pc/stm_approach_test.py
py Code/pc/stm_feedback_scan_test.py
py Code/pc/stm_y_control_test.py
py Code/pc/stm_noise_spectrum_test.py
```

## 7.2 How a run is recorded

**Raw data goes in `sessions/data/<session-name>/`, with its own `README.md` listing every file and
what it is.** Four such directories exist: `2026-09-17-bench`, `2026-09-18-bench`,
`2026-09-19-bench` and `2026-09-19-morning`. **Read the README before opening any CSV** — several
files carry caveats that change what they mean.

**Each session directory also has a `scripts/` folder.** Those are **scratch scripts kept as
provenance, not tools.** They hard-code a COM port and absolute paths to one laptop, and several
of them assume a particular Z direction. **They are history. Do not run them on another machine
without reading them first.**

**Conventions that make runs comparable:**

- Times in UTC.
- **Say which reading you used**: `ADCR` averaged, or `GSTS` field 5 raw.
- **Say what the bias code was.** The usual ones are `BIAS 38229` for −0.5 V at the sample and
  `27307` for +0.5 V.
- **Say which tip is fitted and when it was fitted**, because the Z direction and every junction
  figure belong to a tip, not to the instrument.
- **Say how many minutes since power-on** alongside any noise figure.
- **Note whether anyone was within a metre of the preamplifier.**

## 7.3 Three traps that have already cost data

1. **Write CSV rows as they are taken, not at the end.** Four CSVs were lost on 2026-09-19 because
   the scripts wrote their file only on a clean exit, and stopping a task kills the process before
   that runs. The `.log` files were all that survived.
2. **Grep the file for the thing you claimed to change.** On 2026-09-17 a wrap recorded that a
   scan tool's bias argument was "now actually used". **It was not** — a literal value was still
   there, so every scan that night ran at one bias whatever was typed.
3. **A tool's built-in comparison figures go stale.** `Code/pc/stm_y_control.py` prints a wobble
   figure from 2026-09-17; the 2026-09-19 floor with a junction and X held was 9–19 counts.
   **Check which night and which tip any quoted figure belongs to.**

---

# 8. Analysis

## 8.1 What a scan file contains, and how to read it

**The value in each cell is the Z DAC code the feedback loop needed to hold the setpoint current at
that pixel.** That is the height map. **Higher is not automatically "taller"** — which direction of
Z extends toward the sample is a property of the fitted tip.

**Each line appears twice, forward and backward.** Trace against retrace is the first test of
whether a feature is real.

## 8.2 The tests that decide whether anything is real

**This project's hardest-won lesson is that a convincing image is not evidence.** Four tests are on
record, and all four have changed a conclusion at least once.

| Test | What it is | What has happened |
|---|---|---|
| **Detrend every pass first** | Remove the straight-line tilt before taking any correlation | **There is a fixed tilt of about −0.17 counts of Z per count of X between tip and sample.** Undetrended, the same data gives +0.741 and +0.880 and looks like a breakthrough; detrended, the honest figure is +0.124. **None of the correlations mean anything until this is done** |
| **The X-held control** | Run the identical scan with identical timing, but never move X | On 2026-09-17 the control produced **more** apparent structure than a real scan: 87 counts per line against 29–43 for the real narrow scans. On 2026-09-19 four controls reproduced better than four feedback scans, +0.37 against +0.04 |
| **The three-Y control** | Run the same line at three different Y positions. Different places giving **different** shapes means the profile is the surface; the **same** shape everywhere means it is the scanner's own bow | At 3,000 counts apart the same shape appeared everywhere. At 12,000 apart one run said "surface" at 3.9 sigma **and the repeat did not** |
| **Compare against the height wobble** | Hold the loop at one point and measure how much Z moves | Any apparent structure smaller than that wobble is not structure |

**Two statistical rules the project follows and should keep following:**

- **Compare like with like.** The original three-Y control compared five-pass averages between
  places against single passes within a place. Averaging raises a correlation on its own, so the
  comparison was decided before any physics entered it.
- **Account for multiple comparisons.** If you searched many scans for a feature, say how many, and
  say what that does to the chance of finding one.

## 8.3 Re-analysing without the instrument

Both control tools can re-read a file they wrote, with nothing plugged in:

```
py Code/pc/stm_y_control.py --analyse <file.csv>
py Code/pc/stm_noise_spectrum.py --analyse <file.csv>
py Code/pc/stm_noise_spectrum.py --compare still.csv stamp.csv
```

## 8.4 The charts and pages already written

| Page | What it is |
|---|---|
| `docs/showcase.html` | For a reader judging the work in five minutes. Leads with what the instrument demonstrably does |
| `docs/progress.html` | The public explainer: what an STM is, how tunnelling works, where the build reached |
| `docs/bench_2026-09-17_review.html` | Nine figures reading the 2026-09-17 bench data, written for someone who does not read code |

**None of them has independent authority.** Every number on them is cited from `STATUS.md`,
`docs/FACTS.md` or a session log. **If one disagrees with those, they win and the page is what gets
fixed.**

---

# 9. File organisation: which document owns what

**Every kind of information has exactly one authoritative home.** Writing it anywhere else creates
a copy that will drift, and this project has lost real time to exactly that.

| Information | Canonical home |
|---|---|
| **Any constant or measured number** | **`docs/FACTS.md`** |
| **Any open question, UNKNOWN or VERIFY** | **`docs/OPEN_QUESTIONS.md`** |
| **What to do next at the bench** | **`docs/NEXT_SESSION_PLAN.md`** |
| **Current state, faults, numbered safety rules** | **`STATUS.md`** |
| **Documented conflicts between sources** | **`docs/ENGINEERING_REFERENCE.md`** section 11 |
| **What happened on a given day** | **`sessions/YYYY-MM-DD.md`**, or `-<name>.md` if there is more than one that day. Append-only, never rewritten, and every log indexed in `sessions/README.md` |
| **Pinouts and board layout** | **`docs/WIRING.md`** |
| **Part specs and datasheet facts** | **`docs/COMPONENTS.md`** |
| **What is inside a zip, PDF or mesh** | **`docs/INDEX.md`** |
| **What we physically own** | **`docs/INVENTORY.md`** — never `docs/BOM.md`, which is a specification |

**Citing a number in prose is fine and expected.** What is not fine is building a **second
register** — a table or reference block of constants anywhere but `docs/FACTS.md`. Two registers
drift apart and nobody can tell which is current. **`python3 Code/pc/check_facts.py` is the
protection**, and it runs at session start.

**Which document to believe, when two disagree.** Highest first: `STATUS.md`; then every session
log carrying the newest date; then older session logs; then `docs/PROJECT_HANDOFF_SUMMARY.md`'s
body, parts of which are known to be wrong.

> **But precedence is about conflicts, not about what to read.** A low-ranked document is still
> read; it is only outranked when it disagrees with a higher one. On 2026-09-06 a session spent a
> day re-deriving a pinout that had been sitting in the handoff's header for six days, because
> "ranked last" was read as "not worth opening" — and the re-derivation was shallower and missed
> something. **Freshness is a property of a passage, not of a document.** A correction banner at the
> top of an old file is often the newest thing in the repository. **Check the top of any document
> before dismissing it on rank.**

**The other files worth knowing:**

| Path | What it is |
|---|---|
| `README.md` | The public front page |
| `SETUP.md` | How to set up a computer to work on this project |
| `CLAUDE.md` | The working protocol, read automatically by Claude Code |
| `docs/START_HERE_gotchas.md` | Things that mislead you. Read before touching hardware |
| `docs/soft_launch_test_procedure.md` | The staged bring-up, stages 0 to 6. **Partly superseded — it carries a banner saying which parts** |
| `docs/DAC_BOOT_STATE.md` | DAC power-on behaviour. Read before bringing up the analog side |
| `docs/UPSTREAM_MECHPANDA.md` | The design we are actually building |
| `docs/UPSTREAM_BERARD.md` | Reading notes from Dan Berard's build. **Context, not our design** |
| `docs/OTHER_BUILDERS.md` | What independent DIY STM builders have done. Leads to test, not specifications |
| `docs/BOM.md` | Every part, with CONFIRMED / CHOICE / UNKNOWN status. **A specification** |
| `docs/archive/` | Superseded procedures, kept with banners. **Not current instructions** |
| `CAD/prints/README.md` | Every printed part, measured: sizes, hole grids, which screw goes where |
| `Code/pc/README.md` | The PC tools, and first-time setup on Windows and Mac |
| `Images/ours/` | Photographs of **our** hardware. **`Images/` at the root is Mech Panda's, not ours** |

---

# 10. Troubleshooting

> **`STATUS.md`'s open-faults section is the authority and it changes.** What follows is a working
> summary as at 2026-09-19, arranged by what you would actually see.

## 10.1 Faults that are open right now

### The DACs lose their configuration — `STATUS.md` fault 4

**Symptom:** LED1 to LED4 light. All four go at once. Every DAC output goes dead. **Any reading
taken while one is lit is void.**

**What is established.** They are lit at **every** power-on, before any command is sent, without
exception. **Thirty minutes powered with no commands sent at all left them dark**, so idle time
alone does not trigger it — something we do provokes it. Whether it also recurs mid-session is
**ambiguous and unsettled**: 2026-08-31 recorded it recurring every 30 to 60 minutes; on 2026-09-16
the board was powered for about three hours in stretches with the LEDs dark every time they were
checked, **but that was not a controlled test.**

**The explanation for the power-on half** is power sequencing: USB boots the Teensy in
milliseconds and it writes the DAC configuration into chips whose analog supply is not up yet.
The setup routine never runs again, because USB keeps the Teensy alive.

**What to do.** Send `RSET`, which restores the configuration, then **re-park Z immediately**
because `RSET` slams it to a rail. **The operational fix is free: power the analog supply first,
then plug in the USB.**

**Software cannot detect this.** See section 5.3.

### The approach tool's default Z step is too coarse — `STATUS.md` fault 6, a tip hazard

**Symptom:** an approach goes from no current straight into hard contact between two consecutive
samples, with nothing in between.

**Found by arithmetic, not at the bench.** `Code/pc/stm_approach.py` ships with a default Z step of
200 counts, which is about 2.08 nm of tip travel per sample point, while the window in which a
tunnelling current is above the noise floor and below the contact threshold is about 0.21 nm wide.
**So the sweep takes about a tenth of a sample inside the window it has to detect** — about one
approach in ten lands a reading in tunnelling range.

**The fix is a flag that already exists: `--z-step 5`.** That gives about four samples inside the
window and costs about 3.3 s per half sweep.

> **One assumption behind this is inferred, not measured** — the nanometres-per-count figure comes
> from Berard's disc, not ours. If our scanner is less sensitive the problem shrinks; if it is more
> sensitive, this is worse than stated.

### U13's unused op-amp channel floats — `STATUS.md` fault 4b, a lead not a confirmed fault

**U13 is a dual op-amp. Channel A is the bias buffer that drives the sample. Channel B is connected
to nothing at all.** An op-amp channel with floating inputs can drift to a rail or oscillate, and
it shares a die and both supply pins with the channel next to it.

**The same package is wired correctly elsewhere on this board**, which is the evidence that this is
an oversight rather than a normal spare.

**That the pins are open is confirmed from the netlist. That it is causing a problem is UNKNOWN.**
**Predicted symptom:** noise or slow drift on the bias line that does not track the commanded bias.
**Test:** put a scope on U13 pin 7 with the board powered — a quiet DC level is fine, a rail or an
oscillation is not. **Fix:** two short wires, pin 6 to pin 7 and pin 5 to AGND, which makes it a
unity-gain follower on 0 V. Low risk, no track cutting.

### The old preamp board has no ground pour — `STATUS.md` fault 0d

**This is fixed on the board in service and is unfixed on the old one.** It is here because it
explains why old numbers cannot be trusted.

**The fabricated gerbers have no copper pour at all**, where Berard's Eagle source has a
bottom-layer ground polygon. Six points that should be ground each end at a dead via: C2's ground
end, C3, C4, IC1 pin 3, IC1 pin 8 and JP1 pin 4. **IC1 pin 3 is the amplifier's own 0 V reference.**

**Consequence:** every preamp reading taken before the repair was measured with that reference
floating, so it cannot be converted to an input current. **The gerbers' net labels still say `GND`
for every one of those points**, which is why every document in this repository believed they were
connected. **An upstream conversion defect, not a build fault.**

**Any board reorder must have the pour filled.**

## 10.2 Faults that are fixed, listed so that old documents are not misread

| Fault | Status |
|---|---|
| **`STATUS.md` fault 0 — the measurement chain** | **FIXED 2026-09-16.** `PREAMP−` is grounded at the preamp through the DSUB2 splice, the ADC reads the preamp at about −1.7 counts, and the dummy junction gives 320.5 counts per nA end to end |
| **`STATUS.md` fault 2 — `CCON` jumping Z to midscale** | **FIXED 2026-09-16, uploaded and bench-tested red then green.** The rule against it is kept anyway |
| **`STATUS.md` fault 3 — the motor left energised** | **FIXED 2026-09-16, uploaded and bench-tested.** The coils switch off after every move |
| **`STATUS.md` fault 5 — one JP1 ground pin open** | **Explained** — it is one of the six points fault 0d covers, not a one-off |
| **The preamp offset that blocked the project for weeks** | **The board that showed it is retired.** The reading was real as a voltage but was never a valid current, because that board's amplifier reference floated |

## 10.3 Symptom to cause

### Nothing at all comes back from the board

| Check | |
|---|---|
| Is the USB cable a **data** cable? | A charge-only cable connects the Teensy to nothing. **This wastes more first-day hours than anything else in this project** |
| Are you using `stm_console.py`? | A per-keystroke terminal loses the four-byte race and the command is silently discarded |
| Did you wait about a second after plugging in? | The boot reset takes roughly half a second |
| Is `time_millis` climbing between `GSTS` calls? | If it never increases, the board is resetting repeatedly — check power |
| Garbled characters? | Wrong baud rate. It is 115200 |

### The motor buzzes but does not turn

**The wires are crossed**, undoing the software 1-3-2-4 mapping. Wire it straight across.

### The motor does nothing at all and no LEDs move

The driver's minus terminal is not on Teensy ground. **Or you used the GUI** — `stm_control.py`
line 127 is missing an f-string prefix, so it sends literal text and the motor moves zero steps.
That is an upstream bug and it is why the GUI's motor control does nothing.

### The step counter never changes

The command is not reaching the parser. See "nothing at all comes back", above.

### One supply channel goes into constant-current mode

**Check the current limit first.** On 2026-09-16 one channel was still on the 20 mA preamp setting
and limited at about 2 V. At 200 mA it worked. **A channel still in constant-current mode at 200 mA
is a real fault: do not retry, prove the wiring at the plug.**

### The ADC always reads exactly 0, or exactly 65535, or wild garbage

The converter is not converting properly. **Check ribbon pin 6 to Teensy pin 38** — the read-enable
that looks like a data input a read-only chip would not need.

### The preamp reading is noisy

In the order that has actually mattered:

| Cause | Evidence |
|---|---|
| **Someone is near the board** | A person injects current into a 100 MOhm node. Keep everyone a metre away. **The rule stands; its number does not** |
| **A soldering iron is on** | Measured 2026-09-16: about 17 counts. Small but real |
| **Something was recently soldered or cleaned near the input node** | The leading candidate for two noisy captures on 2026-09-16. **Do not judge noise soon after work at the input node** |
| **Mechanical, not electrical** | With no junction the electronics are flat white noise at 8 to 14 counts. **With a junction everything extra sits below about 30 Hz, with no peak at 60 or 120 Hz.** That is the instrument moving, not the electronics |
| **A loose, moving conductor near the input node** | A large sheet of loose gold next to a 100 MOhm input modulates stray capacitance |

### The tip snaps into contact instead of finding a gap

**This is the current blocker and it is not solved.** Measured on the fitted sample: the current
changes by a factor of ten per roughly 1,650 to 1,970 Z counts going in, against about 6 to 13 for
tunnelling on the inherited scale, and every run shows 705 to 1,868 counts of in/out hysteresis.

**Candidates, and none is ruled out:**

| Candidate | Status |
|---|---|
| The gold leaf lifting electrostatically | **The 2026-09-19 sandwich build was made to fix exactly this.** Leaf held by adhesive cannot lift. **The far edge is still free** |
| The backing paper under the gold | **Untested.** Roughly 50 to 100 microns of compressible cellulose immediately under the measurement surface |
| A blunt or bent tip | The fitted tip was "very blunt" when new and has since been pressed into the gold four times |
| The sample plate sticking and slipping on its three ball supports | **Untested.** Magnetic stiction between the plate's four magnets and the steel balls is a concrete mechanism |
| Magnetic pull on the tip holder's metal stake | **Untested, and a ten-second magnet test settles it.** Tungsten itself is ruled out — it is paramagnetic and very weakly so, and the magnets' field varies over millimetres while the approach happens over microns, so the force is constant across the gap rather than rising |

> **This symptom and the one below are two of the five ranked in
> [`../WHAT_HELD_US_BACK.md`](../WHAT_HELD_US_BACK.md)**, which puts them in order of how much each
> one blocked an image and gives the cost of fixing each. **Read it before deciding what to do at
> the next bench session**; this section is the bench-side view of the same five.

### The gap will not hold still

**With the motor and hands still, and only the piezo sweeping, the gap moved by at least 43,000
counts in 6.4 s and at least 56,000 over about two minutes.** No period was evident, but the data
are too sparse to exclude one.

**Seven untested candidates, not ranked** (`STATUS.md`, the canonical list): the leaf on its paper;
the plate on its rubber bands and ball contacts; thermal motion of the printed head; **air
currents**; **the undressed cables** — an orange lead and a four-way bundle cross from the suspended
platform to the fixed bench and no photograph shows either clamped, taped or tied to a strain-relief
point, and a cable is a nonlinear path to ground that can stick and release; **the coin mass**,
standing tall and unrestrained and free to slide; and **the spring-hook-in-eyebolt joints**.

**The last three came from the photograph review of 2026-09-19 and are candidates only.** A
photograph shows what is touching what, never what moved.

**One further candidate applies to the 6.4 s excursion alone: relaxation after a motor move.** That
window opened 0.1 s after a 60-step retract ended. **It does not explain the measurement** — the
motion reversed and overshot its own starting point, which settling and creep do not do, and the
two-minute figure is measured long after any post-move transient. It is listed so that nobody
rediscovers it as an objection.

> **The free test comes first:** put a cardboard box over the whole instrument, **standing on the
> bench and not on the suspended platform**, leave the room, and repeat the stillness measurement.
> **If the gap holds still with the box and not without, that is the answer and it cost nothing.**

### Drift that appears minutes into a session

**The prime suspect used to be the motor left energised, heating the scan head. That is fixed** —
the coils switch off after every move on the current firmware. **If drift appears anyway, confirm
the driver LEDs really are dark between moves**, and then look at the mechanical candidates above.

---

# 11. How to resume the project after the move

> **This is the most important section in the manual, and it is the one with the most UNKNOWNs in
> it.**
>
> **The instrument was taken apart and moved on 2026-09-19.** `SAID`, Jacob, about 14:19 UTC:
> *"We are now taking it apart and moving it to News House as I'm flying to San Diego for college.
> We will probably continue a little bit less frequently over the next few months."*
> **"News House" is read as Nuh's house and is an inference, not confirmed.**
>
> **What was taken apart, and how it was packed, is UNKNOWN.** Nobody wrote it down. **So nothing
> about the parked state can be assumed**, including the two-turn back-off recorded before the
> move.

**The order below is deliberate: every step is either something that cannot break anything, or
something that protects the step after it. Do not reorder it.** In particular, **every mechanical
and continuity check comes before any power**, and the tip goes in last.

## Stage A — the computer, before you touch the hardware

**None of this needs the instrument.**

1. **Pull the repository** on whatever computer will run the session, and install the tools.

   ```
   git pull --ff-only origin main
   pip install -r Code/pc/requirements.txt
   ```

   On Windows use `py -m pip install pyserial`. **Type `py`, never `python` or `python3`.**

2. **Run the fact checker and read its exit code**, as its own command, not inside a chain.

   ```
   python3 Code/pc/check_facts.py
   ```

   **If it reports anything, fix it before starting work** — it means a number known to be wrong is
   sitting somewhere it will be believed.

3. **Prove the tools run with nothing plugged in.**

   ```
   py Code/pc/stm_console.py GSTS
   ```

   **The pass is exactly `No Teensy found. Ports seen:` with nothing after it.** It exits with code
   1, which is normal for this check. An error mentioning `serial` means pyserial went into a
   different Python.

4. **Run every tool's self-test** (section 7.1). They need no hardware.

5. **Read `STATUS.md`, then every session log carrying the newest date** — there is often more than
   one file for a date and neither supersedes the other. **Then `docs/NEXT_SESSION_PLAN.md`.**

> **Which computer.** Nuh's machine has run the instrument and every bench session so far; Jacob's
> Windows machine was set up on 2026-09-16 and works. **Claude Code on the web cannot reach the
> Teensy from either** — a web session runs in a cloud container and can see only the repository,
> never a USB port. **The tools only run where the USB is plugged in.**
>
> **The 2026-09-19 morning scripts run only on Jacob's laptop.** They carry absolute paths, a
> hardcoded COM port, `winsound`, and they all assume HIGH Z extends toward the sample. **On any
> other computer, use the portable tools in `Code/pc/`, or promote the scratch scripts first.**

## Stage B — take stock of what actually came out of the boxes

**Before rebuilding anything, look at what you have and write it down.**

6. **Go through `docs/INVENTORY.md` row by row and re-confirm each one.** That file is the only
   record of physical reality in this project, and **every row in it describes the instrument as it
   was before it was taken apart.** Anything that changed in the move — a part that went missing, a
   wire that came off, a board that got knocked — belongs in that file **the same day**.

7. **Look for damage specifically at these four places**, which are the fragile ones:

   | Where | Why it is fragile |
   |---|---|
   | **The preamplifier's input node** | The PTFE standoff **does not sit in its board hole** — it rests on the board surface, held only by the 100 MOhm resistor's own lead in tension. **A knock can lean it onto IC1's grounded leg about 2 mm away and short the input.** This is the single most fragile thing in the instrument |
   | **The four 40 AWG ground repair wires on the preamp board's underside** | Hair-thin, and the box has a support post 4 mm tall that passes within about 0.6 mm of the nearest one. **Offer the board onto the post and look underneath before screwing it down** |
   | **The tip and its holder** | The tip pushes into a socket on a stake that is glued to the piezo disc. A bent tip is not obvious by eye and has already fooled this project once |
   | **The piezo disc itself** | **It is destroyed silently.** It still measures correctly on a meter after it is ruined; it simply stops moving |

8. **Check the rubber bands.** Rubber perishes over weeks. Replace any that are cracked or slack.

> ### Figure 11.1 — `12_teardown_platform_off_frame.jpg`
> **The move, documented.** The suspended platform lifted off the frame at 10:15 camera-local on
> 2026-09-19, **with the head, the stepper and the preamplifier box still mounted on it.**
>
> **This answers half of what `STATUS.md` records as UNKNOWN.** Between 10:05 and 10:16 the jumper
> leads were unplugged, the supply leads pulled, the boxes opened, and the platform came off as one
> piece. **How it was packed is still UNKNOWN** — no frame shows anything going into a box.
> `READ`. Source frame `IMG_4916`, Nuh's camera.
>
> **So the most likely reassembly job is hanging that platform back on its three springs**, rather
> than rebuilding the head from parts. **Confirm that before assuming it**, and write what you find
> into `docs/INVENTORY.md`.

9. **Do not repair or rebuild anything yet.** The two standing rules are that **nothing is glued to
   the spare preamp board** (`STATUS.md` safety rule 10) and **no cyanoacrylate goes anywhere near
   the preamp or into its enclosure** (`STATUS.md` safety rule 5).

## Stage C — rebuild the mechanics, unpowered

10. **Rebuild the isolation tower and hang the platform.** Three M8 rods, three spring hangers,
    three springs, the Ø200 mm platform.

11. **Check the platform hangs free.** Nothing may touch it — no cable, no rod, no tie. **A bypass
    makes every spring calculation meaningless and no spring change works around it.** Check every
    wire that leaves the platform has slack: the coax to the preamp, the loom, the stepper leads.
    **A wire that goes taut across the suspension is a rigid bypass, and it could also pull on the
    preamp input node.**

12. **Measure the clearance under the platform**, and write it down. **This has never been measured
    and it is the number that decides what the suspension can do.** You need enough room below the
    platform for it to droop into once the springs are loaded.

> ### Figure 11.2 — `02_platform_damping_gap.jpg`
> **The gap under the suspended platform, and why a photograph cannot measure it.** A bright disc
> is fixed under the black platform and a ring of dark cylinders stands on the tower below it.
> Background light shows between them in some places and not others, which is what a near-edge-on
> view of a small gap looks like.
>
> **NO GAP HAS BEEN MEASURED AND NONE MAY BE TAKEN FROM THIS FRAME.** Jacob settled the question at
> the bench: *"its not sitting on the tower is just about its a perfect fit"* (`SAID` 2026-09-19).
> **The actual clearance is still the unmeasured number that decides what the suspension can do.**
> Source frame `IMG_8624`, 2026-09-18 19:09:07 camera-local.

13. **Check the eddy-damping gap.** The aluminium plate must sit in the magnet gap without touching.
    **A plate resting on its magnets is not damping; it is a clamp.** The magnet holder's height is
    not adjustable, so the platform is the only way to trim this.

14. **Put the coin mass back on and count the bounces.** Nudge the platform gently — **sideways, or
    very gently downward, because the clearance under it is small** — and watch.

    | What it does | What it means |
    |---|---|
    | **Bobs about twice a second**, roughly seven cycles in three seconds | **The springs are OPEN.** The resonance is about 2 Hz and the isolation is working |
    | **A hard, fast, barely-there return**, no countable bounce | **Still shut.** The coils have not opened and the springs are behaving as stiff wire |
    | Sinks back over one or two cycles and stops | Open, and the eddy damping is doing its job |

    **This measures the resonance directly and needs no spring theory at all.** Film it on a phone
    if counting is hard.

15. **Do not add more mass.** The printed height adjusters are already at maximum, so another sag
    could not be corrected, and going from 0.8 to 1.2 kg buys only about 20% on the resonance.

16. **Rebuild the scan head on the platform**, and confirm the sample plate sits on **all three**
    ball ends with the **motor-screw ball actually touching the plate**. On 2026-09-17 both rubber
    bands pulled in line with the two side-by-side balls, so nothing held the motor end down and
    the screw turned in free space for a whole session.

## Stage D — rewire, unpowered

17. **Rewire from `docs/WIRING.md`, not from memory and not from photographs.**

18. **Verify the DB9s by beeping them out with the connectors unplugged.** That needs no colour
    table at all and it is the best check available. The procedure is in
    `docs/NEXT_SESSION_PLAN.md`. **Read the orange trap in section 3.6 of this manual first.**

19. **Meter every shield.** Every point on each shield must beep to its ground wire — near the wire,
    the far corner, and across every seam. **One bond per shield, to AGND.** Two copper-wrapped
    parts touching each other is a second path and therefore a loop.

20. **Take the four unpowered checks from section 5.1**, all of them.

## Stage E — first power, with no tip fitted

**Fit no tip for this stage. With no tip, nothing can be crashed, and every test below is
zero-risk.**

21. **Bring up from cold following `docs/soft_launch_test_procedure.md` stages 0 to 6**, and read
    `docs/DAC_BOOT_STATE.md` first. **Supplies on first, then USB.**

22. **Stage 1, digital only:** `GSTS` must return ten fields with `time_millis` climbing.

23. **Stage 2, the motor:** `MTMV 512` should take about 7.5 s, the driver LEDs should chase, and
    `GSTS` field 6 should then read 512. **`MTMV -512` should bring it back.** Confirm **the driver
    LEDs go dark after the move** — that is the 2026-09-16 firmware fix working.

24. **Stage 3, the analog rails:** LED5 and LED6 both lit, then **LED1 to LED4 checked**, then park
    every axis at 32768.

25. **Stage 4, DACs and ADC:** `BIAS 33000`, then `GSTS` to see field 1 read back. **That proves the
    firmware registered the command, not that the chip output the right voltage** — only a meter
    settles that. Then `ADCR` a few times and look for a plausible number that varies slightly.

26. **Stage 5, the piezo:** use `TONE`, not `TEST`, because `TONE` parks Z at 0 V instead of leaving
    it at a rail. **Judge it with a meter, not by ear**: `DACZ 65535` should give −10 V at the scan
    head end of the DSUB1 cable, on the row-of-four signal wires.

27. **The preamplifier, about two minutes after power-on:** `ADCR` should sit within a few tens of
    counts of zero with the tip lead connected and nobody nearby. **This is the acceptance test for
    the whole measurement chain, and it is the number to compare against 2026-09-19's 40 to 42
    counts of standard deviation with the tip clear.**

28. **Re-run the dummy junction test if anything about the preamplifier was disturbed.** A 100 MOhm
    resistor clipped between the bias wire and the tip holder, bias stepped across its range.
    **The expected answer is about 320 counts per nA, and a positive sample voltage gives negative
    counts.** This is the project's strongest single result and it is cheap to repeat.

## Stage F — fit the tip, and only then

29. **Fit a fresh, sharp tip.** The one that was packed is blunt and has been pressed into the gold
    four times. **`docs/NEXT_SESSION_PLAN.md` asks for a sharper one before the next imaging
    attempt.**

30. **`STATUS.md` safety rule 7: meter the tip holder against the brass piezo electrode. It must
    read OPEN.** Do this after every tip change and after every holder rebuild.

31. **Re-check the Z direction.** It belongs to the tip, not to the instrument. Use a +/−2,000 Z
    lock-in at a clean touch, or `Code/pc/stm_approach.py --z-retracted unknown`, which parks Z at
    midscale for every motor step and searches both ways until first contact tells it. **Do not run
    any of the 2026-09-19 morning scripts until this is confirmed** — every one of them assumes HIGH
    Z extends toward the sample.

32. **Re-check the motor direction is still negative-approaches.** It was settled at the bench and
    nothing about the move should change it, **but the geometry that decides it is a 1 mm lever arm
    and the tip has changed.**

33. **Re-do the hand-set.** The two-turn back-off recorded before the move applies to the old tip
    and the old sample, and **both may have changed.** Turn in from well back with the beeper
    already running.

## Stage G — the science, in the order the plan sets

**`docs/NEXT_SESSION_PLAN.md` is canonical for this and it is written to be executed with no memory
of any conversation.** In short:

1. **The free test first: is it air?** A cardboard box over the whole instrument, standing on the
   bench and not on the platform, then a 15-minute stillness recording. **If the gap holds still
   with the box and not without, that is the answer and it cost nothing.**
2. **A stiffer sample.** In order of preference: a rigid gold surface that does not bend (a
   gold-plated PCB pad, a connector contact); HOPG, which is a purchase and should be decided only
   after step 1; or the leaf bonded all round with no paper under it. **Check `docs/INVENTORY.md`
   and ask before assuming any of these is in the room.**
3. **A sharper tip**, already covered above.
4. **Get the gold within reach** with the live back-off, then approach in 20-step chunks with a
   full Z sweep between, and **start the Z test the instant it finds the gold** — on 2026-09-19 a
   30-second gap between two commands was enough to lose it.
5. **Prove the gap holds still BEFORE any scanning.** Right after a find, with the motor still, a
   full sweep every 5 s for 15 minutes. **Pass: the onset stays within about 500 counts for 15
   minutes.** Any sweep that reads out-of-reach voids the run.
6. **Only then the Z test, and a scan with the constant it measures.** A real tunnel junction gives
   a decade of current per tens of counts or fewer, little hysteresis and gradual onsets.
   **Re-measure the constant immediately before each scan** — on 2026-09-19 it drifted about
   fivefold inside a single run.

**Do not, at any point:** run `APRH`; send `CCON` with a tip in range; send a DAC value outside
0 to 65535; or trust the first reading after a large upward Z jump.

## Stage H — write it down the same day

34. **Write the session log**, `sessions/YYYY-MM-DD.md` from `sessions/TEMPLATE.md`, and **add a row
    to `sessions/README.md`.** **If a log for today already exists, check whose it is** — if it is
    the other person's, start `sessions/YYYY-MM-DD-<your name>.md` instead of appending to theirs.

35. **Update `STATUS.md`** — the stage table, open faults, next actions, open questions, and the
    "Last updated" line.

36. **Update `docs/NEXT_SESSION_PLAN.md`**, including its own `Last updated` line. The fact checker
    fails if a session log is newer than it, and the pre-commit hook then blocks the commit.

37. **Write everything you learned about the physical instrument into `docs/INVENTORY.md`** — what
    was reassembled, how, by whom, and what changed. **These facts live in Jacob and Nuh's heads and
    in their email, and anything that stays in a conversation is lost.**

38. **Commit and push.**

    ```
    git add -A
    git commit -m "Session YYYY-MM-DD: <one line on what changed>"
    git pull --rebase origin main && git push origin main
    ```

    **Work that is not pushed does not exist as far as the other computer is concerned.**

---

# 12. What is still unknown, and what is untested

**`docs/OPEN_QUESTIONS.md` is the authoritative register.** This section lists only the ones that
would change how you operate the instrument, and marks clearly what is a recommendation nobody has
tried.

> **For what to do about them, in priority order, go to
> [`../WHAT_HELD_US_BACK.md`](../WHAT_HELD_US_BACK.md).** It ranks the five mechanical blockers and
> costs each fix — measuring `d` with a loupe and the box test are minutes each with no power, an
> etched tip is an afternoon with equipment already owned. **This section says what is not known;
> that one says what to do first.**

## 12.1 UNKNOWN — nobody has established these

| | Why it matters | What would settle it |
|---|---|---|
| **How far the tip is from the line through the two side-by-side ball ends, and on which side** | **The most valuable unmeasured number in the instrument.** It sets the lever ratio and therefore the Z scale in nanometres, and that decides whether the measured current-versus-Z slope is tunnelling or pressing | Plate off, a straightedge laid across the two ball ends, and see which side the tip stands on and by how much. **No electronics needed** |
| **Our scanner's displacement per volt** | Every nanometre figure for this instrument is inherited from Berard's disc, which is not ours | A real scan calibration, once the gap holds still |
| **What moves the gap** | It is the blocker | The box test, then a rigid sample, then the plate mounting |
| **The platform-to-tower clearance, and the eddy-damping gap** | They decide whether the suspension can work at all | A ruler, at reassembly |
| **The suspended mass, and the actual spring resonance** | The isolation figures are calculated, not measured | The bounce test, thirty seconds. Or staged loading with a ruler, which gives the spring rate and the platform mass together |
| **What the tip holder's "metal stake" is made of** | If it is ferromagnetic, the sample-plate magnets pull on it with a force that rises steeply as the gap closes — a second snap mechanism | **Hold a spare magnet near it. Ten seconds** |
| **Whether the DAC configuration loss recurs mid-session** | If it is startup-only, one `RSET` at the start is enough. If it recurs, LED1 to LED4 must be checked around every single measurement | A controlled test: powered, idle, LEDs watched |
| **The Keystone 11301's actual through-board diameter** | It decides how the input node should be held permanently | Calipers, which **we do not own** |
| **Whether the preamp box's support post presses on the underside repair wires** | A 3.6 mm post pressing a hair-thin wire against the board could break it or short it, and it would only be found after the board was screwed down | Offer the board onto the post and look underneath |
| **Whether the new preamp box's wrap is copper with conductive adhesive** | Aluminium will not do | Look, and meter it |
| **Which parts JLCPCB left off the preamp assembly, beyond the resistor and the standoff** | Decides what has to be hand-fitted on any spare board | The JLCPCB order confirmation email |
| **What was taken apart in the move, and how it was packed** | Everything in section 11 | Ask, at reassembly, and write it into `docs/INVENTORY.md` |

## 12.2 Recommendations that are untested

**These are on record as good ideas. None has been tried, and none should be presented as a fix.**

| Recommendation | Status |
|---|---|
| **A cardboard box over the instrument to test for air currents** | **Untested.** Free, and it is step 1 of the plan |
| **A rigid gold surface or HOPG instead of gold leaf on paper** | **Untested.** HOPG is a purchase — **decide only after the box test** |
| **Removing the backing paper by putting gold straight onto the copper tape's adhesive** | **Untested.** It is Jacob's own fallback |
| **Anchoring more of the gold leaf's perimeter** | **Untested.** The next move if the snap comes back |
| **Two wires on U13 to tie off its floating op-amp channel** | **Untested.** Low risk, no track cutting, not on the critical path |
| **Removing the 50 mm spring-hanger section to raise the platform** | **Untested, and which sections are currently fitted is UNKNOWN.** It would give about twice the droop room needed |
| **Fastening the coin mass to the platform instead of standing it in tubes** | **Untested.** A tube that can tip or slide is a stick-slip source on the one stage whose stability is the problem |
| **Centring the tip on the piezo disc if the holder is ever rebuilt again** | **Untested, and it is free when the holder is open.** It buys maximum Z throw, less X-to-Z coupling, and fixes the lever arm by construction |

## 12.3 Things that are settled — do not spend bench time re-proving them

| | |
|---|---|
| **The piezo scanner** | **Built and working.** Do not re-open it, do not buy low-temperature solder paste, do not spend time on the disc-versus-seat question. **A working scanner exists, so whatever went in fits** |
| **The ADC full scale and the counts-per-nA** | Settled from the datasheet and **measured end to end** |
| **The sign of the reading** | **Measured.** A positive sample voltage gives negative counts |
| **The preamplifier** | **About 4 pA in its box. It is not the problem** |
| **The motor direction** | **Negative approaches**, settled at the bench |
| **That the gold leaf is real gold, and that the copper tape's adhesive conducts** | Both settled 2026-09-17 |

> **A row was removed from the table above on 2026-09-20, and it is worth saying why.** It read
> **"The shields — printed, wrapped, grounded and metered end to end"**, and the metering half of
> that is not true. **The shields are printed, wrapped and grounded. Nobody has metered one end to
> end.**
>
> **This mattered more than an ordinary wrong row, because it sat under a heading telling you not
> to spend bench time on it.** Four other places in this documentation set record the same check as
> still owed — section 3.9's note on figure 3.6, **section 11 step 19, "Meter every shield"**,
> `INCONSISTENCIES.md` item B8, and the poster Q&A. All four are right and the row was wrong.
>
> **Do it at reassembly.** Every point on each shield must beep to its ground wire — near the wire,
> the far corner, across every seam — and each shield gets exactly one bond to AGND. It takes about
> two minutes.

---

# Appendix A: glossary

| Term | What it means here |
|---|---|
| **Counts** | The raw number the ADC returns, or the raw code sent to a DAC. DAC codes run 0 to 65535 with 32768 as 0 V. **1 nA of tip current is about 320 ADC counts** |
| **Setpoint** | The current the feedback loop tries to hold, expressed in ADC counts |
| **Trace and retrace** | Each scan line is swept forward and then backward. Whether the two agree is the first test of whether a feature is real |
| **The X-held control** | A run with identical timing to a scan, but with X never moving. Anything the control also produces is not surface structure |
| **Detrending** | Removing the straight-line tilt from a pass before comparing it with another. **Nothing in this project's correlations means anything until it is done** |
| **The woodpecker approach** | Coarse approach where only the piezo ever closes the gap: retract Z, step the motor, sweep Z looking for current, repeat |
| **Hand-set** | Closing the gap by turning the fine screws by hand until a meter or a beeper says the tip is touching, then backing off. **The motor's whole reach at the tip is only about ±75 microns, so this has to get within about a tenth of a millimetre** |
| **Backlash** | Lost motion after the motor reverses. **100 to 250 steps here**, measured twice |
| **The lever** | The three-screw geometry that turns a screw movement into a much smaller sample movement. **Design ratio 40, unmeasured** |
| **Burnishing** | Pressing and smoothing gold leaf with something soft in small circles until it goes from dull and loose-looking to bright and flat. **That change is how you know it has taken** |
| **ALERT** | The AD5761 pin that says a DAC has lost its configuration. On this board it goes to an LED and nowhere else |
| **`AGND`** | The controller's single ground net. **There is no separate digital ground on this board** — every ground pin on every chip is the same node |
| **Virtual ground** | The amplifier's inverting input, held near 0 V by the feedback loop. **The tip sits here. It is not a real ground** |
| **PAD1** | The bare test pad on the preamp board. **It is the amplifier's OUTPUT, not the tip input** |
| **`SAID` / `READ` / MEASURED** | Jacob or Nuh told us / somebody's reading of an image, plausible and unconfirmed / read off our own hardware with a date |

---

# Appendix B: figures

**Eleven figures are placed and two slots are still empty.** All the placed ones have been opened.
Ten come from `deliverables/2026-09-19-pause/photos/prepared/`, which carries its own caption bar on
each image naming the source frame, its camera-local capture time and whether the reading is `SAID`
or `READ`. The eleventh is an existing repository photograph.

**Nothing in this manual describes a photograph that has not been opened, and no dimension is taken
off any of them.**

| Figure | Section | File | What it carries |
|---|---|---|---|
| **3.1** | 3.9 | `photos/prepared/04_instrument_full_height.jpg` | The whole instrument on the morning of the move |
| **3.2** | 3.9 | `photos/prepared/05_scan_module_in_hand.jpg` | The scanning module off the frame — the best view of how the subsystems sit together |
| **3.3** | 3.9 | `photos/prepared/07_teensy_carrier_and_ribbon.jpg` | The Teensy carrier and the 26-way ribbon |
| **3.4** | 3.9 | `photos/prepared/08_bench_power_supplies.jpg` | The two bench supplies, models legible |
| **3.5** | 3.9 | `photos/prepared/06_stepper_28byj48_label.jpg` | The stepper, its own label legible |
| **3.6** | 3.9 | `photos/prepared/09_faraday_enclosure.jpg` | The scan head shield, off the instrument |
| **4.1** | 4.5 | `photos/prepared/01_sample_plate_gold_window.jpg` | The sample window — gold over part of it, copper exposed beside it |
| **4.2** | 4.5 | `photos/prepared/03_sample_plate_rubber_bands.jpg` | The two twisted rubber bands that hold the plate on |
| **4.3** | 4.5 | `Images/ours/2026-09-18_scanhead_face_1.jpg` | The scan head face, with the three ball ends and the pivot line |
| **11.1** | 11 Stage B | `photos/prepared/12_teardown_platform_off_frame.jpg` | The platform lifted off the frame during the move |
| **11.2** | 11 Stage C | `photos/prepared/02_platform_damping_gap.jpg` | The gap under the platform, and why it cannot be measured from a photograph |

**Still empty, and named so that anyone at the bench knows what to take:**

| Slot | Section | What is wanted | Why no frame exists |
|---|---|---|---|
| **TODO-PHOTO A** | 4.5 | **The DSUB2 splice at the preamp end**, showing the five-way row | Nothing in either new batch shows it. **A caption for it must not quote colours read off the frame** — the preamp's own lead colours are not the J1/J2 colours |
| **TODO-PHOTO B** | 4.5 | **The tip itself, close enough to judge sharpness** | The nearest frames are the 2026-09-16 tip-protrusion pair, and that tip has since been replaced twice |

**Two further things that would be worth having and are not photographs.** `docs/INVENTORY.md` and
`deliverables/2026-09-19-pause/photos/IMAGE_INVENTORY.md` both record them as missing: **how the
instrument was packed** (no frame shows anything going into a box) and **the bench video clips**,
which are all over the file-transfer size limit that was available.

---

**End of manual.**

**Written 2026-09-19 at the pause point. It consolidates `STATUS.md`, `docs/FACTS.md`,
`docs/WIRING.md`, `docs/COMMANDS.md`, `docs/COMPONENTS.md`, `docs/ENGINEERING_REFERENCE.md`,
`docs/BOM.md`, `docs/INVENTORY.md`, `docs/INDEX.md`, `docs/DAC_BOOT_STATE.md`,
`docs/NEXT_SESSION_PLAN.md`, `docs/START_HERE_gotchas.md`, `docs/soft_launch_test_procedure.md`,
`docs/OPEN_QUESTIONS.md`, `README.md`, `SETUP.md`, `Code/pc/README.md`, `CAD/prints/README.md`, the
four `sessions/data/*/README.md` files, `Images/ours/README.md`, and the firmware in
`Code/teensy/`. Its figures come from the photograph review in
`deliverables/2026-09-19-pause/photos/`.**

**Where it disagrees with any of those, they win and this file is the one to fix.** The
corrections it makes to them are listed in `CHANGELOG.md`, and the contradictions found between
them are listed in `INCONSISTENCIES.md`, both in this directory.
