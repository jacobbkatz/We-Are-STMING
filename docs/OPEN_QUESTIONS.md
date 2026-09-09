# Open questions

Every unresolved item in the project, in one place. Previously these were scattered across
`STATUS.md`, `BOM.md` and `START_HERE_gotchas.md`.

**These are not oversights.** Each one is either genuinely undocumented in every source we could
find, or not yet measured. They are flagged rather than guessed on purpose, because a confident
wrong number is worse than an admitted gap.

**If you work one of these out, please open an issue.** Closing these gaps is most of what this
project is for.

---

## 1. Blocking the build

These stop progress right now.

| Question | Why it matters | Where |
|---|---|---|
| **Is the 119 nA offset the cyanoacrylate contamination or the ungrounded case shield?** | Decides whether the spare preamp board gets consumed. Grounding the shield is one reversible wire; the rebuild is not reversible | `STATUS.md` §1, §1b |
| **Is the DAC configuration loss startup-only, or does it recur mid-session?** | 2026-08-31 recorded it recurring every 30–60 min, which means checking LED1–LED4 around every single measurement. If it is startup-only, one `RSET` at the start is enough | `sessions/2026-08-31-results.md` §4 |
| **What is the Keystone 11301's actual mounting-hole diameter?** | Added 2026-09-09. `docs/FACTS.md` records Ø2.184 mm (0.086"), **but 0.086" is also listed as the part's turret-head diameter**, and a PTFE-insulated terminal's hole must clear its insulator, so both cannot be right. Every distributor and manufacturer site was unreachable from this network on 2026-09-09. Decides whether the board hole has to be opened to #44. **Fastest route: calipers on the part when it arrives, and on the board hole** | `docs/FACTS.md` |
| **Which parts did JLCPCB leave off the preamp PCBA, beyond the 100 MΩ and the standoff?** | Added 2026-09-09. Decides what has to be hand-fitted before the spare board can be used. **Fastest route: the JLCPCB order confirmation email, or look at the spare board** | `docs/INVENTORY.md` |
| **How was JLCPCB's C1/C2 polarity question answered at order time?** | Added 2026-09-09. Jacob: they could not determine it and asked. The board has **no silkscreen polarity marking**, so there was nothing for them to work from. Answering this from the order thread would settle fault 1d without needing the boards in hand. **Not blocking** — C2 polarity cannot cause the 119 nA | `STATUS.md` fault 1d, `docs/INVENTORY.md` |
| ~~**Does the AD5761R have internal pull-ups on CLEAR# and RESET#?**~~ **ANSWERED 2026-09-07** | **Yes. `RESET` and `LDAC` both have internal pull-ups and may be left floating** — read from the datasheet. **So the floating-pin hypothesis is very likely wrong and the wire fix is unnecessary.** The symptom is power sequencing, explained in full in `docs/PROJECT_HANDOFF_SUMMARY.md` lines 476–495. Still open only for `CLR` specifically, which does not change the conclusion | `docs/COMPONENTS.md` §2 |
| **Is the LTC2326-16 output signed or straight binary?** | The firmware reads `int16_t`. If the part is unipolar straight-binary, every reading above 32767 appears negative, and the "-400 count baseline" would really be 65136 — near full scale. **This changes the meaning of every ADC number in the project.** Datasheet question | `Code/teensy/lib/LTC2326/` |
| **What causes the DAC configuration loss at all?** | Root cause unknown. U16 is not hot, which weakens the thermal-shutdown theory. LED1–4 lighting proves 3.3 V is present when you look, so any rail explanation needs a brief dip that recovered. A video of the LEDs flickering was recorded and is preserved in git history at `Code/teensy/IMG_7846.mov`, commit `4819a31` — recover it with `git show 4819a31:Code/teensy/IMG_7846.mov > flicker.mov` if it ever becomes useful | `sessions/2026-08-31-results.md` §4 |
| ~~**Confirm the ADC full scale**~~ **CLOSED 2026-09-07** | **It is ±10.24 V**, from the LTC2326-16 datasheet: REFBUF is 4.096 V and the input span is 2.5 × REFBUF. The PC tools were right; `docs/UPSTREAM_MECHPANDA.md` §1 argued for 4.096 and was wrong. **Also closed from the same page: the output is two's complement.** | `docs/UPSTREAM_MECHPANDA.md` §1 |
| **What is the sign of the tunneling current?** | **No longer blocks the approach** — `Code/pc/stm_approach.py` thresholds on absolute deviation and does not care about the sign. Still needed to make the firmware's `APRH` safe, and still worth knowing. The dummy junction test answers it | `STATUS.md` |
| **Which sign of `MTMV` advances the tip toward the sample?** | `stm_approach.py` refuses to run without it. Determinable by eye with the tip removed | `Code/pc/stm_approach.py` |
| **How do we mount the gold foil?** | Decided 2026-09-05 to use gold foil. It needs to be flat and electrically continuous with the bias magnet, or it moves under the tip and looks like drift | `docs/UPSTREAM_BERARD.md` §5 |

---

## 2. Needed before first imaging

| Question | Why it matters |
|---|---|
| ~~Is the scan head shield cover wrapped and grounded?~~ | **Answered 2026-09-06.** Printed, wrapped in copper, grounded. Reported by Jacob, not independently metered. Distinct from the preamp box shield |
| **Is the rebuilt preamp box shield continuous?** VERIFY | Every preamp conclusion next session depends on it. Two minutes with a meter |
| **Does U13's floating op-amp channel misbehave?** | **New 2026-09-06.** U13 pins 5, 6, 7 — the whole unused half of the OPA2227P whose other half drives the sample bias — are connected to nothing. Scope pin 7: a quiet DC level is fine, a rail or an oscillation is not. Fix is two wires, pin 6 to pin 7 and pin 5 to AGND. See `STATUS.md` fault 4b |
| **What is our scan head's lever reduction ratio?** VERIFY | Berard quotes **20 on one page and 30 on another**, giving 7.8 or 5.2 nm/step. **Measured from `PiezoPlate.stl` on 2026-09-06:** the front screw pair sits on a line **40.000 mm** from the rear screw, and the piezo pocket centre is **1.000 mm** in front of that line. If the front pair is the pivot and the rear screw is driven, the ratio is **40**, i.e. **3.88 nm/step**. Exact round numbers, so probably design intent — but it assumes the tip is at the disc centre and the rear screw is the driven one. **Both are readable off the assembled instrument with a ruler in a minute.** Still nothing depends on it: 20, 30 and 40 all give 90–130 steps across the Z range |
| **How does the tip mount, and is it insulated from the brass electrode?** | Berard uses a pin socket in an aluminium standoff on a **sapphire disk**, and warns that glue must not bridge standoff to the grounded brass plate. We have no documented tip mounting at all. Meter-check before imaging |
| **Which Z direction is toward the sample?** | Only resolvable at first tunneling, or from the CAD. Park Z at midscale meanwhile, which is safe either way |
| **Which piezo quadrant is which?** — **not blocking, and not worth asking about.** The scanner is built and working (`docs/INVENTORY.md`) | The four wires are identical bare enamelled copper with no colour code. Not recoverable from any file or photo — label them as you solder, or work it out empirically. A rotated or mirrored first image is this, and it is fixable in software. **If they were not labelled, nothing is lost that a first image cannot recover — but nobody should spend bench time looking for a record that was never made** |
| **Is the rebuilt preamp case shield continuous?** VERIFY | The old wrap was aluminium and copper mixed, and it was **found discontinuous on 2026-09-06** — aluminium's adhesive does not conduct, so the overlaps were open. It was stripped and rebuilt in copper with soldered seams. **The rebuild has not been metered.** Every point on it must beep to the ground wire: near the wire, the far corner, across every seam |
| ~~**Are the copper and aluminium tape in contact anywhere?**~~ | **Resolved by removing the aluminium.** The rule now is copper only, everywhere — `docs/ENGINEERING_REFERENCE.md` §3. If aluminium ever goes back on, this question comes back with it |

---

| **Is the recorded noise real, or is it the floating reference?** | **New 2026-09-07.** The measured 195 mV RMS is ~1,700x the 100 MΩ's Johnson noise and ~10,000x the OPA627's contribution — neither device explains it. **If it is the floating `PREAMP−`, every noise figure in the project is void**, including "the shield halved the noise". **Two-minute test: watch PAD1 on a meter while the ADC scatters** | `docs/NEXT_SESSION_PLAN.md` M2 |
| **Is the warm-up drift the preamp or the reference?** | **New 2026-09-07.** 25,000 counts over an hour. Decides whether every future capture must wait an hour. **Test: meter PAD1 at 10 and 60 minutes** | `docs/NEXT_SESSION_PLAN.md` B1 |
| **What is the preamp's input capacitance?** | **New 2026-09-07.** Sets the TIA's stability margin and noise gain. Estimated at ~20 pF, never measured. **No compensation capacitor is fitted — stability rests entirely on the feedback resistor's stray capacitance** | `docs/COMPONENTS.md` §4 |
| **LTC2326-16 required SPI mode** | The driver uses `SPI_MODE2` on SPI1 and demonstrably returns sane data, but it has never been checked against the datasheet's timing requirement. One datasheet page | `docs/COMPONENTS.md` §3 |
| **Per-IC decoupling audit** | 25 × 100 nF and 14 × 10 µF are fitted but have never been cross-checked against each IC's supply pins. **Nothing observed suggests a problem** — completeness only. Cross-reference `FlyingProbeTesting.json` against the pinouts | `docs/COMPONENTS.md` §9 |
| **OPA2227 output swing at ±15 V** | The Z+X headroom argument rests on approximately ±13 V. One datasheet page | `docs/COMPONENTS.md` §5 |
| ~~**Keystone 11301 mounting hole diameter**~~ **ANSWERED 2026-09-08** | **Ø2.184 mm (0.086")**, from the manufacturer data. Our board hole is Ø2.108 mm, so the 11301 is a **press fit with 0.076 mm interference** — correct for a press-fit part, but tighter than Keystone's recommended hole. **The 11311 we own needs Ø3.45 mm and does not fit at all.** Remaining sub-question: whether the press seats without opening the hole to #44. See the guide | `docs/FACTS.md` |
| **Which op-amp is actually fitted — OPA627AU or OPA124U?** VERIFY, **blocks nothing** | **New 2026-09-08.** `docs/BOM.md` says **OPA627AU**; the Eagle source we build from says **OPA124U**. **Nobody has read the marking on our own board** — a photo that appeared to settle it turned out to be Dan Berard’s board, not ours. Changes the TIA stability margin (~7x vs ~2x) but **not** the leakage conclusion, since both parts have ~1 pA bias current. **Narrowed 2026-09-09: this is now expected, not a discrepancy.** The PCB is Berard’s design, so its Eagle source and schematic naturally say `OPA124U`. **But our parts follow Mech Panda, and Mech Panda used the OPA627AU** — which is almost certainly what `BOM.md`’s CONFIRMED rests on. Berard explicitly endorses the swap. **Both parts work in this circuit:** ~1 pA bias current either way, and the TIA is stable either way (~7x margin for the OPA627, ~2x for the OPA124). **So nothing is blocked.** Read the marking when convenient, to pin the stability margin. | `docs/COMPONENTS.md` §4 |
| **How is C2 fitted on the existing preamp board?** | **New 2026-09-08.** The Eagle source wires **C2's tantalum anode to −15 V and its cathode to GND — reverse-biased by the full rail.** It is an upstream design error, not a build fault. **Nobody has looked at how the physical board is populated.** One minute with a magnifier before that board is retired, and it is a candidate for unexplained negative-rail behaviour | `docs/FACTS.md` |
| **Does PETG-CF's dissipative surface matter at the input node?** | **New 2026-09-08.** Carbon-fibre-filled filament is **static-dissipative**, not insulating — roughly 10⁴–10¹¹ Ω/sq against ~10¹⁵ for unfilled polymer, and the box standoffs touch the board. **Probably not the DC offset** — a dissipative path to a grounded box cannot push current when both ends sit at 0 V — but it is a hard constraint on the rebuild and a possible noise contributor. **Not worth bench time chasing** | `docs/FACTS.md` |
| **LTC2326-16 absolute maximum input, verbatim** | ±16.5 V is taken from the sibling LTC2326-18. Good margin against our 11.9 V, but not confirmed for our exact part. One datasheet page | `docs/COMPONENTS.md` §3 |

---

## 3. Undocumented in every source — hardware

Nobody has ever written these down, in Mech Panda's files, Dan Berard's, or ours.

> **Screw sizes are no longer unknown.** Measured from the STL meshes on 2026-09-06;
> `CAD/prints/README.md` has the full table and `Code/pc/stl_features.py` is the tool.

| Item | What we know | What we don't |
|---|---|---|
| ~~**Plate-to-plate screws**~~ **CLOSED 2026-09-06** | **M3.** `BasePlate` dia 3.200 clearance with a dia 7.000 × 4.0 counterbore, into `5_intermediate_baseplate`'s dia 2.500 self-tapping holes on the same grid. Measured from the meshes | nothing |
| ~~**Motor-mount screws**~~ **CLOSED 2026-09-06** | **M3.** `MotorSupport` has 3 × dia 3.400 full-height holes at 21.2 mm pitch | nothing |
| **Extension springs** | About 300 mm long, 3 of them | **Spring rate** |
| **Damping magnets** | Rectangular, **18** of them | Individual dimensions |
| **Sample pocket magnets** | Small discs, 4 of them | Dimensions |
| **Aluminium damping plate** | Eddy-current damping | Thickness |
| **Heat-set inserts** | Brass, about 10, for PETG-CF. **But no measured part has a hole that fits a standard M3 insert** (those need about dia 4.0–4.6). Every printed joint measured so far is a screw self-tapping into a dia 2.5 or dia 1.6 pillar | Sizes, and **whether they are needed at all**. Do not buy until a part is found that wants one |
| **Piezo disc** | 25–27 mm brass, 15–17 mm ceramic, 15000 pF ±30%. **Berard uses a Murata 7BB-20-6** (20 mm, 6.3 kHz, Digi-Key 490-7711-ND) — a known-good reference part, but **not ours**, ours is larger | Our part number and supplier. **AND, new 2026-09-06: whether it fits at all.** The `PiezoPlate` seat measures **Ø20.500 mm**, which takes a 20 mm disc, not a 25–27 mm one. Measure the disc and the pocket with calipers. Changes both the fit and every nm/V figure |
| ~~**Print material**~~ **CLOSED 2026-09-07** | **PETG-CF**, confirmed directly by Jacob. The `.3mf` plates record an abandoned PA-CF attempt, exactly as suspected | nothing. Good news too: PETG-CF takes up far less moisture than nylon |
| **Isolation stage** | 3 rods, 3 hangers of each of 3 lengths, 3 springs ~300 mm, 3 coin-weight cups, 18 magnets + an aluminium plate for eddy damping | **Is it assembled and hanging?** And the **static droop of the springs** — that one ruler measurement gives the resonant frequency directly, without needing the spring rate or the mass. See `docs/ENGINEERING_REFERENCE.md` §7b |
| **Cable routing off the suspended platform** | Nothing recorded anywhere | **How the ribbon and coax leave the platform.** A taut cable to the bench defeats the springs completely — it is the most common way a good isolation stage is ruined, and this repository has never described it |
| **Piezo-to-plate adhesive** | Berard glues an aluminium standoff to a **sapphire disk**, and that to the brass electrode. He names no adhesive but says the insulator must be sapphire, glass or ceramic — **not plastic** — because it is a better insulator than the glue | The adhesive itself, still unnamed anywhere |
| ~~**Tip lead: coax or fine wire?**~~ **DECIDED 2026-09-07: plain fine wire** | The coax ran only 1–2 cm before becoming bare copper, so it shielded a fraction of the exposed node; it likely loads the flexing piezo disc; it doubles the solder joints on the input node; and Jacob reports it was hard to strip and solder. **Difficulty at that node is itself a fault source** in a build whose blocker is contamination there. Berard uses 40 AWG for the same mechanical reason. Full reasoning in `docs/UPSTREAM_BERARD.md` §4 | Nothing blocking. **Do the open-input measurement BEFORE rebuilding the lead** — the cut coax is what makes that test possible |
| **The part number for our fine screws** | 1/4"-80, same precision as upstream but **about 30 mm longer**. The 97424A590 in the CAD is **Mech Panda's**, not ours | The actual McMaster number. Thread is unchanged so the physics holds; the extra 30 mm costs stiffness and adds ~0.33 µm/°C to the loop |

---

## 4. Undocumented — process

| Item | What we know | What we don't |
|---|---|---|
| ~~**Soldering iron temperature and dwell for the piezo joints**~~ **MOOT 2026-09-09 — the piezo is built.** Kept because the reasoning applies to any future disc | **Largely closed 2026-09-09 by the argument below — the remaining unknown is narrow.** Alloy, melt point and the depolarisation ceiling are in [`docs/FACTS.md`](FACTS.md). An independent builder avoids heat entirely with **conductive epoxy (MG Chemicals 9410)** | **Only this: how far the FX-888DX's displayed temperature differs from the real tip temperature.** We own no tip thermometer. Dwell is no longer critical — see below. The epoxy alternative is untested by us. See `docs/OTHER_BUILDERS.md` §2 |
| **DST-201 DC input impedance** | — | Needed to finish some of the high-impedance arithmetic |

> ### Why the iron temperature is now mostly a settled question
>
> **Added 2026-09-09, remote, no hardware.** This had been open since 2026-09-05 as "actual iron
> temperature and dwell for our discs". It is largely answerable from arithmetic we already had.
>
> **The argument.** The iron tip is the only source of heat in the assembly. Heat flows from hot to
> cold, so in the steady state **no part of the disc can end up hotter than the tip**. Set the tip
> below the depolarisation ceiling and the ceramic physically cannot reach it, **no matter how long
> the iron is held there.** That converts the problem from "how long may I dwell" — which nobody
> could answer without instrumenting a disc — into "what do I set the dial to", which is one number.
>
> The window is generous: the alloy melts at 138 C, the ceramic depolarises around 210 C, so
> anything in between works. **Set the station to 190 C.** That is 52 C above the melt, which is
> ample for wetting, and 20 C below the ceiling. Values in [`FACTS.md`](FACTS.md).
>
> **What is still VERIFY, and it is the whole of the remaining risk.** A soldering station's
> **displayed** temperature is not its **tip** temperature. Tip geometry, wear, oxidation and
> calibration drift all move the real figure, and the FX-888DX has no external calibration
> reference unless you own a tip thermometer. **We do not.** A station reading 20 C low would put
> the tip at 210 C — exactly on the ceiling.
>
> **So the 20 C margin is the thing to protect, and the way to protect it is a test disc.** Buy
> spare discs (`docs/BOM.md` §5 already says five or more) and sacrifice one: make joints on it at
> 190 C, then check it still moves. **A ruined disc still reads correctly on a meter** — see
> `docs/START_HERE_gotchas.md` — so the test has to be mechanical or acoustic, not a resistance
> check.
>
> **This replaces "low temperature and short dwell" as the technique.** Short dwell was a proxy for
> keeping the ceramic cool, and it is a bad proxy: it puts a beginner under time pressure at a
> joint that needs care. **Set the dial correctly and take your time instead.**


---

## 5. Answered — kept so nobody re-opens them

| Question | Answer | Settled |
|---|---|---|
| Is the preamp feedback loop open? | **No, it is closed.** It settles rather than ramping. An open feedback resistor would make it an integrator and pin it against 32767 within two minutes | 2026-08-31 |
| Does the bias path to the sample work? | **Yes.** −3 V at the sample holder for `BIAS 65535`, gain −1 as per schematic | 2026-08-31 |
| Is there a piezo resonance to drive at? | **No usable one when mounted.** A 1–11 kHz sweep found no loudness peak. The 8.6 kHz figure is a free-air buzzer spec | 2026-08-31 |
| Is one JP1 ground pin open? | **Yes.** The earlier retraction of this finding was itself wrong | 2026-08-31 |
| What are the X and Y DAC ranges? | **±3 V**, not the ±5 V the firmware comments claim. Same mode bits as bias, which measures ±3 V | verified by measurement |
| What plugs into the power input? | **JST XH 3-pin.** Pin 1 V--, pin 2 ground, pin 3 V++. Feed it ±18 V | `BOM.md` |
| Does ribbon pin 6 get connected? | **Yes.** Labelled ADC_SDI but it is RDL, a read-enable. Wire it to Teensy pin 38 | `docs/WIRING.md` |
| Is `logTable[abs(adc)]` an out-of-bounds bug? | **No, it is safe.** The table is `[32769]`. Do not "fix" it | 2026-08-31 |
| What sample will we image? | **Gold foil.** Expect atomic terraces, not individual atoms — Berard could not resolve single atoms on metals, attributing it to acoustic noise | 2026-09-05 |
| Which PTFE standoff? | **Keystone Electronics 11301**, the part Berard names | 2026-09-05 |
| Roughly how far does one motor step move the tip? | **~7.8 nm**, from 1/4"-80 pitch ÷ 2048 steps ÷ ~20x lever. Comfortable against a ~700 nm Z range. Lever ratio still VERIFY | 2026-09-05 |
| Why do `SERIAL_LED 0` and `TUNNEL_LED 1` exist if nothing uses them? | Berard drives an LED on pin 0 for serial activity and pin 1 for tunneling. Inherited definitions | 2026-09-05 |
| Is the ADC full scale 4.096 or 10.24 V? | **10.24 V**, from the datasheet 2026-09-07. 4.096 V is REFBUF; the input span is 2.5 × REFBUF. **This row previously said 4.096 and was wrong** | 2026-09-07 |
| Do the DAC ALERT pins reach the Teensy? | **No.** The schematic's H1 net list has no ALERT line. LEDs are the only indication — documented now, not inferred | 2026-09-05 |
| Is `logTable` correct? | **Yes, by construction.** The generating MATLAB is in the file header: 0-32768 in, 0-524287 out | 2026-09-05 |
| Has anyone else built Mech Panda's STM? | **No public replication found.** No build logs, forum threads or repos. We may be first | 2026-09-05 |

---

## How to help

If you have built a similar instrument and know any of the section 3 or 4 answers, an issue
saying so would be genuinely useful — those are the items where we are guessing or have simply
chosen something that works.

For section 1 and 2, we are working on them ourselves and progress appears in `sessions/`.
