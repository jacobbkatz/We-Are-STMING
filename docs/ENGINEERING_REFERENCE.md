# Engineering reference

**The cross-subsystem layer.** `STATUS.md` says where the build is; `docs/WIRING.md` gives pinouts;
this file gives the **relationships** — what connects to what, what a number becomes downstream, and
what else has to be checked when something changes.

Written 2026-09-06 in a repository-wide audit. Every value carries a confidence tag.

| Tag | Means |
|---|---|
| **CONFIRMED** | Direct evidence — measured at the bench, or read from a netlist, mesh or datasheet |
| **DERIVED** | Calculated from CONFIRMED values. The calculation is shown |
| **INFERRED** | Several pieces of evidence agree, no single direct measurement |
| **TENTATIVE** | Plausible, weakly supported |
| **UNKNOWN** | Not established |
| **CONFLICTING** | Repository sources disagree |

---

## 1. System architecture

```
  PC (Python)                Teensy 4.1              Controller PCB            Scan head
  ───────────                ──────────              ──────────────            ─────────
  stm_console.py   USB   ┌─────────────┐   26-way   ┌──────────────┐  DSUB1   ┌──────────┐
  adc_stats.py    ─────► │ 4-char cmds │  ribbon    │ U1 X  ──┐    │ ───────► │ piezo    │
  stm_approach.py        │ stm_firmware│  ────────► │ U2 Y  ──┤    │  4 wires │ 4 quads  │
  (stm_app.py: DO        │             │            │ U3 Z  ──┼─►  │          │          │
   NOT USE)              │  loop():    │            │ U4 bias │ U9 │          │ tip ─────┼─┐
                         │   checkSerial            │         │U10 │          └──────────┘ │
                         │   update()  │            │         │U13 │                       │
                         │   approach()│            └─────────┴────┘                       │
                         │   control_current                │  DSUB2                       │
                         │             │ ◄──────────  U15 ADC ◄── U21 ◄── PREAMP+ ◄────────┘
                         └─────────────┘   SPI1     (LTC2326-16)         (OPA627 TIA,
                                                                          100 MOhm)
       power:  bench supply +/-18 V ──► U19 (JST XH) ──► V++ ──┬─► U17 ──► +15 V
                                                               ├─► U16 ──► 3.3 V
                                                               └─► U22 ──► 5 V
                                                        V-- ────► U18 ──► -15 V
```

**Two SPI buses.** DACs on `SPI` (Teensy 11/13), ADC on `SPI1` (Teensy 27/38/39). **Both run at
1 MHz** — CONFIRMED, and neither may be raised; the ribbon could not carry 40 MHz.

**The motor is not on this diagram's ribbon path.** Teensy 33/34/35/36 go straight to a ULN2003
module. **Nothing motor-related exists on the controller PCB.** CONFIRMED from the netlist.

---

## 2. Grounding map

**CONFIRMED from `FlyingProbeTesting.json`** — the complete controller netlist.

### There is exactly one ground net on the controller board

| Finding | Evidence |
|---|---|
| **`AGND` is the only ground net. 198 pins.** | Net census of all 893 pins |
| **There is no separate DGND** | U1–U4 pin 16 (DGND) and pin 5 (AGND) are **both on `AGND`** |
| The ADC's three ground pins (3, 6, 16) are all `AGND` | same |
| No net named `GND` or `DGND` exists anywhere | same |

**So the usual analog/digital ground-split reasoning does not apply to this board.** Every ground
pin on every IC is the same node. If a ground problem is ever suspected, it is a *routing or
joint* problem within one net, not a split-plane problem.

### Power tree, pin by pin

| Ref | Part | In | Out | Feeds |
|---|---|---|---|---|
| **U19** | B3B-XH-AM JST XH | — | pin 1 `V--`, pin 2 `AGND`, pin 3 `V++` | the board's only power entry |
| U17 | SL7815 | `V++` | **+15 V** (52 pins) | U1–U5, U9, U10, U13, U21 |
| U18 | L7915CV | `V--` | **−15 V** (46 pins) | U1–U4, U9, U10, U13, U21 |
| U16 | BD733L5FP | `V++` | **3.3 V** (42 pins) | U1–U4 DVCC, U15 OVDD |
| U22 | MC7805CDTG | `V++` | **5 V** (8 pins) | U15 VDD only |
| U5 | ADR421 | +15 V (pin 2) | **VREF1** (pin 6, 12 pins) | U1–U4 pin 4 only. **Not the ADC** |

> ### A dependency that matters for tomorrow's rail-scaling test
>
> **`V++` feeds three regulators: +15 V, 3.3 V AND 5 V. `V--` feeds only −15 V.** The supply is
> therefore **asymmetrically loaded**, and dropping the positive rail in the D2 rail-scaling test
> reduces the input to the **digital** regulators as well as the analog one.
>
> U16 is an LDO dropping V++ to 3.3 V, so it has enormous headroom at 18 V and will not drop out
> at 10–13 V. **But if V++ is ever taken low enough to disturb 3.3 V, the DACs lose DVCC — which
> presents exactly as the hourly configuration loss.** Do not confuse the two during D2.
> DERIVED from the power tree.

### The reference is not shared

**`VREF1` (2.5 V, measured across C54) reaches the four DACs and nothing else.** The ADC runs on
its **own internal reference**. CONFIRMED — "VREF1" and "ADR421" appear zero times on the
schematic's ADC sheet.

### Shields and chassis — these are NOT the same as AGND

| Node | Path to AGND | Confidence |
|---|---|---|
| **Preamp box shield** | One soldered ground wire, added 2026-09-06 | CONFIRMED it exists; **continuity across the box UNKNOWN — the acceptance test was never run** |
| **Scan head shield cover** | Grounded at one point | INFERRED (reported by Jacob, not metered) |
| **DSUB1 shell** | **NONE.** Sits alone on its own net | CONFIRMED from netlist |
| **DSUB2 shell** | **NONE.** Same | CONFIRMED |
| **H1 pins 24, 26** | **NONE.** Each alone on its own net | CONFIRMED |
| Piezo brass electrode | Ground, and used to shield the tip from the scan electrodes | INFERRED from Berard |
| Tip / TIA input | **Virtual ground** at the op-amp, not a real ground | CONFIRMED by circuit topology |

> **Loop risk.** Metal DB9 backshells would float — no board-side path. If a shield is grounded at
> the scan head *and* a backshell touches a grounded chassis somewhere else, that is a loop the
> board's netlist cannot show you. Ground each shield **at one point only**.

---

## 3. Copper tape vs aluminium tape — the rule

Asked repeatedly, scattered across three documents. **Consolidated here.**

> ## Use COPPER tape everywhere on this instrument. Do not use aluminium tape at all.

| | Copper | Aluminium |
|---|---|---|
| Takes solder | **Yes** — bond a ground wire directly | **No.** The oxide layer prevents it |
| Adhesive conducts | Buy **conductive-adhesive** copper; then overlaps conduct | **Usually not.** Overlapping strips may not connect to each other |
| Next to the other metal | — | **Forms a galvanic cell** with copper in humidity |
| Cost per area | Higher | Lower |

**Aluminium is only ever attractive for cost, and it fails on all three technical points.**

### Why this is not theoretical here

On 2026-09-06 the preamp box was found wrapped in **both**, and it was:

- **discontinuous** — beeped in some places, open in others, because the aluminium adhesive
  insulated the overlaps;
- **partly grounded** — the ground wire only reached the patches it happened to touch;
- **copper touching aluminium in many places** — a galvanic couple millimetres from the
  highest-impedance node in the instrument.

It was stripped and rebuilt in **copper only, with the seams soldered**. That is the pattern to
follow.

### The rule, stated as instructions

1. **Copper tape only.** Both the preamp box and the scan head shield cover.
2. **Buy conductive-adhesive copper tape.** Non-conductive adhesive reintroduces the
   discontinuity problem.
3. **Solder the seams.** Do not trust overlap alone, on either metal.
4. **Bond to circuit ground at ONE point.** More than one makes a ground loop.
5. **Then meter it.** Every point on the shield must beep to the ground wire — near the wire, the
   far corner, and across every seam. **A shield you have not metered is not a shield you can
   reason about.**
6. **Never put copper and aluminium in contact** anywhere in the assembly.

**If aluminium tape is used anyway** — for cost, over a large area with no ground bond and no
copper nearby — it still must not touch copper, and it still needs a mechanical clamp rather than
a solder joint for any ground connection.

---

## 4. Value chain: a scan command to physical displacement

Each arrow is a place a number changes meaning.

```
GUI / console  "DACZ 50000"
   │  stm_console.py build_frame(): one write, 4-char command + argument + newline   CONFIRMED
   ▼
Teensy  serialCommand() → stm.set_dac_z(50000)                                       CONFIRMED
   │  AD5761::write(CMD_WR_UPDATE_DAC_REG, 50000) over SPI at 1 MHz
   ▼
U3 DAC output ZOUT
   │  code 0..65535, 32768 = 0 V, range bits 000 = +/-10 V                           CONFIRMED
   │  (50000 - 32768) / 32768 * 10 V = +5.26 V at the DAC pin
   ▼
U9 / U10 summing stage
   │  inverting summer, gain exactly -1 per input (non-inverting input at AGND)      CONFIRMED
   │  Z+X = -(ZOUT + XOUT), Z-X = -(ZOUT - XOUT), likewise for Y
   │  through R6/R9/R14/R19 = 220 R in series into the DB9
   ▼
DSUB1 pins 6-9 → four piezo quadrant wires
   │  measured: DACZ 65535 gives -10 V at the scan head end                          CONFIRMED
   ▼
Piezo displacement
      ~34 nm/V in Z, ~83 nm/V in XY                                                  INFERRED
      (Berard's measured figures for a disc scanner, not ours)
```

### Numbers that fall out of that chain

| Quantity | Value | Basis |
|---|---|---|
| Z volts per DAC count | 20 V / 65536 = **0.305 mV** | DERIVED |
| Z displacement per count | 0.305 mV × 34 nm/V = **0.0104 nm** | DERIVED, on an inferred nm/V |
| Z full travel | ±10 V × 34 nm/V ≈ **680 nm** | INFERRED |
| X/Y volts per count | 6 V / 65536 = **0.0916 mV** | DERIVED |
| X/Y full travel | ±3 V × 83 nm/V ≈ **500 nm** | INFERRED |
| Z resolution vs target | 0.0104 nm against Berard's ~0.01 nm goal | DERIVED — **16 bits is just adequate; the absence of sigma-delta is probably fine** |

> **X and Y are ±3 V, not ±5 V.** Range bits `101`. The firmware comments say ±5 V and are wrong.
> `docs/soft_launch_test_procedure.md` §2 has the full RA[2:0] decode: `000` = ±10 V, `010` = ±5 V,
> `101` = ±3 V. CONFIRMED.
>
> **Our X/Y range is a third of Berard's** because he drives ±10 V. That is a resistor-and-range
> choice, not a limit of the disc.

---

## 5. Value chain: tunneling current to a displayed number

```
tip / sample junction
   │  bias set by U4 → R30 3k → U13.1 (OPA2227P) → R32 220R → DSUB2 pin 1
   │  gain -1: BIAS 65535 commands +3.000 V and measures -3 V at the holder   CONFIRMED
   ▼
tunneling current, order 1 nA
   │  OPA627 transimpedance, 100 MOhm feedback, air-wired on a PTFE standoff  CONFIRMED
   │  Vout = -I * 100 MOhm  ->  1 nA = 0.1 V
   ▼
preamp output → JP1 pin 3 → DSUB2 pin 3 (PREAMP+) and pin 2 (PREAMP-)
   │  differential pair back to the controller
   ▼
R23-R26 470 R + C27-C30 3.3 nF  ->  RC corner ~100 kHz                        CONFIRMED
   │  U21 LT1469 dual op-amp buffers the pair
   ▼
U15 LTC2326-16, internal reference                                            CONFIRMED
   │  0.125 mV per count  ->  1 nA = 800 counts
   ▼
firmware  stm_status.adc  (raw single conversion, set by update() each loop)
   │  GSTS field 5 = RAW.  ADCR = 5-sample rolling average                    CONFIRMED
   ▼
PC tools — and here the number goes wrong
      stm_control.py:37 and stm_console.py use 10.24 V full scale.
      It is 4.096. Every current these tools print is 2.5x too large.         CONFIRMED
```

### The ADC scale, and why the signed reading is right

**0.125 mV per count**, from 4.096 V over 32768 counts. Three independent checks agree:

| Check | Result |
|---|---|
| 1 nA × 100 MOhm = 0.1 V ÷ 0.125 mV | **800 counts** — session 3 recorded "~800 counts for 1 nA" |
| 29873 counts × 0.125 mV | **3.734 V** — session 3 recorded 3.73 V |
| 3.734 V ÷ 100 MOhm | **37.3 nA** — session 3 recorded 37 nA |

**The output is signed two's complement, not straight binary.** INFERRED, by contradiction:

- As **signed**, a −400 baseline is −0.050 V — a healthy preamp sitting near zero, and the faulty
  one at +3.73 V. Coherent: the fault is a positive offset.
- As **unsigned**, −400 reads 65136 counts = 4.07 V, and the *faulty* 29873 reads only 1.87 V.
  That makes the healthy baseline higher than the faulty one, which is backwards.

**Still worth confirming from the datasheet**, but the physical coherence argument is strong.

---

## 6. Coarse approach chain

```
"MTMV 500"  →  EfficientStepper::step(500)  →  ULN2003  →  28BYJ-48
   │  setSpeed(2) = 2 rev/min = 68.27 steps/s. 500 steps ~ 7.3 s   CONFIRMED
   ▼
2048 steps per revolution, measured on our unit                     CONFIRMED
   ▼
1/4"-80 fine screw:  25.4 mm / 80 = 317.5 um per revolution         CONFIRMED (BOM + CAD name)
   │  317.5 / 2048 = 155 nm per step AT THE SCREW                   DERIVED
   ▼
three-screw tripod lever reduction, ~20x or ~30x                    CONFLICTING
   ▼
5.2 to 7.8 nm per step at the tip                                   DERIVED
```

> **CONFLICTING.** Berard gives **30** on his scan head page and **20** on his coarse approach
> page and in a comment. Both are his. **Our ratio is Mech Panda's geometry and has never been
> measured** — the numbers are in the `.f3d` files, which this repository cannot read.
>
> It does not currently matter: against ~700 nm of Z travel, either figure gives **90–130 steps per
> Z range**, which is a comfortable woodpecker approach. It would matter if the Z range turned out
> much smaller.

**The firmware's `approach()` is not usable** — it compares `read_adc() > target`, signed, against a
baseline that has been negative all project. Use `Code/pc/stm_approach.py`, which thresholds on
absolute deviation. CONFIRMED.

---

## 7. Mechanical: measured, not quoted

All from `Code/pc/stl_features.py` reading the meshes directly. **CONFIRMED** unless noted.

### The two shielded enclosures are not the same object

| | Size (mm) | Encloses |
|---|---|---|
| `6_shield_cover` | **142.00 × 128.00 × 112.40** | the whole scanning module |
| `1_preamp_box_base` | **34.83 × 29.43 × 20.80** | the preamp board alone (20.6 × 15.2 mm) |

`box_mount` is **142.00 × 128.00 × 5.00** — the **identical footprint** to the shield cover, so it
is the frame the cover lands on. Its opening is 131 × 101, and `5_intermediate_baseplate` is
**130.00 × 100.00 × 5.00**, which fits it. That is the stack-up, confirmed numerically.

### Fasteners — this closes a BOM UNKNOWN

Re-measured 2026-09-06 after the extraction script was rewritten. **The first pass produced wrong
numbers and they were caught before they left this repository** — see the note at the end of this
subsection. Everything below fitted a circle to within **0.0001 mm**, and every value is a round
design number.

**The rule the whole build follows:** a lid has a clearance hole; the base underneath it has a
narrower pillar and the screw **cuts its own thread into the plastic**. No nuts, nothing pre-tapped.

| Joint | Clearance side | Threaded side | Screw | Tag |
|---|---|---|---|---|
| **Preamp box lid to base** | **dia 2.300** | **dia 1.600 pillar** | **M2** | CONFIRMED |
| Teensy / protoboard box | dia 3.400 | **dia 2.500 pillar** | M3 | CONFIRMED |
| `4_scanhead_box` (unused part) | dia 3.400 | dia 2.500 pillar | M3 | CONFIRMED |
| Controller box | dia 3.400 | pillars not resolved | M3 | INFERRED from the pattern |
| **`BasePlate` to `5_intermediate_baseplate`** | **dia 3.200** + dia 7.000 × 4.0 counterbore | **dia 2.500** | **M3** | CONFIRMED |
| `5_intermediate_baseplate` to frame | dia 3.400 + dia 6.500 counterbore | — | M3 | CONFIRMED |
| **`MotorSupport`** | **3 × dia 3.400**, 21.2 mm pitch | — | **M3** | CONFIRMED |
| `box_mount` | 2 × dia 3.300, 120 mm apart | — | M3 | CONFIRMED |
| Isolation tower, `Platform` | dia 4.300 | — | M4 | CONFIRMED |
| Tower rods (`new_body`, `new_topframe`) | 3 × dia 8.200 each | — | **M8** | CONFIRMED — matches the BOM |

> **dia 2.5 and dia 1.6 are TAP sizes, not clearance.** Drive those screws slowly and stop at
> snug. There is no metal thread to bottom out against, so over-tightening strips the printed
> pillar and the lid stops clamping onto its shield — which on the preamp box means losing the
> shield bond that is the current bench question. Do not drill a pillar out to make a screw fit.

> **`docs/BOM.md` listed "plate-to-plate and motor-mount screw sizes" as UNKNOWN. Both are now
> known and the entry is closed.** The `BasePlate`'s nine dia 3.2 clearance holes land on the
> `5_intermediate_baseplate`'s nine dia 2.5 holes on **the same off-centre grid**. That match is
> also independent proof the 7.5 mm X offset is deliberate, not a modelling slip. **6.00 mm of
> `BasePlate` remains below its counterbore**, so an M3×12 gives about 6 mm of thread engagement
> in the plate below. DERIVED.

> **A wrong measurement, caught.** The first version of the script reported six dia 2.03 mm holes
> in the `ThreadAdaptor` and a dia 3.1 counterbored hole pattern in `MotorSupport`. **Neither
> exists.** It was clustering points by proximity, which on a small part merges the whole shell
> into one blob, and then fitting circles to short arcs of the part's own **outside** wall. The
> rewrite segments the mesh into connected surfaces first — so an outer wall can never be read as
> a bore — and prints a fit-error column. The lesson generalises: **a measured diameter that is
> not a round number is a warning, not a dimension.**

### The BasePlate hole grid — the gotchas document is exactly right

Measured offsets from the part centre: **X = −37.5, −7.5, +22.5** and **Y = −27, 0, +27**.
`docs/START_HERE_gotchas.md` states precisely those numbers. **Independently verified.**

The grid is **7.5 mm off centre in X** and symmetric in Y, as documented.

### Other measured parts

| Part | Size (mm) | Note |
|---|---|---|
| `PiezoPlate` | 55.00 × 70.00 × 15.00 | 4 × dia 4.200 and 3 × dia 8.100 bores, plus a dia 18.0/20.5 stepped pocket. **Purposes UNKNOWN** |
| `SamplePlate` | 12.00 × 70.00 × 49.00 | the tall one; sets the stack height. **No vertical round holes at all** — not measured |
| `MotorSupport` | 10.00 × 52.33 × 30.00 | 3 × dia 3.400 full-height, 21.2 mm pitch, in dia 10.0 bosses |
| `ThreadAdaptor` | 21.91 × 22.00 × 17.00 | a dia 22.0 cylinder with a dia 12.800 bore, Z 7–17. Couples motor shaft to the fine screw |
| `Platform` | **200.00 dia × 6.00** | a **disc**, not a square — its bounding box lies. **24 × dia 4.300** on a 30/45/60/90 mm pattern |
| `new_body` / `new_topframe` | 215.12 × 245.34 × 60 / 55 | isolation tower bottom and top. **3 × dia 8.200** each: the M8 rods |

**Scan head stack height:** `BasePlate` 10 mm + `SamplePlate` 49 mm ≈ **59 mm**, against the shield
cover's **112.40 mm** of internal height. Fits with room. DERIVED.

**`4_scanhead_box` cannot substitute for the shield cover.** Its corner ears are 142.8 mm; the
cover's outside is **142.00 mm**. Misses by **0.8 mm** — the gotchas document says exactly this,
and the measurement confirms it. CONFIRMED.

---

## 8. Dependency and impact map

**If this changes, check these.**

### The ADC full-scale constant (4.096)
- `Code/pc/stm_control.py:37` and `stm_console.py` — currently 10.24, **wrong by 2.5×**
- every current figure in `STATUS.md` and every session log
- `stm_approach.py --full-scale` default
- the 37 nA figure, the 0.78 nA noise figure, the 800-counts-per-nA reference

### A DAC range (the mode word in `stm_firmware.hpp`)
- the volts-per-count figure and therefore displacement per count
- the summing stage's headroom at U9/U10 (gain −1, ±15 V rails)
- `stm_control.py`'s `dac_to_dac*_volts` — **already wrong**, all three assume ±5 V
- `stm_approach.py`'s Z window (10000–50000)
- the scan range the GUI reports

### The scanner disc (size, mounting, bonding)
- nm/V in Z and XY, hence every displacement number in §4
- the assembled resonance (Berard: a 6.3 kHz free-air disc measured 3.4 kHz mounted)
- whether 16-bit Z is still adequate — at 34 nm/V it just is
- `PiezoPlate` geometry and the tip standoff stack
- the number of steps per Z range in the approach, hence approach safety

### A printed scan head dimension
- `box_mount` and `6_shield_cover` share a **142 × 128** footprint — change one, check both
- `5_intermediate_baseplate` at 130 × 100 fits `box_mount`'s 131 × 101 opening
- the BasePlate 3×3 grid pitch is mirrored by whatever bolts to it
- fastener length: the counterbore depth sets how much screw is left for engagement
- the 0.8 mm interference that already rules out `4_scanhead_box`

### The preamp feedback resistor (100 MΩ)
- volts per nA at the ADC — 1 nA = 0.1 V = 800 counts
- the maximum measurable current, about 100 nA before the rails clip
- the dummy-junction resistor choice (must be ≥ 100 MΩ, **not** the 1 MΩ the 08-31 plan suggests)
- the leakage budget: 37 nA of offset is 37× a tunneling current

### Grounding anything
- there is **one** ground net; a "ground" fix is a joint or route fix, never a plane split
- both DB9 shells and H1 24/26 float — adding a bond there creates a path that did not exist
- one bond per shield, or a loop

---

## 9. Firmware and software constants

| Constant | Value | Where | Confidence |
|---|---|---|---|
| Serial baud | 115200 | `main.cpp` | CONFIRMED |
| Command length | exactly 4 chars, sent as one write | `main.cpp` `CMD_LENGTH` | CONFIRMED |
| DAC SPI clock | 1 MHz (was 40 MHz) | `AD5761.hpp` | CONFIRMED |
| ADC SPI clock | 1 MHz (was 40 MHz) | `LTC2326_16.hpp` | CONFIRMED |
| ADC reference | 4.096 V, internal | `LTC2326_16.hpp` + schematic | CONFIRMED |
| DAC reference | 2.5 V, ADR421, measured across C54 | schematic + bench | CONFIRMED |
| Steps per revolution | 2048 | `STEPS_PER_REVOLUTION` | CONFIRMED |
| Motor speed | `setSpeed(2)` = 68.27 steps/s | `reset()` | CONFIRMED |
| ADC averaging | 5-sample rolling, `ADCR` only | `_get_adc_avg()` | CONFIRMED |
| PID gains at boot | **0.0, 0.0, 0.0** | not the `INIT_K*` defines, which are only in a commented-out line | CONFIRMED |
| Z clamp in const-current | 10000–50000 | `control_current()` | CONFIRMED |
| `APRH` max travel | 10000 steps, hardcoded | `main.cpp` | CONFIRMED |
| logTable range | index 0–32768, output 0–524287 (20-bit) | generating MATLAB in the header | CONFIRMED |

**Constant-current mode does nothing until `PIDS` is sent**, because the gains initialise to zero.
That is easy to mistake for a dead loop.

---

## 10. Open engineering questions

Ranked by what they block. Full list in `docs/OPEN_QUESTIONS.md`.

| Question | What would settle it |
|---|---|
| **Does the rebuilt preamp box shield conduct end to end?** | Meter every point to the ground wire — near the wire, far corner, across each seam. **Two minutes, and every preamp conclusion depends on it** |
| **Does the AD5761R have internal pull-ups on CLEAR#/RESET#?** | One datasheet page. Decides whether the four-wire fix cures the hourly DAC dropout |
| **Is the LTC2326-16 output two's complement?** | One datasheet page. §5 argues strongly for signed, but from coherence, not documentation |
| **Our scan head lever ratio** | Open `CAD/STM.f3z`'s `.f3d` files in Fusion and measure the rear-screw and tip distances from the front-screw line. This repository cannot read that format |
| **Is the 37 nA contamination, the shield, or flux?** | D1/D2/D3, and the rail-scaling test — if it is rail-to-input leakage the offset scales with rail voltage |
| **Which Z direction is toward the sample** | First tunneling, or the CAD. `stm_approach.py` refuses to run without it |
| **Which sign of `MTMV` advances** | Watch the head with the tip removed |
| **Our disc's actual nm/V** | Every displacement figure in §4 rests on Berard's 20 mm disc; ours is 25–27 mm |
| **Piezo disc part number** | UNKNOWN for ours. Berard's is a Murata 7BB-20-6 |
| **Spring rate and magnet dimensions** | Measure the parts in hand. **Screw sizes are no longer on this list — see §7.** Heat-set inserts may not be needed at all: every printed joint measured is a screw self-tapping into a bare pillar, and no measured hole fits a standard M3 insert |

---

## 11. Conflicts found and not silently resolved

| Conflict | Sources | Status |
|---|---|---|
| Lever ratio 20 vs 30 | Berard's coarse-approach page vs his scan-head page | **Unresolved.** Both recorded; the 5–8 nm range covers it and nothing depends on the difference |
| Z range 3 µm vs 700 nm | Berard's scan-head page vs his own calibration | **Resolved.** 3 µm was his expectation from Alexander's 160 nm/V; 670 nm is what he measured. Measurement wins |
| X/Y range ±5 V vs ±3 V | Firmware comments vs AD5761 range bits | **Resolved: ±3 V.** Bits and measurement agree |
| ADC full scale 10.24 vs 4.096 | PC tools vs firmware driver and schematic | **Resolved: 4.096.** PC tools not yet changed |
| Preamp op-amp "Berard's design" | Our BOM says OPA627AU; Berard's page says OPA124 | **Resolved.** OPA627 is a substitution he endorses, but it is not his part |
| PAD1 upstream or downstream of R1 | Handoff A.8.1 vs the gerber netlist | **Resolved: upstream.** PAD1 and IC1 pin 6 are one net |
| Shield "never grounded" vs "grounded" | 2026-09-01 verbal report vs 2026-09-06 meter | **Resolved.** It was partly grounded and discontinuous — neither document was right |
| DAC loss startup-only vs recurring | Jacob's recollection vs the 2026-08-31 log | **Unresolved.** The 30-minute idle test settles it |

---

## 12. What this instrument is most and least understood

**Most confident:** the controller board. Every net, every pin, every component position is known
from the manufacturing netlist, cross-checked against the schematic and against `docs/WIRING.md`,
and it all agrees. The firmware is small and fully read. The preamp board's netlist is extracted.

**Least confident:** anything involving **actual displacement**. Every nanometre figure in this
document rests on Berard's calibration of a *different* disc scanner. Nothing about our own
scanner's travel, linearity, hysteresis or creep has ever been measured, and it cannot be until
the preamp works and a first image exists.

**Newly solid as of this audit:** the mechanical *dimensions*. Every printed part has been
measured off its mesh, the fastener scheme is fully known, and the two shielded enclosures are no
longer confusable. That is dimensions, not calibration — knowing a plate is 10.00 mm thick says
nothing about how far the scanner moves per volt.

**The gap between them is the project.** The electronics are characterised; the mechanics are
dimensioned but not calibrated; the instrument has never produced a measurement of its own
geometry.
