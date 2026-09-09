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
| **Keystone 11301** turret terminal | **0** | — | **We do not own this.** It is the part Berard names, and it is on order as of 2026-09-09 |
| **100 MΩ feedback resistor** | ≥1 | `SAID` | Value CONFIRMED. Not fitted to the board |
| **Tantalum 4.7 µF 35 V** | 1–2 | `SAID`, from a label | Spares beyond the two JLCPCB fitted |
| **40 AWG magnet wire** | — | `SAID` | For the tip lead |
| **Solder, Sn99.3/Ag0.3/Cu0.7 lead-free** | — | `SAID` | Correct for this work. **Do not buy more** |
| **Flux, non-rosin no-clean** | — | `SAID` | **Wrong type for this board.** Replacement on order |
| Hakko FX-888DX + tips · solder wick · tip tinner · brass wool · fine tweezers · flush cutters · magnifier · helping hands · calipers · safety glasses · nitrile gloves · multimeter · bench PSU | — | `SAID` | |

---

## Known gaps

**Recorded here rather than guessed.** Also in `docs/OPEN_QUESTIONS.md`.

| Question | Why it matters |
|---|---|
| **Which other parts did JLCPCB leave off the preamp PCBA?** | Decides what has to be hand-fitted on the spare board before it can be used |
| **How was JLCPCB's C1/C2 polarity question answered?** | Would settle fault 1d from the order thread instead of needing the boards in hand |
| **Do we own M2 screws, copper tape, heat shrink?** | Three items on the shopping list are "buy only if we do not have it" and nobody has checked |
| **The piezo disc part number and diameter** | Ø20.500 mm seat vs a 25–27 mm disc in the BOM — see `docs/OPEN_QUESTIONS.md` |

---

## How to keep this file honest

- **Add a row when something arrives**, with the order number or "Jacob said so" and the date.
- **Never copy a row out of `docs/BOM.md`.** The BOM is a specification. This is a record of
  reality. The standoff is exactly where those two came apart.
- **A part number in an order confirmation beats every other source**, including this project's
  own documents.
