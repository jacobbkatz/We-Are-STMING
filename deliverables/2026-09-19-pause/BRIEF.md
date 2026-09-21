# Shared brief — the 2026-09-19 pause-point work

**Written by the lead (Claude Code, web session, branch `claude/charming-bell-texacn`) on
2026-09-19, before any subagent was launched.** Every agent reads this file first.

This is not a project document. It is a working brief for a single piece of coordinated work:
**experimental work is paused, and we are turning eleven weeks of bench records into a set of
finished, honest deliverables.** When the work is done this directory is the deliverable and
`STATUS.md` is updated to point at it.

---

## 1. What the project is, and where it actually stands

Jacob Katz and Nuh Shaheer — **neither of them writes code** — have built a scanning tunneling
microscope from 3D-printed parts, following **Mech Panda's `red-panda-stm`** for the mechanics,
firmware and controller board and **Dan Berard's home-built STM** for the scan head and the
transimpedance preamplifier. Work ran roughly 2026-07-25 to 2026-09-19.

**The instrument is now disassembled and being moved.** `STATUS.md`, top block: Jacob, ~14:19 UTC
2026-09-19 — *"We are now taking it apart and moving it to News House as I'm flying to San Diego
for college."* **"News House" is read as Nuh's house and is an inference, not confirmed.** What was
taken apart and how it was packed is UNKNOWN.

### The one-paragraph state of the science

The **measurement chain works end to end and is calibrated**: a 100 MΩ dummy junction gave
−3,205 ± 37 counts per volt against −3,200 predicted (R² 0.993), which is the project's strongest
single result. A **real tip-to-gold junction has been made** and its current responds to Z. **No
image has been produced.** Feedback scans are matched by their own X-held controls, so nothing in
them is established as surface structure. The **blocker is mechanical**: as of 2026-09-19 morning
the gap moves by most of the Z range within seconds to minutes with the motor and hands still, the
junction snaps in rather than opening a clean tunneling gap (per-run medians of ~1,650–1,970 Z
counts per decade of current where tunneling would be ~6–13), and in/out hysteresis of
705–1,868 counts appears in every run. The interpretation on record is **"a soft, pressed, sticky
contact"**, not a tunneling gap — and it is marked as interpretation, not proof.

**No agent may upgrade any of that.** If your work changes one of these statements, say so
explicitly in your handoff and show the evidence; do not quietly restate it differently.

---

## 2. The rules that govern this work

`CLAUDE.md` at the repository root is binding on every agent. **Read it in full before writing
anything.** The parts that will bite you here:

| Rule | What it means for you |
|---|---|
| **§3 precedence** | `STATUS.md` > newest-dated session logs > older logs > `docs/PROJECT_HANDOFF_SUMMARY.md` body. **But a correction banner at the top of an old file is live** — read headers before dismissing a file on rank |
| **§3b search before declaring unknown** | Four times in four days something recorded as unknown was already in the repository. `grep -rin` the prose, `Code/`, and check `docs/INDEX.md` before you write UNKNOWN or start deriving anything |
| **§3bb one value per fact** | `docs/FACTS.md` is the only register of constants. **Do not build a second one.** Citing a figure inside prose or a caption is fine and expected; a table of constants in your deliverable is not |
| **§3c work out the consequence first** | You are not ordering bench actions here, but the same rule applies to anything you write as an instruction |
| **§3d physical reality** | `docs/INVENTORY.md` is the only record of what is in the room. **Never infer what they own from a design file or a BOM** |
| **§4 safety rules** | `STATUS.md`'s numbered list is the authority. **Never cite "safety rule N" against `CLAUDE.md` §4**, which is deliberately unnumbered |
| **The photograph rule** | A photograph is not a measurement of our hardware. Mark every caption **`SAID`** (they told us) or **`READ`** (your reading, plausible, unconfirmed). On 2026-09-09 a session read a part marking off a photo and edited five documents before anyone asked whose board it was — it was Berard's |
| **No emoji** in project documents |

**`python3 Code/pc/check_facts.py` must exit 0.** It was clean when this brief was written. It
gates the commit through `.githooks/pre-commit`. If you break it, fix it or say so loudly.

---

## 3. Authoritative files — read these, do not duplicate them

| What | Canonical home |
|---|---|
| Live state, faults, numbered safety rules | `STATUS.md` (197 KB — read the top blocks and search the rest) |
| Every constant, with provenance and a RETIRED list | `docs/FACTS.md` |
| Every open question / UNKNOWN / VERIFY | `docs/OPEN_QUESTIONS.md` |
| What to do next at the bench | `docs/NEXT_SESSION_PLAN.md` |
| Pinouts, cable colors, LEDs, power tree | `docs/WIRING.md` |
| Every firmware command, what blocks, what replies | `docs/COMMANDS.md` |
| Part specs, design cross-checked against datasheets | `docs/COMPONENTS.md` |
| Cross-subsystem layer, value chains, conflict register §11 | `docs/ENGINEERING_REFERENCE.md` |
| **What is physically in the room** | `docs/INVENTORY.md` — **not** `docs/BOM.md`, which is a specification |
| What is inside every zip/PDF/mesh | `docs/INDEX.md` |
| One log per work session | `sessions/YYYY-MM-DD[-name].md`, indexed in `sessions/README.md` |
| Raw bench data | `sessions/data/<session>/`, each with its own `README.md` |
| Photographs of our own hardware | `Images/ours/` (`Images/` root is **Mech Panda's**, not ours) |

**Existing deliverables, which are to be updated rather than replaced:**

| File | What it is |
|---|---|
| `docs/showcase.html` | For a reader judging the work in five minutes. Leads with what the instrument demonstrably does. Published at <https://claude.ai/artifact/GzwmmzMEgVPsFke5iHWYpD> |
| `docs/progress.html` | Public explainer: what an STM is, how tunneling works, where the build reached |
| `docs/bench_2026-09-17_review.html` | "The First Junction" — the 2026-09-17 session reviewed |
| `docs/bench_card_2026-09-19.html` | Ten bench steps in order. Superseded by the move; keep for the record |
| `docs/gold_leaf_procedure.html`, `docs/preamp_*.html` | Procedure cards from the preamp work |

---

## 4. Known uncertainties, and previous conclusions that need rechecking

These are the things most likely to be wrong, or to be stated with more confidence than they earn.
**Every agent whose work touches one of these must check it against the primary record, not against
a summary.**

1. **"No image" is the current conclusion.** It rests on controls: the X-held control images
   reproduce *better* than the feedback scans (image-to-image +0.37 against +0.04). Subagent 2 is
   explicitly testing whether anything survives that. **The conclusion may stand; it may also be
   too strong.** It may not be weakened without evidence.
2. **The Z scale is inherited, not measured.** "~6–13 counts per decade for tunnelling" comes from
   Berard's calibration of a similar disc, not from our scanner. The hysteresis result does **not**
   depend on the scale; the "decade per 1,650 counts" comparison does.
3. **The 2026-09-18 noise figures (341–350 counts) are stale for the current tip** — 2026-09-19
   bench measured 40–42 with the tip clear and 9–19 with a junction and X held. Tools still quote
   the old numbers. Check which tip and which night any noise figure belongs to.
4. **Trace/retrace anti-correlation (−0.75 to −0.94) was called "loop lag" and then corrected to
   "the loop hunting"** on 2026-09-19 morning. X motion is the likely but unproven cause.
5. **The claim that an X-held control swung Z by 28,000 counts was corrected and withdrawn** — that
   swing was the tool, not the instrument. The gold's own motion was then measured directly the
   next morning, and that measurement stands.
6. **The suspension spring analysis was reversed once already** (`f0 = 15.76/sqrt(droop)` assumed a
   linear spring; these have initial tension). Retired values are in `docs/FACTS.md`.
7. **The Keystone 11301 standoff: three web-sourced answers, all three wrong**, settled only by
   Jacob offering the part up to the hole. A dimension nobody has measured is not a fact.
8. **`d`, the tip-to-pivot-line distance, cannot be measured from photographs.** Three attempts gave
   answers differing by more than 2x. `Images/ours/README.md` records why, in detail. **Do not try
   again.**
9. **Safety rule 6 was not followed as written** on 2026-09-19 — every motor move parked Z at the
   retracted end, not midscale. That is Jacob and Nuh's to amend or keep, not ours.
10. **Whether the suspended platform touches the damping stack has never been measured.** It was
    READ off a photo as touching, and Jacob corrected it within the hour: *"its not sitting on the
    tower is just about its a perfect fit."*

---

## 5. The new photographs — what they are and where they came from

**Thirty-one new photographs were pulled from Jacob's shared Drive folder by the lead at the start
of this work** (folder id `1hSX3R2Jg1eAWyPV-2nJiHesIGyC6Uloi`, owner `jacob@quis.com`). They were
not in the repository and no session has seen the 2026-09-19 set.

| Shoot | Frames | EXIF capture time | Status |
|---|---|---|---|
| **2026-09-18 evening** | `IMG_8619`–`IMG_8626` (8) | 18:08:45 to 19:09:13 | **READ by the 2026-09-18 23:13 session** (commit `6b41855`) but **never committed**. That session's readings — platform resting on the tower, the gold window part copper — are on record and two of the three photo readings that day were corrected by Jacob within the hour |
| **2026-09-19 morning** | `IMG_8630`–`IMG_8653` (23) | 09:35:31 to 09:41:26 camera-local | **Never seen by any session.** Jacob's "we are taking it apart" message is timestamped ~14:19 UTC the same day, so on a UTC−4 reading these frames sit roughly 40 minutes before it |

**Two video clips in the same shoot cannot be fetched**: `IMG_8632.MOV` (24.9 MB) and
`IMG_8654.MOV` (29.7 MB), both over the Drive connector's hard 10 MB cap. `IMG_8632` sits between
frames timed 09:35:33 and 09:38:09; `IMG_8654` is the last item in the folder. **Record them as
unavailable — a tool limit, not a decision.**

**Working copies** are at `Images/ours/incoming_2026-09-19/`, EXIF-stripped (verified: zero tags)
and resized to 1600 px on the long edge, matching the convention the 2026-09-18 batch used.
Originals stay in Jacob's Drive. Full-resolution decoded copies are in the lead's scratchpad at
`/tmp/claude-0/-home-user-We-Are-STMING/5c3eb8ce-8433-54fd-b180-6d24edd1253f/scratchpad/drive_raw/`
and the EXIF table is `.../scratchpad/new_photo_exif.json`. **Do not commit the full-resolution
copies.**

**A first pass by the lead, on contact sheets only, flagged as `READ` and owed a proper
frame-by-frame review:** the 2026-09-18 set shows the sample plate off the head and the instrument
on its frame with paper coin tubes standing on the platform; the 2026-09-19 set contains the room
and bench, **several frames with two people in them**, the assembled instrument on its frame, the
copper-taped enclosure off the instrument, close-ups of the scan-head face and tip region, and
consumables. **Which person is which has NOT been established and must not be guessed** — the
repository only ever confirms one identification, `2026-08-01_nuh_soldering.jpg`, and that was
`SAID` by Jacob.

---

## 6. Agents, ownership, and dependencies

**Wave 1** (evidence): agents 1, 2, 3, 4 run concurrently.
**Wave 2** (synthesis): agents 5, 6 run after wave 1 lands, on wave 1's real outputs.

| # | Agent | Owns — writes ONLY here | Depends on |
|---|---|---|---|
| 1 | Data inventory and analysis | `deliverables/2026-09-19-pause/analysis/**` | — |
| 2 | Candidate images and motion hypothesis | `deliverables/2026-09-19-pause/candidates/**` | — |
| 3 | Setup photographs | `Images/ours/**`, `deliverables/2026-09-19-pause/photos/**` | — |
| 4 | Manual | `deliverables/2026-09-19-pause/manual/**` | photos (second pass) |
| 5 | Poster and talk | `deliverables/2026-09-19-pause/poster/**` | 1, 2, 3 |
| 6 | Report, handoff, emails | `deliverables/2026-09-19-pause/report/**` | 1, 2, 3 |

**Nobody but the lead writes to:** `STATUS.md`, `CLAUDE.md`, `docs/FACTS.md`, `docs/**` (except as
a reader), `sessions/**`, or another agent's directory. **Raw data in `sessions/data/` is
read-only to everyone.** If you need a derived copy, write it into your own directory.

**Every agent writes its handoff to
`deliverables/2026-09-19-pause/_handoffs/<n>-<name>.md`** before finishing, containing:

1. **Files reviewed** and work completed.
2. **Outputs created**, and the exact command that reproduces each one.
3. **Evidence** for each finding — file path, line or row range, and the number.
4. **Uncertainties, blockers, and what is left undone.**

Checkpoint as you go. Do not leave anything only in your final message.

---

## 7. Standing instructions to every agent

- **Separate what was measured from what was inferred.** If a number was measured, say by whom and
  when. If it was derived or assumed, say that instead, in the same sentence.
- **Record what was ruled out.** The false trails in this project have been as valuable as the
  results, and the session logs are written that way.
- **Mark gaps UNKNOWN or VERIFY.** A confident wrong number costs hardware here.
- **Do not invent**: no scale bars, no contributors, no procedures, no safety limits, no metadata,
  no reconstructed image structure.
- **Write for two people who do not read code.** Plain language, and say what a result means at the
  bench, not just what it is.
- **Account for multiple comparisons.** If you searched many scans for a feature, say how many, and
  what that does to the chance of finding one.
- **A visually convincing image is not proof. Lack of repeatability is not automatic dismissal.**
