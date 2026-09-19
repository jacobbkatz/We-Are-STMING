# Inconsistencies found while writing the manual

**Found 2026-09-19 by reading the whole documentation set, the firmware and the PC tools against
each other.** Every item gives the file, the line, what it says, what it should say, and what the
evidence is.

**Nothing here has been fixed.** The manual owns only
`deliverables/2026-09-19-pause/manual/**`; these are all in files owned by someone else.

**Severity:**

- **A — can cost hardware or a bench session.** Fix before the next bench day.
- **B — will mislead a reader about what the instrument is or does.**
- **C — tidiness, or an UNKNOWN that has since been answered elsewhere.**

**`python3 Code/pc/check_facts.py` exits 0 on the repository as it stands**, so none of these is
something the existing guard can catch. That is the point of listing them.

---

## A — fix before the next bench session

### A1. `docs/COMMANDS.md:113` says the approach tool does not exist

> `Code/pc/stm_approach.py` is planned but **not yet written.**

**It exists, it has 40 passing tests, and it has been the only approach route used at the bench
since 2026-09-16.** `docs/COMMANDS.md` is the command reference a bench session reads, and this
sentence sits directly under the warning not to use `APRH`. **So a reader who believes it is left
with no alternative to the one command the project forbids.**
**`STATUS.md` safety rule 2 bars it until the sign of the tunneling current is known.**

**Recommended fix:** replace the sentence with a pointer to `Code/pc/stm_approach.py`, noting that
it thresholds on absolute deviation from a measured baseline and never sends `APRH`.

**Evidence:** the file is at `Code/pc/stm_approach.py`; `Code/pc/README.md` documents it in full;
`sessions/data/2026-09-19-morning/README.md` records `approach_run1.log` as its output.

---

### A2. `SETUP.md:62` tells a Windows reader to type `python`

> ```
> python Code/pc/stm_console.py GSTS
> ```

**On Jacob's Windows machine `python` and `python3` are Microsoft Store placeholders**, not Python.
They print *"Python was not found; run without arguments to install from the Microsoft Store"*
even though Python 3.13 is installed. **`py` works either way.**

`Code/pc/README.md` records this and uses `py` throughout. **`SETUP.md` is the file a new computer
is set up from**, so it is the one place the advice most needs to be right, and it is the one place
it is missing.

**Recommended fix:** in `SETUP.md` section 3, say to type `py` on Windows, with the one-line reason.
The same applies to the `pip install` line at `SETUP.md:53`, which should be `py -m pip install`.

---

### A3. `docs/soft_launch_test_procedure.md:141` and `:467` still teach judging the piezo by ear

> **`:141`** `## 5. There's a built-in piezo test, and it's the best test available today`
> **`:467`** `Then **listen**. Z first, one second pause, then X, pause, then Y.`

**The document's own scope banner already marks section 5 as superseded**, and `docs/COMMANDS.md`
says plainly that there is no usable resonance once the disc is mounted — a sweep from 1 kHz to
11 kHz on 2026-08-31 found no loudness peak anywhere. **But Stage 5, which the same banner keeps as
current, still instructs the reader to run `TEST` and listen, and has a "What you hear" table with
"Nothing → the disc is depolarised."**

**That is a false-negative generator on the one part in this build that is destroyed silently.**

**Recommended fix:** rewrite Stage 5 to use `TONE` (which parks Z at 0 V rather than at a rail) and
to judge the result with a meter: `DACZ 65535` should give −10 V at the scan head end of DSUB1, on
the row-of-four signal wires. Keep the "`TEST` leaves Z at a rail" warning, which is correct and
important.

**Note this is a real conflict inside one document**: its banner supersedes section 5, and its
Stage 5 body — explicitly kept as current — depends on section 5's claim.

---

### A4. `Code/teensy/src/stm_firmware.hpp:519-520` — the DAC range comments are wrong

> ```
> AD5761 dac_x = AD5761(DAC_1, 0b0000000000000101);    // Output range: -5 to 5V
> AD5761 dac_y = AD5761(DAC_2, 0b0000000000000101);    // Output range: -5 to 5V
> ```

**Both are wrong. X and Y are ±3 V.** The range bits are identical to the bias DAC's, which is
commented correctly as ±3 V on line 522 and which has been measured at ±3 V. **Bits that are
identical cannot give different ranges.**

`CLAUDE.md` already names these exact lines. **The behaviour is correct; only the comments are
wrong** — but they are the first thing a reader looking at the firmware sees, and this figure is
one of the retired values `docs/FACTS.md` tracks.

**Recommended fix:** change both comments to `// Output range: -3 to 3V (range bits 101, measured)`.

---

### A5. `Code/teensy/src/stm_firmware.hpp:151-153` — the `TONE` comment repeats the retired resonance advice

> ```
> // is hardwired to 1 kHz while the fitted 18 mm element resonates at
> // 8.6 kHz. Off resonance it barely moves air, which made "did you hear it?"
> // a useless test during bring-up. Sweep near 8.6 kHz and it is unmistakable.
> ```

**"Sweep near 8.6 kHz and it is unmistakable" is exactly the advice that was retired**, and it is
sitting in the source of the command it is telling you to use. The 8.6 kHz figure is a free-air
datasheet number for a disc that is not ours, and a mounted disc has no usable peak.

**Recommended fix:** keep the reason `play_tone` exists (it parks Z at 0 V and swings symmetrically
about midscale, where `test_piezo` leaves the axis at a rail), and delete the resonance-hunting
advice, replacing it with "judge the piezo with a meter, not by ear".

**Same line also carries a second problem:** it calls the fitted element **18 mm**. See B4.

---

## B — will mislead a reader about what the instrument is or does

### B1. `docs/ENGINEERING_REFERENCE.md:684` — the conflict register records the wrong resolution

> `| ADC full scale 10.24 vs 4.096 | PC tools vs firmware driver and schematic | **Resolved: 4.096.** PC tools not yet changed |`

**The resolution is 10.24 V, not 4.096 V.** 4.096 V is REFBUF; the input span is 2.5 times REFBUF.
This was settled from the datasheet on 2026-09-07, it is in `docs/FACTS.md`, and **it is stated
correctly twice elsewhere in this same file** (section 5's value chain and section 11b).

**`docs/ENGINEERING_REFERENCE.md` section 11 is the canonical home for documented conflicts between
sources**, per `CLAUDE.md` section 6. **A conflict register carrying the wrong resolution is worse
than no register**, because it is the file someone checks precisely when two documents disagree.

**Recommended fix:** `**Resolved: 10.24 V.** 4.096 V is REFBUF; the input span is 2.5 x REFBUF.
The PC tools were right and must not be changed.`

---

### B2. `docs/ENGINEERING_REFERENCE.md:692` — the same register carries a retired ceiling

> `| Max measurable current 100 nA vs 41 nA | ... | **Resolved: 40.96 nA.** ... Corrected 2026-09-06 |`

**40.96 nA is in `docs/FACTS.md`'s retired table**, replaced by 102.4 nA. It survives here only
because the word "Corrected" on the line excuses it from the checker. **The number it excuses is
the wrong one.**

**Recommended fix:** `**Resolved: 102.4 nA**, from 10.24 V over 100 MOhm. The earlier 40.96 nA used
the superseded full-scale constant.`

---

### B3. `Code/pc/README.md:218` and `docs/ENGINEERING_REFERENCE.md:596` — "2.5x too large", stale in both

> **`Code/pc/README.md:218`** `**Every current these tools print is therefore 2.5x too large.** The constant is deliberately not changed yet...`
> **`docs/ENGINEERING_REFERENCE.md:596`** `- \`Code/pc/stm_control.py:37\` and \`stm_console.py\` — currently 10.24, **wrong by 2.5×**`

**Both are wrong and both contradict text a few lines above them in their own files.**
`Code/pc/README.md` states the resolution correctly in the paragraph immediately before line 218,
then contradicts it. `docs/ENGINEERING_REFERENCE.md` section 5 states it correctly and the impact
map at line 596 does not.

**This matters because it is an instruction to change a constant that is right.** Changing it would
make every current figure the tools print wrong by a factor of 2.5, and the end-to-end dummy
junction measurement of 2026-09-16 would stop agreeing with theory.

**Recommended fix:** delete both sentences. `Code/pc/README.md` should end that section at
"...so the PC tools are correct."

---

### B4. Three different piezo discs are described as the fitted one

| File | Line | Says |
|---|---|---|
| `docs/WIRING.md` | 471 | **18 mm** copper/brass buzzer disc, 15,000 pF ±30%, 1.5–30 V |
| `docs/BOM.md` | 156 | **about 25 to 27 mm brass**, 15 to 17 mm ceramic |
| `docs/INVENTORY.md` | 105 | **Jessinie SKU `91410_30_JE`** — `SAID` 2026-09-17, Jacob, *"we are using a difference peizo than both dan bernard and mechpanda"* |
| `CAD/prints/README.md` | — | The `PiezoPlate` seat measures **Ø20.500 mm** over an Ø18.000 mm bore |

**`docs/INVENTORY.md` is the only one of these that records what is actually in the room, and it
is the newest.** `docs/WIRING.md` section 11 gives an 18 mm figure with no provenance at all and is
the one a bench session would read, because `docs/WIRING.md` is the bench reference.

**The 18 mm is very likely the free-flex bore rather than the disc**, but that is a reading, not a
finding, and it should not be guessed.

**Recommended fix:** in `docs/WIRING.md` section 11, replace the disc description with a pointer to
`docs/INVENTORY.md` for the fitted part and to `docs/FACTS.md` for the seat dimensions, keeping
only the part of that section that is verified — that the mounted disc has no usable resonance and
must be judged with a meter. **Do not delete the capacitance and working-voltage figures without
first establishing where they came from.**

---

### B5. `docs/ENGINEERING_REFERENCE.md:552-585` — section 7b uses the spring model that was retired

> `f0 = (1 / 2π) sqrt( g / x )        x = the STATIC EXTENSION of the spring under the load`
> followed by a table: 50 mm droop → 2.2 Hz, 100 mm → 1.6 Hz, 200 mm → 1.1 Hz, 300 mm → 0.9 Hz.

**That formula assumes the droop is the spring extension, which requires a linear spring through
the origin. Our springs have initial tension**, so below about 610 to 910 g of load they do not
stretch at all and the droop is not an extension. **`docs/FACTS.md` retired the 11 Hz figure that
came out of exactly this shortcut**, and `STATUS.md` carries the corrected treatment.

The section also says "The mass and the rate both cancel" and "Neither is needed" — **both of which
are false for these springs.** The correct formula needs the rate and the mass.

**Recommended fix:** add a correction banner at the top of section 7b pointing at `STATUS.md`'s
"THE SUSPENSION SPRINGS ARE SHUT, NOT STIFF" block and `docs/FACTS.md`'s spring rows, and strike
through the droop-to-frequency table. **Keep the rest of section 7b** — the physical description of
the isolation stack, the nine spring-hanger solids and the cable-stiffness warning are all still
correct and useful.

---

### B6. `README.md:22` — the status paragraph is out of date

> `The preamplifier is currently the blocker and is being rebuilt.`

**The preamplifier was fixed on 2026-09-15 and has been in service since 2026-09-16 at about 4 pA.**
The blocker is mechanical: the gap does not hold still and the junction is not a clean tunnelling
gap.

**This is the repository's front page**, and `README.md` itself says to read `STATUS.md` instead
because this paragraph will go stale. **It has.**

**Recommended fix:** rewrite the paragraph to say that the measurement chain is calibrated and
working end to end, that a real junction has been made, that no image has been produced, and that
the blocker is mechanical.

---

### B7. `README.md:61-62` — two hardware-overview rows describe a build we do not have

> `:61` `| Coarse approach step | About **7.8 nm** per motor step — ... ~20x lever reduction. |`
> `:62` `| Sample | Gold foil, mounted on a magnetic disc with a conductive path to the bias magnet |`

**Line 61** picks one of three lever ratios and states the number that follows from it. **The ratio
is unresolved** — Berard gives 20 on one page and 30 on another, and our own CAD geometry suggests
40, giving 3.88 nm. `docs/FACTS.md` carries all three and marks the ratio unresolved. **Quoting one
without the range reads as a measurement.**

**Line 62** describes Mech Panda's arrangement, not ours. **We do not use a magnetic puck.** The
gold goes onto the sample plate directly, and the four magnets in the plate serve no purpose now.

**Recommended fix:** line 61 should give the range 3.9 to 7.8 nm with the ratio marked unresolved;
line 62 should describe gold leaf on copper tape on the plate, with a pointer to `docs/INVENTORY.md`
for the current build.

---

### B8. `docs/ENGINEERING_REFERENCE.md:100` contradicts `:172` about whether the shields were metered

| Line | Says |
|---|---|
| 100 | Preamp box shield: **"continuity across the box UNKNOWN — the acceptance test was never run"** |
| 172 (section 3) | **"all shielding has been metered end to end"** — `SAID` 2026-09-15, Jacob — "which closes V1, open since 2026-09-06" |

**Two rows of the same document, one saying the check was never run and the other saying it closed
the question.** `docs/OPEN_QUESTIONS.md` also still carries "Is the rebuilt preamp box shield
continuous? VERIFY" in two separate rows.

**Which is right is not obvious and should not be guessed.** Jacob's statement covers "all
shielding", but the preamp box was rebuilt again afterwards — the box now fitted is a **new print**,
wrapped and grounded on 2026-09-15, and `docs/OPEN_QUESTIONS.md` records that what it was wrapped
*with* was never stated.

**Recommended fix:** ask Jacob one question — was the **new** box metered end to end, and is it
copper? — and then make line 100, section 3 and the two `docs/OPEN_QUESTIONS.md` rows agree. **Until
then, treat it as open**, which is what this manual does.

---

### B9. `docs/COMMANDS.md:65` still calls the motor direction provisional

> `**Direction: negative approaches, PROVISIONALLY**`

**It was settled at the bench on 2026-09-17** and confirmed by every motor approach since that
found the gold. `docs/OPEN_QUESTIONS.md` records it as settled; `docs/COMMANDS.md` does not.

**Recommended fix:** `Direction: negative approaches, settled at the bench 2026-09-17 and confirmed
on 2026-09-19. Re-check after any change to the tip holder, because the lever's short arm is 1 mm.`

---

### B10. `docs/COMMANDS.md:155` quotes a figure whose basis `STATUS.md` flags as in doubt

> `**Check nobody is within a metre of the preamp.** A person injects 20–50 nA; a tunneling current is about 1 nA.`

**`STATUS.md` safety rule 9 keeps the rule and explicitly marks the number as not established**,
because it was measured on the old board whose amplifier reference floated. A direct gloved touch on
the repaired board's input node produced about 0.5 nA — between forty and a hundred times less,
from a far more aggressive stimulus.

**The rule is right. The number is not.** `docs/COMMANDS.md` states it without the caveat.

**Recommended fix:** keep the instruction and replace the figure with "a person nearby injects
enough current into a 100 MOhm input node to swamp a tunnelling signal; the old 20 to 50 nA figure
is not established, see `STATUS.md` safety rule 9."

---

## C — answered elsewhere, or tidiness

### C1. Three UNKNOWNs that have since been answered

| File | Line | Says UNKNOWN | Answered |
|---|---|---|---|
| `docs/OPEN_QUESTIONS.md` | 99 | Extension springs: **"Spring rate"** unknown | **`docs/FACTS.md`, 2026-09-19: about 58 N/m each from the part number.** It only ever needed the listing |
| `docs/OPEN_QUESTIONS.md` | 104 | Piezo disc: **"Our part number and supplier"** unknown | **`docs/INVENTORY.md`, 2026-09-17: Jessinie `91410_30_JE`** |
| `docs/BOM.md` | 183 | Extension springs: **"rate UNKNOWN"** | Same as the first row. `docs/BOM.md` is a specification, so this is lower priority, but it is the row `docs/OPEN_QUESTIONS.md` cites |

**Recommended fix:** close the two `docs/OPEN_QUESTIONS.md` rows with a pointer, in the same
struck-through style the file already uses elsewhere.

---

### C2. `docs/ENGINEERING_REFERENCE.md:576` and `:761` — the isolation stage is known to be hanging

> `:576` `**UNKNOWN whether our isolation is assembled and hanging, or whether the platform is currently resting on the base frame.**`
> `:761` `... Whether the isolation stage is even hanging.`

**Answered 2026-09-19** — `SAID`, Jacob: *"The isolatation stage is engaged"*, recorded in
`docs/INVENTORY.md`. **And Jacob separately corrected a photo reading that the platform was sitting
on the tower:** *"its not sitting on the tower is just about its a perfect fit."*

**Recommended fix:** update both, and carry forward the consequence that is more important than the
answer: **the clearance itself has never been measured, and it is the binding constraint on the
whole isolation plan.**

---

### C3. `docs/BOM.md:109` — the standoff row says we do not own the part

> `**SPECIFIED, NOT OWNED — corrected 2026-09-09.** ... **We do not have it.**`

**Two Keystone 11301 were received on 2026-09-14** (`docs/INVENTORY.md`, DigiKey 36-11301-ND, order
screen seen), and one is in the instrument. **`docs/BOM.md` is a specification and not an
inventory**, which is exactly why this row should not be making a claim about what is in the room at
all.

**Recommended fix:** replace the ownership sentence with a pointer to `docs/INVENTORY.md`, and keep
the part of the row that is a specification — including that **it does not enter our Ø2.108 mm hole**
and that any future board should draw that hole at Keystone's recommended Ø2.184 mm.

---

### C4. `Code/pc/README.md` — the tool table is missing five of the tools

The table lists `stm_console.py`, `adc_stats.py`, `stm_approach.py`, `stm_approach_test.py`,
`stm_control.py`, `stm_app.py` and `stm_control_test.py`.

**It does not list `stm_feedback_scan.py`, `stm_noise_spectrum.py`, `stm_y_control.py`,
`check_facts.py` or `stl_features.py`** — which includes the only imaging tool, the only noise tool
and the only control tool.

**Recommended fix:** add the five rows. `CLAUDE.md` section 6 already describes `check_facts.py` and
`stl_features.py`, so one line each is enough.

---

### C5. `Images/ours/README.md` — two photographs have no caption

`2026-09-16_controller_board.jpg` and `2026-09-16_scanhead_on_platform.jpg` are in the folder and
are not in the README's table. Every other frame has a caption and a `SAID` or `READ` mark.

**This matters more than it looks**, because the folder's whole convention is that a photograph
without a mark is a photograph nobody has said anything about. **An uncaptioned frame is the one a
future session is most likely to read something off.**

**Recommended fix:** add both rows, marked `READ` unless Jacob confirms them.

---

### C6. `Code/pc/check_facts.py` — the `drops in` retired literal over-fires on ordinary English

**Found while writing this manual.** The retired row `drops in` (for the Keystone standoff) matches
the substring in any ordinary sentence containing "drops into" — in this case a troubleshooting
heading about a supply channel dropping into constant-current mode, which has nothing to do with
standoffs.

**The row is unqualified**, so it fires on every occurrence anywhere.

**This is a false positive, not a missed catch**, so it is low severity — but it will keep firing
and the usual response to a noisy check is to stop reading it. `STATUS.md`'s "Known code issues"
section already tracks two other weaknesses in this checker.

**Recommended fix:** qualify the row with words the documents actually use — for example
"the standoff" or "our board hole" — **and then confirm the row still fires** against a
deliberately reintroduced stale line. `Code/pc/check_facts.py`'s own `check_dead_qualifiers`
exists to catch a qualifier that matches nothing, so the confirmation is automatic.

---

## Checked and found consistent

Recorded so that nobody spends time re-checking these.

| | |
|---|---|
| **The DSUB1 and DSUB2 colour tables** | `docs/WIRING.md`, `docs/START_HERE_gotchas.md` and `docs/ENGINEERING_REFERENCE.md` agree pin for pin, including that orange is −15 V on DSUB2 and plain ground on DSUB1 |
| **The H1 ribbon pinout** | `docs/WIRING.md` and `docs/COMPONENTS.md` agree, including pins 24 and 26 unconnected and pin 6 being the read-enable |
| **The Teensy pin assignments** | `docs/WIRING.md` matches `Code/teensy/src/stm_firmware.hpp` exactly, including the deliberate pin 8 = Z, pin 9 = Y ordering |
| **The motor wiring** | `docs/WIRING.md`, `docs/START_HERE_gotchas.md` and `CAD/prints/README.md` agree, and the firmware's `EfficientStepper(steps, IN1, IN3, IN2, IN4)` confirms the software swap |
| **The four DAC range bits** | `docs/WIRING.md`, `docs/FACTS.md`, `docs/DAC_BOOT_STATE.md` and the firmware source all agree on `000` for Z and `101` for X, Y and bias. **Only the firmware's comments disagree** — see A4 |
| **The firmware fixes of 2026-09-16** | `STATUS.md` faults 2 and 3, `docs/COMMANDS.md`, `Code/teensy/src/stm_firmware.hpp` and `Code/teensy/lib/Stepper/EfficientStepper.cpp` all describe the same two changes, and the source carries the fix comments at their sites |
| **The `SCST` bounds problem** | `STATUS.md`'s "Known code issues" matches `Code/teensy/src/main.cpp` — seven integers parsed with no bounds check, and `scan_image_adc`/`scan_image_z` are `[2048]` |
| **The PID gains booting at zero** | `Code/teensy/src/stm_firmware.hpp` declares `Kp = Ki = Kd = 0.0` and the `INIT_K*` defines appear only in a commented-out line, exactly as `docs/FACTS.md` and the soft-launch procedure say |
