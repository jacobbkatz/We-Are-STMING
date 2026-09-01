# Wiring and pinout reference

Everything here is **verified** — cross-checked against the firmware source, the PCB netlist, or
measured at the bench. Nothing on this page is assumed.

Extracted from `PROJECT_HANDOFF_SUMMARY.md` A.4 so it can be used at the bench without scrolling
a 1900-line document. **Corrections from later sessions are already applied here** — where this
page and the handoff differ, this page is right.

---

## 1. Connector names — read this first

The documents, the silkscreen, and ordinary conversation use different names for the same
connectors. This caused repeated confusion.

| Called | Silkscreen | Board | What it is | Where |
|---|---|---|---|---|
| J1 | **DSUB1** | Controller | DB9 to scan head / piezo | bottom **left** |
| J2 | **DSUB2** | Controller | DB9 to preamp | bottom **right** |
| JP1 | JP1 | **Preamp board** | 5-pin header, ±15 V in, signal out | separate PCB |
| — | **H1** | Controller | 26-pin ribbon to Teensy | top **left** |
| — | **U19** | Controller | 3-pin JST XH, **power input** | **right edge** |
| JP2 | — | — | **Does not exist anywhere in this project** | — |

> **Power goes into U19, the JST XH.** The ±15 V pins on DSUB2 are **outputs** to the preamp.
> Feeding a supply into them pushes voltage backwards into regulator outputs.
> Input should be roughly **±18 V**, not ±15 V, or the regulators drop out.

---

## 2. Teensy 4.1 pin assignments

From the firmware source, `stm_firmware.hpp`.

| Teensy pin | Signal | Goes to |
|---|---|---|
| 7 | SYNC1 | U1, **X** DAC chip select |
| 8 | SYNC3 | U3, **Z** DAC chip select |
| 9 | SYNC2 | U2, **Y** DAC chip select |
| 10 | SYNC4 | U4, **bias** DAC chip select |
| 11 | SDI (MOSI) | SPI data, **all four DACs** |
| 13 | SCLK | SPI clock, **all four DACs**. Also the onboard LED |
| 18 | ADC_BUSY | conversion status, input |
| 19 | ADC_CNV | start conversion |
| 27 | ADC_SCK | SPI1 clock |
| 38 | ADC_SDI / **RDL** | ADC read-enable, effectively chip select |
| 39 | ADC_SDO | SPI1 data in |
| 33, 34, 35, 36 | IN1–IN4 | ULN2003 motor driver, **direct, not via the ribbon** |

Pins 8 and 9 are deliberately "swapped" relative to axis order. **That is correct — do not fix it.**

`SERIAL_LED 0` and `TUNNEL_LED 1` are defined in the source but **never used anywhere.**

### Motor wiring

Wire it straight across: **33→IN1, 34→IN2, 35→IN3, 36→IN4.**

Sources online will tell you a 28BYJ-48 needs its coils driven 1-3-2-4. That is true, and **the
firmware already does it** — `EfficientStepper(steps, IN1, IN3, IN2, IN4)` performs the swap in
software. Swap the wires too and the two swaps cancel; the motor buzzes instead of turning.

---

## 3. H1 ribbon pinout, 26-pin

| Teensy | H1 pin | Net | Purpose |
|---|---|---|---|
| 19 | 2 | ADC_CNV | start conversion |
| 18 | 4 | ADC_BUSY | conversion status |
| 38 | **6** | ADC_SDI | LTC2326 **RDL read-enable** |
| 27 | 8 | ADC_SCK | SPI1 clock |
| 39 | 10 | ADC_SDO | SPI1 data in |
| **13** | 12 | SCLK | SPI clock, all four DACs |
| **11** | 14 | SDI | SPI data, all four DACs |
| 10 | 16 | SYNC4 | U4, bias |
| 9 | 18 | SYNC2 | U2, Y |
| 8 | 20 | SYNC3 | U3, Z |
| 7 | 22 | SYNC1 | U1, X |
| — | 1, 3, 5 … 23, 25 | AGND | all 13 odd pins |
| — | **24, 26** | — | **unconnected by design** |

**Pin 6 does get connected.** It is labelled ADC_SDI, which sounds like a data input a read-only
ADC would not need. On this chip it is **RDL**, a read-enable. It was left disconnected at first
and that was wrong.

> **There is no MISO on the DAC bus.** Teensy pin 12 is not wired to the ribbon and H1 carries no
> DAC data-return line. **The DACs can never be read back.** This is why a DAC that has lost its
> configuration is invisible to software, and why LED1–LED4 are the only indicator.

**Easy rule, avoids counting pins:** on H1 the odd pins are all ground, the even pins are signals.

---

## 4. DAC identity and ranges

| Chip | Net | SYNC | Teensy | Axis | Range bits | **Range** |
|---|---|---|---|---|---|---|
| U1 | XOUT | SYNC1 | 7 | X | `101` | **±3 V** |
| U2 | YOUT | SYNC2 | 9 | Y | `101` | **±3 V** |
| U3 | ZOUT | SYNC3 | 8 | Z | `000` | **±10 V** |
| U4 | SAMPLE | SYNC4 | 10 | bias | `101` | **±3 V** |

DAC codes run 0 to 65535, with **32768 = 0 V**.

> **The firmware comments are wrong about X and Y.** `stm_firmware.hpp:497-498` says −5 to +5 V.
> X, Y and bias all use identical mode bits, so they cannot have different ranges, and bias
> measures ±3 V. Confirmed by measurement, not only by reading the bits. The comment is wrong;
> the behaviour is correct.

**VREF1 measures exactly 2.5 V** across C54. U5 sources it and is powered from +15 V.

---

## 5. Controller board LEDs

| LED | Fed from | Through | Sinks into | Means |
|---|---|---|---|---|
| LED1 | 3.3 V | R1 | U1 pin 1 | **X DAC ALERT asserted** |
| LED2 | 3.3 V | R2 | U2 pin 1 | **Y DAC ALERT asserted** |
| LED3 | 3.3 V | R3 | U3 pin 1 | **Z DAC ALERT asserted** |
| LED4 | 3.3 V | R4 | U4 pin 1 | **bias DAC ALERT asserted** |
| LED5 | V++ | R27 | AGND | positive input rail present |
| LED6 | AGND | R33 | V-- | negative input rail present |

> **LED1–4 dark means the DACs are configured and working. Lit means they are dead.**
> This is the single most useful indicator on the board, and the only way to detect a
> configuration loss. **Check them before and after every measurement** — a reading taken with
> any of them lit is void.

---

## 6. DB9 cable colours

Standard JUXINICE DB9-male-to-bare-wire cable:

| DB9 pin | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| Colour | Black | Brown | Red | Orange | Yellow | Green | Blue | Grey | White |

> **The same colour means completely different things on the two cables.** Orange is −15 V on the
> preamp cable and plain ground on the scan head cable. Check which cable you are holding.

### DSUB2 — to the preamp

| Colour | Pin | Function |
|---|---|---|
| Black | 1 | BIAS |
| Brown | 2 | PREAMP− |
| Red | 3 | PREAMP+ |
| **Orange** | 4 | **−15 V** |
| **Yellow** | 5 | **+15 V** |
| Green, Blue, Grey, White | 6–9 | AGND |

### DSUB1 — to the scan head

| Colour | Pin | Function |
|---|---|---|
| Black, Brown, Red, Orange, Yellow | 1–5 | AGND |
| Green | 6 | Z−Y |
| Blue | 7 | Z+Y |
| Grey | 8 | Z−X |
| White | 9 | Z+X |

**Row rule, avoids pin counting:** on DSUB1 the row of 5 is all ground and the row of 4 carries
signal. On DSUB2 it is the opposite — the row of 5 carries signal and the row of 4 is all ground.

---

## 7. Power tree

| Ref | Part | Package | In | Out |
|---|---|---|---|---|
| **U19** | B3B-XH-AM | JST XH 3-pin | — | **power input:** pin 1 V--, pin 2 GND, pin 3 V++ |
| U17 | SL7815 | TO-220 | V++ | +15 V |
| U18 | L7915CV | TO-220 | V-- | −15 V |
| U16 | BD733L5FP-CE2 | TO-252 | V++ | 3.3 V |
| U22 | MC7805CDTG | DPAK | V++ | 5 V |

**The two TO-220 regulators have different pin orders. This is correct, not an error** — negative
regulators use a different pinout from positive ones.

- **U17:** pad 1 = V++ in, pad 2 = AGND, pad 3 = +15 V out
- **U18:** pad 1 = AGND, pad 2 = V-- in, pad 3 = −15 V out

Feed **±18 V** into U19. A single-output bench supply cannot do this — you need two independently
adjustable channels, or two supplies stacked in series with the junction as ground.

---

## 8. Output stage

```
U3 (DAC Z) --ZOUT--> R8 --> U9 pin 6 --> U9 pin 7 --> R6 --> DSUB1 pin 9 (Z+X)
U1 (DAC X) --XOUT--> R7 -----^
```

- R5, R7, R8, R10, R11, R12, R13, R15, R17, R18, R21, R22 = **3 k**
- R6, R9, R14, R19 = **220 R**, in series into the DB9

U9 channel B has its non-inverting input tied to AGND, making it an **inverting summing amp with
gain exactly −1 per input**. A positive command produces a negative output. Channel A produces
Z−X as a difference amp. U10 does the same for the Y pair.

U9 and U10 pinout, identical: 1 = OUT A, 2 = −IN A, 3 = +IN A, 4 = −15 V, 5 = AGND (+IN B),
6 = −IN B, 7 = OUT B, 8 = +15 V.

### Bias path

```
U4 pin 7 --SAMPLE--> R30 (3k) --> U13 (OPA2227P) --> R32 (220R) --BIAS--> DSUB2 pin 1
                                    ^                                        |
                              R31 (3k) || C48 (4.7nF)            black wire, sample holder
```

**Verified 2026-08-31:** `BIAS 65535` commands +3.000 V at the DAC and measures **−3 V at the
sample holder**, confirming the path and the gain of −1. U13 supplies: pin 8 = +15 V, pin 4 = −15 V.

---

## 9. Board layout

Millimetres from the lower-left of the component area. Board is roughly 103 × 88 mm.

```
        LEFT                                              RIGHT
  y=72  .                    U16(54)      U22(73)      U19(91)  <- power JST in
  y=67  H1(17) ribbon
  y=63  .                                          LED5(88) LED6(92)
  y=52  .                                                   U18(91)  <- -15V reg
  y=43  U1(6)   U3(21)   U2(35)   U4(49)   U5(60)   <- four DACs + reference
  y=38  .                                                   U17(91)  <- +15V reg
  y=17  U9(14)          U10(37)           U13(63)   <- output op-amps
  y=0   DSUB1(18)                       DSUB2(74)
```

Both TO-220 regulators and the power input are on the **right edge**. The DACs run across the
middle. The −15 V rail crosses about 90 mm to reach U1.

---

## 10. Preamp board

**PAD1 is the amplifier output, not the tip input.** It is wired to the op-amp's pin 6. It is the
only obvious pad, it sits near the edge, and it looks exactly like where you would attach the tip.
Solder the tip there and the microscope will never see a tunneling current.

**The tip goes to an insulated standoff** pressed into a bare hole near the R2 silkscreen. The
100 MΩ resistor, the tip wire, and a link to the op-amp input all meet there in mid-air.

The R2 footprint has **no copper at all**, just bare drilled holes. That is deliberate — at picoamp
currents, leakage across the board surface would swallow the signal, so the input node is built in
the air instead.

**Ground the case shield**, at one point only. See `STATUS.md` — an ungrounded shield is currently
a leading suspect for the offset blocking the build.

---

## 11. Piezo element

18 mm copper/brass buzzer disc. Capacitance 15,000 pF ±30%. Working voltage 1.5–30 V.

Datasheet resonance is 8.6 ± 0.7 kHz, **but that is a free-air figure and does not apply once the
disc is mounted.** A sweep on 2026-08-31 from 1 kHz to 11 kHz found **no loudness peak anywhere** —
clamping at the rim and mass-loading by the tip holder damps that resonance out of existence.

**Do not judge the piezo by ear at any frequency. Use a meter.** `DACZ 65535` should give −10 V at
the scan head end of the DSUB1 cable, on the row-of-4 signal wires.

The four piezo quadrant wires are **identical bare enamelled copper with no colour code.** There
is no way to recover which quadrant is +X from any file or photo, so label them as you solder. If
your first image comes out rotated or mirrored, this is why, and it is fixable in software.
