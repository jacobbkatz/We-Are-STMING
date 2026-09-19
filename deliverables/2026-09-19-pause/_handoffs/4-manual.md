# Handoff — Subagent 4, the manual

**Written 2026-09-19.** Owns and wrote only `deliverables/2026-09-19-pause/manual/**`. **Nothing
else in the repository was modified.**

---

## 1. Files reviewed

**Read in full:**

`CLAUDE.md` · `deliverables/2026-09-19-pause/BRIEF.md` · `deliverables/2026-09-19-pause/SOURCE_INVENTORY.md`
· `README.md` · `SETUP.md` · `docs/WIRING.md` · `docs/COMMANDS.md` · `docs/START_HERE_gotchas.md`
· `docs/DAC_BOOT_STATE.md` · `docs/FACTS.md` · `docs/INVENTORY.md` · `Code/pc/README.md`
· `CAD/prints/README.md` · all four `sessions/data/*/README.md` · `Images/ours/README.md`
· `docs/gold_leaf_procedure.html` (text extracted)

**Read in the parts that matter, with the rest skimmed by heading:**

`STATUS.md` (197 KB — the top blocks in full, then the stage table, all open faults, next actions,
the standing safety rules, open questions and known code issues in full) ·
`docs/soft_launch_test_procedure.md` (banner and stages 0–6 in full) ·
`docs/ENGINEERING_REFERENCE.md` (sections 1–8, 10–12 in full) · `docs/COMPONENTS.md` (by heading,
plus the sections cited) · `docs/BOM.md` (sections 3–6) · `docs/OPEN_QUESTIONS.md` (sections 1–3) ·
`docs/NEXT_SESSION_PLAN.md` (the live top block in full, the rest by heading) · `docs/INDEX.md` (by
heading)

**Firmware and tools, read as source:**

`Code/teensy/src/main.cpp` (all) · `Code/teensy/src/stm_firmware.hpp` (all 543 lines) ·
`Code/teensy/lib/Stepper/EfficientStepper.cpp` (all) · `Code/pc/check_facts.py` (the scanning and
checking logic, to write compliant text) · the headers and usage blocks of
`Code/pc/stm_approach.py`, `stm_feedback_scan.py`, `stm_noise_spectrum.py`, `stm_y_control.py`

**Photographs opened individually** (see section 5): eight prepared figures from
`deliverables/2026-09-19-pause/photos/prepared/` plus `Images/ours/2026-09-18_scanhead_face_1.jpg`.
`deliverables/2026-09-19-pause/photos/IMAGE_INVENTORY.md` and `photos/prepare_photos.py` were read
for provenance and marks.

---

## 2. Work completed

**A single consolidated manual was written**, covering what the instrument is, which revision is
fitted, assembly and connections, sample and tip, startup and shutdown, every firmware command,
data collection, file ownership, analysis, troubleshooting, and a staged procedure for resuming
after the move.

**Two supporting documents** record what changed and what contradicts what.

**The reading in the brief is confirmed: there is no single existing manual and there never has
been.** Section 1 of `CHANGELOG.md` sets out what was missing and where each piece was scattered.
The nearest thing is `docs/soft_launch_test_procedure.md`, which covers powering up from cold and
says in its own banner that parts of it are superseded, and
`docs/PROJECT_HANDOFF_SUMMARY.md`, whose body `CLAUDE.md` section 3 explicitly supersedes.

---

## 3. Outputs

| File | What it is | Size |
|---|---|---|
| `deliverables/2026-09-19-pause/manual/MANUAL.md` | The manual, 12 sections plus two appendices, with a table of contents | ~1,940 lines |
| `deliverables/2026-09-19-pause/manual/CHANGELOG.md` | What changed, what was outdated, what was corrected, what is newly unknown, and what was deliberately NOT upgraded | ~150 lines |
| `deliverables/2026-09-19-pause/manual/INCONSISTENCIES.md` | 21 numbered inconsistencies with file, line, evidence and a recommended fix, graded A/B/C, plus eight things checked and found consistent | ~420 lines |

**Reproducing them:** they are hand-written prose, not generated. The check that gates them is

```
python3 Code/pc/check_facts.py
```

---

## 4. Evidence for the main findings

**Every inconsistency in `INCONSISTENCIES.md` carries its own file, line and evidence, and every
line number was re-verified against the files at the end of this work.** The five that would cost a
bench session:

| Finding | Evidence |
|---|---|
| `docs/COMMANDS.md:113` says the approach tool "is planned but not yet written" | The file exists at `Code/pc/stm_approach.py` with 40 tests; `sessions/data/2026-09-19-morning/README.md` lists `approach_run1.log` as its output |
| `SETUP.md:62` tells a Windows reader to type `python` | `Code/pc/README.md` records that `python` and `python3` are Store placeholders on Jacob's machine and that `py` works |
| `docs/soft_launch_test_procedure.md:141` and `:467` teach judging the piezo by ear | The same document's banner marks section 5 superseded; `docs/COMMANDS.md` records a 1–11 kHz sweep finding no peak |
| `Code/teensy/src/stm_firmware.hpp:519-520` — DAC range comments | Line 522 comments the identical range bits correctly as ±3 V |
| `Code/teensy/src/stm_firmware.hpp:151-153` — `TONE` comment repeats the retired resonance advice | Same as above |

**The two worst documentation contradictions:**

| Finding | Evidence |
|---|---|
| `docs/ENGINEERING_REFERENCE.md:684` recorded the ADC full-scale conflict as resolved to the retired value. **Corrected by someone else the same day, re-checked at the end of this work** | That file is the canonical home for documented conflicts (`CLAUDE.md` section 6), and it states the right answer twice elsewhere in itself — section 5's value chain and section 11b. **The same stale claim is still live in two other places**, `docs/ENGINEERING_REFERENCE.md:596` and `Code/pc/README.md:218` |
| `docs/ENGINEERING_REFERENCE.md:100` says the preamp box shield's continuity was never checked; `:172` says all shielding was metered end to end | Two rows of the same file. `docs/OPEN_QUESTIONS.md` carries the question open in two more rows, and the photograph review's own caption for the enclosure independently records it as never metered |

**Three UNKNOWNs that have since been answered elsewhere** (`INCONSISTENCIES.md` C1–C2): the spring
rate (`docs/FACTS.md`, 2026-09-19), the piezo disc part number (`docs/INVENTORY.md`, 2026-09-17),
and whether the isolation stage is hanging (`docs/INVENTORY.md`, 2026-09-19).

---

## 5. Figures — filled, and what is left

**`deliverables/2026-09-19-pause/photos/IMAGE_INVENTORY.md` and `photos/prepared/` both exist**, and
the figure slots were filled from them near the end of this work. **Eleven figures are placed; two
slots remain empty.**

**Every placed figure was opened by this agent, not taken on trust.** The eight prepared images
opened are 01, 02, 03, 04, 05, 06, 07, 08, 09 and 12, plus
`Images/ours/2026-09-18_scanhead_face_1.jpg`.

| Placed | Where | File |
|---|---|---|
| 3.1 | section 3.9 | `photos/prepared/04_instrument_full_height.jpg` |
| 3.2 | section 3.9 | `photos/prepared/05_scan_module_in_hand.jpg` |
| 3.3 | section 3.9 | `photos/prepared/07_teensy_carrier_and_ribbon.jpg` |
| 3.4 | section 3.9 | `photos/prepared/08_bench_power_supplies.jpg` |
| 3.5 | section 3.9 | `photos/prepared/06_stepper_28byj48_label.jpg` |
| 3.6 | section 3.9 | `photos/prepared/09_faraday_enclosure.jpg` |
| 4.1 | section 4.5 | `photos/prepared/01_sample_plate_gold_window.jpg` |
| 4.2 | section 4.5 | `photos/prepared/03_sample_plate_rubber_bands.jpg` |
| 4.3 | section 4.5 | `Images/ours/2026-09-18_scanhead_face_1.jpg` |
| 11.1 | section 11 Stage B | `photos/prepared/12_teardown_platform_off_frame.jpg` |
| 11.2 | section 11 Stage C | `photos/prepared/02_platform_damping_gap.jpg` |

**UNFILLED, and listed in Appendix B of the manual:**

| Slot | What is wanted | Why it is empty |
|---|---|---|
| **TODO-PHOTO A** | **The DSUB2 splice at the preamp end**, showing the five-way row | No frame in either new batch shows it. **A caption must not quote colours read off the frame** — the preamp's own lead colours are not the J1/J2 colours |
| **TODO-PHOTO B** | **The tip, close enough to judge sharpness** | The nearest frames are the 2026-09-16 tip-protrusion pair, and that tip has been replaced twice since |

**Two further gaps that are not photographs and cannot be closed here:** how the instrument was
packed (no frame shows anything going into a box) and the bench video clips, all of which are over
the transfer size limit.

**No figure carries a measurement.** In particular the scan-head face figure carries an explicit
warning that no dimension may be taken from it, because three attempts to measure the
tip-to-pivot-line distance from those frames gave answers more than a factor of two apart.

---

## 6. Uncertainties, blockers and what is left undone

### The checker exits 0

```
python3 Code/pc/check_facts.py
```

**Clean, run as its own command and read by its exit code, with all three manual files present.**

**It caught three things during this work, and two of them were checker defects rather than
content.** A troubleshooting heading in the manual reading *"drops into constant-current mode"*
tripped the retired `drops in` literal, and a line in another agent's file tripped the retired
`800 counts` inside *"1,800 counts per decade"*. **Both are the same class — a retired literal that
is also a substring of innocent text — and both have since been fixed at the source by the lead**,
in commits `0b1ea09` and `4d416b9`. `INCONSISTENCIES.md` item C6 keeps the record for the rule it
demonstrates: **a checker that fires on correct lines gets switched off.**

The third was in the manual's own text: a `safety rule 2` citation sharing no wording with the
rule it cited. Reworded to name the sign of the tunnelling current.

### Things the manual states as open because they genuinely are

1. **Whether the fitted preamp box shield was ever metered end to end.** The repository contradicts
   itself. **One question to Jacob settles it.** Until then the manual treats it as open, which is
   the conservative reading.
2. **Where to park Z before a motor move.** `STATUS.md` safety rule 6 says midscale; every motor
   move on 2026-09-19 parked at the retracted end. **The manual states both and says the decision is
   owed. It is Jacob and Nuh's, not ours.**
3. **What was taken apart in the move and how it was packed.** The teardown photographs answer the
   first half — the platform came off as one piece with the head, motor and preamp on it — and
   nothing answers the second.

### Things a bench session would need that this manual cannot supply

- **The live back-off beeper is scratch code on Jacob's laptop.** It is the method that actually
  worked for setting the gap by hand, and it is not in `Code/pc/`. The manual says so and points at
  `docs/NEXT_SESSION_PLAN.md`, which already asks for it to be promoted.
- **No procedure is invented anywhere.** Where a step exists only as scratch code or only in a
  session log, the manual names that and does not write a substitute.
- **No safety limit is invented.** Every limit cited resolves to `STATUS.md`'s numbered list or to
  `docs/FACTS.md`.

### What was deliberately not done

- **No existing document was edited.** All 21 findings are recorded with file and line for the lead
  to apply.
- **No conclusion was upgraded.** `CHANGELOG.md` section 3 lists the nine statements carried forward
  with their hedges intact, including "no image", the soft-contact interpretation, the inherited Z
  scale, and the withdrawn 28,000-count claim.
- **No second register of constants was created.** The connection tables are reproduced because the
  brief asked for them, and they carry a banner saying `docs/WIRING.md` is canonical.

### One thing worth a second opinion

**`INCONSISTENCIES.md` B4 says three different piezo discs are described as the fitted one** — an
18 mm figure in `docs/WIRING.md`, 25–27 mm in `docs/BOM.md`, and a Jessinie part number in
`docs/INVENTORY.md`. **The likeliest explanation is that the 18 mm is the free-flex bore rather than
the disc, but that is a reading and it is deliberately not written as a finding.** Somebody should
check where the `docs/WIRING.md` figure came from before it is changed.
