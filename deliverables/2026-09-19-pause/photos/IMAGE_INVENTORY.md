# Image inventory — every photograph of our hardware, all 92

**Written 2026-09-19 for the pause-point work.** Every frame below was opened and looked at
individually, at full resolution where a detail mattered. This is the single inventory: it covers
the 31 frames that were already in `Images/ours/`, the 31 new ones from Jacob's phone and the
30 new ones from Nuh's.

---

## How to read this file

**`SAID`** — Jacob or Nuh told us, with the date.
**`READ`** — a reading of the frame by Claude. Plausible, **not confirmed**. One word from Jacob
or Nuh settles any of these and the mark should then change to `SAID` with the date.

`CLAUDE.md` is explicit that **a photograph is not a measurement of our hardware**, after the
2026-09-09 session read a part marking off a shared photo and edited five documents before anyone
asked whose board it was. It was Dan Berard's. Everything in this folder is our own bench, so
*whose* is settled; *what each frame shows* is not, and that is what the marks are for.

**No number has been taken off any photograph here**, and in particular **`d`, the tip-to-pivot
distance, has NOT been measured and must not be.** `Images/ours/README.md` records three attempts
that gave answers differing by more than a factor of two, and four reasons the measurement cannot
work.

### The three shoots, and why the camera matters

| Batch | Frames | Camera | Owner of the Drive files |
|---|---|---|---|
| Already in the repository, committed 2026-09-17/18 | 31 | not recorded | Jacob |
| **New — Jacob's batch** | 31 (`IMG_86xx`) | **iPhone 17 Pro** | `jacob@quis.com` |
| **New — Nuh's batch** | 30 (`IMG_46xx`–`IMG_49xx`) | **iPhone 13 Pro Max** | `nuh.bmshaheer@gmail.com` |

**The two new batches are independent shoots**, and on 2026-09-19 they overlap in time: Jacob's run
09:35–09:41 and Nuh's 09:33–10:15, both camera-local. **Nuh's run half an hour later and they are
the ones that catch the teardown.**

> **File ownership is not authorship and it is not identity.** Nuh uploading a frame makes him the
> likely photographer, not the likely subject.

### Times

All capture times are **camera-local, with no offset tag in the EXIF**, so the relation to the UTC
timestamps in the session logs is an inference, not a fact. The EXIF tables are in
`deliverables/2026-09-19-pause/SOURCE_INVENTORY.md` and `NUH_PHOTOS_ADDENDUM.md`. The working
copies in `Images/ours/` are EXIF-stripped (verified zero tags); **the IMG_ number in every row
below is how the Drive original is found again.**

### Who is who

**`SAID`, Jacob, 2026-09-19:** *"white guy is jacob brown guy with beared is nuh"*.

That settles which person is which **in a frame that shows a person**. It does not settle whose
hands appear in a close-up, who took a photograph, or who did any step shown — those stay UNKNOWN.

> **How I applied it, and the one caveat.** Jacob gave two discriminators, skin tone and a beard.
> **In these frames the beard is unambiguous and the skin tone is not**, so the beard is what I
> used: the person with the full dark beard is Nuh, the clean-shaven person with dark curly hair is
> Jacob. **Cross-checked and consistent:** the bearded person in the new frames is the same person
> as in `2026-08-01_nuh_soldering.jpg`, which Jacob independently identified as Nuh on 2026-09-18,
> and the clean-shaven person wears a UC San Diego sweatshirt on the day Jacob said he was leaving
> for college in San Diego. **Two independent checks agree.** If either is wrong, say so and every
> caption below marked `SAID (by Jacob's rule)` changes together.

**Publication:** Jacob confirmed 2026-09-19 that **a team photograph may appear on the poster.**
Permission to publish is a separate thing from identification; both are now given.

### Suitability columns

- **M** — usable in the manual (`deliverables/2026-09-19-pause/manual/`)
- **R** — usable in the report
- **P** — usable on the poster
- A dash means not recommended: out of focus, redundant, or nothing in it for that audience.

---

## A. The 31 photographs already in the repository

Captions as committed on 2026-09-17/18, **with three changes made in this pass**, marked `NEW`.

| File | IMG | Date | What it shows | Mark | M | R | P |
|---|---|---|---|---|---|---|---|
| `2026-07-25_controller_pcb_as_delivered.jpg` | — | 2026-07-25 | The controller PCB, held, as it arrived. Four DAC packages, the ADC, two DSUB footprints along the top edge, the 26-way ribbon header at the left. **It arrived populated** — JLCPCB PCBA (`docs/INVENTORY.md`) | `READ` | M | R | P |
| `2026-07-25_second_board_as_delivered.jpg` | — | 2026-07-25 | The second board from the same delivery, held up to the camera. **Which board is not confirmed** | `READ` | — | — | — |
| `2026-07-26_frame_and_suspension_assembled.jpg` | — | 2026-07-26 | The printed frame on the bench with the three suspension posts up, parts still bagged | `READ` | M | — | — |
| `2026-08-01_printed_platform_and_mount.jpg` | — | 2026-08-01 | The printed circular platform and the scan-head mount plate, loose, hole grids visible | `READ` | M | — | — |
| `2026-08-01_nuh_soldering.jpg` | — | 2026-08-01 | **Nuh**, soldering at the bench | `SAID` 2026-09-18 | — | — | P |
| `2026-08-02_frame_assembled.jpg` | — | 2026-08-02 | The frame with the platform hung on its three suspension rods | `READ` | M | — | — |
| `2026-08-07_uln2003_stepper_driver.jpg` | — | 2026-08-07 | The ULN2003 driver board for the 28BYJ-48, in hand. IN1–IN7 labels legible | `READ` | M | — | — |
| `2026-08-07_first_electronics_hookup.jpg` | — | 2026-08-07 | **The first full electronics hookup** — controller, ribbon, stepper, driver, wired on the bench | `SAID` 2026-09-18 | M | R | — |
| `2026-08-07_teensy_carrier_protoboard.jpg` | — | 2026-08-07 | The Teensy 4.1 on its protoboard carrier with the ribbon attached | `READ` | M | — | — |
| `2026-08-19_preamp_board.jpg` | — | 2026-08-19 | The OPA627 transimpedance preamp board against an anti-static bag | `READ` | M | R | — |
| `2026-08-21_preamp_with_coax.jpg` | — | 2026-08-21 | The preamp with its coax tail attached, on a bench mat | `READ` | M | — | — |
| `2026-08-24_scanhead_on_copper_ground_plane.jpg` | — | 2026-08-24 | The scan head on the copper-covered base plate, on the platform, orange coax running off | `READ` | M | — | P |
| `2026-08-26_bench_full_rig.jpg` | — | 2026-08-26 | The whole bench: frame, suspension, supplies, laptop, **Nuh** working. **`NEW` — the person is now identified.** Same beard and same jersey as `2026-08-01_nuh_soldering.jpg`; the caption previously said "which of the two people this is has not been confirmed" | `SAID` 2026-09-19 (by Jacob's rule) | — | R | P |
| `2026-08-29_rig_on_suspension.jpg` | — | 2026-08-29 | The instrument on its suspension with both bench supplies live | `READ` | M | R | P |
| `2026-08-30_ribbon_wiring_diagram_in_use.jpg` | — | 2026-08-30 | A screen showing **this repository's own** 26-way ribbon wiring diagram, in use at the bench | `READ` | — | R | P |
| `2026-09-15_bench_before_powered_session.jpg` | — | 2026-09-15 | The bench set up before the 2026-09-16 powered session | `READ` | M | — | — |
| `2026-09-16_controller_board.jpg` | — | 2026-09-16 | The controller board. **`NEW` — this file was never in the README table** | `READ` | M | R | — |
| `2026-09-16_scanhead_on_platform.jpg` | — | 2026-09-16 | The scan head on the suspended platform. **`NEW` — this file was never in the README table** | `READ` | M | — | — |
| `2026-09-16_faraday_enclosure_on_suspension.jpg` | — | 2026-09-16 | The copper-foil enclosure over the scan head, hanging on the suspension, loom coming out | `READ` | M | R | P |
| `2026-09-16_tip_protrusion_measurement_1.jpg` | — | 2026-09-16 | **The tip-protrusion measurement**, tape against the head face — the provenance for the 1.8 cm in `docs/INVENTORY.md` | `SAID` 2026-09-18 | M | R | — |
| `2026-09-16_tip_protrusion_measurement_2.jpg` | — | 2026-09-16 | The same measurement, closer, three ball ends and the tape in one frame | `SAID` 2026-09-18 | M | R | — |
| `2026-09-16_scan_module_top_down.jpg` | — | 2026-09-16 | **Top-down of the scanning module. The preamp is the little copper box in the middle** | `SAID` 2026-09-18 | M | R | P |
| `2026-09-16_first_gold_attempt_removed.jpg` | — | 2026-09-16 | **The first gold-leaf attempt, made and then removed**, never reported at the time | `SAID` 2026-09-18 | — | R | — |
| `2026-09-16_gold_leaf.jpg` | — | 2026-09-16 | Loose gold leaf flakes on the bench, for scale | `READ` | M | — | P |
| `2026-09-17_sample_plate_rebuilt.jpg` | — | 2026-09-17 | The sample plate off the head: aluminium tape, a square window, gold inside it | `READ` — worth one word from Jacob | M | R | — |
| `2026-09-17_head_and_coax_on_suspension.jpg` | — | 2026-09-17 | The head on the platform with the orange coax looping down to the preamp | `READ` | M | — | — |
| `2026-09-18_scanhead_side.jpg` | — | 2026-09-18 | Side view: copper-taped preamp box above, aluminium-taped head, ball-end screws, copper base plate | `SAID` 2026-09-18 | M | — | — |
| `2026-09-18_scanhead_face_1.jpg` | — | 2026-09-18 | The head face straight on: piezo disc in its bore, tip at the disc centre, tip lead, three ball ends | `SAID` 2026-09-18 | M | R | — |
| `2026-09-18_scanhead_face_2.jpg` | — | 2026-09-18 | Same, second angle | `SAID` 2026-09-18 | — | — | — |
| `2026-09-18_scanhead_face_3.jpg` | — | 2026-09-18 | Same, third angle | `SAID` 2026-09-18 | — | — | — |
| `2026-09-18_scanhead_face_4.jpg` | — | 2026-09-18 | Same, fourth angle | `SAID` 2026-09-18 | — | — | — |

---

## B. New — Jacob's batch, 31 frames (iPhone 17 Pro)

### B1. 2026-09-18 evening, 8 frames — the rebuilt sample plate and the instrument on its frame

These are the frames the **2026-09-18 23:13 session** (commit `6b41855`) read and wrote two
findings from. **They were never committed.** They are now filed, and both readings are checked
against the frames below.

| File | IMG | Captured | What it shows | Mark | M | R | P |
|---|---|---|---|---|---|---|---|
| `2026-09-18_sample_plate_gold_window_1.jpg` | `IMG_8619` | 18:08:45 | **The rebuilt sample plate, face up, off the head.** Aluminium tape over the face; a square window framed in black tape; inside it crinkled copper-coloured foil with a **bright, smooth, flat gold patch covering roughly the centre and centre-right** of the opening. **Copper is exposed to the gold's left and below it.** The orange bias wire enters under the tape at the top; a round through-hole to the right of the window; four black screw heads standing proud | `READ` — **confirms the 2026-09-18 session's reading** | M | R | P |
| `2026-09-18_sample_plate_gold_window_2.jpg` | `IMG_8620` | 18:08:45 | The same plate, one second later, from a fractionally different angle. Nothing differs | `READ` | — | — | — |
| `2026-09-18_instrument_on_suspension_1.jpg` | `IMG_8621` | 19:09:01 | Three-quarter view of the whole instrument on the bench: frame, springs, circular suspended platform, copper base plate, scan head, **three paper coin wrappers standing on the platform**, two dark printed cups at the platform rim | `READ` | M | R | P |
| `2026-09-18_instrument_on_suspension_2.jpg` | `IMG_8622` | 19:09:03 | Side-on. The orange wire loops from the platform down to the bench; other wires run off to the left | `READ` | — | R | — |
| `2026-09-18_platform_and_damping_stack_1.jpg` | `IMG_8623` | 19:09:05 | Side-on, lower, showing the underside of the platform and the tower below it | `READ` | — | R | — |
| `2026-09-18_platform_and_damping_stack_2.jpg` | `IMG_8624` | 19:09:07 | **The clearest view of the platform underside.** A bright disc is fixed under the black platform, and a ring of dark cylinders stands on the tower below it. **At full resolution, background light IS visible between the two in places** | `READ` — **does NOT support the 2026-09-18 reading "no daylight between them"** | M | R | — |
| `2026-09-18_scan_head_top_down_1.jpg` | `IMG_8625` | 19:09:12 | **Top-down of the scan head with the sample plate OFF.** Copper base plate, the head body, the stepper and its lead screw, the rubber bands, wires. Two US coins visible face-up in printed cups at the right | `READ` | M | R | — |
| `2026-09-18_scan_head_top_down_2.jpg` | `IMG_8626` | 19:09:13 | The same, wider, with all three paper coin wrappers in frame. **Each wrapper is hollow at the top** | `READ` | M | — | — |

### B2. 2026-09-19 morning, 23 frames — never seen by any session

| File | IMG | Captured | What it shows | Mark | M | R | P |
|---|---|---|---|---|---|---|---|
| `2026-09-19_instrument_assembled_front.jpg` | `IMG_8630` | 09:35:31 | **The instrument, still fully assembled**, on the bench: top plate on three threaded columns with printed knobs above it, three fine springs down to the platform, the head, three coin wrappers, two coin cups | `READ` | M | R | P |
| `2026-09-19_workshop_room.jpg` | `IMG_8631` | 09:35:33 | **The room.** A basement utility room: concrete floor, wooden bench, the instrument and a laptop on it, a wall-mounted electrical panel and a standby-generator transfer switch a few metres away, cardboard boxes. A hand at the left edge; no face | `READ` | — | R | P |
| `2026-09-19_team_at_bench_1.jpg` | `IMG_8633` | 09:38:09 | **Both of them at the bench with the instrument behind them.** Nuh at the left, Jacob at the right | `SAID` 2026-09-19 (by Jacob's rule) | — | R | **P — best team frame** |
| `2026-09-19_team_at_bench_2.jpg` | `IMG_8634` | 09:38:19 | The same, a second pose | `SAID` 2026-09-19 (by Jacob's rule) | — | — | P |
| `2026-09-19_bench_selfie_1.jpg` | `IMG_8635` | 09:38:50 | Jacob, selfie, the instrument behind | `SAID` 2026-09-19 (by Jacob's rule) | — | — | — |
| `2026-09-19_bench_selfie_2.jpg` | `IMG_8636` | 09:38:51 | The same | `SAID` 2026-09-19 (by Jacob's rule) | — | — | — |
| `2026-09-19_bench_selfie_3.jpg` | `IMG_8637` | 09:38:53 | Jacob pointing at the instrument; **the instrument is sharp in this one** | `SAID` 2026-09-19 (by Jacob's rule) | — | — | P |
| `2026-09-19_team_selfie_1.jpg` | `IMG_8638` | 09:38:55 | Both of them, selfie | `SAID` 2026-09-19 (by Jacob's rule) | — | — | P |
| `2026-09-19_team_selfie_2.jpg` | `IMG_8639` | 09:38:56 | The same, a second frame | `SAID` 2026-09-19 (by Jacob's rule) | — | — | — |
| `2026-09-19_team_selfie_with_laptop.jpg` | `IMG_8640` | 09:40:37 | Both of them with the laptop, a session on screen | `SAID` 2026-09-19 (by Jacob's rule) | — | — | P |
| `2026-09-19_multimeter_and_bench.jpg` | `IMG_8641` | 09:40:50 | **The meter, model legible: `FNIRSI DST-201`.** Also: the controller box with its two DB9s, the tower, loose bare alligator-clip jaws and two loose springs on the bench | `READ` — **new to the repository** | M | R | — |
| `2026-09-19_consumables_clips_and_cutters.jpg` | `IMG_8642` | 09:40:52 | Consumables on a paper towel. A retail card reading **"…gator Clips", "NON-IN[SULATED]", "4"**, bare clip jaws loose beside it, a probe, flush cutters rated "MAX Ø40 (1 mm) DIA. COPPER WIRE", rubber bands, a small green breakout | `READ` | — | — | — |
| `2026-09-19_consumables_copper_tape_and_wick.jpg` | `IMG_8643` | 09:40:53 | A large roll of copper tape, a spool of fine copper-coloured wire, a desoldering-wick reel, a bag of rubber bands, scissors, a small black printed box, red heat-shrink | `READ` | M | — | — |
| `2026-09-19_consumables_scissors_and_box.jpg` | `IMG_8644` | 09:40:54 | Scissors, copper tape squares, the printed box, wick | `READ` | — | — | — |
| `2026-09-19_isopropyl_99_percent.jpg` | `IMG_8645` | 09:40:58 | **99% isopropyl alcohol, Signature Care, 16 fl oz (473 mL)**, held. Photographic backing for the `docs/INVENTORY.md` row | `READ` | — | R | — |
| `2026-09-19_distilled_water.jpg` | `IMG_8646` | 09:40:59 | **CVS Health Distilled Water, 1 US gallon**, "purified by steam distillation". `docs/INVENTORY.md` calls the row "deionised / distilled"; **the label says distilled** | `READ` | — | R | — |
| `2026-09-19_instrument_full_height.jpg` | `IMG_8647` | 09:41:02 | **The best single overview of the assembled instrument.** Full height, frame to base, everything on the platform in one frame | `READ` | **M — hero** | R | **P** |
| `2026-09-19_faraday_enclosure_on_bench.jpg` | `IMG_8648` | 09:41:06 | The copper-foil enclosure **off** the instrument, beside the soldering station, with a **ChipQuik RMA791** flux jar and wick | `READ` | M | R | — |
| `2026-09-19_laptop_screen_blurred.jpg` | `IMG_8649` | 09:41:10 | A laptop screen, **badly motion-blurred and unreadable**. Kept for completeness only | `READ` | — | — | — |
| `2026-09-19_scan_head_close_bands_1.jpg` | `IMG_8650` | 09:41:19 | **Close-up of the head.** Two black knurled thumb-knobs on threaded shafts, the aluminium-taped plate, **two twisted rubber bands** hooked over screw heads, the stepper, a paper wrapper labelled **"$10.00 QUARTERS · N.F. STRING & SON, INC. · HARRISBURG, PA."** | `READ` | M | R | — |
| `2026-09-19_scan_head_close_bands_2.jpg` | `IMG_8651` | 09:41:21 | Closer on the two twisted bands and the screws they hook over | `READ` | M | — | — |
| `2026-09-19_scan_head_close_out_of_focus.jpg` | `IMG_8652` | 09:41:23 | The same region, **out of focus**. No usable detail | `READ` | — | — | — |
| `2026-09-19_scan_head_close_bands_3.jpg` | `IMG_8653` | 09:41:26 | **The sharpest frame of the sample-plate retention**: both twisted bands, the screws, three threaded ball-end shanks, a small metal terminal behind the plate, the orange bias wire | `READ` | **M** | **R** | — |

---

## C. New — Nuh's batch, 30 frames (iPhone 13 Pro Max)

### C1. Build history, 8 frames — 2026-08-01 to 2026-09-06

| File | IMG | Captured | What it shows | Mark | M | R | P |
|---|---|---|---|---|---|---|---|
| `2026-08-01_frame_parts_at_home.jpg` | `IMG_4657` | 2026-08-01 09:30 | **Early frame assembly, indoors at a dining table** — not the workshop. The printed top plate and triangular base on threaded rods; **six flat rectangular metal bars laid on the base**; a 600-piece M2–M4 screw kit box; Jacob | `READ`, person `SAID` 2026-09-19 (by Jacob's rule). **What the six bars are is UNKNOWN — ASK** | M | R | P |
| `2026-08-01_teensy_carrier_build_1.jpg` | `IMG_4658` | 2026-08-01 11:44 | Top-down: two people's hands over a green perfboard; a **Teensy 4.1** and a brass-insert kit box; a **yellow IDC ribbon** | `READ`. Hands UNKNOWN | M | — | — |
| `2026-08-01_teensy_carrier_build_2.jpg` | `IMG_4659` | 2026-08-01 11:44 | The same perfboard with the first wire going on; strippers, a Sharpie, a pink sticky note | `READ` | M | — | — |
| `2026-08-09_tip_etching_setup_1.jpg` | `IMG_4713` | 2026-08-09 15:35 | **The tip-etching setup, outdoors.** A bench supply, a lab stand with a clamp over a beaker, further glassware, long gloves, leads running off-frame, a white bottle | **`SAID` Jacob 2026-09-19**: *"The etcher is just the etching setup its not a machine or anything just powersupply through sodium hydroxide"* | M | **R** | P |
| `2026-08-09_tip_etching_setup_2.jpg` | `IMG_4714` | 2026-08-09 15:35 | The same, clearer. Jacob at the table; the bottle's label reads **SODIUM HYDROXIDE** | as above, person `SAID` 2026-09-19 (by Jacob's rule) | **M** | **R** | **P** |
| `2026-08-30_teensy_carrier_wiring_side.jpg` | `IMG_4838` | 2026-08-30 14:44 | **The Teensy carrier from the wiring side**, in hand. A 70 × 90 mm protoboard, point-to-point hand wiring, about a dozen coloured leads, a ribbon leaving the bottom edge, a USB cable at the top | `READ`. **NO CONNECTION HAS BEEN READ OFF THIS AND NONE MAY BE** — `docs/WIRING.md` is the pinout reference | — | R | — |
| `2026-09-06_preamp_board_in_head.jpg` | `IMG_4851` | 2026-09-06 12:50 | **The preamplifier board in the scan head, silkscreen legible: JP1, R1, C1, C2, C3, IC1** — the same designators as `docs/WIRING.md` §10. An axial leaded part is mounted in the air on bent leads; five wires enter JP1; copper and aluminium tape all round. **THE OLD BOARD** — the preamp was rebuilt into a new box on 2026-09-15 | `READ`. **No value taken from the resistor's colour bands and none should be** | **M** | **R** | — |
| `2026-09-06_preamp_module_in_hand.jpg` | `IMG_4852` | 2026-09-06 13:50 | The preamp module held in a gloved hand, copper tape framing the board, the wire bundle entering, **a fine bare wire protruding to the right ending in a small blob**. Bench, meter and jumper wires behind | `READ`. Whose hand is UNKNOWN | M | R | P |

### C2. 2026-09-19 morning, before the teardown — 11 frames, 09:33 to 09:41

| File | IMG | Captured | What it shows | Mark | M | R | P |
|---|---|---|---|---|---|---|---|
| `2026-09-19_faraday_enclosure_held.jpg` | `IMG_4898` | 09:33:31 | **The copper-foil enclosure held up**, in a different room (hardwood floor, kitchen stools). Two rectangular openings in one face, a small round hole in the top. Jacob, in a UC San Diego sweatshirt | `READ`, person `SAID` 2026-09-19 (by Jacob's rule) | **M** | R | P |
| `2026-09-19_bench_power_supplies_1.jpg` | `IMG_4899` | 09:40:51 | **Both bench supplies, models legible: `JESVERTY SPS-3010 0–30 V 0–10 A` and `LONGWEI LW-K3010D 30 V/10 A`.** A 20 × 80 mm perfboard sits on top with a yellow lead and a copper-tape splice | `READ` — **new to the repository** | **M** | R | — |
| `2026-09-19_bench_power_supplies_top.jpg` | `IMG_4900` | 09:40:57 | Top-down of the same, showing the perfboard, the jumper leads and a crumpled copper-tape splice joining several wires | `READ`. **How the two supplies are joined has NOT been read off this and must not be** | — | R | — |
| `2026-09-19_bench_power_supplies_2.jpg` | `IMG_4901` | 09:41:02 | Close on the two front panels. **The LONGWEI's displays are lit**, so it had mains power at that moment; whether its output was enabled cannot be read | `READ` | — | R | — |
| `2026-09-19_controller_in_enclosure.jpg` | `IMG_4902` | 09:41:05 | **The controller PCB inside its black printed box**, top-down: the board, a yellow ribbon header along the top edge, **two DB9 connectors on the front face**, many jumper leads | `READ` | **M** | R | — |
| `2026-09-19_electronics_stack.jpg` | `IMG_4903` | 09:41:07 | The electronics as a stack: the Teensy carrier in its tray above, a second printed box below with a perfboard and a small module, the controller box beneath | `READ` | M | R | — |
| `2026-09-19_teensy_carrier_in_tray.jpg` | `IMG_4904` | 09:41:09 | **The Teensy 4.1 on its carrier in a printed tray**, the yellow 26-way ribbon plugged into the carrier, a USB cable at the left | `READ` | **M** | R | — |
| `2026-09-19_platform_and_springs.jpg` | `IMG_4905` | 09:41:14 | **The platform assembly in context**: springs coming down, an eyebolt at the platform rim with a spring hooked into it, the copper base plate, the head, the two thumb-knobs, the twisted bands, three coin wrappers, a coin cup with a coin in it, the orange wire running down off the platform | `READ` | **M** | **R** | P |
| `2026-09-19_scan_head_rear_1.jpg` | `IMG_4906` | 09:41:25 | **The head from the back, and the preamp box is OPEN** — a small green board and a **bright metal post standing on it** are visible inside the copper-taped box | `READ`. **Whether that post is the turret standoff `docs/INVENTORY.md` records fitted 2026-09-15 is NOT confirmed — ASK** | **M** | **R** | — |
| `2026-09-19_scan_head_rear_2.jpg` | `IMG_4907` | 09:41:26 | The same, one second later, slightly different angle | `READ` | — | — | — |

### C3. THE TEARDOWN — 9 frames, 10:05 to 10:16

**`STATUS.md` records "What was taken apart and how it was packed is UNKNOWN". These frames answer
the first half of that and not the second.**

| File | IMG | Captured | What it shows | Mark | M | R | P |
|---|---|---|---|---|---|---|---|
| `2026-09-19_teardown_jumpers_unplugged.jpg` | `IMG_4908` | 10:05:34 | A hand holding **five jumper leads, unplugged**, with their black female housings | `READ`. Whose hand is UNKNOWN; what they were unplugged from is UNKNOWN | — | R | — |
| `2026-09-19_teardown_wiring_1.jpg` | `IMG_4909` | 10:05:38 | Wider: the same leads in hand, the electronics boxes open on the bench, a DB9 being handled, the platform still on the frame | `READ` | — | R | — |
| `2026-09-19_teardown_wiring_2.jpg` | `IMG_4910` | 10:05:49 | More leads in hand; **a spring eyebolt on the platform rim, clearly visible** | `READ` | — | R | — |
| `2026-09-19_teardown_supply_lead.jpg` | `IMG_4911` | 10:09:05 | A hand holding a **disconnected red supply lead**; the controller box open behind | `READ` | — | R | — |
| `2026-09-19_teardown_supply_disconnect.jpg` | `IMG_4912` | 10:09:09 | The same lead at the supplies; the boxes open | `READ` | — | R | — |
| `2026-09-19_teardown_bench_overview.jpg` | `IMG_4913` | 10:09:18 | Bench overview mid-teardown: boards at the left, the platform still on the frame at the right | `READ` | — | R | — |
| `2026-09-19_teardown_teensy_and_driver.jpg` | `IMG_4914` | 10:09:42 | **The Teensy carrier and the stepper-driver board**, both out of their boxes. The driver has four LEDs, a white JST connector and a DIP — the same board as `2026-08-07_uln2003_stepper_driver.jpg` | `READ` | M | R | — |
| `2026-09-19_teardown_stepper_driver_board.jpg` | `IMG_4915` | 10:09:50 | The driver board lifted, its five-way motor ribbon attached | `READ` | — | R | — |
| `2026-09-19_platform_lifted_off_1.jpg` | `IMG_4916` | 10:15:40 | **THE PLATFORM, OFF THE FRAME AND IN THE HAND**, head, motor, preamp and coin cups still on it. Springs gone. Room, boxes and electrical panel behind | `READ` | M | **R** | **P** |
| `2026-09-19_platform_lifted_off_stepper_label.jpg` | `IMG_4917` | 10:15:42 | The same from the motor side. **The stepper's own label is legible: "STEP MOTOR 28BYJ-48 5V DC"** | `READ` from the label — **first photographic confirmation on our hardware** | **M** | **R** | — |
| `2026-09-19_platform_lifted_off_2.jpg` | `IMG_4918` | 10:15:53 | The same, best angle: the head with both twisted bands, the motor and lead screw, the preamp box, an **empty spring eyebolt**, two coin cups with coins | `READ` | **M** | **R** | **P** |
| `2026-09-19_scan_module_held_portrait.jpg` | `IMG_4919` | 10:15:59 | **Jacob holding the complete scanning module**, in the workshop: electrical panel, doors, benches, a chessboard, packing boxes | Person `SAID` 2026-09-19 (by Jacob's rule). Publication permitted | — | R | **P — best single frame** |

---

## D. What could NOT be fetched

**Five video clips, all over the Drive connector's hard 10 MB cap. A tool limit, not a decision.**

| File | Bytes | Batch |
|---|---|---|
| `IMG_8632.MOV` | 24,930,867 | Jacob — sits between frames timed 09:35:33 and 09:38:09 |
| `IMG_8654.MOV` | 29,673,694 | Jacob — the last item in the folder |
| `IMG_4615.MOV` | 25,341,025 | Nuh |
| `IMG_4896.MOV` | 88,596,809 | Nuh |
| `IMG_7846.MOV` | 23,155,874 | Nuh — **already in our git history** at commit `4819a31`; a previous session watched it (345 frames, no LED lit in any) |

`Images/ours/README.md` lists twenty-two further clips in the same position and three ways to get
them in: trim on the phone, export at 720p, or screenshot the moment out of the video.

**`IMG_8632.MOV` is the one worth asking for.** It falls inside the 09:35–09:38 gap in Jacob's
sequence, which is exactly the window in which the instrument was last filmed assembled.
