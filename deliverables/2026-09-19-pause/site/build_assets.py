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

THE CAPTION BAR. Photographs in `photos/prepared/` carry their caption burnt into a
black bar. The page sets its own captions, so the bar is cropped off here using the
poster's `bar_top` rather than a second copy of it.
"""
from __future__ import annotations

import importlib.util
import os
import sys
import subprocess
import re

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PAUSE = os.path.dirname(HERE)
OUT = os.path.join(HERE, "img")
REPO = os.path.abspath(os.path.join(PAUSE, "..", ".."))

# Page name -> where the original lives. Only what index.html actually references.
CANDIDATES = {
    "candidateA": "candidates/gallery/01_candidateA_wide_profile.png",
}

PHOTOS = {
    "instrument": "photos/prepared/04_instrument_full_height.jpg",
    "room":       "photos/prepared/15_workshop_room.jpg",
    "teardown":   "photos/prepared/12_teardown_platform_off_frame.jpg",
    "wiring":     "photos/prepared/16_scan_module_wiring.jpg",
}

# Frames showing Jacob or Nuh. These come straight from Images/ours/ rather than
# photos/prepared/, because prepared/ carries a caption bar burnt into the image and
# the page sets its own captions. Every one is cleared: Jacob consented for himself
# 2026-09-19, Nuh 2026-09-20 (second-hand, via Jacob, and recorded as such in
# photos/prepared/MANIFEST.md). That consent covers this project's own deliverables,
# which this page is. It does NOT cover press, a third party's publication, or a
# social post - those are a separate ask.
PEOPLE = {
    # The hero photograph. It comes from Images/ours/ rather than photos/prepared/ so it
    # arrives WITHOUT the arrows and callouts: labels belong on a figure a reader has
    # already decided to study, not on the first thing they see.
    "hero":      "2026-09-19_instrument_full_height.jpg",
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
    """The poster's caption-bar finder, rather than a second copy of it."""
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


# The width each photograph is actually DRAWN at, measured in a browser at 390 px and at
# 1280 px on 2026-09-21 - not guessed from the CSS. A browser picks from srcset using
# these, so a wrong number here silently downloads the wrong file. Re-measure if the
# layout changes; audit_live.py prints them.
DRAWN = {
    "hero":       (350, 406), "instrument": (350, 481), "room":     (350, 481),
    "wiring":     (390, 980), "laptop":     (350, 980), "teardown": (350, 980),
    "poster":     (350, 980), "nuh":        (350, 472), "module":   (350, 472),
    "etching":    (350, 492), "team":       (350, 446),
}


def stamp_srcset() -> None:
    """Offer a narrow copy of each photograph, and say how wide it will be drawn.

    WHY. Every photograph was served at its full width whatever the screen. Measured on
    2026-09-21: the page draws them between 406 and 980 px on a laptop and 350 px on a
    phone, against files 1,200 to 1,800 px wide - so an ordinary-density laptop was
    downloading two to three times the pixels it could show, 3.7 MB of it across the page.

    The browser can only choose correctly if it is told BOTH what copies exist (srcset)
    and how wide the picture will be drawn (sizes). Given only srcset it assumes full
    viewport width and picks the big one every time, which is the common way this goes
    wrong and looks like it is working.
    """
    path = os.path.join(HERE, "index.html")
    page = open(path, encoding="utf-8").read()
    changed = 0

    def fix(m):
        nonlocal changed
        tag, rel = m.group(0), m.group(1)
        name = os.path.basename(rel)[:-4]
        if name not in DRAWN or not os.path.exists(os.path.join(OUT, name + "-800.jpg")):
            return tag
        full_w = Image.open(os.path.join(HERE, rel)).size[0]
        phone, desk = DRAWN[name]
        # Three candidates, not two. With only 800 and the full file, a 2x laptop
        # wanting 944 px and a 3x phone wanting 1,050 both jumped straight to the
        # 1,400-1,800 px original - correct, but a long way past what they could show.
        srcset = "img/%s-800.jpg 800w, img/%s-1100.jpg 1100w, %s %dw" % (name, name, rel, full_w)
        sizes = "(max-width: 760px) %dpx, %dpx" % (phone, desk)
        clean = re.sub(r'\s(?:srcset|sizes)="[^"]*"', "", tag)
        want = clean.replace('src="%s"' % rel,
                             'src="%s" srcset="%s" sizes="%s"' % (rel, srcset, sizes))
        if want != tag:
            changed += 1
        return want

    out = IMG_TAG.sub(fix, page)
    if changed:
        open(path, "w", encoding="utf-8").write(out)
    print("  stamped srcset/sizes on %d photograph(s)" % changed
          if changed else "  every photograph already offers a narrow copy")


# ---------------------------------------------------------------- repository counts
#
# Seven numbers on the page describe THE REPOSITORY ITSELF - how many lines of protocol,
# how many session logs, how many commits. They were typed in, and on 2026-09-20 an audit
# found three of them stale on the live site: the checker had grown from 565 lines to 598,
# a twenty-eighth session log had been written, and the commit count was ten behind.
#
# Typing them is the bug. They are computed here, at build time, and stamped into the page,
# so the deployed site cannot state a count the repository does not have.

WORDS = ("zero one two three four five six seven eight nine ten eleven twelve thirteen "
         "fourteen fifteen sixteen seventeen eighteen nineteen").split()
TENS = ("  twenty thirty forty fifty sixty seventy eighty ninety").split()


def _in_words(n: int) -> str:
    """0-99 as words, Capitalised. Above that, digits: nobody writes 'one hundred and six'."""
    if n < 20:
        w = WORDS[n]
    elif n < 100:
        w = TENS[n // 10 - 2] + ("-" + WORDS[n % 10] if n % 10 else "")
    else:
        return format(n, ",")
    return w[0].upper() + w[1:]


def repo_counts() -> dict:
    """Every number the page states about this repository, measured now."""
    def lines(rel):
        with open(os.path.join(REPO, rel), encoding="utf-8") as fh:
            return sum(1 for _ in fh)

    logs = [n for n in os.listdir(os.path.join(REPO, "sessions"))
            if re.match(r"^\d{4}-\d{2}-\d{2}.*\.md$", n)]

    data = 0
    for root, _dirs, names in os.walk(os.path.join(REPO, "sessions", "data")):
        data += sum(1 for n in names if n.endswith((".csv", ".log", ".json")))

    photos = [n for n in os.listdir(IMAGES_OURS)
              if n.lower().endswith((".jpg", ".jpeg", ".png"))]

    # docs/FACTS.md's own counter, so the page and the register agree by construction.
    facts = subprocess.run([sys.executable, os.path.join(REPO, "Code", "pc", "count_facts.py")],
                           capture_output=True, text=True)
    m = re.search(r"TOTAL\s+(\d+)", facts.stdout)
    # A SHALLOW CLONE WOULD LIE, and quietly: `git rev-list --count HEAD` returns 1 in
    # a depth-1 checkout, so the build would stamp "1 commit" onto the live page and
    # every checker would agree with it, because they all read the same shallow repo.
    # Refuse instead. The workflow sets fetch-depth: 0; this is what makes that a
    # guarantee rather than something somebody has to remember.
    shallow = subprocess.run(["git", "rev-parse", "--is-shallow-repository"], cwd=REPO,
                             capture_output=True, text=True)
    if shallow.stdout.strip() == "true":
        raise SystemExit(
            "this is a SHALLOW clone, so the commit count would be wrong. The page "
            "states it, so the build stops here. Set fetch-depth: 0 on the checkout, "
            "or run `git fetch --unshallow`.")
    commits = subprocess.run(["git", "rev-list", "--count", "HEAD"], cwd=REPO,
                             capture_output=True, text=True)
    return {
        "claude-lines": lines("CLAUDE.md"),
        "checker-lines": lines(os.path.join("Code", "pc", "check_facts.py")),
        "session-logs": len(logs),
        "data-files": data,
        "photographs": len(photos),
        "facts-rows": int(m.group(1)) if m else None,
        "commits": int(commits.stdout.strip()) if commits.returncode == 0 else None,
    }


COUNT_TAG = re.compile(r'(<(\w+)([^>]*\bdata-repo-count="([a-z-]+)"[^>]*)>)([^<]*)(</\2>)')


def stamp_repo_counts() -> None:
    """Rewrite every <... data-repo-count="x"> with the value measured just now."""
    counts = repo_counts()
    path = os.path.join(HERE, "index.html")
    page = open(path, encoding="utf-8").read()
    changed, missing = [], []

    def fix(m):
        open_tag, _tag, attrs, key, body, close = m.groups()
        n = counts.get(key)
        if n is None:
            missing.append(key)
            return m.group(0)
        want = _in_words(n) if 'data-format="words"' in attrs else format(n, ",")
        if want != body:
            changed.append("%s: %s -> %s" % (key, body, want))
        return open_tag + want + close

    out = COUNT_TAG.sub(fix, page)
    if out != page:
        open(path, "w", encoding="utf-8").write(out)
    if missing:
        raise SystemExit("the page asks for counts this script does not know: %s"
                         % sorted(set(missing)))
    if changed:
        print("  repository counts restamped: %s" % "; ".join(changed))
    else:
        print("  every repository count on the page is already correct")


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    total = 0
    for f in sorted(os.listdir(os.path.join(PAUSE, "figures/png"))):
        if f.endswith(".png"):
            src = os.path.join(PAUSE, "figures/png", f)
            total += shrink(src, os.path.join(OUT, f[:5] + ".jpg"), 1500, 90)
            # The gallery at the foot of the page shows these at about 210 px wide. It
            # was loading the full-size files to do it - 2.86 MB for thirteen thumbnails.
            # 460 px covers the widest the grid ever gets on a 2x screen; the full file is
            # still one click away behind the link.
            total += shrink(src, os.path.join(OUT, f[:5] + "-thumb.jpg"), 460, 78)
    # The candidate scan shown in the imaging section. It is a gallery analysis figure
    # rather than one of the thirteen page figures, so it is copied by name, but it
    # regenerates from the same committed source as everything else.
    for name, rel in CANDIDATES.items():
        src = os.path.join(PAUSE, rel)
        total += shrink(src, os.path.join(OUT, name + ".jpg"), 1500, 88)
        total += shrink(src, os.path.join(OUT, name + "-thumb.jpg"), 900, 82)
    for name, rel in PHOTOS.items():
        src = os.path.join(PAUSE, rel)
        total += shrink(src, os.path.join(OUT, name + ".jpg"), 1500, 82, crop_bar=True)
        total += shrink(src, os.path.join(OUT, name + "-1100.jpg"), 1100, 81, crop_bar=True)
        total += shrink(src, os.path.join(OUT, name + "-800.jpg"), 800, 80, crop_bar=True)
    for name, rel in PEOPLE.items():
        src = os.path.join(IMAGES_OURS, rel)
        total += shrink(src, os.path.join(OUT, name + ".jpg"), 1400, 82)
        total += shrink(src, os.path.join(OUT, name + "-1100.jpg"), 1100, 81)
        total += shrink(src, os.path.join(OUT, name + "-800.jpg"), 800, 80)
    total += shrink(os.path.join(PAUSE, POSTER), os.path.join(OUT, "poster.jpg"), 1800, 82)
    total += shrink(os.path.join(PAUSE, POSTER), os.path.join(OUT, "poster-1100.jpg"), 1100, 81)
    total += shrink(os.path.join(PAUSE, POSTER), os.path.join(OUT, "poster-800.jpg"), 800, 80)

    stamp_sizes()
    stamp_srcset()
    stamp_repo_counts()

    # A bar here would print the same words twice. Checked by switching the crop
    # off: it does go red.
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
