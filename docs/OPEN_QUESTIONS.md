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
| **Is the 37 nA offset the cyanoacrylate contamination or the ungrounded case shield?** | Decides whether the spare preamp board gets consumed. Grounding the shield is one reversible wire; the rebuild is not reversible | `STATUS.md` §1, §1b |
| **Is the DAC configuration loss startup-only, or does it recur mid-session?** | 2026-08-31 recorded it recurring every 30–60 min, which means checking LED1–LED4 around every single measurement. If it is startup-only, one `RSET` at the start is enough | `sessions/2026-08-31-results.md` §4 |
| **Does the AD5761R have internal pull-ups on CLEAR# and RESET#?** | Both are marked no-connect on all four DACs. If there are no internal pull-ups, four floating active-low resets glitching together explains the whole fault, and the fix is four wires to 3.3 V. **Datasheet question, nobody has looked** | `docs/UPSTREAM_MECHPANDA.md` §4b |
| **Is the LTC2326-16 output signed or straight binary?** | The firmware reads `int16_t`. If the part is unipolar straight-binary, every reading above 32767 appears negative, and the "-400 count baseline" would really be 65136 — near full scale. **This changes the meaning of every ADC number in the project.** Datasheet question | `Code/teensy/lib/LTC2326/` |
| **What causes the DAC configuration loss at all?** | Root cause unknown. U16 is not hot, which weakens the thermal-shutdown theory. LED1–4 lighting proves 3.3 V is present when you look, so any rail explanation needs a brief dip that recovered. A video of the LEDs flickering was recorded and is preserved in git history at `Code/teensy/IMG_7846.mov`, commit `4819a31` — recover it with `git show 4819a31:Code/teensy/IMG_7846.mov > flicker.mov` if it ever becomes useful | `sessions/2026-08-31-results.md` §4 |
| **Confirm the 4.096 V full scale with one meter reading** | The schematic settles that the ADC uses its internal reference, so 4.096 is right and 10.24 is wrong. What remains is a simultaneous R23-vs-`ADCR` reading, and checking the datasheet's full-scale-to-REFBUF relationship, before the Python constant is changed | `docs/UPSTREAM_MECHPANDA.md` §1 |
| **What is the sign of the tunneling current?** | **No longer blocks the approach** — `Code/pc/stm_approach.py` thresholds on absolute deviation and does not care about the sign. Still needed to make the firmware's `APRH` safe, and still worth knowing. The dummy junction test answers it | `STATUS.md` |
| **Which sign of `MTMV` advances the tip toward the sample?** | `stm_approach.py` refuses to run without it. Determinable by eye with the tip removed | `Code/pc/stm_approach.py` |
| **How do we mount the gold foil?** | Decided 2026-09-05 to use gold foil. It needs to be flat and electrically continuous with the bias magnet, or it moves under the tip and looks like drift | `docs/UPSTREAM_BERARD.md` §5 |

---

## 2. Needed before first imaging

| Question | Why it matters |
|---|---|
| ~~Is the scan head shield cover wrapped and grounded?~~ | **Answered 2026-09-06.** Printed, wrapped in copper, grounded. Reported by Jacob, not independently metered. Distinct from the preamp box shield |
| **Is the rebuilt preamp box shield continuous?** VERIFY | Every preamp conclusion next session depends on it. Two minutes with a meter |
| **What is our scan head's lever reduction ratio?** VERIFY | Berard quotes **20 on one page and 30 on another**, giving 7.8 or 5.2 nm/step. Both are comfortable, so this is no longer urgent. Measurable from `CAD/prints/scan-head/`: (front-screw-line to tip) ÷ (front-screw-line to rear screw) |
| **How does the tip mount, and is it insulated from the brass electrode?** | Berard uses a pin socket in an aluminium standoff on a **sapphire disk**, and warns that glue must not bridge standoff to the grounded brass plate. We have no documented tip mounting at all. Meter-check before imaging |
| **Which Z direction is toward the sample?** | Only resolvable at first tunneling, or from the CAD. Park Z at midscale meanwhile, which is safe either way |
| **Which piezo quadrant is which?** | The four wires are identical bare enamelled copper with no colour code. Not recoverable from any file or photo — label them as you solder, or work it out empirically. A rotated or mirrored first image is this, and it is fixable in software |
| **Is the rebuilt preamp case shield continuous?** VERIFY | The old wrap was aluminium and copper mixed, and it was **found discontinuous on 2026-09-06** — aluminium's adhesive does not conduct, so the overlaps were open. It was stripped and rebuilt in copper with soldered seams. **The rebuild has not been metered.** Every point on it must beep to the ground wire: near the wire, the far corner, across every seam |
| ~~**Are the copper and aluminium tape in contact anywhere?**~~ | **Resolved by removing the aluminium.** The rule now is copper only, everywhere — `docs/ENGINEERING_REFERENCE.md` §3. If aluminium ever goes back on, this question comes back with it |

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
| **Piezo disc** | 25–27 mm brass, 15–17 mm ceramic, 15000 pF ±30%. **Berard uses a Murata 7BB-20-6** (20 mm, 6.3 kHz, Digi-Key 490-7711-ND) — a known-good reference part, but **not ours**, ours is larger | Our part number and supplier |
| **Piezo-to-plate adhesive** | Berard glues an aluminium standoff to a **sapphire disk**, and that to the brass electrode. He names no adhesive but says the insulator must be sapphire, glass or ceramic — **not plastic** — because it is a better insulator than the glue | The adhesive itself, still unnamed anywhere |
| **Tip lead: coax or fine wire?** | We chose RG-178. **Berard uses plain 40 AWG wire** deliberately — stiff cable transmits vibration | Which is better here. Untested either way |

---

## 4. Undocumented — process

| Item | What we know | What we don't |
|---|---|---|
| **Soldering iron temperature and dwell for the piezo joints** | Low-temp Sn42/Bi58 paste at ~138 °C, ultra-fine wire. **Depolarisation happens above about 210 °C** internal temperature. An independent builder avoids heat entirely with **conductive epoxy (MG Chemicals 9410)** | Actual iron temperature and dwell for our discs. The epoxy alternative is untested by us. See `docs/OTHER_BUILDERS.md` §2 |
| **DST-201 DC input impedance** | — | Needed to finish some of the high-impedance arithmetic |

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
| Is the ADC full scale 4.096 or 10.24 V? | **4.096.** The LTC2326 runs on its internal reference; no external reference reaches it. One meter check still outstanding | 2026-09-05 |
| Do the DAC ALERT pins reach the Teensy? | **No.** The schematic's H1 net list has no ALERT line. LEDs are the only indication — documented now, not inferred | 2026-09-05 |
| Is `logTable` correct? | **Yes, by construction.** The generating MATLAB is in the file header: 0-32768 in, 0-524287 out | 2026-09-05 |
| Has anyone else built Mech Panda's STM? | **No public replication found.** No build logs, forum threads or repos. We may be first | 2026-09-05 |

---

## How to help

If you have built a similar instrument and know any of the section 3 or 4 answers, an issue
saying so would be genuinely useful — those are the items where we are guessing or have simply
chosen something that works.

For section 1 and 2, we are working on them ourselves and progress appears in `sessions/`.
