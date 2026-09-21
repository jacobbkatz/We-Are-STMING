# Handoff 3 — Setup photographs and apparatus documentation

**Subagent 3, 2026-09-19.** Scope grew twice mid-flight: 62 photographs at launch, then 92 when
Nuh's 30 arrived. **All 61 new frames were opened and looked at individually**, at full resolution
wherever a detail decided anything.

---

## 1. Files reviewed

| Read first, in order | |
|---|---|
| `CLAUDE.md` | in full, including the photograph rule and §3d |
| `deliverables/2026-09-19-pause/BRIEF.md` | in full, §5 especially |
| `deliverables/2026-09-19-pause/NUH_PHOTOS_ADDENDUM.md` | in full, both versions (it gained the "WHO IS WHO" block mid-task) |
| `Images/ours/README.md` | in full, including the section on why `d` cannot be measured |
| `docs/INVENTORY.md` | in full |
| `docs/WIRING.md` §6–§10, `docs/BOM.md`, `STATUS.md` top blocks | |
| `git show 6b41855` | the 2026-09-18 23:13 session's two photo readings, and its `STATUS.md` diff |
| `Code/pc/check_facts.py` | `check_links()` and `main()`, to find out what it actually validates |

**Photographs opened individually: 61 new** (31 Jacob, 30 Nuh) **plus 2 existing** re-opened for the
identity cross-check (`2026-08-01_nuh_soldering.jpg`, `2026-08-26_bench_full_rig.jpg`). Fourteen
full-resolution crops were made to settle specific questions.

---

## 2. Outputs, and the command that reproduces each

| Output | How to reproduce |
|---|---|
| **`Images/ours/`** — 61 new frames filed under the `YYYY-MM-DD_short_description.jpg` convention; both staging directories removed. **92 photographs now, all listed** | the rename map is `deliverables/2026-09-19-pause/_handoffs/` narrative below; the files are committed |
| **`Images/ours/README.md`** — new "Who is who" section; five new batch tables in the existing style, every row carrying its `IMG_` number and `SAID`/`READ` mark; two previously unlisted files added; the `2026-08-26` person caption upgraded to `SAID` | hand-edited |
| **`deliverables/2026-09-19-pause/photos/IMAGE_INVENTORY.md`** — all 92 photographs: file, IMG number, capture time, what it shows, `SAID`/`READ`, and manual / report / poster suitability | hand-written |
| **`deliverables/2026-09-19-pause/photos/MECHANICAL_OBSERVATIONS.md`** — for Subagent 2 | hand-written |
| **`deliverables/2026-09-19-pause/photos/prepared/`** — 15 cropped, annotated, captioned images + `MANIFEST.md` | `python3 deliverables/2026-09-19-pause/photos/prepare_photos.py` |

**`python3 Code/pc/check_facts.py` exits 0.**

---

## 3. Evidence — findings, with the frame each rests on

### 3.1 The two 2026-09-18 readings, checked against the actual images

**This was the task's first question and both now have an answer.**

| The 2026-09-18 23:13 session wrote | Verdict against the frames |
|---|---|
| *"the gold window is not all gold, bare copper tape exposed to its left"* | **CONFIRMED.** `2026-09-18_sample_plate_gold_window_1.jpg` (`IMG_8619`) at full resolution: a bright, smooth, flat gold patch covers roughly the center and center-right of the opening; the rest is a distinctly pinker, crinkled copper foil, exposed **to the gold's left and below it**. The two materials are unambiguously different in hue at full resolution. Prepared as `prepared/01_sample_plate_gold_window.jpg` |
| *"the suspended platform may be resting on the damping stack on top of the tower … no daylight visible between them"* | **NOT SUPPORTED.** `2026-09-18_platform_and_damping_stack_2.jpg` (`IMG_8624`) at full resolution shows **three** layers, not two: the black platform, **a separate bright disc fixed under it**, and **a ring of flat dark cylinders standing on the tower**. Background light **is** visible between the disc and the cylinder tops in places. Prepared as `prepared/02_platform_damping_gap.jpg` |

**Jacob's correction stands and the frames agree with it** (*"its not sitting on the tower is just
about its a perfect fit"*). **No gap has been measured from any frame and none should be** — the
camera is a hand-held phone a few degrees off the plane, which is the same geometry that makes `d`
unmeasurable.

### 3.2 A third earlier misreading, also now settled

`docs/INVENTORY.md` records a session counting **four** coin tubes in some frames and **three** in
others, corrected by Jacob to *"18 quaters x 3"*. **Every frame in which the platform is fully
visible shows three** — `IMG_8621`, `IMG_8626`, `IMG_8630`, `IMG_8647`, `IMG_4905`. The four-tube
count is not reproducible.

The "tubes look empty" reading is also explained rather than contradicted: the wrappers **are**
hollow at the top, which is exactly what 18 quarters (about 32 mm of stack) at the bottom of a
`$10.00 QUARTERS` wrapper looks like from above. **No frame shows the inside of a wrapper well
enough to count coins and none should be used to.**

### 3.3 What the new photographs add that the repository did not have

| Finding | Frame | Mark |
|---|---|---|
| **The sample plate is held on by two doubled, twisted rubber bands hooked over screw heads.** `STATUS.md` already names "the plate on its bands and balls" as an untested cause of gap drift; there was no photograph of it | `IMG_8653`, `IMG_8651`, `IMG_8650`, `IMG_4918` | `READ` |
| **The teardown is documented.** `STATUS.md` says "What was taken apart and how it was packed is UNKNOWN". Nuh's 10:05–10:16 frames show jumper leads unplugged, supply leads pulled, boxes opened, and **the suspended platform lifted off the frame with head, motor and preamp still on it** | `IMG_4908`–`IMG_4919` | `READ` |
| **The coarse-approach motor's own label, legible: `STEP MOTOR 28BYJ-48 5V DC`.** First photographic confirmation on our hardware; agrees with `docs/BOM.md` and `docs/WIRING.md` | `IMG_4917` | `READ` |
| **Both bench supplies, models legible: `JESVERTY SPS-3010 0–30 V 0–10 A` and `LONGWEI LW-K3010D 30 V/10 A`.** `docs/INVENTORY.md` had "bench PSU" with no model | `IMG_4899`, `IMG_4901` | `READ` |
| **The multimeter, model legible: `FNIRSI DST-201`.** `docs/INVENTORY.md` had "multimeter" with no model. **This one has teeth** — `STATUS.md` safety rule 12 turns on what the meter's top resistance range actually is, and until now nobody could look it up | `IMG_8641` | `READ` |
| **The preamplifier as built on 2026-09-06**, silkscreen legible (`JP1 R1 C1 C2 C3 IC1`, the same designators as `docs/WIRING.md` §10), with an axial leaded part mounted in the air on bent leads. **This is the OLD board, before the 2026-09-15 rebuild** | `IMG_4851`, `IMG_4852` | `READ` |
| **The tip-etching setup, in use** — a capability the repository had no record of. Now `SAID` by Jacob and already in `docs/INVENTORY.md` by the lead | `IMG_4713`, `IMG_4714` | `SAID` |
| **The room**: a wooden bench on a concrete floor in a basement utility room, a few meters from a breaker panel and a standby-generator transfer switch | `IMG_8631`, `IMG_4919` | `READ` |
| **The preamp box open**, showing a small green board and a bright metal post standing on it | `IMG_4906`, `IMG_4907` | `READ` |
| **The alligator clips Jacob bought on 2026-09-16, never itemized**: a retail card reading "…gator Clips", "NON-IN[SULATED]", "4" | `IMG_8642` | `READ` |
| **99% IPA is Signature Care 473 mL; the water is CVS Health DISTILLED, 1 US gallon.** `docs/INVENTORY.md` says "deionised / distilled"; the label says distilled | `IMG_8645`, `IMG_8646` | `READ` |

### 3.4 The identity cross-check, and the caveat you asked for

**Jacob's rule** (`SAID` 2026-09-19): *"white guy is jacob brown guy with beared is nuh"*.

**Cross-check against the one prior identification: they AGREE.** The bearded person in the new
frames is visibly the same person as in `2026-08-01_nuh_soldering.jpg` — same full dark beard, same
white-and-maroon jersey — which Jacob identified as Nuh on 2026-09-18. **No disagreement to report.**

> **The caveat, stated loudly because it is the one place I exercised judgment.** Jacob gave two
> discriminators. **In these frames the beard is unambiguous and the skin tone is not** — the
> clean-shaven person is olive/tan rather than obviously "white". **I used the beard.** A second,
> independent check agrees: the clean-shaven person wears a UC San Diego Tritons sweatshirt
> (`IMG_8633`, `IMG_4898`) on the day Jacob said he was leaving for college in San Diego. **Two
> independent checks agree, so I am confident — but if the reading is wrong, every caption marked
> `SAID 2026-09-19 (by Jacob's rule)` changes together**, in `Images/ours/README.md`,
> `IMAGE_INVENTORY.md` and prepared images 11, 13 and 14.

**This also corrected an error I nearly made.** On first pass I read the person holding the module
in `IMG_4919` as Nuh, from skin tone in a single frame. A face-level comparison against `IMG_8633`
shows it is the **same clean-shaven person**, i.e. Jacob. The frame came from Nuh's camera, which
is exactly the trap the addendum warned about.

**Not settled, and left UNKNOWN everywhere:** whose hands appear in any close-up (several teardown
frames are hands only), who took any photograph, and who performed any step shown.

### 3.5 Frames with faces, and what is permitted

Jacob has confirmed a team photograph **may** go on the poster. **That covers the poster.** Anything
else is his call, not ours. The frames containing a recognizable face are:

`IMG_8633`, `IMG_8634`, `IMG_8635`, `IMG_8636`, `IMG_8637`, `IMG_8638`, `IMG_8639`, `IMG_8640`
(Jacob's batch, filed as `2026-09-19_team_at_bench_*`, `_bench_selfie_*`, `_team_selfie_*`), and
`IMG_4657`, `IMG_4713`, `IMG_4714`, `IMG_4898`, `IMG_4919` (Nuh's batch). `IMG_8631` and several
teardown frames contain a hand or arm but no face. Two existing frames also contain a person:
`2026-08-01_nuh_soldering.jpg` (back of head) and `2026-08-26_bench_full_rig.jpg` (face).

**Two are prepared for the poster: `13_poster_module_portrait.jpg` (`IMG_4919`) and
`14_poster_team_at_bench.jpg` (`IMG_8633`).**

---

## 4. Best frames for the poster

In order, with the reason.

1. **`prepared/13_poster_module_portrait.jpg`** (`IMG_4919`) — **the single best frame in the whole
   set.** Jacob holding the complete scanning module, well lit, the instrument legible, a real
   workshop behind. Taken minutes after it came off the frame.
2. **`prepared/04_instrument_full_height.jpg`** (`IMG_8647`) — the best overview of the assembled
   instrument, four parts named. **The one to put beside any result.**
3. **`prepared/14_poster_team_at_bench.jpg`** (`IMG_8633`) — both of them, instrument behind.
4. **`prepared/05_scan_module_in_hand.jpg`** (`IMG_4918`) — the module as an object, hero-lit,
   copper against black.
5. **`prepared/01_sample_plate_gold_window.jpg`** (`IMG_8619`) — the sample at the scale a reader
   can see, and the one image that carries a real technical point.
6. **`prepared/11_tip_etching_setup.jpg`** (`IMG_4713`) — the process shot: gloves, glassware, a
   supply, outdoors.

---

## 5. Uncertainties, what is left undone, and one thing to fix

### 5.1 `check_facts.py` does NOT validate image references

**The task brief says the checker "checks for broken file references, so if you rename files, fix
every reference to them." It does not check image references.** `check_links()` (line 127) matches
only backtick-quoted paths beginning `docs|sessions|Code|CAD|PCB|gerbers` and ending
`.md|.py|.hpp|.cpp|.json|.txt`. **`Images/` is not in that list and `.jpg` is not in that list.**

I confirmed it by re-introducing the fault deliberately, per `CLAUDE.md` §7 rule 2: a
`Images/ours/<does-not-exist>.jpg` reference added to my own file **did not turn the checker red**.

**So I verified the 61 renames by a separate scan of every tracked `.md`, `.html`, `.py` and `.txt`
file in the repository for `Images/ours/*.jpg` references and for backticked `YYYY-MM-DD_*.jpg`
names. Result: no broken image references.** But this is a real gap and the next rename will not be
caught. **`check_links()`'s regex needs `Images` added to the directory alternation and `jpg|png|
svg` to the extension alternation.** That file is `Code/pc/check_facts.py`, which is not mine to
edit — flagging it for the lead.

### 5.2 Things I deliberately did NOT do

- **No attempt at `d`.** `Images/ours/README.md` records why, and the same geometry defeats the
  platform-gap measurement in §3.1.
- **No connection read off `IMG_4838`** (the Teensy carrier wiring side) or `IMG_4904`, and the
  prepared caption says so on the image.
- **No value read off the preamp resistor's color bands**, and no capacitor polarity read off
  `IMG_4851`, although the parts are visible. **`STATUS.md` fault 1d (how JLCPCB's C1/C2 polarity
  question was answered) is exactly the kind of thing a photograph looks like it could settle and
  cannot** — the relevant board is the old one, it has been reworked since, and a molded marking
  under warm light at an angle is not a polarity determination. **It is a lead for someone with the
  board in hand, not an answer.**
- **No supply topology read off `IMG_4899`/`IMG_4900`**, though a perfboard and a copper-tape splice
  bridging the two supplies are plainly visible. `docs/WIRING.md` §7 requires ±18 V; how these two
  are joined is not something to take off a photograph.
- **No electrolyte, voltage or electrode read off the etching frames.** The bottle's label is
  legible and I recorded that a bottle so labeled is in the frame; **that is an object, not a
  statement about the cell.** Jacob's own words are what the caption rests on.

### 5.3 Left undone

- **Five video clips could not be fetched** (all over the 10 MB Drive cap): `IMG_8632.MOV`,
  `IMG_8654.MOV`, `IMG_4615.MOV`, `IMG_4896.MOV`, `IMG_7846.MOV`. **`IMG_8632.MOV` is the one worth
  asking for** — it falls in the 09:35:33–09:38:09 gap in Jacob's sequence, the last window in which
  the assembled instrument was filmed.
- **`docs/INVENTORY.md` rows that these photographs could now support** — the two supply models, the
  meter model, the clip count, the distilled-water label, the IPA size. **`docs/` is not mine to
  write to.** They are listed in §3.3 for the lead.
- **A second pass for the manual** (Subagent 4) has not happened; the manifest marks which prepared
  images suit it.

---

## 6. Questions for Jacob and Nuh — one word settles each

**Numbered so they can be put directly.**

1. **The etcher — was it ever used successfully, and has any tip actually fitted to the instrument
   come off it, or have they all been cut?** *(This is the one that decides whether the etcher
   matters. Every tip in `docs/INVENTORY.md` is described as cut and blunt, and tip bluntness is a
   live blocker.)*
2. **Did the etching setup survive the move, and where is it now?**
3. **In `2026-08-01_frame_parts_at_home.jpg` (`IMG_4657`) there are six flat rectangular metal bars
   lying on the frame base. What are they?** *(Candidate: the eddy-damping magnets, whose number and
   type `docs/INVENTORY.md` records as UNKNOWN. I have NOT written that anywhere — it is a guess and
   I am asking instead.)*
4. **Inside the open preamp box in `2026-09-19_scan_head_rear_1.jpg` (`IMG_4906`) there is a bright
   metal post standing on the small green board. Is that the Keystone turret standoff?**
5. **The multimeter is an `FNIRSI DST-201` (read off the bezel in `IMG_8641`). Is that the meter
   used for the continuity and resistance checks?** *(It changes what "OL" means, which is
   `STATUS.md` safety rule 12.)*
6. **The two bench supplies are a `JESVERTY SPS-3010` and a `LONGWEI LW-K3010D`. Are those the two
   that feed the controller's ±18 V, and is the little perfboard on top of them the series
   junction?**
7. **The alligator clips bought on 2026-09-16 — is it 4, non-insulated?** *(Read off the retail card
   in `IMG_8642`.)*
8. **The water is CVS Health DISTILLED water, not deionized. Is distilled what you want for the
   input-node rinse, or was DI intended?**
9. **Is `2026-09-17_sample_plate_rebuilt.jpg` the plate the inventory calls "rebuilt 2026-09-17"?**
   *(Open since 2026-09-18; still unanswered.)*
10. **Which of the two of you is in `2026-08-26_bench_full_rig.jpg`?** *(I have written **Nuh**, by
    your rule and by the match to `2026-08-01_nuh_soldering.jpg`. Confirm and it becomes settled.)*
11. **Do you confirm the person identifications generally?** *(I used the beard, not skin tone,
    because the beard is unambiguous in these frames and the skin tone is not. If that reading is
    wrong, several captions change together.)*
12. **Beyond the poster, may frames containing faces be used in the report or the manual?** *(You
    have said yes to a team photograph on the poster. The frames with faces are listed in §3.5.)*
13. **Can `IMG_8632.MOV` be trimmed or screenshotted and re-shared?** *(It sits between the frames
    timed 09:35:33 and 09:38:09 on the last morning — the last footage of the instrument assembled.
    A 10-second trim or a single screenshot is enough.)*
14. **How was it packed, and what came apart?** *(The photographs show the teardown up to 10:16:
    leads off, boxes open, platform lifted off the frame. **No frame shows anything going into a
    box**, so `STATUS.md`'s "how it was packed is UNKNOWN" still stands. In particular: were the
    three springs taken off and kept, and did the sample plate stay on its rubber bands?)*
15. **When it is rebuilt, do the rubber bands go back?** *(Not a photograph question, but it is the
    softest joint in the load path and `docs/NEXT_SESSION_PLAN.md` already asks for a stiffer
    sample-plate mounting. Worth deciding before reassembly rather than after.)*
