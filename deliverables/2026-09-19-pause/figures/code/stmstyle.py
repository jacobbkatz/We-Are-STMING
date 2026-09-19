"""The shared visual system for the 2026-09-19 pause-point presentation figures.

Every figure in `deliverables/2026-09-19-pause/figures/` imports this module and
nothing else for its look. One place to change typography, colour, grid weight and
export sizes, so all the figures read as coming from one instrument.

The palette is the validated default from the `dataviz` skill's `references/palette.md`
and was re-checked here with that skill's own validator; the results are recorded in
`../STYLE.md`. Do not add a hue by eye: run the validator.

NOTHING IN THIS FILE IS A PROJECT CONSTANT. Every measured number lives in
`docs/FACTS.md` or in the raw file the figure cites. This module knows about colour and
type only.

Run any figure script from the repository root, e.g.

    python3 deliverables/2026-09-19-pause/figures/code/fig01_calibration.py
"""
from __future__ import annotations

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

# ---------------------------------------------------------------- paths

HERE = os.path.dirname(os.path.abspath(__file__))
FIGURES = os.path.dirname(HERE)                       # .../figures
PAUSE = os.path.dirname(FIGURES)                      # .../2026-09-19-pause
REPO = os.path.abspath(os.path.join(PAUSE, "..", ".."))
DATA = os.path.join(REPO, "sessions", "data")
PNG = os.path.join(FIGURES, "png")
PRINT = os.path.join(FIGURES, "print")


def data_path(session: str, name: str) -> str:
    """A file under sessions/data/<session>/. READ ONLY - never written by this code."""
    return os.path.join(DATA, session, name)


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
    # Sequential blue ramp, steps 100..700
    ramp=["#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7",
          "#3987e5", "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b"],
)

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

# Status palette - fixed, never themed, and never used for "series 4".
# Always shipped with a word beside it, never colour alone.
STATUS = dict(good="#0ca30c", warning="#fab219", serious="#ec835a", critical="#d03b3b")

# The active theme. set_theme() swaps it.
C = dict(LIGHT)
_THEME = "light"


def series(i: int) -> str:
    """Categorical slot i (0-based), in fixed order. Never cycled past 8."""
    if i >= len(C["series"]):
        raise IndexError(
            "slot %d: the palette stops at 8 by design. Fold the tail into 'Other' "
            "or facet into small multiples - never generate a 9th hue." % i)
    return C["series"][i]


# ---------------------------------------------------------------- typography
#
# One scale, used everywhere. Sizes are points at the figure's own scale, so a
# figure exported 8 in wide prints these sizes literally.

TYPE = dict(title=13, subtitle=10.5, label=10, tick=9.5, annot=9.5, small=8.5, hero=34)

FONT = ["DejaVu Sans", "Liberation Sans", "sans-serif"]


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
        "font.family": "sans-serif",
        "font.sans-serif": FONT,
        "font.size": TYPE["label"],
        "figure.facecolor": C["surface"],
        "savefig.facecolor": C["surface"],
        "axes.facecolor": C["surface"],
        "axes.edgecolor": C["axis"],
        "axes.linewidth": 0.8,
        "axes.labelcolor": C["ink2"],
        "axes.labelsize": TYPE["label"],
        "axes.titlesize": TYPE["subtitle"],
        "axes.titlecolor": C["ink"],
        "axes.titlelocation": "left",
        "axes.titlepad": 8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": C["grid"],
        "grid.linewidth": 0.8,
        "grid.linestyle": "-",          # solid hairline. Never dashed.
        "grid.alpha": 1.0,
        "xtick.color": C["muted"],
        "ytick.color": C["muted"],
        "xtick.labelcolor": C["ink2"],
        "ytick.labelcolor": C["ink2"],
        "xtick.labelsize": TYPE["tick"],
        "ytick.labelsize": TYPE["tick"],
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
        "lines.linewidth": 2.0,          # 2px lines
        "lines.solid_capstyle": "round",
        "lines.solid_joinstyle": "round",
        "lines.markersize": 5,           # >= 8 px diameter
        "patch.linewidth": 0.0,
        "figure.dpi": 150,
        "svg.fonttype": "path",
    })


set_theme("light")


# ---------------------------------------------------------------- figure furniture

def make_fig(width=8.0, height=5.0, nrows=1, ncols=1, **kw):
    """A figure plus axes with the house style already applied."""
    fig, ax = plt.subplots(nrows, ncols, figsize=(width, height), **kw)
    return fig, ax


def titles(fig, title, subtitle=None, y=0.985):
    """Figure title (what the chart says) and subtitle (how to read it).

    The title is a sentence, not a label. A reader who reads only the title should
    come away with the finding, not the variable names.
    """
    fig.text(0.008, y, title, ha="left", va="top",
             fontsize=TYPE["title"], fontweight="bold", color=C["ink"])
    if subtitle:
        fig.text(0.008, y - 0.052, subtitle, ha="left", va="top",
                 fontsize=TYPE["subtitle"], color=C["ink2"])


def footer(fig, text, y=0.012):
    """Provenance line: source file, measurement date, and what the figure is not."""
    fig.text(0.008, y, text, ha="left", va="bottom",
             fontsize=TYPE["small"], color=C["muted"], linespacing=1.5)


def note(ax, x, y, text, **kw):
    """An annotation in ink, never in a series colour."""
    kw.setdefault("fontsize", TYPE["annot"])
    kw.setdefault("color", C["ink2"])
    return ax.text(x, y, text, **kw)


def tidy(ax, xlabel=None, ylabel=None, title=None, grid="y"):
    """Axis labels (with units - always), a left-set axis title, and one grid direction."""
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
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

    Uses the typographic minus (U+2212), matching matplotlib's own default, so a
    negative tick does not sit next to a shorter hyphen elsewhere on the figure.
    """
    f = FuncFormatter(lambda v, _: format(int(round(v)), ",").replace("-", "−"))
    if which in ("y", "both"):
        ax.yaxis.set_major_formatter(f)
    if which in ("x", "both"):
        ax.xaxis.set_major_formatter(f)


def ring(marker_artists):
    """The 2px surface ring that keeps overlapping dots legible."""
    for a in marker_artists:
        a.set_markeredgecolor(C["surface"])
        a.set_markeredgewidth(2.0)


def dot(ax, x, y, color, size=7, z=5):
    """A single data dot with the surface ring already on it."""
    return ax.plot(x, y, "o", color=color, markersize=size,
                   markeredgecolor=C["surface"], markeredgewidth=2.0, zorder=z)


# ---------------------------------------------------------------- export

def save(fig, name, pad=0.28):
    """Write screen and print copies.

    png/<name>.png     150 dpi, for a screen or a slide
    print/<name>.png   300 dpi, for a 48 x 36 in poster
    print/<name>.svg   vector, for anything that will be scaled further

    Both carry the same pixels of layout, so a caption written against one is true of
    the other.
    """
    os.makedirs(PNG, exist_ok=True)
    os.makedirs(PRINT, exist_ok=True)
    out = []
    screen = os.path.join(PNG, name + ".png")
    fig.savefig(screen, dpi=150, bbox_inches="tight", pad_inches=pad,
                facecolor=C["surface"])
    out.append(screen)
    hi = os.path.join(PRINT, name + ".png")
    fig.savefig(hi, dpi=300, bbox_inches="tight", pad_inches=pad,
                facecolor=C["surface"])
    out.append(hi)
    vec = os.path.join(PRINT, name + ".svg")
    fig.savefig(vec, bbox_inches="tight", pad_inches=pad, facecolor=C["surface"])
    out.append(vec)
    for p in out:
        print("  wrote %s" % os.path.relpath(p, REPO))
    plt.close(fig)
    return out
