#!/usr/bin/env python3
"""Audit the website for the mistakes that are cheap to make and expensive to spot.

    python3 deliverables/2026-09-19-pause/site/check_site.py

WHY THIS EXISTS. index.html is 1,300 lines of hand-written markup carrying about
sixty links, two dozen images and every number this project claims. Reading it end
to end catches prose mistakes and misses mechanical ones - a heading level skipped,
an anchor pointing at an id that was renamed, an image whose stated size stopped
matching the file, a color pair that fails contrast in dark mode only. Those are a
CLASS of defect, so they get a program rather than another read-through.

WHAT IT CHECKS, all without a browser:

  links        every href="#id" resolves, and no id is defined twice
  files        every local src/href exists on disk
  sizes        every <img> width/height matches the real pixel size of the file
  alt          every <img> has alt text, or is labeled by a sibling in its link
  headings     no level is skipped (h2 -> h4), exactly one h1
  contrast     every foreground/background token pair meets WCAG AA, light AND dark
  document     lang, title, viewport, description present and sane
  figures      every <figure> says what it is, as a caption or as alt text
  duplicates   no paragraph appears twice (the usual scar of a bad copy-paste)
  counts       every number the page states about THIS repository is current
               (except the commit count, which the build stamps - see the note there)
  spelling     no British spelling survives - including the inflections a bulk
               substitution of the base word leaves behind
  claims       a short list of statements this repository DISPROVES, each of which was
               on the page at some point and each refuted by a named file

The browser-side checks - console errors, 404s, sideways scroll, tap targets - need
Playwright and live in `audit_live.py` beside this file.

Exit code 1 if anything fails, so it can go in a hook or a workflow.
"""
from __future__ import annotations

import html
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(HERE, "index.html")

# ---------------------------------------------------------------- tiny helpers

TAG = re.compile(r"<(?P<close>/?)(?P<name>[a-zA-Z][a-zA-Z0-9]*)(?P<attrs>[^>]*?)(?P<self>/?)>")
ATTR = re.compile(r'([a-zA-Z-]+)\s*=\s*"([^"]*)"')


def attrs_of(chunk: str) -> dict:
    return {k.lower(): v for k, v in ATTR.findall(chunk)}


def srgb_to_lin(c: float) -> float:
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * srgb_to_lin(r) + 0.7152 * srgb_to_lin(g) + 0.0722 * srgb_to_lin(b)


def contrast(a: str, b: str) -> float:
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


# ---------------------------------------------------------------- the checks

def check_ids_and_anchors(page, fail):
    ids = re.findall(r'\sid="([^"]+)"', page)
    for name, n in Counter(ids).items():
        if n > 1:
            fail("links", 'id "%s" is defined %d times' % (name, n))
    have = set(ids)
    for href in re.findall(r'href="#([^"]+)"', page):
        target = href.split("?")[0]
        if target and target not in have:
            fail("links", 'href="#%s" points at an id that does not exist' % target)
    return have


def check_local_files(page, fail):
    refs = set()
    for m in re.finditer(r'(?:src|href)="([^"#?:]+)"', page):
        v = m.group(1)
        if v.startswith(("http", "//", "mailto:", "#", "data:")):
            continue
        refs.add(v)
    for rel in sorted(refs):
        if not os.path.exists(os.path.join(HERE, rel)):
            fail("files", "%s is referenced but not on disk" % rel)
    return refs


def check_images(page, fail):
    try:
        from PIL import Image
    except ImportError:
        fail("sizes", "Pillow is not installed, so image sizes were NOT checked")
        return
    for m in re.finditer(r"<img\b([^>]*)>", page):
        a = attrs_of(m.group(1))
        src = a.get("src", "")
        if not src or src.startswith(("http", "data:")):
            continue
        path = os.path.join(HERE, src)
        if not os.path.exists(path):
            continue                                    # already reported by files
        w, h = Image.open(path).size
        if "width" not in a or "height" not in a:
            fail("sizes", "%s has no width/height attribute, so the page will "
                          "jump when it loads" % src)
            continue
        if (int(a["width"]), int(a["height"])) != (w, h):
            fail("sizes", "%s says %sx%s but the file is %dx%d"
                 % (src, a["width"], a["height"], w, h))


def check_alt_text(page, fail):
    """Every image is either described, or labeled by text inside its own link."""
    for m in re.finditer(r"<img\b([^>]*)>", page):
        a = attrs_of(m.group(1))
        if a.get("alt", "").strip():
            continue
        # An empty alt is correct when a sibling <span> in the same link names it.
        tail = page[m.end():m.end() + 400]
        if re.match(r"\s*<span[^>]*>[^<]+</span>\s*</a>", tail):
            continue
        fail("alt", "%s has no alt text and nothing else names it"
             % a.get("src", "an image"))


def check_headings(page, fail):
    levels = [(int(m.group(1)), re.sub(r"<[^>]+>", "", m.group(2)).strip()[:52])
              for m in re.finditer(r"<h([1-6])\b[^>]*>(.*?)</h\1>", page, re.S)]
    ones = [t for lv, t in levels if lv == 1]
    if len(ones) != 1:
        fail("headings", "the page has %d <h1> elements, it should have exactly one"
             % len(ones))
    prev = 0
    for lv, text in levels:
        if prev and lv > prev + 1:
            fail("headings", 'h%d "%s" follows an h%d - a level is skipped'
                 % (lv, text, prev))
        prev = lv


def _tokens(block: str) -> dict:
    return {k: v for k, v in re.findall(r"--([a-z0-9-]+)\s*:\s*(#[0-9A-Fa-f]{3,6})", block)}


# The pairs the page actually paints: (foreground token, background token, what it is,
# the ratio it must meet). 4.5 for body text, 3.0 for large text and for UI edges.
PAIRS = [
    ("ink", "ground", "body text on the page", 4.5),
    ("ink2", "ground", "secondary text on the page", 4.5),
    ("muted", "ground", "captions and footnotes", 4.5),
    ("ink", "raise", "text on a raised card", 4.5),
    ("ink2", "raise", "secondary text on a raised card", 4.5),
    ("muted", "raise", "captions on a raised card", 4.5),
    ("gold", "ground", "links", 4.5),
    ("gold", "goldwash", "links on the gold wash", 4.5),
    ("verified", "ground", "the verified mark", 4.5),
    ("verified", "verwash", "the verified mark on its wash", 4.5),
]


def check_contrast(page, fail):
    light = _tokens(page[page.index(":root{"):page.index("}", page.index(":root{"))])
    dm = re.search(r"@media \(prefers-color-scheme: dark\)\{(.*?)\n  \}\}", page, re.S)
    if not dm:
        fail("contrast", "no dark-mode token block found, so dark mode was NOT checked")
        dark = {}
    else:
        dark = dict(light)
        dark.update(_tokens(dm.group(1)))
    for scheme, tok in (("light", light), ("dark", dark)):
        if not tok:
            continue
        for fg, bg, what, need in PAIRS:
            if fg not in tok or bg not in tok:
                fail("contrast", "%s: token --%s or --%s is missing"
                     % (scheme, fg, bg))
                continue
            r = contrast(tok[fg], tok[bg])
            if r < need:
                fail("contrast", "%s: %s is %.2f:1 (%s on %s), needs %.1f:1"
                     % (scheme, what, r, tok[fg], tok[bg], need))


def check_document(page, fail):
    if not re.search(r'<html[^>]*\blang="', page):
        fail("document", "<html> has no lang attribute")
    if "<title>" not in page:
        fail("document", "the page has no <title>")
    if 'name="viewport"' not in page:
        fail("document", "no viewport meta, so phones will render it at desktop width")
    d = re.search(r'name="description" content="([^"]*)"', page)
    if not d:
        fail("document", "no meta description")
    elif not (60 <= len(d.group(1)) <= 320):
        fail("document", "the meta description is %d characters; 60-320 reads well "
                         "in a search result" % len(d.group(1)))


def check_figures(page, fail):
    """A figure must SAY what it is - as a caption, or as alt text on its image.

    Not every figure wants a caption: a portrait sitting directly above the person's
    name is captioned by the name. What no figure may do is arrive with neither, and
    that is what this looks for.
    """
    for m in re.finditer(r"<figure\b.*?</figure>", page, re.S):
        block = m.group(0)
        if "<figcaption" in block or 'class="cap"' in block:
            continue
        alts = re.findall(r'<img\b[^>]*\balt="([^"]*)"', block)
        if alts and all(a.strip() for a in alts):
            continue
        src = re.search(r'src="([^"]+)"', block)
        fail("figures", "%s is in a <figure> with no caption and no alt text"
             % (src.group(1) if src else "a figure"))


def check_duplicates(page, fail):
    body = page[page.index("<body"):] if "<body" in page else page
    paras = [re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", p))).strip()
             for p in re.findall(r"<p\b[^>]*>(.*?)</p>", body, re.S)]
    for text, n in Counter(p for p in paras if len(p) > 80).items():
        if n > 1:
            fail("duplicates", 'this paragraph appears %d times: "%s..."'
                 % (n, text[:70]))


def check_repo_counts(page, fail):
    """Every number the page states about this repository, against the repository.

    build_assets.py stamps these at build time, so they should never be wrong. This
    is the belt to that braces: it catches a page committed without a rebuild, which
    is exactly how three of them went stale on the live site on 2026-09-20.
    """
    sys.path.insert(0, HERE)
    try:
        from build_assets import repo_counts, _in_words
    except Exception as exc:                                 # noqa: BLE001
        fail("counts", "could not load the counter from build_assets.py: %s" % exc)
        return
    live = repo_counts()
    for m in re.finditer(
            r'<(\w+)([^>]*\bdata-repo-count="([a-z-]+)"[^>]*)>([^<]*)</\1>', page):
        _tag, attrs, key, body = m.groups()
        # The commit count is stale the instant you commit, by construction: committing
        # the page increments the number the page states. Checking it here made every
        # commit fail its own checker, which is how a checker starts being ignored. The
        # deployed value is right because build_assets.py stamps it during the build,
        # and it cannot be wrong in the other direction because that same script refuses
        # to produce a count at all from a shallow clone.
        if key == "commits":
            continue
        n = live.get(key)
        if n is None:
            fail("counts", 'the page asks for a count called "%s" that nothing measures' % key)
            continue
        want = _in_words(n) if 'data-format="words"' in attrs else format(n, ",")
        if body != want:
            fail("counts", '%s: the page says "%s", the repository says "%s" '
                           "(run build_assets.py)" % (key, body, want))


# The page is written in US English. A bulk substitution catches the common word and
# misses its inflections: converting "tunnelling" on 2026-09-21 left "tunnelled" standing
# in the central claim of the tunnelling section, and "grey" in a comment. That is a CLASS
# of mistake - one rule, applied to a word list that was not complete - so it gets a list
# and a test rather than another read-through.
BRITISH = [
    (r"tunnell(ing|ed|er)", "tunnel + one l: tunneling, tunneled"),
    (r"colou(r|rs|red|ring)\\b", "color"),
    (r"(la|mode|trave|cance|signa|tota|enamè?e?|enamel)lled", "one l before -ed"),
    (r"analogue", "analog"),
    (r"\bcentre(d|s)?\b", "center"),
    (r"\b(nano|micro|milli|kilo)?metres?\b", "meter"),
    (r"\bgrey\b", "gray"),
    (r"behaviour", "behavior"),
    (r"neighbour", "neighbor"),
    (r"jeweller", "jeweler"),
    (r"artefact", "artifact"),
    (r"aluminium", "aluminum"),
    (r"\bwhilst\b", "while"),
    (r"\bamongst\b", "among"),
    (r"\b(recogni|organi|emphasi|analy)s(e|ed|es|ing)\b", "-ize / -yze"),
    (r"\bdefence\b", "defense"),
    (r"\bmodelling\b", "modeling"),
]


def check_spelling(page, fail):
    for pattern, want in BRITISH:
        for m in re.finditer(pattern, page, re.I):
            line = page.count("\n", 0, m.start()) + 1
            around = page[max(0, m.start() - 46):m.end() + 46].replace("\n", " ")
            fail("spelling", 'line %d: "%s" is British, use %s  ...%s...'
                 % (line, m.group(0), want, around.strip()))


# Claims this repository disproves. Each one was actually on the page at some point, and
# each is refuted by a named file. This list is short on purpose: it is not a fact checker,
# it is a memory of specific mistakes that have already been made once.
#
# It exists because a correction script that printed two successful substitutions crashed
# before writing the file, and both were silently lost - the commit that claimed to fix
# them shipped without them. A printed success is not a saved one.
REFUTED = [
    ("wrote the firmware",
     "the firmware is Mech Panda's - README.md line 10, and Code/teensy/src/main.cpp still "
     "carries his typo 'Serial Commnications'. We adapted it"),
    ("every line of code here was written by Claude",
     "same: the firmware came from red-panda-stm"),
    ("at least eleven times the width of the window",
     "docs/FACTS.md: tip travel per motor step is UNDER 1.94 nm, so eleven times is the "
     "ceiling, not the floor"),
    ("coin-wrapper dampers",
     "docs/INVENTORY.md records the wrappers as MASS; the damping is eddy-current"),
    ("damping the springs",
     "same - and STATUS.md lists that coin mass as candidate 6 of 7 for the drift"),
    ("0.16%",
     "the arithmetic gives 0.15%; 0.16% came from a ratio computed on an already-rounded slope"),
    # NOT a bare "word for word": the page legitimately uses it to introduce Jacob's own
    # sentence, printed verbatim right after it. What was wrong was claiming the HERO is
    # his words. So match the claim, not the phrase - a checker that cries wolf on correct
    # text is one people switch off.
    ("top of this page is his, word for word",
     "the hero is our expansion of Jacob's sentence, not a quotation of it. FRAMING.md "
     "asks for his sentence verbatim where one line is needed, which is a different place"),
]


def check_refuted_claims(page, fail):
    low = page.lower()
    for phrase, why in REFUTED:
        i = low.find(phrase.lower())
        if i < 0:
            continue
        line = page.count("\n", 0, i) + 1
        fail("claims", 'line %d: "%s" - %s' % (line, phrase, why))


# The number of drift candidates must NOT be written onto the page.
#
# It was "seven candidates" and went stale inside 24 hours when an outside reading added
# piezo creep - the same failure the session-log and commit counts were fixed for on
# 2026-09-20 by moving them into build_assets.py. Unlike those two, this one cannot be
# counted mechanically: the list lives in prose in STATUS.md. So the rule is simply not to
# state it. "a list of candidates" never goes stale.
CANDIDATE_COUNT = re.compile(
    r"\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|\d+)\s+"
    r"(untested\s+|possible\s+|likely\s+)?candidates\b", re.I)


def check_candidate_count(page, fail):
    for m in CANDIDATE_COUNT.finditer(page):
        line = page.count("\n", 0, m.start()) + 1
        fail("claims",
             'line %d: "%s" - do not write the candidate count on the page. It was "seven" '
             "and went stale in 24 hours when piezo creep was added. STATUS.md is the "
             'register; say "a list of candidates" instead' % (line, m.group(0)))


def main() -> int:
    page = open(PAGE, encoding="utf-8").read()
    problems = []

    def fail(area, msg):
        problems.append((area, msg))

    check_ids_and_anchors(page, fail)
    check_local_files(page, fail)
    check_images(page, fail)
    check_alt_text(page, fail)
    check_headings(page, fail)
    check_contrast(page, fail)
    check_document(page, fail)
    check_figures(page, fail)
    check_duplicates(page, fail)
    check_repo_counts(page, fail)
    check_spelling(page, fail)
    check_refuted_claims(page, fail)
    check_candidate_count(page, fail)

    areas = ["links", "files", "sizes", "alt", "headings", "contrast",
             "document", "figures", "duplicates", "counts", "spelling", "claims"]
    for area in areas:
        hits = [m for a, m in problems if a == area]
        if hits:
            print("%-11s %d problem(s)" % (area, len(hits)))
            for m in hits:
                print("            - %s" % m)
        else:
            print("%-11s clear" % area)
    print()
    if problems:
        print("FAIL: %d problem(s) in the page" % len(problems))
        return 1
    print("PASS: the page is mechanically sound")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
