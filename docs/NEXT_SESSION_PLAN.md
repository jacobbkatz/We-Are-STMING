# Next session plan

**Last updated:** 2026-09-17, second pass — gold leaf card now also covers **proving the leaf is real gold** and **cutting it to size**; **`--z-step 5` in step 6** (STATUS.md fault 6)

**This document assumes no memory of any conversation.** Everything needed is here or named by
file. Read `STATUS.md` first for state; this file is the procedure.

---

# START HERE — after the 2026-09-16 approach attempt

**State left:** powered off. Tip fitted, a placeholder. Gold leaf on the sample plate in front of the
tip. **Coarse screw at +6144 motor steps, about 1 mm out, from the position set by hand** — the
firmware counter resets at restart, so carry this number by hand. **Motor direction provisional and
disputed; Z direction unknown.** `sessions/2026-09-16-bench.md` §3.8–§3.11.

**Why the approach found nothing is not known.** Do these, in order, before approaching again:

1. **Motor direction, by looking.** Sample plate off. Look straight at the head's face: **is the tip on
   the motor-driven screw's side of the straight line through the two side-by-side ball ends, or
   beyond it?** Photo with a ruler in frame. **On the driven screw's side: negative approaches. Beyond:
   positive approaches.** This also tells the lever ratio: 40 mm divided by that distance.
2. **Gold to bias, with a meter**, powered off: the gold leaf to the orange sample-plate wire must
   beep. Touch the leaf lightly at an edge away from the tip. **Last session checked plate-to-ground
   and plate-to-tip only.**
3. **Replace the crumpled wad with a flat piece** patted onto clean copper tape in front of the tip,
   if it will stay. A crumpled high point meets the tip first.
   > **Step by step, with the meter checks: [`gold_leaf_procedure.html`](gold_leaf_procedure.html)**,
   > written 2026-09-17. **Two gates come before any gold is mounted.** **Part 0: is the leaf actually
   > gold** — never tested; a flame test on a 2 mm scrap settles it, brass blackens instantly and gold
   > does not. **Part 1: does the copper tape's adhesive conduct** — if it does not then the gold
   > carries no bias and no tunnelling current can exist whatever else is right.
   > **Stock, `SAID` 2026-09-17: four 1-inch squares, which is about 100 usable 5 mm pieces, not four
   > attempts.** Cut them sandwiched between paper; never cut unsupported leaf.
4. **Find contact by hand, then back off a known amount.** Powered off, **preamp DB9 unplugged**, meter
   on continuity from the tip holder to the orange wire. **Turn the two side-by-side screws in tiny
   equal amounts until it beeps**, then back both off **1/16 turn — about 20 µm** of a 1/4"-80 screw.
   The screws sit close to the tip, so that is roughly the gap. **It costs the placeholder tip a
   touch.** Plug the DB9 back in.
5. **Power up**: supply at 200 mA limits, then USB. LED1–LED4 dark. `DACZ 32768`, `BIAS 32768`.
   **20 `ADCR` baseline; then `BIAS 38229`, sample −0.5 V, 10 `ADCR` as a touch check** — near the
   baseline means no contact; a reading near its limit means contact, so set `BIAS 32768` and stop.
6. **Approach** with `py Code/pc/stm_approach.py --z-retracted unknown --motor-toward-sample <from
   step 1> --motor-step 10 --max-steps 1000 --z-step 5 -y`, in 1000-step chunks of about 5 minutes.
   > **`--z-step 5` is not optional — added 2026-09-17, `STATUS.md` fault 6.** At the tool's default
   > of 200 the sweep moves **2.08 nm per sample point** against a detectable tunnelling window of
   > **0.21 nm**, so about nine approaches in ten would step from no current straight into contact.
   > `--z-step 5` gives four samples inside the window and costs about 3.3 s per half sweep. **Cap the
   total at twice the steps that cover the back-off at the step-1 lever ratio**: 20 µm at a ratio of 40
   is 800 µm of screw, about 5,200 steps, so a cap of about 10,400. **Mind the screw's range**: from
   +6144 there is about 2 mm left outward and 4 mm inward, **if** Jacob's ±3 mm estimate holds; only
   about 1 mm outward from base has been demonstrated. **Operator a metre away, iron off.**
7. **At first contact the tool prints the Z direction. Record it** in `docs/OPEN_QUESTIONS.md` and use
   `--z-retracted low|high` from then on.

**Do not:** send a single motor move of more than a few hundred steps outside the tool; retract by
hand relying on an unconfirmed direction; `APRH`; `CCON` with a tip in range (safety rule 8 is
annotated, not lifted).

> **Written 2026-09-07. Refreshed at the end of every session from 2026-09-09 onward** — `/wrap`
> step 3 updates it, and `check_facts.py` fails if a session log is newer than the date above.
> **Before 2026-09-09 nothing kept it current**, so it sat unmaintained for two days and neither
> Jacob nor Nuh knew it existed.

---

# WHERE THINGS STAND — 2026-09-15, end of the evening

# THE PREAMP WORKS. ~4 pA in its box at 45 minutes

**The gate is passed. The preamp is no longer the blocker on this instrument.** Full account:
[`sessions/2026-09-15-bench.md`](../sessions/2026-09-15-bench.md) §11. Everything below this block
that treats the preamp as broken, unbuilt or unmeasured is history.

| | |
|---|---|
| Input current, boxed, 45 min | **~4 pA** — safety rule 14 wanted under 0.1 V, this is 250× inside |
| Drift, 20 to 45 min | **None.** Safety rule 0's 45-minute wait is **RETIRED** — about 2 minutes to settle is enough |
| Cost of the box and shield | **None** — 4 pA boxed against 6 pA bare |
| Blocking the controller | **Nothing** |

## ~~START HERE — the splice is DONE and VERIFIED. Power it up~~ DONE 2026-09-16: THE ADC CHAIN WORKS

> **Done 2026-09-16, Jacob at the bench, commands sent by Claude from Jacob's machine.** Controller at
> about 40 mA with 200 mA limits, LED1–LED4 dark after `RSET`, Z at 32768, two minutes' settle.
> **`ADCR` 89, 22, −13, then twenty more with a mean of −1.7 counts and no drift**, which is the
> "chain works" row of the table below and matches last night's −0.4 mV meter reading.
> `sessions/2026-09-16-bench.md` §3.2b. **Still owed: a known signal through the preamp**, because a
> grounded input would also read near zero. **The next section is the tip lead.** The steps below are
> kept as the power-up procedure for any cold start.

> **Done 2026-09-15:** the preamp is spliced to the DSUB2 cable and the splice was verified
> unpowered with the DB9 unplugged. **Row of five, left to right: nothing, white, orange, tan,
> grey.** Correct. **Nothing has been powered through the controller yet.**
>
> **~~Verify the splice~~ — done. The verification sections below are kept for the next rewiring.**

~~**Use the Windows machine.** It has run this instrument before.~~ **Corrected 2026-09-16: that
was Nuh's machine, and it was never named.** Jacob's Windows machine was new to the project on
2026-09-16 and is being set up; `Code/pc/README.md` has the first-time Windows steps beside the Mac
ones. **Whichever computer it is, Claude Code has to be running ON that computer**, as the desktop
app or the CLI. **A Claude Code web session runs in the cloud and cannot open the USB port**, which
is what stopped the 2026-09-16 session at the moment of plugging in.

0. **First time on a machine:** follow the Windows or Mac section of `Code/pc/README.md`, and run
   `python Code/pc/stm_console.py GSTS` with nothing plugged in. **"Cannot find the Teensy" is the
   pass.** Do this before the bench, not at it. **Done on Jacob's machine 2026-09-16. On Windows type
   `py`, not `python`**: there `python` is a Microsoft Store placeholder.

> ## 2026-09-16: THE FIRST ATTEMPT AT STEP 3 HIT A CURRENT LIMIT. Do this before powering again
>
> **One channel went into constant-current mode at about 2 V and the other held 18 V.** Switched off.
> **One channel's limit was still at the preamp tests' 20 mA, the other at 200 mA** (`SAID`, Jacob): the controller draws about
> **60 mA from V++ and 36 mA from V--** (measured 2026-08-29, `docs/PROJECT_HANDOFF_SUMMARY.md`
> §A.1.11). **But raising the limit is what would let a wiring mistake do damage, so prove the
> wiring first:**
>
> 1. **Plug out of U19. USB unplugged.** Both current limits to about **200 mA**, the value the
>    2026-08-29 bring-up used.
> 2. **Outputs on, plug hanging free.** Meter on DC volts, black probe on the plug's **middle** wire.
>    The two outer wires must read about **+18 V and −18 V**. Two positives, or a zero: stop.
> 3. **Outputs off.** On the board, beep each outer U19 pin to **U18's middle leg**, which is its
>    V-- input (`docs/WIRING.md` §7). **That pin must receive the −18 V wire.**
> 4. **Then step 3 below at 200 mA.** Expect roughly 60 mA and 36 mA plus a few mA for the preamp.
>    **A channel still in current mode at 200 mA is a real fault: switch off, do not retry.**

**The configuration:** preamp in its copper box, **no sample plate, no overall shield cover, no tip,
no tip lead.** Nothing can be crashed.

1. **Pull the repo** on the Windows machine so it has tonight's changes.
2. **DB9 back into DSUB2. Bench supply completely off the preamp** — the controller's DSUB2 pins 4
   and 5 are outputs and feed it now. **If the supply has a current limit, set both channels to
   about 200 mA**: over three times the controller's measured draw, and it turns a real short into a
   warning. **Changed from 300 mA on 2026-09-16** to match the 2026-08-29 bring-up. **Check it: the
   preamp tests left the limits at 20 mA**, which the controller exceeds.
3. **Analog supply on** — ±18 V into U19, the JST XH. **Note what BOTH channels draw** against the
   2026-08-29 baseline of 60 mA and 36 mA (~~a baseline nobody has ever recorded~~ — **corrected
   2026-09-16, it was recorded in the handoff's history**), and **watch the negative channel for a
   minute.** Roughly
   equal and steady is the pass. **A negative channel much higher than the positive, or climbing,
   is the reused C2 failing: switch off.** That is the residual risk of safety rule 14's amended
   clause (a), and this is its cheap mitigation. If the supply goes into constant-current mode,
   switch off. **LED1–LED4 will be lit. That is normal at every power-on.**
4. **USB.** The documented order is analog supply first, then USB.
5. **`GSTS`** first, to prove the serial link before anything is trusted. Then **`RSET`.**
   **Check LED1–LED4: they are lit at every power-on and `RSET` clears them** — safety rule 1.
   **Confirm all four are dark before and after every reading.**
6. **`DACZ 32768`** to park Z at 0 V. `RSET` leaves it at a rail. **Type the number**: a bare
   `DACZ` or a value outside 0–65535 throws Z to the opposite rail, safety rule 13.
7. **Wait about two minutes**, hands away from the preamp box and its cable, then **`ADCR` three
   times and one `GSTS`** — field 5 of `GSTS` is a raw single conversion and is the control on the
   averaged number.

**Expected: within a few tens of counts of zero.** The preamp output was −0.4 mV on the meter last
night, which is about one count at 0.3125 mV per count; the buffer's and the ADC's own offsets add a
few more. `PREAMP−` now sits at the preamp's own ground, so the converter should finally be inside
its specified input conditions.

**What the controller puts on the preamp, checked 2026-09-16 before this was written:** +15 V and
−15 V from U17 and U18 onto the grey and tan leads, the same rails the preamp has already run on for
over an hour from the bench supply; the preamp's ~0 V output onto the ADC's IN+, inside ±10.24 V;
the bias pin open at the preamp end; Z at a rail from power-on until step 6, with no tip and no
sample plate, so nothing to crash.

| `ADCR` reads | Meaning |
|---|---|
| **within a few tens of counts of 0** | **The chain works.** First time in this project |
| a few hundred counts either way | Fine — that is millivolts at the preamp. Record as the new baseline |
| pinned near ±32767 | Over-range. Stop, meter the OUT lead at the preamp |
| the old ~−400 baseline exactly | Suspicious. Check the splice took |

**Do not run `APRH`** — safety rule 2. **Do not send `CCON`** — safety rule 8. Neither is needed.

**Any noise figure taken in this configuration is NOT representative**, because the overall shield
cover is off. Counts, baselines and offsets are fair; noise is not.

---

## Reference: the wiring, kept for the next rewiring

**Nothing blocks it, and it touches nothing on the input node**, so the ~4 pA baseline survives. It
tests the one chain that has never worked in this project: **every ADC reading ever taken was made
with the converter operated outside its specified input conditions**, because `PREAMP−` was not
grounded. That is fixed on this board.

### The colour trap. Read this before anything is joined

> ## The preamp's own lead colours are NOT the cable's colours, and ORANGE means two different things
>
> **Preamp lead orange = the amplifier's OUTPUT. DSUB2 cable orange = −15 V.**
> **Joining orange to orange puts −15 V onto the amplifier's output through R1.** At 220 Ω that is
> about **68 mA driven into the output stage**, against a part that limits in the tens of mA.
> **It would very likely destroy IC1**, on a board that took two weeks to get right.
>
> **Go by function, never by matching colours.** Jacob's own caveat, recorded 2026-09-14: *"jumper
> cable colours don't necessarily align with J2's colours."* **This is what that means in practice.**

| Preamp lead | Is | JP1 hole | Joins DSUB2 | Cable colour |
|---|---|---|---|---|
| **white** | GND | 1 | **pin 2 `PREAMP−` AND one of pins 6–9 AGND** | brown **and** green |
| **grey** | +15 V | 2 | **pin 5** | yellow |
| **orange** | **OUT** | 3 | **pin 3 `PREAMP+`** | **red** |
| **tan** | −15 V | 5 | **pin 4** | **orange** |

**White takes two wires.** Green (AGND) and brown (`PREAMP−`) both join it at the splice — **three
wires into one joint** — and that is the repair that makes the ADC's negative reference real.
**Decided when the ground repair was planned, 2026-09-13**, and recorded in `docs/WIRING.md` §10.

> **A second colour collision, harmless but it would defeat the point.** **DSUB2 pins 6–9 are all
> AGND: green, blue, grey and WHITE.** So the cable has a white wire too, and the preamp has a white
> lead. **Joining white to white is electrically fine** — both are ground — **but it leaves brown,
> the ADC's negative reference, unconnected**, which is the exact fault this whole splice exists to
> fix. **Use the green one, and take brown with it.** Blue, grey and the cable's white can be left
> unconnected; they are spare grounds off the same point.

**Make this joint mechanically solid.** It carries the reference for every measurement the instrument
will ever take. Heat shrink is fine here — this splice is at the connector end, nowhere near the
input node, so the "no adhesive-lined shrink" rule does not apply to it. **Row rule if you are ever unsure at the
connector: on DSUB2 the row of five carries signal and the row of four is all ground.**

### The configuration for this bring-up: no sample plate, no overall shield cover

**Jacob's decision, 2026-09-15, and it is the right one.** Neither is needed for what comes next, and
leaving them off has three advantages.

- **Safety rule 11 already says not to bring the sample plate near the tip holder until the offset is
  understood.** Not fitting it at all goes further, and no tip is fitted either, so **nothing in this
  bring-up can be crashed.**
- **The big cover, `6_shield_cover.stl`, is for imaging noise, not for electrical bring-up.**
  Berard's own note is that without a shield his images were dominated by 60 Hz pickup. That is a
  problem for pictures, not for an `ADCR` reading.
- **It removes a loop risk.** One fewer copper-wrapped part that could touch the preamp box and
  create a second bond — see the shield question in `docs/OPEN_QUESTIONS.md`.

> **The consequence, and it matters when the numbers come in.** **Any noise figure taken in this
> configuration is NOT representative and must not be recorded as one.** Counts, baselines and
> offsets are all fair; **noise is not, until the cover is on.** This project has already had to void
> a set of noise figures once.

### BEST verification: unplug the DB9 and beep it. Unpowered, and it needs no colour table at all

**Added 2026-09-15, and better than the powered method below**, because it can be done after the
splice is made and it depends only on the netlist, which is solid.

**Unplug the DSUB2 connector from the controller.** The cable and the preamp are now one assembly in
your hand. **Nothing powered.** Meter on continuity.

**The connector has a row of FIVE pins and a row of FOUR.** On DSUB2 the row of five carries signal
and the row of four is all ground. **You do not need to read the tiny numbers** — the order along the row of
five identifies everything:

| Probe | Expect |
|---|---|
| **white** ↔ the row of FOUR | **beep on EXACTLY ONE of them** — the pin green is spliced to. **CORRECTED 2026-09-15: this line first said "beep, all four", and that was WRONG.** With the connector unplugged the four AGND pins are only tied together *inside the controller*, so at the cable end they are four separate wires and only the spliced one beeps. **A correct splice would have looked like a fault** |
| **white** ↔ one pin in the row of five | **beep** — that is pin 2, `PREAMP−`, the sense wire |
| **orange, tan, grey** ↔ the row of five | each beeps to **exactly one** pin |

**Then check the order along the row of five.** Counting from the end where the row of four's own
count starts, the sequence must read:

| Pin | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Function | BIAS | `PREAMP−` | `PREAMP+` | **−15 V** | **+15 V** |
| Your lead | nothing | **white** | **orange** | **tan** | **grey** |

**White, orange, tan, grey — in that order, with one empty pin at the start.**

> ### The one reading that must be SILENT
>
> **orange ↔ the pin that tan is on.** If the amplifier's output beeps to the −15 V pin, **do not
> power anything.** That is the fault that destroys IC1, and it is the only one worth a dedicated
> check.

**If the order comes out different, stop and tell me** rather than reasoning it out at the bench.

### Older method, powered: verify the colours before you trust them

**The FUNCTIONS are netlist-verified and I am confident in them. The COLOURS are not ours** — they
come from the standard colour order of a JUXINICE DB9-to-bare-wire cable (`docs/WIRING.md` §6), which
is a property of whatever cable was bought, not of this build. **That is the one link in the chain
taken on trust, and it is the link that could destroy IC1. Measure it instead.**

1. **Preamp NOT connected.** DSUB2 cable plugged into the controller, **bare ends free, taped apart,
   touching nothing and not each other.**
2. **Power the controller** the usual way, ±18 V into U19.
3. **Meter on DC volts. Black probe on a KNOWN controller ground** — U19's middle pin, `AGND`. **Not
   on a cable wire**, because which cable wires are ground is the thing being tested.
4. **Red probe on each bare wire in turn.**

| Reading | That wire is | Expected colour |
|---|---|---|
| **+15 V** | **DSUB2 pin 5.** Joins the preamp's **grey** | yellow |
| **−15 V** | **DSUB2 pin 4.** Joins the preamp's **tan** | orange |
| **solid 0 V**, four of them | AGND, pins 6–9. Use **one** of these | green, blue, grey, white |
| near 0 and drifting, two of them | the ADC inputs, pins 2 and 3, high impedance and unconnected | brown, red |
| **some other DC level** | `BIAS`, pin 1. **Leave it alone** | black |

**The two that matter are found with certainty: the rails.** Getting those right is what protects
the board. **If brown and red were ever swapped the ADC would read inverted, which is recoverable**;
putting a rail on the output is not.

5. **Power off before splicing anything.**

> **If the colours do not come out as the table predicts, stop and tell me.** It means the cable is
> not the one `docs/WIRING.md` §6 describes, and the whole mapping needs redoing from measurement.

### Then, in order

1. **Splice the four leads as above, with nothing powered.** Check twice against the table, not
   against the colours.
2. **The bench supply comes OFF the preamp entirely.** The controller's DSUB2 pins 4 and 5 are
   **outputs**, and they will now power the preamp.
3. **Power the controller the usual way: ±18 V into U19, the JST XH.** **This is where the 18 V
   figure belongs** — the controller's regulators need headroom above 15 V. It was never the
   preamp's number.
4. **USB, then `RSET`.** **LED1–LED4 are lit at every power-on and `RSET` clears them** — safety
   rule 1. **Check they are dark before and after every reading.**
5. **`DACZ 32768`** to park Z at 0 V. `RSET` leaves it at a rail.
6. **`ADCR`.**

### What to expect, and what each answer means

**The preamp output is about 0 V and `PREAMP−` is now genuinely at ground, so the ADC should read
near zero counts.**

| `ADCR` reads | Meaning |
|---|---|
| **near 0** | **The chain works.** First time in this project. The ADC is inside its input conditions and the number means something |
| a few hundred counts either way | Still fine — that is millivolts at the preamp. Note it as the new baseline |
| pinned near ±32767 | Over-range. Stop and meter the OUT lead: something is not what it was on the bench |
| the old ~−400 baseline exactly | Suspicious. Check the splice actually took |

**No tip is fitted and none should be.** **Do not run `APRH`** — safety rule 2. **Do not send
`CCON`** — safety rule 8. Neither is needed for this.

## Then: the tip lead

## The tip lead, after the above

> **BUILT 2026-09-16** (`SAID`, Jacob): standoff to tip holder beeps, tip holder to the piezo's
> brass electrode is open, so **the safety rule 7 meter check below is done.** Read as no tip fitted,
> not yet confirmed. **Not stated:** the IPA clean, how the standoff is held, the box's final
> position, slack in the lead. **NEXT: re-measure through the ADC** with the power-up steps at the top
> of this file, and compare with the **−1.7-count baseline** from `sessions/2026-09-16-bench.md`
> §3.2b:
>
> | Mean `ADCR` | Meaning |
> |---|---|
> | **within a few tens of counts of −1.7** | **The lead, holder and piezo add no measurable leakage** |
> | **shifted by a few hundred counts** | **About 1 nA added**, 320 counts per nA. That is a tunnelling current's worth. Record, and find it before imaging |
> | **pinned near ±32767** | Stop. An open joint or a hard path to a driven electrode |
>
> **The spread will likely be wider** with the holder on the input node and the shield cover off.
> **It is still not a noise figure.**
>
> **RE-MEASURED 2026-09-16: PASSES.** No tip, IPA-cleaned, lead slack (`SAID`, Jacob). **20 `ADCR`:
> mean −22.3 counts** against −1.7 before, under one standard error apart, so any added leakage is
> below about 0.2 nA. **Standard deviation 131.5 counts against 45**: the spread tripled.
> `sessions/2026-09-16-bench.md` §3.2d.
>
> ## NEXT: the scan head shield cover, then the same twenty readings
>
> 1. **First, find out where the ground wires land** — the cover's, and the preamp box's. Open in
>    `docs/OPEN_QUESTIONS.md`. **One bond per shield to circuit ground, and the cover must not touch
>    the preamp box**, or the two form a second path.
> 2. **Power down before fitting it**: USB out, then supply off. No tip, so nothing can be crashed.
> 3. **Fit the cover over the scanning module**, then the power-up steps at the top of this file and
>    **twenty `ADCR`**, hands well away.
> 4. **Compare the standard deviation with 131.5 counts.** A large drop means the spread was pickup
>    and this is the instrument's first representative noise figure. **Little change points at the
>    other mechanisms in §3.2d**, and moving the lead or the operator is the next split.
>
> **Still owed after that: a known signal through the preamp**, which proves the chain end to end.
>
> **DONE 2026-09-16, AND IT MADE THE SPREAD WORSE.** Cover on, both shields bonded to what Jacob
> called "universal ground": **standard deviation 294.9 counts, against 131.5 without the cover.**
> `sessions/2026-09-16-bench.md` §3.2e.
>
> **SUPERSEDED THE SAME EVENING.** "Universal ground" is the junction of the two supply channels,
> which **is** `AGND` — the bonds were already right. **With nothing changed but Jacob a metre away
> after a break and a power cycle: standard deviation 12.7 counts, about 40 pA, mean −3.0.**
> `sessions/2026-09-16-bench.md` §3.2g and §3.2h.
>
> ## NEXT: name what made §3.2e noisy — twenty readings with the operator CLOSE
>
> 1. ~~**Ask whether the soldering iron, or anything else on the bench, was on earlier and is off
>    now.**~~ **ANSWERED: the soldering iron was on during both noisy captures** (`SAID`, Jacob,
>    2026-09-16) **and fits all four runs.** Leading candidate. **Also run the reverse test: iron on,
>    in its stand where it was, operator a metre away**, and see whether the spread returns.
> 2. **Power up with the steps at the top of this file.** After the LEDs go dark, **Jacob stands
>    where Jacob stood during §3.2e**, near the scan head, **touching nothing.** Twenty `ADCR`.
> 3. **Compare with 12.7 counts.** A jump toward 131 or 295 names the operator, and safety rule 9
>    becomes a hard rule for every capture. **No change** points at the room or the power cycle:
>    then switch the suspect equipment on, standing away, and repeat.
> 4. **Always capture with the operator a metre away** until this is settled.
>
> **BOTH TESTS DONE 2026-09-16.** Operator close, iron off: **17.9 counts.** Iron hot, operator
> away: **21.5 counts.** **Neither explains the earlier 131.5 and 294.9.** The iron's small addition
> is significant, so **iron off for every capture that matters.** `sessions/2026-09-16-bench.md`
> §3.2j and §3.2k.
>
> **DONE 2026-09-16, AND IT PASSES.** 100 MΩ dummy, bias jumper to tip holder: **−3,205 ± 37
> counts per volt, 320.5 counts per nA, R² 0.993; positive sample voltage reads NEGATIVE.**
> `sessions/2026-09-16-bench.md` §3.4. **The procedure below is kept for re-running after any
> change to the current path.**
>
> ## ~~THEN: THE DUMMY JUNCTION TEST — blocked on clips, 2026-09-16~~ DONE
>
> **The payoff test, planned since 2026-08-31 and never run.** Procedure: `sessions/2026-09-06-plan.md`
> Block F, with the commands sent from Claude and `py` in place of `python` on Jacob's machine.
>
> **Needs, and not confirmed in the room:** **a resistor of 100 MΩ or more** (anything up to about
> 1 GΩ; **never 1 MΩ**, which overloads the preamp), and **clip leads or mini-grabbers** — **none
> owned** (`docs/INVENTORY.md`). **Also ask whether the sample holder is still wired to the black
> `BIAS` wire**; if not, the resistor goes to that wire's bare end.
>
> **Order:** powered off; handle the resistor by its leads only, gloved; one lead gently to the tip
> holder with no pull on the piezo or the tip lead; the other to the sample holder or black wire;
> nothing else touching. **Power up, `RSET`, `DACZ 32768`, LEDs dark**, then `BIAS` at 32768, 40000,
> 50000, 25000, 15000 and back to 32768, **five `ADCR` at each.** With 100 MΩ, expect about **3,200
> counts per volt at the sample holder**: roughly 2,100 counts at 40000 and 5,000 at 50000, with the
> sign to be measured. **`RSET` alone puts about +3 V on the sample holder**, about 9,600 counts with
> 100 MΩ, which is inside the range.
>
> **DONE 2026-09-16, BOTH PASS.** Red on the old firmware: Z 20000 jumped to 32768 on `CCON`; two
> driver LEDs stayed lit after `MTMV 100`. Uploaded with PlatformIO's Teensy Loader, no button
> press. Green on the new: Z held at 20000; refused at Z 5000; LEDs flickered during `MTMV -400`
> and went dark after. **Faults 2 and 3 are FIXED.** **Safety rule 8 is kept until Jacob and Nuh
> decide.** `sessions/2026-09-16-bench.md` §3.5. **The procedure below is kept for any future
> firmware change.**
>
> ## ~~FIRMWARE: upload and bench-test the two fixes — written 2026-09-16, NOT uploaded~~ DONE
>
> **`CCON` now starts from the current Z** and refuses outside 10000–50000; **the motor coils switch
> off after every move.** Both build. `STATUS.md` faults 2 and 3, `sessions/2026-09-16-bench.md`
> §3.3. **Nothing is uploaded without Jacob's go-ahead.** **No tip for any of this**: Z will move by
> volts and the motor will turn.
>
> **RED FIRST, on the old firmware, so the tests are proven able to fail:**
>
> 1. Powered, `RSET`, LED1–LED4 dark. `DACZ 20000`, `GSTS`: field 2 reads 20000.
> 2. **`CCON 100`**, wait a second, `GSTS`. **Expect field 2 = 32768 and field 8 = 1**: the jump.
>    Then **`CCOF`** and **`DACZ 32768`.**
> 3. Z is parked. **`MTMV 100`**, about 1.5 s. **Look at the four LEDs on the motor driver board
>    after it stops: on the old firmware some stay lit.** Then `MTMV -100`.
>
> **UPLOAD** (Claude runs it): `py -m platformio run -d Code/teensy -t upload`. **Nothing else may
> hold the Teensy's port** — on 2026-08-29 a forgotten serial monitor made the loader ask for the
> PROGRAM button on every upload (`docs/PROJECT_HANDOFF_SUMMARY.md` §A.1.2). One press is fine;
> repeated requests mean something holds the port. **Afterwards `GSTS` shows a small uptime**, and
> the firmware's own start-up `reset()` leaves Z at a rail: **re-park with `DACZ 32768`.**
>
> **GREEN, on the new firmware:**
>
> 1. `RSET`, LEDs dark, `DACZ 20000`, **`CCON 100`**, wait, `GSTS`. **Expect field 2 = 20000 and
>    field 8 = 1.** `CCOF`.
> 2. **`DACZ 5000`, `CCON 100`, `GSTS`. Expect field 2 = 5000 and field 8 = 0**: the refusal.
>    `DACZ 32768`.
> 3. **`MTMV 100`: the driver LEDs go dark within a fraction of a second after it stops.** `MTMV
>    -100`, same, and `GSTS` field 6 back to its starting value.
>
> **Only when all three pass** do faults 2 and 3 become FIXED, and safety rule 8 gets reconsidered.
>
> ## MOTOR DIRECTION — found 2026-09-16, PROVISIONAL: negative `MTMV` approaches
>
> `MTMV +6144` pushed the driven screw's tip **out**; the tip holder sits 1.00 mm on the driven
> screw's side of the pivot pair, so out = sample pushed away. `sessions/2026-09-16-bench.md` §3.6,
> `docs/OPEN_QUESTIONS.md`. **Screw returned to base.**
>
> **Rules for every motor move from now on:**
>
> 1. **Z parked at 32768 first.**
> 2. **A few hundred steps per command, at most.** A move cannot be stopped by command; unplugging
>    USB is the only stop. **Range UNVERIFIED**: Jacob estimated ±3 mm of screw from base and then
>    doubted it; **only about 1 mm outward, 6144 steps, is demonstrated.**
> 3. **Keep a running total of steps from base**, because the firmware's counter resets at every
>    restart.
>
> **ATTEMPTED 2026-09-16 with no contact — the current procedure is START HERE at the top of this
> file.** This list is kept as it stood before the attempt.
>
> ## STILL NEEDED BEFORE A FIRST APPROACH
>
> 1. ~~**Which Z direction retracts**~~ **Cannot be settled on paper** (2026-09-16,
>    `docs/OPEN_QUESTIONS.md`). **Use `--z-retracted unknown`**, which finds it safely at first contact.
> 2. **The tip's position**: **its distance from the line joining the two side-by-side screw centres,
>    and which side.** Jacob measured about 1.8 cm of protrusion and about halfway along the pair; **the
>    1 mm that matters is still unmeasured**, so the motor sign stays provisional.
> 3. ~~**A tip**~~ **fitted 2026-09-16**, blunt and bent, a placeholder. **The gold sample** still to
>    mount. **Dummy junction resistor removed?** Not stated — confirm before any approach.
> 4. **The sample set by hand to within about 75 µm of the tip** — the motor only reaches about that far.
>    **The side-by-side screws now stand beyond the tip** (`SAID`), so the plate can go on without
>    touching it; fit it slowly, watching the tip from the side.
>
> **A TIP IS FITTED. Every `DACZ`, `MTMV`, `TEST` and `TONE` is now a tip hazard.** Keep Z parked at
> 32768, and move nothing with the sample near until an approach is planned.
>
> ## NEXT SESSION: first capture of the day, before any soldering
>
> **Leading candidate for the earlier noise: the freshly soldered, IPA-cleaned input node still drying
> and settling.** It cannot be re-created without re-contaminating the node, so **do not test it
> deliberately.** Instead:
>
> 1. **Iron off and unplugged. Nothing soldered or cleaned that day yet.**
> 2. **Power up with the steps at the top of this file**, operator a metre away, and **twenty
>    `ADCR`**, same as tonight.
> 3. **Compare with 12.7 counts.** Quiet again means tonight's quiet was not luck of the hour, and the
>    cover-on figure stands as the instrument's first noise figure. **Noisy again, with no soldering
>    that day, rules out the drying node** and points at the power-on state or the building.
> 4. **After any future soldering or cleaning near the input node, wait before judging noise.** How
>    long is UNKNOWN: between roughly a quarter of an hour and three hours.
>
> ## ~~NEXT: move each shield's ONE bond to `AGND`, then the same twenty readings~~ MOOT — already on `AGND`
>
> 1. **Find out what "universal ground" is.** If it is mains earth, that is the suspect.
> 2. **Power down**: USB out, then supply off.
> 3. **Take both shield ground wires off "universal ground".** Bond **each shield once** to `AGND`.
>    **The easy point is the junction of the two supply channels**, the middle wire of the U19 plug.
>    **The preamp box's preferred point is the preamp's own ground**, the white lead at the DSUB2
>    splice (`docs/OPEN_QUESTIONS.md`). **The two shields must not touch each other**, and nothing
>    else metal should touch either.
> 4. **Power up with the steps at the top of this file.** After the LEDs go dark, **step at least a
>    metre away** for the wait and the twenty `ADCR`.
> 5. **Compare the standard deviation with 294.9 counts with the cover on, and 131.5 without it.**
>    Well below 131.5 means the earth bond was injecting noise and the cover now works. Unchanged
>    means the bond is not the cause: look at operator distance, then the scan head.

**BUILD THE TIP LEAD.** Safety rule 0b gated it on the bare board being measured; that is done, and
**~4 pA is the baseline every later number gets compared against.** H3 below has the wire.

**Three things first, none a formality:**

1. **Settle how the standoff is held.** It rests on the board surface under the 100 MΩ's own lead in
   tension, and the pole is about 2 mm from IC1's grounded leg. **A second wire pulling on it is a
   mechanical problem.** **Do not glue the spare preamp board to anything, not the box and not the
   PTFE standoff** — safety rule 10.
2. **Fix the box in its final position** relative to the scan head, then cut the wire to length. It
   exits through the **Ø4.00 mm hole at box (15.15, Z 8.60)**.
3. **Decide nothing about the tip yet.** No tip is fitted and none should be.

**Building it:** 40 AWG magnet wire to the standoff's metal pole, same as the resistor. **Burn the
enamel off both ends** — an open joint rails the output and looks exactly like a catastrophic leak.
**Leave it slack**, so it neither pulls on the standoff nor stiffens the piezo, which has to flex
freely. **Local clean with 99% IPA afterwards**: that joint is the one spot that cannot be cleaned
later. **Then re-measure.** Any degradation from ~4 pA belongs to the lead, the holder or the piezo,
and that is now a measurement rather than an argument.

**Then safety rule 7**, before any imaging: meter the tip holder against the brass piezo electrode.
It must be open.

## Then

1. **Connect to the controller** and re-establish the ADC chain. Nothing blocks this now.
2. **Buy copper tape** if any more shielding is wanted. **C2 is not being replaced** — Jacob's
   decision, 2026-09-15.
3. **Get the OPA627's quiescent current** when the network allows, and close the chip-identity
   question against the 4 mA measured tonight.
4. **Fix the `check_facts.py` defects**, including the false positive it threw tonight, each with a
   red-then-green test.

## Open, and worth knowing

| Question | Why |
|---|---|
| **Why did the bench supply's rails wander?** | It will look exactly like a board fault next time. The supply's display at that moment was never captured |
| **How did Berard fit an 11301 into a 2.1082 mm hole?** | Ours will not go. **Draw that hole at Ø2.184 mm on any future board order** |
| **Which op-amp is fitted?** | Open since 2026-09-09. Tonight's 4 mA may answer it for free |
| **Is the piezo block bonded to ground?** | It is aluminium-wrapped. An unbonded conductor near the scan head couples and re-radiates |

---

# WHERE THINGS STOOD — 2026-09-15, earlier the same run

**The ground repair is verified, Part B has passed, and the board has been washed.** All four wires
on and IC1 pin 3 beeps to hole 1 ([`sessions/2026-09-14.md`](../sessions/2026-09-14.md) §3.1); all
six lead free-end readings as expected ([`sessions/2026-09-15.md`](../sessions/2026-09-15.md) §3.1);
washed in 99% IPA and left to dry overnight on a lint-free pad.

**The board has still never been powered. The next thing that happens to it is Part C.**

> **START HERE: is it dry?** It was washed late on 2026-09-14 and dried overnight. **If there is any
> doubt at all, give it longer before powering anything.** Waiting costs an evening; a wrong first
> measurement costs the credibility of the whole rebuild, and that measurement (D5) is the one this
> project has been trying to take for two weeks.

## What is now in the room

| | |
|---|---|
| **Keystone 11301 standoff, 2 off** | **Received 2026-09-14**, DigiKey 36-11301-ND. **PTFE base with a metal pole.** **It does NOT enter our hole** — bench, 2026-09-15. Fitted on 2026-09-15 by resting it on the board surface, held by the resistor lead |
| **99% IPA** | **IN THE ROOM.** Used for the wash on 2026-09-14 |
| **Deionised water** | In the room, **but the water rinse is dropped** — see Part D |
| **Foam swabs, soft brush** | In the room, 2026-09-14 |
| **Calipers** | **NONE. Corrected 2026-09-14** — `docs/INVENTORY.md` wrongly listed them. **No procedure here needs one** |
| **60–70 °C oven or dehydrator** | **NONE, and none was ever bought.** This is what dropped the water rinse |
| **4.7 µF 50 V 1812 ceramics** | **Not owned.** Needed before the controller, not before D5 |
| **Copper tape, conductive adhesive** | **Not owned.** For the box shield, later |

## The JP1 lead colours on the spare board

**Recorded 2026-09-14 and nowhere before that.** Use these for the preamp's own leads.
**They do NOT match the J1/J2 colours in `docs/WIRING.md`** — Jacob's own caveat.

| Hole 1 GND | Hole 2 +15 V | Hole 3 OUT | Hole 4 | Hole 5 −15 V |
|---|---|---|---|---|
| **white** | **grey** | **orange** | **empty** | **tan** |

---

> **UPDATED 2026-09-15, late: THE INPUT NODE IS BUILT.** Jacob fitted the standoff and air-mounted
> the 100 MOhm before Part C was run, so **Part C and the D5 measurement have merged** — with feedback
> in place the output no longer rails, so the first power-up reports both the short check and the
> leakage at once. **The order below is therefore superseded for this board.** What runs now is the
> eight unpowered continuity checks, then the current-limited ramp, then the timed hour:
> **[`docs/preamp_input_node_tests.html`](preamp_input_node_tests.html)**, which is the bench page
> for it and has a to-scale drawing of the node as built.

**A bench page for all of this**, tick-as-you-go and readable on a phone, is
`docs/preamp_next_steps.html`. The verified ground repair it follows on from is
`docs/preamp_ground_repair_map.html`.

---

# THE ORDER THESE GO IN

> **Resequenced 2026-09-14 late, at Jacob's decision.** He chose to skip the smoke test until the
> board is built. **The smoke test is NOT dropped — it moves to after the wash and before the input
> node goes on**, which is strictly better than either running it first or leaving it to the end:
> the board is clean by then, and a fault still gets found while the board is bare and reworkable.
> **Rework after the node is built means flux and a second wash at the one place that cannot be
> cleaned afterwards.** Order is now **B → D-wash → C → D-node → D5**.

Each one gates the next. The input node is built last because it is the part that cannot be
cleaned afterwards.

| | What | Powered? | Roughly | State |
|---|---|---|---|---|
| **B** | Continuity at the four lead free ends | No | 5 min | **DONE 2026-09-14, all six as expected** |
| **D-wash** | Wash the board in 99% IPA, dry | No | An evening + drying | **DONE 2026-09-14, drying overnight** |
| **C** | Current-limited smoke test | **Bench supply only** | 20 min | **NEXT. Confirm the board is dry first** |
| **D0** | Standoff | No | 2 min | **DONE 2026-09-15. It does NOT enter the hole** — sits on the surface, held by the resistor lead |
| **D-node** | Fit the standoff, air-mount the 100 MΩ, run the 40 AWG link | No | An evening | After C passes |
| **D5** | **The first valid preamp measurement this project has had** | Bench supply | 1 hour | The point of all of it |

---

# PART B — continuity at the lead free ends. Unpowered

**To-scale probe map, tick-as-you-go:** `docs/preamp_partB_probe_map.html`.

**This is NOT the test done on 2026-09-14.** That one put the black probe in hole 1 and moved the red
probe around the **board**, which verified the four repair wires. **This one probes the free ends of
the four jumper leads**, and answers a different question: is each lead the one you think it is, and
is it touching any of the others? It matters because Part C clips a bench supply onto those ends.

| Between | Expect |
|---|---|
| +15 V lead ↔ C1's far pad (away from the holes) | Beep |
| −15 V lead ↔ C2's far pad | Beep |
| GND lead ↔ C1's near pad | Beep |
| OUT lead ↔ PAD1 | About 220 Ω |
| OUT lead ↔ each of the other leads | Open |
| +15 V lead ↔ −15 V lead, and each ↔ GND lead | No continuous beep |

---

# PART C — smoke test on the bench supply. Not the controller

The feedback resistor is not fitted yet, so **PAD1 will sit near a supply rail. That is expected and
is not a preamp measurement.** This test checks current and heat only.

1. **Set the supply first.** Supply off. Both channels **5.0 V**, current limit **20 mA**. Check each
   output with the meter.
2. **Make a ± supply.** Channel A's − terminal joined to channel B's + terminal = ground. Then:
   - ground → GND lead
   - A+ → +15 V lead
   - B− → −15 V lead
   - OUT lead taped, touching nothing
3. **On.** Both channels should read **a few mA, in the same ballpark as each other.** The op-amp's
   current flows from +15 V straight to −15 V, so the two match. **Much more current on the −15 V
   channel alone means C2 is leaking.**

   > **"Within 1 mA" was over-specified — corrected 2026-09-14 late, at Jacob's objection.** He is
   > right that our supplies cannot resolve it, and right that it does not matter. **1 mA of
   > sensitivity was only ever going to catch a *mildly* degraded C2 — and C2 is being replaced
   > before this board meets the controller regardless** (safety rule 14), so that reading could
   > never have changed a decision. **Do not let a coarse current display stop you running this
   > test.** Everything it exists to catch is gross and visible on any supply:
   >
   > | What it catches | How it shows |
   > |---|---|
   > | A short from the repair work | A channel pinned at the limit — the CC / constant-current light |
   > | A shorted or badly leaking C2 | Large asymmetry, or the −15 V channel at the limit |
   > | Anything drawing more as it heats | Current visibly climbing |
   > | A part cooking | It is warm to the touch |
   >
   > **The pass is: neither channel at the limit, neither climbing, nothing warm.** No resolution
   > needed. If you want a real number, put the multimeter in current mode in series with one
   > supply lead — it will beat the supply's own display easily.
4. **Off immediately if:**
   - a channel is at the 20 mA limit,
   - the current keeps rising,
   - anything is warm.
5. **Then 15.0 V for 10 minutes.** Never higher: the op-amp's limit is ±18 V. Recheck both currents,
   and touch C2.
6. **Disconnect** −15 V, then +15 V, then ground.

---

# PART D0 — the standoff. Unpowered

**DONE 2026-09-15, and it did not go in. Do not drill anything.**

> **Settled at the bench, against three web-sourced answers.** Jacob offered the part up and **it
> would not enter the hole at all.** It is the 11301, confirmed from the bag. **The node was built
> with the standoff resting on the board surface**, held by the 100 MOhm's own lead in tension —
> nothing glued, nothing drilled, nothing forced.
>
> **What this section said before, and why it was wrong twice.** First that the 11301 was a press fit
> with 0.076 mm of interference, with a #44 drill as the remedy. Then, corrected 2026-09-14, that it
> previously **drops in** with 0.076 mm of clearance, from a distributor's 0.080" pin figure and from Berard's
> own Eagle board specifying `drill="2.1082"` for this exact hole, which our board matches.
> **Two documents agreeing is not a measurement.** Its real through-board diameter is **UNKNOWN** —
> we have no calipers — and all that is established is that it exceeds our Ø2.108 mm.
>
> **Still do not drill.** The node is now built over that hole, we do not know the target size, and
> it is 2.54 mm from the board edge at the input node. **A future board order should draw this hole
> at Keystone's recommended Ø2.184 mm.** See `docs/FACTS.md` and `docs/OPEN_QUESTIONS.md`.

## D0.1 No measurement is needed. There are no calipers, and none are required

> **Rewritten 2026-09-14 late.** This asked for a caliper reading on the pin below the PTFE base,
> expecting ~2.03 mm. **There are no calipers in the room** — Jacob, at the bench; the `SAID` row in
> `docs/INVENTORY.md` that listed them was wrong and is corrected. **Nothing is lost.** The fit was
> never decided by measurement: it is settled by Berard's own board file specifying `drill="2.1082"`
> for this exact hole against our 2.108 mm, with the part's 2.032 mm pin passing through it. The
> caliper was only ever going to confirm an answer we already had.

**The test is the fit itself.** Offer the standoff up to the hole when the time comes. It drops
through, or takes a light push. The PTFE base sits flat on the board surface; the metal pole stands
proud above it.

**Do it AFTER the wash, not before** — you cannot clean underneath a fitted standoff, and that spot
is the input node. So there is nothing to do here tonight except know that it will go in.

**If it will not go:** stop and tell me. Do not force it and do not drill. FR4 is brittle, this hole
is 2.540 mm from the board edge, and **it is the insulator for the input node of a 100 MΩ
amplifier** — a radial crack here is both a leakage path and a contamination trap, in the 100 MΩ to
10 GΩ range a multimeter cannot see. If it does not fit, something about the part is not what we
think and that is worth an hour of my time rather than two minutes of yours.

## D0.2 What we know about the part

- **PTFE base, metal only on the pole** — seen at the bench, 2026-09-14. A top-mount insulated
  terminal. **The input node gets a real PTFE insulator, which is what Berard was doing.**
- **2 off**, DigiKey 36-11301-ND. One spare.

# PART D — gates before the input node is built

**Prerequisites: B and C passed.** B passed 2026-09-14 late, all six readings as expected.

1. **On the bench before you start:** 99% IPA, foam swabs, a soft brush. **91% IPA is not enough for
   the node wash** (`sessions/2026-09-13.md` §5). All are in the room (`docs/INVENTORY.md`).
2. **Wash the whole board — IPA ONLY unless the board can be baked.**

   > **Changed 2026-09-14 late, after Jacob asked whether water on a board is sensible.** It is a
   > fair question and the answer has a condition attached. **Water on an UNPOWERED board that is
   > then properly dried is ordinary practice** — assembly houses wash boards in aqueous cleaners,
   > and deionised water is specifically the kind that leaves **no** residue behind. Tap water is the
   > one that would be a mistake, because its minerals are the very contamination we are removing.
   > **Nothing fitted to this board is water-sensitive:** IC1 is a moulded SOIC-8, C1/C2 are moulded
   > 1812 tantalums, C3/C4/R1 are 0603 ceramics. No trimmer, no relay, no can, no label.
   >
   > **The real risk is not the water. It is water that does not leave.** It wicks under IC1 and the
   > 1812s and sits there, and trapped moisture at a 100 MΩ input node **is the exact fault class
   > this project has been chasing for two weeks.** Worse, it would mimic the signature we already
   > cannot explain: a high PAD1 that slowly improves over an hour looks identical to the "warm-up
   > drift". **A water rinse without a bake could manufacture a fresh copy of our own open question.**
   >
   > **We have no oven or dehydrator** — it was listed as "only if needed" and never bought
   > (`docs/INVENTORY.md`). **So: IPA only.**
   >
   > **Two further points if a bake ever does become available.** The water rinse targets *ionic
   > activator* residue; RMA791 is **mildly** activated and its bulk is rosin, which IPA takes.
   > And the order written here was wrong: **a water rinse must be followed by a final 99% IPA
   > rinse, not preceded by one.** IPA and water mix, so an IPA rinse afterwards displaces the water
   > and flashes off fast. Ending on water is the worst case for drying.

   **Before you start.** Board unpowered, nothing connected to the four leads. **Ventilate the
   room and put the iron away** — 99% IPA is more flammable than the 91%, and its vapour is heavier
   than air. Nitrile gloves on (`docs/INVENTORY.md`).

   **Bath or brush? Bath — preferred, added 2026-09-14 late at Jacob's question.** Immersion beats
   scrubbing here, because **the rosin that matters is under IC1 and the two 1812 tantalums**, where
   no brush reaches. It is also gentler on the four 40 AWG repair wires than dry scrubbing. The
   board is **20.625 × 15.230 mm** (`docs/FACTS.md`) — postage-stamp sized — so a few millilitres
   covers it and fresh IPA for the final rinse costs nothing.

   > **The one rule that makes or breaks a bath: the LAST liquid to touch the board must be CLEAN
   > IPA.** A bath saturates with dissolved rosin as it works — that is it doing its job. Lift the
   > board straight out of a dirty bath and the film that drains off dries **leaving rosin spread
   > over the whole board, including the input node.** That is worse than not washing at all. So:
   > **two containers, never one.**
   >
   > **Container:** glass is unambiguously safe — a shot glass, ramekin or small jam jar. HDPE or PP
   > (food tubs marked 2 or 5) are fine. **Avoid thin clear brittle tubs**, which are often
   > polystyrene and can craze in IPA; dissolved plastic on a 100 MΩ input node would be a
   > self-inflicted version of the exact fault we are chasing. **Shallow dish beats a tall jar**, so
   > the four leads drape out over the edge rather than being forced in.
   >
   > **Do not let the board dry between the bath and the clean rinse.** Go straight from one to the
   > other, wet. If it dries in between, the rosin sets back down and you have to start again.
   >
   > A few minutes is plenty — rosin dissolves quickly and this is not an overnight soak. Swirl it,
   > or brush gently **while it is submerged**, which is the gentlest option of all for the repair
   > wires. The leads will wick a little IPA into their insulation; that evaporates, which is one
   > more reason it is IPA here and not water.

   1. **Bath 1, the wash — or scrub with 99% IPA and the soft brush.** Both sides. Flood it rather than dampening it —
      the IPA has to carry the rosin away, not just move it around. Concentrate on **JP1**, where
      the flux actually went, and around **C2**, which was removed and refitted.
      - **Brush ALONG the four repair wires, never across them.** They are 40 AWG magnet wire and
        finer than a hair. Do not lever the brush under them.
      - **No ultrasonic cleaner.** Not that we have one — but it is what people reach for, and
        those four wires and their scraped-via joints are exactly what it would break.
   2. **Bath 2 / rinse, in clean 99% IPA** — fresh from the bottle, never the dirty liquid from
      step 1. Dip it, then **pour fresh IPA over it as it comes out**, so the very last thing to
      touch the board is clean. **This is the step that matters and the one people skip.** The wash
      dissolves the rosin; only the clean rinse removes it. If the runoff still looks coloured,
      change the IPA and do it again — at this board size that is pennies.
   3. ~~Rinse with distilled water.~~ **SKIPPED — see the note above.** No bake is available, and
      **the four leads are jumper cable**: if they are stranded, as most jumper cable is, water
      wicks up inside the insulation and sits there for days where nothing can dry it.
   4. **Dry. Stand the board on edge so it drains** — do not lay it flat, which traps IPA under
      IC1 and the two 1812s. Somewhere warm, dust-free and out of the way, **overnight.** A cool or
      low hairdryer setting will blow the bulk off first if you want; it does not replace the wait.
      **Board only, never the printed box** — PETG softens near 80 °C.
   5. **From the rinse onward, handle the board by its edges only.** Skin oil and salt are precisely
      the leakage path being removed, and a fingerprint on the input-node area undoes the wash. This
      matters more after cleaning than before it.
   6. **Nothing gets powered until it is completely dry.** If in doubt, give it longer: waiting costs
      an evening, a wrong first measurement costs the credibility of the whole rebuild.
3. **Build the node:**
   1. Press in the standoff, if D0 did not already do it.
   2. Air-mount the 100 MΩ **from PAD1 (the output) to the standoff**. Don't shorten its leads or lay
      it flat.
   3. Run a slack 40 AWG link from the standoff to IC1 pin 2's pad toe.
   4. Clean locally with swabs and IPA, then dry.
4. **The first valid preamp measurement this project will have:**
   - **Setup.** Bench supply ±15 V with 20 mA limits. Meter clipped to the OUT lead, which reads the
     same as PAD1. No box, no tip lead. Nobody within a metre.
   - **Readings.** At 1, 5, 10, 20, **45** and 60 minutes, recording both channel currents each time.
   - **Interpreting it.** The table is in `STATUS.md`, next actions, "Validate the rebuild".
5. **`STATUS.md` safety rule 14 before the controller:** PAD1 under 0.1 V at 45 minutes.
   ~~C2 replaced with a fresh part~~ — **withdrawn 2026-09-15 by Jacob's decision.**

---

# OPTIONAL — was the "119 nA" ever real?

**Ground the old board's IC1 pin 3 and meter its PAD1 again.** If PAD1 drops to near 0 V, the old
readings were the floating input, not leakage.

**Plan it with Claude before doing it.**
- **How to reach pin 3.** The old board is glued into its box.
- **Its wiring to the controller is undocumented.** On 2026-08-31 its ground lead was recorded on
  JP1 pin 4, which has no copper.
- **Its C2 is probably still reversed. Do not ground C2.** Grounding it would put 15 V across a
  reversed tantalum.

---

## ~~BEFORE ANYTHING: two gates added 2026-09-09~~ — status 2026-09-13

**Gate 1 is CLOSED, 2026-09-14 late: the 99% IPA is in the room**, with the DI water, foam swabs and
soft brush already here. The input node may now be built. Soldering at JP1 had already gone ahead on
2026-09-13, because flux there sits on low-impedance pins 16 mm from the input node.
**Gate 2 (M2×6, not M2×8) still stands.** Original text follows.

**1. Do not solder the preamp until the cleaning kit is in the room.** The Chip Quik RMA791 rosin
flux arrives 2026-09-11, but **no 99% IPA, distilled water, soft brushes, lint-free wipes or foam
swabs were ordered with it.** Rosin left on this board is a leakage path at the exact node the
119 nA fault sits on. **Flux without cleaning makes the board worse, not better.**
**Copper tape** with conductive adhesive, for H2, is also still unbought.

**2. When the M2 screws arrive: use the M2x6. NOT the M2x8.** The box pilot is **5.00 mm deep and
blind** and the boss is 4.00 mm tall (measured from the mesh — `docs/FACTS.md`). Through a 1.6 mm
board an M2x6 engages 4.4 mm; **an M2x8 needs 6.4 mm and bottoms out, cracking the boss or jacking
the board off the standoff.** **Put calipers on the board first** — 1.6 mm is JLCPCB's default, not
a measured figure. Drive slowly, stop at snug; the thread is plastic and there is no metal insert.

**Also arriving 2026-09-11:** a manual syringe dispenser (load it from the flux jar) and an assorted
heat-shrink kit — **check whether it is adhesive-lined, and use none of it at the input node**
either way.

---

## Standing rules — read before touching anything

1. **`RSET` after powering the analog supply, every time.** LED1–4 lit means the DACs are
   unconfigured. This happens at every power-on and is expected.
2. **Then `DACZ 32768`** to park Z at 0 V. `RSET` leaves Z at −10 V.
3. **Keep every DAC argument between 0 and 65535.** Out of range wraps silently and jumps the axis
   to the opposite rail. A bare `DACZ` with no number sends 0.
4. **Nobody within a metre of the preamp during any capture.** A body injects 20–50 nA.
5. **Check LED1–4 before and after every capture.** A reading with one lit is void.
6. **No tip is fitted.** Nothing can be crashed. Do not fit one during this session.
7. **No cyanoacrylate near the preamp, ever.**

---

## Equipment for the whole session

Multimeter · bench PSU (two channels, ±18 V) · USB cable · the assembled controller and Teensy ·
the preamp still in its old box · `Code/pc/stm_console.py` · `Code/pc/adc_stats.py` ·
the 3D printer · PETG-CF · copper tape with conductive adhesive · soldering iron · IPA · callipers ·
a ruler.

---

# BLOCKERS — nothing downstream is trustworthy until these are done

## ~~B1. Establish whether the drift is the preamp or the floating reference~~ MOOT 2026-09-13

> **The old board's IC1 +IN floats** (`STATUS.md` fault 0d), so its PAD1 drift cannot be attributed
> to the preamp. Replaced by the timed readings on the repaired spare in Part D. Kept for method.

**Why it matters.** Nuh measured **25,000 counts of climb over an hour** after power-on. If that is
the preamp, every measurement must wait an hour. If it is the floating `PREAMP−` charging, the
preamp may be stable within minutes and **every noise figure in this project is void**, including
"the shield halved the noise". This one measurement decides how every future capture is run.

**Prerequisites.** None. Board powered, no tip, box as it is.

**Procedure.**
1. Power the analog supply, then connect USB. Send `RSET`, then `DACZ 32768`. Confirm LED1–4 dark.
2. Note the time. Put the meter on **PAD1** on the preamp board (the op-amp output pad).
3. Record **PAD1 voltage and an `ADCR` reading together** at: 5 min, 10 min, 20 min, 40 min, 60 min.
4. Step back a metre for each reading pair; do not lean over the board.

**Equipment.** Meter, `stm_console.py`.

**Expected result.** One of two clean outcomes.

| Outcome | Meaning | Decision |
|---|---|---|
| **PAD1 steady, ADC counts climb** | The drift is the **floating reference**, not the preamp | **Stop waiting an hour.** Mark all historical noise figures void. Do B2 immediately |
| **PAD1 climbs with the ADC** | The drift is **real and in the preamp** | Every future capture waits ≥60 min. Record the curve. Likely moisture or charge settling in the contamination |

**Failure indication.** PAD1 reads near ±13 V (railed) or the meter reads nothing — stop and check
the rails at JP1 before continuing.

**Record.** A five-row table: time, PAD1 volts, ADC counts, LED state.

---

## ~~B2. Find and bond the open ground — the `PREAMP−` fault~~ SUPERSEDED 2026-09-13

> **JP1 pin 4 has no copper at all** — it is part of the missing ground pour. On the spare board,
> hole 4 is left empty; green (AGND) and brown (`PREAMP−`) both join the single GND lead in hole 1 at
> the DSUB2 splice. **Do not connect the spare board to the controller until PAD1 reads under 0.1 V** — `STATUS.md` safety rule 14.
> Kept for history.

**Why it matters.** `PREAMP−` is the ADC's negative reference and it is connected to nothing.
The LTC2326-16 is **pseudo-differential and requires IN− within ±500 mV of GND** — ours sits near
**2.7 V**, five times outside spec. **Every ADC reading ever taken by this project was made with
the converter operated outside its specified input conditions.** Nothing measured through the ADC
means anything until this is fixed.

**Prerequisites.** B1 done (so you know what the drift is). **Board unpowered for steps 1–3.**

**Procedure.**
1. **Power off.** Meter on continuity.
2. **JP1 pin 1 to controller ground**, and **JP1 pin 4 to controller ground.** **One will be open.**
   Orientation rule: JP1's layout is asymmetric and the **negative supply is at the end of the row**
   — use that to identify pin 1 rather than guessing.
3. **The `PREAMP−` wire at DSUB2 pin 2 to JP1 pins 1 and 4.** This tells you whether the break is
   on the preamp board or in the cable.
4. **Bond the open one.** Both pins are GND on the board, so joining them is electrically correct.
   The old "do not run a wire between JP1 pins" rule was retired on 2026-09-06 once the pinout was
   known from the gerber netlist.
5. Power up, `RSET`, `DACZ 32768`, and take one `ADCR`.

**Equipment.** Meter, fine wire, soldering iron, `docs/WIRING.md` §10 for the JP1 pinout.

**Expected result.** **The ADC will read pinned at or near 32767.** That is **correct and expected**,
not a failure: with `PREAMP−` at 0 V the ADC sees the preamp's full ~11.9 V, which is over the
±10.24 V full scale. **It is well inside the ±16.5 V absolute maximum, so damage is unlikely** —
though that rating is `[DS-SIB]`, taken from the sibling LTC2326-18. See `docs/COMPONENTS.md` §3.

| Outcome | Decision |
|---|---|
| **Pins at ~32767** | Correct. The reference is fixed. ADC readings become meaningful once the preamp offset falls below ~102 nA |
| **Reads ~30,000 as before** | The bond did not take, or `PREAMP−` is broken somewhere else. Re-meter |
| **Reads near zero** | Something else changed. Stop and re-measure PAD1 with the meter |

**Record.** Which JP1 pin was open; where the break was (board or cable); the ADC reading before and
after; a photo of the joint.

**If you would rather not bond it yet:** that is defensible. The rebuild is validated with a meter
at PAD1 and does not need the ADC. Bonding after the rebuild, when PAD1 is under 0.1 V, removes the
over-range question entirely. **Either order works. Do not do it while unsure.**

---

# HIGH-PRIORITY VERIFICATION

## ~~V1. Meter the rebuilt shield's continuity~~ CLOSED 2026-09-15

> **`SAID` 2026-09-15, Jacob: all shielding has been metered end to end.** This item had been open
> since 2026-09-06 and was the thing every shield conclusion in this project rested on.
> **The preamp box is copper.** Two places are aluminium by decision — the motor mount extenders,
> which have copper over aluminium, and the piezo holding block. Both are recorded in
> `docs/ENGINEERING_REFERENCE.md` §3 with what to watch. **Kept below for method.**

## V1 (retained for method only). Meter the rebuilt shield's continuity

**Why it matters.** Every conclusion about the shield rests on it being continuous. It was rebuilt
on 2026-09-06 and **has never been metered.** The box being open makes this easier, not harder.

**Procedure.** Continuity from the ground wire to: the point nearest the wire, the far corner, and
**across every soldered seam** individually.
**Expected.** Every point beeps. **Failure:** any point that does not — reflow that seam.
**Record.** Number of points tested, number that failed, which.

## V2. Meter the tip holder against the piezo's brass electrode

**Why it matters.** Berard warns that glue must not bridge the tip standoff to the grounded brass
plate. **We now know the piezo was superglued into its socket**, so this is a test of a live
candidate rather than a precaution.

**Procedure.** Meter on its highest resistance range between the tip holder and the brass electrode.
**Expected.** Open. **Failure:** any reading at all.
> **A DMM tops out around 20–60 MΩ. "OL" only proves >60 MΩ**, and the leakage that matters here is
> 100 MΩ–10 GΩ. **A pass here does not clear the path** — it only rules out a gross short.

## V3. ~~Callipers on the piezo disc and its pocket~~ CLOSED 2026-09-09 — skip it

**The piezo scanner is built and working** (Jacob, 2026-09-09). Whatever disc went in fits, so the
Ø20.500 mm seat versus 25-27 mm BOM conflict is a documentation artefact. **Do not spend bench time
on it.** The section is kept below only because its method generalises to any pocket-and-part fit.

## V3 (retained for method only). Callipers on the piezo disc and its pocket

**Why it matters.** `PiezoPlate.stl`'s disc seat measures **Ø20.500 mm**; `docs/BOM.md` says the
disc is **25–27 mm**. Both cannot be right, and **a larger disc moves further per volt**, so every
nm/V figure in the project depends on the answer.

**Procedure.** Measure the actual disc's brass diameter, and the actual pocket in the printed plate.
**Decision:** if the disc is 25–27 mm it **cannot** use that pocket and either the plate or the disc
must change. Record both numbers in `docs/BOM.md` and `CAD/prints/README.md`.

---

# HARDWARE WORK

## H1. Print the new preamp box — do this first, it is the long-lead item

**Why it matters.** The current *physical* box **cannot be reused: it is full of cured CA**, the
leading candidate for the 119 nA. That reason stands on its own.

> **The geometry reason was wrong — corrected 2026-09-08.** This section previously said the box's
> standoffs (11.43 mm) did not match the board's mounting holes (`5.93 mm`, now retired as wrong). **They match exactly:
> both are 11.430 mm.** The board has **three** non-plated holes and the Ø2.108 mm one is the
> **PTFE standoff hole**, not a mounting hole. See `docs/FACTS.md`.

**Files. Print the ORIGINAL base:** `1_preamp_box_base.stl` and `1_preamp_box_lid.stl`.

> **Do NOT print `1_preamp_box_base_v2_screwmount.stl`.** Its added boss at (4.04, 9.12) sits under
> the board's PTFE standoff hole — the input node — and would put an M2 screw and a
> carbon-fibre-filled pillar at the most sensitive point on the instrument. §0.3 of the guide.

**Settings.** PETG-CF, 0.08 mm layers, 2 walls, **no supports**, 40% infill is fine.
**Bambu Studio may offer to repair the model — accept.** The added boss is a separate closed solid
overlapping the floor, an ordinary union.

**Expected.** **TWO** Ø1.600 mm pilots, at **(5.63, 14.83)** and **(5.63, 3.40)**, each in a
Ø6.000 boss 4.00 mm tall, plus one **Ø3.600 support post at (17.70, 9.12)**. Measured from the
original mesh with `Code/pc/stl_features.py`, fit error 0.0001.

> **Corrected 2026-09-09.** This said to expect **three** pilots "including the new one at
> (4.04, 9.12)" — **that is the v2 boss this same section forbids.** Anyone printing the original
> and checking it against that line would have judged a correct print faulty, or printed v2 and put
> a carbon-fibre pillar under the input node. **The original has two pilots. There is no hole at
> (4.04, 9.12).**

**Failure.** Slicer reports non-manifold errors it cannot repair — report it, do not print.
**Do not glue the board in.** Two M2x6 screws into those two pilots — see the gate at the top.

## H2. Wrap and ground the new box

**Copper tape only. No aluminium.** Conductive adhesive, **solder the seams**, bond to circuit
ground at **exactly one point**, **then meter it** as in V1.
**Do not wrap the interior** — the exterior wrap is the Faraday cage; interior copper adds stray
capacitance millimetres from the input node and buys nothing.

## H3. Prepare the tip lead in fine wire — CLEARED TO BUILD 2026-09-15, but it goes LAST

> **Safety rule 0b gated this on the bare board being measured. That gate is now cleared** — the
> board reads about 6 pA. **Three things still come first:** the boxed 45-minute reading, so the
> bare-board baseline exists before the lead is added to the input node; settling how the standoff
> is held, since it currently hangs on the resistor lead's tension; and fixing the box in its final
> position, so the wire can be cut to length. It exits through the **Ø4.00 mm hole at box
> (15.15, Z 8.60)**. Full ordering and the soldering notes are in `STATUS.md`.

**The coax is being retired.** It shielded only 1–2 cm before becoming bare copper, added just
~2 pF, doubled the solder joints on the input node, and — the strongest reason — **it lands on the
tip holder, which sits on a piezo disc that must flex freely**; bending stiffness goes as diameter⁴.

**Use 40 AWG magnet wire** (`docs/BOM.md` §7). Cut it, do not fit it yet.

## H4. Two wires on U13 — optional, low risk

**Pin 6 to pin 7, and pin 5 to AGND.** Makes the unused half of the bias buffer's op-amp a
unity-gain follower at 0 V instead of leaving its inputs floating beside the channel that drives the
sample. **Scope pin 7 first** — a quiet DC level means it is behaving and the fix is cosmetic; a
rail or an oscillation means it matters.

---

# FIRMWARE AND SOFTWARE WORK

**No firmware change is required this session, and none should be made before the preamp works.**
The known defects are recorded in `STATUS.md` under "Known code issues". Three are worth restating:

| Where | Issue | Action |
|---|---|---|
| `AD5761.cpp` `write()` | `uint16_t` argument, so out-of-range DAC commands wrap silently | **Operational rule 3 above.** Do not patch mid-diagnosis |
| `main.cpp` `SCST` | Seven ints parsed with no bounds check; `y_resolution > 2048` overruns two arrays | Keep y_resolution ≤ 2048 |
| `stm_control.py`, `stm_console.py` | Use 10.24 V ADC full scale | **Correct. Do not change.** Confirmed from the datasheet 2026-09-07 |

---

# MEASUREMENTS AND TESTS

## ~~M1. Repeat the bias, Z and rail sweeps with a meter on PAD1~~ MOOT for the old board, 2026-09-13

> The old board's +IN floats, so a sweep there measures nothing about leakage. **Worth running on
> the repaired spare** once it reads small. Kept for method.

**Why it matters.** All three were run on 2026-09-07 through the ADC and **all three are in doubt** —
the reference was floating and 2.7 V outside the converter's allowed range, so those sweeps may not
have been measuring the preamp at all.

**Prerequisites.** B1 done. Meter on PAD1 throughout — **do not use ADC counts for this.**

**Procedure.** For each sweep, settle 3 s per point and return to the start so drift can be
separated from response.
- **Bias:** `BIAS` at 0, 16384, 32768, 49152, 65535, then 0 again.
- **Z:** `DACZ` at 0, 16384, 32768, 49152, 65535, then 32768 again. **Park at 32768 afterwards.**
- **Rails:** drop **only the negative** PSU channel to give −9 to −10 V at JP1 pin 5, hold, then
  restore. Then repeat on the positive channel alone.

**Expected.** PAD1 **does not respond** to bias or Z.

| Outcome | Meaning | Decision |
|---|---|---|
| No response to any | The leak is not driven by bias, the piezo, or the rails | Contamination on the board. Rebuild as planned |
| **PAD1 tracks bias** | The sample-plate path is implicated | The slope gives the leakage resistance directly. Investigate before rebuilding |
| **PAD1 tracks Z** | The glue at the piezo socket is implicated | Check V2 again more carefully |
| **PAD1 tracks the negative rail** | A resistive leak from −15 V | Confirms the standoff-glue hypothesis and names the fault |

**Record.** Every point: commanded code, commanded volts, PAD1 volts. Note the drift between the
first and last reading at the same setting.

> **A failed prediction on 2026-09-07:** the rail-scaling test predicted ~19,000 counts and measured
> 30,175. **That test is one of the three in doubt**, so this repeat is what decides it.

## ~~M2. A noise capture with the meter, not the ADC~~ MOOT for the old board, 2026-09-13

> Every recorded noise figure came from a board with +IN floating. Re-take the noise baseline on the
> repaired spare. Kept for method.

**Why it matters.** The recorded noise is **195 mV RMS at the output — about 1,700× the 100 MΩ
resistor's thermal floor and 10,000× the OPA627's own contribution.** Neither device explains it.
**The floating reference is the prime suspect, which would void every noise figure in the project.**

**Procedure.** With the meter on PAD1, watch it for two minutes. Note the range of the reading.
**Expected.** If PAD1 is quiet to a few mV while the ADC scatters by 600 counts (≈190 mV), **the
noise is the reference, not the preamp.**
**Decision.** If confirmed, mark the "shield halved the noise" observation void in `STATUS.md` and
`sessions/2026-09-07.md`, and re-take the noise baseline after B2.

## M3. The ruler measurements — cheap and each closes an open question

- **Spring droop.** How far do the springs stretch under the hanging platform? **f₀ = (1/2π)√(g/x)**
  — mass and spring rate both cancel. 200 mm of droop is 1.1 Hz; 100 mm is 1.6 Hz. Closes a BOM
  unknown with a ruler. Also record **whether the platform is hanging at all.**
- **Scan head lever.** Which screw does the motor drive, and where is the tip relative to the
  front-screw line? The CAD gives 40.000 mm and 1.000 mm, which would make the ratio **40** and one
  motor step **3.88 nm** — against Berard's 20 (7.75 nm) or 30 (5.17 nm). One minute settles a
  question open all project.
- **Cable routing off the platform.** Photograph it. A taut cable to the bench defeats the springs
  entirely and nothing in this repository describes the routing.

---

# DOCUMENTATION AND REPOSITORY CLEANUP

- **Record every measurement in `sessions/YYYY-MM-DD.md`** (or `-<your name>.md` if the other
  person already logged today) as it is taken, with conditions — bench
  clear or not, LED state, time since power-on. **Time since power-on is now known to matter.**
- **Update `STATUS.md`** for anything that changes state, especially if B1 or M2 voids the noise
  figures.
- **If V3 finds the disc does not fit**, correct `docs/BOM.md` §5 and `CAD/prints/README.md`.
- **`docs/COMPONENTS.md` §12 lists six UNVERIFIED items.** If you have unrestricted network, close
  items 1, 2, 4 and 5 — they are one datasheet page each.

---

# OPTIONAL, IF TIME REMAINS

- **Per-IC decoupling audit** against the netlist. Nothing suggests a problem; it is completeness.
- **A `--tag` convention for `adc_stats.py` captures** that records uptime as well as the change
  being tested. The 2026-09-07 session produced one void capture because a tag did not match the
  actual rail state.
- **Photograph the preamp board top surface** at high magnification before it is retired. It is the
  only record of what contamination on a failed input node looks like, and the board cannot be
  removed from its box.

---

# What is explicitly NOT in scope this session

- ~~**Do not rebuild the preamp board or the tip lead**~~ **Preamp half superseded 2026-09-13:** the
  rebuild went ahead, judged by a meter at PAD1 rather than the ADC. **Still do not rebuild the tip
  lead** until the bare board is measured — safety rule 0b, because the instrument that
  would tell you whether a rebuild helped has a floating reference.
  **Updated 2026-09-09:** this said "that is Sunday's work, when Jacob is home", a stale calendar
  reference. The gate is the floating `PREAMP−`, not the date.
- ~~**Do not solder anything on the preamp until the cleaning supplies arrive.**~~ **CLOSED
  2026-09-14 late — the 99% IPA is in the room and the cleaning kit is complete.** See the gate at the
  top of this file.
- **Do not re-open the piezo.** Built and working. Do not buy Sn42/Bi58 paste.
- **Do not fit a tip.** The zero-risk window is worth keeping.
- **Do not bring the sample plate near the tip holder.**
- **Do not change any firmware constant**, especially the 10.24 V ADC full scale.
- **Do not rebuild the tip lead** until the open-input measurements are finished.
