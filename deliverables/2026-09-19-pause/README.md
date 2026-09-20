# The pause-point deliverables — what each one is, and which to read

**Written 2026-09-19, rewritten 2026-09-20.** Experimental work stopped when the instrument was
taken apart and moved. This directory turns the bench record into things people can read.

**Every document here is also a Google Doc in Jacob's Drive, editable.** The Drive folder carries an
index with every link. **The repository is the source of truth**; a Drive copy is a snapshot, and if
the two differ, the repository is right.

---

## If you only read one thing

| You want | Read |
|---|---|
| **What this project claims, in one sentence** | [`FRAMING.md`](FRAMING.md) — the first section |
| **Why there is no image, and what would fix it** | [`WHAT_HELD_US_BACK.md`](WHAT_HELD_US_BACK.md) — five blockers, each with a one-line fix |
| **The whole story, properly** | [`report/FINDINGS_REPORT.md`](report/FINDINGS_REPORT.md) |
| **To rebuild or operate the instrument** | [`manual/MANUAL.md`](manual/MANUAL.md) |
| **To stand next to the poster and answer questions** | [`poster/SPEAKER_SCRIPT.md`](poster/SPEAKER_SCRIPT.md) and [`poster/QUESTIONS_AND_ANSWERS.md`](poster/QUESTIONS_AND_ANSWERS.md) |

**The one sentence, and it is Jacob's own:**

> ## **"We detected tunnelling, but weren't able to maintain tunnelling range for long enough to get an image."**

---

## The documents, by what they are for

### Read first

| File | What it is |
|---|---|
| [`FRAMING.md`](FRAMING.md) | **How this work is presented, and why.** Carries the canonical sentence above with each half separately sourced, and a say-this / not-this table. **Binding on every other deliverable** |
| [`WHAT_HELD_US_BACK.md`](WHAT_HELD_US_BACK.md) | **The five things between this instrument and an image**, ranked by how much each actually blocked one, each with a one-sentence fix. Opens by saying what was NOT the problem — the electronics |
| [`JUNCTIONS.md`](JUNCTIONS.md) | **Every junction we made and what each one showed.** Three of them, three decisive tests. Written to answer "show me why you think no tunnelling happened", then corrected the same day when that question turned out to be mis-framed |

### The report

| File | What it is |
|---|---|
| [`report/FINDINGS_REPORT.md`](report/FINDINGS_REPORT.md) | **The full technical account.** Every result, every limitation, every withdrawn claim |
| [`report/PAUSE_POINT_HANDOFF.md`](report/PAUSE_POINT_HANDOFF.md) | **For someone picking the project up cold.** State, blockers, and where everything lives |
| [`report/UPDATE_NOTE.md`](report/UPDATE_NOTE.md) | **A draft email to outside contacts, for Jacob to adapt and send.** Not a status note — read the questions in it before sending anything |
| [`report/LINKEDIN_POST.md`](report/LINKEDIN_POST.md) | Four drafts, a table of what is deliberately not claimed, and a checklist for before posting |

### The poster

| File | What it is |
|---|---|
| [`poster/poster.html`](poster/poster.html) | **The poster source.** All text is plain HTML; panel 06 is marked for Jacob to word himself |
| `poster/poster.pdf` | **The print file. 48 x 36 in landscape, confirmed by Jacob 2026-09-20** |
| [`poster/render.py`](poster/render.py) | Turns the HTML into the PDF and a preview. Reports anything that does not fit |
| [`poster/SPEAKER_SCRIPT.md`](poster/SPEAKER_SCRIPT.md) | A 2-3 minute walk-through, a 20-second version, and the one question they will ask |
| [`poster/QUESTIONS_AND_ANSWERS.md`](poster/QUESTIONS_AND_ANSWERS.md) | Hard questions, common questions, and **seven whose answer is not in the repository** |

### The manual

| File | What it is |
|---|---|
| [`manual/MANUAL.md`](manual/MANUAL.md) | **The instrument, end to end**: what it is, how to bring it up, how to operate it, what goes wrong |
| [`manual/CHANGELOG.md`](manual/CHANGELOG.md) | What changed in the manual and why |
| [`manual/INCONSISTENCIES.md`](manual/INCONSISTENCIES.md) | Contradictions found between source documents while writing it |

### The evidence

| File | What it is |
|---|---|
| [`LEAD_VERIFICATION.md`](LEAD_VERIFICATION.md) | **Every claim re-derived independently before it was allowed into a deliverable.** Thirteen checks, including three where the lead was wrong and was corrected. **The one document that shows how the conclusions were reached rather than what they are** |
| [`analysis/FINDINGS.md`](analysis/FINDINGS.md) | The analysis, in full |
| [`analysis/DATA_INVENTORY.md`](analysis/DATA_INVENTORY.md) | **Every raw file the project holds**, with what is in it and what is wrong with it |
| [`analysis/COMPARISON_TABLES.md`](analysis/COMPARISON_TABLES.md) | The numbers side by side |
| [`candidates/GALLERY.md`](candidates/GALLERY.md) | **Every candidate image**, with what it is and is not |
| [`candidates/VERDICT.md`](candidates/VERDICT.md) | What survived scrutiny. **One measurement is still genuinely open** |

### The pictures

| File | What it is |
|---|---|
| [`figures/`](figures/) | **Thirteen figures**, `png/` for screen and `print/` for the poster, each regenerable by the script of the same name in `figures/code/` |
| [`photos/IMAGE_INVENTORY.md`](photos/IMAGE_INVENTORY.md) | **All 92 photographs of our own hardware, captioned**, each marked `SAID` or `READ` |
| [`photos/MECHANICAL_OBSERVATIONS.md`](photos/MECHANICAL_OBSERVATIONS.md) | What the photographs show about the mechanics — **and three gap-motion candidates that came from them, which are leads and not evidence** |
| [`photos/prepared/MANIFEST.md`](photos/prepared/MANIFEST.md) | The images prepared for publication, with permissions |

### Context and working notes

| File | What it is |
|---|---|
| [`BRIEF.md`](BRIEF.md) | The shared context this work ran on |
| [`SOURCE_INVENTORY.md`](SOURCE_INVENTORY.md) | Where every input came from |
| [`NUH_PHOTOS_ADDENDUM.md`](NUH_PHOTOS_ADDENDUM.md) | The photographs Nuh contributed |
| [`AI_WORKFLOW_SECTION.md`](AI_WORKFLOW_SECTION.md) | **The canonical text on the framework built so an AI model could run this project reliably** — the protocol, the register, the checker, and the retractions that prove it works. Poster panel 07 |
| [`_handoffs/`](_handoffs/) | **Frozen history.** What each agent was told and what it reported. **Deliberately not updated** — do not quote a number from one |

---

## Two things to know before quoting anything

1. **Numbers live in [`docs/FACTS.md`](../../docs/FACTS.md), not here.** Citing a figure in prose is
   fine and normal; `Code/pc/check_facts.py` guards against a retired value sitting in a live
   document. **If a number here disagrees with `docs/FACTS.md`, `docs/FACTS.md` wins.**
2. **Withdrawn claims are kept, struck through, beside what replaced them.** That is deliberate.
   **If you see a strike-through, the text after it is current and the text before it is what was
   believed.**
