#!/usr/bin/env python3
"""Prepare the selected photographs for the manual, the report and the poster.

Run from the repository root:

    python3 deliverables/2026-09-19-pause/photos/prepare_photos.py

Inputs are the EXIF-stripped 1600 px working copies now filed in `Images/ours/`,
EXCEPT where a crop needs more pixels than 1600 px carries; those read the
full-resolution decoded originals from the lead's scratchpad, which are NOT in
the repository. If the scratchpad is gone the script falls back to the 1600 px
copy and says so, and the output is softer but still correct.

Nothing here changes factual content. Every label names something visible in
the frame it sits on. Labels that are a reading rather than something Jacob or
Nuh stated carry "(READ)".
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
OURS = os.path.join(REPO, "Images", "ours")
OUT = os.path.join(REPO, "deliverables", "2026-09-19-pause", "photos", "prepared")
RAW = ("/tmp/claude-0/-home-user-We-Are-STMING/"
       "5c3eb8ce-8433-54fd-b180-6d24edd1253f/scratchpad/drive_raw")

FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

INK = (255, 214, 0)          # arrow / callout colour, readable on copper and black
INK_DARK = (20, 20, 20)
BAR = (12, 12, 12)


def load(filed_name, img_num, prefer_raw=True):
    """Open a photograph, orientation-corrected, preferring full resolution."""
    raw = os.path.join(RAW, img_num + ".JPG")
    if prefer_raw and os.path.exists(raw):
        return ImageOps.exif_transpose(Image.open(raw)).convert("RGB"), "full-res"
    filed = os.path.join(OURS, filed_name)
    return Image.open(filed).convert("RGB"), "1600px"


def fit(im, box, long_edge=1500):
    w, h = im.size
    l, t, r, b = [int(v * s) for v, s in zip(box, [w, h, w, h])]
    c = im.crop((l, t, r, b))
    m = max(c.size)
    if m != long_edge:
        f = long_edge / m
        c = c.resize((max(1, int(c.width * f)), max(1, int(c.height * f))),
                     Image.LANCZOS)
    return c


def font(size, bold=True):
    return ImageFont.truetype(FONT_B if bold else FONT_R, size)


def arrow(d, xy_from, xy_to, width=5):
    """Straight arrow with a solid head, in fractional coordinates."""
    d.line([xy_from, xy_to], fill=INK, width=width)
    import math
    dx, dy = xy_to[0] - xy_from[0], xy_to[1] - xy_from[1]
    ang = math.atan2(dy, dx)
    L = width * 4.5
    for s in (2.6, -2.6):
        d.line([xy_to, (xy_to[0] - L * math.cos(ang + s / 3.0),
                        xy_to[1] - L * math.sin(ang + s / 3.0))],
               fill=INK, width=width)


def label(d, xy, text, size=30, anchor="lt"):
    f = font(size)
    bb = d.textbbox(xy, text, font=f, anchor=anchor)
    pad = size // 3
    d.rectangle([bb[0] - pad, bb[1] - pad, bb[2] + pad, bb[3] + pad],
                fill=(0, 0, 0))
    d.text(xy, text, font=f, fill=INK, anchor=anchor)


def _wrap(d, text, f, maxw):
    """Greedy word wrap to a pixel width."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=f) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def caption_bar(im, lines, size=26):
    """Add a black bar under the image carrying the caption, word-wrapped.

    The first entry is the headline and is set bold; the rest are body text.
    """
    f = font(size, bold=False)
    fb = font(size)
    pad = size
    maxw = im.width - 2 * pad
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    # Merge the body entries into paragraphs so the wrap is clean; a "Source:"
    # entry always starts a new paragraph.
    paras, cur = [], None
    for i, ln in enumerate(lines):
        if i == 0:
            paras.append(("head", ln))
            cur = None
            continue
        if ln.startswith("Source:") or cur is None:
            paras.append(["body", ln])
            cur = paras[-1]
        else:
            cur[1] = cur[1] + " " + ln
    laid = []
    for kind, ln in paras:
        head = (kind == "head")
        use = fb if head else f
        for sub in _wrap(probe, ln, use, maxw):
            laid.append((sub, use, head))
    line_h = int(size * 1.42)
    h = pad * 2 + line_h * len(laid)
    out = Image.new("RGB", (im.width, im.height + h), BAR)
    out.paste(im, (0, 0))
    d = ImageDraw.Draw(out)
    y = im.height + pad
    for sub, use, head in laid:
        d.text((pad, y), sub, font=use,
               fill=(255, 255, 255) if head else (205, 205, 205))
        y += line_h
    return out


def save(im, name, quality=90):
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, name)
    im.save(p, quality=quality, optimize=True)
    print("%-52s %s" % (name, im.size))


# ---------------------------------------------------------------- 01 gold window
def p01():
    im, src = load("2026-09-18_sample_plate_gold_window_1.jpg", "IMG_8619")
    c = fit(im, (0.28, 0.28, 0.65, 0.57), 1500)
    d = ImageDraw.Draw(c)
    W, H = c.size
    arrow(d, (W * 0.84, H * 0.12), (W * 0.52, H * 0.42))
    label(d, (W * 0.98, H * 0.08), "gold leaf (READ)", 30, anchor="rt")
    arrow(d, (W * 0.10, H * 0.82), (W * 0.33, H * 0.62))
    label(d, (W * 0.02, H * 0.85), "bare copper tape, exposed (READ)", 30)
    arrow(d, (W * 0.06, H * 0.14), (W * 0.24, H * 0.26))
    label(d, (W * 0.02, H * 0.07), "aluminium tape (SAID)", 30)
    c = caption_bar(c, [
        "The window in the sample plate is NOT all gold.",
        "Bright smooth leaf covers roughly the centre and right of the opening; duller crinkled copper tape is",
        "exposed to its left and below. The tip lands on gold only if it lands on the gold part.",
        "Source: Images/ours/2026-09-18_sample_plate_gold_window_1.jpg (IMG_8619, 2026-09-18 18:08:45 camera-local).",
        "READ from the frame. Confirms the reading made by the 2026-09-18 23:13 session, commit 6b41855.",
    ])
    save(c, "01_sample_plate_gold_window.jpg")


# ---------------------------------------------------- 02 platform / damping stack
def p02():
    im, src = load("2026-09-18_platform_and_damping_stack_2.jpg", "IMG_8624")
    c = fit(im, (0.12, 0.30, 0.92, 0.45), 1500)
    d = ImageDraw.Draw(c)
    W, H = c.size
    arrow(d, (W * 0.12, H * 0.05), (W * 0.26, H * 0.30))
    label(d, (W * 0.02, H * 0.02), "suspended platform", 28)
    arrow(d, (W * 0.72, H * 0.08), (W * 0.52, H * 0.42))
    label(d, (W * 0.99, H * 0.03), "bright disc fixed under it (READ: damping plate)",
          26, anchor="rt")
    arrow(d, (W * 0.30, H * 0.97), (W * 0.40, H * 0.72))
    label(d, (W * 0.14, H * 0.99), "cylinders on the tower top (READ: damping magnets)",
          26, anchor="lb")
    c = caption_bar(c, [
        "The gap under the suspended platform - a photograph cannot measure it.",
        "Two distinct parts are visible: a bright disc fixed under the black platform, and a ring of dark cylinders",
        "standing on the tower below it. Background light shows between them in places and not in others, which is",
        "what a near-edge-on view of a small gap looks like. NO GAP HAS BEEN MEASURED AND NONE SHOULD BE TAKEN FROM THIS.",
        "Jacob settled it at the bench: \"its not sitting on the tower is just about its a perfect fit\" (SAID 2026-09-19).",
        "Source: Images/ours/2026-09-18_platform_and_damping_stack_2.jpg (IMG_8624, 2026-09-18 19:09:07 camera-local).",
    ])
    save(c, "02_platform_damping_gap.jpg")


# ------------------------------------------------------- 03 sample plate retention
def p03():
    im, src = load("2026-09-19_scan_head_close_bands_3.jpg", "IMG_8653")
    c = fit(im, (0.02, 0.02, 0.98, 0.98), 1500)
    d = ImageDraw.Draw(c)
    W, H = c.size
    arrow(d, (W * 0.30, H * 0.06), (W * 0.45, H * 0.20))
    label(d, (W * 0.03, H * 0.02), "twisted rubber band", 30)
    arrow(d, (W * 0.30, H * 0.94), (W * 0.45, H * 0.80))
    label(d, (W * 0.03, H * 0.97), "second twisted rubber band", 30, anchor="lb")
    arrow(d, (W * 0.90, H * 0.30), (W * 0.80, H * 0.21))
    label(d, (W * 0.97, H * 0.33), "screw the band hooks over", 30, anchor="rt")
    c = caption_bar(c, [
        "What holds the sample plate on: two twisted rubber bands.",
        "The plate is pulled against the head by two elastic bands, each doubled and twisted, hooked over a screw",
        "head on either side. STATUS.md already lists \"the plate on its bands and balls\" as one of four untested",
        "causes of the gap drifting; this is the first photograph in the repository that shows the mounting.",
        "Source: Images/ours/2026-09-19_scan_head_close_bands_3.jpg (IMG_8653, 2026-09-19 09:41:26 camera-local).",
        "READ. Nothing about band tension, age or creep can be taken from a photograph.",
    ])
    save(c, "03_sample_plate_rubber_bands.jpg")


# ------------------------------------------------------------ 04 whole instrument
def p04():
    im, src = load("2026-09-19_instrument_full_height.jpg", "IMG_8647")
    c = fit(im, (0.02, 0.02, 0.98, 0.86), 1500)
    d = ImageDraw.Draw(c)
    W, H = c.size
    arrow(d, (W * 0.06, H * 0.13), (W * 0.20, H * 0.22))
    label(d, (W * 0.02, H * 0.09), "top plate, threaded columns", 28)
    arrow(d, (W * 0.95, H * 0.30), (W * 0.83, H * 0.36))
    label(d, (W * 0.98, H * 0.26), "suspension spring", 28, anchor="rt")
    arrow(d, (W * 0.14, H * 0.60), (W * 0.30, H * 0.58))
    label(d, (W * 0.02, H * 0.62), "paper coin wrapper", 28)
    arrow(d, (W * 0.80, H * 0.76), (W * 0.58, H * 0.63))
    label(d, (W * 0.98, H * 0.79), "scan head, copper taped", 28, anchor="rt")
    c = caption_bar(c, [
        "The instrument as it stood on the morning of the move.",
        "Printed frame; a top plate on threaded columns; long fine springs down to eyebolts on the circular",
        "suspended platform; the copper-taped scan head on a copper-covered base plate; three paper quarter",
        "wrappers standing on the platform as added mass.",
        "Source: Images/ours/2026-09-19_instrument_full_height.jpg (IMG_8647, 2026-09-19 09:41:02 camera-local).",
        "READ, except the coin mass, which docs/INVENTORY.md records as SAID by Jacob: 18 quarters x 3 plus 10 nickels.",
    ])
    save(c, "04_instrument_full_height.jpg")


# ------------------------------------------------------------- 05 platform in hand
def p05():
    im, src = load("2026-09-19_platform_lifted_off_2.jpg", "IMG_4918")
    c = fit(im, (0.02, 0.05, 0.86, 0.95), 1500)
    d = ImageDraw.Draw(c)
    W, H = c.size
    arrow(d, (W * 0.62, H * 0.06), (W * 0.52, H * 0.20))
    label(d, (W * 0.64, H * 0.03), "preamp box, copper taped", 28)
    arrow(d, (W * 0.95, H * 0.42), (W * 0.83, H * 0.36))
    label(d, (W * 0.98, H * 0.45), "stepper motor", 28, anchor="rt")
    arrow(d, (W * 0.06, H * 0.54), (W * 0.25, H * 0.51))
    label(d, (W * 0.02, H * 0.50), "rubber bands", 28)
    arrow(d, (W * 0.14, H * 0.82), (W * 0.11, H * 0.70))
    label(d, (W * 0.02, H * 0.85), "printed coin cup with a coin in it", 28)
    c = caption_bar(c, [
        "The whole scanning module, lifted off the frame during the move.",
        "The suspended platform with everything it carries: copper-covered base plate, the head held by two rubber",
        "bands, the coarse-approach stepper on its lead screw, the copper-taped preamp box, an empty spring eyebolt",
        "at the right, and two printed cups holding coins.",
        "Source: Images/ours/2026-09-19_platform_lifted_off_2.jpg (IMG_4918, 2026-09-19 10:15:53 camera-local,",
        "Nuh's camera). READ. Whose hand this is has NOT been established.",
    ])
    save(c, "05_scan_module_in_hand.jpg")


# ------------------------------------------------------------- 06 stepper label
def p06():
    im, src = load("2026-09-19_platform_lifted_off_stepper_label.jpg", "IMG_4917")
    c = fit(im, (0.14, 0.52, 0.52, 0.82), 1400)
    c = caption_bar(c, [
        "The coarse-approach motor, label legible.",
        "\"STEP MOTOR  28BYJ-48  5V DC\". This is the first photograph of OUR hardware in which the stepper's own",
        "label can be read; docs/BOM.md and docs/WIRING.md both specify a 28BYJ-48 and this agrees with them.",
        "Source: Images/ours/2026-09-19_platform_lifted_off_stepper_label.jpg (IMG_4917, 2026-09-19 10:15:42",
        "camera-local, Nuh's camera). READ from the label.",
    ])
    save(c, "06_stepper_28byj48_label.jpg")


# ----------------------------------------------------------------- 07 electronics
def p07():
    im, src = load("2026-09-19_teensy_carrier_in_tray.jpg", "IMG_4904")
    c = fit(im, (0.05, 0.28, 0.80, 0.78), 1500)
    d = ImageDraw.Draw(c)
    W, H = c.size
    arrow(d, (W * 0.10, H * 0.06), (W * 0.26, H * 0.20))
    label(d, (W * 0.02, H * 0.02), "Teensy 4.1 (READ)", 30)
    arrow(d, (W * 0.80, H * 0.90), (W * 0.62, H * 0.74))
    label(d, (W * 0.83, H * 0.93), "26-way ribbon", 30, anchor="rt")
    c = caption_bar(c, [
        "The control electronics: Teensy on a hand-wired carrier, in a printed tray.",
        "The microcontroller sits on a 70 x 90 mm protoboard carrier in its own printed box, and a yellow 26-way",
        "ribbon runs from the carrier to the controller board in the box below.",
        "NO CONNECTION HAS BEEN READ OFF THIS PHOTOGRAPH and none should be - docs/WIRING.md is the pinout reference.",
        "Source: Images/ours/2026-09-19_teensy_carrier_in_tray.jpg (IMG_4904, 2026-09-19 09:41:09 camera-local,",
        "Nuh's camera). READ.",
    ])
    save(c, "07_teensy_carrier_and_ribbon.jpg")


# -------------------------------------------------------------- 08 power supplies
def p08():
    im, src = load("2026-09-19_bench_power_supplies_1.jpg", "IMG_4899")
    c = fit(im, (0.0, 0.22, 1.0, 0.80), 1500)
    d = ImageDraw.Draw(c)
    W, H = c.size
    arrow(d, (W * 0.14, H * 0.05), (W * 0.24, H * 0.42))
    label(d, (W * 0.02, H * 0.02), "JESVERTY SPS-3010, 0-30 V 0-10 A", 28)
    arrow(d, (W * 0.80, H * 0.06), (W * 0.74, H * 0.24))
    label(d, (W * 0.98, H * 0.02), "LONGWEI LW-K3010D, 30 V / 10 A", 28, anchor="rt")
    c = caption_bar(c, [
        "The two bench supplies, model numbers legible.",
        "docs/WIRING.md section 7 says the controller needs +-18 V and that \"a single-output bench supply cannot do",
        "this\" - two channels or two supplies in series are required. These are the two supplies that were in use.",
        "HOW THEY ARE CONNECTED TO EACH OTHER HAS NOT BEEN READ OFF THIS FRAME and must not be.",
        "Source: Images/ours/2026-09-19_bench_power_supplies_1.jpg (IMG_4899, 2026-09-19 09:40:51 camera-local,",
        "Nuh's camera). Model names READ from the front panels.",
    ])
    save(c, "08_bench_power_supplies.jpg")


# ------------------------------------------------------------------- 09 enclosure
def p09():
    im, src = load("2026-09-19_faraday_enclosure_held.jpg", "IMG_4898")
    c = fit(im, (0.14, 0.28, 0.92, 0.78), 1400)
    c = caption_bar(c, [
        "The copper-foil enclosure, off the instrument.",
        "A printed box wrapped in copper tape, with two rectangular openings in one face and a small round hole in",
        "the top. This is the shield that goes over the scan head.",
        "Its electrical continuity has never been metered on any box in this project - docs/NEXT_SESSION_PLAN.md V1.",
        "Source: Images/ours/2026-09-19_faraday_enclosure_held.jpg (IMG_4898, 2026-09-19 09:33:31 camera-local,",
        "Nuh's camera). READ.",
    ])
    save(c, "09_faraday_enclosure.jpg")


# ----------------------------------------------------------------- 10 preamp board
def p10():
    im, src = load("2026-09-06_preamp_board_in_head.jpg", "IMG_4851")
    c = fit(im, (0.33, 0.33, 0.82, 0.72), 1500)
    d = ImageDraw.Draw(c)
    W, H = c.size
    arrow(d, (W * 0.88, H * 0.06), (W * 0.60, H * 0.20))
    label(d, (W * 0.97, H * 0.02), "axial part, mounted in the air", 28, anchor="rt")
    arrow(d, (W * 0.08, H * 0.30), (W * 0.24, H * 0.36))
    label(d, (W * 0.02, H * 0.25), "JP1, wires soldered in", 28)
    c = caption_bar(c, [
        "The preamplifier board in the scan head - the AS-BUILT state on 2026-09-06.",
        "Silkscreen designators JP1, R1, C1, C2, C3 and IC1 are legible and match docs/WIRING.md section 10. An axial",
        "leaded component is mounted in the air on bent leads, which is where docs/INVENTORY.md records the 100 Mohm",
        "feedback resistor being fitted. NO VALUE HAS BEEN TAKEN FROM ITS COLOUR BANDS AND NONE SHOULD BE.",
        "THIS IS THE OLD BOARD: the preamp was rebuilt into a new box on 2026-09-15 with a turret standoff, and this",
        "frame predates that. Source: Images/ours/2026-09-06_preamp_board_in_head.jpg (IMG_4851, 2026-09-06 12:50:49",
        "camera-local, Nuh's camera). READ.",
    ])
    save(c, "10_preamp_board_2026-09-06.jpg")


# ------------------------------------------------------------------ 11 tip etching
def p11():
    im, src = load("2026-08-09_tip_etching_setup_2.jpg", "IMG_4714")
    c = fit(im, (0.0, 0.10, 0.85, 0.85), 1500)
    c = caption_bar(c, [
        "The tip-etching setup, outdoors, 2026-08-09.",
        "SAID, Jacob, 2026-09-19: \"The etcher is just the etching setup its not a machine or anything just",
        "powersupply through sodium hydroxide\". Visible in the frame (READ): a bench supply, a lab stand and clamp",
        "over a beaker, further glassware, gloves, and leads running off-frame.",
        "UNKNOWN and not to be filled in from anywhere else: the NaOH concentration, the voltage, the counter-electrode",
        "material, whether it was ever used successfully, and whether any tip fitted to the instrument came off it.",
        "Berard etched in 4 M KOH. That is HIS chemistry, not ours - ours is sodium hydroxide.",
        "Source: Images/ours/2026-08-09_tip_etching_setup_2.jpg (IMG_4714, 2026-08-09 15:35:06, Nuh's camera).",
    ])
    save(c, "11_tip_etching_setup.jpg")


# -------------------------------------------------------------------- 12 teardown
def p12():
    im, src = load("2026-09-19_platform_lifted_off_1.jpg", "IMG_4916")
    c = fit(im, (0.10, 0.02, 0.92, 0.82), 1500)
    c = caption_bar(c, [
        "The move, documented: the suspended platform off the frame at 10:15.",
        "STATUS.md records \"What was taken apart and how it was packed is UNKNOWN\". These frames answer the first",
        "half. Between 10:05 and 10:16 camera-local the jumper leads were unplugged, the supply leads pulled, the",
        "boxes opened, and the platform lifted off the frame with the head, motor and preamp still mounted on it.",
        "HOW IT WAS PACKED IS STILL UNKNOWN - no frame shows anything going into a box.",
        "Source: Images/ours/2026-09-19_platform_lifted_off_1.jpg (IMG_4916, 2026-09-19 10:15:40 camera-local,",
        "Nuh's camera). READ.",
    ])
    save(c, "12_teardown_platform_off_frame.jpg")


# ---------------------------------------------------------------------- 13 poster
def p13():
    im, src = load("2026-09-19_scan_module_held_portrait.jpg", "IMG_4919")
    c = fit(im, (0.08, 0.08, 0.95, 0.92), 1500)
    c = caption_bar(c, [
        "The instrument and the person who built it, on the day it came apart.",
        "Jacob Katz, holding the complete scanning module. Identification per Jacob, SAID 2026-09-19.",
        "Publication on the poster is permitted - Jacob, 2026-09-19.",
        "Source: Images/ours/2026-09-19_scan_module_held_portrait.jpg (IMG_4919, 2026-09-19 10:15:59 camera-local,",
        "Nuh's camera).",
    ])
    save(c, "13_poster_module_portrait.jpg")


# ------------------------------------------------------------------ 14 poster team
def p14():
    im, src = load("2026-09-19_team_at_bench_1.jpg", "IMG_8633")
    c = fit(im, (0.0, 0.26, 1.0, 0.74), 1500)
    c = caption_bar(c, [
        "The team, at the bench, with the instrument.",
        "Nuh Shaheer at the left, Jacob Katz at the right; identification per Jacob, SAID 2026-09-19. The instrument",
        "is on the bench behind them, still assembled. Publication on the poster is permitted - Jacob, 2026-09-19.",
        "Source: Images/ours/2026-09-19_team_at_bench_1.jpg (IMG_8633, 2026-09-19 09:38:09 camera-local).",
    ])
    save(c, "14_poster_team_at_bench.jpg")


# ------------------------------------------------------------------- 15 workshop
def p15():
    im, src = load("2026-09-19_workshop_room.jpg", "IMG_8631")
    c = fit(im, (0.02, 0.06, 0.98, 0.94), 1500)
    c = caption_bar(c, [
        "Where the work happened.",
        "The instrument stands on a wooden bench on a concrete floor in a basement utility room, a few metres from",
        "a wall-mounted electrical panel and a standby-generator transfer switch.",
        "This is context for the noise and vibration problem, not a measurement of either.",
        "Source: Images/ours/2026-09-19_workshop_room.jpg (IMG_8631, 2026-09-19 09:35:33 camera-local). READ.",
    ])
    save(c, "15_workshop_room.jpg")


def main():
    for fn in [p01, p02, p03, p04, p05, p06, p07, p08, p09, p10,
               p11, p12, p13, p14, p15]:
        try:
            fn()
        except Exception as exc:                       # noqa: BLE001
            print("FAILED %s: %s" % (fn.__name__, exc), file=sys.stderr)
            raise


if __name__ == "__main__":
    main()
