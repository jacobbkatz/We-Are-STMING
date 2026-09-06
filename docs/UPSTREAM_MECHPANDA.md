# Notes from Mech Panda's repository and the controller schematic

Findings from a file-by-file review of [`MechRedPanda/red-panda-stm`](https://github.com/MechRedPanda/red-panda-stm)
and from the controller schematic already sitting in our own `PCB/` directory, 2026-09-05.

**This is the design we are building.** Where `UPSTREAM_BERARD.md` is background, this is the
source. Our firmware differs from his in three places only: `play_tone()`, the ADC SPI clock drop
to 1 MHz, and the `TONE` command in `main.cpp`. `stm_control.py`, `stm_app.py` and
`EfficientStepper.cpp` are byte-identical to his.

---

## 1. The ADC full scale is 4.096 V, not 10.24 V

**This closes the question that made every current figure in the project ambiguous.**

The schematic in `PCB/PDF_Scanning Tunneling Microscope_2023-11-04.zip` was readable all along.
Page 2 is the ADC sheet. What it shows:

| Evidence | Source |
|---|---|
| U15 is an **LTC2326HMS-16** with pins **REFIN (8)** and **REFBUF (7)** | Schematic page 2 |
| **No external voltage reference is connected to the ADC.** The strings "VREF1" and "ADR421" appear **zero times** on the ADC sheet | Searched the extracted page text |
| The board's only reference IC, **U5 ADR421**, drives net **VREF1**, which goes to pin 4 (VREFIN) of the four AD5761 DACs and nowhere else | Schematic page 1 |
| Berard's driver declares `const float _ref_buffer_volts = 4.096f` — named after the **REFBUF pin** on this exact chip | `lib/LTC2326/LTC2326_16.hpp` |
| Probing R23 on 2026-08-31 gave ~2.5 V against ~15000–18000 counts, implying a full scale near 4–5 V | `sessions/2026-08-31-results.md` §3.8 |

So the ADC runs on its **own internal reference**, and 4.096 V is the figure the original author
attached to it.

**Where 10.24 came from is unknown.** It appears only in our PC-side tools
(`stm_control.py:37`, `stm_console.py`), never in the firmware, and it does not correspond to
anything on this schematic. Most likely copied from a different ADC in another design.

> **Status: strongly supported, not yet formally proven.** The remaining step is to confirm from
> the LTC2326-16 datasheet how the full-scale input range relates to REFBUF, and to take one
> simultaneous meter reading at R23 against `ADCR`. Until then, treat currents computed from
> 10.24 as **2.5× too large**.

**Nothing has been changed in the Python tools yet.** Changing the constant would silently alter
every number those tools print, and the change should land with the calibration that proves it.

## 2. `read_volts()` is broken. Do not use it.

```cpp
float LTC2326_16::read_volts()
{
    int16_t val = read();
    return val * _ref_buffer_volts;     // multiplies COUNTS by 4.096
}
```

This should divide by full scale, not multiply. As written, a full-scale reading of 32767 returns
"134213 volts". **It is never called anywhere in the firmware**, so it has done no harm, but it is
a trap for anyone who reaches for it. Present identically in our copy and upstream.

## 3. Two files are explicitly MIT licensed, with headers intact

The repository as a whole carries **no licence** (see `STATUS.md`), but two files inside it do:

| File | Author | Licence |
|---|---|---|
| `Code/teensy/lib/LTC2326/LTC2326_16.hpp` | Daniel Berard, dated Oct 14 2015 | Full MIT text in the header |
| `Code/teensy/src/logTable.hpp` | Daniel Berard, same date | Berard's copyright header |

**Our copies retain both notices**, which is what MIT requires of a modified copy — we changed the
SPI clock in `LTC2326_16.hpp` and left the header alone. Checked, not assumed.

`logTable.hpp` even carries the MATLAB that generated it:

```matlab
x  = 0:32768;
lt = round(log(x+1)*(2^19-1)/log(2^15+1))';
```

0–32768 in, 0–524287 out. That is a 20-bit log table indexed by the absolute value of a 16-bit
ADC reading — which independently confirms that `logTable[abs(adc)]` is correct by construction.
**Do not "fix" it.**

## 4. ALERT really is unrouted — now documented, not inferred

The project has been treating "the DAC ALERT pins do not reach the Teensy" as an inference. The
schematic settles it. Page 3 lists every net on the H1 ribbon header:

```
ADC_CNV  ADC_BUSY  ADC_SDI  ADC_SCK  ADC_SDO
SCLK  SDI  SYNC1  SYNC2  SYNC3  SYNC4
```

Eleven signals, no ALERT among them. U1–U4 pin 1 (ALERT#) goes to R1–R4 and LED1–LED4 only.

**LED1–LED4 are the only indication of the DAC configuration loss, confirmed from the schematic.**

## 4b. CLEAR#, RESET# and LDAC# are marked no-connect on all four DACs

Read off the schematic symbols on page 1. Every AD5761 carries a green no-connect cross on:

| Pin | Name | |
|---|---|---|
| 2 | **CLEAR#** | active-low, floating |
| 3 | **RESET#** | active-low, floating |
| 10 | SDO | confirms there is no DAC readback, consistent with H1 having no MISO |
| 11 | LDAC# | active-low, floating. The firmware uses `CMD_WR_UPDATE_DAC_REG`, which updates directly, so LDAC is not needed |
| 9 | DNC | correct, this pin is do-not-connect |

**This is the leading hypothesis for the DAC configuration loss.** A floating active-low CMOS
input can be pulled low by coupled noise, and four of them in the same environment would glitch
together — which is precisely the observed symptom. See `STATUS.md` fault 4.

**Unverified:** whether the AD5761R has internal pull-ups on CLEAR# and RESET#. Nobody has read
the datasheet on this point, and if it does, the hypothesis weakens considerably.

## 5. The ADC input stage, newly documented

**Corrected 2026-09-06 against the netlist.** The earlier sketch below had R24 on the minus line
and drew one RC per side. Both are wrong. The real topology, pad by pad from
`FlyingProbeTesting.json`:

```
                      C27 3.3nF
                  +-------||-------+
                  |                |
PREAMP+ --R23 470--+--R24 470--+---+--> U21 pin 3 (+IN A)
                              |    |
                        C28 3.3nF  +--> U21 pins 1,2 tied  = follower out = ADC IN+ (U15 pin 4)
                              |
                             AGND

                      C29 3.3nF
                  +-------||-------+
                  |                |
PREAMP- --R25 470--+--R26 470--+---+--> U21 pin 5 (+IN B)
                              |    |
                        C30 3.3nF  +--> U21 pins 6,7 tied  = follower out = ADC IN- (U15 pin 5)
                              |
                             AGND
```

- **R23 and R24 are both on the plus line; R25 and R26 are both on the minus line.** All four are
  470 R, C27–C30 are 3.3 nF.
- **C27 and C29 do not go to ground.** They return to the op-amp *output*. With the follower
  (U21 pins 1–2 tied, and 6–7 tied) that makes each side a **second-order Sallen-Key low-pass**,
  not a single RC.
- **f₀ = 1 / (2π × 470 Ω × 3.3 nF) = 103 kHz**, and with equal Rs and Cs **Q = 0.5** — overdamped,
  no peaking, rolling off at **40 dB per decade** above the corner rather than 20. The corner
  frequency is what the older note said; the rolloff is twice as steep as it claimed, which is
  what actually matters for aliasing.
- **The buffers have gain exactly 1** (output tied to the inverting input). Confirmed from the
  netlist, and it matters: it means the only gain in the current chain is the preamp's 100 MΩ.
- **U21 is an LT1469IN8**, a dual op-amp buffering the differential pair. This matches Berard's
  description of taking a differential measurement to reject noise picked up in the preamp cable.
- **U21 runs on ±15 V while the ADC runs on 5 V and 3.3 V.** The buffer can therefore present far
  more than the ADC's ±4.096 V input span if the preamp output ever swings hard. Nothing in
  between limits it. **VERIFY the LTC2326-16's absolute-maximum input against the datasheet
  before deliberately driving the preamp to its rails** — a railed preamp is a real state here,
  it is what the 2026-08-31 session saw.
- **R29 is a 10 k pull-up to 3.3 V on ADC_SDI**, which is the LTC2326's **RDL/SDI** pin.
- **R28 is 100 R in series on ADC_SDO.**

## 6. The ADC driver's chip-select looks inverted

```cpp
SPI1.beginTransaction(_spi_settings);
digitalWrite(_cs, HIGH);       // <- normally you would assert LOW here
val = SPI1.transfer16(0x00);
digitalWrite(_cs, LOW);
```

Chip selects are conventionally active-low, so this reads backwards. It is also the pin
`main.cpp` hands to `SPI1.setCS(38)`, so hardware and manual control touch the same pin, and it
carries the 10 k pull-up from section 5.

**Stage 4 passes and the ADC returns sensible data, so whatever this is, it works.** Recorded as
an observation, not a bug.

> **Do not "correct" this without a scope on the pin.** This project has already lost time to
> confident fixes of things that were not broken.

Neither driver ever calls `endTransaction()` — already known for `AD5761`, now confirmed for
`LTC2326` too. Harmless while nothing else shares either bus.

## 7. Upstream has no BOM

Mech Panda's README lists **"Add BOM List"** under Future Work, and `README_ZH.md` ends with
`TODO: 增加 BOM 表` — "TODO: add BOM table".

So `docs/BOM.md` is **our own work**, reconstructed from the JLCPCB assembly file, photographed
labels and CAD metadata. Worth knowing both for what we can claim as ours, and because it means
no upstream BOM exists to check ours against.

## 8. The CAD names the approach screw

`CAD/STM.f3z` is a zip. Its `DesignDescription.json` names the four referenced components:

```
MOTOR MODEL 28BYJ-48 5V v4 v1
ScanHead_97424A590_Ultra-Fine-Thread Plastic-Head Thumb Screw
ScanStage
98625A960_0.438 Long Brass Insert
```

**The 1/4"-80 screw is explicitly a scan head part**, and the 28BYJ-48 sits in the same assembly.
That is the basis of the ~7.8 nm/step figure in `docs/UPSTREAM_BERARD.md` §2 confirmed from the
design file rather than assumed from the BOM.

The lever ratio itself is still **VERIFY** — the geometry is inside the `.f3d` files, which are a
proprietary binary format this review could not read.

## 9. Schematic values that confirm existing documentation

Checked against `docs/WIRING.md`, all agree — no corrections needed:

- Output stage: R5, R7, R8, R10–R13, R15, R17, R18, R21, R22 = **3 k**; R6, R9, R14, R19 = **220 R**
- Bias path: R30 3k, R31 3k, R32 220 R, C48 4.7 nF, through U13.1 (OPA2227P)
- DSUB1 carries AGND plus Z+X, Z−X, Z+Y, Z−Y. DSUB2 carries BIAS, PREAMP±, ±15 V, AGND
- U19 is a **B3B-XH-AM** JST XH 3-pin taking V++, AGND, V--
- U5 ADR421: VIN = pin 2, VOUT = pin 6, feeding VREF1 to all four DAC pin 4s
- Regulators U16 BD733L5FP (3.3 V), U17 SL7815 (+15 V), U18 L7915CV (−15 V), U22 MC7805CDTG (5 V)
- LED5 via R27 10k, LED6 via R33 10k, on V++ and V-- respectively

Only **U13.1** is used; the second half of that OPA2227P is spare.

---

## How to read the schematic yourself

The PDF's text is vector-outlined, so most tools extract nothing. PyMuPDF works:

```bash
pip install pymupdf
python3 -c "
import pymupdf
d = pymupdf.open('SCH_Controller_2023-11-04.pdf')
for i, page in enumerate(d):
    print('=== PAGE', i+1, '==='); print(page.get_text())
"
```

Page 1 is DACs and the output stage, page 2 the ADC, page 3 connectors and power.
