# Component and datasheet reference

**Built 2026-09-07.** Every part in the electronics stack, with the specifications that actually
matter for this instrument — not just links.

**How to use this file.** It exists so a future session can answer "what voltage can this pin
take", "is this op-amp stable", "could the Teensy damage this input" **without searching from
scratch**. If you find yourself about to look up a part, look here first. If the answer is not
here, add it when you find it.

## Confidence marks used below

| Mark | Means |
|---|---|
| **[DS]** | Read from the manufacturer datasheet. Quoted or closely paraphrased |
| **[DS-SIB]** | From a sibling part's datasheet in the same family. Strongly indicative, **not** confirmed for our exact part |
| **[MEAS]** | Measured on our hardware |
| **[CALC]** | Calculated from [DS] or [MEAS] values. The calculation is shown |
| **[UNVERIFIED]** | Not established. What is missing, and how to get it, is stated |

> **Network note.** This session could not fetch PDFs — `analog.com`, `farnell.com`, `digikey.*`
> and `ti.com` are all blocked by the egress proxy. Everything marked [DS] came through search
> result summaries of the manufacturer datasheet. **Where a number would change a decision, it is
> marked and the gap is named.** A session with unrestricted network should re-verify the [DS-SIB]
> and [UNVERIFIED] rows first.

---

## 1. The signal chain at a glance

```
tip ── 40 AWG wire ── OPA627AU TIA, 100 MΩ ── JP1.3 ── DSUB2.3 (PREAMP+) ─┐
                                              DSUB2.2 (PREAMP-) ──────────┤ FLOATING. FAULT
                                                                          │
   R23 470 ─ R24 470 ─┬─ U21.3 ──┬─ U15 IN+ (pin 4)                       │
                    C27,C28      └─ U21.1,2 tied = unity follower         │
   R25 470 ─ R26 470 ─┬─ U21.5 ──┬─ U15 IN- (pin 5)  ◄────────────────────┘
                    C29,C30      └─ U21.6,7 tied = unity follower
                                     LTC2326-16, ±10.24 V, two's complement
```

**Total gain from tip current to ADC input: 100 MΩ and nothing else.** Both buffers are unity.
Confirmed two ways — from the netlist (outputs tied to inverting inputs) and by measurement (PAD1
11.905 V, R23 11.914 V, a 9 mV difference across the whole chain). [MEAS]

---

## 2. U1–U4 — AD5761RBRUZ, 16-bit DACs (X, Y, Z, bias)

Analog Devices. TSSOP-16. `AD5761R/AD5721R` datasheet, Rev. C.

| Spec | Value | Ours | Mark |
|---|---|---|---|
| VDD (positive analog) | **4.75 V to 30 V** | +15 V | [DS] |
| VSS (negative analog) | **−16.5 V to 0 V** | −15 V | [DS] |
| Absolute max, VDD to VSS | **−0.3 V to +34 V** | 30 V. **4 V of margin** | [DS] |
| VLOGIC | 3.3 V from U16 | 3.3 V | netlist |
| **SCLK maximum** | **50 MHz** | **run at 1 MHz** | [DS] |
| Data clocked in on | **falling edge of SCLK** | `SPI_MODE2` = CPOL 1, CPHA 0 → samples on the first (falling) edge. **Correct** | [DS] + code |
| Internal reference | 2.5 V | used. `VREF1` net reaches all four pin 4s | [DS] + netlist |
| Power-on / reset output | **zero scale**, CV = 00 and PV = 00 | Z sits at −10 V, X/Y/bias at −3 V | [DS] + `docs/DAC_BOOT_STATE.md` |

### The floating-pin question — ANSWERED 2026-09-07, and it changes a hypothesis

**`RESET` has an internal pull-up and may be left floating.** [DS]
**`LDAC` has an internal pull-up and may be left floating.** [DS]

The netlist shows U1–U4 pins 2, 3, 9, 10 and 11 unconnected — 20 single-pad nets. **That is by
design and the datasheet permits it.**

> **This substantially weakens `STATUS.md` fault 4's leading hypothesis.** "CLEAR#/RESET# are
> floating and glitch together" required those pins to be genuinely undriven. They are internally
> pulled up. **The proposed two-wire fix onto ribbon pins 24/26 is very likely unnecessary.**
>
> `docs/PROJECT_HANDOFF_SUMMARY.md` lines 476–495 already explains the symptom completely as a
> **power-sequencing** problem: USB boots the Teensy, `setup()` writes DAC config into unpowered
> chips, the writes go nowhere. Nuh's 2026-09-07 data fits it exactly — lit at **every** power-on,
> cleared by `RSET`, and **not** triggered by 30 minutes of idle.
>
> **[UNVERIFIED]: whether `CLR` specifically also has an internal pull-up.** Searches returned
> RESET and LDAC explicitly but not CLR. **Fastest check:** the AD5761R pin-function table, one
> page. It does not change the conclusion above, which rests on the power-sequencing evidence.

### Output range bits RA[2:0]

| Bits | Range | Used for |
|---|---|---|
| `000` | ±10 V | Z |
| `010` | ±5 V | not used |
| `101` | **±3 V** | X, Y, bias |

Decode from `docs/soft_launch_test_procedure.md` §2. **±3 V confirmed by measurement** — `BIAS 65535`
commands +3.000 V and reads −3 V at the sample holder through the −1 stage. [MEAS]
**The firmware comments at `stm_firmware.hpp:497-498` say ±5 V for X and Y and are wrong.**

---

## 3. U15 — LTC2326HMS-16, 16-bit ADC

Analog Devices (Linear). MSOP-16. **This part caused the project's largest single error.**

| Spec | Value | Mark |
|---|---|---|
| **Analog input range** | **±10.24 V true bipolar** | [DS] |
| **REFBUF** | **4.096 V**, from an onboard buffer gaining the 2.048 V bandgap by 2 | [DS] |
| **Relationship** | **input span = 2.5 × REFBUF** | [DS] |
| **Output format** | **two's complement** | [DS] |
| Input topology | **pseudo-differential** | [DS] |
| **IN− allowed range** | **±500 mV with respect to GND** | [DS] |
| IN+ range | IN+ − IN− within ±2.5 × VREFBUF | [DS] |
| Absolute max IN+/IN− | **−16.5 V to +16.5 V** | **[DS-SIB]** — from the LTC2326-18 |
| Supplies | 5 V analog (pin 2), 3.3 V I/O (pin 15) | netlist |
| Resolution | 16 bit, 250 ksps, 93.5 dB SNR | [DS] |

### The two things this settles

**1. Volts per count is 0.3125 mV, not 0.125 mV.** 10.24 / 32768. `_ref_buffer_volts = 4.096f` in
the driver is the **REFBUF** voltage, exactly as its name says — **not** the input span.
`stm_control.py` and `stm_console.py` use 10.24 and **are correct. Do not change them.**

**2. `PREAMP−` floating at ~2.7 V is a specification violation, not merely an inconvenience.**
IN− must stay **within ±500 mV of GND**. Ours sits at about **2.7 V** — **five times outside the
allowed range**. Every ADC reading this project has taken was made with the converter operated
outside its specified input conditions.

> **Consequence for the plan.** Bonding `PREAMP−` to ground **fixes a spec violation** and is
> supported by the numbers: it would put 11.9 V on IN+, which is over the ±10.24 V full scale — so
> the reading will **pin at 32767**, which is the expected and correct outcome — but well inside the
> **±16.5 V absolute maximum [DS-SIB]**. **Damage is unlikely.**
>
> **[UNVERIFIED]: the LTC2326-**16**'s own absolute maximum table, verbatim.** Every host is
> blocked. **Fastest check:** one page of the datasheet from an unrestricted machine. **The plan is
> arranged so this never gates anything** — the preamp rebuild is validated with a meter at PAD1,
> and by the time the bond is made PAD1 should be under 0.1 V.

### Driver notes

- `SPISettings(1000000, MSBFIRST, SPI_MODE2)` on SPI1. **[UNVERIFIED]** against the datasheet's
  required SPI mode, but it demonstrably returns sane data.
- `read()` returns `int16_t` — **correct, now that two's complement is confirmed.** [DS]
- `read_adc_raw()` **does** wait on BUSY, with a 1 ms timeout. Verified in source.
- **The chip-select polarity looks inverted** (driven HIGH before the transfer, LOW after). The pin
  is `RDL/SDI`, not a conventional CS. `docs/PROJECT_HANDOFF_SUMMARY.md` says explicitly
  **"Do not change the RDL polarity in `LTC2326_16.cpp`. It is correct as written."** Leave it.
- `read_volts()` is **broken and never called** — it multiplies counts by REFBUF. Do not use it.

---

## 4. IC1 — OPA627AU, the transimpedance amplifier

Texas Instruments (Burr-Brown). SOIC-8. **The most important part in the instrument.**

| Spec | Value | Mark |
|---|---|---|
| **Input bias current** | **~1 pA** | [DS] |
| Gain-bandwidth product | **16 MHz** | [DS] |
| Slew rate | 55 V/µs | [DS] |
| Supply range | **±4.5 V to ±18 V** | [DS] |
| Our supply | **±15 V** — inside range. Board nets are *named* `+9V`/`−9V`, see `docs/WIRING.md` §10 | netlist |
| Output swing on ±15 V | approx ±13 V | **[UNVERIFIED]** — see below |

### What the 119 nA means against this part

**The OPA627's own input bias current is about 1 pA. Our measured input current is 119 nA.**
That is **119,000 times** the amplifier's own contribution. [CALC]

**Nothing about the op-amp explains it.** The leakage is external to the device — surface
conduction on the board, at the PTFE standoff, or through the enclosure. This is the single
strongest argument that the fault is contamination and not a damaged or wrong part.

### Stability of the TIA — analysed, and it is marginal by accident

A transimpedance amplifier is stable when the feedback capacitance satisfies
`C_f ≥ √(C_in / (2π · R_f · GBW))`.

| Term | Value |
|---|---|
| R_f | 100 MΩ [DS/BOM] |
| GBW | 16 MHz [DS] |
| C_in (op-amp + stray, tip lead removed) | ~20 pF **[UNVERIFIED estimate]** |
| **Required C_f** | **≥ 0.045 pF** [CALC] |
| **Actual C_f** | **none fitted.** Only the resistor's own stray, typically 0.1–0.5 pF | design |

> **The circuit is stable only because of the feedback resistor's stray capacitance. There is no
> deliberate compensation capacitor.** It has enough margin at ~0.3 pF, but this is worth knowing:
> **do not "tidy" the feedback resistor by shortening its leads or laying it flat on the board.**
> Air-mounting it is what keeps stray capacitance predictable, and it is also what keeps the input
> node off the board surface.

**Resulting bandwidth:** `f = 1/(2π · R_f · C_f)` = **~5 kHz** at 0.3 pF. [CALC]
That is the real bandwidth of the current measurement, and it is far below the ADC front end's
103 kHz. **The TIA is the bandwidth limit, not the filter.**

**Noise gain peaking:** at high frequency the noise gain is `1 + C_in/C_f` ≈ **67**. [CALC]
The OPA627's ~5 nV/√Hz becomes ~335 nV/√Hz at the output over that band.

### Noise budget — and a number that does not add up

| Source | Contribution at the output | Mark |
|---|---|---|
| Johnson noise of the 100 MΩ, 12.9 fA/√Hz over ~8 kHz | **~0.12 mV RMS** | [CALC] |
| OPA627 voltage noise × noise gain 67 over ~5 kHz | **~0.02 mV RMS** | [CALC] |
| **Measured, 2026-08-31** | **623 counts × 0.3125 mV = 195 mV RMS** | [MEAS] |

**The measured noise is about 1,700 times the resistor's thermal floor and roughly 10,000 times
the op-amp's contribution.** Neither device explains it.

> **New hypothesis from this audit: the "noise" may not be the preamp at all — it may be the
> floating `PREAMP−` reference wandering.** A node with no defined impedance, sitting 2.7 V outside
> the converter's allowed input range, is exactly the kind of thing that produces large slow
> wander. **This also fits the hour-long warm-up drift.**
>
> **This is testable and costs nothing:** take a noise capture with a meter on PAD1 instead of
> through the ADC. If PAD1 is quiet while the ADC counts scatter by 600, the noise is the reference.
> **If that is confirmed, every noise figure in this project is void**, including the "shield nearly
> halved the noise" observation.

---

## 5. U9, U10, U13 — OPA2227P, dual op-amps

Texas Instruments. PDIP-8. Pinout, all three identical:
`1 = OUT A, 2 = −IN A, 3 = +IN A, 4 = V−, 5 = +IN B, 6 = −IN B, 7 = OUT B, 8 = V+`

| Role | Where |
|---|---|
| **U9** | Z±X output stage. Channel B is an inverting summer, gain −1 per input; channel A a difference amp |
| **U10** | Z±Y, identical |
| **U13** | Channel A is the **bias buffer** to the sample. **Channel B is entirely unconnected** — fault 4b |

**Supply: ±15 V.** Output swing on ±15 V: approximately ±13 V. **[UNVERIFIED]** — searches did not
return the swing table. **Fastest check:** the OPA2227 datasheet's output voltage swing spec at
±15 V with a 10 kΩ load. **It matters** — see the headroom note below.

### Headroom — why X and Y are ±3 V and cannot simply be raised

The summing stage adds Z and X into one output, so the worst case is the sum:

| | |
|---|---|
| Z full scale | ±10 V [DS/measured] |
| X (or Y) full scale | ±3 V [DS/measured] |
| **Worst-case summed output** | **±13 V** [CALC] |
| Supply rails | ±15 V |

**At simultaneous full-scale Z and X the summing amplifier sits at the edge of its output swing.**
That is almost certainly *why* X and Y are ±3 V: at ±5 V the sum would be 15 V and would clip.
**Raising the X/Y range means checking this first.**

**Closed-loop scanning is safe by accident:** `control_current()` clamps Z to counts 10000–50000,
which is **−6.95 V to +5.26 V**, so the worst sum during a scan is about 9.95 V. Only a hand-typed
`DACZ` reaches the limit. [CALC from source]

### U13 channel B — a real defect

Pins 5, 6, 7 connect to nothing. **An op-amp channel with floating inputs can drift to a rail or
oscillate, and it shares a die and both supply pins with the bias buffer next to it.** The same
package is wired correctly on U9 and U10, where channel B's `+IN` is tied to AGND — which is the
evidence this is an oversight rather than a choice.

**Fix: two wires — pin 6 to pin 7, and pin 5 to AGND.** Makes it a unity-gain follower at 0 V.
**Test: one scope probe on pin 7.** A quiet DC level is fine; a rail or an oscillation is not.

---

## 6. U21 — LT1469IN8, ADC input buffers

Analog Devices (Linear). PDIP-8. Dual op-amp, **both channels used as unity-gain followers**
(outputs tied to inverting inputs — confirmed from the netlist).

**Supply: ±15 V, while the ADC it drives runs on 5 V.** Nothing between them limits the swing.
That is how 11.9 V reached a ±10.24 V converter. **The protection is the ADC's own ±16.5 V
absolute maximum [DS-SIB], not anything in our design.**

---

## 7. U5 — ADR421BRZ, precision voltage reference

Analog Devices. SOIC-8. Output on the `VREF1` net, reaching **U1–U4 pin 4** and decoupled by C54.
**Measured 2.5 V at C54.** [MEAS]

Pins 1, 3, 5, 7, 8 are unconnected — trim and no-connect pins, correctly unused. [netlist]

---

## 8. Power tree

| Ref | Part | In | Out | Feeds |
|---|---|---|---|---|
| U19 | B3B-XH-AM, JST XH 3-pin | **V++ / AGND / V--** | — | the board's only power input |
| U17 | SL7815, TO-220 | V++ | **+15 V** | analog |
| U18 | L7915CV, TO-220 | V-- | **−15 V** | analog |
| U16 | BD733L5FP-CE2, TO-252 | V++ | **3.3 V** | DAC VLOGIC, ADC I/O |
| U22 | MC7805CDTG, DPAK | V++ | **5 V** | ADC analog supply |

**Feed ±18 V, not ±15 V** — the regulators need headroom. A single-output bench supply cannot do
this; use two channels with the junction as ground.

> **The two TO-220 regulators have different pin orders and that is correct**, not an error.
> U17: pad 1 = V++ in, 2 = AGND, 3 = +15 V out. U18: pad 1 = AGND, 2 = V-- in, 3 = −15 V out.

> **Asymmetry worth knowing: V++ feeds three regulators, V-- feeds only U18.** So the positive
> input rail carries roughly three times the load. This matters for the rail-scaling test —
> dropping V++ affects the digital supplies as well as the analog one, while dropping V-- affects
> only the −15 V rail.

**Measured dropout on U18: 0.74 V.** At a 13.91 V input the −15 V rail fell to −13.171 V. [MEAS]

---

## 9. Passives that matter, and why they are there

| Ref | Value | Purpose |
|---|---|---|
| R5, R7, R8, R10–R13, R15, R17, R18, R21, R22 | **3 kΩ** | Summing/difference network. Equal in and feedback gives gain exactly −1 |
| **R6, R9, R14, R19** | **220 Ω** | In series into DSUB1. **These are stability isolation resistors, not just protection.** An op-amp driving a ~15 nF piezo directly is a classic oscillator; the series resistor is the standard cure. RC = 3.3 µs → 48 kHz, far above any scan rate [CALC] |
| R23, R24 (plus line), R25, R26 (minus line) | **470 Ω** | Sallen-Key anti-alias into the ADC |
| C27, C29 | **3.3 nF** | **Return to the op-amp OUTPUT**, not ground — this is what makes it 2nd order |
| C28, C30 | **3.3 nF** | To AGND |
| R30, R31 | 3 kΩ | Bias buffer, gain −1. C48 4.7 nF across R31 |
| R32 | 220 Ω | Series into DSUB2 pin 1 |
| R1–R4 | 10 kΩ | LED1–4 from 3.3 V to U1–U4 pin 1 (ALERT) |
| R28 | 100 Ω | Series damping on ADC_SDO |
| R29 | 10 kΩ | Pull-up to 3.3 V on ADC_SDI (RDL) |
| **Preamp R1** | — | **NOT the feedback resistor.** It sits between the op-amp output and JP1 pin 3. The 100 MΩ feedback is air-wired between IC1 pin 2 and pin 6 |

**ADC front-end filter, calculated:** f₀ = 1/(2π × 470 Ω × 3.3 nF) = **103 kHz**, **Q = 0.5**
(overdamped), rolling off at **40 dB/decade**. [CALC]

**Decoupling:** 25 × 100 nF and 14 × 10 µF are fitted across the board. Not individually audited
against each IC's pins. **[UNVERIFIED]** — low priority; nothing observed suggests a decoupling
problem.

---

## 10. Connectors — pinouts and signal direction

### H1, 26-pin ribbon, Teensy ↔ controller

Odd pins 1–25 are **all AGND**. Signals on even pins:

| H1 | Teensy | Net | Direction |
|---|---|---|---|
| 2 | 19 | ADC_CNV | Teensy → board |
| 4 | 18 | ADC_BUSY | board → Teensy |
| 6 | — | ADC_SDI (RDL) | Teensy → board |
| 8 | 27 | ADC_SCK | Teensy → board |
| 10 | 39 | ADC_SDO | **board → Teensy** |
| 12 | 13 | SCLK | Teensy → board |
| 14 | 11 | SDI | Teensy → board |
| 16 | 10 | SYNC4 — U4, **bias** | Teensy → board |
| 18 | 9 | SYNC2 — U2, **Y** | Teensy → board |
| 20 | 8 | SYNC3 — U3, **Z** | Teensy → board |
| 22 | 7 | SYNC1 — U1, **X** | Teensy → board |
| **24, 26** | — | **unconnected — two spare conductors** | — |

> **Note the `#define` order trap in `stm_firmware.hpp`:** the defines run 7, 8, 9, 10 but are
> named DAC_1, DAC_**3**, DAC_**2**, DAC_4. **Pin 8 is Z and pin 9 is Y**, not the other way round.

**There is no MISO on the DAC bus.** Teensy pin 12 is not wired to the ribbon, so **the DACs cannot
be read back.** `GSTS` reports firmware bookkeeping, never the chips.

### DSUB1 — scanner, 9-way

| Pin | Net | Direction |
|---|---|---|
| 1–5 | AGND | — |
| 6 | Z−Y | board → piezo |
| 7 | Z+Y | board → piezo |
| 8 | Z−X | board → piezo |
| 9 | Z+X | board → piezo |
| **shell** | **NET_1/NET_2 — floating** | nothing bonds it to AGND |

### DSUB2 — preamp, 9-way

| Pin | Net | Direction |
|---|---|---|
| 1 | BIAS | board → sample holder |
| 2 | **PREAMP−** | preamp → board. **CURRENTLY FLOATING — the fault** |
| 3 | PREAMP+ | preamp → board |
| 4 | **−15 V** | board → preamp |
| 5 | **+15 V** | board → preamp |
| 6–9 | AGND | — |
| **shell** | **NET_3/NET_4 — floating** | nothing bonds it to AGND |

> **±15 V and the high-impedance signal share one 9-way connector and one cable.** Worth knowing
> when hunting noise.

### JP1 — preamp board, 5-pin

`1 = GND, 2 = +supply, 3 = OUTPUT, 4 = GND, 5 = −supply`

**Pin 4 is GND in the netlist but has no copper routed to it on either layer.** A routing defect,
not a build fault. **This is very likely the source of the floating `PREAMP−`.**

**Orientation rule:** the layout is asymmetric — the negative supply is at the end of the row.

---

## 11. Teensy 4.1 — PJRC, NXP i.MX RT1062

| Spec | Value | Mark |
|---|---|---|
| **GPIO logic level** | **3.3 V. NOT 5 V tolerant** | [DS] |
| **Driving any pin above 3.3 V** | **permanent damage** | [DS] |
| Recommended output current | **4 mA per pin** | [DS] |
| Analog inputs | 0 to 3.3 V only, **no pin may exceed 3.3 V** | [DS] |
| SPI buses | SPI (DACs) and SPI1 (ADC), configured in `setup()` | code |
| SPI1 pins | SCK 27, CS 38, MISO 39 | code |
| USB power | **boots the Teensy the instant USB is connected**, independent of the analog supply | [DS] + handoff |

### Voltage compatibility — audited, and it is clean

**Every signal reaching the Teensy is 3.3 V or lower:**

- The DACs' VLOGIC and the ADC's I/O supply are both **3.3 V** from U16. [netlist]
- **`ADC_SDO` is the only board → Teensy signal**, and it comes from U15's 3.3 V I/O rail. [netlist]
- `ADC_BUSY` likewise. [netlist]
- The ULN2003 stepper driver takes 3.3 V logic in from the Teensy and its outputs go to the motor,
  **never back to the Teensy**. [design]
- **No 5 V or ±15 V node has a path to a Teensy pin** anywhere in the netlist. **Verified.**

> **The one way to break this is miswiring the motor driver.** The ULN2003 module has a 5 V supply
> pin adjacent to its input pins. **Meter before connecting** — 5 V onto a Teensy GPIO destroys it.

### The power-on behaviour that explains the DAC fault

**USB boots the Teensy in milliseconds. `setup()` runs `stm.reset()` immediately, writing DAC
configuration.** If the analog supply is off at that moment the DACs are unpowered and **those
writes go nowhere**. Switch the analog supply on afterwards and the DACs come up unconfigured with
ALERT asserted and LED1–4 lit. **`setup()` never runs again** — cycling the analog supply does not
reboot the Teensy because USB keeps it alive.

**This is documented in full in `docs/PROJECT_HANDOFF_SUMMARY.md` lines 476–495**, under the
heading "THE OPERATING RULE THAT MATTERS MOST", with two fixes:

1. **Send `RSET` after powering up the analog supply.** Always works.
2. Power the analog supply on **before** connecting USB.

**Nuh's 2026-09-07 data confirms it**: LED1–4 lit at every power-on without exception, cleared by
`RSET`, and **not** triggered by 30 minutes of idle.

### Stepper

`EfficientStepper(STEPS_PER_REVOLUTION, IN1, IN3, IN2, IN4)` — **the pin order 1-3-2-4 is
deliberate**, it is the coil sequence the 28BYJ-48 needs. **Do not "correct" it to 1-2-3-4.**

Motor pins **33, 34, 35, 36 go directly to the ULN2003, not through the ribbon.**

---

## 12. What is still UNVERIFIED, ranked by how much it matters

| # | Unknown | Why it matters | Fastest way to close |
|---|---|---|---|
| 1 | **LTC2326-16 absolute maximum input, verbatim** | Decides whether bonding `PREAMP−` while PAD1 is at 11.9 V is safe | One datasheet page from an unrestricted machine. **[DS-SIB] says ±16.5 V, which gives good margin** |
| 2 | **OPA2227 output swing at ±15 V** | The Z+X headroom claim rests on ~±13 V | One datasheet page |
| 3 | **Preamp input capacitance C_in** | Sets TIA stability margin and noise gain. Estimated at 20 pF | Hard to measure directly; bound it by observing the step response |
| 4 | **Whether `CLR` has an internal pull-up** | Completeness only — the power-sequencing explanation already covers the symptom | One page of the AD5761R pin table |
| 5 | **LTC2326-16 required SPI mode** | The driver uses MODE2 and works | One datasheet page |
| 6 | **Per-IC decoupling audit** | Nothing suggests a problem | Cross-check the netlist against each IC's supply pins |

---

## 13. Sources

- [Analog Devices AD5761R product page](https://www.analog.com/en/products/ad5761r.html) and [AD5761R/AD5721R datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/ad5761r_5721r.pdf)
- [Analog Devices LTC2326-16 product page](https://www.analog.com/en/products/ltc2326-16.html) and [datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/232616fa.pdf)
- [Texas Instruments OPA627](https://www.ti.com/product/OPA627)
- [PJRC Teensy 4.1](https://www.pjrc.com/store/teensy41.html)
- [Analog Devices EngineerZone, LTC2326-16 input range](https://ez.analog.com/data_converters/precision_adcs/f/q-a/542689/ltc2326-16-8c93---only--5v-input)

**All were read through search summaries, not fetched directly** — see the network note at the top.
