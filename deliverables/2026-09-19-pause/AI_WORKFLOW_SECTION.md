# The second instrument: the system that runs the science

**This is the canonical text for the AI-workflow section. It goes in every deliverable.**
**Written 2026-09-20 at Jacob's instruction. Adapt the length to fit the document; do not change
the claims. Every number in it is counted from the repository, and the counting command is given.**

---

## The short version, for a poster panel or an abstract

> **Neither of us writes code. So the second thing we built was the system that does.**
>
> This instrument was designed, assembled, characterised and documented by two undergraduates
> directing an AI model, working inside a framework we built for it: **a 575-line operating
> protocol, a single canonical register holding every number in the project with its provenance and
> its date, 27 append-only session logs, and a 565-line checker that runs seven classes of
> automated test at the start of every session and blocks a commit that fails.**
>
> **The point of that framework is not that the model writes well. It is that the model gets caught.**
> Over four weeks the checks and the verification passes forced the retraction of published claims
> in this project's own documents — a statistical result computed across truncated files, a
> reproducibility figure that turned out to be the feedback loop rather than the sample, a
> detector's full-scale voltage recorded backwards in a live reference document, and eleven wrong
> numbers in a single commit, caught before the second push. **Every retraction is still in the
> record next to the claim it replaced.**
>
> **An AI that produces confident prose is not hard to get. An AI workflow that produces a
> retraction is, and that is the part we built.**

---

## The longer version, for a report or a manual

### What the problem was

Two undergraduates, no prior programming experience and no prior electronics experience, work
on this instrument from two different computers, days apart, in between other commitments. **The
failure mode is not that the work is hard. It is that a number gets corrected in one document and
not in the eleven others that quote it**, and six weeks later somebody builds on the stale copy.

That is not a hypothetical. It is what happened here: on 2026-09-07 two constants changed, both had
been written into more than a dozen documents, and correcting every copy anyone could think of
**still left stale values in six files.**

### What we built

| Component | What it is | Size |
|---|---|---|
| **The protocol** (`CLAUDE.md`) | The operating instructions the model must read before doing anything: which document outranks which, what to do before recording something as unknown, what to compute before giving an instruction that touches hardware, and what to do at the start and end of every session | **575 lines** |
| **The register** (`docs/FACTS.md`) | One canonical value for every number that matters, each with units, provenance and a date, plus a RETIRED table of every value that has ever been replaced | **157 rows** — 137 live and 20 retired, counted 2026-09-20 by `Code/pc/count_facts.py`, which **is** the rule. **The 164 this said before is retired: it could not be reproduced from the wording that accompanied it, which gives 167 on the same file** |
| **The checker** (`Code/pc/check_facts.py`) | Seven classes of automated test, run at session start and before every commit | **565 lines** |
| **The session record** (`sessions/`) | One append-only log per working session. Past measurements are never rewritten | **27 logs** |
| **The reference set** (`docs/`) | Wiring, commands, components, open questions, engineering cross-references, an index of what is inside every binary and archive | **18 documents** |
| **The bench tools** (`Code/pc/`) | Python programs that talk to the instrument, analyse its output and measure the printed parts straight out of the CAD meshes | **15 tools** |
| **The session hook** (`.claude/session-start.sh`) | Runs automatically: syncs both computers, reports the state, names every session log carrying the newest date, and runs the checker | — |

### The seven checks

Run `python3 Code/pc/check_facts.py` and it verifies:

1. No value the register lists as RETIRED is still sitting in a live document.
2. Every file path cited in prose actually exists.
3. No archived, superseded document is cited as if it were current.
4. Every "safety rule N" citation resolves, **and points at the rule it claims to**.
5. Every session log is indexed in `sessions/README.md`.
6. Every RETIRED entry's qualifying wording still matches the real text.
7. The next-session plan is not older than the newest session log.

**Checks 4 and 6 exist because both failure modes happened.** Rule numbering drifted between two
files until the same number meant different rules in each; and a retirement was written with a
qualifier that no longer matched the document it was guarding.

### Every fact carries where it came from

No number is stated without a tag saying how it is known:

**`MEASURED`** at the bench · **`CALC`** derived, with the inputs shown · **`DS`** from a
manufacturer datasheet · **`MESH`** measured out of the CAD file · **`ORDER`** from an order
confirmation · **`SAID`** stated by Jacob or Nuh · **`READ`** the model's reading of a photograph,
plausible and unconfirmed

**`SAID` and `READ` are deliberately the weakest tags, and they are the ones that have been wrong
most often.** One `READ` of a part marking off a shared photograph put a wrong component into five
documents before anybody asked whose board it was. It was not ours. Every edit was reversed, and
the rule that came out of it — *a photograph is not a measurement of our hardware* — is now in the
protocol.

### What proves it works

**The system's output is not the documents. It is the retractions.**

| What was published | What the system did |
|---|---|
| "The controls reproduce better than the scans, +0.37 against +0.04" | Traced to a control file that was a single line long. **Withdrawn**, and the same defect swept across every other comparison in the project |
| A reproducible feature in the scan data, at 3.9 sigma | Found to be the feedback loop recovering from a horizontal flyback, predicted to the exact count. **Withdrawn** |
| The detector's full-scale voltage, in a live engineering reference | **Recorded backwards** — the corrected value listed as the retired one. Caught and fixed |
| A single commit's session log | **Eleven wrong numbers**, found by a verification pass and corrected before the second push |
| "d is 1.000 mm, and that settles the tunnelling question" | Wrong reading of what Jacob said. **Re-opened**, twice, and it is open now |

**Four of those five were the model's own errors, found by the framework the model was made to work
inside.** The fifth was found by Jacob, against a confident and wrong statement from the model.

### The honest boundary

**We did not train a model.** What we built is the scaffolding that makes a general-purpose model
usable as a laboratory assistant: the protocol, the single-source register, the provenance tags,
the append-only logs and the automated checks. **The model is off the shelf. The discipline is
ours**, and without it the same model produces confident, unverifiable, quietly-drifting prose —
which is what it did here before the framework existed.

### How to check any of this

```bash
wc -l CLAUDE.md Code/pc/check_facts.py   # the protocol and the checker
ls sessions/*.md | wc -l                 # the session logs
python3 Code/pc/check_facts.py           # the seven checks, run on the live repository
cat .githooks/pre-commit                 # what blocks a failing commit
```
