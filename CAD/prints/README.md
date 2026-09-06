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
