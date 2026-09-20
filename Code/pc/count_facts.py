#!/usr/bin/env python3
"""Count the rows in the register, by one stated rule, so the number stops drifting.

    python3 Code/pc/count_facts.py

WHY THIS EXISTS. Five documents carried a row count that has since been RETIRED,
under the rule "table lines that are neither a separator nor a continuation".
Nobody could reproduce that figure from that wording, and the register had grown
since. A number that cannot be recomputed is exactly what this project's register
was built to stop, so here is the rule as a program rather than as a sentence.

THE RULE. A row is a line in `docs/FACTS.md` that

  * begins with a pipe,
  * is not a table separator (a line of only pipes, dashes, colons and spaces), and
  * is not a table header (the line immediately above a separator).

Rows wrapped over several source lines count once, because only the first line of a
wrapped row begins with a pipe. Live rows and retired rows are counted separately
and reported together, because "the register" means both: the values in force and
the values that have been replaced.

THE COUNT IS NOT ITSELF A ROW. A row in the register that counts the register
changes the answer every time anyone touches it, so the count lives here, in the
program that computes it, and nowhere else. Quote it with the date you ran this.
"""
from __future__ import annotations

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FACTS = os.path.normpath(os.path.join(HERE, "..", "..", "docs", "FACTS.md"))

SEP = re.compile(r"^\|[\s:|-]+\|?\s*$")
RETIRED_HEADING = re.compile(r"^##\s+Retired values")


def count(path: str = FACTS):
    lines = open(path, encoding="utf-8").read().split("\n")
    headers = set()
    for i, line in enumerate(lines):
        if SEP.match(line) and i and lines[i - 1].startswith("|"):
            headers.add(i - 1)
    live = retired = 0
    in_retired = False
    for i, line in enumerate(lines):
        if RETIRED_HEADING.match(line):
            in_retired = True
        if not line.startswith("|") or SEP.match(line) or i in headers:
            continue
        if in_retired:
            retired += 1
        else:
            live += 1
    return live, retired


def main() -> None:
    live, retired = count()
    print("docs/FACTS.md")
    print("  live rows    %4d" % live)
    print("  retired rows %4d" % retired)
    print("  TOTAL        %4d   <- this is the number to quote" % (live + retired))
    print()
    print("  Rule: a line starting with a pipe, that is not a separator and not the")
    print("  header directly above one. Wrapped rows count once. Retired values are")
    print("  part of the register, so they are in the total.")
    if "--total" in sys.argv:
        pass


if __name__ == "__main__":
    main()
