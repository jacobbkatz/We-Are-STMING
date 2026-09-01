# Current status

**Last updated:** 2026-08-31, end of session 3
**Updated by:** Jacob

> This file is the single source of truth for where the build is right now.
> It is rewritten at the end of every work session. If anything else in the repo
> disagrees with this file, **this file wins** — see `CLAUDE.md` for the full rule.

---

## Where we are in one line

Stages 0 through 5 pass and the bias path passes. **The preamplifier is the blocker**, and it
is being rebuilt on the spare board because of cyanoacrylate contamination.

---

## Stage table

| Stage | Status | Notes |
|---|---|---|
| 0 Continuity | PASS | |
| 1 Serial, `GSTS` | PASS | |
| 2 Motor | PASS | |
| 3 Analog rails | PASS | LED5 and LED6 lit |
| 4 DACs and ADC | PASS | |
| 5 Piezo drive | PASS | −10 V at the scan head for `DACZ 65535` |
| Bias path to sample | PASS | −3 V at the sample holder for `BIAS 65535`, gain −1 as per schematic |
| 6 Preamp | **FAIL** | 37 nA input leakage. Rebuild in progress |
| DAC config stability | **FAIL** | All four DACs drop config roughly hourly |
| JP1 grounds | **FAIL** | One ground pin genuinely open on the old board |

---

## Open faults

### 1. Preamp — 37 nA input leakage (the blocker)

The feedback loop is **closed**, not open. It settles rather than ramping, which is the whole
diagnosis. The fault is cyanoacrylate contamination: CA blooms while curing and deposited a
conductive haze over the whole board, including the input node.

37 nA has eaten 91% of the ADC range, leaving 3.6 nA of headroom. A tunneling current is about
1 nA, so there is nowhere to put it.

- **Decision taken:** rebuild on the spare board.
- **IPA will not fix it.** Cured CA needs acetone or a nitromethane debonder, neither of which is
  attractive around an air-wired node.
- **Rebuild rules and the acceptance test** are in `sessions/2026-08-31-results.md` section 6.
- **Acceptance test:** `python adc_stats.py -n 50 -i 9.0 --tag "new preamp, undisturbed"`,
  bench clear, nobody within a metre, ten minutes. Settling near 0 counts means fixed.
  Settling near 29873 again means it was never contamination and we rethink.

### 2. DACs lose configuration roughly hourly

All four go at once. LED1–LED4 light. Every DAC output goes dead. `RSET` restores it.

**Software cannot detect this.** The ALERT pins go to the LEDs and nowhere else, they are not
wired to the Teensy, and there is no DAC readback because H1 carries no MISO for the DAC bus.
`GSTS` will happily report `dac_z = 65535` while the chip outputs nothing — the status fields are
firmware bookkeeping, not measurements.

> **Rule: look at LED1–LED4 immediately before and immediately after every measurement.
> Any reading taken with one lit is void.** This cost an hour on 2026-08-31.

Cause unknown. U16 was checked and is not hot, which weakens the thermal-shutdown theory.

### 3. One JP1 ground pin is open

Measured empirically on 2026-08-31: two pins wander when only one should. The handoff document
retracted this finding once; **the retraction was wrong.**

**Do not run a wire to fix it.** If the pin numbering is mirrored, the pin we are calling ground
could physically be −15 V, and bonding it to ground shorts a supply rail. The board is being
rebuilt anyway, so this resolves itself.

---

## Next actions, in order

1. **Finish the preamp rebuild** and run the acceptance test above. This gates everything else.
2. **Characterise the DAC config loss.** Suggested experiment: `RSET`, confirm LED1–4 dark, then
   leave the board completely alone for 30 minutes with no commands sent and check the LEDs again.
   That separates "activity triggers it" from "time or the rail triggers it".
3. **Calibrate counts to amps.** Simultaneous meter reading at R23 and `ADCR`, bench clear, two
   well-separated points. Settles the 4.096 vs 10.24 question below.
4. **Dummy junction test.** A resistor between 1 MΩ and 100 MΩ clipped between the sample holder
   and the tip holder. Proves the whole current path with no tip and no crash risk, gives counts
   per amp directly, and **tells us the sign of the current**.
5. **Write `Code/pc/stm_approach.py`.** A PC-side stepping loop, abortable with Ctrl-C, with the
   threshold on absolute deviation from baseline rather than a signed comparison. Not yet written.

---

## Standing safety rules — do not violate these

1. **Check LED1–LED4 before and after every measurement.** No software substitute exists.
2. **Do not run `APRH`** until the sign of the tunneling current is known. `approach()` tests
   `read_adc() > target` against a baseline that has been negative all project, so if tunneling
   drives the reading more negative it will never trigger and the tip will drive into the sample.
3. **Do not raise either SPI clock above 1 MHz.** Both buses were at 40 MHz and the ribbon cannot
   carry it.
4. **Do not run a wire between JP1 pins** on the old board.
5. **Do not use cyanoacrylate** anywhere near the preamp, or in the same enclosure, ever.
6. **Park Z at midscale (32768) before moving the motor.** `RSET` and `TEST` both slam Z to a
   rail, so re-park after either.
7. **No preamp measurement is valid while anyone is leaning over the board.** A person within a
   metre injects 20 to 50 nA, which is twenty to fifty times a tunneling current.

---

## Open questions

| Question | Why it matters |
|---|---|
| Is there a sample material? HOPG, gold on mica, anything | You cannot image without one. Nothing in the project has confirmed we have one |
| How far does one motor step move the tip, in nm? | One step must move less than the Z piezo range or an approach is a crash regardless of the electronics |
| Which Z direction is toward the sample | Only resolvable at first tunneling, or from the CAD. Park Z at midscale meanwhile |
| ADC full scale: 4.096 or 10.24 V? | `LTC2326_16.hpp` says 4.096, `stm_control.py:37` and `stm_console.py` say 10.24. The R23 reading favours 4.096. Every current figure depends on this |
| DST-201 DC input impedance | Needed to finish some of the high-impedance arithmetic |

---

## Known code issues, deliberately not fixed yet

| Where | Issue |
|---|---|
| `stm_firmware.hpp` `approach()` | Signed `>` comparison against a negative baseline. Route around it with a PC-side loop instead. Fix once the current sign is known |
| `stm_control.py:37`, `stm_console.py` | ADC full scale hardcoded as `10.24`. Evidence favours 4.096 but it is not a calibration yet |
| `stm_firmware.hpp` | Duplicate `LTC2326_16` object at file scope and as a class member, same pins |
| `AD5761.cpp` `write()` | Missing `SPI.endTransaction()` |

`logTable[abs(adc)]` is **safe** — the table is `[32769]`. Do not "fix" it.
