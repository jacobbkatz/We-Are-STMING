#!/usr/bin/env python3
"""Collect the poster's images into poster/assets/.

WHAT THIS DOES, in plain language
---------------------------------
1. Copies the presentation figures made by the figures agent
   (deliverables/2026-09-19-pause/figures/print/) into poster/assets/.
   Nothing about them is changed.

2. Takes the prepared, annotated photographs
   (deliverables/2026-09-19-pause/photos/prepared/) and CROPS OFF the black
   caption bar at the bottom of each one. The caption is not lost - it is
   re-set in the poster's own large type, in poster.html, keeping the
   SAID / READ marks, the source path, the IMG number and the capture time
   exactly as photos/MANIFEST.md and photos/IMAGE_INVENTORY.md give them.
   photos/prepared/MANIFEST.md explicitly invites this:
   "If your layout has its own caption style, crop the bar off."

   NOTHING ELSE IS DONE TO ANY PHOTOGRAPH. No retouching, no color change,
   no compositing, no scaling up. The yellow annotation arrows and labels
   that the photos agent drew are left exactly as they are.

3. Prints the pixel size of every asset and the biggest width, in inches,
   at which it still prints at 150 dots per inch. Those numbers are what
   poster.html's photo sizes were chosen against.

Run it from anywhere:

    python3 deliverables/2026-09-19-pause/poster/prepare_assets.py
"""
import os
import shutil

from PIL import Image
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PAUSE = os.path.dirname(HERE)
ASSETS = os.path.join(HERE, "assets")
PHOTOS = os.path.join(PAUSE, "photos", "prepared")
FIGPRINT = os.path.join(PAUSE, "figures", "print")

# The caption bar the photos agent draws is solid RGB(12, 12, 12).
BAR = np.array([12, 12, 12])

# The photographs this poster uses. Add or remove a line here and re-run.
PHOTO_FILES = [
    "01_sample_plate_gold_window.jpg",
    "04_instrument_full_height.jpg",
    "05_scan_module_in_hand.jpg",
    "11_tip_etching_setup.jpg",
    "13_poster_module_portrait.jpg",
    "14_poster_team_at_bench.jpg",
    "15_workshop_room.jpg",
]

# The figures this poster uses. These are copied byte for byte from the PRINT
# versions (300 dpi), which is why they can be placed a foot wide and still look
# sharp. All nine exist; the poster itself does not have room for all of them, and
# poster.html says beside each one which is in and which is spare.
FIGURE_FILES = [
    "fig01_calibration.png",
    "fig02_iv_curve.png",
    "fig03_gap_motion.png",
    "fig04_control.png",
    "fig05_ztest.png",
    "fig06_noise.png",
    "fig07_signal_chain.png",
    "fig08_scale.png",
    "fig09_timeline.png",
]


def bar_top(path):
    """Row index where the black caption bar starts, or None if there is none.

    The bar's top 26 rows are pure BAR color with no text on them, so we look
    for the highest run of at least 18 rows that are ~100% bar color and have
    nothing but bar below them. Matching the exact color, rather than just
    "dark", is what makes this work on the photographs that are themselves dark.
    """
    a = np.asarray(Image.open(path).convert("RGB")).astype(int)
    h = a.shape[0]
    m = (np.abs(a - BAR).max(axis=2) <= 12).mean(axis=1)
    pure = m >= 0.995
    best = None
    i = h - 1
    while i >= 0:
        if pure[i]:
            j = i
            while j >= 0 and pure[j]:
                j -= 1
            start, end = j + 1, i
            if end - start + 1 >= 18 and m[start:].mean() >= 0.75:
                best = start
            i = j
        else:
            i -= 1
    return best


def main():
    os.makedirs(ASSETS, exist_ok=True)
    print("%-34s %-14s %s" % ("asset", "pixels", "max width at 150 dpi"))
    print("-" * 78)

    for name in PHOTO_FILES:
        src = os.path.join(PHOTOS, name)
        if not os.path.exists(src):
            print("MISSING  %s" % src)
            continue
        im = Image.open(src).convert("RGB")
        top = bar_top(src)
        if top is None:
            print("  no caption bar found in %s - copied whole" % name)
            out = im
        else:
            out = im.crop((0, 0, im.width, top))
        dst = os.path.join(ASSETS, name)
        out.save(dst, quality=92, optimize=True)
        print("%-34s %-14s %.1f in wide" %
              (name, "%d x %d" % out.size, out.width / 150.0))

    for name in FIGURE_FILES:
        src = os.path.join(FIGPRINT, name)
        if not os.path.exists(src):
            print("%-34s %s" % (name, "not produced by the figures agent - skipped"))
            continue
        dst = os.path.join(ASSETS, name)
        shutil.copyfile(src, dst)
        im = Image.open(dst)
        print("%-34s %-14s %.1f in wide (figure, 300 dpi source)" %
              (name, "%d x %d" % im.size, im.width / 300.0))


if __name__ == "__main__":
    main()
