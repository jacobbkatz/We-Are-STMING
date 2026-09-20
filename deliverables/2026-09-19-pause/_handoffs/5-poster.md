# Handoff 5 — The candidate figure, the assets, the speaker script and the question sheet

**Subagent 5, 2026-09-19 into 2026-09-20.** Continuation of an attempt cut off by a rate limit
after gathering assets.

> **SCOPE CHANGED MID-TASK, and the change is the first thing to know.** I built a full poster; the
> lead then rebuilt `poster.html` from scratch after Jacob rejected the earlier one — *"really ugly
> and reads as a 'this is what went wrong' poster"* — and took ownership of `poster.html`,
> `poster.pdf`, `poster_preview.png` and `render.py`. **I stopped writing to all four on
> instruction.** What I own and finished: the candidate figure and its script, the asset pipeline,
> **`SPEAKER_SCRIPT.md`** and **`QUESTIONS_AND_ANSWERS.md`**, both rewritten against the lead's new
> six panels.

---

## 1. Files read, in order

| Read | |
|---|---|
| `CLAUDE.md` | in full |
| `deliverables/2026-09-19-pause/FRAMING.md` | in full, **including the addendum**: the conditions, the candidate-image instruction, and the say/do-not-say table |
| `deliverables/2026-09-19-pause/LEAD_VERIFICATION.md` | V1–V10 at the start; **V11 and V12 found mid-task** and acted on (§4) |
| `deliverables/2026-09-19-pause/report/FINDINGS_REPORT.md` | in full |
| `deliverables/2026-09-19-pause/candidates/VERDICT.md` | in full |
| `deliverables/2026-09-19-pause/photos/prepared/MANIFEST.md` | in full, plus the caption source in `photos/prepare_photos.py` |
| `deliverables/2026-09-19-pause/report/UPDATE_NOTE.md` | for the repository URL and the recipient-neutral phrasing |
| `STATUS.md`, `docs/OPEN_QUESTIONS.md` (the `d` row), `docs/NEXT_SESSION_PLAN.md`, `docs/FACTS.md` | the passages these documents cite |
| All nine presentation figures | opened and looked at individually, plus `figures/code/*.py` docstrings for their sources |
| `sessions/data/2026-09-19-bench/ycontrol_run2/3/4` | read directly, to draw the candidate figure |

**The brief named a captions file in `figures/` that does not exist.** The figures carry their
captions **inside the image**: a title, a subtitle, a source line and a "what this does not show"
note, all baked in by `figures/code/`. Every caption written here was written against those, and
against the sources they name.

---

## 2. What I produced

| Output | How to reproduce |
|---|---|
| **`poster/make_candidate_figure.py`** and **`poster/assets/fig10_candidate.png`** — the three-Y candidate, drawn in the figure set's house style from the raw CSVs. **The lead's poster uses it in panel 06** | `python3 deliverables/2026-09-19-pause/poster/make_candidate_figure.py` |
| **`poster/prepare_assets.py`** extended — all **nine** figures now copied (it listed six, one of them a file that was never made), plus `15_workshop_room.jpg` | `python3 deliverables/2026-09-19-pause/poster/prepare_assets.py` |
| **`poster/SPEAKER_SCRIPT.md`** — a spoken 2–3 minute walk-through **panel by panel, in the new order**, a 20-second version, and the one question that decides the conversation | hand-written |
| **`poster/QUESTIONS_AND_ANSWERS.md`** — 25 questions with answers that each trace to a named source, including the hard ones, a "what this number on the poster means" table, and **seven questions whose answer is not in the repository and must not be improvised** | hand-written |

**Not mine any more, and untouched since the instruction:** `poster.html`, `poster.pdf`,
`poster_preview.png`, `render.py`.

**`python3 Code/pc/check_facts.py` exits 0.**

---

## 3. Why the candidate figure was redrawn rather than reused

**`candidates/gallery/03_candidateB_three_y.png` could not go on a poster as it stood**, for two
reasons that are about accuracy, not style:

1. Its heading calls run 2 *"the 3.9 sigma run"*. **That sigma was withdrawn at this pause point**
   (`VERDICT.md` §4): it treated 45 within-place and 108 between-place pairwise correlations as
   independent when every pass appears in many of them. The defensible figure is the permutation
   **p = 0.0036**.
2. Its heading says the runs are *"~2 min"* apart. **`LEAD_VERIFICATION.md` V9 and V5b correct
   that**: neither `ycontrol` log carries a timestamp, so the interval is **UNKNOWN**, bounded only
   by the ~5 minutes between the two timestamped sections around them.

`make_candidate_figure.py` redraws the same three runs from the same raw files, with the same
detrending convention (`Code/pc/stm_y_control.py`), in the figure set's own style, and carries the
corrected statements in its footer. **No data are changed, and the script says so at the top.**
Run 2, run 4 (the repeat) and run 3 (the X-held control) are drawn on **one shared y scale**,
because the control genuinely is smaller and rescaling each panel to fill itself would hide exactly
that.

---

## 4. The tunnelling position changed twice under me — what the two documents now say

**My brief said to present the 2026-09-17 junction as UNDECIDED on a threshold of `d` below about
0.13 mm. That threshold is wrong, and both documents were rewritten.**

| When | What the record said |
|---|---|
| My brief, from V10 | Undecided; below ~0.13 mm it was tunnelling; one straightedge settles it |
| **V11** | **0.13 mm conflates two criteria.** On the decay criterion the tip must be within **26 µm**: one motor step is 155 nm of screw, tunnelling needs 0.1 nm per decade, so the lever ratio must be ~1,550. At 1 mm it is **39× too slow**; at 0.13 mm, still 5× too slow. 0.13 mm is the **wobble** criterion, a different question |
| **V12**, and the lead's message | **`d` is still UNKNOWN** and is marked **CONTESTED — do not use** in `docs/FACTS.md`. Jacob reported it is **under 0.5 mm**, which is as fine as a straightedge and an eye resolve, and **could not resolve 26 µm** |

**So both documents now carry this, and keep panel 06 deliberately undecided:**

> The 2026-09-19 junction was a pressed contact, measured. Our best junction, on the 17th, was a
> real barrier; for it to have been a vacuum gap the tip would have to sit within about **26 µm** of
> the pivot line. **We measured that distance to under half a millimetre and cannot resolve
> 26 µm — so we do not say.** An eyepiece or an optical comparator closes it in minutes, with the
> power off, and the same measurement gives the instrument its first height scale.

**Neither document claims tunnelling, and neither dismisses it.** Both say in a marked block that
**if the poster's wording differs from theirs, the poster wins**, and point at V11, V12 and the
CONTESTED row in `docs/FACTS.md`.

---

## 5. What is in the two documents, and what they deliberately refuse to do

**`SPEAKER_SCRIPT.md`** — opens on the conditions, in Jacob's own terms: two first-year students,
neither writes code, first soldering either of them has done, a basement in a lived-in house with
people moving and no control of the air. **Then straight into what works**, panel by panel, and the
limitation once, as a measurement, in panel 04. It ends with the two sentences worth memorising.
**Stage directions name what to point at as well as the panel number**, so a renumbered poster does
not invalidate it.

**`QUESTIONS_AND_ANSWERS.md`** — five hard questions from somebody who knows what an STM is, ten
common ones, a table mapping each headline number on the poster to a defensible sentence, and
**seven questions whose answer is genuinely not in the repository**: the total cost, the scan area
in nanometres, the resolution, the nm-per-Z-count, the scan speed for imaging, the shield
continuity, and what is actually moving the gap. **For every one of those the instruction is to say
"we have not measured that"**, with a note that the cost figure belongs in `docs/INVENTORY.md` if
Jacob knows it.

**Both refuse, explicitly:** any claim of tunnelling, any claim of an image, any distance in
nanometres offered as if it were measured, and any number not in `docs/FACTS.md` or
`LEAD_VERIFICATION.md`.

---

## 6. What Jacob must check before anything is printed

1. **THE PAGE SIZE IS PROVISIONAL.** 48 × 36 in landscape was **not** checked against any UCSD event
   specification. **No event spec exists anywhere in the project files and none was invented.** The
   size, the orientation and any required template have to come from the event.
2. **Is the repository public?** The poster and the Q&A both print
   `github.com/jacobbkatz/We-Are-STMING` — real, from `git remote`, and already in the draft
   collaborator note. **If the repository is private, that line should come out** and the Q&A says
   to offer an email instead.
3. **The photographs with faces.** Jacob's permission of 2026-09-19 covers the poster, per
   `photos/prepared/MANIFEST.md`. **Nuh has not been asked as far as the repository records**, and
   he is in the team frame.
4. **Affiliations.** "University of California San Diego" and "Worcester Polytechnic Institute" come
   from the brief. **Nothing in the repository confirms either**, and a poster carries them as
   institutional claims.
5. **`d`.** If it is measured properly before the event, panel 06, the speaker script's last
   paragraph and the Q&A's second answer all change together. They are cross-referenced so that is
   findable.

---

## 7. What I checked, and how

- **Every figure was opened and looked at individually**, and every panel of my own draft was
  re-checked zoomed after each render, until the renderer reported no cut-off text twice in a row.
- **Every number was traced to a source**, and the ones corrected at this pause point were taken in
  their corrected form: **V^1.55** not V², **+0.04 against +0.07** not +0.37, **209 reproducibility
  tests** and **p < 2.4 × 10⁻⁴**, the permutation p values rather than the withdrawn 3.9 σ, **12
  stages** in the calibration chain rather than the report's "fifteen things" (its own list
  contradicts it), and the interval between the three-Y runs left **UNKNOWN**.
- **Resolution**: every image placed in my draft sat at **200 dpi or better** at its printed size;
  the figures are the 300 dpi print exports.
- **A renderer defect worth knowing about, since the lead now owns that file.** Rendering the same
  HTML twice gave two different answers: once, the PDF came out **with the pictures missing and the
  text in a fallback font**, because the page was printed before the fonts and images had settled.
  **Waiting on `document.fonts.status === 'loaded'`, forcing every image to `decode()`, and
  requiring the layout to stop changing before measuring** made it deterministic. **A render that
  looks right once is not evidence** — it is worth checking the PDF's file size is in the range you
  expect before sending it anywhere.
