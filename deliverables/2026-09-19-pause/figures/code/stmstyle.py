"""The shared visual system for the 2026-09-19 pause-point presentation figures.

Every figure in `deliverables/2026-09-19-pause/figures/` imports this module and nothing
else for its look. One place to change typeface, color, grid weight and export sizes, so
all the figures read as coming from one instrument.

TYPEFACE. Inter, committed to `../fonts/` under the SIL Open Font License. It is loaded
from a path relative to this module, so it works on any machine that has the repository -
nothing has to be installed. Inter was drawn for screens and for small sizes, its figures
are even-width so columns of numbers line up, and it stays legible on a poster read from
two meters. matplotlib's DejaVu Sans default is what makes a chart look like a lab report,
and `assert_font_loaded()` below fails loudly rather than falling back to it silently.

HIERARCHY IS WEIGHT, NOT SIZE. Four sizes in the whole system - 13.5 / 10.5 / 9.5 / 8.5 -
and the emphasis comes from weight: SemiBold for a title or the one number that matters,
Medium for a direct label on a mark, Regular for everything else. Nothing is Bold.

PALETTE. The validated default from the `dataviz` skill's `references/palette.md`,
re-checked here with that skill's own validator; the results are in `../STYLE.md`. Do not
add a hue by eye: run the validator.

NOTHING IN THIS FILE IS A PROJECT CONSTANT. Every measured number lives in
`docs/FACTS.md` or in the raw file the figure cites. This module knows color and type.

Run any figure script from the repository root, e.g.

    python3 deliverables/2026-09-19-pause/figures/code/fig01_calibration.py
"""
from __future__ import annotations

import glob
import os
import re

import matplotlib

matplotlib.use("Agg")
import matplotlib.font_manager as fm  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

# ---------------------------------------------------------------- paths

HERE = os.path.dirname(os.path.abspath(__file__))
FIGURES = os.path.dirname(HERE)                       # .../figures
PAUSE = os.path.dirname(FIGURES)                      # .../2026-09-19-pause
REPO = os.path.abspath(os.path.join(PAUSE, "..", ".."))
DATA = os.path.join(REPO, "sessions", "data")
FONTS = os.path.join(FIGURES, "fonts")
PNG = os.path.join(FIGURES, "png")
PRINT = os.path.join(FIGURES, "print")


def data_path(session: str, name: str) -> str:
    """A file under sessions/data/<session>/. READ ONLY - never written by this code."""
    return os.path.join(DATA, session, name)


# ---------------------------------------------------------------- the typeface

for _f in sorted(glob.glob(os.path.join(FONTS, "*.ttf"))):
    fm.fontManager.addfont(_f)

FAMILY = "Inter"


def assert_font_loaded() -> None:
    """Fail loudly if Inter is not registered.

    `addfont` is silent when a family name does not match, and matplotlib then falls back
    to DejaVu Sans without a word. A figure that silently ships in the wrong typeface is
    exactly the failure this check exists to catch.
    """
    have = {e.name for e in fm.fontManager.ttflist}
    if FAMILY not in have:
        raise RuntimeError(
            "%s is not registered. Expected the .ttf files in %s. Found families: %s"
            % (FAMILY, FONTS, sorted(n for n in have if "Inter" in n) or "none"))
    resolved = fm.findfont(fm.FontProperties(family=FAMILY, weight=600))
    if "Inter" not in os.path.basename(resolved):
        raise RuntimeError("%s resolved to %s - matplotlib fell back" % (FAMILY, resolved))


assert_font_loaded()

# Four sizes. Nothing else.
#
# Raised about a quarter on 2026-09-20. A figure 10 in wide renders at 1140 CSS px in
# the website's column and at 350 px on a phone, so every point of type is scaled by
# 1.55 on a laptop and by 0.48 on a phone. At the old 8.5 pt the footer came out at
# 4 px on a phone - a gray smear, measured, not guessed. These sizes plus the shorter
# footers and the scrollable figure frame in the site are what make it legible.
TYPE = dict(title=17.0, label=13.0, annot=12.0, small=11.0, hero=38)
# Three weights. Hierarchy lives here, not in the sizes.
W_TITLE, W_EMPH, W_BODY = 600, 500, 400


# ---------------------------------------------------------------- the palette
#
# Validated default palette, `dataviz` skill references/palette.md.
# Light and dark are the same eight hues stepped for their own surface, not a flip.

LIGHT = dict(
    surface="#fcfcfb",
    plane="#f9f9f7",
    ink="#0b0b0b",
    ink2="#52514e",
    muted="#898781",
    grid="#e1e0d9",
    axis="#c3c2b7",
    band="#f0efec",          # neutral wash: the diverging midpoint step
    series=["#2a78d6", "#eb6834", "#1baf7a", "#eda100",
            "#e87ba4", "#008300", "#4a3aa7", "#e34948"],
    ramp=["#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7",
          "#3987e5", "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b"],
)   # 'word' is attached below, once the text steps are defined

DARK = dict(
    surface="#1a1a19",
    plane="#0d0d0d",
    ink="#ffffff",
    ink2="#c3c2b7",
    muted="#898781",
    grid="#2c2c2a",
    axis="#383835",
    band="#383835",
    series=["#3987e5", "#d95926", "#199e70", "#c98500",
            "#d55181", "#008300", "#9085e9", "#e66767"],
    ramp=["#0d366b", "#104281", "#184f95", "#1c5cab", "#256abf", "#2a78d6",
          "#3987e5", "#5598e7", "#6da7ec", "#86b6ef", "#9ec5f4", "#b7d3f6", "#cde2fb"],
)

# Status palette - fixed, never themed, never used for "series 4".
# Always shipped with a word beside it, never color alone.
STATUS = dict(good="#0ca30c", warning="#fab219", serious="#ec835a", critical="#d03b3b")

# ---------------------------------------------------------------- colored words
#
# These figures name their series by coloring the word in the subtitle instead of
# carrying a legend box. A legend box costs space, sits inside the plot, and collides
# with the data; a colored word is read at poster distance.
#
# A MARK COLOR IS NOT A TEXT COLOR. On the light surface the series hues run 2.7-4.3:1
# against the surface - fine for a 2px line, below the 4.5:1 WCAG needs for body text.
# So each slot has a DARKER TEXT STEP of the same hue, used only for words, while the
# mark keeps the validated series hue. Measured contrast against the surface, computed
# with the dataviz validator's own formula and recorded in ../STYLE.md:
#   blue 6.46  orange 5.16  aqua 4.62  yellow 4.70  magenta 4.98  green 6.33
#   violet 8.33  red 5.12      - every one clears 4.5:1. Dark mode: 7.5 to 9.2.
TEXT_LIGHT = ["#1c5cab", "#b04e27", "#14835b", "#9a6800",
              "#a25672", "#006e00", "#4a3aa7", "#c03e3d"]
# On the dark surface the same idea runs the other way: lighter steps of the same hues.
TEXT_DARK = ["#86b6ef", "#f0936c", "#5fcda4", "#e0b64a",
             "#f0a8c4", "#5fc95f", "#b3abf0", "#f09a9a"]

LIGHT["word"] = TEXT_LIGHT
DARK["word"] = TEXT_DARK

C = dict(LIGHT)
_THEME = "light"


def series(i: int) -> str:
    """Categorical slot i (0-based), in fixed order. Never cycled past 8."""
    if i >= len(C["series"]):
        raise IndexError(
            "slot %d: the palette stops at 8 by design. Fold the tail into 'Other' "
            "or facet into small multiples - never generate a 9th hue." % i)
    return C["series"][i]


def word(i: int) -> str:
    """The TEXT step of slot i - darker (or, in dark mode, lighter) than the mark.

    Use this and only this for a colored word. Never set text in `series(i)`.
    """
    return C["word"][i]


def set_theme(name: str = "light") -> None:
    """'light' or 'dark'. Call before make_fig()."""
    global C, _THEME
    C = dict(LIGHT if name == "light" else DARK)
    _THEME = name
    _rc()


def theme() -> str:
    return _THEME


def _rc() -> None:
    plt.rcParams.update({
        "font.family": FAMILY,
        "font.sans-serif": [FAMILY, "DejaVu Sans"],
        "font.size": TYPE["label"],
        "font.weight": W_BODY,
        "figure.facecolor": C["surface"],
        "savefig.facecolor": C["surface"],
        "axes.facecolor": C["surface"],
        "axes.edgecolor": C["axis"],
        "axes.linewidth": 0.8,
        "axes.labelcolor": C["ink2"],
        "axes.labelsize": TYPE["label"],
        "axes.labelweight": W_BODY,
        "axes.titlesize": TYPE["annot"],
        "axes.titleweight": W_EMPH,
        "axes.titlecolor": C["ink"],
        "axes.titlelocation": "left",
        "axes.titlepad": 10,
        "axes.spines.top": False,        # no top or right spine, anywhere
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.axisbelow": True,          # gridlines behind the data, always
        "grid.color": C["grid"],
        "grid.linewidth": 0.8,
        "grid.linestyle": "-",           # solid hairline. Never dashed.
        "grid.alpha": 1.0,
        "xtick.color": C["muted"],
        "ytick.color": C["muted"],
        "xtick.labelcolor": C["ink2"],
        "ytick.labelcolor": C["ink2"],
        "xtick.labelsize": TYPE["annot"],
        "ytick.labelsize": TYPE["annot"],
        "xtick.direction": "out",
        "ytick.direction": "out",
        "xtick.major.size": 3,
        "ytick.major.size": 3,
        "xtick.major.width": 0.8,
        "ytick.major.width": 0.8,
        "legend.frameon": False,
        "legend.fontsize": TYPE["annot"],
        "legend.labelcolor": C["ink2"],
        "legend.handlelength": 1.6,
        "legend.borderaxespad": 0.0,
        "lines.linewidth": 2.0,
        "lines.solid_capstyle": "round",
        "lines.solid_joinstyle": "round",
        "lines.markersize": 5,
        "patch.linewidth": 0.0,
        "figure.dpi": 150,
        "svg.fonttype": "path",
    })


set_theme("light")


# ---------------------------------------------------------------- figure furniture

def make_fig(width=8.0, height=5.0, nrows=1, ncols=1, **kw):
    """A figure plus axes with the house style already applied."""
    return plt.subplots(nrows, ncols, figsize=(width, height), **kw)


def titles(fig, title, subtitle=None, x=0.012, y=0.982, gap=0.050):
    """Figure title (what the chart says) and subtitle (how to read it).

    The title is a sentence, not a label. A reader who reads only the title should come
    away with the finding, not the variable names.
    """
    fig.text(x, y, title, ha="left", va="top",
             fontsize=TYPE["title"], fontweight=W_TITLE, color=C["ink"])
    if subtitle:
        fig.text(x, y - gap, subtitle, ha="left", va="top",
                 fontsize=TYPE["label"], fontweight=W_BODY, color=C["ink2"],
                 linespacing=1.55)


def titles_keyed(fig, title, subtitle, props, x=0.012, y=0.982, gap=0.050):
    """Title plus a subtitle whose <marked> words are colored to name the series.

    This replaces the legend box. Identity is carried by the words the reader is already
    reading, which is the biggest legibility win at poster distance - and it removes the
    legend-versus-data collision that a box inside the plot always eventually causes.

    `props` is one dict per <marked> span, in order, e.g.
        [{"color": S.word(0), "fontweight": S.W_EMPH}, ...]
    Color a word only with `word(i)`, never with `series(i)`: see the note on the text
    steps above.
    """
    from highlight_text import fig_text
    fig.text(x, y, title, ha="left", va="top",
             fontsize=TYPE["title"], fontweight=W_TITLE, color=C["ink"])
    # vsep is highlight_text's own line spacing, in points. linespacing does nothing
    # here because every line is assembled from separate text boxes.
    fig_text(x=x, y=y - gap, s=subtitle, ha="left", va="top", fig=fig, vsep=3,
             highlight_textprops=props, fontsize=TYPE["label"], fontweight=W_BODY,
             color=C["ink2"])


def footer(fig, text, y=0.010, x=0.012):
    """Provenance line: source file, measurement date, and what the figure is not.

    The text object is kept on the figure so `save()` can measure it and lift the axes
    clear of it. Before that, every script carried a hand-tuned `subplots_adjust(bottom=)`
    that was only correct for one type scale and one wording - raising the type a quarter
    on 2026-09-20 ran five footers straight through their own x-axis label.
    """
    t = fig.text(x, y, text, ha="left", va="bottom",
                 fontsize=TYPE["small"], fontweight=W_BODY, color=C["muted"],
                 linespacing=1.6)
    fig._stm_footer = t
    return t


def _add_paper(fig, inches):
    """Make the figure taller, keeping every axes the same physical size.

    The first version of this compressed the axes instead, and on fig12 it squeezed a
    chart into a tenth of its height to make room for a nine-line footer. Squeezing the
    picture to fit the caption is the wrong way round: the picture is the figure. Extra
    paper at the bottom costs nothing, because a browser scales an image by its WIDTH.
    """
    h = fig.get_figheight()
    keep = [(ax, ax.get_position()) for ax in fig.axes]
    fixed = [(ax, (h - p.y1 * h, p.height * h, p.x0, p.width)) for ax, p in keep]
    new_h = h + inches
    fig.set_figheight(new_h)
    for ax, (from_top, height_in, x0, width) in fixed:
        y1 = (new_h - from_top) / new_h
        y0 = y1 - height_in / new_h
        ax.set_position([x0, y0, width, y1 - y0])


# A block starts at the beginning, or after a sentence end, and is either "Source:" or a
# shouted label. Anchoring on the sentence end is what stops the split landing inside the
# label itself - a bare lookahead matches at every word of "WHAT THIS DOES NOT SHOW:".
_BLOCK = re.compile(r"(?:^|(?<=[.\u2014] ))(?=(?:Source:|[A-Z][A-Z0-9\u2019' -]{6,}:))")


def _paragraphs(text):
    """Split a footer into its labeled blocks.

    The line breaks authors typed are soft - they fall mid-sentence - so they are
    thrown away and the text re-wrapped. What must survive is the block structure:
    `Source:` and shouted labels like `WHAT THIS DOES NOT SHOW:` start a new line.
    """
    flat = " ".join(text.split())
    parts = [p.strip() for p in _BLOCK.split(flat) if p.strip()]
    return parts or [flat]


def _content_right(fig, r, skip):
    """Rightmost pixel of everything on the figure except `skip`."""
    xs = []
    for ax in fig.axes:
        bb = ax.get_tightbbox(r)
        if bb is not None:
            xs.append(bb.x1)
    for t in fig.texts:
        if t is skip:
            continue
        try:
            xs.append(t.get_window_extent(r).x1)
        except Exception:                                  # noqa: BLE001
            pass
    return max(xs) if xs else fig.bbox.width


def narrow_footer(fig, floor=0.55):
    """Re-wrap the footer to the width of everything else on the figure.

    WHY THIS MATTERS MORE THAN IT LOOKS. `save()` writes with `bbox_inches="tight"`,
    so the widest single element sets the width of the exported image - and that was
    always the footer, running a third wider than the chart. The browser then scales
    the whole image down to the column, shrinking the CHART to pay for the footer's
    long lines. Wrapping the footer to the chart's own width makes the exported image
    narrower, so the chart lands on screen about half as large again. Measured on
    fig01: 2,178 px wide before, 1,432 px after, same chart.
    """
    t = getattr(fig, "_stm_footer", None)
    if t is None:
        return
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    want = max(_content_right(fig, r, t) - t.get_window_extent(r).x0,
               fig.bbox.width * floor)
    if t.get_window_extent(r).width <= want:
        return
    probe = fig.text(0.0, -1.0, "", fontsize=t.get_fontsize(),
                     fontweight=t.get_fontweight(), figure=fig)

    def width_of(txt):
        probe.set_text(txt)
        return probe.get_window_extent(r).width

    lines = []
    for para in _paragraphs(t.get_text()):
        cur = ""
        for word in para.split():
            trial = (cur + " " + word).strip()
            if not cur or width_of(trial) <= want:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    probe.remove()
    t.set_text("\n".join(lines))


def fit_footer(fig, gap_in=0.16, rounds=4):
    """Make room under the axes for the footer. Measured, not guessed.

    Asks the renderer where the footer really ends and where the axes really begin -
    tight bounding boxes, so x-axis labels and tick labels count - and adds paper at
    the bottom of the figure if the two meet. Iterates because adding paper changes
    the figure fractions everything else is expressed in.
    """
    t = getattr(fig, "_stm_footer", None)
    if t is None:
        return 0.0
    # A figure whose single axes fills the canvas is a DRAWING, not a plot: its content
    # is hand-placed in data units and its author has already left room under it.
    if fig.axes and all(ax.get_position().height > 0.97 and ax.get_position().width > 0.97
                        for ax in fig.axes):
        return 0.0
    added = 0.0
    for _ in range(rounds):
        fig.canvas.draw()
        r = fig.canvas.get_renderer()
        top = t.get_window_extent(r).y1
        lows = [ax.get_tightbbox(r).y0 for ax in fig.axes
                if ax.get_tightbbox(r) is not None]
        if not lows:
            return added
        deficit = (top + gap_in * fig.dpi) - min(lows)
        if deficit <= 1.0:
            return added
        _add_paper(fig, deficit / fig.dpi)
        added += deficit / fig.dpi
    return added


def note(ax, x, y, text, **kw):
    """An annotation in ink, never in a series color, Regular unless told otherwise."""
    kw.setdefault("fontsize", TYPE["annot"])
    kw.setdefault("color", C["ink2"])
    kw.setdefault("fontweight", W_BODY)
    kw.setdefault("linespacing", 1.6)
    return ax.text(x, y, text, **kw)


def key(ax, x, y, text, **kw):
    """A direct label riding a mark: Medium, primary ink, so it reads before the axes."""
    kw.setdefault("color", C["ink"])
    kw.setdefault("fontweight", W_EMPH)
    return note(ax, x, y, text, **kw)


def tidy(ax, xlabel=None, ylabel=None, title=None, grid="y"):
    """Axis labels (units always), a left-set axis title, and one grid direction."""
    if xlabel:
        ax.set_xlabel(xlabel, labelpad=8)
    if ylabel:
        ax.set_ylabel(ylabel, labelpad=8)
    if title:
        ax.set_title(title)
    ax.grid(axis="both" if grid == "both" else grid, which="major")
    if grid == "y":
        ax.grid(axis="x", visible=False)
    elif grid == "x":
        ax.grid(axis="y", visible=False)
    elif grid == "none":
        ax.grid(False)
    return ax


def thousands(ax, which="y"):
    """Thousands-separated tick labels, which is how the bench reads DAC counts.

    Uses the typographic minus (U+2212), matching matplotlib's own default, so a negative
    tick does not sit beside a shorter hyphen elsewhere on the figure.
    """
    f = FuncFormatter(lambda v, _: format(int(round(v)), ",").replace("-", "−"))
    if which in ("y", "both"):
        ax.yaxis.set_major_formatter(f)
    if which in ("x", "both"):
        ax.xaxis.set_major_formatter(f)


def dot(ax, x, y, color, size=8, z=5, **kw):
    """A data dot with the 2px surface ring already on it."""
    return ax.plot(x, y, "o", color=color, markersize=size,
                   markeredgecolor=C["surface"], markeredgewidth=2.0, zorder=z, **kw)


# ---------------------------------------------------------------- export

def save(fig, name, pad=0.32):
    """Write screen and print copies.

    png/<name>.png     150 dpi, for a screen or a slide
    print/<name>.png   300 dpi, for a 48 x 36 in poster
    print/<name>.svg   vector, for anything that will be scaled further

    All three carry the same layout, so a caption written against one is true of all.
    """
    os.makedirs(PNG, exist_ok=True)
    os.makedirs(PRINT, exist_ok=True)
    narrow_footer(fig)
    fit_footer(fig)
    out = []
    for path, dpi in ((os.path.join(PNG, name + ".png"), 150),
                      (os.path.join(PRINT, name + ".png"), 300),
                      (os.path.join(PRINT, name + ".svg"), None)):
        kw = dict(bbox_inches="tight", pad_inches=pad, facecolor=C["surface"])
        if dpi:
            kw["dpi"] = dpi
        fig.savefig(path, **kw)
        out.append(path)
    for p in out:
        print("  wrote %s" % os.path.relpath(p, REPO))
    plt.close(fig)
    return out
