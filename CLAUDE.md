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
2. **Every session log carrying the newest date in `sessions/`** — what happened last session and
   why. **There is often more than one file for a date**, because both of us log the same day and
   the second is written hours after the first. `2026-09-09.md` and `2026-09-09-jacob.md` are two
   different sessions, and **neither supersedes the other.**

   > **Corrected 2026-09-09.** This said "the newest **file**", singular, and the start-up hook
   > implemented it as `ls sessions/*.md | sort | tail -1`. That is a lexical sort: `-` sorts before
   > `.`, so **`2026-09-09-jacob.md` sorts BEFORE `2026-09-09.md`** and the later log of the day was
   > never named. Every session since has been pointed at the older of the two. **Fixed in both
   > places** — see `sessions/2026-09-09-jacob.md` §15.
3. Anything else you need for the specific task.

A `SessionStart` hook in `.claude/settings.json` tries to do the pull automatically and prints a
summary. **Do not rely on it silently** — confirm you are up to date. If the hook reported a
problem, deal with it before starting work.

> **The hook is code and it has been wrong.** On 2026-09-09 an audit found four defects in it, all
> of which fed a session bad information in the very first thing it reads: it named the wrong
> session log, printed a STATUS.md header cut off mid-sentence, would have merged `origin/main`
> into a feature branch unasked, and — when `check_facts.py` reported **any** of its four problem
> types, or crashed outright — announced a retired value as the cause regardless. **All four are
> fixed and each is commented at its site in `.claude/session-start.sh`.** Treat the hook's output
> as evidence, not as gospel: if what it says does not match what you find, believe the repository.

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
2. **Every session log carrying the newest date in `sessions/`** — newer sessions correct older
   ones. **Two logs sharing a date do not correct each other**; they are different sessions.
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
| Stage 6 is an open feedback loop | Loop is **closed**. 119 nA of input leakage |
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

## 3bb. One value per fact — `docs/FACTS.md`

**This repository's most expensive failure mode is a corrected number that only got corrected in
some places.** On 2026-09-07 the ADC full scale went from 4.096 V to 10.24 V and the preamp offset
from 37 nA to 119 nA. Both had been written into more than a dozen documents. **Correcting the ones
anybody thought of still left stale copies in six files**, where the next session would have
believed them.

**So:**

1. **`docs/FACTS.md` holds the canonical value of every number that matters.** Value, units,
   provenance, date.
2. **Do not build a second register.** A table, list or reference block of constants anywhere but
   `docs/FACTS.md` is the thing that goes wrong — two registers drift apart and nobody can tell
   which is current. **Citing a number inside an argument is different and is fine**, because prose
   with the figures stripped out and replaced by links is unreadable. **The protection is the
   checker, not a prohibition.**

   > **Corrected 2026-09-09.** This rule read "do not restate one of those numbers in another
   > document, link to it" — an absolute that **the repository has never followed and cannot**:
   > `10.24 V` is in 11 live documents, `119 nA` in 10, **including this file.** The 2026-09-08
   > audit had already decided against it in writing (`sessions/2026-09-08.md`, "One honest
   > limitation") and `CLAUDE.md` was never updated to match. **A rule that every document breaks
   > teaches the reader that the rules here are decorative**, which is worse than the duplication
   > it was trying to prevent.
3. **When a value changes, change it in `docs/FACTS.md` first**, add the old one to its RETIRED
   table, then run `python3 Code/pc/check_facts.py` and fix what it finds.
4. **Session logs are history and keep their original numbers.** The checker skips them. Never
   rewrite a past measurement.

The checker runs automatically at session start. **If it reports something, fix it before starting
work** — it means a number known to be wrong is sitting where it will be believed.

---

## 3c. Before you tell them to do anything, work out what it will do

**Added 2026-09-07, after this failed.** A session told Nuh to bond a floating ground, and only
afterwards said "check the datasheet absolute maximum first". **That is backwards, and it put the
ADC at risk.** Jacob's words: *"you have the data, not us. 100% should never happen again."*

He is right. **You have the repository, the netlists, the datasheets and the arithmetic. They have
a meter and a bench.** Checking is your job, not theirs.

**Before any instruction that changes a connection, a supply voltage, or sends a command:**

1. **Compute the resulting state at every node the action touches.** Write the number down. If
   bonding a node changes what an amplifier or converter sees, say what it will now see.
2. **If any part could be taken past a limit, get the limit FIRST.** Search the repository, then
   the web. `WebSearch` and `WebFetch` are available — use them.
3. **If you cannot get the number, say so plainly and do not order the action.** Give a route that
   does not depend on it. "Check the datasheet" is not an instruction to hand to them; it is work
   you have not done.
4. **Never order steps so that a protective check comes after the risky one.**
5. **State the expected reading.** If they see something else, that is information rather than
   alarm.

**A test you have not thought through is not a test. It is an experiment on their hardware.**

---

## 3d. What we physically own is not in any design file. Ask.

**Added 2026-09-09, after getting this wrong four times in one session.**

Sections 3b and 3c are both about work you can do yourself: search the repository, get the
datasheet, do the arithmetic. **This section is the opposite case — the one where no amount of
searching will help, because the answer was never written down.**

| I inferred | From | Actually |
|---|---|---|
| The preamp board was hand-populated | `docs/BOM.md` listing its parts individually | **JLCPCB PCBA, 2 off.** Most of those parts arrived soldered down |
| We already own the Keystone 11301 standoff | `docs/BOM.md` "CONFIRMED", and the shopping list's "already have" | **We own the 11311.** It needs a hole 1.34 mm bigger than ours and would not fit |
| Nobody had checked C1/C2 polarity | Nothing said otherwise | **JLCPCB raised it at order time** and it was settled by email |

**`docs/BOM.md` is a specification. It records what was chosen, not what arrived.** A netlist
records what was drawn. A shopping list records what someone intended to buy. **None of them is
an inventory**, and reading one as if it were is how all three errors above happened.

**So, before stating anything about what is in the room — a part we own, a quantity, how a board
was assembled, what a supplier did or asked:**

1. **Check [`docs/INVENTORY.md`](docs/INVENTORY.md).** That is the only file that records physical
   reality, and it carries provenance: an order number, a photo, a bench observation, or "Jacob
   said so", with a date.
2. **If it is not there, ask.** One question costs a sentence. A wrong assumption about what is on
   the bench costs a purchase, a rework, or a part.
3. **If you cannot ask, write UNKNOWN.** Never fill the gap by inferring from a design document.
4. **When they tell you, write it into `docs/INVENTORY.md` in the same session.** These facts live
   in Jacob and Nuh's heads and in their email. Anything that stays in the conversation is lost
   the moment the context is compacted — which is exactly how this failure happened.

> **An order confirmation outranks every document in this repository, including this one.**

---

## 4. Hardware safety rules — never violate these

> **`STATUS.md`'s numbered list is the authority and the only one that may be cited.** It runs
> **0, 0b, 0c, then 1 to 13**, and it grows. **The rules below are deliberately UNNUMBERED.**
>
> **Why.** Until 2026-09-09 this section was a numbered list of seven, and `STATUS.md` had a
> different list of sixteen. **The same number meant different rules in the two files** — this
> section's 7 was `CCON`, `STATUS.md`'s 7 was the tip-holder meter check — while this file claimed
> "these are in `STATUS.md` too". **Never cite "safety rule N" against this section.** When you see
> "safety rule N" anywhere in the repository it means `STATUS.md`, always.

**These are the ones that cost hardware. The list is a summary, not a substitute — read
`STATUS.md`'s before any bench session, because it is longer and it changes.**

- **Check LED1–LED4 before and after every measurement.** They are lit at **every** power-on and
  `RSET` clears them — power sequencing, not a random fault, see `STATUS.md` fault 4. Any reading
  taken with one lit is void. **There is no software way to detect this** — the ALERT pins are not
  wired to the Teensy, and `GSTS` reports firmware bookkeeping, not measurements.
- **Never tell the user to run `APRH`** until the sign of the tunneling current is known.
  `approach()` compares `read_adc() > target` against a baseline that has been negative all
  project. If tunneling drives the reading more negative it never triggers, and the tip drives into
  the sample.
- **Never raise either SPI clock above 1 MHz.** The ribbon cannot carry 40 MHz.
- **Park Z at midscale (32768) before the motor moves.** `RSET` and `TEST` both leave Z at a rail,
  so re-park after either.
- **No cyanoacrylate** anywhere near the preamp or in its enclosure. CA vapour blooms and
  contaminates the input node — this is the current blocker.
- **Preamp measurements are invalid if anyone is within a metre of the board.** A human body
  injects tens of nA; a tunneling current is about 1 nA.
- **Never tell the user to send `CCON` with a tip in tunneling range.** `control_current()`
  hardcodes midscale, so engaging the loop snaps Z to 32768 from wherever it was. Unfixed. See
  `STATUS.md` fault 2.

**Four more that live only in `STATUS.md`, and are just as capable of costing hardware or a day.
Added here 2026-09-09 because this section had silently omitted them:**

- **An out-of-range DAC value does not error — it silently jumps the axis to the opposite rail.**
  `write()` takes a `uint16_t`, so anything outside 0–65535 wraps modulo 65536. **A tip hazard, not
  a typo.** `STATUS.md` safety rule 13.
- **No preamp measurement is valid until the board has been powered for 45 minutes.** The offset
  climbs for over an hour after power-on. A reading taken early looks like a spectacular
  improvement and is worthless. `STATUS.md` safety rule 0.
- **A multimeter cannot clear a suspect leakage path here.** What matters is 100 MΩ to 10 GΩ; a
  typical DMM tops out near 60 MΩ, so **"OL" only proves ">60 MΩ"**. **Never read OL as "ruled
  out."** `STATUS.md` safety rule 12.
- **Do not glue the spare preamp board to anything**, and **do not rebuild the preamp or the tip
  lead** until the measurement chain is fixed. `STATUS.md` safety rules 10 and 0b.

---

## 5. End of every session — do this before stopping

Work that isn't pushed doesn't exist as far as the other computer is concerned. **Do all five
steps.** Do not stop after step 1.

### Step 1 — write the session log

Copy `sessions/TEMPLATE.md` to `sessions/YYYY-MM-DD.md` using today's date.

**If a log for today already exists, check whose it is before touching it.** If it is the other
person's, **do not append to it** — start `sessions/YYYY-MM-DD-<your name>.md`. Only add to a file
that is your own session's. **Then add a row to `sessions/README.md`**, which `check_facts.py`
verifies.

> **Corrected 2026-09-09.** This said "if a file for today already exists, add to it". On
> 2026-09-09 the existing file was **Nuh's**, and following this literally would have written
> Jacob's work into Nuh's log.

Write it the way the existing logs are written: **measurements with numbers, what was actually
observed rather than what was expected, and explicit notes on what was ruled out.** Record failed
approaches too — the false trails in this project have been as valuable as the successes.

### Step 2 — update `STATUS.md`

Rewrite the parts that changed: the stage table, open faults, next actions, open questions.
Update the "Last updated" line at the top. **This is the file the other person's Claude will read
first**, so it must reflect reality, not intentions.

### Step 3 — update `docs/NEXT_SESSION_PLAN.md`

**The only place that says what to do next at the bench**, written to be executed with no memory of
any conversation. Rewrite what this session changed, strike through what is now moot, and **update
its `Last updated` line** — `check_facts.py` fails if a session log is newer than it, and the
pre-commit hook will then block the commit.

> **Added 2026-09-09.** Nothing had ever updated this file. It sat stale for two days across three
> sessions because neither `/wrap` nor `/catchup` mentioned it.

### Step 4 — commit

```bash
git add -A
git commit -m "Session YYYY-MM-DD: <one line on what changed>"
```

### Step 5 — push

```bash
git pull --rebase origin main && git push origin main
```

The `pull --rebase` first is what stops the two computers from clobbering each other. If it
reports conflicts, resolve them and explain to the user in plain language what conflicted.

**Then tell the user it is pushed.** They need to know their work is safe on GitHub before they
close the laptop.

---

## 6. Where things live

### Who owns what — check this before writing a fact down

**Established 2026-09-08.** Every kind of information has exactly one authoritative home. Writing
it anywhere else creates a copy that will drift.

| Information | Canonical home | Everywhere else |
|---|---|---|
| **Any constant or measured number** | **`docs/FACTS.md`** | **no second register.** Citing a figure in prose is fine and `check_facts.py` guards it — see §3bb |
| **Any open question, UNKNOWN or VERIFY** | **`docs/OPEN_QUESTIONS.md`** | link to it |
| **What to do next at the bench** | **`docs/NEXT_SESSION_PLAN.md`** | `STATUS.md` summarises, does not duplicate |
| **Current state, faults, safety rules** | **`STATUS.md`** | — |
| **Documented conflicts between sources** | **`docs/ENGINEERING_REFERENCE.md`** §11 | — |
| **What happened on a given day** | **`sessions/YYYY-MM-DD.md`**, or `-<name>.md` if more than one that day | append-only, never rewritten. Index every log in `sessions/README.md` |
| **Pinouts and board layout** | **`docs/WIRING.md`** | — |
| **Part specs and datasheet facts** | **`docs/COMPONENTS.md`** | — |
| **What is inside a zip, PDF or mesh** | **`docs/INDEX.md`** | — |
| **What we physically own** | **`docs/INVENTORY.md`** | `docs/BOM.md` is a specification, never an inventory |

**`python3 Code/pc/check_facts.py` enforces the first row and checks for broken links and
archived documents cited as current. It runs automatically at session start.**

### Every file, and what it is for

| Path | What it is |
|---|---|
| `STATUS.md` | Live state. Read first, update last |
| `sessions/` | One log per work session, newest wins |
| `sessions/TEMPLATE.md` | Copy this to start a new log |
| `docs/WIRING.md` | **Verified pinouts, cable colours, LEDs, power tree.** The bench reference |
| `docs/COMMANDS.md` | **Every firmware command**, what blocks, what replies |
| `docs/ENGINEERING_REFERENCE.md` | **The cross-subsystem layer.** Grounding map, the copper-vs-aluminium tape rule, value chains from a command to a displacement and from a current to a number, the impact map for "if I change X, what else has to be rechecked", and every constant with a confidence tag |
| **`docs/FACTS.md`** | **The canonical value of every number that matters, with provenance — and a list of RETIRED values.** One value per fact. **Do not restate a number from here elsewhere; link to it.** When a value changes, change it here first |
| `docs/COMPONENTS.md` | **Every electronic part, with the specs that matter and the design cross-checked against them.** Voltage limits, stability, noise, pinouts, what the Teensy can and cannot drive. **Check here before looking up any datasheet** |
| `docs/NEXT_SESSION_PLAN.md` | **The prioritised plan for the next bench session**, written to be executed with no memory of any conversation |
| `docs/INDEX.md` | **What is inside every archive and binary.** Check before deriving anything |
| `docs/OPEN_QUESTIONS.md` | Every UNKNOWN and VERIFY in the project, in one place |
| **`docs/INVENTORY.md`** | **What is physically in the room**, with provenance — order numbers, photos, bench observations. **Not the BOM.** The BOM says what was specified; this says what arrived. **Never infer what we own from a design file** — see section 3d |
| `docs/UPSTREAM_MECHPANDA.md` | **The design we are actually building.** Schematic-derived facts, what differs from upstream, and the ADC reference answer |
| `docs/UPSTREAM_BERARD.md` | Reading notes from Dan Berard's build. **Context, not our design** — ours is Mech Panda's apart from the preamp. Says which of his numbers apply to us and which do not |
| `docs/OTHER_BUILDERS.md` | What independent DIY STM builders have done. Leads to test, not specifications |
| `docs/START_HERE_gotchas.md` | Things that mislead you. Read before touching hardware |
| `docs/BOM.md` | Every part, with CONFIRMED / CHOICE / UNKNOWN status |
| `docs/PROJECT_HANDOFF_SUMMARY.md` | Deep history. **Partly superseded** — see section 3 |
| `docs/soft_launch_test_procedure.md` | The staged bring-up procedure. **Partly superseded — it carries a scope banner saying which parts.** Stages 0–6 are still the reference for powering up from cold |
| `docs/DAC_BOOT_STATE.md` | DAC power-on behaviour, read before bringing up analog |
| `docs/archive/` | **Superseded procedures, kept with banners.** Not current instructions — each says what replaced it and where its unique content went |
| `Code/teensy/` | Teensy 4.1 firmware, PlatformIO |
| `Code/pc/` | Python tools that talk to the Teensy over serial |
| `Code/pc/stl_features.py` | Measures the printed parts straight out of the STL meshes. **Run this instead of guessing a hole size** |
| `Code/pc/check_facts.py` | Reports anywhere a value `docs/FACTS.md` lists as retired still sits in a live document. **Runs automatically at session start** |
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

### Before you say something is fixed — added 2026-09-09, after three shallow passes in one day

**On 2026-09-09 Jacob asked why sessions had got worse. It took three attempts to answer, and the
first two both stopped early. The misses were not subtle: a mechanical `grep` found them in
seconds.** These four rules are what would have caught them, and they cost almost nothing.

1. **A defect is a class, not an instance. Grep for every other occurrence before reporting it
   fixed, and say how many you found.** The start-up hook assumed one session log per day. That
   assumption was in **eight** places — `CLAUDE.md` three times, both slash commands, the template,
   the plan, and the index. The first fix changed one of them and called it done.

2. **A test that has never failed has not been run.** Re-introduce the fault deliberately and
   confirm the check goes red. The first version of the safety-rule checker **passed while the bug
   was present** — it reused a regex matching `wrong` and `error`, words that sit beside both real
   miscitations in ordinary prose. It looked green because it had only ever been run on a clean
   tree.

3. **Run the check as its own command and read the exit code, before committing.** Not inside an
   `&&` chain, which reports the success of the last thing in it. Commit `1198651` was pushed to
   `main` with `check_facts.py` failing on its own repository, for exactly that reason.

4. **"I have found the root cause" is a hypothesis, not a stopping condition.** A satisfying causal
   story feels like completion and is not. **Enumerate the mechanisms that could produce the
   symptom, then test each one** — the first two passes each followed a single thread to a tidy
   ending and stopped there.

### The one thing that actually limits the damage — added 2026-09-09

**Errors are not the problem. Acting on them before Jacob or Nuh can see the reading is.** Every
one of the nine failures on 2026-09-09 was caught by them — but only after the work was done,
written into the repository, and committed. The cost was never the mistake; it was the twenty
minutes and the commit that followed it.

**So before spending effort on any of these three, say in one sentence which reading you took:**

| Trigger | Why |
|---|---|
| **They are about to spend money** | A wrong reading costs a second order and shipping |
| **An instruction that touches hardware** | §3c already covers the arithmetic; this covers the intent |
| **Writing a claim about physical reality into the repository** | It is inherited as fact by the other computer |

**"You mean the flux for the preamp, not the piezo paste — confirming before I write it up"** costs
one line and would have saved the entire exchange that produced this rule. **They correct it in one
word if it is wrong.**

**This is prose, and prose has failed here before.** It is worth adding only because it differs
from the rules above in kind: those ask for better judgement, which is the thing that failed. This
one asks to **expose the judgement before acting on it**, which is checkable by someone else.

> **What was NOT the cause.** `CLAUDE.md` roughly doubled in length over four days and that looked
> like the obvious culprit. **It was not, and there is no evidence it was.** Every defect found was
> a statement that had become **untrue** — a citation pointing at a renumbered rule, a list claiming
> to mirror another list, a naming convention nobody followed. **Length was a red herring; accuracy
> was the problem.** Do not compress this file in the belief that it will help.



Carried forward from the existing documents, because it has served this project well:

- **A photograph is not a measurement of OUR hardware. Ask whose board it is before reading
  anything off it.** **Applied 2026-09-09 from Nuh's own recommendation** in
  `sessions/2026-09-09.md` §9, which had been written down and never acted on. That session read
  the marking `A BB OPA124U` off a shared photo and edited **five documents** to say that is our
  fitted part, before anyone asked whose board it was. **It was Dan Berard's.** Every edit was
  reversed. The rule below was already in this file for wire colours; **it generalises to any
  hardware fact — a part marking, a connector, a solder joint, a colour, a count.**
- **A search-result summary is not a datasheet.** Same session, same day: the Keystone 11301's
  hole was recorded as Ø2.03 mm from a search snippet and declared a clearance fit. **2.03 mm is
  the part's length below the flange, not a diameter.** The real figure is larger than our hole —
  interference, not clearance. **Get the manufacturer's own parameter table before a number
  decides anything.**
- **Use wire colours, and use the J1 / J2 ones from `docs/WIRING.md`.** Jacob and Nuh prefer
  colours to pin numbers, and they translate to their own jumpers themselves. **Do not read
  colours off a photograph** — the jumper leads at the preamp end are different colours from the
  J1/J2 wiring, and quoting a photo's colours back is what would cause a mistake. Say "the J2
  −15 V wire" using the documented colour, and let them do the translation.
- **Measurements over inference.** If a number was measured, say so. If it was derived or
  assumed, say that instead.
- **Record what was ruled out**, not just what was found.
- **Take a control measurement.** An hour was lost to a fault that did not exist because no
  known-good channel was tested with the same method.
- **Mark gaps as UNKNOWN or VERIFY** rather than guessing.
- No emoji in project documents.
