#!/usr/bin/env python3
"""
Find stale numbers that a correction left behind.

    python3 Code/pc/check_facts.py

Why this exists: on 2026-09-07 the ADC full scale was corrected from 4.096 V to
10.24 V and the preamp offset from 37 nA to 119 nA. Both had been written into
more than a dozen documents, and correcting the ones anybody thought of still
left stale copies in the rest. Nothing caught it. This does.

`docs/FACTS.md` holds the canonical value of every number that matters, and a
table of RETIRED values. This script reads that table and reports anywhere a
retired value still appears in a live document.

WHAT IT SKIPS, deliberately:
  * sessions/       -- history. Old logs SHOULD contain the old numbers
  * docs/FACTS.md   -- it lists the retired values on purpose
  * anything the harness generates, and non-prose files

WHAT IT DOES NOT DO: it cannot tell you a number is wrong. It only tells you a
number we already know is wrong is still sitting somewhere it will be believed.

Exit status 0 if clean, 1 if anything was found, so a hook can act on it.
"""

import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FACTS = os.path.join(REPO, 'docs', 'FACTS.md')

SKIP_DIRS = {'.git', 'sessions', '__pycache__', 'node_modules'}
SKIP_FILES = {'FACTS.md', 'check_facts.py'}

# A line that is itself recording the correction is not stale. These are the
# words used when a document says "this used to say X, it is now Y".
EXCUSES = re.compile(
    r'~~|retired|superseded|corrected|was wrong|were wrong|no longer|'
    r'previously|used to|stale|not a bug|do not change|incorrect|'
    r'\bwrong\b|\bvoid\b|replaced by|instead of|rather than|\berror\b|not the input span|is not the|range option|REFBUF',
    re.I)


def retired_patterns():
    """Read the RETIRED table out of docs/FACTS.md.

    Each row looks like:  | `37 nA` as the preamp offset | **119 nA** | ... |
    The first backticked item on the row is the retired literal; the rest of the
    cell is context that narrows when it counts.
    """
    if not os.path.exists(FACTS):
        sys.stderr.write("cannot find docs/FACTS.md -- run from the repository\n")
        sys.exit(2)
    rows, in_table = [], False
    for line in open(FACTS, encoding='utf-8'):
        if line.startswith('## Retired values'):
            in_table = True
            continue
        if in_table and line.startswith('## '):
            break
        if not in_table or not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) < 2 or cells[0].startswith('---') or cells[0] == 'Retired':
            continue
        m = re.search(r'`([^`]+)`', cells[0])
        if not m:
            continue
        literal = m.group(1)
        # "as the ADC full scale" means only flag it near those words
        qual = re.search(r'as the \*\*?([^*|]+?)\*\*?\s*$', cells[0])
        rows.append((literal, qual.group(1).strip().lower() if qual else None,
                     re.sub(r'[*`]', '', cells[1])))
    return rows


def live_files():
    for root, dirs, names in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for n in names:
            if n in SKIP_FILES:
                continue
            if n.endswith(('.md', '.py', '.hpp', '.cpp', '.txt')):
                yield os.path.join(root, n)


def main():
    pats = retired_patterns()
    if not pats:
        print("no retired values listed in docs/FACTS.md -- nothing to check")
        return 0

    hits = []
    for path in sorted(live_files()):
        rel = os.path.relpath(path, REPO)
        try:
            lines = open(path, encoding='utf-8', errors='replace').read().splitlines()
        except OSError:
            continue
        for i, line in enumerate(lines, 1):
            if EXCUSES.search(line):
                continue
            for literal, qual, replacement in pats:
                if literal.lower() not in line.lower():
                    continue
                # If the corrected value is on the same line, the line is a
                # correction table or a sentence saying "X, not Y". Not stale.
                num = re.search(r'[\d.]+', replacement)
                if num and num.group(0) in line:
                    continue
                # A qualified entry ("`4.096` as the ADC full scale") only counts
                # when its qualifying words are nearby -- so 4.096 as REFBUF, and
                # +/-5 V as a DAC range option, do not trip it.
                if qual:
                    window = ' '.join(lines[max(0, i - 2):i + 2]).lower()
                    if not all(w in window for w in qual.split() if len(w) > 3):
                        continue
                hits.append((rel, i, literal, replacement, line.strip()[:88]))

    if not hits:
        print("check_facts: clean. No retired value found in a live document.")
        return 0

    print("check_facts: %d possible stale value(s).\n" % len(hits))
    print("Each line below still contains a number docs/FACTS.md lists as RETIRED.")
    print("If the line is deliberately quoting the old value, add a word like")
    print("'was', 'corrected' or 'superseded' to it and this will stop flagging it.\n")
    last = None
    for rel, ln, literal, repl, text in hits:
        if rel != last:
            print("  %s" % rel)
            last = rel
        print("    %4d  '%s'  ->  should be %s" % (ln, literal, repl))
        print("          %s" % text)
    print("\n%d to review. This script cannot tell you a number is wrong --" % len(hits))
    print("only that one we already know is wrong is still where it will be believed.")
    return 1


if __name__ == '__main__':
    sys.exit(main())
