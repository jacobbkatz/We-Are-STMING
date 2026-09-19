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
20 mA setting and dropped into constant-current mode at about 2 V; at 200 mA it worked, drawing
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

> **TODO-PHOTO 1 — the whole instrument on its frame.** Wanted: one frame showing the printed
> tower, the suspended platform with its coin mass, the scan head on top and the supplies and
> laptop in shot, so that a reader who has never seen it understands the scale and the layout.
> Candidate source: the 2026-09-19 morning set.

> **TODO-PHOTO 2 — the controller board with its connectors labelled.** Wanted: a frame in which
> H1 (top left), DSUB1 (bottom left), DSUB2 (bottom right) and U19 (right edge) are all visible,
> to go beside section 3.1. `Images/ours/2026-09-16_controller_board.jpg` exists and is a
> candidate; it has not been opened for this manual, so it is not cited as showing this.

> **TODO-PHOTO 3 — the preamp box in place at the centre of the scanning module.** Wanted: the
> top-down view that shows where the amplifier physically sits relative to the head.
> `Images/ours/2026-09-16_scan_module_top_down.jpg` is identified by Jacob as exactly this
> (`SAID` 2026-09-18) and is the best existing candidate.

---

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

> **TODO-PHOTO 4 — the scan head face, straight on.** Wanted: the piezo disc recessed in its bore,
> the tip, the tip lead crossing the face, and all three ball-end screws in one frame.
> `Images/ours/2026-09-18_scanhead_face_1.jpg` through `_4.jpg` are existing candidates.
> **No dimension may be taken off any of them** — three attempts to measure the tip-to-pivot
> distance from these frames gave three answers more than a factor of two apart.

> **TODO-PHOTO 5 — the sample plate off the head, showing the gold.** Wanted: the aluminium tape
> over the face, the window cut in it, and the gold assembly inside the window with the bias wire
> entering at the top. `Images/ours/2026-09-17_sample_plate_rebuilt.jpg` shows the 2026-09-17
> build; **a frame of the 2026-09-19 sandwich build would be more useful** and may be in the new
> 2026-09-19 set.

> **TODO-PHOTO 6 — the plate mounted, with the rubber bands and the three screws visible.**
> Wanted specifically to show which way round the plate goes and how the bands are routed, because
> the band routing is what failed on 2026-09-17.

---

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
