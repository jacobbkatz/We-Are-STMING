#!/usr/bin/env python3
"""Report text that collides with other text in any figure of this set.

WHY THIS EXISTS. On 2026-09-20 the figure type scale was raised about a quarter, so
every figure would survive being scaled into a website column and onto a phone. That
broke five layouts at once - a footer through an x-axis label, a panel title through
the row below's ticks, two annotation blocks into each other - and finding them by
eye took four rounds of rendering and looking. This finds them in one pass.

It draws each figure, asks the renderer for the bounding box of every piece of text,
and reports any pair that overlaps by more than `TOL` of the smaller box. Text drawn
with its own opaque background box is allowed to sit on top of other things, which is
what a background box is for, so a pair is only reported when NEITHER carries one.

Run from the repository root:

    python3 deliverables/2026-09-19-pause/figures/code/check_layout.py

Exit code 1 if anything overlaps. It is not a substitute for looking at the figure -
it cannot see a label pointing at the wrong thing - but it catches the whole class of
collision that hand-tuned margins produce.
"""
from __future__ import annotations

import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import matplotlib                                            # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt                              # noqa: E402
from matplotlib.text import Text                             # noqa: E402
from matplotlib.transforms import Bbox                       # noqa: E402

import stmstyle as S                                         # noqa: E402

TOL = 0.06          # fraction of the smaller box that may overlap before it is a fault
TICK_TOL = 0.25     # neighbouring ticks on one axis: their boxes carry the line gap too

FIGURES = ["fig01_calibration", "fig02_iv_curve", "fig03_gap_motion", "fig04_control",
           "fig05_ztest", "fig06_noise", "fig07_signal_chain", "fig08_scale",
           "fig09_timeline", "fig10_push_pull", "fig11_hysteresis", "fig12_lever",
           "fig13_could_we_have_missed_it"]


def _has_background(t):
    """True if this text carries its own opaque box, so it may sit over other marks."""
    p = t.get_bbox_patch()
    return p is not None and p.get_facecolor()[3] > 0.5


def _visible_texts(fig):
    """Every piece of text that is actually drawn, tagged with what kind it is.

    The universe is `findobj`, because the subtitle is built by highlight_text out of
    artists that never reach `fig.texts` - a checker that walked `fig.texts` alone
    reported fig12 clear while its y-axis label ran straight through the subtitle.
    What is then taken OUT is the tick labels that are not drawn: matplotlib keeps a
    Text for every tick it has ever placed, including ticks outside the current view
    limits, and those still report a bounding box.
    """
    drawn_ticks, all_ticks = set(), set()
    for ax in fig.axes:
        for axis, lo_hi in ((ax.xaxis, ax.get_xlim()), (ax.yaxis, ax.get_ylim())):
            lo, hi = min(lo_hi), max(lo_hi)
            for tick in axis.get_major_ticks() + axis.get_minor_ticks():
                t = tick.label1
                all_ticks.add(id(t))
                v = tick.get_loc()
                if v is not None and lo - 1e-9 <= v <= hi + 1e-9:
                    drawn_ticks.add(id(t))
    out, seen = [], set()
    for t in fig.findobj(Text):
        if id(t) in seen:
            continue
        seen.add(id(t))
        if not t.get_visible() or not t.get_text().strip():
            continue
        if id(t) in all_ticks and id(t) not in drawn_ticks:
            continue
        out.append(("tick" if id(t) in all_ticks else "other", t))
    return out


def _deflate(fig, t, bb):
    """Trim the leading that `linespacing` adds, which is empty by definition.

    matplotlib gives every line a box `fontsize * linespacing` tall, so a single line
    of 12 pt text at the house linespacing of 1.6 reports a box half again as tall as
    its glyphs. Comparing those boxes made the checker report fig08's ladder rows as
    colliding when they are seventeen pixels apart on the page. Only the ink counts.
    """
    try:
        slack = t.get_fontsize() * (t._linespacing - 1.0) * fig.dpi / 72.0
    except Exception:                                        # noqa: BLE001
        return bb
    lines = t.get_text().count("\n") + 1
    trim = min(slack * lines * 0.5, (bb.height - 2.0) / 2.0)
    if trim <= 0:
        return bb
    return Bbox.from_extents(bb.x0, bb.y0 + trim, bb.x1, bb.y1 - trim)


def collisions(fig):
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    items = []
    for kind, t in _visible_texts(fig):
        try:
            bb = t.get_window_extent(r)
        except Exception:                                    # noqa: BLE001
            continue
        if bb.width <= 1 or bb.height <= 1:
            continue
        items.append((kind, t, _deflate(fig, t, bb)))
    out = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            ka, ta, a = items[i]
            kb, tb, b = items[j]
            if _has_background(ta) or _has_background(tb):
                continue
            ov = a.intersection(a, b)
            if ov is None or ov.width <= 0 or ov.height <= 0:
                continue
            small = min(a.width * a.height, b.width * b.height)
            # Neighbouring ticks on one axis crowd rather than collide: a wider
            # tolerance, because their boxes carry the line gap as well as the glyphs.
            tol = TICK_TOL if (ka == "tick" and kb == "tick") else TOL
            if ov.width * ov.height > tol * small:
                out.append((ta.get_text().replace("\n", " / ")[:46],
                            tb.get_text().replace("\n", " / ")[:46]))
    return out


def main():
    bad = 0
    for name in FIGURES:
        mod = importlib.import_module(name)
        saved = {}

        def capture(fig, fname, pad=0.32, _s=saved):
            S.narrow_footer(fig)
            S.fit_footer(fig)
            _s[fname] = collisions(fig)
            plt.close(fig)

        real, S.save = S.save, capture
        try:
            (mod.main if hasattr(mod, "main") else mod.build)()
        finally:
            S.save = real
        for fname, hits in saved.items():
            if hits:
                bad += len(hits)
                print("%s: %d overlapping pair(s)" % (fname, len(hits)))
                for a, b in hits:
                    print("    %-48s  x  %s" % (a, b))
            else:
                print("%s: clear" % fname)
    print()
    if bad:
        print("FAIL: %d overlapping text pair(s)" % bad)
        return 1
    print("PASS: no text in this figure set overlaps other text")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
