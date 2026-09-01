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
| **What causes the DAC configuration loss at all?** | Root cause unknown. U16 is not hot, which weakens the thermal-shutdown theory. LED1–4 lighting proves 3.3 V is present when you look, so any rail explanation needs a brief dip that recovered. A video of the LEDs flickering was recorded and is preserved in git history at `Code/teensy/IMG_7846.mov`, commit `4819a31` — recover it with `git show 4819a31:Code/teensy/IMG_7846.mov > flicker.mov` if it ever becomes useful | `sessions/2026-08-31-results.md` §4 |
| **Is the ADC full scale 4.096 V or 10.24 V?** | `LTC2326_16.hpp` says 4.096; `stm_control.py:37` and `stm_console.py` say 10.24. **Every current figure in the project depends on this.** The R23 reading favours 4.096 but is not a calibration | `STATUS.md` |
| **What is the sign of the tunneling current?** | Makes `APRH` safe to think about. Until it is known, an automated approach can drive the tip into the sample without ever triggering. The dummy junction test answers it | `STATUS.md` |
| **Do we have a sample material?** HOPG, gold on mica, anything | You cannot image without one. `BOM.md` lists a mounted HOPG part number as CONFIRMED from a photographed label, but whether we actually have it is unconfirmed | `BOM.md` §5 |

---

## 2. Needed before first imaging

| Question | Why it matters |
|---|---|
| **How far does one motor step move the tip, in nm?** | One step must move less than the Z piezo range, or an approach is a crash regardless of the electronics. Needs the screw pitch and any lever reduction from the CAD |
| **Which Z direction is toward the sample?** | Only resolvable at first tunneling, or from the CAD. Park Z at midscale meanwhile, which is safe either way |
| **Which piezo quadrant is which?** | The four wires are identical bare enamelled copper with no colour code. Not recoverable from any file or photo — label them as you solder, or work it out empirically. A rotated or mirrored first image is this, and it is fixable in software |
| **Is the preamp case shield continuous?** VERIFY | Aluminium tape adhesive is usually non-conductive, so overlapping strips may not connect to each other at all. Meter check |
| **Are the copper and aluminium tape in contact anywhere?** VERIFY | In contact with humidity they form a galvanic cell. Meter check while the box is open |

---

## 3. Undocumented in every source — hardware

Nobody has ever written these down, in Mech Panda's files, Dan Berard's, or ours.

| Item | What we know | What we don't |
|---|---|---|
| **Plate-to-plate screws** | M3 elsewhere in the build | Exact sizes |
| **Motor-mount screws** | — | Sizes |
| **Extension springs** | About 300 mm long, 3 of them | **Spring rate** |
| **Damping magnets** | Rectangular, **18** of them | Individual dimensions |
| **Sample pocket magnets** | Small discs, 4 of them | Dimensions |
| **Aluminium damping plate** | Eddy-current damping | Thickness |
| **Heat-set inserts** | Brass, about 10, for PETG-CF | Sizes |
| **Piezo disc** | 25–27 mm brass, 15–17 mm ceramic, 15000 pF ±30% | **Part number and supplier** |
| **Piezo-to-plate adhesive** | — | What it is |
| **Miniature coax** | RG-178 or RG-316 was our choice | Never specified upstream. Length also unspecified |

---

## 4. Undocumented — process

| Item | What we know | What we don't |
|---|---|---|
| **Soldering iron temperature and dwell for the piezo joints** | Low-temp Sn42/Bi58 paste at ~138 °C, ultra-fine wire | Actual iron temperature and how long to dwell. The original designer destroyed 4 or 5 discs learning this |
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

---

## How to help

If you have built a similar instrument and know any of the section 3 or 4 answers, an issue
saying so would be genuinely useful — those are the items where we are guessing or have simply
chosen something that works.

For section 1 and 2, we are working on them ourselves and progress appears in `sessions/`.
