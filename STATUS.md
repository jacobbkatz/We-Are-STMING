# Current status

**Last updated:** 2026-09-05
**Updated by:** Jacob (remote, no bench work)

> This file is the single source of truth for where the build is right now.
> It is rewritten at the end of every work session. If anything else in the repo
> disagrees with this file, **this file wins** — see `CLAUDE.md` for the full rule.

---

## Where we are in one line

Stages 0 through 5 pass and the bias path passes. **The preamplifier is the blocker.** There are
now **three candidate causes** for its 37 nA offset — cyanoacrylate contamination, an ungrounded
case shield, and flux residue — and all three are surface conduction into the input node. The
cheapest test has not been run yet: **ground the shield and retest before rebuilding the board.**

Two unfixed firmware faults were found on 2026-09-05 that will damage a tip if hit: **`CCON` snaps
Z to midscale**, and **the motor is left energised** and heats the scan head.

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
| 6 Preamp | **FAIL** | 37 nA input leakage. Two candidate causes, see below |
| Preamp case shielding | **FAIL** | Copper and aluminium tape, never bonded to ground |
| DAC config stability | **FAIL** | All four DACs drop config roughly hourly |
| JP1 grounds | **FAIL** | One ground pin genuinely open on the old board |

---

## Open faults

### 1. Preamp — 37 nA input leakage (the blocker)

**The feedback loop is closed, not open.** It settles rather than ramping, and that is the whole
diagnosis — an amplifier with an open feedback resistor behaves as an integrator and would have
pinned against 32767 within two minutes. Do not let any older document tell you otherwise.

37 nA has eaten 91% of the ADC range, leaving 3.6 nA of headroom. A tunneling current is about
1 nA, so there is nowhere to put it. **The offset is the problem, not the noise** — noise measured
0.78 nA RMS with the bench clear, which would not block an approach.

**Two candidate causes. Nothing measured so far distinguishes them.**

| Candidate | Found | Status |
|---|---|---|
| **A. Cyanoacrylate contamination.** CA blooms while curing and deposited a conductive haze over the whole board, input node included | 2026-08-31 | Live. Fix is a rebuild on the spare board |
| **B. The case shield is floating.** Copper and aluminium tape on the preamp box, never bonded to ground | 2026-09-01 | Live, and **untested** |
| **C. Flux residue.** Berard independently reports "huge leakage currents" from flux left on this exact circuit | 2026-09-05 | Live. Addressed by the existing rebuild clean, but not excluded on the current board |

**Test B first.** Grounding the shield is one wire and is reversible; the rebuild consumes the
spare board and is not. And critically: **if B is the cause, a rebuild will not fix it**, because
the new board goes back into the same ungrounded box.

- **IPA will not remove cured CA.** It needs acetone or a nitromethane debonder, neither
  attractive around an air-wired node.
- **Rebuild rules** are in `sessions/2026-08-31-results.md` section 6.
- **Acceptance test**, used for either fix:
  `python adc_stats.py -n 50 -i 9.0 --tag "<what changed>"`, bench clear, nobody within a metre,
  ten minutes. Settling near 0 counts means fixed. A few thousand counts means a large
  improvement with some residual leakage. Settling near 29873 again means that candidate was not
  the cause. Ramping to a rail means a genuinely open feedback path, which would be a build error.

### 1b. Preamp case shielding was never grounded

The preamp enclosure is shielded with copper tape and aluminium tape, and **the shielding was
never bonded to ground.**

Two mechanisms, both **inference and needing test**, not established fact:

- **Galvanic cell.** Copper and aluminium in contact, with humidity as the electrolyte, form a
  real galvanic couple — a few hundred millivolts of DC sitting on the enclosure at no defined
  potential. To drive 37 nA, 0.5 to 1 V needs a path of roughly 13 to 27 MΩ, which is entirely
  plausible for a contaminated surface. That is arithmetic, not a measurement.
- **Floating shield.** An ungrounded conductive enclosure couples capacitively to everything
  around it with no fixed reference. **A floating shield can be worse than no shield.**

**Rules for fixing it:**

1. Bond the shield to circuit ground **at one point only.** Multiple bonds around an enclosure
   create a ground loop and trade one noise problem for another.
2. **Solder the ground wire to the copper tape.** Aluminium tape cannot be soldered.
3. **Do not leave copper and aluminium tape in contact.** `docs/START_HERE_gotchas.md` already
   says they are not interchangeable because of solderability; this is a second, independent
   reason.
4. Aluminium tape adhesive is usually non-conductive, so **overlapping strips may not connect at
   all.** Check continuity across the shield with a meter rather than assuming it.

### 2. `CCON` jumps Z to midscale and will crash a tip

**Found 2026-09-05 by cross-referencing Dan Berard's write-up against our source. Not yet fixed.**

`turn_on_const_current()` assigns `dac_z_control_value = stm_status.dac_z` and **nothing ever reads
it.** `control_current()` computes `int z = (pTerm + iTerm) + 32768` with midscale hardcoded, so
the first call after `CCON` drives Z to roughly 32768 **wherever Z actually was.**

From Z = 15000 that is a ~17000-count step, roughly **180 nm toward the sample** using Berard's
34 nm/V disc figure. Tunneling happens under 1 nm. Berard documents this exact failure on his own
build: *"the feedback will cause a small jump in the Z-piezo when it's switched on, which crashes
the tip!"*

> **Rule until fixed: never send `CCON` with a tip in tunneling range.** Expect Z to snap to
> midscale on engage.

**Fix, not applied and not bench-tested:** seed `iTerm = stm_status.dac_z - 32768` in
`turn_on_const_current()`, so the loop's first output equals the current Z. See
`docs/UPSTREAM_BERARD.md` §1.1.

### 3. The stepper motor is left energised, which heats the scan head

**Found 2026-09-05, same source. Not yet fixed.**

`EfficientStepper::step()` calls `enable()` and never disables afterwards. `disable()` is called in
exactly one place — inside `approach()`, on success only. After any `MTMV` the motor sits powered
and warming.

Berard: *"The motor produces a substantial amount of heat, which can cause the scanner to drift out
of range within minutes."* The 28BYJ-48 is geared and holds position without holding current, which
is why a geared motor was chosen in the first place.

**Prime suspect if drift ever appears minutes into a session.** Fix is to call `disable()` at the
end of `step()`. Not applied, needs bench testing.

### 4. DACs lose configuration roughly hourly

All four go at once. LED1–LED4 light. Every DAC output goes dead. `RSET` restores it.

**Software cannot detect this.** The ALERT pins go to the LEDs and nowhere else, they are not
wired to the Teensy, and there is no DAC readback because H1 carries no MISO for the DAC bus.
`GSTS` will happily report `dac_z = 65535` while the chip outputs nothing — the status fields are
firmware bookkeeping, not measurements.

> **Rule: look at LED1–LED4 immediately before and immediately after every measurement.
> Any reading taken with one lit is void.** This cost an hour on 2026-08-31.

Cause unknown. U16 was checked and is not hot, which weakens the thermal-shutdown theory.

> **Do not "fix" this with a periodic `RSET` on a timer.** `AD5761::reset()` sends a full software
> reset, and `STM::reset()` rebuilds the status struct, so a timed `RSET` also **slams Z to a
> rail**, zeroes the bias, and zeroes the step counter. With the tip engaged that is a scheduled
> tip crash.
>
> The safer stopgap, if one is wanted, is to **re-arm rather than reset**: write `CMD_WR_CTRL_REG`
> with the channel's range, then re-send the last commanded value from `stm_status`. That restores
> state instead of destroying it. **Not yet written.**
>
> Neither approach **detects** anything, and neither helps mid-scan. The real fix is wiring the
> AD5761 ALERT pins to spare Teensy GPIOs so the firmware can see the fault at all.

### 5. One JP1 ground pin is open

Measured empirically on 2026-08-31: two pins wander when only one should. The handoff document
retracted this finding once; **the retraction was wrong.**

**Do not run a wire to fix it.** If the pin numbering is mirrored, the pin we are calling ground
could physically be −15 V, and bonding it to ground shorts a supply rail.

This was previously filed as "resolves itself when the board is rebuilt". **That is no longer
safe to assume**, since the rebuild is now deferred behind the shield test. If the shield fix
solves the offset and the old board stays in service, this open ground still needs resolving —
by establishing the pin numbering first, not by running a speculative wire.

---

## Next actions, in order

1. **Ground the preamp case shield and retest, before rebuilding anything.** One wire, reversible,
   and it tells the two candidate causes apart without consuming the spare board. Meter-check the
   shield's continuity and whether copper and aluminium are in contact anywhere while you are there.
2. **Then rebuild the preamp if it is still bad**, and run the same acceptance test.
3. **Characterise the DAC config loss.** Suggested experiment: `RSET`, confirm LED1–4 dark, then
   leave the board completely alone for 30 minutes with no commands sent and check the LEDs again.
   That separates "activity triggers it" from "time or the rail triggers it".
4. **Calibrate counts to amps.** Simultaneous meter reading at R23 and `ADCR`, bench clear, two
   well-separated points. Settles the 4.096 vs 10.24 question below.
5. **Dummy junction test.** A resistor between 1 MΩ and 100 MΩ clipped between the sample holder
   and the tip holder. Proves the whole current path with no tip and no crash risk, gives counts
   per amp directly, and **tells us the sign of the current**.
6. ~~**Write `Code/pc/stm_approach.py`.**~~ **Written 2026-09-05.** PC-side woodpecker loop,
   Ctrl-C abortable, thresholds on absolute deviation so the current's sign does not matter. Never
   sends `APRH`. 40 tests pass against a simulated microscope. **Never run on hardware yet**, and
   it refuses to start while the preamp is railed. It also requires the two direction answers
   below before it will run at all.

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
   Mount with screws or nylon standoffs first, 2-part epoxy second, foam tape third.
6. **Park Z at midscale (32768) before moving the motor.** `RSET` and `TEST` both slam Z to a
   rail, so re-park after either.
7. **Never send `CCON` with a tip in tunneling range** until the integral-init bug in fault 2 is
   fixed. Engaging the loop snaps Z to midscale.
8. **No preamp measurement is valid while anyone is leaning over the board.** A person within a
   metre injects 20 to 50 nA, which is twenty to fifty times a tunneling current.

---

## Open questions

The full register, including the undocumented hardware and process items, is in
[`docs/OPEN_QUESTIONS.md`](docs/OPEN_QUESTIONS.md). The ones blocking work right now:

| Question | Why it matters |
|---|---|
| Is the 37 nA the CA contamination or the floating shield? | Decides whether the spare board gets consumed |
| Is the DAC configuration loss startup-only, or does it recur mid-session? | 2026-08-31 recorded it recurring every 30 to 60 minutes, which requires checking LED1–LED4 around every measurement. If it is startup-only, one `RSET` at the start is enough. **Currently ambiguous, needs settling at the bench** |
| ~~Is there a sample material?~~ | **Answered 2026-09-05: gold foil.** It must be mounted flat on a magnetic disc with a conductive path to the bias magnet — see `docs/UPSTREAM_BERARD.md` §5. Expect atomic terraces, not individual atoms; Berard could not resolve single atoms on metals |
| How far does one motor step move the tip, in nm? | **Largely answered 2026-09-05: about 7.8 nm**, from the 1/4"-80 pitch, 2048 steps/rev, and a ~20x lever reduction. **VERIFY our lever ratio** — 20 is Berard's geometry, ours is Mech Panda's. Even with no lever, 155 nm/step against a ~700 nm Z range works. This replaces the old 244 nm estimate and removes the crash-margin worry. See `docs/UPSTREAM_BERARD.md` §2 |
| Which Z direction is toward the sample | Only resolvable at first tunneling, or from the CAD. Park Z at midscale meanwhile. **`stm_approach.py` requires this answer before it will run** |
| Which sign of `MTMV` advances toward the sample | Determinable by eye with the tip removed. **`stm_approach.py` requires this too** |
| ADC full scale: 4.096 or 10.24 V? | `LTC2326_16.hpp` says 4.096, `stm_control.py:37` and `stm_console.py` say 10.24. The R23 reading favours 4.096. Every current figure depends on this |
| DST-201 DC input impedance | Needed to finish some of the high-impedance arithmetic |

---

## Known code issues, deliberately not fixed yet

| Where | Issue |
|---|---|
| `stm_firmware.hpp` `approach()` | Signed `>` comparison against a negative baseline. **Routed around** — use `Code/pc/stm_approach.py`, which never sends `APRH`. Left unfixed deliberately |
| `stm_control.py:37`, `stm_console.py` | ADC full scale hardcoded as `10.24`. Evidence favours 4.096 but it is not a calibration yet |
| `stm_firmware.hpp` | Duplicate `LTC2326_16` object at file scope and as a class member, same pins |
| `AD5761.cpp` `write()` | Missing `SPI.endTransaction()` |
| `stm_firmware.hpp:497-498` | Comments say X and Y are ±5 V. They are **±3 V** — same mode bits as bias, which measures ±3 V. Comment only, the behaviour is correct |

`logTable[abs(adc)]` is **safe** — the table is `[32769]`. Do not "fix" it.
