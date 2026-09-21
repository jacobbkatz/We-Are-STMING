#!/usr/bin/env python3
"""Count this repository and write the answers into the poster.

    python3 deliverables/2026-09-19-pause/poster/stamp_counts.py

WHAT THIS IS FOR, in plain language
-----------------------------------
Eight numbers on the poster are not measurements of the microscope. They are
measurements of THIS REPOSITORY: how many lines of operating protocol, how many
session logs, how many rows in the register. Those numbers change every time
anybody works on the project.

They used to be typed into `poster.html` by hand, and on 2026-09-21 an audit found
three of them wrong on a poster that was about to be printed: a twenty-eighth
session log had been written, the checker had grown from 565 lines to 598, and a
sixteenth bench tool had been added. Nobody had done anything careless. Typing a
number that changes on its own is the bug.

So this script counts them, now, and writes them into `poster.html`. Run it and the
poster cannot state a count the repository does not have. `render.py` runs it for
you before every render, so in normal use you never run it yourself.

IT IS SAFE TO RUN AT ANY TIME. Running it twice in a row changes nothing the second
time - it says "already correct" and stops. It only ever rewrites the digits inside
a `<span data-repo-count="...">` tag; it cannot touch a word of the poster's prose.

WHERE THE COUNTING RULES COME FROM, and why they are not in this file
---------------------------------------------------------------------
The project website states most of the same numbers, and it stamps them the same
way, from `site/build_assets.py`. **Two programs counting the same thing is exactly
how two documents come to disagree** - which is the failure `CLAUDE.md` section 3bb
is written about. So six of the eight rules are not repeated here: this script
imports `repo_counts()` out of the website's script and uses whatever it says. If
somebody changes what "a session log" means, the poster and the website change
together, because there is only one definition to change.

Two counts are the poster's alone, because the website does not state them, and
they are defined below with the reason beside each.

WHAT EACH NAME COUNTS
---------------------
  claude-lines         lines in CLAUDE.md                     (from the website)
  facts-rows           rows in docs/FACTS.md, live + retired, counted by
                       Code/pc/count_facts.py                 (from the website)
  checker-lines        lines in Code/pc/check_facts.py        (from the website)
  session-logs         files in sessions/ named YYYY-MM-DD*.md(from the website)
  data-files           .csv / .log / .json under sessions/data(from the website)
  photographs          .jpg / .jpeg / .png in Images/ours     (from the website)
  reference-documents  .md files directly in docs/            (this file)
  bench-tools          .py files in Code/pc/                  (this file)

IF IT STOPS AND COMPLAINS ABOUT A SHALLOW CLONE. That means this computer has only
part of the project's history, so the counting cannot be trusted. Type:

    git fetch --unshallow

and run this again. Nothing is broken.
"""
from __future__ import annotations

import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PAUSE = os.path.dirname(HERE)
REPO = os.path.abspath(os.path.join(PAUSE, "..", ".."))
POSTER = os.path.join(HERE, "poster.html")

# The two briefing documents that quote the same counts in prose. They are checked
# and corrected too, so the poster and what Jacob and Nuh say beside it agree.
BRIEFINGS = ("QUESTIONS_AND_ANSWERS.md", "SPEAKER_SCRIPT.md")


def _website_counts() -> dict:
    """The website's own `repo_counts()`, rather than a second copy of its rules."""
    path = os.path.join(PAUSE, "site", "build_assets.py")
    if not os.path.exists(path):
        raise SystemExit(
            "cannot find the website's build script at %s. The poster's counts are "
            "defined there on purpose, so that the poster and the website cannot "
            "disagree. If the website has been moved, point this script at it." % path)
    spec = importlib.util.spec_from_file_location("site_build_assets", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    # repo_counts() refuses to run in a shallow clone, because the COMMIT count it
    # produces would silently be 1. The poster does not print a commit count, so
    # this is stricter than the poster strictly needs - but the alternative is a
    # second set of counting rules living here, which is the thing this script
    # exists to prevent. One clear instruction is a better price than two registers.
    return mod.repo_counts()


def counts() -> dict:
    c = dict(_website_counts())

    # ---- the two the website does not state -------------------------------------
    # "Reference documents" means the working reference set a session actually reads:
    # the .md files directly in docs/. docs/archive/ is deliberately NOT counted -
    # those carry banners saying they are superseded and are not current instructions
    # (CLAUDE.md section 6). Counted 18 on 2026-09-21.
    docs = os.path.join(REPO, "docs")
    c["reference-documents"] = len([n for n in os.listdir(docs)
                                    if n.endswith(".md")
                                    and os.path.isfile(os.path.join(docs, n))])

    # "Bench tools" means every Python program in Code/pc/ - the ones that talk to the
    # instrument, the ones that analyze its output, and the ones that check the
    # repository itself. The self-test files (`*_test.py`) are counted: they are how
    # the tools that move hardware are trusted, and leaving them out would understate
    # the thing the panel is actually about. Counted 16 on 2026-09-21, the sixteenth
    # being Code/pc/count_facts.py, added 2026-09-20.
    pc = os.path.join(REPO, "Code", "pc")
    c["bench-tools"] = len([n for n in os.listdir(pc) if n.endswith(".py")])
    return c


# Exactly the website's tag shape, so the two pages work the same way.
COUNT_TAG = re.compile(r'(<(\w+)([^>]*\bdata-repo-count="([a-z-]+)"[^>]*)>)([^<]*)(</\2>)')


def stamp_poster(c: dict) -> int:
    page = open(POSTER, encoding="utf-8").read()
    changed, missing = [], []

    def fix(m):
        open_tag, _tag, _attrs, key, body, close = m.groups()
        n = c.get(key)
        if n is None:
            missing.append(key)
            return m.group(0)
        want = format(n, ",")
        if want != body:
            changed.append("%s: %s -> %s" % (key, body, want))
        return open_tag + want + close

    out = COUNT_TAG.sub(fix, page)
    if missing:
        raise SystemExit("poster.html asks for counts this script does not know: %s"
                         % sorted(set(missing)))
    if out != page:
        open(POSTER, "w", encoding="utf-8").write(out)
    if changed:
        print("  poster.html restamped: %s" % "; ".join(changed))
    else:
        print("  every count in poster.html is already correct")
    return len(changed)


# The same numbers, quoted in the prose of the two briefing documents. Each entry is
# a pattern whose capture groups are counts, in order. Add a line here when a
# briefing starts quoting a count in a new form of words.
PROSE = [
    (re.compile(r"(\d+)-line operating protocol"), ["claude-lines"]),
    (re.compile(r"(\d+)-line checker"), ["checker-lines"]),
    (re.compile(r"(\d+)\s*\n?>?\s*append-only session logs"), ["session-logs"]),
    (re.compile(r"\*\*(\d+) lines, (\d+) numbers, (\d+) lines, (\d+) logs\*\*"),
     ["claude-lines", "facts-rows", "checker-lines", "session-logs"]),
]


def stamp_briefings(c: dict) -> int:
    total = 0
    for name in BRIEFINGS:
        path = os.path.join(HERE, name)
        src = open(path, encoding="utf-8").read()
        txt, changed = src, []
        for rx, keys in PROSE:
            def fix(m, keys=keys):
                # Rewrite ONLY the digits inside each capture group, leaving every
                # other character of the sentence exactly as it was. Edits are
                # applied back to front so that changing the width of one number
                # cannot move the position of another.
                whole, base, edits = m.group(0), m.start(), []
                for i, key in enumerate(keys):
                    want = format(c[key], ",")
                    if m.group(i + 1) != want:
                        changed.append("%s: %s -> %s" % (key, m.group(i + 1), want))
                    edits.append((m.start(i + 1) - base, m.end(i + 1) - base, want))
                for s, e, want in reversed(edits):
                    whole = whole[:s] + want + whole[e:]
                return whole
            txt = rx.sub(fix, txt)
        if txt != src:
            open(path, "w", encoding="utf-8").write(txt)
        if changed:
            print("  %s restamped: %s" % (name, "; ".join(changed)))
            total += len(changed)
        else:
            print("  every count quoted in %s is already correct" % name)
    return total


def main() -> int:
    c = counts()
    print("repository counts, measured now:")
    for k in sorted(c):
        print("    %-20s %s" % (k, c[k]))
    n = stamp_poster(c) + stamp_briefings(c)
    print("stamped %d stale number(s)" % n if n else "nothing was stale")
    return 0


if __name__ == "__main__":
    sys.exit(main())
