# Current status

**Last updated:** 2026-09-07
**Updated by:** Jacob (remote, from a photo of the rebuilt preamp box — nothing was powered and nothing was measured on hardware)

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

> ### Physical state of the preamp right now — read before planning any measurement
>
> Established 2026-09-07 from a photograph and Jacob's description.
>
> | | |
> |---|---|
> | **The box is OPEN** | Lid off, and the back cut away for probe access. **An open box is not a shield** |
> | **The tip coax is CUT** | Severed to get the module out. The input node no longer includes the cable, tip holder or tip — **which makes a bisection test possible for the first time** |
> | **The board is glued in and cannot be removed** | Heavily superglued to three standoffs printed as part of the box |
> | **The PTFE standoff is also glued to the board** | With cyanoacrylate. **This is the new leading candidate for the 37 nA** — see fault 1, candidate A0 |
> | **The bias HAS been on the whole time** | **Corrected 2026-09-07.** An earlier version of this box said there was no bias. Wrong. The sample plate is wired and biased; it is simply parked away from the tip holder, not near it |
> | **No tip is fitted** | Only the tip holder. **Nothing can be crashed**, so bias sweeps, Z sweeps and rail scaling are all zero-risk right now |
> | **The piezo is superglued into its socket** | **A third CA site**, and this one is at the scan head, next to the tip holder — which is part of the input node |
> | **The spare board is bare** | Not assembled. **Do not glue it in** — see safety rule 10 |
> | **3D prints are PETG-CF** | Confirmed by Jacob 2026-09-07. Closes the PA-CF/PETG-CF conflict opened by the slicer files |

> **New on 2026-09-06, second pass.** A verification audit found the first pass had stopped early.
> The five `.3mf` slicer files, the CAD render and the reference images had never been opened; two
> numbers in the reference were wrong. Highlights, all detailed below or in the reference:
> **safety rule 10** (an out-of-range DAC command silently jumps to the opposite rail),
> **fault 4b** (U13's unused op-amp channel floats next to the bias buffer),
> **the measurable-current ceiling is 41 nA, so the 37 nA fault is eating 91% of the ADC's range**,
> and **H1 pins 24 and 26 are spare ribbon conductors** — exactly the two wires the DAC fix needs.
>
> **New on 2026-09-06: `docs/ENGINEERING_REFERENCE.md`.** A repository-wide audit that pulls the
> cross-subsystem picture into one place — the grounding map, **the copper-vs-aluminium tape
> rule**, what a scan command becomes in nanometres, what a tunneling current becomes on screen,
> and an impact map for "if I change this, what else has to be rechecked". Every value in it
> carries a confidence tag. It does not replace this file; it explains how the pieces relate.
>
> The same audit **measured the printed parts** and closed two long-standing unknowns: all
> plate-to-plate and motor-mount screws are **M3**, and every printed box is held by a screw that
> **self-taps into a bare printed pillar** (dia 2.5 for M3, dia 1.6 on the preamp box for M2).
> Drive those slowly and stop at snug — over-tightening strips the pillar and the lid stops
> clamping onto its shield. `CAD/prints/README.md` has the table.

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
| **A0. Cyanoacrylate AT THE BASE OF THE PTFE STANDOFF.** The standoff would not fit through the board hole, so it was glued down. That standoff's only job is to hold the input node off the board on the best insulator available — **and CA bonds straight across it** | **2026-09-07** | **LEADING.** A solid contact path at **0 mm** from the node, not a vapour path at a distance. See below |
| **A. Cyanoacrylate contamination / bloom.** CA blooms while curing and deposited a conductive haze over the board, input node included. The board is also **heavily** glued to three printed standoffs, the nearest **4.8 mm** from the input pad | 2026-08-31 | Live |
| **B. The case shield is floating.** | 2026-09-01 | **Shield rebuilt 2026-09-06**, all copper, seams soldered, one ground bond. Still **untested electrically**. Now the leading suspect for the **noise** rather than the offset — see the noise note below |
| **C. Flux residue.** Berard independently reports "huge leakage currents" from flux left on this exact circuit | 2026-09-05 | Live. Addressed by the existing rebuild clean, but not excluded on the current board |
| **D. The coax or the tip holder.** Never separated from the board until now | **2026-09-07** | **Now testable in one reading** — the coax has been cut, so the input node no longer includes it |
| **E. Cyanoacrylate at the piezo socket.** The disc was glued into its socket — a **third** CA site, at the scan head and right next to the tip holder, which is part of the input node | **2026-09-07** | Live. Berard's warning in safety rule 7 was already that glue must not bridge the tip standoff to the grounded brass electrode. **We now know glue was used exactly there.** Meter-check it |

> ### A0: the glue at the PTFE standoff, and what the output SIGN says
>
> **Superglue was used twice on this build, and the first use is the serious one.** A small amount
> bonds the PTFE standoff to the board; a large amount bonds the board into the box. The standoff
> exists to insulate the input node from the board surface. Cured CA is hygroscopic and
> `sessions/2026-08-31-results.md` already says it "conducts at exactly the level measured".
>
> **The sign of the output points somewhere specific.** For a transimpedance amplifier, a leak to
> the **negative** rail pulls current out of the virtual-ground node, so the op-amp must supply it
> back through the feedback resistor — which drives the output **positive**. **The measured output
> is +3.73 V, positive.** About **402 MΩ** would produce 37 nA from −15 V, and `IC1` pin 4 is the
> −15 V rail sitting **2.54 mm** from the input pad.
>
> **Caveats, stated plainly.** This rests on the ADC being signed two's complement, which is still
> INFERRED — though if the rail test agrees, that independently settles the signed question.
> And `IC1` pin 3 is GND, directly between pins 2 and 4, which guards a straight-line surface path.
> So the leak more likely goes over or around the pins, which is what a blob of glue and a standoff
> would do.
>
> **The test: scale the rails independently, not together.** If the offset follows the negative
> rail and ignores the positive one, this candidate is confirmed.

> ### Every other voltage in the instrument has the WRONG SIGN — added 2026-09-07
>
> This is the sharpest argument the project has, and it came out of correcting a mistake: the bias
> has been on the whole time, not off. Working out what that implies narrowed things rather than
> widening them.
>
> Nothing had commanded a DAC before the 2026-08-31 capture, so by `docs/DAC_BOOT_STATE.md` every
> DAC sat at **zero scale**, and the inverting output stages flip each one:
>
> | Source | Where it sits | Would drive the preamp output | Matches the measured **+3.73 V**? |
> |---|---|---|---|
> | Sample holder, via bias | DAC −3 V → holder **+3 V** | negative | **No** |
> | Piezo electrodes, DSUB1 | DAC −10 V → DSUB1 **+10 V** | negative | **No** |
> | Preamp **+15 V** rail | **+15 V** | negative | **No** |
> | **Preamp −15 V rail** | **−15 V** | **positive** | **YES** |
>
> **A leak from any positive source pushes current INTO the virtual-ground input, which drives the
> output negative. The output is positive. So the source must be negative — and the only negative
> voltage anywhere near the input node is the preamp's own −15 V rail.**
>
> That is on the preamp board, which is exactly where the glued PTFE standoff sits, 2.54 mm from
> `IC1` pin 4.
>
> **Caveats, and they matter.** This rests on the ADC being signed two's complement (INFERRED, not
> confirmed) — if it were unsigned every row flips. It assumes no DAC was commanded earlier in that
> session, which is not recorded. And the hourly DAC configuration loss means the real outputs are
> never certain.
>
> **But every caveat is cheap to close, and with no tip fitted all three tests are zero-risk:**
> sweep the bias and watch the offset; sweep Z and watch the offset; scale each rail separately.
> **If the offset ignores bias and Z but follows the negative rail, the diagnosis is complete —
> and the signed-ADC question is settled at the same time.**

> ### The noise is several hundred times the theoretical floor
>
> The 100 MΩ feedback resistor's own Johnson noise is about **12.9 fA/√Hz**, which over the
> transimpedance bandwidth gives roughly **1 pA RMS**. The measured noise was **780 pA RMS**.
>
> That is far too much to be the resistor, and it points at **pickup** — and the shield was
> discontinuous when that capture was taken. **So the offset and the noise may have different
> causes:** contamination for the DC, the broken shield for the noise.
>
> **Consequence for the shield test: record the standard deviation, not just the mean.** The old
> plan only compares offsets against 29873 counts. The shield should show up most clearly in the
> noise, and there is a lot of room to demonstrate an improvement even if the DC offset does not
> move at all.

> ### The board cannot be removed, and cleaning is therefore partial
>
> It is heavily glued to three standoffs that are printed as part of the box. The top surface can
> be cleaned — worth doing, since the input pad is a top-side SMD pad and bloom is a surface
> deposit. **Underneath cannot.** So a clean-and-remeasure that shows no improvement **does not
> clear the superglue.** Replacing the board also means a new box print.

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

**Test order revised 2026-09-07.** Two cheaper and more decisive tests now come before the shield
work: **the coax bisection** (candidate D, one reading, made possible by the cut) and **independent
rail scaling** (candidate A0). Both are reversible, neither consumes the spare board. The shield
test follows — and it still requires the continuity check first, **and a closed box.**

> **The preamp box is currently OPEN. The lid is off and the back has been cut away for probe
> access.** An open box is not a shield. Offset numbers taken in that state are measurements of an
> **unshielded** preamp and must be labelled as such. A D3 result taken with the box open would
> understate the shield and could wrongly send us to consume the spare board.

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
96 nets, **34 have only a single pad on them** — and twenty of those are U1–U4 pins 2, 3, 9, 10 and
11. CLEAR# and RESET# are connected to nothing at all, by design, on every DAC.

**Recounted 2026-09-06: it is 34, not 25.** The full breakdown, because the other fourteen turn out
to matter:

| Pads | What they are |
|---|---|
| 20 | **U1–U4 pins 2, 3, 9, 10, 11** — the DAC control pins. This fault |
| 5 | U5 (ADR421 reference) pins 1, 3, 5, 7, 8 — trim and not-internally-connected. Correctly unused |
| **4** | **DSUB1 and DSUB2 shell / mounting posts.** Both D-sub shells float; nothing bonds them to AGND on the board. Any cable shield landed on a backshell is floating |
| **2** | **H1 ribbon pins 24 and 26 — spare conductors.** Two unused wires already run from the Teensy to the board. If the four-wire fix for this fault goes ahead, CLEAR# and RESET# can be commoned across all four DACs onto exactly these two spare pins. **No new cable is needed** |
| **3** | **U13 pins 5, 6, 7 — the entire unused second channel of the OPA2227P** whose first channel is the bias buffer. Floating inputs on an unused op-amp half. See the note below |

Also
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

### 4b. U13's unused op-amp channel is left floating — a new lead, not a confirmed fault

**Found 2026-09-06 in the same netlist recount.** U13 is an **OPA2227P dual op-amp**. Channel A is
the **bias buffer that drives the sample**. Channel B — pins 5 (+IN), 6 (−IN) and 7 (OUT) — is
connected to **nothing at all**.

That is a recognised design defect rather than a normal spare. An op-amp channel with floating
inputs can drift to a rail or oscillate, and it shares a die and both supply pins with the channel
next to it. Whatever it does couples into the bias line, and the bias line goes straight to the
tunnel junction.

**The same package is wired correctly elsewhere on this board**, which is the evidence that this is
an oversight: on U9 and U10, channel B's non-inverting input is tied to AGND. On U13 it is open.

| | |
|---|---|
| **Confidence** | The pins are open: **CONFIRMED** from the netlist. That it is *causing* a problem: **UNKNOWN** |
| **Predicted symptom** | Noise or slow drift on the bias line that does not track the commanded bias |
| **Test** | Scope U13 pin 7 with the board powered. A quiet DC level is fine; a rail or an oscillation is not |
| **Fix** | Two short wires: **pin 6 to pin 7**, and **pin 5 to AGND**. That makes it a unity-gain follower on 0 V, which is the standard treatment. Low risk, no track cutting |

Not on the critical path — the preamp is — but it is cheap, and bias noise is the kind of thing
that would otherwise be blamed on the preamp.

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

> **Renumbered 2026-09-07.** The list had grown into `-2, -1b, -1, -0b, 0, 0b, 1...` as tests were
> inserted ahead of others. That is not something to read at a bench. It is now a plain 1..12, in
> the order to actually do them.
>
> **The bench plan `sessions/2026-09-06-plan.md` is superseded in part** — it carries a banner
> saying which parts. This list is the current one.

### Group A — zero risk, no tip fitted, do these first

**No tip is installed, so nothing can be crashed.** That will not be true later. Use the window.

1. **Trim the cut coax stub short and clean, leave the input open, and measure.**
   The tip coax was cut to remove the preamp module, so **for the first time the input node does
   not include the cable, the tip holder or the tip.** One reading bisects the fault:
   **still ~37 nA** → the leak is on the board, and the cable and tip holder are cleared;
   **drops substantially** → the leak was never on the board and the rebuild plan changes.
   > Do not measure with the frayed end as it is. At 100 MΩ that stub is an antenna and a
   > contamination magnet. Trim it short and clean first.
   > **And do not rebuild the tip lead until after this reading** — the cut is what makes it possible.

2. **Sweep the bias and watch the offset. Then sweep Z.**
   Both are falsifiable predictions from the sign table in fault 1: **the offset should ignore
   both.** If it moves with bias, the sample-plate path is implicated and the slope gives the
   leakage resistance directly. If it moves with Z, the glue at the piezo socket (candidate E) is
   implicated. **Park Z back at 32768 afterwards** — safety rule 6.

3. **Scale the two supply rails independently.** Not together, which is what the old D2 did.
   If the offset follows the **negative** rail and ignores the positive one, candidate A0 is
   confirmed and the fault is named. If neither moves it, the rails are not the source.
   **This settles the signed-versus-unsigned ADC question as a by-product.**

4. **Meter the tip holder against the piezo's brass electrode.** Safety rule 7 always said to do
   this before imaging, on Berard's warning that glue must not bridge the two. **We now know the
   piezo was superglued into its socket**, so it is a test of a live candidate, not a precaution.
   It must read open — and remember rule 12: OL on a DMM only proves >60 MΩ, which does not clear it.

5. **Verify the rebuilt shield with a meter.** Every point on the shield must beep to the ground
   wire — near the wire, the far corner, **and across every soldered seam**. Two minutes.
   **The box being open makes this easier, not harder.**

6. **The four five-minute checks**, any of which can be done whenever there is a gap:
   - **Calipers on the piezo disc and on the `PiezoPlate` pocket.** The pocket measures
     **Ø20.500 mm**; `docs/BOM.md` says the disc is **25–27 mm**. They cannot both be right, and
     the answer changes every nm/V figure. See `CAD/prints/README.md`.
   - **A ruler on the suspension.** How far do the springs stretch under the hanging platform?
     That one number gives the resonant frequency — 200 mm of droop is 1.1 Hz — with no need for
     the spring rate or the mass. See `docs/ENGINEERING_REFERENCE.md` §7b.
   - **A scope on U13 pin 7.** The unused half of the bias buffer's op-amp is floating. A quiet DC
     level is fine; a rail or an oscillation is fault 4b, and two wires to fix.
   - **A ruler on the scan head lever.** Which screw does the motor drive, and where is the tip
     relative to the front-screw line? The CAD says 40.000 mm and 1.000 mm, which would make the
     ratio 40 and one step 3.88 nm. One minute settles a question open all project.

7. **Answer the two datasheet questions.** Neither needs the bench.
   (a) Does the AD5761R have internal pull-ups on CLEAR#/RESET#?
   (b) Is the LTC2326-16 output signed two's complement or straight binary?
   > **If (a) means the fix goes ahead, it is cheaper than it looked.** CLEAR# and RESET# can be
   > commoned across all four DACs — two wires — and **H1 pins 24 and 26 are spare ribbon
   > conductors already running from the Teensy to the board.** No new cable needed.

### Group B — after Group A, and only with the box closed

8. **Close the box — lid AND back — before any D1/D2/D3 offset numbers.**
   **An open box is not a shield.** Record the **standard deviation** as well as the mean: the
   noise is several hundred times the Johnson floor, and that is where a working shield should show
   up most clearly.

9. **Run the shield test properly: D1, D2, D3.** Baseline with the shield wire disconnected, then
   rail scaling, then with the shield connected.

10. **Characterise the DAC config loss.** `RSET`, confirm LED1–4 dark, then leave the board
    completely alone for 30 minutes with no commands sent and check the LEDs again. Separates
    "activity triggers it" from "time or the rail triggers it".

11. **Calibrate counts to amps.** Simultaneous meter reading at R23 and `ADCR`, bench clear, two
    well-separated points. Settles the 4.096 vs 10.24 question.

12. **Dummy junction test.** A **100 MΩ resistor or larger** clipped between the sample holder and
    the tip holder. Proves the whole current path with no tip and no crash risk, gives counts per
    amp directly, and **tells us the sign of the current**.
    > **Do not use 1 MΩ.** An earlier version of this list said "between 1 MΩ and 100 MΩ".
    > **The instrument reads to 40.96 nA** (4.096 V ÷ 100 MΩ). 1 MΩ at 3 V of bias pushes
    > **3 µA, seventy times over range** and instantly saturated.

### Only when the preamp is working

- **Rebuild the tip lead in plain fine wire, not coax.** Decided 2026-09-07 — see
  `docs/UPSTREAM_BERARD.md` §4 for the reasoning and the method.
- **`Code/pc/stm_approach.py` is written and tested** (2026-09-05, 40 tests against a simulated
  microscope) but has **never been run on hardware**. It refuses to start while the preamp is
  railed, and it needs both direction answers first: which Z direction approaches the sample, and
  which sign of `MTMV` advances.

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
10. **Do not glue the spare preamp board to anything — not the box, and not the PTFE standoff.**
    Added 2026-09-07. Superglue was used twice on the current board: a little to stick the PTFE
    standoff down, and a lot to bond the board into the box. **Both are now suspects**, and the
    first sits directly across the insulator that holds the input node. Gluing the spare the same
    way reproduces the fault and makes the rebuild untestable.
    - **Measure the spare bare first** — on nylon or PTFE standoffs, no box, nothing glued. There
      has never been a measurement of this preamp outside its box, so **the project has no
      baseline.** That single reading is worth more than the whole D1/D2/D3 sequence.
    - **The box print needs fixing before anything is mounted in it.** Its two threaded standoffs
      are 11.43 mm apart; the board's two mounting holes are **5.93 mm** apart. Only one of the two
      screw positions is usable, which is why it got glued. Move the standoffs to match the board
      and keep the Ø1.600 mm pilots.
11. **Do not bring the sample plate near the tip holder** until the offset is understood.
    **Corrected 2026-09-07** — an earlier version of this rule said the bias was off. It is not;
    it has been on throughout, with the plate simply parked away from the tip. The rule that
    matters is the physical separation, not the bias.
    - **Do not fit a tip either.** Without one, nothing can be crashed, and every test below —
      bias sweep, Z sweep, rail scaling — is zero-risk. That is worth preserving until the offset
      is understood.
12. **A multimeter cannot clear a suspect leakage path in this project.** What matters here is
    100 MΩ to 10 GΩ. A typical DMM tops out around 20–60 MΩ, so **"OL" only proves ">60 MΩ"** and
    leaves the entire dangerous range unmeasured. **Never read OL as "ruled out."** The instrument
    that reaches into that range is the rail-scaling test.
13. **Type DAC commands carefully. An out-of-range value does not error — it silently jumps the
    axis to the opposite rail.** Found 2026-09-06 by reading the driver. `set_dac_z(int)` hands its
    value to `AD5761::write(uint8_t, uint16_t)`, so anything outside 0–65535 wraps modulo 65536
    with no warning:

    | You type | Firmware actually sends | DAC output |
    |---|---|---|
    | `DACZ 65535` | 65535 | +10 V, as expected |
    | **`DACZ 70000`** | **4464** | **−8.6 V.** You asked for the top rail and got most of the way to the bottom one |
    | **`DACZ -1`** | **65535** | **+10 V.** You asked for below zero and got the top rail |
    | **`DACZ`** with no number | **0** | **−10 V.** `parseInt()` times out and returns zero |

    From midscale, each of those is a jump of roughly 8 to 10 V — **hundreds of nanometres**, far
    more than a tunneling gap. **Keep every DAC argument between 0 and 65535, and never send a
    bare `DACZ` / `DACX` / `DACY`.** There is no clamp anywhere in the path: not in `main.cpp`, not
    in `set_dac_*`, not in the driver.

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
| `AD5761.cpp` `write()` | **`reg_data` is `uint16_t`, so every DAC command wraps modulo 65536 with no error.** See safety rule 10 — this is a tip hazard, not a cosmetic issue. Found 2026-09-06 |
| `main.cpp` `SCST` handler | **Seven integers parsed straight from serial with no bounds check.** `y_resolution` indexes `scan_image_adc[2048]` and `scan_image_z[2048]`, so **`y_resolution > 2048` writes past the end of both arrays.** `sample_per_pixel = 0` divides by zero. Keep y_resolution ≤ 2048. Found 2026-09-06 |
| `AD5761.cpp` `write_volt()` | **Never called, and wrong if it were.** `(voltage/2.5 + 4)/8 * 65536` assumes the ±10 V range, so it is wrong for X, Y and bias (±3 V); and at exactly +10 V it computes 65536, which wraps to 0 and outputs −10 V. Same class of trap as `read_volts()`. Do not use it. Found 2026-09-06 |
| `AD5761.hpp` header comments | Document the mode words as `0b0000000101000` (±10 V) and `0b0000000101101` (±3 V). The firmware actually writes `0b0…000` and `0b0…101`. **Only the low three bits agree.** The firmware's words are the ones measured to work; the header's comments are stale. Found 2026-09-06 |
| `checkSerial()` in `main.cpp` | Fires on **one** available byte then reads four without waiting, and leaves the terminator in the buffer after an argument-less command. `stm_console.py` already works around both — it sends one write, and a newline **only when there is an argument**. **Anything else (Arduino Serial Monitor, a hand-typed terminal) will desynchronise**: after `RSET` or `ADCR` the stray newline eats the first character of your next command |

`logTable[abs(adc)]` is **safe** — the table is `[32769]`. Do not "fix" it.
