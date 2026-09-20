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

THE CAPTION BAR. The photographs in `photos/prepared/` carry their caption burnt
into a black bar at the foot of the image, so that a frame pulled out of the
repository is never separated from its source and its provenance. A web page sets
its own captions, so that bar is cropped off here - it would otherwise print the
same sentence twice, once in white on black and once in grey below. The crop uses
the poster's `bar_top`, which was written for exactly this and has been run on
these files before; there is deliberately not a second copy of it in this script.
`photos/prepared/MANIFEST.md` invites the crop in as many words.
"""
from __future__ import annotations

import importlib.util
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

# Frames showing Jacob or Nuh. These come straight from Images/ours/ rather than
# photos/prepared/, because prepared/ carries a caption bar burnt into the image and
# the page sets its own captions. Every one is cleared: Jacob consented for himself
# 2026-09-19, Nuh 2026-09-20 (second-hand, via Jacob, and recorded as such in
# photos/prepared/MANIFEST.md). That consent covers this project's own deliverables,
# which this page is. It does NOT cover press, a third party's publication, or a
# social post - those are a separate ask.
PEOPLE = {
    "team":      "2026-09-19_team_at_bench_1.jpg",
    "soldering": "2026-08-01_nuh_soldering.jpg",
    "module":    "2026-09-19_scan_module_held_portrait.jpg",
    "etching":   "2026-08-09_tip_etching_setup_1.jpg",
    "benchrig":  "2026-08-26_bench_full_rig.jpg",
    "nuh":       "2026-08-26_bench_full_rig.jpg",
    "laptop":    "2026-09-19_team_selfie_with_laptop.jpg",
}
IMAGES_OURS = os.path.join(os.path.dirname(PAUSE), "..", "Images", "ours")
POSTER = "poster/poster_preview.png"


def _bar_top():
    """Borrow the poster's caption-bar finder rather than writing a second one."""
    path = os.path.join(PAUSE, "poster", "prepare_assets.py")
    spec = importlib.util.spec_from_file_location("poster_prepare_assets", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.bar_top


bar_top = _bar_top()


def shrink(src: str, dst: str, maxw: int, quality: int, crop_bar: bool = False) -> int:
    im = Image.open(src)
    if crop_bar:
        top = bar_top(src)
        if top is None:
            raise SystemExit(
                "%s was expected to carry a caption bar and does not. Either the "
                "photo was regenerated without one, in which case drop it from "
                "PHOTOS_WITH_BAR, or bar_top has stopped working." % src)
        im = im.crop((0, 0, im.width, top))
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


IMG_TAG = re.compile(r'<img\s+[^>]*?src="(img/[^"]+)"[^>]*>')
SIZE_ATTR = re.compile(r'\s+(?:width|height)="\d+"')


def stamp_sizes() -> None:
    """Write each image's real pixel size onto its tag in index.html.

    WHY THIS MATTERS, in plain language. Every photograph on the page is loaded
    late, only when the reader scrolls near it. Until it arrives the browser does
    not know how tall it will be, so it leaves no room - and when the picture
    lands, everything below it jumps down the page under the reader's eyes. Giving
    the browser the width and height up front lets it hold the space open. Nothing
    about the look changes; the CSS still sizes the image. Run this and the page is
    correct again, whatever a figure was regenerated at.
    """
    path = os.path.join(HERE, "index.html")
    page = open(path, encoding="utf-8").read()
    changed = 0

    def fix(m):
        nonlocal changed
        tag, rel = m.group(0), m.group(1)
        w, h = Image.open(os.path.join(HERE, rel)).size
        clean = SIZE_ATTR.sub("", tag)
        want = clean.replace('src="%s"' % rel,
                             'src="%s" width="%d" height="%d"' % (rel, w, h))
        if want != tag:
            changed += 1
        return want

    out = IMG_TAG.sub(fix, page)
    if changed:
        open(path, "w", encoding="utf-8").write(out)
    print("  stamped width/height on %d image tag(s)" % changed
          if changed else "  every image tag already carries its true size")


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    total = 0
    for f in sorted(os.listdir(os.path.join(PAUSE, "figures/png"))):
        if f.endswith(".png"):
            total += shrink(os.path.join(PAUSE, "figures/png", f),
                            os.path.join(OUT, f[:5] + ".jpg"), 1500, 90)
    for name, rel in PHOTOS.items():
        total += shrink(os.path.join(PAUSE, rel), os.path.join(OUT, name + ".jpg"),
                        1500, 82, crop_bar=True)
    for name, rel in PEOPLE.items():
        total += shrink(os.path.join(IMAGES_OURS, rel), os.path.join(OUT, name + ".jpg"), 1400, 82)
    total += shrink(os.path.join(PAUSE, POSTER), os.path.join(OUT, "poster.jpg"), 1800, 82)

    stamp_sizes()

    # Fail loudly if any built image still carries a burnt-in caption bar. The page
    # writes its own captions under every photograph, so a bar here means the same
    # words twice and a frame that looks like an internal working file. This check
    # has been run with the crop switched off and it does go red.
    barred = [f for f in sorted(os.listdir(OUT))
              if bar_top(os.path.join(OUT, f)) is not None]
    if barred:
        raise SystemExit("built images still carry a caption bar: %s" % barred)

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
