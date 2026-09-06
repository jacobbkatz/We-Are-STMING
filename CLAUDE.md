# Instructions for Claude

This repository is worked on from **two different computers** by two people who are **not
programmers**. Everything below exists to keep both machines in sync and to stop us from
destroying hardware.

Read this file completely before doing anything.

---

## 1. Who you are working with

Jacob and Nuh are building a 3D-printed scanning tunneling microscope. **Neither of us writes
code.** You do all of it.

That has consequences for how you should work:

- **Explain in plain language what you changed and why.** Not just "updated the ADC clock" —
  say what it does and what we should expect to see differently at the bench.
- **Never assume we can debug something ourselves.** If a command might fail, say what failure
  looks like and what to do about it.
- **Tell us when you are unsure.** This project has a strong culture of marking things
  UNKNOWN or VERIFY rather than guessing. A confident wrong number costs us hardware.
  Keep doing that.
- We work at a physical bench with a real instrument. **Some mistakes here are expensive**
  — a destroyed piezo, a crashed tip, a shorted supply rail. When in doubt, stop and ask.

---

## 2. Start of every session — do this first

The other person may have worked since you last ran. **Their work is on GitHub. Yours is not,
until you push it.**

```bash
git pull --ff-only origin main
```

Then read, in this order:

1. **`STATUS.md`** — where the build actually is right now. Always read this.
2. **The newest file in `sessions/`** — what happened last session and why.
3. Anything else you need for the specific task.

A `SessionStart` hook in `.claude/settings.json` tries to do the pull automatically and prints a
summary. **Do not rely on it silently** — confirm you are up to date. If the hook reported a
problem, deal with it before starting work.

### If the pull fails

`--ff-only` fails safely rather than making a mess. The usual causes:

- **"Your local changes would be overwritten"** — there is unfinished work on this computer.
  Show the user `git status`, explain what is uncommitted, and ask whether to keep it or discard
  it. Do not discard without asking.
- **"Not possible to fast-forward"** — both computers have commits the other doesn't. Use
  `git pull --rebase origin main`, resolve any conflicts, and explain plainly what you did.

---

## 3. Which document to believe

This project has accumulated documents that **contradict each other**, because findings were
corrected as we learned more. This is the most common way to get a fact wrong here.

**The precedence order, highest first:**

1. **`STATUS.md`** — the live state. Rewritten every session.
2. **The newest file in `sessions/`** — newer sessions correct older ones.
3. **Older files in `sessions/`.**
4. **`docs/PROJECT_HANDOFF_SUMMARY.md`** — large and useful, but parts of it are known to be
   wrong, corrected in `sessions/2026-08-31-results.md` section 5. Never cite the handoff's **body**
   against a newer document.

If two documents disagree and you cannot tell which is newer, **say so and ask.** Do not average
them or pick one silently.

### Precedence is about conflicts. It is NOT about what to read.

**A low-ranked document is still read. It is only outranked when it disagrees with a higher one.**

This distinction has cost this project real time. On 2026-09-06 a remote session spent a day
re-deriving the JP1 pinout from the preamp gerbers — **an answer that had been sitting on `main`
for six days**, in the header of the handoff, put there by the person who did the work. It was
skipped because the handoff is ranked last, and "ranked last" was read as "not worth opening".

The result was worse than duplication: the re-derivation was **shallower** and missed that pin 4
has no copper routed to it at all.

> **Freshness is not a property of a document. It is a property of a passage.**
> A correction banner at the top of an old file is newer than the file it sits in — often newer
> than anything else in the repository, because that is where someone wrote it the moment they
> found it.

**So: `docs/PROJECT_HANDOFF_SUMMARY.md`'s body is superseded. Its header banner is a live
correction log and is read FIRST, not last.** Check the top of any document before dismissing it
on rank.

---

## 3b. Before you record anything as unknown, search for it

**Four times in four days, something recorded as unknown or blocked was already answered by a file
in this repository.** This is now the single most common failure mode in this project — more than
wrong measurements, more than bad reasoning.

| Recorded as | Where the answer already was |
|---|---|
| "ADC full scale unresolvable without a bench calibration" | The controller schematic, in our own `PCB/` directory |
| "JP1 numbering unknown, do not run a wire" | The handoff's header banner, from Nuh's own commit |
| Copper tape and grounding advice, missing | `WHICH_SCANHEAD_PART.txt`, inside a zip |
| Both boards' netlists, "would need tracing" | Inside both gerber archives all along |

**Before writing UNKNOWN, VERIFY, "needs a bench test", or "we would have to derive this" — and
before starting any derivation from scratch — run these:**

```bash
grep -rin "<the thing>" --include=*.md . | head -30      # every prose document
grep -rin "<the thing>" Code/ | head -20                 # source and comments
head -40 docs/PROJECT_HANDOFF_SUMMARY.md                 # the live correction banner
```

**Then check `docs/INDEX.md`**, which lists what is inside every archive and binary in this
repository. Zips, PDFs and CAD files are not greppable; that index exists so their contents are.

### A hard-to-read file is not an empty one

**"I could not open it" is never the same as "it does not contain the answer."** Try a second
tool before concluding anything:

| File type | What worked here |
|---|---|
| Schematic PDF with vector-outlined text | `pip install pymupdf`, then `page.get_text()`. Three other tools returned nothing |
| Gerbers | They are plain text. KiCad's carry `%TO.N` / `%TO.P` net and pin attributes — a full netlist |
| JLCPCB gerber archive | Contains `FlyingProbeTesting.json`, the complete board netlist |
| Fusion `.f3z` | A zip. `DesignDescription.json` names every referenced component |
| Any `.zip` | `unzip -l` first. Contents are often documents, not just data |

### If you find the answer was already there, say so

Do not quietly present it as new. Say where it was, why it was missed, and **credit whoever wrote
it down.** Jacob and Nuh cannot read the code or the files themselves — if a finding is presented
as fresh when it was already recorded, they lose the ability to tell what is actually new.

### Specific corrections already in force

| The handoff says | Actually |
|---|---|
| Stage 6 is an open feedback loop | Loop is **closed**. 37 nA of input leakage |
| ADC clock is the "library default" | It was explicitly 40 MHz. Now 1 MHz |
| Use `TONE 8600` as the standard piezo check | No usable resonance when mounted. Do not judge the piezo by ear at all |
| PAD1 is "downstream of R1" (A.8.1) | **Upstream.** PAD1 and IC1 pin 6 are the same net; R1 feeds JP1 pin 3 |
| Power-on Z at −10 V is a tip hazard | That is the DAC output; the inverting stage puts +10 V on DSUB1. Direction is unproven |
| Re-park after `TEST` | Re-park after **`RSET` too** — it also slams Z to a rail |

**JP1**, which the handoff's own header already corrects: pin 4 is `GND` in the netlist but
**unrouted on the PCB** — no copper track lands on it on either layer. A routing defect, not a
build fault. See `docs/WIRING.md` §10.

The **firmware source comments are also wrong** about the DAC ranges. `stm_firmware.hpp:497-498`
says X and Y are −5 to +5 V. They are **±3 V**: X, Y and bias all use identical mode bits
(`0b101`), so they cannot differ, and bias measures ±3 V. `docs/WIRING.md` has the verified table.
Trust the range bits and the measurement, not the comment.

---

## 4. Hardware safety rules — never violate these

These are in `STATUS.md` too. They are repeated here because breaking one can cost hardware.

1. **Check LED1–LED4 before and after every measurement.** The DACs silently lose configuration
   roughly once an hour. Any reading taken with one of those LEDs lit is void. **There is no
   software way to detect this** — the ALERT pins are not wired to the Teensy, and `GSTS` reports
   firmware bookkeeping, not measurements.
2. **Never tell the user to run `APRH`** until the sign of the tunneling current is known.
   `approach()` compares `read_adc() > target` against a baseline that has been negative all
   project. If tunneling drives the reading more negative, it never triggers and the tip drives
   into the sample.
3. **Never raise either SPI clock above 1 MHz.** The ribbon cannot carry 40 MHz.
4. **Park Z at midscale (32768) before the motor moves.** `RSET` and `TEST` both leave Z at a rail.
5. **No cyanoacrylate** anywhere near the preamp or in its enclosure. CA vapour blooms and
   contaminates the input node — this is the current blocker.
6. **Preamp measurements are invalid if anyone is within a metre of the board.** A human body
   injects 20 to 50 nA; a tunneling current is about 1 nA.
7. **Never tell the user to send `CCON` with a tip in tunneling range.** `control_current()`
   hardcodes midscale, so engaging the loop snaps Z to 32768 from wherever it was — up to a
   ~180 nm lurch. Unfixed. See `STATUS.md` fault 2.

---

## 5. End of every session — do this before stopping

Work that isn't pushed doesn't exist as far as the other computer is concerned. **Do all four
steps.** Do not stop after step 1.

### Step 1 — write the session log

Copy `sessions/TEMPLATE.md` to `sessions/YYYY-MM-DD.md` using today's date. If a file for today
already exists, add to it rather than overwriting.

Write it the way the existing logs are written: **measurements with numbers, what was actually
observed rather than what was expected, and explicit notes on what was ruled out.** Record failed
approaches too — the false trails in this project have been as valuable as the successes.

### Step 2 — update `STATUS.md`

Rewrite the parts that changed: the stage table, open faults, next actions, open questions.
Update the "Last updated" line at the top. **This is the file the other person's Claude will read
first**, so it must reflect reality, not intentions.

### Step 3 — commit

```bash
git add -A
git commit -m "Session YYYY-MM-DD: <one line on what changed>"
```

### Step 4 — push

```bash
git pull --rebase origin main && git push origin main
```

The `pull --rebase` first is what stops the two computers from clobbering each other. If it
reports conflicts, resolve them and explain to the user in plain language what conflicted.

**Then tell the user it is pushed.** They need to know their work is safe on GitHub before they
close the laptop.

---

## 6. Where things live

| Path | What it is |
|---|---|
| `STATUS.md` | Live state. Read first, update last |
| `sessions/` | One log per work session, newest wins |
| `sessions/TEMPLATE.md` | Copy this to start a new log |
| `docs/WIRING.md` | **Verified pinouts, cable colours, LEDs, power tree.** The bench reference |
| `docs/COMMANDS.md` | **Every firmware command**, what blocks, what replies |
| `docs/ENGINEERING_REFERENCE.md` | **The cross-subsystem layer.** Grounding map, the copper-vs-aluminium tape rule, value chains from a command to a displacement and from a current to a number, the impact map for "if I change X, what else has to be rechecked", and every constant with a confidence tag |
| `docs/INDEX.md` | **What is inside every archive and binary.** Check before deriving anything |
| `docs/OPEN_QUESTIONS.md` | Every UNKNOWN and VERIFY in the project, in one place |
| `docs/UPSTREAM_MECHPANDA.md` | **The design we are actually building.** Schematic-derived facts, what differs from upstream, and the ADC reference answer |
| `docs/UPSTREAM_BERARD.md` | Reading notes from Dan Berard's build. **Context, not our design** — ours is Mech Panda's apart from the preamp. Says which of his numbers apply to us and which do not |
| `docs/OTHER_BUILDERS.md` | What independent DIY STM builders have done. Leads to test, not specifications |
| `docs/START_HERE_gotchas.md` | Things that mislead you. Read before touching hardware |
| `docs/BOM.md` | Every part, with CONFIRMED / CHOICE / UNKNOWN status |
| `docs/PROJECT_HANDOFF_SUMMARY.md` | Deep history. **Partly superseded** — see section 3 |
| `docs/soft_launch_test_procedure.md` | The staged bring-up test procedure |
| `docs/DAC_BOOT_STATE.md` | DAC power-on behaviour, read before bringing up analog |
| `docs/FIND_THE_15V_BREAK.md` | Bench procedure for tracing the −15 V rail |
| `Code/teensy/` | Teensy 4.1 firmware, PlatformIO |
| `Code/pc/` | Python tools that talk to the Teensy over serial |
| `Code/pc/stl_features.py` | Measures the printed parts straight out of the STL meshes. **Run this instead of guessing a hole size** |
| `CAD/prints/README.md` | Every printed part, measured: sizes, hole grids, **which screw goes where** |
| `CAD/`, `PCB/`, `gerbers/`, `our_preamp_cad_files/` | Design files |

### The hardware, briefly

Teensy 4.1 → four AD5761 DACs (X, Y and bias ±3 V, Z ±10 V) over SPI, and an LTC2326-16 ADC
on SPI1. A 26-pin ribbon connects the Teensy to the controller PCB. An OPA627 transimpedance
preamp with a 100 MΩ feedback resistor sits at the scan head. A 28BYJ-48 stepper through a
ULN2003 handles coarse approach, wired **directly to the Teensy**, not through the ribbon.

Firmware commands are exactly four characters: `GSTS`, `ADCR`, `RSET`, `DACX/Y/Z`, `BIAS`,
`MTMV`, `APRH`, `TEST`, `TONE`, `CCON`, `CCOF`, `PIDS`, `SCST`, `IVME`, `IVGE`, `STOP`.
Talk to the board with `Code/pc/stm_console.py` — it sends each command as a single write,
which the firmware's serial parser requires. **`docs/COMMANDS.md` documents every command**,
including which ones block and which reply. **`docs/WIRING.md` has every verified pinout** — use
it rather than re-deriving one from the handoff.

---

## 7. Working style

Carried forward from the existing documents, because it has served this project well:

- **Measurements over inference.** If a number was measured, say so. If it was derived or
  assumed, say that instead.
- **Record what was ruled out**, not just what was found.
- **Take a control measurement.** An hour was lost to a fault that did not exist because no
  known-good channel was tested with the same method.
- **Mark gaps as UNKNOWN or VERIFY** rather than guessing.
- No emoji in project documents.
