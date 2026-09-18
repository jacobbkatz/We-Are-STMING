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
| **Preamp PCB, assembled (PCBA)** | **2** | `SAID` 2026-09-09, Jacob | **JLCPCB PCBA, not bare.** One is built into the current preamp box; one is the spare. **WHERE THE FITTED ONE IS: the little copper-taped box at the CENTRE of the scanning module**, — `SAID` 2026-09-18, Jacob, identifying `Images/ours/2026-09-16_scan_module_top_down.jpg`: *"top down veiw of scanning module on suspension the preamp is the little copper box in the middle"*. **That photograph is the only picture in the repository that shows where the amplifier physically sits relative to the head** |
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
| **100 MΩ feedback resistor** | ≥1 | `SAID` | Value CONFIRMED. Not fitted to the board. **One is now the rebuilt preamp's feedback resistor (2026-09-15). ~~Whether a SPARE of 100 MΩ or more exists is UNKNOWN~~** **A spare exists**: `SAID` 2026-09-16, Jacob, "Resistor is 100Mega ohms, same as the preamp". **In use as the dummy junction**, clipped between the tip holder and the bias jumper cable |
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
| **Tip holder, improvised** | 1, fitted | `SAID` 2026-09-16, Jacob | **A metal shaft stuck to the underside of the piezo, insulated from it, with a socket soldered to the shaft that tips insert into.** **Adhesive not stated.** Its offset from the disc centre is **unmeasured**, and it matters for the motor direction (`docs/OPEN_QUESTIONS.md`). **Tips vary in length.** The tip lead is soldered to it; open to the piezo brass on a meter, 2026-09-16. **THE TIP IS TUNGSTEN WIRE** — `SAID` 2026-09-18, Jacob. **The standard STM tip material, and the right choice.** **Paramagnetic and very weakly so** (χ ≈ +7.8e-5), so **the sample-plate magnets cannot snap it in**: the force reaches at most about 15 µN, and because the magnets are Ø4.2 mm their field varies over millimetres while the approach happens over microns, so the force is constant across the gap rather than rising. **No runaway.** Tungsten is also stiff, E ≈ 400 GPa, about twice steel, which makes it a far less likely snapper than the 100 nm gold leaf. **STILL NOT RECORDED: what the "metal stake" the holder is soldered to is made of.** The magnet test still applies to that. Added 2026-09-18. The tip is described only as a blunt, bent placeholder and the holder as a metal shaft, a "metal stake" superglued to the piezo (`SAID` 2026-09-18 bench). **Neither material is written down.** **The sample plate carries four disc magnets a millimetre or two behind the gold** (`docs/BOM.md`, `CAD/prints/README.md`), so **if either is ferromagnetic there is a DC pull on the tip that rises steeply as the gap closes — a second snap mechanism, independent of the loose leaf.** **Ten-second test: hold a spare magnet near the tip and the holder.** Tungsten and platinum-iridium, the two standard STM tip materials, are effectively non-magnetic; steel is not. See `STATUS.md`. **A TIP IS NOW FITTED** (`SAID`, later 2026-09-16): sticks out **about 1.8 cm from the plate face**, positioned **about halfway along the pair of side-by-side screws, about 2 cm**; **"horribly probably extremly blunt and bent downwards towrds the baseplate"** — a placeholder until tip-making is improved. **Its distance from the line joining those two screws — the 1 mm that decides the motor direction — is not measured.** **Photos are now IN THE REPOSITORY**: `Images/ours/2026-09-16_tip_protrusion_measurement_1.jpg` and `_2.jpg` (from Jacob's phone via Drive, 2026-09-18; originally `IMG_8586` and `IMG_8588`). **`SAID` 2026-09-18, Jacob, confirming what they show:** *"Yes your correct"* — the 1.8 cm is measured **from the plate face**, with the tape held **halfway along the side-by-side screws**. **That is the provenance for the 1.8 cm, and it is a tape-measure reading against a hand-held tape, so it is good to a millimetre or so and no better.** **Jacob then adjusted the side-by-side pair — "I screwed in the pair of screws more so they are now beyond the tip" — so their ball ends stand beyond the tip** and the sample plate clears it. **Whether the dummy junction resistor was removed first was not stated**. **REBUILT 2026-09-18 — `SAID`, Jacob: *"fixed the tip holder"*. WHAT WAS DONE IS NOT STATED AND IS THE OPEN QUESTION:** whether any adhesive was used and which, whether the tip is now removable without rebuilding, and where the tip now sits relative to the line through the two ball ends. **MEASURED 2026-09-18, `SAID` Jacob, and it is a RANGE not a value: d is BETWEEN 0 AND 1 mm** — *"its between 1mm and 0mm its really hard to measure"*. **An earlier figure of 5 mm was stated and then retracted by Jacob within minutes as a mis-measurement; it was never written into any document.** That range puts the lever ratio at **40 or more** — the design value is its upper bound — but it does not settle the tunnelling question, which turns on whether d is above or below about **0.13 mm**. See `docs/bench_2026-09-17_review.html` section 03. **`SAID` 2026-09-18: the new tip holder is CONTINUOUS to the standoff**, so the rebuild did not break the input signal path. **The OTHER check, `STATUS.md` safety rule 7 — tip holder to the brass piezo electrode must read OPEN — is still outstanding.** **Two consequences until those are answered: (1) `STATUS.md` safety rule 7 — the tip holder must meter OPEN to the brass piezo electrode — has to be re-checked, because that check passed on 2026-09-16 against the OLD holder and a rebuild is exactly what can bridge it; (2) the tip holder is part of the preamp input node, and the piezo is already a cyanoacrylate site, so if CA was used here it is a third one at the most sensitive point in the instrument.** **UPDATED 2026-09-18 bench, `SAID` Jacob** (`sessions/2026-09-18-bench.md` §3.1): *"The holder has always been attached via solder to a metal stake which is superglued to the peizo this was done before superglue issues were made apparnet. tip sits roughly in the middle"*. **So the attachment method is the same as before the rebuild**, and **the tip is roughly central on the disc** — which replaces the off-centre reading taken from photographs in `sessions/2026-09-18.md` §3.5. **Safety rule 7 re-checked against the rebuilt holder: OPEN** (`SAID`). **d: "1ish mm"** (`SAID`), and no means in the room to measure it or the disc offset better. **The rebuild left the tip about 2.2 mm further from the sample**: the hand-set needed about 7 turns of the side-by-side screws before the beep (`SAID`), at 0.3175 mm per turn. |
| **Alligator clips, clip leads, mini-grabbers** | ~~0~~ **some, bought 2026-09-16** | `SAID` 2026-09-16, Jacob: "I dont have aligator clips"; **then, after a trip to Home Depot: "Im back with the clips"** — type, size and count not stated | **None in the room.** **Blocks the dummy junction test**, which needs a resistor held temporarily between the sample holder, or the black `BIAS` wire, and the tip holder. Small hook-type grabbers put less force on the tip holder and piezo than spring alligator clips |
| **Solder, Sn99.3/Ag0.3/Cu0.7 lead-free** | — | `SAID` | Correct for this work. **Do not buy more** |
| **Low-temp solder paste, Sn42/Bi58** | **UNKNOWN** | — | **Nobody has said whether we own any.** Needed for the piezo quadrant wires and nothing else. `docs/BOM.md` §5 specifies it; a specification is not an inventory. **Ask before ordering** |
| **Flux, non-rosin no-clean** | — | `SAID` | **Wrong type for this board.** Superseded by the RMA791 below. **Do not use it on the preamp** |
| **Chip Quik RMA791 rosin paste flux, 50 g jar** | 1 | `ORDER` Amazon, **arriving 2026-09-11** | **The correct flux.** ROL0 — rosin, low activity, halide-free. **Must still be cleaned off** — see `docs/PREAMP_SHOPPING_LIST.md` |
| **Manual flux/glue syringe dispenser** + 10 cc syringe + blunt tips | 1 | `ORDER` Amazon, **arriving 2026-09-11** | Load it from the RMA791 jar. **Solves the jar-vs-syringe question** |
| **M2 self-tapping pan-head screws, 800 pc assortment** | M2x4 to M2x20 | `ORDER` Amazon, **arriving 2026-09-11** | **Use the M2x6.** M2x8 bottoms out in the box pilot — see `docs/FACTS.md` |
| **Heat shrink tubing, assorted kit** | — | `ORDER` Amazon, **arriving 2026-09-11** | **VERIFY whether it is adhesive-lined (dual-wall).** Either way, **none at the input node** — the adhesive lining outgases |
| **Computers that run the project** | 2 | `SAID` 2026-09-16, Jacob: "this is the first time I've run Claude on this computer, we usually use Nuh's" | **Nuh's machine has run the instrument and every bench session so far.** **Jacob's Windows machine was new to the project on 2026-09-16**: no repository, Git or Python present at first. **Confirmed working later on 2026-09-16** (`BENCH`, read off the machine by Claude Code desktop): Git 2.55.0 in `C:\stm\Git`; Python 3.13.15, **reached with `py` only**, because `python` and `python3` are Microsoft Store placeholders and Python's own folder is not on the PATH; pyserial 3.5; the no-Teensy dry run passed. **`bash` is not on its PATH.** **PlatformIO Core 6.2.0 installed there 2026-09-16** with `py -m pip install platformio`, and the firmware builds on it. **Plain `git` is not found in the Claude app's own terminal panel either**; use Git's full path there, or a normal Windows terminal, until the app is restarted. The repository is in a folder on Jacob's OneDrive desktop, not in the home folder the README suggests. **Claude Code on the web cannot reach the Teensy**, whichever computer it is opened from; the tools run only where the USB is plugged in. First-time steps in `Code/pc/README.md` |
| Hakko FX-888DX + tips · solder wick · tip tinner · brass wool · fine tweezers · flush cutters · magnifier · helping hands · ~~calipers~~ · safety glasses · nitrile gloves · multimeter · bench PSU | — | `SAID` | **CORRECTED 2026-09-14 late: there are NO calipers.** Jacob, at the bench: "I don't have a caliper." This row's `SAID` was wrong. **Every procedure that says "put calipers on it" needs a route that does not use them** — see the standoff (no measurement needed, the fit is settled from Berard's board file) and the board-thickness check before the M2 screws |
| **60–70 °C oven or dehydrator** | **UNKNOWN — probably none** | never confirmed | Listed in `docs/PREAMP_SHOPPING_LIST.md` under "only if needed" and **never bought or confirmed.** **This is what gates the distilled-water rinse**: without a controlled bake, water under IC1 or the 1812s is a leakage path at the input node. Ask before planning any wash that ends in water |

---

### Piezo discs — added 2026-09-17

| What | Qty | How we know | Notes |
|---|---|---|---|
| **Piezo disc, Jessinie `91410_30_JE`** | — | `SAID` 2026-09-17, Jacob: *"we are using a difference peizo than both dan bernard and mechpanda, our peizos are made by jessinie sku being 91410_30_JE"* | **This is the scanner disc actually fitted.** **It is NOT Berard's disc**, so **`docs/FACTS.md`'s 34 nm/V and the 0.0104 nm per DAC count derived from it do not describe our scanner** — they were always marked INFER. **Measured 2026-09-17 against the motor, which is the only mechanical ruler we have: about 250 Z DAC counts per motor step**, and one motor step is 155 nm of screw, or 3.9 nm at the tip at the assumed 40:1 lever. **That is roughly 0.016 nm per Z count and a full Z range near 1 um** — the same order as the inherited figure, **not** the 50x smaller value estimated earlier the same evening from the current-versus-Z slope, which is retracted. **The lever ratio is itself unmeasured, so this scales with it.** See `sessions/2026-09-17-bench.md`. **Datasheet not yet obtained** **THE 250 COUNTS PER MOTOR STEP IS SUSPECT — 2026-09-18 bench.** It came from a staircase run in the retract direction straight after a reversal, inside the 100-250 steps of slack measured the same night. **On 2026-09-18 a single step moved the onset 14,000-29,000 Z counts when it moved it at all, and runs of 20-40 steps moved it not at all** — the stage sticks. **So the nm-per-count scale of this disc is UNMEASURED**, and neither night's figure is a calibration. `sessions/2026-09-18-bench.md` §5. |

---

### Sample material — added 2026-09-17

| What | Qty | How we know | Notes |
|---|---|---|---|
| **Gold leaf** | **4 squares, about 1 inch each** | `SAID` 2026-09-17, Jacob: *"I have 4 inch by inch squares left pretty much"* | ~~**Whether it is real gold or imitation (brass "Dutch metal") is UNKNOWN and has never been tested.**~~ **REAL GOLD — flame test, `SAID` 2026-09-17, Jacob: *"Flame test done its real gold"*.** It mattered: gold does not oxidise, brass grows an insulating tarnish within days. **Whether it is loose leaf or transfer (backed) leaf is still UNKNOWN**. Minus one scrap for the test |

> **Four squares is not four attempts.** A 1-inch square is 25 mm, so it cuts into 5 × 5 = **25
> pieces of 5 mm**, and the scanner's whole range is **0.5 µm** — a 5 mm piece is ten thousand times
> wider than anything the tip ever sees. **The budget is roughly 100 usable pieces.**

| **Copper tape** | — | `BENCH` — it is visibly on the sample plate, the scan head and the preamp box in the 2026-09-16 photographs | ~~**Whether its adhesive is conductive is STILL UNKNOWN**, open since 2026-09-09 and now blocking.~~ **THE ADHESIVE CONDUCTS — `SAID` 2026-09-17, Jacob: *"the glue is conductive"*.** Read as the `docs/gold_leaf_procedure.html` Part 1 overlap test beeping; the method was not stated. **Checked on a scrap of the tape on the bench, not on the tape already fitted to the preamp box or scan head**, which may be from the same roll but that is not confirmed |
| **Sample plate, as rebuilt 2026-09-17** | 1 | `SAID` 2026-09-17, Jacob, with a photo in the conversation — **and a photograph dated the same day is now in the repository as `Images/ours/2026-09-17_sample_plate_rebuilt.jpg`**, showing aluminium tape over the face, a square window cut in it and gold inside the window, which matches this entry point for point. **NOT CONFIRMED that it is the same plate** — that is a reading of the frame, not something Jacob has said, and one word settles it | **Face covered in ALUMINIUM tape** (`SAID`: *"the silver tape you see is aluminium tape"*), with a square window cut in it showing **copper tape**, and **fresh gold leaf** on that copper. Copper tape also along one edge. The orange sample-plate wire enters under the aluminium at the top edge. **Aluminium tape's adhesive usually does not conduct** (`docs/ENGINEERING_REFERENCE.md` §3) **and its surface oxide is an insulator**, so **a tip landing on the aluminium would most likely read nothing even in contact** — the gold must be what is in front of the tip. **Whether the aluminium is joined to the bias wire, to ground, or to nothing is UNKNOWN.** Gold to orange wire: not yet reported. ~~**Where the tip actually lands is UNCONFIRMED** — `SAID` 2026-09-17, Jacob, at the end of the session: *"I think your prooabbly over copper"*.~~ **A FIRST GOLD ATTEMPT ON 2026-09-16 WAS MADE AND REMOVED, and was never reported at the time** — `SAID` 2026-09-18, Jacob, identifying photo `IMG_8593` (16 Sep, 20:33): *"that is the first attempt on 16 I didnt tell you about I removed it."* **So the gold history is: attempt 1 on 2026-09-16, removed; the 2026-09-17 patch on copper tape, which held; the 2026-09-18 whole-plate sheet, which is loose.** **SUPERSEDED 2026-09-18: a second sheet of gold leaf was laid so that the ENTIRE sample plate face is covered** — `SAID`, Jacob: *"Just added anouther sheet of gold so the enitre sample plate is covered"*. **The tip now lands on gold wherever it lands**, which removes the copper-oxide confound that 2026-09-17 could not resolve. **NOT YET CONFIRMED and worth one meter check: that the new leaf is electrically continuous to the orange bias wire.** The old plate had the gold on copper tape which the wire reached; a fresh sheet laid over aluminium tape may not be joined to anything, and aluminium tape's adhesive usually does not conduct. **If the gold is not on the bias, no tunnelling current can exist** **CONFIRMED 2026-09-18 bench: the gold beeps to the orange bias wire** (`SAID`), and the bias flip at a real contact passed the same night. **BUT THE SHEET IS NOT STUCK DOWN — `SAID` 2026-09-18, after that session:** *"the seccond session today the gold wasnt as stuck on as the first with whole gold foil on it was moveing a bit if i blew on it versus it didnt the first session"*. **The 2026-09-17 patch, gold on copper tape with the adhesive under it, did NOT move when blown on. The whole-plate sheet DOES.** **This is now the leading explanation for everything erratic in `sessions/2026-09-18-bench.md`** — see `STATUS.md`. **Leaf is about 100 nm thick and weighs 0.019 Pa. The bias pulls on it at 1.1 Pa across a 1 um gap and 111 Pa at 100 nm, rising as 1/gap^2**, so an unadhered sheet lifts to meet the tip and the lift accelerates. **The blow test calibrates it: a gentle breath is 0.6 to 15 Pa, the same order as the electrostatic pull at a micron.** **`docs/gold_leaf_procedure.html` requires burnishing** — press and smooth with something soft in small circles until it goes from dull and loose-looking to bright and flat. **Whether the second sheet was burnished, and what is under it, is NOT RECORDED and should be.** |


---

### Scan head suspension — added 2026-09-18 bench

| What | Qty | How we know | Notes |
|---|---|---|---|
| **Suspension springs** | 3, ~300 mm (BOM) | `SAID` 2026-09-18, Jacob: droop *"maybe 2mm"* (`sessions/2026-09-18.md`); then, 2026-09-18 bench: *"these springs are more strechy than I thought adding more wieght could help I think"* | **Rate in N/mm still UNKNOWN.** The 2 mm droop and ~11 Hz resonance in `docs/FACTS.md` stand until re-measured. If the springs have initial tension, the droop from slack understates their softness and added weight goes straight into stretch — **not verified** |
| **Sample-pocket disc magnets** | **4** | `SAID` 2026-09-18, Jacob: *"like mechpandas design we have magnets below the copper on the sample bank becuase his hopg carbon sample came on a magnet plate so we intended to do the same"*; **count and pockets independently in `docs/BOM.md` and `CAD/prints/README.md`** — four blind pockets Ø4.200 x 6 mm deep, 4 along Y at X centre of `SamplePlate` | **Size, grade and field UNKNOWN.** **The intent was to hold a magnetic sample puck, as Mech Panda's HOPG came on. We do not use a puck — the gold goes straight onto the plate — so they serve no purpose now, but they are still in the plate, a millimetre or two behind the gold.** **They CANNOT move the gold** (diamagnetic, at most 7% of the leaf's own weight at 0.5 T and 1,000 T/m) **and CANNOT make the noise** (0.0063 pA against a 1 nA signal). **They MIGHT pull on a ferromagnetic tip or holder, and might magnetically stick the plate to its three steel ball screws** — both untested, both stronger since the plate came ~2.2 mm closer on 2026-09-18. `STATUS.md` |
| **Eddy-current damping magnets** | UNKNOWN | `SAID` 2026-09-18 bench, Jacob: *"I cant add weight with the current set up becuase of the damening magnets right below the hanging platform"* | **Were not in this file at all.** Number, type and the gap to the platform are UNKNOWN. **Any change that lowers the platform must lower the magnets by the same amount**, or the gap closes and the platform lands on them. **Measure the gap before adding weight** |
---

## Known gaps

**Recorded here rather than guessed.** Also in `docs/OPEN_QUESTIONS.md`.

| Question | Why it matters |
|---|---|
| **Which other parts did JLCPCB leave off the preamp PCBA?** | Decides what has to be hand-fitted on the spare board before it can be used |
| **How was JLCPCB's C1/C2 polarity question answered?** | Would settle fault 1d from the order thread instead of needing the boards in hand |
| ~~**Do we own M2 screws, copper tape, heat shrink?**~~ **M2 screws and heat shrink ORDERED 2026-09-09.** **Copper tape is still unchecked** **Copper tape: owned, and its adhesive conducts** (`SAID` 2026-09-17, see the sample material table above) | The shield rebuild needs copper tape with conductive adhesive. Aluminium will not do — `docs/ENGINEERING_REFERENCE.md` §3 |
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
