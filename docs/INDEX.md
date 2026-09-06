# What is inside every archive and binary

**Zips, PDFs and CAD files are not greppable. This file exists so their contents are.**

Four times in four days, something recorded as unknown or blocked in this project turned out to be
sitting inside one of these files. **Check here before deriving anything from scratch, and before
writing UNKNOWN or "needs a bench test".**

`CLAUDE.md` §3b is the rule this file serves.

---

## Answers already extracted from these files

Do not re-derive these. They are done, and where they live now:

| Question | Answer | Came from | Now written up in |
|---|---|---|---|
| Is the ADC full scale 4.096 V or 10.24 V? | **4.096.** The LTC2326 runs on its internal reference; no external reference reaches it | Controller schematic PDF | `docs/UPSTREAM_MECHPANDA.md` §1 |
| What is the JP1 pinout? | 1=GND, 2=+supply, 3=OUTPUT, 4=GND, 5=−supply | Preamp gerber X2 attributes | `docs/WIRING.md` §10 |
| Why does JP1 pin 4 wander? | **No copper track lands on it.** A routing defect, not a build fault | Preamp gerber copper layers | `docs/WIRING.md` §10 |
| Are CLEAR#/RESET# really floating? | **Yes** — 25 single-pad nets, 20 of them the DAC control pins | `FlyingProbeTesting.json` | `STATUS.md` fault 4 |
| Which scan head enclosure do we use? | `6_shield_cover`. **Wrap in copper tape and ground at one point** | `WHICH_SCANHEAD_PART.txt`, inside a zip | `CAD/prints/README.md` |
| What is the coarse approach screw? | 1/4"-80, and it is a scan head part | `CAD/STM.f3z` → `DesignDescription.json` | `docs/UPSTREAM_BERARD.md` §2 |
| Every net on the controller board | 96 nets, 893 pins, all named | `FlyingProbeTesting.json` | `docs/WIRING.md` |

---

## The archives

### `gerbers/Gerber_PCB1_all_red.zip` — controller manufacturing files

**Contains `FlyingProbeTesting.json` — the complete board netlist.** 541 components and 893 pins,
each with its net name, position, layer, pad shape and hole size. This is the most information-dense
file in the repository.

Also: copper, silkscreen, mask and paste gerbers; three drill files; `How-to-order-PCB.txt`.

```python
import json
d = json.load(open('FlyingProbeTesting.json'))
d['pins']['fields']   # PIN_NO PIN_NAME PIN_X PIN_Y LAYER PIN_TYPE NET_NAME ...
d['pins']['rows']     # 893 of them
```

**A net with only one pad on it is an unconnected pin.** That is how the floating DAC control pins
were found.

### `gerbers/STM_Preamp_OPA627_Gerbers(1).zip` — preamp manufacturing files

**KiCad gerbers carrying X2 attributes**, which embed component, pin and net names directly in the
copper files. Effectively the preamp netlist.

```bash
grep -o '%TO\.[PN],[^*]*\*%' tunnelAmp-F_Cu.gbr | head
```

`%TO.P,<component>,<pin>*%` names a pad; `%TO.N,<net>*%` names its net; the `X..Y..D03*` line that
follows is where it sits. `tunnelAmp.drl` is a plain-text Excellon drill file with every hole,
its size, and whether it is plated.

### `PCB/PDF_Scanning Tunneling Microscope_2023-11-04.zip` — the controller schematic

**Three pages: DACs and output stage, the ADC, connectors and power.** This answered the ADC
reference question that had been recorded as needing a bench calibration.

**Its text is vector-outlined, so most PDF tools extract nothing.** PyMuPDF works:

```bash
pip install pymupdf
python3 -c "
import pymupdf
d = pymupdf.open('SCH_Controller_2023-11-04.pdf')
for i, p in enumerate(d): print('=== PAGE', i+1, '==='); print(p.get_text())
"
```

**Text extraction gives pin names but NOT connectivity.** No-connect markers are graphical. To see
those, render and look:

```python
page.get_pixmap(dpi=300, clip=rect).save("zoom.png")
```

### `PCB/Altium_Scanning Tunneling Microscope_2023-11-04.zip`

Altium source for the controller: `1_ADC.schdoc`, `2_Connectors.schdoc` and other sheets. Binary
Altium format. **The PDF above is the same schematic and is readable — use that instead.**

### `PCB/STMP_easyEDA.zip`

EasyEDA Pro project for the controller. `SHEET/*/1.esch`, `2.esch`, `3.esch` are the three
schematic sheets; plus symbol, footprint and PCB files under hashed names. Proprietary format.
**The PDF is the readable version of the same design.**

### `We-Are-STMING_PCB.zip` (repository root)

A distribution bundle. Contains the preamp gerbers **and Eagle source** (`preamplifier/eagle/`,
including `LICENSE_MIT.txt`), the controller EasyEDA project, and the schematic PDF.

> **It also contains stale copies of `START_HERE_gotchas.md`, `README.md` and `BOM.md`.**
> Those are older than the live versions in `docs/`. **Do not read them.** They were deliberately
> not extracted on 2026-09-01 for this reason.

### `CAD/STM.f3z` — Fusion 360 archive

**A zip.** `DesignDescription.json` names every referenced component:

```
MOTOR MODEL 28BYJ-48 5V v4 v1
ScanHead_97424A590_Ultra-Fine-Thread Plastic-Head Thumb Screw
ScanStage
98625A960_0.438 Long Brass Insert
```

The four `.f3d` files are proprietary binary. **The scan head lever ratio is in there and has not
been extracted** — that is still VERIFY.

---

### `CAD/prints/*.stl` — the printed parts

**STL files are binary meshes, so they are not greppable — but they are trivially measurable.**
Every part's real dimensions are tabulated in `CAD/prints/README.md`. **Read that table before
asking what a part is.** It settled the two-shields question in one look:

| | |
|---|---|
| `6_shield_cover` | **142 × 128 × 112 mm** — over the whole scanning module |
| `1_preamp_box` | **35 × 29 × 21 mm** — around one small PCB |

To measure any mesh yourself, bounding box from the facet vertices:

```python
import struct
d = open('part.stl','rb').read()
n = struct.unpack('<I', d[80:84])[0]          # binary STL: facet count at byte 80
# each facet is 50 bytes: 12 floats (normal + 3 vertices) + 2 byte attribute
```

## Not archives, but easy to overlook

| File | What is in it |
|---|---|
| `Code/teensy/src/logTable.hpp` | 393 KB. The header carries **the MATLAB that generated it** and Berard's MIT copyright |
| `Code/teensy/lib/LTC2326/LTC2326_16.hpp` | Full **MIT licence text** in the header, and the `4.096` reference constant |
| `docs/PROJECT_HANDOFF_SUMMARY.md` | 1918 lines. **Its header banner is a live correction log** — the newest corrections get written there. Read the top even though the body is ranked last |
| `Images/*.bmp` | Mech Panda's own atomic-resolution HOPG scans. Reference images, not our data |

---

## When you add a file

**If it is an archive, a PDF, or any binary, add a row here saying what is inside it.** Otherwise
it becomes another place an answer can hide.
