#!/usr/bin/env python3
"""Draw the hero trace from the raw file, and stamp it into index.html.

    python3 deliverables/2026-09-19-pause/site/build_hero_trace.py

WHY THIS EXISTS. The hero carries a small chart of one real approach - the current
climbing off the noise floor as the tip closes in. Its points were written straight
into the markup and no script in this repository reproduced them, so the one visual
above the fold was the only chart on the site that could not be recomputed. The page
says, four lines above it, that "every measurement on this page can be recomputed
from the raw files". This makes that true of the hero too.

WHAT IT DRAWS. One cycle of the Z test, chosen by a rule rather than by eye: the
approach whose reading count is closest to the median, the same rule figure 13 uses,
so the two show the same kind of event rather than two different flattering ones.

The page is rewritten between the markers in index.html, so the layout, the CSS and
the caption around it are untouched.
"""
from __future__ import annotations

import collections
import csv
import math
import os
import re
import statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))
PAUSE = os.path.dirname(HERE)
REPO = os.path.abspath(os.path.join(PAUSE, "..", ".."))
DATA = os.path.join(REPO, "sessions", "data", "2026-09-19-morning")
FILE = "ztest_1789822585.csv"

CPN = 320.5                       # ADC counts per nanoamp, docs/FACTS.md
FLOOR_NA = 0.05                   # where the drawing bottoms out, just under the noise
TOP_NA = 3.0
W, H = 1000.0, 262.0
L, R, T, B = 52.0, 976.0, 14.0, 249.0


def approaches(path):
    cyc = collections.defaultdict(list)
    with open(path) as fh:
        for r in csv.DictReader(fh):
            if r["phase"] != "in":
                continue
            try:
                cyc[int(r["cycle"])].append((int(r["z"]), abs(float(r["adc"]))))
            except ValueError:
                pass
    return cyc


def main() -> None:
    cyc = approaches(os.path.join(DATA, FILE))
    counts = {c: len(v) for c, v in cyc.items() if len(v) > 8}
    med = st.median(counts.values())
    pick = min(counts, key=lambda c: abs(counts[c] - med))
    pts = cyc[pick]

    zs = [z for z, _ in pts]
    z0, z1 = min(zs), max(zs)
    span = z1 - z0

    def sx(z):
        return L + (R - L) * (z - z0) / float(span)

    def sy(na):
        na = min(max(na, FLOOR_NA), TOP_NA)
        lo, hi = math.log10(FLOOR_NA), math.log10(TOP_NA)
        return B - (B - T) * (math.log10(na) - lo) / (hi - lo)

    # Thin to about 95 points: an SVG in the markup should not carry 400 of them.
    step = max(1, len(pts) // 95)
    thin = pts[::step]
    poly = " ".join("%.1f,%.1f" % (sx(z), sy(a / CPN)) for z, a in thin)

    grid = []
    for na, label in ((0.1, "0.1"), (1.0, "1"), (2.0, "2")):
        y = sy(na)
        grid.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="gl"/>'
                    '<text x="%.1f" y="%.1f" class="gt">%s</text>'
                    % (L, y, R, y, L - 9.0, y + 4.0, label))

    peak = max(a for _z, a in pts) / CPN
    alt = ("A measured approach: the current climbs from the noise floor of about "
           "%.2f nanoamps to %.1f nanoamps as the tip moves %s converter counts "
           "closer to the gold." % (FLOOR_NA, peak, format(span, ",")))

    svg = ('<svg class="trace" viewBox="0 0 %d %d" role="img" aria-label="%s">\n      '
           % (int(W), int(H), alt)
           + "".join(grid)
           + '<polyline class="tr" pathLength="1" points="%s"/>\n    </svg>' % poly)

    path = os.path.join(HERE, "index.html")
    page = open(path, encoding="utf-8").read()
    page, n = re.subn(r'<svg class="trace".*?</svg>', lambda _m: svg, page, count=1,
                      flags=re.S)
    if not n:
        raise SystemExit("could not find the hero trace svg in index.html")

    page = re.sub(r'(<p class="axlab axfoot">tip moving toward the gold, )[\d,]+( converter counts</p>)',
                  lambda m: m.group(1) + format(span, ",") + m.group(2), page, count=1)
    page = re.sub(r'(<p class="tracenote">One real approach, drawn from the raw file\.)(.*?)(</p>)',
                  lambda m: m.group(1) + (
                      " Cycle %d of <code>%s</code>, the one whose "
                      "reading count is closest to the median of the %d approaches in that file. "
                      "The tip moves toward the gold and the current climbs off the noise floor. "
                      "We recorded 109 of these across five files."
                      % (pick, FILE, len(counts))) + m.group(3),
                  page, count=1, flags=re.S)
    open(path, "w", encoding="utf-8").write(page)
    print("hero trace: cycle %d of %s, %d readings, %s Z counts, peak %.2f nA"
          % (pick, FILE, len(pts), format(span, ","), peak))


if __name__ == "__main__":
    main()
