# Preamp rebuild — what to buy

**2026-09-08.** The board is populated. Left to do: press in the standoff, air-mount the 100 MΩ,
wire the five JP1 holes and the tip lead, clean it, mount it. We have the standoff and the resistor.

## Buy

| Item | Used for | Why it has to be this |
|---|---|---|
| **Rosin flux**, gel syringe + a pen | Every joint we make: the five JP1 holes, the turret, the tip lead. Cored flux is spent on the first melt, and lead-free needs extra to wet | **It must say ROSIN** (R / RMA / RA). Rosin residue dissolves completely in IPA; non-rosin synthetic low-solids flux does not, and half-removed flux smears activator over a wider area. **“No-clean” on the label is not disqualifying if the flux is rosin-based** — the two describe different things, chemistry vs intended handling. **The flux we own is a non-rosin no-clean, which is why we need a different one.** **Chosen: Chip Quik RMA791 rosin paste flux, 50 g jar.** RMA rather than RA — the milder activator fails gracefully if a trace survives somewhere the brush could not reach. A jar is fine for through-holes, the turret and the tip lead; only awkward for surface-mount rework |
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

## Buy only if we do not already have it

| Item | Used for | Why |
|---|---|---|
| **M2 screws**, 6–8 mm, ×6 | Screwing the board to the two box standoffs | The box standoffs already line up with the board holes, so **no glue is needed** — and glue is the leading suspect for the current fault |
| **Copper tape**, conductive adhesive | Lining the preamp box as a shield | Solders, so the ground bond is a real joint. **Aluminium will not solder and its adhesive does not conduct** |
| **Heat shrink**, assorted | Insulating each JP1 wire joint and the bundle | Stops bare conductor touching its neighbour at 2.54 mm pitch. **None at the input node** — the adhesive lining outgases |

> **Solder: the lead-free Sn99.3/Ag0.3/Cu0.7 we own is fine. Do not buy solder.**
> It melts at 217–227 °C against 183 °C for leaded, so **run the iron at 340–360 °C**, not higher.
> The risk is not the alloy — it is that lead-free wets reluctantly, so people hold the iron on
> until it flows, and *that* lifts pads. Plenty of flux, 2–3 seconds per joint.
> **What we lose:** lead-free joints are dull even when perfect, so the sheen test does not work.
> Use the **continuity tester** for opens and shorts and a **gentle tug on each wire** for cold
> joints — a cold joint still conducts, so the meter alone will not catch it.

## Only if the C2 check fails

**4.7 µF 50 V X7R ceramic, 1206/1210, ×4.** Used to replace C2 if the polarity check shows it
reverse-biased. C2 is a tantalum whose anode sits on −15 V in the source design; a reverse-biased
tantalum leaks, heats and can fail short. **Ceramics are not polarized**, so the problem cannot come
back. A few pounds of insurance.

## Do not buy

**Non-rosin flux** (a "no-clean" that is not rosin-based) · bismuth/low-temperature solder ·
aluminium tape · solder of any kind · the op-amp, C1–C4, R1 (fitted) · a header for JP1 (wires go
straight into the holes) · PTFE wire (the only high-impedance run is the tip lead, and that is
40 AWG magnet wire we already have).

## Already have

FX-888DX and tips · solder wick · tip tinner · brass wool · fine tweezers · flush cutters ·
magnifier · helping hands · calipers · safety glasses · nitrile gloves · Keystone 11301 standoff ·
100 MΩ resistor · multimeter · bench PSU · 40 AWG magnet wire (`docs/BOM.md` §5, for the tip lead)

## Only if needed

**#44 drill (2.184 mm)** — only if the standoff will not press into the Ø2.108 mm hole. That is
exactly Keystone's specified hole size, and it still leaves 1.45 mm of board to the edge.
**A 60–70 °C oven or dehydrator** — drying the board after washing, to drive moisture out of the
FR-4. **Board only, never the printed box**: PETG softens near 80 °C.
