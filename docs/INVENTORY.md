# What we physically own

**This file exists because the project got a fact wrong four times in one session for the same
reason: there was no record of what is actually in the room.**

`docs/BOM.md` records what was **specified**. This file records what was **bought and received**.
They are not the same, and on 2026-09-09 they disagreed about the one part the instrument's
sensitivity depends on.

> **Rule.** What we physically own cannot be derived from any design file, netlist, BOM or
> shopping list in this repository. If it is not written here, **ask Jacob or Nuh** or mark it
> UNKNOWN. Do not infer it from a document. See `CLAUDE.md` §3d.

**Provenance marks:** `ORDER` an order confirmation or invoice · `PHOTO` a photograph ·
`BENCH` seen or measured in the room · `SAID` Jacob or Nuh stated it.

---

## Boards

| What | Qty | How we know | Notes |
|---|---|---|---|
| **Controller PCB, assembled** | 5 | `ORDER` | JLCPCB PCBA, $321.44 for 5, ~$64 each. See `gerbers/README.md` |
| **Preamp PCB, assembled (PCBA)** | **2** | `SAID` 2026-09-09, Jacob | **JLCPCB PCBA, not bare.** One is built into the current preamp box; one is the spare |
| **Preamp PCB, silkscreen only (bare)** | the rest of the order | `SAID` 2026-09-09, Jacob | Ordered 2 assembled, the remainder bare |

### State of the two preamp boards — 2026-09-13, `BENCH`

| Board | State |
|---|---|
| **Old board** (glued in the original box) | **IC1 pin 3 not connected to JP1 pin 1** (beep test). C2's ground end not connected either. C1/C2 stripe orientation **not checked** |
| **Spare board** | **C2 was reversed, rotated with the original part** (4.65 µF after). Four jumper-cable leads in JP1 holes 1, 2, 3, 5; hole 4 empty. Underside vias for IC1 pin 3 and C4 scraped and wired to hole 1 with 40 AWG magnet wire; **C2 and C3 not yet wired; repair not verified; never powered**. Possibly a leftover partial wire on the top side from an abandoned attempt — UNKNOWN |

> **The 2026-09-11 order:** "we have all components except for the standoff" — `SAID` 2026-09-13.
> **VERIFY item by item** (RMA791 flux, syringe dispenser, M2 screws, heat shrink); not individually
> confirmed. **Whether the 1812 ceramics were ordered is UNKNOWN.**

### What JLCPCB did NOT fit on the preamp PCBA

`SAID` 2026-09-09, Jacob. **These are ours to solder:**

- The **100 MΩ feedback resistor** — deliberate, it is air-mounted on the PTFE standoff
- The **PTFE standoff terminal** itself
- Some other parts, not itemised. **UNKNOWN which** — see `docs/OPEN_QUESTIONS.md`

**What JLCPCB DID fit:** IC1, C1, C2, C3, C4, R1. Confirmed by the shopping list's "already
fitted" line and by Jacob 2026-09-09.

> ### JLCPCB flagged C1 and C2 polarity at order time
>
> `SAID` 2026-09-09, Jacob: *"this came up in the ordering, they couldn't determine the polarity
> of C1 and C2."*
>
> **This matters.** The board carries **no polarity marking on the silkscreen** — both pads of C1
> and of C2 get an identical plain rectangle (aperture D16 in `tunnelAmp-F_Silkscreen.gbr`), and
> the Eagle footprint's anode stripe sits on layer 51 (tDocu), which is never plotted. So JLCPCB
> had nothing on the artwork to work from and had to ask.
>
> **How the question was answered at ordering time is UNKNOWN.** Which way the parts actually went
> on can only be settled by looking at the boards. See `STATUS.md` fault 1d.

---

## Parts in hand

| What | Qty | How we know | Notes |
|---|---|---|---|
| **Keystone 11311** turret terminal, PTFE insulated | **2** | `ORDER` DigiKey salesorder **100750867**, 2026-08-02, DK part 36-11311-ND, $2.81 ea | **Does NOT fit our board.** Needs a Ø3.45 mm hole; ours is Ø2.108 mm. Tried at the bench and it would not go |
| **Keystone 11301** turret terminal | **2** | `ORDER` DigiKey **36-11301-ND**, mfr part **11301**, "TERM TURRET SINGLE L=6.35MM TIN", $2.09 ea, $4.18. Order screen seen 2026-09-14 | **The part Berard names.** Received 2026-09-14. **It does NOT enter our Ø2.108 mm hole** — offered up at the bench 2026-09-15 and it would not go; the clearance figure previously stated here was wrong, as were the two claims before it. Its through-board diameter is UNKNOWN, there being no calipers. **PTFE base with metal only on the pole** (`BENCH`, Jacob 2026-09-14) — a top-mount insulated terminal, so the input node gets a real PTFE insulator. **`BENCH` 2026-09-15: a standoff was offered up to the board hole and DID NOT ENTER** — Jacob: "the standoff doesn't fit in the hole at all." **Which part was in hand was not confirmed**, and the two 11311 are in the same room. **Nothing was forced and nothing was drilled.** **`BENCH` 2026-09-15, later the same evening: IT WENT IN AND THE NODE IS BUILT.** Jacob: *"I got it to work, the tension in the resistor wire holds the standoff in place after I solder both together."* **So the hole does not grip the part — retention is the 100 MOhm's own lead in tension, not the hole and not any adhesive.** Safety rule 10 is honoured: nothing was glued. **Not yet confirmed:** whether the part's pin actually sits inside the Ø2.108 mm hole or the standoff rests on the board surface held only by the resistor lead. **The 100 MOhm is a leaded axial part** — it has wire leads that can be put in tension |
| **4.7 µF 50 V 1812 ceramic, for C2** | **0** | `SAID` 2026-09-15, Jacob: *"C2 will be getting replaced, we don't have it"* | **NOT IN THE ROOM and not on order as far as anyone has said.** This was UNKNOWN from 2026-09-13 until now. **It is half of safety rule 14 and it blocks the controller**, so nothing integrates until it is bought and fitted |
| **Preamp box, new print** | **1** | `SAID` 2026-09-15, Jacob: *"the box is printed wrapped and grounded"* | **Printed, wrapped and grounded.** Replaces the CA-contaminated original. **What it was wrapped WITH is UNKNOWN and matters** — `docs/ENGINEERING_REFERENCE.md` §3 requires **copper tape with conductive adhesive**, and the inventory had copper tape as **not owned** as recently as this evening. **Aluminium will not do.** **The shield's continuity has never been metered on any box in this project** — `docs/NEXT_SESSION_PLAN.md` V1 |
| **100 MΩ feedback resistor** | ≥1 | `SAID` | Value CONFIRMED. Not fitted to the board |
| **Tantalum 4.7 µF 35 V** | 1–2 | `SAID`, from a label | Spares beyond the two JLCPCB fitted. **2026-09-13: "we don't have access to a spare" (`SAID`).** Whether they exist somewhere is UNKNOWN |
| **91% isopropyl alcohol** | — | `SAID` 2026-09-13 | In the room. **Not enough for the input-node wash** |
| **99% isopropyl alcohol** | — | `SAID` 2026-09-14 (late), Jacob: "yes IPA is here" | **IN THE ROOM.** Collected this evening as planned. **This was the last gate on the input-node wash** — with the DI water, foam swabs and brush already here, the full cleaning kit is now present |
| **Deionised / distilled water** | — | `SAID` 2026-09-14, Jacob: "I also just got the DI" | **In the room.** For the final rinse after the IPA |
| **Jumper cables** (plugs cut off) | — | `SAID` 2026-09-13 | **Used as the four JP1 leads on the spare board.** Conductor material not checked |
| **JP1 lead colours on the spare board** | 4 | `BENCH` 2026-09-14 late, Jacob, meter in hand | **hole 1 GND = WHITE · hole 2 +15 V = GREY · hole 3 OUT = ORANGE · hole 4 = EMPTY · hole 5 −15 V = TAN.** Recorded for the first time — previously "conductor material not checked" with no colours at all. **These are the jumper-cable colours and they do NOT match the J1/J2 wiring colours in `docs/WIRING.md`** (Jacob, same message). Use these only for the preamp board's own leads |
| **Foam swabs** | — | `SAID` 2026-09-14, Jacob | **In the room.** For the input-node wash |
| **Soft brush** | — | `SAID` 2026-09-14, Jacob | **In the room.** For the input-node wash |
| **Scalpel and razor blade** | — | `SAID` 2026-09-13 | Used to scrape solder mask off vias |
| **Second soldering iron** | access | `SAID` 2026-09-13 | Used for two-iron removal of C2. Model not recorded |
| **40 AWG magnet wire** | — | `SAID` | For the tip lead |
| **Solder, Sn99.3/Ag0.3/Cu0.7 lead-free** | — | `SAID` | Correct for this work. **Do not buy more** |
| **Low-temp solder paste, Sn42/Bi58** | **UNKNOWN** | — | **Nobody has said whether we own any.** Needed for the piezo quadrant wires and nothing else. `docs/BOM.md` §5 specifies it; a specification is not an inventory. **Ask before ordering** |
| **Flux, non-rosin no-clean** | — | `SAID` | **Wrong type for this board.** Superseded by the RMA791 below. **Do not use it on the preamp** |
| **Chip Quik RMA791 rosin paste flux, 50 g jar** | 1 | `ORDER` Amazon, **arriving 2026-09-11** | **The correct flux.** ROL0 — rosin, low activity, halide-free. **Must still be cleaned off** — see `docs/PREAMP_SHOPPING_LIST.md` |
| **Manual flux/glue syringe dispenser** + 10 cc syringe + blunt tips | 1 | `ORDER` Amazon, **arriving 2026-09-11** | Load it from the RMA791 jar. **Solves the jar-vs-syringe question** |
| **M2 self-tapping pan-head screws, 800 pc assortment** | M2x4 to M2x20 | `ORDER` Amazon, **arriving 2026-09-11** | **Use the M2x6.** M2x8 bottoms out in the box pilot — see `docs/FACTS.md` |
| **Heat shrink tubing, assorted kit** | — | `ORDER` Amazon, **arriving 2026-09-11** | **VERIFY whether it is adhesive-lined (dual-wall).** Either way, **none at the input node** — the adhesive lining outgases |
| **Computers that run the project** | 2 | `SAID` 2026-09-16, Jacob: "this is the first time I've run Claude on this computer, we usually use Nuh's" | **Nuh's machine has run the instrument and every bench session so far.** **Jacob's Windows machine was new to the project on 2026-09-16**: no repository, Git or Python present at first. **Confirmed working later on 2026-09-16** (`BENCH`, read off the machine by Claude Code desktop): Git 2.55.0 in `C:\stm\Git`; Python 3.13.15, **reached with `py` only**, because `python` and `python3` are Microsoft Store placeholders and Python's own folder is not on the PATH; pyserial 3.5; the no-Teensy dry run passed. **`bash` is not on its PATH.** The repository is in a folder on Jacob's OneDrive desktop, not in the home folder the README suggests. **Claude Code on the web cannot reach the Teensy**, whichever computer it is opened from; the tools run only where the USB is plugged in. First-time steps in `Code/pc/README.md` |
| Hakko FX-888DX + tips · solder wick · tip tinner · brass wool · fine tweezers · flush cutters · magnifier · helping hands · ~~calipers~~ · safety glasses · nitrile gloves · multimeter · bench PSU | — | `SAID` | **CORRECTED 2026-09-14 late: there are NO calipers.** Jacob, at the bench: "I don't have a caliper." This row's `SAID` was wrong. **Every procedure that says "put calipers on it" needs a route that does not use them** — see the standoff (no measurement needed, the fit is settled from Berard's board file) and the board-thickness check before the M2 screws |
| **60–70 °C oven or dehydrator** | **UNKNOWN — probably none** | never confirmed | Listed in `docs/PREAMP_SHOPPING_LIST.md` under "only if needed" and **never bought or confirmed.** **This is what gates the distilled-water rinse**: without a controlled bake, water under IC1 or the 1812s is a leakage path at the input node. Ask before planning any wash that ends in water |

---

## Known gaps

**Recorded here rather than guessed.** Also in `docs/OPEN_QUESTIONS.md`.

| Question | Why it matters |
|---|---|
| **Which other parts did JLCPCB leave off the preamp PCBA?** | Decides what has to be hand-fitted on the spare board before it can be used |
| **How was JLCPCB's C1/C2 polarity question answered?** | Would settle fault 1d from the order thread instead of needing the boards in hand |
| ~~**Do we own M2 screws, copper tape, heat shrink?**~~ **M2 screws and heat shrink ORDERED 2026-09-09.** **Copper tape is still unchecked** | The shield rebuild needs copper tape with conductive adhesive. Aluminium will not do — `docs/ENGINEERING_REFERENCE.md` §3 |
| ~~**Do we own low-temp Sn42/Bi58 solder paste?**~~ **MOOT — the piezo is built.** See below | Nothing to buy |
| **The piezo disc part number and diameter** | Ø20.500 mm seat vs a 25–27 mm disc in the BOM — see `docs/OPEN_QUESTIONS.md` |

---

## The piezo scanner — BUILT AND WORKING

**`SAID` 2026-09-09, Jacob: the piezo scanner is finished and it works.** Recorded as fact, not as a
question. **Nobody needs to ask about it again.**

| | |
|---|---|
| **Status** | **Built, complete and working.** `SAID`, Jacob, 2026-09-09 |
| **Sn42/Bi58 low-temp paste** | **Do not buy.** The joints are made |
| Quadrant-to-axis mapping | **Not recorded, and does not need to be.** The four wires are identical bare copper; the mapping falls out of the first image and is fixed in software. See `docs/OPEN_QUESTIONS.md` |

> **Disc-versus-seat is settled by construction.** `docs/FACTS.md` carried a conflict between the
> Ø20.500 mm seat in `PiezoPlate` and the 25-27 mm disc in `docs/BOM.md`. **A working scanner is
> built, so whatever went in fits.** The paper conflict is a documentation artefact, not a
> hardware problem, and no bench time should go on it.

## How to keep this file honest

- **Add a row when something arrives**, with the order number or "Jacob said so" and the date.
- **Never copy a row out of `docs/BOM.md`.** The BOM is a specification. This is a record of
  reality. The standoff is exactly where those two came apart.
- **A part number in an order confirmation beats every other source**, including this project's
  own documents.
