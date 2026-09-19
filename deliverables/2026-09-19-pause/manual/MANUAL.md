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

---

## Table of contents

1. [What the instrument is](#1-what-the-instrument-is)
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
- [Appendix B: figure slots](#appendix-b-figure-slots)

---

# 1. What the instrument is

## 1.1 In one paragraph

A scanning tunnelling microscope holds a sharp metal tip about a nanometre above a conducting
surface, puts a small voltage between them, and measures the tiny current that quantum-mechanically
tunnels across the gap. That current changes about tenfold for every 0.1 nm of gap change, which is
what makes the instrument sensitive enough to see atoms. **Ours is built from 3D-printed parts**,
following **Mech Panda's `red-panda-stm`** for the mechanics, firmware and controller board, and
**Dan Berard's home-built STM** for the scan head and the transimpedance preamplifier.

**What it demonstrably does today** (all MEASURED, all in `docs/FACTS.md` and the session logs):

- **The measurement chain works end to end and is calibrated.** A 100 MOhm dummy junction gave
  −3,205 +/− 37 counts per volt against −3,200 predicted, 53 readings, R-squared 0.993. That is
  the project's strongest single result.
- **A real tip-to-gold junction has been made**, repeatedly, and its current responds to Z and to
  the sign of the bias.
- **The electronics are quiet enough.** Tip clear, the reading's standard deviation was 40–42
  counts on 2026-09-19; with a junction and X held it was 9–19 counts. A tunnelling current is
  about 1 nA, which is about 320 counts.

**What it has not done:**

- **No image has been produced.** Every feedback scan is matched or beaten by its own X-held
  control, so nothing in them is established as surface structure.
- **The junction is not a clean tunnelling gap.** On 2026-09-19 the current changed by a factor of
  ten per roughly 1,650–1,970 Z counts going in, where tunnelling on the inherited (and unmeasured)
  Z scale would be about 6–13 counts. Every run showed 705–1,868 counts of in/out hysteresis. The
  interpretation on record is **"a soft, pressed, sticky contact"** — and it is marked as
  interpretation, not proof.
- **The gap does not hold still.** With the motor and hands still, it moved by most of the Z range
  within seconds to minutes. **What moves it is UNKNOWN**; four untested candidates are the gold
  leaf on its backing paper, the sample plate on its rubber bands and ball contacts, thermal motion
  of the printed head, and air currents.

**So the blocker is mechanical, not electrical.** That is the single most useful sentence in this
manual, because it tells you where not to spend time.

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
> gives 40, but that assumes the tip sits at the disc centre. Jacob's bench estimate of the tip's
> distance from the pivot line is *"between 1mm and 0mm its really hard to measure"*. **A
> straightedge laid across the two ball ends settles it and needs no electronics.** It decides the
> Z scale in nanometres, and therefore whether the measured current-versus-Z slope is tunnelling or
> pressing. See `docs/OPEN_QUESTIONS.md`.

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

**Four tips have been fitted. Documents from different days mean different tips.**

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
