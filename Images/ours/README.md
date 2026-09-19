# `Images/ours/` — photographs of this instrument

**Everything in this folder is our own hardware.** The other folder, `Images/`, contains Mech
Panda's HOPG scans and is not ours — see [`../README.md`](../README.md) before using anything from
there.

---

## The build record, 2026-07-25 to 2026-09-17

**Added 2026-09-18** from Jacob's phone, via a Drive folder he shared. Twenty-four frames, resized
to 1600 px on the long edge and **stripped of EXIF** — the originals carried the camera's metadata
and the repository gets shown to other people. **Full-resolution originals stay in Jacob's Drive**;
these are the working copies.

### How to read the "Confirmed by" column

**This project has a rule about photographs**, in `CLAUDE.md`: *a photograph is not a measurement
of our hardware — ask whose board it is before reading anything off it.* It exists because on
2026-09-09 a session read a part marking off a shared photo and edited five documents before
anyone asked whose board it was. It was Dan Berard's.

These are all our own bench, so *whose* is settled. **What is not settled is what each one shows**
— that is a reading of an image, and readings have been wrong here. So every caption is marked:

- **`SAID`** — Jacob or Nuh told us what it is, with the date.
- **`READ`** — a reading of the frame. **Plausible, not confirmed.** One word from Jacob or Nuh
  settles any of these, and the caption should then be changed to `SAID` with the date.

### Who is who — settled 2026-09-19

**`SAID`, Jacob, 2026-09-19:** *"white guy is jacob brown guy with beared is nuh"*.

| In a frame | Is |
|---|---|
| The lighter-skinned person, no beard, dark curly hair | **Jacob Katz** |
| The darker-skinned person with a full beard | **Nuh Shaheer** |

**This is only the second person identification the project has ever had.** The first is
`2026-08-01_nuh_soldering.jpg`, `SAID` by Jacob on 2026-09-18, and the two agree: the bearded
person in the new frames is the same person, in the same jersey.

> **The discriminator actually used was the beard.** Jacob gave two — skin tone and a beard — and in
> these frames the beard is unambiguous where the skin tone is not. A second, independent check
> agrees: the clean-shaven person wears a UC San Diego sweatshirt on the day Jacob said he was
> leaving for college in San Diego. **If either reading is wrong, every caption marked
> `SAID 2026-09-19 (by Jacob's rule)` changes together.**

**What this does NOT settle**, and these stay UNKNOWN: **whose hands** appear in a close-up, **who
took** any photograph, and **who performed** any step shown.

**Publication:** Jacob confirmed 2026-09-19 that **a team photograph may appear on the poster**.
Permission to publish and identification are two different things; both are now given.

**Nothing in this folder has had a number taken off it**, and the section below this one records
in detail why one particular attempt to do so failed.

| File | What it shows | Confirmed by |
|---|---|---|
| `2026-07-25_controller_pcb_as_delivered.jpg` | The controller PCB, held, as it arrived. Four DAC packages, the ADC, the two DSUB footprints along the top edge and the 26-way ribbon header at the left. **It arrived populated** — JLCPCB PCBA, not hand-built (`docs/INVENTORY.md`) | `READ` |
| `2026-07-25_second_board_as_delivered.jpg` | The second board from the same delivery, held up to the camera | `READ` — **which board this is has not been confirmed.** It is smaller than the controller and was photographed the same minute |
| `2026-07-26_frame_and_suspension_assembled.jpg` | The printed frame standing on the bench with the three suspension posts up, parts still bagged around it | `READ` |
| `2026-08-01_printed_platform_and_mount.jpg` | The printed circular platform and the scan-head mount plate, loose on the bench, with the hole grids visible | `READ` |
| `2026-08-01_nuh_soldering.jpg` | **Nuh**, soldering at the bench | `SAID` 2026-09-18 |
| `2026-08-02_frame_assembled.jpg` | The frame with the platform hung on its three suspension rods | `READ` |
| `2026-08-07_uln2003_stepper_driver.jpg` | The ULN2003 driver board for the 28BYJ-48 coarse-approach stepper, held in hand. IN1-IN7 labels legible | `READ` |
| `2026-08-07_first_electronics_hookup.jpg` | **The first full electronics hookup.** Controller board, 26-way ribbon, stepper and its driver, all wired together on the bench | `SAID` 2026-09-18 |
| `2026-08-07_teensy_carrier_protoboard.jpg` | The Teensy 4.1 on its protoboard carrier with the ribbon attached | `READ` |
| `2026-08-19_preamp_board.jpg` | The OPA627 transimpedance preamp board, held against an anti-static bag | `READ` |
| `2026-08-21_preamp_with_coax.jpg` | The preamp with its coax tail attached, on a bench mat | `READ` |
| `2026-08-24_scanhead_on_copper_ground_plane.jpg` | The scan head assembled on the copper-covered base plate, on the suspended platform, orange coax running off | `READ` |
| `2026-08-26_bench_full_rig.jpg` | The whole bench: frame, suspension, supplies, laptop, and **Nuh** working. ~~which of the two people this is has not been confirmed~~ **SETTLED 2026-09-19** — same beard and same jersey as `2026-08-01_nuh_soldering.jpg`, which Jacob identified as Nuh | `SAID` 2026-09-19, by Jacob's rule — see "Who is who" below |
| `2026-08-29_rig_on_suspension.jpg` | The instrument on its suspension with both bench supplies live | `READ` |
| `2026-08-30_ribbon_wiring_diagram_in_use.jpg` | **A screen showing this repository's own 26-way ribbon wiring diagram**, being used at the bench. Title legible: *Teensy 4.1 <-> STM Controller — 26-way Ribbon Wiring* | `READ` |
| `2026-09-15_bench_before_powered_session.jpg` | The bench set up before the 2026-09-16 powered session: supplies, meter, the rig, tools laid out | `READ` |
| `2026-09-16_faraday_enclosure_on_suspension.jpg` | The copper-foil-wrapped enclosure over the scan head, hanging on the suspension, with the wiring loom coming out of it | `READ` |
| `2026-09-16_tip_protrusion_measurement_1.jpg` | **The tip-protrusion measurement**, tape measure against the head face. This is the provenance for the **1.8 cm** figure in `docs/INVENTORY.md`: measured from the plate face, halfway along the side-by-side screws | `SAID` 2026-09-18 |
| `2026-09-16_tip_protrusion_measurement_2.jpg` | The same measurement, closer, with the three ball ends and the tape in one frame | `SAID` 2026-09-18 |
| `2026-09-16_scan_module_top_down.jpg` | **Top-down view of the scanning module on the suspension. The preamp is the little copper box in the middle** | `SAID` 2026-09-18 |
| `2026-09-16_first_gold_attempt_removed.jpg` | **The first gold-leaf attempt, made on 2026-09-16 and then removed.** It was never reported at the time and only came to light on 2026-09-18 when Jacob identified this frame. See `docs/INVENTORY.md` | `SAID` 2026-09-18 |
| `2026-09-16_gold_leaf.jpg` | Loose gold leaf flakes on the bench surface, for scale | `READ` |
| `2026-09-17_sample_plate_rebuilt.jpg` | The sample plate off the head: aluminium tape over the face, a square window cut in it, gold leaf inside the window. **This looks like the plate `docs/INVENTORY.md` describes as "rebuilt 2026-09-17"** — that entry records its photo as being "in the conversation, not in the repository", and this is dated the same day | `READ` — **worth one word from Jacob**, because if it is that plate the inventory entry should point here |
| `2026-09-17_head_and_coax_on_suspension.jpg` | The head on the suspended platform with the orange coax looping down to the preamp | `READ` |
| `2026-09-16_controller_board.jpg` | The controller board. **Added to this table 2026-09-19** — the file was committed with the batch and was never listed here | `READ` |
| `2026-09-16_scanhead_on_platform.jpg` | The scan head on the suspended platform. **Added to this table 2026-09-19** — the file was committed with the batch and was never listed here | `READ` |

### What was deliberately left out

- **Two video clips** were the only ones small enough to fetch. One was 0.2 s of a laptop screen and
  one was a 2.4 s personal selfie with no hardware in it. **Neither is project content and neither
  was kept.**
- **The other twenty videos could not be fetched at all** — see "The videos" below.
- Duplicate frames of the same subject taken seconds apart: one of each was kept.

### The videos — NOT AVAILABLE, and this is a tooling limit, not a decision

Jacob's Drive folder holds **22 video clips, about 3.6 GB**, including what look like the whole of
the 2026-09-16 and 2026-09-17 bench sessions. **Twenty of them could not be retrieved.**

**The reason is a hard 10 MB cap on the Drive connector's download.** Files above it return
*"File too large for download, over limit of 10 MB"* and no partial read is offered. The other
routes were checked and are closed too:

| Route | Result |
|---|---|
| Connector download | **10 MB cap.** 20 of 22 clips are over it, the largest 1.19 GB |
| Anonymous fetch of the share link | **Closed.** The folder is shared to the `quis.com` domain, not to anyone with the link |
| A thumbnail or preview frame from the file metadata | **Not offered** by the connector |

**So the only clips in this repository's reach are the two that were under 10 MB, and neither was
useful.** To get the bench videos in, one of these has to happen at Jacob's end:

1. **Trim them on the phone** to the few seconds that matter and re-share — a 10 s clip at phone
   bitrate is comfortably under 10 MB.
2. **Export them at a lower resolution** (720p) before uploading.
3. **Screenshot the moment** out of the video on the phone and drop the image in the folder. A still
   is what would end up in a write-up anyway.

---
## 2026-09-18 — the rebuilt tip holder and the scan head face

Sent by Jacob from the bench, taken to settle **d**, the distance from the line through the two
side-by-side ball ends to the tip. **They are our own hardware** (`SAID`, Jacob, taken at his bench
the same evening).

| File | What it shows |
|---|---|
| `2026-09-18_scanhead_side.jpg` | Side view. The copper-taped preamp box above, the aluminium-taped head, the ball-end screws protruding, the copper-covered base plate |
| `2026-09-18_scanhead_face_1..4.jpg` | The head face straight on: the piezo disc recessed in its bore, the tip at the disc centre, the tip lead crossing the face, and three ball-end screws |

**Nothing has been read off these as a measurement.** `CLAUDE.md` is explicit that a photograph is
not a measurement of our hardware, after the 2026-09-09 session read a part marking off a shared
photo and edited five documents before asking whose board it was. Repeated by-eye estimates of d
from these frames spread over about ±1 mm, which is the same size as the quantity, so **no value
for d has been written into `docs/FACTS.md` or `docs/INVENTORY.md` from them.**

**Two things must be confirmed by Jacob before any number is taken from these:**

1. **Which two ball ends are the side-by-side pair.** Read from the frames as the TOP and BOTTOM
   ones, with the motor screw on the RIGHT — so the pivot line runs vertically in this view. If that
   is wrong, every distance taken from these photos is wrong.
2. **How far the tip protrudes from the face, against how far the ball ends stand proud.** The balls
   stand well clear of the face and the tip sits recessed inside the bore. The old tip stuck out
   **about 1.8 cm** (`docs/INVENTORY.md`); the tip in these frames looks far shorter, but it may
   simply be pointing at the camera. **If the tip now sits behind the plane of the three ball ends,
   the sample plate rests on the balls and can never reach it.**

### 2026-09-18: d CANNOT be measured from these photographs. Three attempts, three answers.

**Jacob confirmed the layout** (`SAID` 2026-09-18): the TOP and BOTTOM ball ends are the
side-by-side pair, so the pivot line runs vertically in these frames, and the motor screw is the
one on the RIGHT. That part is settled and is safe to rely on.

**Measuring d from the frames was then tried three times and failed three times:**

| Attempt | Method | Disc diameter it gave |
|---|---|---|
| 1 | By eye off a 50 px grid, cropped near the bore | ~425 px |
| 2 | By eye off a 100 px grid, whole face | ~210 px |
| 3 | Colour detection of the brass disc, `numpy` | 687 to 725 px, and inconsistent across the four frames |

**A factor of more than two between attempts.** The by-eye readings disagreed with each other, and
the automatic one caught the warm-lit aluminium foil along with the brass because the whole scene is
copper-toned. **No value for d has been taken from these photographs and none should be.**

**Four reasons it cannot work, recorded so nobody tries again:**

1. **The tip is not a point.** It is a substantial soldered structure inside the bore, clearly
   offset from the disc centre, and **which feature is the working tip cannot be told from the
   image.** Two candidates were marked and sent to Jacob as A and B; they sit on opposite sides of
   the disc centre and several millimetres apart.
2. **The scene has no colour contrast.** Brass disc, aluminium tape and copper tape under warm light
   all sit in the same hue band.
3. **The depth defeats the perspective.** The ball ends stand proud toward the camera and the tip is
   recessed in the bore. With about 15 mm between them, the camera must be square to **half a
   degree** for the apparent offset to stay under 0.13 mm. No hand-held photograph is that square.
4. **The threshold is 3 pixels.** Tunnelling needs d under about 0.13 mm, and the scale here is
   roughly 0.04 mm per pixel.

**What to ask instead, and it takes a minute at the bench:** which feature is the tip, and **how far
is it from the centre of the brass disc**, by ruler or caliper against the disc rim. Both are at the
same depth, so that measurement has none of the problems above, and the CAD already fixes the disc
centre at **1.000 mm** from the pivot line (`docs/FACTS.md`, piezo pocket offset, MESH). d then
follows.

---

# 2026-09-19 — SIXTY-ONE MORE PHOTOGRAPHS, FROM TWO CAMERAS

**Added 2026-09-19** during the pause-point work, from the same shared Drive folder. **Two
independent batches, from two different phones, by two different people**, and they are kept apart
below because that distinction matters when reading them.

| Batch | Frames | Camera | Drive owner | Span |
|---|---|---|---|---|
| **Jacob's** | 31, `IMG_8619`–`IMG_8653` | iPhone 17 Pro | `jacob@quis.com` | 2026-09-18 18:08 to 2026-09-19 09:41 |
| **Nuh's** | 30, `IMG_4657`–`IMG_4919` | iPhone 13 Pro Max | `nuh.bmshaheer@gmail.com` | 2026-08-01 to 2026-09-19 10:15 |

**Every frame below was opened and looked at individually**, at full resolution where a detail
mattered. All are EXIF-stripped (verified zero tags) and resized to 1600 px on the long edge, as
the earlier batches were. **The `IMG_` number is kept in every row so the Drive original can always
be found again.** Full-resolution originals stay in the Drive.

**Capture times are camera-local.** Neither camera wrote an offset tag, so the relation to the UTC
timestamps in the session logs is an inference, not a fact.

> **File ownership is not authorship and it is not identity.** Nuh uploading a frame makes him the
> likely photographer, not the likely subject.

**A fuller inventory, with suitability for the manual, report and poster, is at
[`../../deliverables/2026-09-19-pause/photos/IMAGE_INVENTORY.md`](../../deliverables/2026-09-19-pause/photos/IMAGE_INVENTORY.md).**

## Jacob's batch — 2026-09-18 evening, 8 frames

**These are the frames the 2026-09-18 23:13 session read** (commit `6b41855`) and wrote two
findings from. They were never committed until now. **Both readings have been checked against the
frames and the results are in the rows below.**

| File | IMG | Captured | What it shows | Confirmed by |
|---|---|---|---|---|
| `2026-09-18_sample_plate_gold_window_1.jpg` | `IMG_8619` | 18:08:45 | **The rebuilt sample plate, face up, off the head.** Aluminium tape over the face, a square window framed in black tape, and inside it crinkled copper-coloured foil with a **bright, smooth gold patch over roughly the centre and centre-right**. **Copper is exposed to the gold's left and below.** Orange bias wire entering at the top | `READ` — **confirms the 2026-09-18 session's reading that the window is not all gold** |
| `2026-09-18_sample_plate_gold_window_2.jpg` | `IMG_8620` | 18:08:45 | The same plate a fraction of a second later. Nothing differs | `READ` |
| `2026-09-18_instrument_on_suspension_1.jpg` | `IMG_8621` | 19:09:01 | The whole instrument three-quarter on: frame, springs, circular platform, copper base plate, scan head, **three paper coin wrappers standing on the platform**, printed cups at the rim | `READ` |
| `2026-09-18_instrument_on_suspension_2.jpg` | `IMG_8622` | 19:09:03 | Side-on. The orange wire loops from the platform down to the bench; other leads run off to the left | `READ` |
| `2026-09-18_platform_and_damping_stack_1.jpg` | `IMG_8623` | 19:09:05 | Side-on, lower — the platform underside and the tower below it | `READ` |
| `2026-09-18_platform_and_damping_stack_2.jpg` | `IMG_8624` | 19:09:07 | **The clearest view under the platform.** A bright disc is fixed under the black platform and a ring of dark cylinders stands on the tower below it. **At full resolution, background light IS visible between the two in places** | `READ` — **does NOT support the 2026-09-18 reading of "no daylight". Consistent with Jacob's correction: "its not sitting on the tower is just about its a perfect fit"** |
| `2026-09-18_scan_head_top_down_1.jpg` | `IMG_8625` | 19:09:12 | **Top-down of the scan head with the sample plate OFF**: copper base plate, head body, stepper and lead screw, the rubber bands, two coins face-up in printed cups | `READ` |
| `2026-09-18_scan_head_top_down_2.jpg` | `IMG_8626` | 19:09:13 | The same, wider, all three coin wrappers in frame. **Each is hollow at the top**, which is what 18 quarters at the bottom of a long wrapper looks like from above | `READ` |

## Jacob's batch — 2026-09-19 morning, 23 frames

**Never seen by any session.** Captured about 40 minutes before the "we are taking it apart"
message on a UTC−4 reading.

| File | IMG | Captured | What it shows | Confirmed by |
|---|---|---|---|---|
| `2026-09-19_instrument_assembled_front.jpg` | `IMG_8630` | 09:35:31 | **The instrument still fully assembled**: top plate on three threaded columns with printed knobs above, three fine springs to the platform, the head, three coin wrappers, the coin cups | `READ` |
| `2026-09-19_workshop_room.jpg` | `IMG_8631` | 09:35:33 | **The room.** A basement utility room: concrete floor, wooden bench with the instrument and laptop, a wall breaker panel and a standby-generator transfer switch a few metres off, packing boxes | `READ` |
| `2026-09-19_team_at_bench_1.jpg` | `IMG_8633` | 09:38:09 | **Both of them at the bench, the instrument behind.** **Nuh** at the left, **Jacob** at the right | `SAID` 2026-09-19, by Jacob's rule |
| `2026-09-19_team_at_bench_2.jpg` | `IMG_8634` | 09:38:19 | The same, second pose | `SAID` 2026-09-19, by Jacob's rule |
| `2026-09-19_bench_selfie_1.jpg` | `IMG_8635` | 09:38:50 | **Jacob**, selfie, instrument behind | `SAID` 2026-09-19, by Jacob's rule |
| `2026-09-19_bench_selfie_2.jpg` | `IMG_8636` | 09:38:51 | The same | `SAID` 2026-09-19, by Jacob's rule |
| `2026-09-19_bench_selfie_3.jpg` | `IMG_8637` | 09:38:53 | **Jacob** pointing at the instrument; the instrument is sharp in this one | `SAID` 2026-09-19, by Jacob's rule |
| `2026-09-19_team_selfie_1.jpg` | `IMG_8638` | 09:38:55 | Both of them, selfie | `SAID` 2026-09-19, by Jacob's rule |
| `2026-09-19_team_selfie_2.jpg` | `IMG_8639` | 09:38:56 | The same, second frame | `SAID` 2026-09-19, by Jacob's rule |
| `2026-09-19_team_selfie_with_laptop.jpg` | `IMG_8640` | 09:40:37 | Both of them with the laptop, a session on screen | `SAID` 2026-09-19, by Jacob's rule |
| `2026-09-19_multimeter_and_bench.jpg` | `IMG_8641` | 09:40:50 | **The meter, model legible: `FNIRSI DST-201`.** Also the controller box with its two DB9s, the tower, and loose bare alligator-clip jaws and two loose springs on the bench | `READ` — **the model was not recorded anywhere before** |
| `2026-09-19_consumables_clips_and_cutters.jpg` | `IMG_8642` | 09:40:52 | Consumables. A retail card reading **"…gator Clips", "NON-IN[SULATED]", "4"**, with bare clip jaws loose beside it; a probe; flush cutters; rubber bands | `READ` — **the clips Jacob bought on 2026-09-16 were never itemised; this reads as 4, non-insulated** |
| `2026-09-19_consumables_copper_tape_and_wick.jpg` | `IMG_8643` | 09:40:53 | A large roll of copper tape, a spool of fine copper-coloured wire, a desoldering-wick reel, rubber bands, scissors, a small black printed box, red heat-shrink | `READ` |
| `2026-09-19_consumables_scissors_and_box.jpg` | `IMG_8644` | 09:40:54 | Scissors, copper tape squares, the printed box, wick | `READ` |
| `2026-09-19_isopropyl_99_percent.jpg` | `IMG_8645` | 09:40:58 | **99% isopropyl alcohol, Signature Care, 16 fl oz (473 mL)**, held | `READ` — photographic backing for the `docs/INVENTORY.md` row |
| `2026-09-19_distilled_water.jpg` | `IMG_8646` | 09:40:59 | **CVS Health Distilled Water, 1 US gallon**, "purified by steam distillation" | `READ` — the inventory row says "deionised / distilled"; **the label says distilled** |
| `2026-09-19_instrument_full_height.jpg` | `IMG_8647` | 09:41:02 | **The best single overview of the assembled instrument** — full height, frame to base, everything on the platform in one frame | `READ` |
| `2026-09-19_faraday_enclosure_on_bench.jpg` | `IMG_8648` | 09:41:06 | The copper-foil enclosure **off** the instrument, beside the soldering station, with a **ChipQuik RMA791** flux jar | `READ` |
| `2026-09-19_laptop_screen_blurred.jpg` | `IMG_8649` | 09:41:10 | A laptop screen, **badly motion-blurred and unreadable**. Kept for completeness only | `READ` |
| `2026-09-19_scan_head_close_bands_1.jpg` | `IMG_8650` | 09:41:19 | **Close-up of the head**: two black knurled thumb-knobs on threaded shafts, the aluminium-taped plate, **two twisted rubber bands** hooked over screw heads, the stepper, and a wrapper labelled **"$10.00 QUARTERS · N.F. STRING & SON, INC."** | `READ` |
| `2026-09-19_scan_head_close_bands_2.jpg` | `IMG_8651` | 09:41:21 | Closer on the two twisted bands and the screws they hook over | `READ` |
| `2026-09-19_scan_head_close_out_of_focus.jpg` | `IMG_8652` | 09:41:23 | The same region, out of focus. No usable detail | `READ` |
| `2026-09-19_scan_head_close_bands_3.jpg` | `IMG_8653` | 09:41:26 | **The sharpest frame of the sample-plate retention**: both twisted bands, the screws they hook over, three threaded ball-end shanks, a small metal terminal behind the plate, the orange bias wire | `READ` |

## Nuh's batch — build history, 8 frames

**These fill gaps.** `2026-08-09` and `2026-09-06` had no photograph in this repository at all.

| File | IMG | Captured | What it shows | Confirmed by |
|---|---|---|---|---|
| `2026-08-01_frame_parts_at_home.jpg` | `IMG_4657` | 2026-08-01 09:30 | **Early frame assembly, indoors at a dining table** — not the workshop. Printed top plate and triangular base on threaded rods, **six flat rectangular metal bars laid on the base**, a 600-piece M2–M4 screw kit. **Jacob** | `READ`; person `SAID` 2026-09-19, by Jacob's rule. **What the six bars are is UNKNOWN — worth one word** |
| `2026-08-01_teensy_carrier_build_1.jpg` | `IMG_4658` | 2026-08-01 11:44 | Two people's hands over a green perfboard; a **Teensy 4.1**, a brass-insert kit box, a **yellow IDC ribbon** | `READ`. Whose hands is UNKNOWN |
| `2026-08-01_teensy_carrier_build_2.jpg` | `IMG_4659` | 2026-08-01 11:44 | The same perfboard with the first wire going on; strippers, a Sharpie, a pink sticky note | `READ` |
| `2026-08-09_tip_etching_setup_1.jpg` | `IMG_4713` | 2026-08-09 15:35 | **The tip-etching setup, outdoors**: a bench supply, a lab stand and clamp over a beaker, further glassware, long gloves, leads running off-frame, a white bottle | **`SAID` Jacob 2026-09-19:** *"The etcher is just the etching setup its not a machine or anything just powersupply through sodium hydroxide"* |
| `2026-08-09_tip_etching_setup_2.jpg` | `IMG_4714` | 2026-08-09 15:35 | The same, clearer. **Jacob** at the table; the bottle's label reads SODIUM HYDROXIDE | as above; person `SAID` 2026-09-19, by Jacob's rule |
| `2026-08-30_teensy_carrier_wiring_side.jpg` | `IMG_4838` | 2026-08-30 14:44 | **The Teensy carrier from the wiring side**, in hand: a 70 × 90 mm protoboard, point-to-point hand wiring, about a dozen coloured leads, a ribbon leaving the bottom edge | `READ`. **NO CONNECTION HAS BEEN READ OFF THIS AND NONE MAY BE** — `docs/WIRING.md` is the pinout reference |
| `2026-09-06_preamp_board_in_head.jpg` | `IMG_4851` | 2026-09-06 12:50 | **The preamplifier board in the scan head, silkscreen legible: JP1, R1, C1, C2, C3, IC1** — the same designators as `docs/WIRING.md` §10. An axial leaded part is mounted in the air on bent leads; five wires enter JP1 | `READ`. **THIS IS THE OLD BOARD** — the preamp was rebuilt into a new box on 2026-09-15. **No value has been taken from the resistor's colour bands and none should be** |
| `2026-09-06_preamp_module_in_hand.jpg` | `IMG_4852` | 2026-09-06 13:50 | The preamp module in a gloved hand, copper tape framing the board, the wire bundle entering, **a fine bare wire protruding to the right ending in a small blob** | `READ`. Whose hand is UNKNOWN |

## Nuh's batch — 2026-09-19 before the teardown, 10 frames

| File | IMG | Captured | What it shows | Confirmed by |
|---|---|---|---|---|
| `2026-09-19_faraday_enclosure_held.jpg` | `IMG_4898` | 09:33:31 | **The copper-foil enclosure held up**, in a different room from the workshop. Two rectangular openings in one face, a small round hole in the top. **Jacob** | `READ`; person `SAID` 2026-09-19, by Jacob's rule |
| `2026-09-19_bench_power_supplies_1.jpg` | `IMG_4899` | 09:40:51 | **Both bench supplies, models legible: `JESVERTY SPS-3010 0–30 V 0–10 A` and `LONGWEI LW-K3010D 30 V/10 A`.** A 20 × 80 mm perfboard sits on top with a yellow lead and a copper-tape splice | `READ` — **neither model was recorded anywhere before** |
| `2026-09-19_bench_power_supplies_top.jpg` | `IMG_4900` | 09:40:57 | Top-down of the same, showing the perfboard, the jumper leads and a crumpled copper-tape splice joining several wires | `READ`. **How the two supplies are joined to each other has NOT been read off this and must not be** |
| `2026-09-19_bench_power_supplies_2.jpg` | `IMG_4901` | 09:41:02 | Close on the two front panels. **The LONGWEI's displays are lit**, so it had mains power at that moment; whether its output was enabled cannot be read from the frame | `READ` |
| `2026-09-19_controller_in_enclosure.jpg` | `IMG_4902` | 09:41:05 | **The controller PCB inside its black printed box**: the board, a yellow ribbon header along the top edge, **two DB9 connectors on the front face**, many jumper leads | `READ` |
| `2026-09-19_electronics_stack.jpg` | `IMG_4903` | 09:41:07 | The electronics as a stack: the Teensy carrier in its tray above, a second printed box with a perfboard and a small module, the controller box beneath | `READ` |
| `2026-09-19_teensy_carrier_in_tray.jpg` | `IMG_4904` | 09:41:09 | **The Teensy 4.1 on its carrier in a printed tray**, the yellow 26-way ribbon plugged into the carrier, a USB cable at the left | `READ` |
| `2026-09-19_platform_and_springs.jpg` | `IMG_4905` | 09:41:14 | **The platform assembly in context**: springs coming down, **an eyebolt at the platform rim with a spring hooked into it**, the copper base plate, the head, the two thumb-knobs, the twisted bands, three coin wrappers, a coin cup with a coin in it, and the orange wire running down off the platform to the bench | `READ` |
| `2026-09-19_scan_head_rear_1.jpg` | `IMG_4906` | 09:41:25 | **The head from the back, and the preamp box is OPEN** — a small green board and a **bright metal post standing on it** are visible inside the copper-taped box | `READ`. **Whether that post is the turret standoff `docs/INVENTORY.md` records fitted 2026-09-15 is NOT confirmed** |
| `2026-09-19_scan_head_rear_2.jpg` | `IMG_4907` | 09:41:26 | The same, one second later, slightly different angle | `READ` |

## Nuh's batch — THE TEARDOWN, 12 frames, 10:05 to 10:16

**`STATUS.md` records "What was taken apart and how it was packed is UNKNOWN". These frames answer
the first half of that. They do NOT answer the second — no frame shows anything going into a box.**

| File | IMG | Captured | What it shows | Confirmed by |
|---|---|---|---|---|
| `2026-09-19_teardown_jumpers_unplugged.jpg` | `IMG_4908` | 10:05:34 | A hand holding **five jumper leads, unplugged**, in their black female housings | `READ`. Whose hand, and what they came off, are UNKNOWN |
| `2026-09-19_teardown_wiring_1.jpg` | `IMG_4909` | 10:05:38 | The same leads in hand; the electronics boxes open on the bench, a DB9 being handled, the platform still on the frame | `READ` |
| `2026-09-19_teardown_wiring_2.jpg` | `IMG_4910` | 10:05:49 | More leads in hand; a spring eyebolt on the platform rim clearly visible | `READ` |
| `2026-09-19_teardown_supply_lead.jpg` | `IMG_4911` | 10:09:05 | A hand holding a **disconnected red supply lead**; the controller box open behind | `READ` |
| `2026-09-19_teardown_supply_disconnect.jpg` | `IMG_4912` | 10:09:09 | The same lead at the supplies; the boxes open | `READ` |
| `2026-09-19_teardown_bench_overview.jpg` | `IMG_4913` | 10:09:18 | Bench overview mid-teardown: boards at the left, the platform still on the frame at the right | `READ` |
| `2026-09-19_teardown_teensy_and_driver.jpg` | `IMG_4914` | 10:09:42 | **The Teensy carrier and the stepper-driver board**, both out of their boxes. The driver has four LEDs, a white JST connector and a DIP — the same board as `2026-08-07_uln2003_stepper_driver.jpg` | `READ` |
| `2026-09-19_teardown_stepper_driver_board.jpg` | `IMG_4915` | 10:09:50 | The driver board lifted, its five-way motor ribbon still attached | `READ` |
| `2026-09-19_platform_lifted_off_1.jpg` | `IMG_4916` | 10:15:40 | **THE SUSPENDED PLATFORM, OFF THE FRAME AND IN THE HAND** — head, motor, preamp box and coin cups still mounted on it, springs gone | `READ` |
| `2026-09-19_platform_lifted_off_stepper_label.jpg` | `IMG_4917` | 10:15:42 | The same from the motor side. **The stepper's own label is legible: "STEP MOTOR 28BYJ-48 5V DC"** | `READ` from the label — **the first photographic confirmation of the motor part number on our hardware** |
| `2026-09-19_platform_lifted_off_2.jpg` | `IMG_4918` | 10:15:53 | The same, best angle: the head with both twisted bands, the motor and lead screw, the preamp box, **an empty spring eyebolt**, two printed cups with coins | `READ` |
| `2026-09-19_scan_module_held_portrait.jpg` | `IMG_4919` | 10:15:59 | **Jacob holding the complete scanning module**, in the workshop: electrical panel, doors, benches, a chessboard, packing boxes. **The best single frame in the whole set** | Person `SAID` 2026-09-19, by Jacob's rule. Publication on the poster permitted |

## Five more videos that could not be fetched

**Same 10 MB cap as before. A tool limit, not a decision.**

| File | Bytes | Batch |
|---|---|---|
| `IMG_8632.MOV` | 24,930,867 | Jacob — **falls inside the 09:35:33 to 09:38:09 gap**, the last window in which the instrument was filmed assembled. **This is the one worth asking for** |
| `IMG_8654.MOV` | 29,673,694 | Jacob — the last item in the folder |
| `IMG_4615.MOV` | 25,341,025 | Nuh |
| `IMG_4896.MOV` | 88,596,809 | Nuh |
| `IMG_7846.MOV` | 23,155,874 | Nuh — **already in our git history** at commit `4819a31`; a previous session watched it (345 frames, no LED lit in any) |
