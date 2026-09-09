# Preamp rebuild — what to buy

**2026-09-08, revised 2026-09-09.** The board came **assembled (PCBA) from JLCPCB**, 2 off. Left to do: press in the standoff, air-mount the 100 MΩ,
wire the five JP1 holes and the tip lead, clean it, mount it. **We have the resistor. We do NOT
have a usable standoff** — see the standoff section below.

## Buy

| Item | Used for | Why it has to be this |
|---|---|---|
| **Rosin flux** — **see the flux section below before ordering. The chosen RMA791 is jar-only, and the syringe alternatives are not verifiable from here** | Every joint we make: the five JP1 holes, the turret, the tip lead. Cored flux is spent on the first melt, and lead-free needs extra to wet | **It must say ROSIN** (R / RMA / RA). Rosin residue dissolves completely in IPA; non-rosin synthetic low-solids flux does not, and half-removed flux smears activator over a wider area. **“No-clean” on the label is not disqualifying if the flux is rosin-based** — the two describe different things, chemistry vs intended handling. **The flux we own is a non-rosin no-clean, which is why we need a different one.** **Chosen: Chip Quik RMA791 rosin paste flux, 50 g jar.** RMA rather than RA — the milder activator fails gracefully if a trace survives somewhere the brush could not reach. A jar is fine for through-holes, the turret and the tip lead; only awkward for surface-mount rework |
| **Isopropyl alcohol, 99%** | Washing all flux off the board after soldering, before the input node is built | 91% is 9% water. That water carries ionic contamination and leaves it as a conducting film exactly where we cannot afford one |
| **Distilled water** | One final rinse after the IPA, then dry | IPA dissolves rosin but not ionic salts. Water takes those. Tap water leaves mineral deposits, which is the same problem again |
| **Soft brushes ×4** | Scrubbing flux off the board under IPA | Horsehair or ESD-safe nylon — stiff bristles scratch soldermask. **Four so one stays clean**: a brush that has scrubbed dirty flux spreads it around when reused |
| **Lint-free wipes** | Wiping the board down during and after cleaning | Paper towel sheds fibres. A fibre lying across the input node is both a leakage path and something that moves and makes noise |
| **Foam or polyester swabs** | Cleaning into corners and around the standoff | Cotton buds shed and hold moisture — the two things we are trying to remove |
| **Stranded silicone wire, 28–30 AWG** | The five JP1 holes, replacing the jumper wires | Not electrical — nothing on JP1 is high impedance. **Mechanical:** the preamp sits on the scan head, and stiff wire carries building vibration into the instrument. Silicone stays limp and will not shrink back when soldered |

> **Why we clean even a flux sold as "no-clean".** "No-clean" means the residue is benign enough to
> leave on a **normal** board. The pass mark is **IPC J-STD-004B's surface insulation resistance
> requirement: 100 MΩ minimum.** Our feedback resistor is **100 MΩ** — so residue that *passes* the
> standard is only guaranteed to be about as resistive as the thing we measure through. 100 MΩ from
> the input node to a ±15 V rail injects **150 nA**, more than the instrument's whole measurable
> range and larger than the offset we are already chasing. **On this board there is no flux you can
> leave on.** So: clean whatever we use, and buy the one that comes off completely — rosin.

## The flux and its applicator — SETTLED AND BOUGHT 2026-09-09

**Bought, arriving 2026-09-11: the Chip Quik RMA791 50 g jar, plus a manual syringe dispenser with
blunt tips.** That is the right answer and it closes the question.

**Why it had to be done in two parts.** RMA791 is **jar-only** — Chip Quik's whole paste-flux family
(RA691, RMA771, RMA791, RA891) is 2 oz jars, with no syringe SKU. This list's own item line asked for
a "gel syringe" while its chosen product was a jar; the two had disagreed unnoticed.

**Do not substitute a different flux to get a syringe.** Chip Quik's syringe products are a separate
"tack flux" line whose J-STD-004 codes and vendor descriptions **contradict each other**: SMD491 and
NC191 are classified `ROL0` (`RO` = rosin) yet titled "**Synthetic** No-Clean" by their own vendors;
RMA591NL is `ROM1` and called "RMA **synthetic** paste"; SMD291 is **`REL0`** — `RE` is resin, **not
rosin at all**. **That is exactly how the wrong no-clean flux we already own got bought.** No primary
datasheet could be opened to settle it — chipquik.com, mouser.com and amazon.com are all blocked from
the remote session that checked.

**Loading the syringe:** pull the plunger right out, spoon paste into the open back of the barrel,
refit the plunger. Paste will not draw up through a tip. **Use the widest blunt tip supplied**, or
none — rosin paste is stiff and a fine-gauge needle will simply not pass it.

**Why a syringe is worth it here, beyond convenience.** A jar that a brush is repeatedly dipped into
becomes a **contamination reservoir** — skin oils, board debris, spent flux, all returned to the
supply. On a node where a human within a metre injects tens of nA, that matters. A syringe dispenses
a fresh bead and the bulk is never touched. **If the jar is used directly, never dip twice** — scoop
onto a clean surface with a clean tool.

> **The flux pen is still not resolved.** This list originally asked for "gel syringe **and** a pen".
> **Most flux pens are low-solids no-clean — the wrong chemistry.** None has been verified. Do not
> buy one on the assumption it is fine.

> ### The flux is only half of it. THE CLEANING SUPPLIES ARE NOT BOUGHT.
>
> RMA791 is rosin, so it comes off — **but only if something takes it off.** As of 2026-09-09 none of
> **99% IPA, distilled water, the four soft brushes, lint-free wipes or foam swabs** has been
> ordered. **Rosin left on this board is a leakage path at the exact node we are chasing.**
> **Do not solder the preamp until the cleaning kit is in the room.**

## Buy only if we do not already have it

| Item | Used for | Why |
|---|---|---|
| ~~**M2 screws**~~ **BOUGHT 2026-09-09** — an 800 pc M2x4-M2x20 assortment | Screwing the board to the two box standoffs | **Use the M2x6. NOT the M2x8.** The pilot is **5.00 mm deep, blind** and the boss is 4.00 mm tall (measured from the mesh, `docs/FACTS.md`). Through a 1.6 mm board an M2x6 engages 4.4 mm of a 5.0 mm hole; **an M2x8 needs 6.4 mm and will bottom out**, cracking the boss or jacking the board off the standoff. **Put calipers on the board first** — 1.6 mm is JLCPCB's default, not a measured figure. **Drive slowly and stop at snug**; the thread is plastic |
| **Copper tape**, conductive adhesive — **STILL NOT CHECKED, and now the only unbought item in this table** | Lining the preamp box as a shield | Solders, so the ground bond is a real joint. **Aluminium will not solder and its adhesive does not conduct** |
| ~~**Heat shrink**, assorted~~ **BOUGHT 2026-09-09** | Insulating each JP1 wire joint and the bundle | Stops bare conductor touching its neighbour at 2.54 mm pitch. **None at the input node** — the adhesive lining outgases. **VERIFY on arrival whether the kit is adhesive-lined (dual-wall)**; plain polyolefin is what is wanted |

> **Solder: the lead-free Sn99.3/Ag0.3/Cu0.7 we own is fine. Do not buy solder.**
> It melts at 217–227 °C against 183 °C for leaded, so **run the iron at 340–360 °C**, not higher.
> The risk is not the alloy — it is that lead-free wets reluctantly, so people hold the iron on
> until it flows, and *that* lifts pads. Plenty of flux, 2–3 seconds per joint.
> **What we lose:** lead-free joints are dull even when perfect, so the sheen test does not work.
> Use the **continuity tester** for opens and shorts and a **gentle tug on each wire** for cold
> joints — a cold joint still conducts, so the meter alone will not catch it.

## Buy — the standoff. Corrected 2026-09-09.

**Keystone 11301, ×4.** DigiKey part **36-11301-ND**, about $2.81 each.

**We do not own this part, despite `docs/BOM.md` having said "CONFIRMED" and this list having said
"already have".** Both were wrong. What we own is the **11311** (DigiKey order 100750867, 2 off,
2026-08-02), which needs a Ø3.45 mm mounting hole against our board's Ø2.108 mm — **1.34 mm
undersize, and confirmed at the bench that it will not go in.**

**Do not open the hole to fit the 11311.** The hole is 2.540 mm from the board edge; at Ø3.45 mm
only **0.815 mm** of material would remain, under the one component the instrument's sensitivity
depends on.

> **VERIFY before pressing.** The 11301's own mounting-hole spec is disputed — `docs/FACTS.md`
> records Ø2.184 mm, but that figure is also listed as the part's turret-head diameter and the two
> cannot both be right. Every distributor and manufacturer site was unreachable on 2026-09-09.
> **Put calipers on the part and on the board hole when it arrives.**

## Buy — the C2 replacement ceramics

**4.7 µF 50 V X7R ceramic, 1812 package, ×4.** KEMET `C1812C475K5RACTU` or TDK
`C4532X7R1H475K200KB`. Put these on the same DigiKey order as the standoff so shipping is paid once.

**1812, not 1206/1210 — corrected 2026-09-09 from the gerber.** The C2 pads are **2.750 × 1.800 mm
at 5.250 mm centres**, leaving a **2.500 mm gap**. A 1206 or 1210 is 3.2 mm long and would land only
**0.35 mm on each pad**. An 1812 is 4.5 mm and lands a full 1 mm.

**Why buy rather than just rotating the tantalum.** Rotating works and costs nothing, but if C2 is
reversed it has been held at 15 V reverse for weeks and its dielectric is degraded. **Ceramics are
not polarized**, so once fitted the problem cannot recur on either board.

> **C1 is correctly connected. Do not rotate or replace C1.** Only C2 is in question.

## Do not buy

**Non-rosin flux** (a "no-clean" that is not rosin-based) · **bismuth/low-temperature solder — for THIS board.** It is brittle, and this list is the preamp only. **The piezo disc is the opposite case and does need it** — see `docs/BOM.md` §5 ·
aluminium tape · **solder wire of any kind** (we own a lead-free that is fine) · the op-amp, C1–C4, R1 (fitted) · a header for JP1 (wires go
straight into the holes) · PTFE wire (the only high-impedance run is the tip lead, and that is
40 AWG magnet wire we already have).

## Already have

FX-888DX and tips · solder wick · tip tinner · brass wool · fine tweezers · flush cutters ·
magnifier · helping hands · calipers · safety glasses · nitrile gloves ·
100 MΩ resistor · multimeter · bench PSU · 40 AWG magnet wire (`docs/BOM.md` §5, for the tip lead)

> **The Keystone 11301 was listed here in error until 2026-09-09.** We own the **11311**, which
> does not fit. See the standoff section above and [`docs/INVENTORY.md`](INVENTORY.md).
> **Check this list against `docs/INVENTORY.md`, not against `docs/BOM.md`** — the BOM is a
> specification and says what was chosen, not what arrived.

## Only if needed

**#44 drill (2.184 mm)** — only if the 11301 will not press into the Ø2.108 mm hole. It leaves
1.45 mm of board to the edge, which is safe. **It was recorded as exactly Keystone's specified hole
size; that is now VERIFY** — measure the part first, and only open the hole if the part demands it.
**A 60–70 °C oven or dehydrator** — drying the board after washing, to drive moisture out of the
FR-4. **Board only, never the printed box**: PETG softens near 80 °C.
