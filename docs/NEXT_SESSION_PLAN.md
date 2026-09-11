# Next session plan

**Last updated:** 2026-09-11

**This document assumes no memory of any conversation.** Everything needed is here or named by
file. Read `STATUS.md` first for state; this file is the procedure.

> **Written 2026-09-07. Refreshed at the end of every session from 2026-09-09 onward** — `/wrap`
> step 3 updates it, and `check_facts.py` fails if a session log is newer than the date above.
> **Before 2026-09-09 nothing kept it current**, so it sat unmaintained for two days and neither
> Jacob nor Nuh knew it existed.

---

## BEFORE ANYTHING: two gates added 2026-09-09

**1. Do not solder the preamp until the cleaning kit is in the room.** The Chip Quik RMA791 rosin
flux arrived 2026-09-11. Rosin left on this board is a leakage path at the exact node the 119 nA
fault sits on. **Flux without cleaning makes the board worse, not better.**

> **Updated 2026-09-11 — partly closed, not closed.**
>
> **We have IPA and soft brushes.** `SAID`, Jacob, 2026-09-11. **The grade of the IPA and the type
> and count of the brushes are UNKNOWN and must be confirmed before either is used on this board.**
> 91% IPA is 9% water, and that water carries ionic contamination and leaves it as a conducting film
> on the one node that cannot tolerate one; the list calls for **99%**. Stiff bristles scratch
> soldermask. See `docs/INVENTORY.md`.
>
> **Still not owned: lint-free wipes, and foam or polyester swabs.** These are the step that
> *removes* the rosin, and they are not optional. IPA only dissolves it — if the alcohol dries on
> the board the rosin comes back out of solution as a thin film spread over a **wider** area than
> the blob you started with, which is worse, because leakage depends on the area bridged. **Brushes
> lift, IPA dissolves, wipes and swabs carry it off the board.** Swabs specifically reach around the
> standoff, which is the input node itself. Not cotton buds: they shed and hold moisture.
>
> **Distilled water is DOWNGRADED to optional for this flux, and may do harm.** Its stated purpose
> was to take the ionic salts IPA leaves behind — but **RMA791 is ROL0: rosin, low activity,
> halide-free**, which is the whole reason RMA was chosen over RA.
> [`sessions/2026-09-09-jacob.md`](../sessions/2026-09-09-jacob.md) §11.4 already drew this line
> from the other side, calling the water rinse the step that *carries* the risk only for the
> halide-bearing RA alternative. Rosin is also not water-soluble, so water meeting an IPA-and-rosin
> solution can drop the rosin back out as a white bloom. **Confidence: trade sources, not the
> manufacturer's own document — chipquik.com is blocked by the network here, as it was on
> 2026-09-09.** Treat this as a downgrade, not a settled prohibition.
>
> **Copper tape** with conductive adhesive, for H2, is still unbought.

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

## B1. Establish whether the drift is the preamp or the floating reference

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

## B2. Find and bond the open ground — the `PREAMP−` fault

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

## V1. Meter the rebuilt shield's continuity

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

## V4. Read C2's stripe under the magnifier — before any rework, and do not touch C1

**Folded in 2026-09-11 from [`sessions/2026-09-09-jacob.md`](../sessions/2026-09-09-jacob.md) §9,
where it had been recorded and never carried into this plan.**

**Why it matters — and why it is NOT a blocker.** JLCPCB raised a C1/C2 polarity question at order
time and how it was answered is unknown. **C2 polarity cannot be the 119 nA** and that is settled by
argument in §6.1 of that log: `N$4` has exactly one connection in the whole design (`IC1.-IN`), C2
connects −15 V to GND and touches neither, and **C2's pads sit at −15 V and 0 V whichever way the
part faces** — so the surface-leakage map toward the input pad is identical either way. It does not
explain the warm-up drift either: C2 is **7.1 mm** from IC1, and a 6032 part settles thermally in a
minute or two, not 45.

**Procedure.** Two minutes with the magnifier. **Read the stripe.** That is the only thing that
settles it — **continuity testing cannot detect capacitor polarity** (§6.2: a capacitor is a DC open
both ways, and buzzing the pads only tells you which net each is on, which is the same either way).

**Expected.** Stripe consistent with the footprint. **If it is reversed:** record it, do not rework
it during a diagnosis. **Do not re-rank the 119 nA candidates because of C2** — the superglue at the
PTFE standoff remains the lead.

**Record.** What the stripe shows, and a photo through the magnifier.

## V5. Calipers on the Keystone 11301 and on the board hole, when the 11301 arrives

**Folded in 2026-09-11 from the same §9.** **Arrival date UNKNOWN** — it was on order as of
2026-09-09.

**Why it matters.** The 11301's own mounting-hole spec is **disputed and marked VERIFY** in
[`docs/FACTS.md`](FACTS.md): it is recorded as Ø2.184 mm (0.086"), but **0.086" is also listed as
that part's turret-head diameter**, and a PTFE-insulated terminal's hole must clear its insulator,
so both cannot be true. Every attempt to reach Keystone, DigiKey, Mouser, RS and Octopart on
2026-09-09 was blocked by the network, and distributor snippets contradict each other. **One
measurement with calipers closes it.**

**Procedure.** Measure the part's actual mounting-hole diameter and the board's actual standoff
hole. The board hole is **Ø2.108 mm NPTH** at (2.540, 7.620) per the netlist.

**Decision.** Press fit, clearance, or interference — and whether the **#44 drill (2.184 mm)** is
needed. **Do not open the hole beyond 2.184 mm.** See the do-not list at the end of this file.

**Record.** Both numbers, into [`docs/FACTS.md`](FACTS.md), replacing the VERIFY row.

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

## H3. Prepare the tip lead in fine wire

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

## M1. Repeat the bias, Z and rail sweeps with a meter on PAD1

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

## M2. A noise capture with the meter, not the ADC

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
- **Fill in the gaps in [`docs/INVENTORY.md`](INVENTORY.md).** **Folded in 2026-09-11 from
  [`sessions/2026-09-09-jacob.md`](../sessions/2026-09-09-jacob.md) §9.** Open ones: **which other
  parts JLCPCB left off the preamp PCBA**, **how the C1/C2 polarity question was answered at order
  time**, **whether we own copper tape**, and the **grade of the IPA and type/count of the brushes**
  added 2026-09-11. **These facts live in Jacob and Nuh's heads and in their email — anything left
  in conversation is lost at the next compaction.** `CLAUDE.md` §3d.
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

- **Do not rebuild the preamp board or the tip lead** — safety rule 0b, because the instrument that
  would tell you whether a rebuild helped has a floating reference.
  **Updated 2026-09-09:** this said "that is Sunday's work, when Jacob is home", a stale calendar
  reference. The gate is the floating `PREAMP−`, not the date.
- **Do not solder anything on the preamp until the cleaning supplies arrive** — see the gate at the
  top of this file.
- **Do not re-open the piezo.** Built and working. Do not buy Sn42/Bi58 paste.
- **Do not fit a tip.** The zero-risk window is worth keeping.
- **Do not bring the sample plate near the tip holder.**
- **Do not change any firmware constant**, especially the 10.24 V ADC full scale.
- **Do not rebuild the tip lead** until the open-input measurements are finished.

**Three more, folded in 2026-09-11 from
[`sessions/2026-09-09-jacob.md`](../sessions/2026-09-09-jacob.md) §9:**

- **Do not rotate or replace C1.** It is correctly connected.
- **Do not open the standoff hole to fit the 11311.** The hole is 2.540 mm from the board edge; at
  the 11311's Ø3.45 mm only **0.815 mm** of material would remain, directly under the one component
  the instrument's sensitivity depends on. **The 11311 does not fit and is not going to** — the
  11301 is on order. `docs/FACTS.md`.
- **Do not treat C2 as a candidate for the 119 nA.** Ruled out by argument in §6.1 of that log.
  Read its stripe (V4), record what you see, and leave the candidate ranking alone.
