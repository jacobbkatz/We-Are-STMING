# Current status

**Last updated:** 2026-09-06
**Updated by:** Nuh (bench, meter only — nothing was powered), then Jacob (remote, documentation)

> **Before recording anything here as unknown, read `CLAUDE.md` §3b and check `docs/INDEX.md`.**
> Four items in this file's history were marked unknown while the answer sat in a repository file.

> This file is the single source of truth for where the build is right now.
> It is rewritten at the end of every work session. If anything else in the repo
> disagrees with this file, **this file wins** — see `CLAUDE.md` for the full rule.

---

## Where we are in one line

Stages 0 through 5 pass and the bias path passes. **The preamplifier is the blocker.** Its 37 nA
offset has **two remaining candidate causes** — cyanoacrylate contamination and flux residue, both
surface conduction into the input node. The third, the case shield, has been **rebuilt** and is
about to be tested properly for the first time.

**On 2026-09-06 the shield was found to be discontinuous and only partly grounded**, which would
have made the planned shield test return a false negative and pushed us into consuming the spare
preamp board for nothing. It was stripped and rebuilt in all copper with soldered seams.
**The rebuild has not been verified with a meter yet — do that first.**

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
| **Preamp box** shielding | **REBUILT, unverified** | All copper, seams soldered, one ground wire, 2026-09-06. **Continuity not yet metered — VERIFY first thing** |
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

**Candidate causes. Nothing measured so far distinguishes them.**

| Candidate | Found | Status |
|---|---|---|
| **A. Cyanoacrylate contamination.** CA blooms while curing and deposited a conductive haze over the whole board, input node included | 2026-08-31 | Live. Fix is a rebuild on the spare board |
| **B. The case shield is floating.** | 2026-09-01 | **Shield rebuilt 2026-09-06**, all copper, seams soldered, one ground bond. Still **untested electrically** — the D1/D2/D3 captures have never been run |
| **C. Flux residue.** Berard independently reports "huge leakage currents" from flux left on this exact circuit | 2026-09-05 | Live. Addressed by the existing rebuild clean, but not excluded on the current board |

**Ranking them by impedance, added 2026-09-06.** For surface leakage to push current into the
preamp's input, that input is a **virtual ground**, so the current is set by whatever voltage sits
at the far end of the leakage path divided by its resistance:

| Source at the far end | Path resistance needed for 37 nA | Plausible for a surface path? |
|---|---|---|
| A ±15 V supply rail | **405 MOhm** | **Yes** — very typical of a contaminated surface |
| A 0.5 V galvanic cell on the shield | **13 MOhm** | Low. That is a poor insulator, not a contaminated one |

**This favours the contamination hypotheses (A and C) over the shield (B) as the DC offset
source.** It does not clear the shield — a floating shield is still a real noise problem and still
needs grounding — but the arithmetic says the offset more likely comes from a rail leaking to the
input node across a dirty surface.

**A cheap discriminating test follows:** if the offset is rail-to-input leakage, it should **scale
with the rail voltage**. Drop the supply from ±15 V to ±10 V and the offset should fall by about a
third. If it does not move, the source is not the rails.

**Still test B first.** The shield work is done and reversible; the rebuild consumes the spare
board and is not. And critically: **if B is the cause, a rebuild would not have fixed it**, because
the new board would have gone back into the same bad box. That box has now been rebuilt, so this
is at last a test that can give a clean answer — **provided the shield continuity is verified with
a meter first.**

- **IPA will not remove cured CA.** It needs acetone or a nitromethane debonder, neither
  attractive around an air-wired node.
- **Rebuild rules** are in `sessions/2026-08-31-results.md` section 6.
- **Acceptance test**, used for either fix:
  `python adc_stats.py -n 50 -i 9.0 --tag "<what changed>"`, bench clear, nobody within a metre,
  ten minutes. Settling near 0 counts means fixed. A few thousand counts means a large
  improvement with some residual leakage. Settling near 29873 again means that candidate was not
  the cause. Ramping to a rail means a genuinely open feedback path, which would be a build error.

### 1b. Preamp BOX shield — rebuilt 2026-09-06, continuity not yet verified

> ## THERE ARE TWO SEPARATE SHIELDS. DO NOT CONFUSE THEM.
>
> | | What it is | Status |
> |---|---|---|
> | **Preamp box shield** | `1_preamp_box` — **35 × 29 × 21 mm**, around the **preamp board only** (the board is 20.6 × 15.2 mm) | **Rebuilt 2026-09-06.** All copper, seams soldered, one ground wire. **Continuity NOT yet metered** |
> | **Scan head shield cover** | `6_shield_cover.stl` — **142 × 128 × 112 mm**, drops over the **whole scanning module**. Also wants copper tape and one ground bond | **Printed, wrapped in copper, and grounded.** Reported by Jacob, 2026-09-06. Not independently metered — if 60 Hz ever dominates an image, re-check this before assuming anything else |
>
> **Everywhere in this file, "the shield" means the PREAMP BOX** unless it says otherwise. The two
> carry the identical instruction — copper tape, grounded at one point — which is exactly why they
> get mixed up.
>
> **The sizes settle it:** 142 × 128 × 112 mm versus 35 × 29 × 21 mm. Measured from the STLs, in
> `CAD/prints/README.md`.
>
> Berard uses both: the preamp sits in its own box on the head, **and** a metal can goes over the
> whole instrument during scanning. He is explicit that without the outer one, *"the images
> produced by the STM are dominated by 60 Hz noise pickup"*.

**Metered on 2026-09-06. Both earlier descriptions of this were wrong.**

The shield was neither "floating" (as `sessions/2026-09-01.md` recorded from a verbal report and
never measured) nor grounded. It was **discontinuous and partially grounded**:

| Check, as found | Result |
|---|---|
| Continuity across the shield tape | **Beeps in places, open in others.** Not one conductor |
| Copper tape touching aluminium tape | **Yes, in many places** |
| Shield to circuit ground | **Beeps in places, not others** |

A ground wire had been added to the **outside** of the box **after 31 August** — late in a session,
to see whether the preamp might not need rebuilding — and was never written down. It grounded
whichever tape patches it reached; the rest stayed floating. Aluminium tape adhesive is an
insulator, which is the likely reason the overlaps did not conduct.

> **This would have produced a false negative.** Block D3 tests "ground the shield and re-measure",
> and a null result sends the project into consuming the only spare preamp board. With a
> discontinuous shield that test would really have been "one patch grounded", and could have read
> "no improvement" even if the floating shield were genuinely the cause.

**What was done, 2026-09-06:** aluminium tape stripped completely, box re-covered in **copper only**,
**seams soldered**, one ground wire attached. All on the outside of the box, so the air-wired
100 MOhm resistor and the IC1 pin 2 input node were never approached.

**The galvanic cell is now eliminated by construction** — there is no dissimilar metal left in the
assembly. It was never disproved; it was removed.

> **VERIFY BEFORE ANY OTHER PREAMP WORK.** The acceptance test was not run:
> **every point on the shield must beep to the ground wire** — near the wire, the far corner, and
> across every seam. Until that passes, a D3 result still means nothing.

**Rules that still apply:**

1. Bond the shield to circuit ground **at one point only.** Multiple bonds create a ground loop.
2. **Solder to copper.** Aluminium cannot be soldered, and a pressure contact on aluminium grows
   an insulating oxide skin and fails later.
3. **Do not reintroduce aluminium tape.** `docs/START_HERE_gotchas.md` says the two are not
   interchangeable because of solderability; the galvanic couple and the non-conducting overlaps
   are two further independent reasons.
4. **Never assume tape conducts to itself.** Check continuity across every seam with a meter.

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

### Leading hypothesis, found 2026-09-06: CLEAR# and RESET# are floating

**CONFIRMED from the manufacturing data.** The JLCPCB flying-probe test file
(`gerbers/Gerber_PCB1_all_red.zip`, `FlyingProbeTesting.json`) carries the full board netlist. Of
96 nets, **25 have only a single pad on them** — and twenty of those are U1–U4 pins 2, 3, 9, 10 and
11. CLEAR# and RESET# are connected to nothing at all, by design, on every DAC.

(The other five single-pad nets are U5's test-point, trim and not-internally-connected pins, which
are correctly unused.) Also
pin 11 (LDAC#) and pin 10 (SDO). Read off the symbols on schematic page 1 — every AD5761 carries
a green no-connect cross on those pins.

Those are **active-low control inputs**. Left floating, a CMOS input sits at an undefined
potential and can be driven low by nothing more than coupled noise. **Four floating RESET# pins in
the same noise environment would glitch together** — which is exactly the symptom: all four DACs
drop configuration simultaneously, ALERT lights, and `RSET` restores them.

This fits better than the rail-dip and thermal theories, neither of which explains why all four go
at once and nothing else on the 3.3 V rail is affected.

**Two things had to be checked before believing it. One is now done.**

1. **Does the AD5761R have internal pull-ups on CLEAR# and RESET#?** If it does, floating is far
   less dangerous and this hypothesis weakens a lot. **Datasheet question. STILL NOBODY HAS
   LOOKED. This is now the only thing gating the fix.**
2. ~~**Are they actually open on our board?**~~ **CONFIRMED AT THE BENCH 2026-09-06.** Continuity
   from each chip's own pin 15 (3.3 V) to pins 2 and 3: **all eight open, on all four DACs.** Two
   control measurements (U1 pin 15 to U3 pin 15, and U1 pin 5 to U1 pin 16) both beeped first, so
   these are genuine opens and not eight failed probe contacts. Three independent sources now
   agree: the schematic symbols, the manufacturing netlist, and the meter.

**If the datasheet answer is "no internal pull-ups", the fix is four short wires**: tie CLEAR# and
RESET# to 3.3 V on each DAC. Permanent, rather than the periodic re-arm workaround discussed below.

> **Do not solder those wires until the datasheet question is answered.** Everything about this
> hypothesis is now confirmed except the one fact that decides whether it matters.

Cause otherwise unknown. U16 was checked and is not hot, which weakens the thermal-shutdown theory.
**Confirmed from the schematic 2026-09-05:** the H1 ribbon carries only ADC_CNV, ADC_BUSY,
ADC_SDI, ADC_SCK, ADC_SDO, SCLK, SDI and SYNC1-4. There is no ALERT line. The LEDs really are the
only indication, and this is now documented rather than inferred.

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

**The numbering is now known**, extracted from the preamp gerber's embedded netlist on
2026-09-06:

| Pin | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Net | GND | **+supply** | **OUTPUT** | GND | **−supply** |

**Orientation rule, unambiguous because the layout is asymmetric:** the **negative supply sits at
the very end** of the row; the **positive supply is one in from the other end**. The middle pin is
always the output. So measure the two supplies and the numbering follows, with no reliance on
silkscreen.

> **This retires the earlier "do not run a wire between JP1 pins" rule.** That existed only because
> the numbering might be mirrored, making a supposed ground actually −15 V. Pins 1 and 4 are both
> GND on the board, so once they are identified by the rule above, bonding the open one to the good
> one is electrically correct. See `docs/WIRING.md` §10.

This was previously filed as "resolves itself when the board is rebuilt". **That is no longer
safe to assume**, since the rebuild is deferred behind the shield test. If the shield fix solves
the offset and the old board stays in service, this open ground still needs resolving — and it is
now a straightforward job rather than a blocked one.

**Next step:** block A2b of [`sessions/2026-09-06-plan.md`](sessions/2026-09-06-plan.md) —
identify the pins with a meter, record which ground wanders, then bond it.

---

## Next actions, in order

> **A bench plan for these is written up step by step in
> [`sessions/2026-09-06-plan.md`](sessions/2026-09-06-plan.md)**, written to be run by one person
> alone. Start there rather than from this list.
>
> **Two known errors in that plan, found while running it on 2026-09-06.** Read
> `sessions/2026-09-06.md` §18 before following it:
> - **Block A** says "board unpowered for all of Block A", but **A2b needs power** to identify the
>   supply pins by voltage. Do A2b unpowered with continuity instead — the two GND pins beep to
>   each other and to controller ground, the middle pin is the output, and the asymmetry rule
>   names the supplies. The fault being hunted is an open ground, so continuity is the better
>   instrument anyway.
> - **Block C** assumes no ground wire exists and that the shield is continuous. **Both were
>   false.** The shield has since been rebuilt; Block C is now just the verification step.

0. **Verify the rebuilt shield with a meter.** Every point on the shield must beep to the ground
   wire — near the wire, the far corner, **and across every soldered seam**. This takes two minutes
   and **everything below depends on it.** A D3 result taken on an unverified shield is worthless.
1. **Answer the two datasheet questions.** Neither needs the bench, and one of them gates a fix
   that is otherwise ready to go. (a) Does the AD5761R have internal pull-ups on CLEAR#/RESET#?
   (b) Is the LTC2326-16 output signed two's complement or straight binary?
2. **Run the shield test properly: D1, D2, D3.** Baseline with the shield wire disconnected, then
   the rail-scaling test, then with the shield connected. **Then rebuild the preamp if it is still
   bad**, and run the same acceptance test.
3. **Characterise the DAC config loss.** Suggested experiment: `RSET`, confirm LED1–4 dark, then
   leave the board completely alone for 30 minutes with no commands sent and check the LEDs again.
   That separates "activity triggers it" from "time or the rail triggers it".
4. **Calibrate counts to amps.** Simultaneous meter reading at R23 and `ADCR`, bench clear, two
   well-separated points. Settles the 4.096 vs 10.24 question below.
5. **Dummy junction test.** A **100 MΩ resistor or larger** clipped between the sample holder and
   the tip holder. Proves the whole current path with no tip and no crash risk, gives counts per
   amp directly, and **tells us the sign of the current**.
   > **Do not use 1 MΩ.** An earlier version of this list said "between 1 MΩ and 100 MΩ". The
   > preamp reads to about 100 nA; 1 MΩ at 3 V of bias pushes 3 µA, thirty times over range and
   > instantly saturated. Corrected in `sessions/2026-09-06.md` §11.
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
4. ~~**Do not run a wire between JP1 pins** on the old board.~~ **RETIRED 2026-09-06.** This rule
   existed only because a mirrored pin numbering could make a supposed ground actually −15 V. The
   numbering is now known from the preamp gerber netlist and is identifiable with a meter — see
   fault 5. **This rule and fault 5 contradicted each other inside this file for a day; fault 5 is
   the correct one.**
5. **Do not use cyanoacrylate** anywhere near the preamp, or in the same enclosure, ever.
   Mount with screws or nylon standoffs first, 2-part epoxy second, foam tape third.
6. **Park Z at midscale (32768) before moving the motor.** `RSET` and `TEST` both slam Z to a
   rail, so re-park after either.
7. **Before first imaging, meter-check the tip holder against the brass piezo electrode.** Berard
   warns that glue must not bridge the tip standoff to the grounded brass plate. That path is a
   shunt across the preamp input — it costs signal and adds noise. It is **not** an offset source,
   so it is not a candidate for the 37 nA, but it must be open before imaging.
8. **Never send `CCON` with a tip in tunneling range** until the integral-init bug in fault 2 is
   fixed. Engaging the loop snaps Z to midscale.
9. **No preamp measurement is valid while anyone is leaning over the board.** A person within a
   metre injects 20 to 50 nA, which is twenty to fifty times a tunneling current.

---

## Open questions

The full register, including the undocumented hardware and process items, is in
[`docs/OPEN_QUESTIONS.md`](docs/OPEN_QUESTIONS.md). The ones blocking work right now:

| Question | Why it matters |
|---|---|
| **Does the rebuilt **preamp box** shield actually conduct end to end?** | **VERIFY, two minutes with a meter.** Every preamp conclusion next session depends on it |
| **Does the AD5761R have internal pull-ups on CLEAR#/RESET#?** | Everything else about the floating-pin hypothesis is now confirmed. This is the only fact left that decides whether the four-wire fix is worth doing. **Datasheet question, still nobody has looked** |
| Is the 37 nA the CA contamination or the shield? | Decides whether the spare board gets consumed |
| Is the DAC configuration loss startup-only, or does it recur mid-session? | 2026-08-31 recorded it recurring every 30 to 60 minutes, which requires checking LED1–LED4 around every measurement. If it is startup-only, one `RSET` at the start is enough. **Currently ambiguous, needs settling at the bench** |
| ~~Is there a sample material?~~ | **Answered 2026-09-05: gold foil.** It must be mounted flat on a magnetic disc with a conductive path to the bias magnet — see `docs/UPSTREAM_BERARD.md` §5. Expect atomic terraces, not individual atoms; Berard could not resolve single atoms on metals |
| How far does one motor step move the tip, in nm? | **Largely answered 2026-09-05: roughly 5 to 8 nm.** From the 1/4"-80 pitch and 2048 steps/rev, with a lever reduction Berard quotes as **either 20 or 30 on different pages** — 7.8 nm at 20, 5.2 nm at 30. **Nothing depends on resolving it**: both give 90–130 steps per Z range. **VERIFY our own ratio** — ours is Mech Panda's geometry. Replaces the old 244 nm estimate. See `docs/UPSTREAM_BERARD.md` §2b |
| Which Z direction is toward the sample | Only resolvable at first tunneling, or from the CAD. Park Z at midscale meanwhile. **`stm_approach.py` requires this answer before it will run** |
| Which sign of `MTMV` advances toward the sample | Determinable by eye with the tip removed. **`stm_approach.py` requires this too** |
| ADC full scale: 4.096 or 10.24 V? | `LTC2326_16.hpp` says 4.096, `stm_control.py:37` and `stm_console.py` say 10.24. The R23 reading favours 4.096. Every current figure depends on this |
| DST-201 DC input impedance | Needed to finish some of the high-impedance arithmetic |

---

## Known code issues, deliberately not fixed yet

| Where | Issue |
|---|---|
| `stm_firmware.hpp` `approach()` | Signed `>` comparison against a negative baseline. **Routed around** — use `Code/pc/stm_approach.py`, which never sends `APRH`. Left unfixed deliberately |
| `stm_control.py:37`, `stm_console.py` | ADC full scale hardcoded as `10.24`. **Now known to be wrong — it is 4.096.** Deliberately not changed yet: it would silently alter every number these tools print, so it should land together with the calibration that proves it |
| `LTC2326_16.cpp` `read_volts()` | **Broken upstream**: multiplies raw counts by 4.096 instead of scaling by full scale. Returns "134213 volts" at full scale. Never called, so harmless. Do not use it |
| `stm_firmware.hpp` | Duplicate `LTC2326_16` object at file scope and as a class member, same pins |
| `AD5761.cpp` `write()` | Missing `SPI.endTransaction()` |
| `stm_control.py:127` | `send_cmd('MTMV {steps}')` — **missing the `f` prefix**, so it sends the literal text and the motor moves **zero steps**. This is why the GUI's motor control does nothing. Upstream bug, verified 2026-09-06 |
| `stm_control.py:88` | `set_buffer_size()` is **Windows-only** in pyserial. On macOS or Linux the GUI cannot open the port at all |
| `stm_control.py:40-49` | All three axis voltage conversions use ±5 V. Z is **±10 V**, X and Y are **±3 V**. Every voltage the GUI displays is wrong |
| `stm_firmware.hpp:497-498` | Comments say X and Y are ±5 V. They are **±3 V** — same mode bits as bias, which measures ±3 V. Comment only, the behaviour is correct |

`logTable[abs(adc)]` is **safe** — the table is `[32769]`. Do not "fix" it.
