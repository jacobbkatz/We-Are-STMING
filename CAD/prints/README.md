# Printable parts

Every part you need to print, extracted from the distribution zip so **GitHub renders the STLs in
your browser** — click any file to spin it around before you slice it.

**Print in PETG-CF or PA-CF. Not PLA.** PLA creeps under sustained load and moves with
temperature, and that shows up directly as drift in your images. Budget roughly 500–800 g.

`print-plates/` holds the 3MF plates we actually printed from, if your slicer takes them.

---

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
| **`6_shield_cover.stl`** | **Use this one.** Matches the original build: the head sits open on its baseplate and the shield drops over the whole assembly. **Wrap it in copper tape and ground it at one point.** |
| `4_scanhead_box_base/_lid.stl` | An earlier enclosed-box approach, kept for reference only. Its corner ears are 142.8 mm wide, so it will not fit inside the shield cover anyway |

> **Ground the shield at one point.** Not several — multiple bonds around an enclosure make a
> ground loop. And an ungrounded shield can be worse than no shield at all; that is currently a
> leading suspect for the fault blocking this build. See `STATUS.md`.

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

## Hardware note

**The preamp box is the only part using M2 screws.** Everything else is M3. Buy one bag of
hardware and it will be wrong for exactly that one box.

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
