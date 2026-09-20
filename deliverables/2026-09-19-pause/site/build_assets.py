#!/usr/bin/env python3
"""Rebuild the website's images from the originals in this repository.

    python3 deliverables/2026-09-19-pause/site/build_assets.py

WHAT IT DOES, in plain language. `index.html` next to this file is the project
website. It shows figures and photographs that live elsewhere in the repository at
full size - too large to publish directly - so this script makes web-sized copies of
exactly the ones the page uses, into `site/img/`.

WHY THE COPIES ARE NOT COMMITTED. They are derived files: every one can be rebuilt
from the original by running this. Committing them would double the repository's
image weight for no gain, and they would drift out of date the moment a figure is
regenerated.

HOW TO PUBLISH AN UPDATE. Run this, then publish `index.html` with `site/img/` as
its supporting files. The published page keeps its URL.

QUALITY. Charts are saved at JPEG quality 90 because thin plot lines pick up
artefacts below that; photographs at 82, where nothing is visible. Both are capped
at 1500 px wide, which is enough for a full-width figure on a large screen.
"""
from __future__ import annotations

import os
import re

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PAUSE = os.path.dirname(HERE)
OUT = os.path.join(HERE, "img")

# Page name -> where the original lives. Only what index.html actually references.
PHOTOS = {
    "instrument": "photos/prepared/04_instrument_full_height.jpg",
    "room":       "photos/prepared/15_workshop_room.jpg",
    "teardown":   "photos/prepared/12_teardown_platform_off_frame.jpg",
}
POSTER = "poster/poster_preview.png"


def shrink(src: str, dst: str, maxw: int, quality: int) -> int:
    im = Image.open(src)
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    if im.mode in ("RGBA", "P", "LA"):
        # flatten onto the page's own ground so no black edge appears behind transparency
        bg = Image.new("RGB", im.size, (252, 252, 251))
        im = im.convert("RGBA")
        bg.paste(im, mask=im.split()[-1])
        im = bg
    im.convert("RGB").save(dst, "JPEG", quality=quality, optimize=True, progressive=True)
    return os.path.getsize(dst)


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    total = 0
    for f in sorted(os.listdir(os.path.join(PAUSE, "figures/png"))):
        if f.endswith(".png"):
            total += shrink(os.path.join(PAUSE, "figures/png", f),
                            os.path.join(OUT, f[:5] + ".jpg"), 1500, 90)
    for name, rel in PHOTOS.items():
        total += shrink(os.path.join(PAUSE, rel), os.path.join(OUT, name + ".jpg"), 1500, 82)
    total += shrink(os.path.join(PAUSE, POSTER), os.path.join(OUT, "poster.jpg"), 1800, 82)

    # Fail loudly if the page asks for something this script does not produce.
    page = open(os.path.join(HERE, "index.html"), encoding="utf-8").read()
    used = sorted(set(re.findall(r'(?:src|href)="(img/[^"]+)"', page)))
    missing = [u for u in used if not os.path.exists(os.path.join(HERE, u))]
    if missing:
        raise SystemExit("index.html references images this script does not build: %s" % missing)
    print("built %d images, %.1f MB, and index.html references %d of them"
          % (len(os.listdir(OUT)), total / 1e6, len(used)))


if __name__ == "__main__":
    main()
