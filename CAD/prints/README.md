# Printable parts

Every part you need to print, extracted from the distribution zip so **GitHub renders the STLs in
your browser** — click any file to spin it around before you slice it.

**Print in PETG-CF or PA-CF. Not PLA.** PLA creeps under sustained load and moves with
temperature, and that shows up directly as drift in your images. Budget roughly 500–800 g.

`print-plates/` holds the 3MF plates we actually printed from, if your slicer takes them.

---

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
