# Canonical facts

**One value per fact. Everything else in this repository points here rather than restating it.**

This file exists because the same number kept being written into a dozen documents, and when it
turned out to be wrong only some of them got fixed. On 2026-09-07 the ADC full scale was corrected
from 4.096 V to 10.24 V and the preamp offset from 37 nA to 119 nA — **and stale copies of both
survived in a dozen files.**

## Rules

1. **If a number is in this table, do not restate it elsewhere. Link here.**
2. **When a value changes, change it here first**, then run `python3 Code/pc/check_facts.py`.
3. **Retired values are kept below, not deleted.** The checker uses that list to find stale copies.
4. Session logs are **history** and keep their original numbers. The checker skips them.

## Provenance marks

`MEAS` measured on our hardware · `DS` manufacturer datasheet · `DS-SIB` sibling part's datasheet ·
`CALC` calculated, derivation shown · `NETLIST` from a manufacturing file · `MESH` from a CAD mesh ·
`INFER` several pieces of evidence agree · `UNVERIFIED` not established

---

## Measurement chain

| Fact | Value | Prov | Date | Where it came from |
|---|---|---|---|---|
| ADC input full scale | **±10.24 V** | DS | 2026-09-07 | LTC2326-16. Span = 2.5 × REFBUF |
| ADC REFBUF | **4.096 V** | DS | 2026-09-07 | Onboard buffer, 2 × the 2.048 V bandgap. **Not the input span** |
| ADC volts per count | **0.3125 mV** | CALC | 2026-09-07 | 10.24 / 32768 |
| ADC output format | **two's complement** | DS | 2026-09-07 | |
| ADC input topology | **pseudo-differential** | DS | 2026-09-07 | |
| **ADC IN− allowed range** | **±500 mV of GND** | DS | 2026-09-07 | **Ours sits at ~2.7 V — out of spec** |
| ADC absolute max IN+/IN− | ±16.5 V | DS-SIB | 2026-09-07 | From the LTC2326-18. **Not confirmed for our part** |
| Preamp transimpedance | **100 MΩ** | DS | — | Air-wired, IC1 pin 2 to pin 6 |
| Counts per nA | **320** | CALC | 2026-09-07 | 0.1 V / 0.3125 mV |
| **Max measurable current** | **102.4 nA** | CALC | 2026-09-07 | 10.24 V / 100 MΩ |
| **Present input offset** | **~119 nA** | MEAS | 2026-09-07 | PAD1 = 11.905 V, R23 = 11.914 V |
| Offset on 2026-08-31 | ~119 nA | CALC | 2026-09-07 | 29,873 counts rescaled. **It never changed** |
| ADC front-end filter | 103 kHz, Q 0.5, 2nd order | CALC | 2026-09-06 | Sallen-Key, 470 Ω and 3.3 nF |
| ADC front-end gain | **exactly 1** | NETLIST | 2026-09-06 | U21 outputs tied to inverting inputs |
| **TIA bandwidth** | **~5 kHz** | CALC | 2026-09-07 | 1/(2π·100 MΩ·0.3 pF). **The real limit, not the filter** |

## DACs and drive

| Fact | Value | Prov | Date | Notes |
|---|---|---|---|---|
| Z range | **±10 V** | DS+MEAS | — | Mode bits `000` |
| X, Y, bias range | **±3 V** | DS+MEAS | — | Mode bits `101`. Firmware comments say ±5 V and are **wrong** |
| Z volts per count | 0.305 mV | CALC | — | 20 V / 65536 |
| X/Y volts per count | 0.0916 mV | CALC | — | 6 V / 65536 |
| DAC power-on output | **zero scale**, not 0 V | DS | — | Z at −10 V, X/Y/bias at −3 V |
| Summing stage gain | **−1 per input** | NETLIST | — | DSUB1 carries −(Z±X), −(Z±Y) |
| Worst-case summed output | **±13 V** on ±15 V rails | CALC | 2026-09-07 | Why X/Y are ±3 V and cannot be raised |
| Z clamp in const-current | counts 10000–50000 = −6.95 to +5.26 V | CALC | — | Keeps the summer in range by accident |
| SPI clock | **1 MHz** | — | — | The **ribbon** is the limit; the AD5761R accepts 50 MHz (DS) |
| AD5761R RESET, LDAC | **internal pull-ups, may float** | DS | 2026-09-07 | Kills the floating-pin hypothesis |
| Bias path gain | **−1**, verified | MEAS | 2026-08-31 | `BIAS 65535` → +3.000 V DAC, −3 V at the holder |

## Mechanical

| Fact | Value | Prov | Date |
|---|---|---|---|
| Fine screw thread | **1/4"-80**, 0.31750 mm/turn | DS | — |
| Fine screw length | **~30 mm longer than the CAD part** | Jacob | 2026-09-07 |
| Motor steps per revolution | **2048** | — | — |
| Lever ratio | **20, 30 or 40 — unresolved.** CAD geometry suggests 40 | MESH | 2026-09-07 |
| nm per motor step | **3.88 / 5.17 / 7.75** for ratio 40 / 30 / 20 | CALC | 2026-09-07 |
| Plate-to-plate screws | **M3**, Ø3.200 clear into Ø2.500 self-tap | MESH | 2026-09-06 |
| Preamp box screws | **M2**, Ø2.300 clear into Ø1.600 self-tap | MESH | 2026-09-06 |
| Preamp board | **20.625 × 15.230 mm**, holes 5.93 mm apart | NETLIST | 2026-09-06 |
| Piezo disc seat in `PiezoPlate` | **Ø20.500 × 3.00 mm deep** over Ø18.000 | MESH | 2026-09-06 |
| Piezo disc in the BOM | **25–27 mm brass** | BOM | — |
| **Disc vs seat** | **CONFLICT — a 25–27 mm disc does not fit a 20.5 mm seat** | — | 2026-09-06 |
| Print material | **PETG-CF** | Jacob | 2026-09-07 |
| Scanner displacement | ~34 nm/V in Z, ~83 nm/V in XY | INFER | — | **Berard's disc, not ours** |

## Retired values — the checker looks for these

**If you find one of these outside a session log, it is stale. Fix it.**

| Retired | Replaced by | When | Why |
|---|---|---|---|
| `37 nA` as the preamp offset | **119 nA** | 2026-09-07 | Derived from ADC counts with the wrong full scale |
| `3.73 V` / `3.734 V` as the preamp output | **11.905 V** | 2026-09-07 | Same cause |
| `4.096` as the **ADC full scale** | **10.24 V** | 2026-09-07 | 4.096 is REFBUF. Span is 2.5 × REFBUF |
| `0.125 mV` per count | **0.3125 mV** | 2026-09-07 | Same cause |
| `800 counts` per nA | **320 counts** | 2026-09-07 | Same cause |
| `40.96 nA` as the measurable ceiling | **102.4 nA** | 2026-09-07 | Same cause |
| `91%` as the **ADC range consumed** | **116% — off the top of the scale** | 2026-09-07 | Same cause |
| `25 single-pad nets` | **34** | 2026-09-06 | Recount |
| `McMaster 97424A590` as **our** fine screw | unknown, ~30 mm longer | 2026-09-07 | That is Mech Panda's CAD part |
| `±5 V` as the **X and Y range** | **±3 V** | 2026-08-31 | Firmware comments are wrong |
| `244 nm` as the **motor step** | **3.88–7.75 nm** | 2026-09-05 | Old estimate |

> **`4.096` is still correct as REFBUF and as the driver constant `_ref_buffer_volts`.** The checker
> only flags it when it appears near the words "full scale". Same for the retired screw part number,
> which is legitimately named when describing Mech Panda's design.
