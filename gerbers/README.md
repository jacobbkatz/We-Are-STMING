# Manufacturing files

Send these to a board house.

| File | Board | Notes |
|---|---|---|
| `Gerber_PCB1_all_red.zip` | **Controller** | 15 files: copper, silkscreen, mask, paste, outline, drill, plus flying-probe test data |
| `STM_Preamp_OPA627_Gerbers(1).zip` | **Preamplifier, rev 1** — the boards we own | 11 files. 20.625 × 15.23 mm, 2-layer. **Do not order this one again**: its ground fill is missing (`STATUS.md` fault 0d) and C2 is drawn backwards (fault 1d) |
| `gerbers_rev2_preamp_nuhshaheer_jacobkatz.zip` | **Preamplifier, rev 2** | **UNTESTED — see below.** 12 files. Same size and holes as rev 1 |

## Preamp rev 2 — NOT TESTED

**Designed by Nuh in KiCad 10, 2026-10-12 to 2026-10-13. Not ordered, not built, not powered, not
measured.** It is better than rev 1 **on paper only**. Nothing about it has been proven on hardware.

**What it changes from rev 1**, starting from Dan Berard's original Eagle layout:

- **The ground fill on the underside is filled.** Rev 1's files were exported with it empty, so six
  ground points were connected to nothing and had to be scraped and hand-wired on the spare
  (`STATUS.md` fault 0d). On rev 2 the only hand-wiring should be **the five JP1 wires plus the
  feedback resistor and tip wire on the PTFE standoff**.
- **C2 is turned round** so its + end is on ground. Berard's design puts it on -15 V, reverse-biasing
  the tantalum (`STATUS.md` fault 1d). The copper is unchanged; only which pad is + changes.
- **Printed `+` beside C1 and C2's + pads.** Rev 1 printed no polarity mark, which is why JLCPCB asked.
- **JP1 holes 1 and 4** join the ground fill solidly; ground fill clearance 0.3 mm; edge rule 0.3 mm.
- **"REV2" and the builders' names** printed on the underside, so it cannot be mistaken for a rev 1.
- **Standoff hole left at 2.108 mm**, Berard's original. **VERIFY before ordering**: whether our
  Keystone 11301's pin sits inside that hole on the spare is disputed in the record (`docs/OPEN_QUESTIONS.md`).

**What was checked, from the files only** (2026-10-13, Claude, on Nuh's zip as committed):

| Check | Result |
|---|---|
| `Code/pc/gerber_netcheck.py` — every net one piece of copper, no shorts | **PASS** |
| Tantalum polarity, from the pad labels | C1 + on +9V, **C2 + on GND** — both correct |
| Outline, holes and top copper against rev 1 | **Identical**; the bottom is rev 1's copper plus about 175 mm² of ground fill |
| KiCad design rule check | **0 unconnected.** Remaining warnings are inherited from Berard's layout, plus one: the underside names are 0.6 mm tall, under KiCad's 0.8 mm minimum, the same line width as Berard's own lettering |

**None of that is a test of the board.** It shows the files say what was intended. **Whether the board
works is unknown until one is built and measured** — the first check would be the same continuity
readings done on the spare (`sessions/2026-09-14.md` §3.1), then the bench-supply smoke test.

The supply nets are still named `+9V` / `-9V` inside the files, as in Berard's original. The board runs
on ±15 V and the printed labels say so. **The KiCad project is in [`../PCB/preamp_rev2/`](../PCB/preamp_rev2/)**;
re-plotting it reproduces this zip exactly (checked layer by layer, 2026-10-13).

We paid **$321.44 for 5 assembled controller boards** at JLCPCB in 2026, about $64 each.

## Two things about the preamp board

**The 100 MΩ feedback resistor is not on the board.** The R2 footprint has **no copper at all**,
just bare drilled holes. That is deliberate — at picoamp currents, leakage across the board
surface would swallow the signal, so the input node is built in the air on a PTFE standoff.

**PAD1 is the amplifier output, not the tip input.** It is wired to the op-amp's pin 6. Solder the
tip there and the microscope will never see a tunneling current. See
[`../docs/WIRING.md`](../docs/WIRING.md) section 10.

## Through-hole parts are not placed

JLCPCB does not fit them. Even on an assembled controller board you solder these yourself: the
OPA2227P and LT1469IN8 op-amps, both TO-220 regulators, both DB9 sockets, the JST XH power header
and the 26-pin box header. Buy DIP-8 sockets rather than soldering the op-amps in directly.
