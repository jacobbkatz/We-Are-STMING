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

These are all Jacob's own photographs of our own bench, so *whose* is settled. **What is not
settled is what each one shows** — that is a reading of an image, and readings have been wrong
here. So every caption is marked:

- **`SAID`** — Jacob told me what it is, in the conversation of 2026-09-18.
- **`READ`** — my reading of the frame. **Plausible, not confirmed.** One word from Jacob or Nuh
  settles any of these, and the caption should then be changed to `SAID` with the date.

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
| `2026-08-26_bench_full_rig.jpg` | The whole bench: frame, suspension, supplies, laptop, someone working | `READ` — **which of the two people this is has not been confirmed** |
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
