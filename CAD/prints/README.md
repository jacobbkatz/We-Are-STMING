# Printable parts

Every part you need to print, extracted from the distribution zip so **GitHub renders the STLs in
your browser** — click any file to spin it around before you slice it.

**Print in PETG-CF or PA-CF. Not PLA.** PLA creeps under sustained load and moves with
temperature, and that shows up directly as drift in your images. Budget roughly 500–800 g.

`print-plates/` holds the 3MF plates we actually printed from, if your slicer takes them.

---

> **These parts have all been printed and assembled together before** — reported by Jacob,
> 2026-09-06. So the fits below are not just nominal dimensions; the stack-up is known to work in
> practice. **Reported, not re-measured on an assembled unit.**

## The enclosures, measured from the STLs

Bounding boxes read directly off the mesh files. **There are two shielded enclosures and they are
very different sizes** — this table exists so nobody has to ask again.

| Part | X × Y × Z (mm) | What it actually is |
|---|---|---|
| **`6_shield_cover`** | **142.00 × 128.00 × 112.40** | **The shield over the WHOLE scanning module.** Drops over the entire scan head |
| `box_mount` | 142.00 × 128.00 × 5.00 | **Same footprint as the shield cover** — the frame the cover sits on. Opening 131 × 101 |
| `5_intermediate_baseplate` | 130.00 × 100.00 × 5.00 | Fits the 131 × 101 opening above |
| **`1_preamp_box_base`** | **34.83 × 29.43 × 20.80** | **The small box holding the PREAMP BOARD only.** The board is 20.6 × 15.2 mm |
| `1_preamp_box_lid` | 34.83 × 29.43 × 3.60 | its lid |
| `2_controller_box_base` | 129.18 × 113.88 × 39.80 | controller PCB |
| `3_teensy_protoboard_box_base` | 89.80 × 109.80 × 41.80 | Teensy and protoboard |
| `4_scanhead_box_base` | 130.00 × 134.00 × 88.20 | the rejected alternative, see below |

**Both shielded enclosures get the same treatment — copper tape, grounded at one point — which is
exactly why they get confused in conversation. They are not the same object:**

- **Scan head shield cover**, 142 × 128 × 112 mm, over the whole module.
- **Preamp box**, 35 × 29 × 21 mm, around one small PCB.

### The scan head parts it has to cover

| Part | X × Y × Z (mm) |
|---|---|
| `BasePlate` | 100.00 × 70.00 × 10.00 |
| `PiezoPlate` | 55.00 × 70.00 × 15.00 |
| `SamplePlate` | 12.00 × 70.00 × 49.00 |
| `MotorSupport` | 10.00 × 52.33 × 30.00 |
| `ThreadAdaptor` | 21.91 × 22.00 × 17.00 |

Stacked, the tallest column is roughly 59 mm against the cover's 112 mm of height. It fits with
room to spare.

### Why `4_scanhead_box` cannot be used instead

`docs/START_HERE_gotchas.md` says its corner ears are **142.8 mm** wide and so it will not fit
inside the shield cover. The measurements confirm it exactly: the shield cover's outside is
**142.00 mm**. It misses by 0.8 mm.

## Choose one scan head enclosure

`4_scanhead_box_*` and `6_shield_cover` do the same job different ways. **They are alternatives,
not a set.**

| | |
|---|---|
| **`6_shield_cover.stl`** | **Use this one.** Matches the original build: the head sits open on its baseplate and the shield drops over the whole assembly. **Wrap it in copper tape — not aluminium — solder the seams and ground it at one point.** |
| `4_scanhead_box_base/_lid.stl` | An earlier enclosed-box approach, kept for reference only. Its corner ears are 142.8 mm wide, so it will not fit inside the shield cover anyway |

> **Copper tape only. Not aluminium, and never both.** Aluminium cannot be soldered, its adhesive
> usually does not conduct so the overlaps stay open, and against copper it forms a galvanic cell.
> The preamp box was wrapped in both, and on 2026-09-06 it metered as discontinuous and only
> partly grounded. **Solder the seams, bond to ground at ONE point — not several, which makes a
> ground loop — then meter every corner and every seam.** An ungrounded or broken shield can be
> worse than no shield at all. Full rule: `docs/ENGINEERING_REFERENCE.md` §3.

---

## Names that do not mean what they look like

| File | What it actually is |
|---|---|
| `box_mount.stl` | **Not a mount for a box.** It is the rectangular frame the scan head sits in. Opening is 131.00 × 101.00 mm, 5 mm thick |
| `new_body.stl`, `new_topframe.stl` | The **bottom and top of the isolation tower**, joined by the three M8 threaded rods. The `new_` prefix is left over from the original author's revisions and means nothing |
| `Platform.stl` | **A circular disc, 200 mm diameter × 6 mm.** Its bounding box reads 200 × 200 so it looks square in any file listing |
| `1_` through `6_` prefixes | Just labels. **Not an assembly order**, and 4 and 6 are alternatives to each other |

**The `BasePlate` hole grid is not centred.** It is a 3×3 grid of M3 holes sitting **7.5 mm off
centre in X**. Offsets from the part centre are X = −37.5, −7.5, +22.5 and Y = −27, 0, +27. Assume
it is centred, drill a mating part, and none of the nine holes will line up.

---

## Fastener sizes, measured from the meshes

**Measured 2026-09-06 with `Code/pc/stl_features.py`.** `docs/BOM.md` listed "plate-to-plate and
motor-mount screw sizes" under *what we still don't know*. They are now measured.

How to trust these numbers: an STL's *vertices* sit exactly on the surface the CAD tool exported,
and the script fits a least-squares circle to each cylindrical wall it finds. Every number below
came back with a fit error of 0.0001 mm or better, and they are round numbers -- 3.200, 2.500,
1.600. That is what a real design dimension looks like. **The script prints a fit error column;
anything above about 0.01 mm means two features got measured as one, and must not be quoted as a
size.**

### The rule the whole build follows

**Every printed box is screwed together the same way: the lid has a clearance hole, and the base
has a narrower pillar that the screw cuts its own thread into.** Nothing is tapped in advance and
there are no nuts inside the boxes.

| | Lid hole (clearance) | Base pillar (screw self-taps) | Screw |
|---|---|---|---|
| Preamp box | **Ø2.300** | **Ø1.600** | **M2** |
| Controller box | **Ø3.400** | (posts not resolved) | M3 |
| Teensy / protoboard box | **Ø3.400** | **Ø2.500** | M3 |
| `4_scanhead_box` (unused) | Ø3.400 | Ø2.500 | M3 |

**This is the single most useful thing on this page for assembly day.** Ø1.6 and Ø2.5 are the
*tap* sizes for M2 and M3. Drive those screws **slowly, and stop at snug** -- there is no metal
thread to bottom out against, so if you keep going you strip the printed pillar and the lid no
longer clamps down onto its shield. And **do not drill a pillar out** to make a screw "fit"; then
nothing holds the lid at all.

### Plate to plate

| Part | Feature | Measured | Reading |
|---|---|---|---|
| **`BasePlate`** | 9 holes | **Ø3.200**, Z 4–10 | **M3 clearance** |
| **`BasePlate`** | same 9, coaxial | **Ø7.000 × 4.0 mm deep**, Z 0–4 | Counterbore for the head, on the Z = 0 face |
| **`BasePlate`** | grid | **30.0 mm in X, 27.0 mm in Y** | offsets −37.5, −7.5, +22.5 and −27, 0, +27 |
| **`5_intermediate_baseplate`** | 9 holes | **Ø2.500** | **The mating half.** Same grid, exactly. M3 self-taps into these |
| **`5_intermediate_baseplate`** | 4 holes at (±51.96, ±30) | **Ø3.400** through, **Ø6.500** counterbore | M3 clearance, to the frame below |
| **`box_mount`** | 2 holes | **Ø3.300** | M3 clearance, on the centreline, **120 mm apart** |
| **`MotorSupport`** | 3 holes, full 30 mm height | **Ø3.400** | **M3 clearance.** 21.2 mm pitch on the centreline |
| **`PiezoPlate`** | 4 bores | **Ø4.200** | Not a screw size we recognise. Purpose UNKNOWN |
| **`new_body`** (tower) | 9 bores | **Ø4.300** | M4 clearance |
| **`new_body`**, **`new_topframe`** | 3 bores each | **Ø8.200** | **The M8 threaded rods.** Confirms the BOM |
| **`Platform`** | 24 bores | **Ø4.300** | M4 clearance, on a 30/45/60/90 mm pattern |

> **The `5_intermediate_baseplate` is the answer to "what does the BasePlate screw to".** Its nine
> Ø2.5 mm holes sit on the same off-centre grid as the BasePlate's nine Ø3.2 mm ones. That
> match is the confirmation that the odd 7.5 mm offset is deliberate and not a modelling slip.

> **Which way up?** The BasePlate's counterbore is on the Z = 0 face *of the mesh*. Which way that
> face points in the assembled instrument is **not** something a mesh can tell you -- slicers and
> assemblies flip parts freely. Look at the physical plate before deciding which side the screw
> heads go in. VERIFY.

### Bores that are not vertical

**Added 2026-09-06.** The first pass only looked for holes running along Z and therefore reported
`SamplePlate` and `ThreadAdaptor` as having no features at all. That was a limitation of the tool,
not of the parts. It now scans all three axes.

| Part | Bore | Measured | Reading |
|---|---|---|---|
| **`PiezoPlate`** | 3 along **X** | **Ø4.200**, 5 mm deep, at Y = −27, 0, +27 from centre, Z = 7.50 | **The same −27 / 0 / +27 spacing as the BasePlate hole grid.** Not a coincidence |
| **`PiezoPlate`** | 4 along **Y** | **Ø4.200**, 5 mm deep, at X = ±15, Z = 7.50 | Blind pockets from both faces |
| **`SamplePlate`** | 4 along **Y** | **Ø4.200**, 6 mm deep, at X centre, Z = 9.50 and 39.50 | **Four blind pockets, and the BOM lists exactly four disc magnets.** INFERRED, worth one look at the real part |
| **`SamplePlate`** | 1 along **X** | **Ø2.000**, X 171.02–181.53 | A single small cross-hole low on the plate. **Purpose UNKNOWN** — a wire feed-through and a set screw are both plausible |
| **`ThreadAdaptor`** | 2 along **Y** | **Ø4.199**, ~5 mm deep, at Z = 12.00 | Grub-screw or pin holes into the coupling |

`Ø4.2` recurs across three parts and is distinct from the `Ø4.3` used throughout the isolation
tower, where it is M4 clearance. **Ø4.2 is something else and it is consistent.** Not resolved.

---

### The scan head lever geometry — measured

The `PiezoPlate` carries **three Ø8.100 mm through-holes** in an isosceles triangle. The BOM lists
three 1/4"-80 fine-adjust screws and three brass inserts, and 8.1 mm is a sensible bore for a
0.438"-long insert. **That the counts match is the evidence; it is not independently confirmed.**

| Measurement | Value | Tag |
|---|---|---|
| Front pair spacing (the two screws on one line) | **35.000 mm** | CONFIRMED |
| Front-screw line to the third (rear) screw | **40.000 mm** | CONFIRMED |
| Other two triangle sides | 43.661 mm each | CONFIRMED |
| Piezo disc pocket centre, relative to the front-screw line | **1.000 mm in front of it** | CONFIRMED |

Those are exact round numbers — 35.000, 40.000, 1.000 — which is what design intent looks like.

> **This may answer the lever-ratio question that has been open all project.** If the front two
> screws are the pivot and the rear screw is the one the motor drives, the geometric reduction at
> the disc is **40.00 / 1.00 = 40**, giving **3.88 nm per motor step** rather than the 7.8 (ratio
> 20) or 5.2 (ratio 30) taken from Berard.
>
> **Do not treat that as settled.** It assumes the tip sits at the disc centre and that the rear
> screw is the driven one. Both are readable off the assembled instrument in about a minute with
> a ruler, and that is the check worth doing. Recorded as a lead, not a result.

---

### The piezo disc pocket does not match the disc in the BOM

**This is the most consequential thing found in the mechanical audit.**

Measured on `PiezoPlate`, fit error 0.0000 and 0.0001:

```
Ø20.500 recess, 3.00 mm deep, on the Z = 15 face
    over
Ø18.000 through-bore, the remaining 12.00 mm
```

That is the textbook mounting for a unimorph disc scanner: the brass rim is clamped in the shallow
recess and the ceramic centre flexes freely into the clearance below.

**But `docs/BOM.md` specifies a disc of "about 25 to 27 mm brass".** A 25–27 mm disc does not go
into a 20.5 mm pocket. Meanwhile Berard's reference part, the Murata 7BB-20-6, is **20 mm** — which
fits Ø20.5 with 0.25 mm of clearance all round.

Three possibilities, and the repository cannot choose between them:

1. **The BOM is wrong** and this design was always dimensioned for a 20 mm disc.
2. **The pocket is not for the disc at all** and the disc mounts elsewhere.
3. **The pocket was modelled for Berard's 20 mm part and never updated** when a larger disc was chosen.

**Resolve it with a caliper.** Measure the disc actually in hand and the actual pocket in the
printed plate. If the disc is 25–27 mm, it cannot use this pocket and something has to change —
and it matters beyond fit, because **a larger disc gives more displacement per volt**, so every
nm/V figure in `docs/ENGINEERING_REFERENCE.md` §4 depends on which disc is really mounted.

---

### Not measured

`SamplePlate` and `ThreadAdaptor` have **no vertical round holes at all**, so this method reports
nothing for them. That is "not measured", not "no holes" -- both have features cut sideways or
non-round, and neither was resolved.

> **A warning, because it nearly went into this table as fact.** An earlier version of the script
> reported six Ø2.03 mm holes in the `ThreadAdaptor`. They do not exist. It was measuring short
> arcs of the part's own Ø22 mm outer wall and fitting circles to them. The fix was to segment the
> mesh into connected surfaces first, so an outside wall can never be mistaken for a bore, and to
> print the fit error so a bad measurement is visible. **If a diameter is not a round number,
> distrust it.**

To re-run any of this:

```bash
python3 Code/pc/stl_features.py                                  # every part
python3 Code/pc/stl_features.py CAD/prints/scan-head/BasePlate.stl
```

---

## How these parts were actually printed

**From the five `.3mf` project files in `CAD/prints/print-plates/`, opened 2026-09-06.** A 3MF is a
zip; each of these carries the slicer's complete settings and the list of objects on the plate.
Nobody had opened them. They are the only record of what the physical parts are made of.

| Setting | Value |
|---|---|
| Printer | **Bambu Lab X1 Carbon**, 0.4 mm nozzle |
| Material **selected in these files** | Bambu **PA-CF**, nozzle 290 °C, bed 100 °C — **but see the warning below** |
| Layer height | **0.08 mm** ("Extra Fine"), 0.2 mm first layer |
| Walls | 2 |
| Top / bottom shells | 9 / 7 |
| Infill | **40% zig-zag on the scan-head plate; 15% grid on the isolation parts** |
| Supports | **off** on every plate |
| Brim | auto |
| Bed | textured PEI |

Every object on every plate is assigned to extruder 1, and slot 1 holds the PA-CF. PLA sits in
slot 2 and is never used.

> ### The material in these files CONFLICTS with the BOM. Do not trust the plates on this.
>
> These project files were saved by the slicer on **2026-07-03** with **PA-CF** selected.
> `docs/BOM.md` §10, written later on **2026-08-14**, says in the first person: *"We used PETG-CF.
> Mech Panda used PA-CF, but we tried it first and couldn't print it reliably at these tolerances."*
>
> **The BOM is the newer statement and it is first-hand, so it wins.** The most likely story is that
> these plates record the earlier PA-CF attempt, the switch to PETG-CF happened at the printer, and
> the project files were never re-saved. That fits: 290 °C and a 100 °C bed would be badly wrong for
> PETG-CF, which wants roughly 250 °C and 70 °C — so whatever was actually printed did **not** use
> the temperatures in these files.
>
> **Treat the plates as reliable for geometry, layout and infill, and unreliable for material and
> temperature.** UNKNOWN which material the parts in hand actually are — and it is a one-question
> answer from whoever ran the printer. It matters: PA-CF and PETG-CF differ in stiffness, creep and
> moisture uptake, and all three show up as drift in an STM image.
>
> If PA-CF is ever used, **dry the filament first** — nylon is hygroscopic and wet nylon prints
> weak and dimensionally off.

**The 40% / 15% infill split is a deliberate, sensible choice** and worth preserving if anything is
reprinted: the stiffness-critical scan-head plates got more than twice the infill of the big
isolation parts, where mass matters more than stiffness.

### What is on which plate

| Plate file | Contents |
|---|---|
| `Masterplate_1.1.3mf` | **The whole scan head**: BasePlate, MotorSupport, PiezoPlate, SamplePlate, ThreadAdaptor, box mount — plus 9 spring-hanger pieces and 2 coin weights |
| `Masterplate2.3mf` | `Platform` |
| `masterplate3.3mf` | `new_topframe` |
| `Masterplate4.3mf` | `new_body` |
| `masterplate5.3mf` | `magnet mount` |

**No plate contains any of the six enclosures** (`1_preamp_box` … `6_shield_cover`). They were
printed some other way, or from a project file that was never saved here. Not a problem — they
exist physically — but if one needs reprinting there is **no saved plate for it**, and the settings
above are the best guide.

---

## Multi-part STLs — two files are not one part each

Two of the isolation STLs contain **several separate solids**, which is why the slicer shows more
objects than files. Counted by splitting the meshes into connected components:

| File | Solids | What they are |
|---|---|---|
| **`Spring_hangers_and_extentions.stl`** | **9** | Three of each of three designs, all Ø25.00 mm: **3 × 8 mm tall** (a cap, Ø14.7 recess, Ø4.3 bore), **3 × 50 mm tall**, **3 × 85 mm tall** |
| **`coin_weights.stl`** | **3** | Three identical Ø24.00 × 15.00 mm cups, each with an M3 clearance hole (Ø3.400) counterbored Ø8.000 |

**Three of each is the signature of the three-point suspension**, and it matches the BOM's three
springs, three rods and three top caps. The two tall pieces each carry a ~25 mm section of larger
bore at one end (Ø18.222 on the 50 mm piece, Ø17.334 on the 85 mm piece) which is consistent with
the BOM's **M20 × 2 spring top caps** screwing into them — INFERRED from the diameters, not
confirmed, and note the bores are plain cylinders in the mesh, so any thread is cut or printed
separately rather than modelled.

---

## Hardware note

**The preamp box is the only part using M2 screws.** Every other box and plate is M3. The
isolation tower is its own world: M4 through the `Platform` and `new_body` bores, and M8 for the
three threaded rods. Buy one bag of M3 and it will be wrong for exactly the preamp box and the
whole tower.

---

## Directories

| | |
|---|---|
| `scan-head/` | BasePlate, PiezoPlate, SamplePlate, MotorSupport, ThreadAdaptor, box_mount |
| `isolation/` | Tower body and top frame, Platform, spring hangers, magnet mount, coin weights |
| `enclosures/` | Preamp, controller, Teensy protoboard boxes, intermediate baseplate, shield cover |
| `print-plates/` | 3MF plates as printed |

`our_preamp_cad_files/` in the repository root holds **our own modified** preamp box, which
differs from `enclosures/1_preamp_box_*` here. Both are kept deliberately.
