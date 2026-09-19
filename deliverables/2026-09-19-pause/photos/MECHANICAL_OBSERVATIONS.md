# What the photographs show about mechanical stability

**Written 2026-09-19 for Subagent 2 (candidate images and the motion hypothesis), from a
frame-by-frame review of all 92 photographs of our hardware.**

---

## Read this first — what this file can and cannot do

**A photograph can SUGGEST an explanation for instability. It CANNOT prove the cause of a recorded
signal.**

Every observation below is a **static** picture of the instrument. It shows what is touching what,
what is held by what, and what is loose. **It shows nothing about motion**, because none of these
frames is a time series, none carries a scale bar, and none was taken while a scan was running.

- A soft mounting **may** move. It also may not.
- A stiff-looking mounting **may** still move, by creep, by thermal expansion, or by something out
  of frame.
- **Nothing here dates a mechanism to a particular run.** The gap motion measured on the morning of
  2026-09-19 — ≥ 43,000 Z counts in 6.4 s, ≥ 56,000 over about two minutes, with the motor and
  hands still (`STATUS.md`) — happened before any of the 09:35–10:16 frames were taken, on an
  instrument that had by then been handled.

**So: use this as a list of candidates to test, not as evidence for any of them.** `STATUS.md`
already names four untested candidates for the gap moving — the leaf on its paper, the plate on its
bands and balls, thermal motion, and air currents. **The photographs add detail to the second and
add three more candidates. They settle none of them.**

The one thing photographs are good for is **ruling a thing IN as physically present**. "The sample
plate is held on by rubber bands" is a fact about the build; "the rubber bands caused the drift" is
not, and is not claimed anywhere below.

---

## 1. The sample plate is retained by two twisted rubber bands

**The clearest new observation in the whole set, and the repository had no photograph of it.**

`Images/ours/2026-09-19_scan_head_close_bands_3.jpg` (`IMG_8653`),
`_2.jpg` (`IMG_8651`), `_1.jpg` (`IMG_8650`), and from the other side
`2026-09-19_platform_lifted_off_2.jpg` (`IMG_4918`).

**What is visible.** Two elastic bands, each **doubled over and twisted along its length**, run
horizontally across the aluminium-taped plate — one near the top, one near the bottom — and each is
hooked over a **black pan-head screw on the left and another on the right**. The plate is pulled
back against the head by band tension and nothing else. Three threaded ball-end screw shanks stand
between the plate and the head body.

**Why it matters, and the honest limit.** `STATUS.md` already lists *"the plate on its bands and
balls"* as one of four untested causes of the gap drifting, and `docs/INVENTORY.md` records
Jacob's *"the plate sits on all three ball-ended screws"* (`SAID`, 2026-09-19 morning). **What the
photographs add is what the preload actually is: twisted rubber.** That is a soft, frictional,
creep-prone joint by construction.

**What CANNOT be taken from these frames:**

- **Any band tension, in newtons or otherwise.** Twist count is not a force.
- **Whether the bands are new or old.** Rubber creeps and relaxes with age, temperature and
  sustained strain, and none of that is visible.
- **Whether the plate slid, rocked or crept during any run.** No frame shows the plate at two times.
- **Whether the contact at the three balls is three-point or partial.** The frames are too oblique.

**The test that would settle it is at the bench, not in an image**: load the plate, record a long
stillness run, then re-seat it and repeat. `docs/NEXT_SESSION_PLAN.md` already calls for a stiffer
sample-plate mounting.

---

## 2. Cables run from the suspended platform to the fixed bench, and they are not dressed

`2026-09-18_instrument_on_suspension_2.jpg` (`IMG_8622`),
`2026-09-19_platform_and_springs.jpg` (`IMG_4905`),
`2026-09-19_instrument_full_height.jpg` (`IMG_8647`),
`2026-09-19_teardown_bench_overview.jpg` (`IMG_4913`).

**What is visible.** An **orange wire** leaves the head, crosses the platform, drops over the
platform edge and runs across the bench to the electronics. A **bundle of white, blue, teal and
purple leads** leaves the platform on the other side and does the same. In `IMG_4905` and
`IMG_8647` these cables hang in free loops; **in no frame is any of them clamped, taped or tied to
a strain-relief point on the platform or on the frame.**

**Why this is worth testing.** A suspended stage is only as soft as its softest path to ground, and
**a cable is a path to ground.** An undressed cable adds stiffness in parallel with the springs,
and worse, it adds a path that is nonlinear — it can stick to the bench and release. A very soft
suspension is exactly where a stiff cable matters most.

**What CANNOT be taken from the frames.** How stiff those cables are. How much of the platform's
restoring force they carry. Whether they touched anything during a run. **All three would need a
measurement** — the simplest being: hang the platform, add a known small mass, measure the droop
with the cables connected and again with them lifted clear.

---

## 3. The coin mass stands tall and loose on the platform

`2026-09-18_scan_head_top_down_2.jpg` (`IMG_8626`),
`2026-09-19_instrument_full_height.jpg` (`IMG_8647`),
`2026-09-19_platform_and_springs.jpg` (`IMG_4905`).

**What is visible.** **Three** paper coin wrappers stand upright on the platform, one labelled
`$10.00 QUARTERS · N.F. STRING & SON, INC. · HARRISBURG, PA.`. They stand **on** the platform and
the copper base plate; **no frame shows any of them taped, clipped or restrained.** Separately, two
or three small black printed cups sit at the platform rim, each with a US coin visible in it.

**This CONFIRMS the corrected count and clears an earlier misreading.** `docs/INVENTORY.md`
records that a session counted four tubes in some frames and three in others, and that Jacob
corrected it: *"18 quaters x 3 and then 10 nickels"* (`SAID` 2026-09-19). **Every frame in which
the platform is fully visible shows three wrappers.** The earlier four-tube count is not
reproducible in these images.

**It also explains the "empty tubes" misreading.** The wrappers are **hollow at the top** in the
top-down frames, which is exactly what 18 quarters (roughly 32 mm of stack) sitting at the bottom
of a wrapper several times that long looks like from above. **The frames do not contradict Jacob;
they are consistent with him.** No frame shows the inside of a wrapper well enough to count coins,
and none should be used to.

**Why it is a candidate.** Mass standing tall and unrestrained on a suspended stage raises the
centre of gravity, which invites a low-frequency **rocking** mode — the opposite of what the mass
was added for — and a tube that can tip or slide is a stick-slip source. **`docs/INVENTORY.md`
already raises both points in writing.** The photographs confirm the geometry that the concern was
about; they do not show any tube moving.

---

## 4. The gap under the platform: the photographs do NOT support "resting on the tower"

`2026-09-18_platform_and_damping_stack_2.jpg` (`IMG_8624`) and `_1.jpg` (`IMG_8623`).
Prepared and annotated as `prepared/02_platform_damping_gap.jpg`.

**Background.** The 2026-09-18 23:13 session (commit `6b41855`) read these same frames and wrote
into `STATUS.md`, as CHECK ZERO, that *"the suspended platform appears to be resting on the damping
stack on top of the black tower — there is a bright band right under the platform's edge and no
daylight visible between them."* **It was flagged as a reading and nothing was written as fact,
which is the rule working.** Jacob corrected it within the hour: *"its not sitting on the tower is
just about its a perfect fit"* (`SAID`, in `docs/INVENTORY.md`).

**What a full-resolution look at the same frames shows.** Three distinct layers, not two:

1. the black suspended platform;
2. **a separate bright disc fixed under it** — thick, with a machined or extruded edge, `READ` as
   the aluminium eddy-damping plate;
3. **a ring of flat dark cylinders standing on the tower top**, `READ` as the damping magnets.

**Background light IS visible between layers 2 and 3 in places**, and is not visible in others.
That is what a nearly-edge-on view of a small gap looks like when the near rim projects over the
far one.

**Conclusion, stated carefully.** The frames are **consistent with Jacob's correction** and they
**do not support** the original reading of no daylight. **They do not measure the gap and no gap
figure may be taken from them** — the camera is a hand-held phone a few degrees off the plane, and
`Images/ours/README.md` already records in detail why small out-of-plane distances cannot be read
off frames like these.

**The live suspect that survives.** A small clearance can still be crossed **intermittently** —
a platform that touches on a bump and lifts off again is a chattering, nonlinear bypass, which
`docs/INVENTORY.md` notes would look exactly like a stage that is not under control. **No
photograph can rule that in or out.** The paper-slip test in `STATUS.md` can, in ten seconds.

---

## 5. What holds the platform up, described exactly

`2026-09-19_instrument_assembled_front.jpg` (`IMG_8630`),
`2026-09-19_instrument_full_height.jpg` (`IMG_8647`),
`2026-09-19_platform_and_springs.jpg` (`IMG_4905`).

**Two different kinds of vertical member run between the top plate and the base, and they are easy
to confuse at a glance:**

- **Threaded columns**, thicker, with a visible helical thread and **hex nuts** where they pass
  through the top plate, and **printed knobs standing above the top plate**. These are structure,
  and `docs/INVENTORY.md` records Jacob using printed height adjusters at the top to raise the
  platform — *"it is already at max height"*.
- **Fine smooth wires** hanging from the top plate down to **steel eyebolts screwed into the
  platform**, ending in a hook. These are the springs. `docs/INVENTORY.md` has them from an order
  record: **three fitted**, FOCMKEAS 304 stainless, wire Ø0.50 mm, OD Ø3.00 mm, free length 300 mm.
  At the image scale a 3 mm spring is a few pixels wide and its coils do not resolve, which is
  precisely why the two are confusable.

**In `IMG_4905` and `IMG_4910` the eyebolt-and-hook joint is unambiguous**, and in
`IMG_4916`/`IMG_4918`, after the teardown, **an eyebolt is visible empty** with the spring gone.

**A candidate worth one look at the bench:** a spring hooked through an eyebolt is a **metal-on-
metal sliding contact under load**, free to creep round the eye and to stick and release. Three of
them in parallel is three such joints. **Nothing in any frame shows one moving**, and this is a
suggestion for the list, not a finding.

---

## 6. The room: a wooden bench on a concrete floor, beside an electrical panel

`2026-09-19_workshop_room.jpg` (`IMG_8631`), `2026-09-19_scan_module_held_portrait.jpg`
(`IMG_4919`), and in the background of most 2026-09-19 frames.

**What is visible.** A basement utility room. **Concrete floor. A wooden workbench**, on which the
instrument's base stands directly. A few metres away on the wall: a **breaker panel** and a
**standby-generator automatic transfer switch**. Ducting, shelving, packing boxes.

**Why it is here.** It is context for two open questions and evidence for neither.

- **Vibration.** A wooden bench top on a concrete slab is a structure with its own modes, and the
  instrument's frame stands on it with no isolation between the two. **The stamp test in
  `STATUS.md` is the measurement that decides whether the building is getting in at all** — and the
  result of that test, whichever way it goes, is worth more than any reading of this photograph.
- **Mains.** A panel and a transfer switch nearby are a plausible 50/60 Hz radiator. **The
  measurement already exists and is better than the photograph**: 60 Hz line content was 10 counts
  on 2026-09-19, down from 87 (`STATUS.md`). Nothing in this frame changes that number.

**No distance, no coupling and no field strength may be taken from this image.**

---

## 7. What the photographs rule OUT, or fail to support

Recording the negatives, because this project's false trails have been as valuable as its results.

| Suggestion | What the frames actually show |
|---|---|
| "The platform is resting on the tower with no daylight" (2026-09-18 reading) | **Not supported.** Three distinct layers and visible background light between two of them in places. §4 |
| "The coin tubes are empty" (2026-09-18 reading) | **Not supported and already corrected by Jacob.** The tubes read hollow at the top, which is what 18 quarters in a long wrapper looks like from above. §3 |
| "There are four coin tubes" (earlier count) | **Not reproducible.** Every frame with the platform fully in view shows **three**. §3 |
| Something resting on or leaning against the suspended platform | **Nothing visible.** In every assembled frame the only things touching the platform are the springs at their eyebolts, the head assembly bolted to it, the coin cups and wrappers standing on it, and the cables in §2. **Absence in a photograph is weak evidence**, and a contact at the underside would be hidden. |
| The enclosure was on the instrument during the last runs | **Cannot be told.** `IMG_8648` and `IMG_4898` show the enclosure **off** and in hand on the morning of 2026-09-19; no frame shows whether it was on during any particular run. |

---

## 8. For Subagent 2, in one paragraph

**Nothing in these photographs can date a mechanism to a run, and nothing in them can rescue or
condemn an image.** What they do give is a **precise physical description of the three softest
joints in the load path** — a sample plate held by twisted rubber bands against three ball screws
(§1), undressed cables bridging the suspended stage to the fixed bench (§2), and unrestrained
mass standing tall on the platform (§3) — plus a fourth, the spring-hook-in-eyebolt joints (§5).
**If your analysis finds a signature that wants a mechanical explanation, those four are the
physically present candidates and they are worth naming.** If it does not, none of this is
evidence of anything. **The instrument is now disassembled**, so every one of these is a question
for reassembly, and each will have to be re-checked then rather than assumed to have survived the
move unchanged.
