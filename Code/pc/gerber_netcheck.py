#!/usr/bin/env python3
"""Check, from the gerber files alone, that every pad is joined by copper to its own net and to no other.

Why this exists: the preamp boards JLCPCB built (rev 1) were made from gerbers whose ground fill was
never filled. Their X2 net labels still said GND on every ground pad, so every document believed the
grounds were connected -- six of them were not (STATUS.md fault 0d). A net LABEL is the intended net;
this tool checks the COPPER, which is what the factory actually makes.

How: draw each copper layer as a picture (0.02 mm per pixel), find the separate islands of copper,
join the two layers wherever there is a plated hole, then ask for every net named in the X2 pad
attributes:
  * OPEN  -- are all of its pads on one island?           (rev 1 fails this for GND)
  * SHORT -- does any island carry pads of two nets?

Usage:
    python3 Code/pc/gerber_netcheck.py <directory or .zip of gerbers>
    python3 Code/pc/gerber_netcheck.py --test        # proves it goes red on rev 1 and green on a fix

Exit code 0 = every net whole and no shorts. 1 = a fault. 2 = could not read the files.

Needs numpy and Pillow. Handles what KiCad writes: C/R/O/P apertures, aperture macros made of
primitives 1, 4, 5, 20, 21, linear and circular draws, regions (G36/G37) and LPD/LPC polarity.
"""
import io
import math
import re
import sys
import zipfile
from collections import defaultdict, deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

PX_PER_MM = 50          # 0.02 mm per pixel; the tightest clearance on these boards is 0.2 mm = 10 px
MARGIN_MM = 1.0


# ---------------------------------------------------------------------------------------------
# Reading the files
# ---------------------------------------------------------------------------------------------

def load_files(src):
    """Return {filename: text} from a directory or a zip."""
    src = Path(src)
    out = {}
    if src.is_dir():
        for p in src.iterdir():
            if p.is_file():
                out[p.name] = p.read_text(errors="replace")
    elif zipfile.is_zipfile(src):
        with zipfile.ZipFile(src) as z:
            for n in z.namelist():
                if not n.endswith("/"):
                    out[Path(n).name] = z.read(n).decode(errors="replace")
    else:
        raise FileNotFoundError(f"not a directory or zip: {src}")
    return out


def file_function(text):
    m = re.search(r"%TF\.FileFunction,([^*]*)\*%", text)
    return m.group(1) if m else ""


def pick_layers(files):
    """Find the front copper, back copper and drill files, by X2 file function, then by name."""
    front = back = None
    drills = []
    for name, text in files.items():
        ff = file_function(text)
        low = name.lower()
        if ff.startswith("Copper") and ff.endswith("Top") or low.endswith(("f_cu.gbr", ".gtl")):
            front = name
        elif ff.startswith("Copper") and ff.endswith("Bot") or low.endswith(("b_cu.gbr", ".gbl")):
            back = name
        elif low.endswith((".drl", ".xln")) or "M48" in text[:200]:
            drills.append(name)
    if not (front and back and drills):
        raise ValueError(f"need front copper, back copper and a drill file; found {front}, {back}, {drills}")
    return front, back, drills


# ---------------------------------------------------------------------------------------------
# Aperture macros
# ---------------------------------------------------------------------------------------------

def eval_expr(expr, params):
    expr = expr.strip().replace("x", "*").replace("X", "*")
    expr = re.sub(r"\$(\d+)", lambda m: repr(params.get(int(m.group(1)), 0.0)), expr)
    if not re.fullmatch(r"[0-9eE.+\-*/() ]*", expr):
        raise ValueError(f"unsafe macro expression {expr!r}")
    return float(eval(expr, {"__builtins__": {}}, {}))


def rot(pt, deg):
    a = math.radians(deg)
    x, y = pt
    return (x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a))


def macro_shapes(body, args):
    """Return a list of (exposure, polygon-in-mm) for one instance of a macro."""
    params = {i + 1: v for i, v in enumerate(args)}
    shapes = []
    for block in body:
        block = block.strip()
        if not block or block.startswith("0"):
            continue
        if "=" in block and block.startswith("$"):
            k, v = block.split("=", 1)
            params[int(k[1:])] = eval_expr(v, params)
            continue
        f = [eval_expr(t, params) for t in block.split(",")]
        code = int(f[0])
        if code == 1:                                   # circle: exp, dia, cx, cy[, rot]
            exp, d, cx, cy = f[1:5]
            r_ = f[5] if len(f) > 5 else 0.0
            cx, cy = rot((cx, cy), r_)
            shapes.append((exp, [(cx + d / 2 * math.cos(t), cy + d / 2 * math.sin(t))
                                 for t in np.linspace(0, 2 * math.pi, 48, endpoint=False)]))
        elif code == 4:                                 # outline: exp, n, x0,y0 ... xn,yn, rot
            exp, n = f[1], int(f[2])
            pts = [(f[3 + 2 * i], f[4 + 2 * i]) for i in range(n + 1)]
            r_ = f[3 + 2 * (n + 1)]
            shapes.append((exp, [rot(p, r_) for p in pts]))
        elif code == 5:                                 # polygon: exp, n, cx, cy, dia, rot
            exp, n, cx, cy, d, r_ = f[1], int(f[2]), f[3], f[4], f[5], f[6]
            pts = [(cx + d / 2 * math.cos(2 * math.pi * i / n), cy + d / 2 * math.sin(2 * math.pi * i / n))
                   for i in range(n)]
            shapes.append((exp, [rot(p, r_) for p in pts]))
        elif code == 20:                                # vector line: exp, w, x1, y1, x2, y2, rot
            exp, w, x1, y1, x2, y2, r_ = f[1:8]
            dx, dy = x2 - x1, y2 - y1
            L = math.hypot(dx, dy) or 1e-9
            nx, ny = -dy / L * w / 2, dx / L * w / 2
            pts = [(x1 + nx, y1 + ny), (x2 + nx, y2 + ny), (x2 - nx, y2 - ny), (x1 - nx, y1 - ny)]
            shapes.append((exp, [rot(p, r_) for p in pts]))
        elif code == 21:                                # centre line: exp, w, h, cx, cy, rot
            exp, w, h, cx, cy, r_ = f[1:7]
            pts = [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)]
            shapes.append((exp, [rot(p, r_) for p in pts]))
        else:
            raise ValueError(f"aperture macro primitive {code} is not supported")
    return shapes


# ---------------------------------------------------------------------------------------------
# Gerber interpreter
# ---------------------------------------------------------------------------------------------

class Layer:
    """Draws one gerber copper layer and remembers where each attributed pad sits."""

    def __init__(self, text, origin, size_px):
        self.img = Image.new("1", size_px, 0)
        self.draw = ImageDraw.Draw(self.img)
        self.origin = origin                      # (xmin, ymax) in mm
        self.pads = []                            # (net, component, pin, x_mm, y_mm)
        self._parse(text)

    def px(self, x, y):
        return ((x - self.origin[0]) * PX_PER_MM, (self.origin[1] - y) * PX_PER_MM)

    def _poly(self, pts, value):
        if len(pts) >= 3:
            self.draw.polygon([self.px(*p) for p in pts], fill=value)

    def _flash(self, ap, x, y, value):
        kind, args = ap
        if kind == "C":
            r = args[0] / 2
            self._poly([(x + r * math.cos(t), y + r * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 48, endpoint=False)], value)
        elif kind == "R":
            w, h = args[0] / 2, args[1] / 2
            self._poly([(x - w, y - h), (x + w, y - h), (x + w, y + h), (x - w, y + h)], value)
        elif kind == "O":
            w, h = args[0], args[1]
            r = min(w, h) / 2
            if w >= h:
                a, b = (x - w / 2 + r, y), (x + w / 2 - r, y)
            else:
                a, b = (x, y - h / 2 + r), (x, y + h / 2 - r)
            self._stroke(a, b, 2 * r, value)
        elif kind == "P":
            d, n = args[0], int(args[1])
            r_ = args[2] if len(args) > 2 else 0.0
            self._poly([(x + d / 2 * math.cos(math.radians(r_) + 2 * math.pi * i / n),
                         y + d / 2 * math.sin(math.radians(r_) + 2 * math.pi * i / n)) for i in range(n)], value)
        elif kind == "M":
            body, margs = args
            for exp, pts in macro_shapes(body, margs):
                self._poly([(x + px_, y + py_) for px_, py_ in pts], value if exp else 1 - value)
        else:
            raise ValueError(f"aperture type {kind} is not supported")

    def _stroke(self, a, b, width, value):
        """A straight draw with a round aperture: a rectangle with round ends."""
        (x1, y1), (x2, y2) = a, b
        r = width / 2
        L = math.hypot(x2 - x1, y2 - y1)
        if L > 1e-9:
            nx, ny = -(y2 - y1) / L * r, (x2 - x1) / L * r
            self._poly([(x1 + nx, y1 + ny), (x2 + nx, y2 + ny), (x2 - nx, y2 - ny), (x1 - nx, y1 - ny)], value)
        for cx, cy in (a, b):
            self._poly([(cx + r * math.cos(t), cy + r * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 32, endpoint=False)], value)

    @staticmethod
    def _arc_points(start, end, centre, clockwise):
        sx, sy = start
        ex, ey = end
        cx, cy = centre
        r = math.hypot(sx - cx, sy - cy)
        a0 = math.atan2(sy - cy, sx - cx)
        a1 = math.atan2(ey - cy, ex - cx)
        if clockwise:
            while a1 >= a0:
                a1 -= 2 * math.pi
        else:
            while a1 <= a0:
                a1 += 2 * math.pi
        if abs(a1 - a0) < 1e-9:
            a1 = a0 + (-2 if clockwise else 2) * math.pi
        n = max(8, int(abs(a1 - a0) / (2 * math.pi) * 64))
        return [(cx + r * math.cos(a0 + (a1 - a0) * i / n), cy + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(1, n + 1)]

    def _parse(self, text):
        fmt_div = 10 ** 6
        macros, apertures = {}, {}
        cur_ap, x, y = None, 0.0, 0.0
        interp, region, region_pts = "G01", False, []
        polarity = 1
        attrs = {}
        # Split into extended commands (%...%) and word commands (...*)
        tokens = re.findall(r"%[^%]*%|[^%*\n]+\*", text)
        for tok in tokens:
            tok = tok.strip()
            if tok.startswith("%"):
                body = tok[1:-1]
                if body.startswith("FS"):
                    m = re.search(r"X(\d)(\d)", body)
                    fmt_div = 10 ** int(m.group(2))
                elif body.startswith("MO") and "IN" in body:
                    raise ValueError("inch gerbers are not supported")
                elif body.startswith("AM"):
                    parts = [p for p in body.split("*") if p.strip()]
                    macros[parts[0][2:]] = parts[1:]
                elif body.startswith("AD"):
                    m = re.match(r"ADD(\d+)([A-Za-z_.$][A-Za-z0-9_.$]*),?([^*]*)\*", body)
                    code, name, rest = int(m.group(1)), m.group(2), m.group(3)
                    nums = [float(v) for v in rest.split("X") if v.strip()] if rest else []
                    if name in ("C", "R", "O", "P"):
                        apertures[code] = (name, nums)
                    elif name in macros:
                        apertures[code] = ("M", (macros[name], nums))
                    else:
                        raise ValueError(f"unknown aperture {name}")
                elif body.startswith("LP"):
                    polarity = 1 if body[2] == "D" else 0
                elif body.startswith("TO."):
                    k, _, v = body[3:].rstrip("*").partition(",")
                    attrs[k] = v.split(",")
                elif body.startswith("TD"):
                    k = body[2:].rstrip("*")
                    if k:
                        attrs.pop(k.lstrip("."), None)
                    else:
                        attrs.clear()
                continue
            word = tok[:-1]
            if word.startswith("G04") or word in ("M02", "M00", "M01"):
                continue
            if word == "G36":
                region, region_pts = True, []
                continue
            if word == "G37":
                self._poly(region_pts, polarity)
                region, region_pts = False, []
                continue
            if word in ("G74", "G75"):
                continue
            m = re.match(r"(G0[123])?(D\d+)?$", word)
            if m and (m.group(1) or m.group(2)) and not re.search(r"[XYIJ]", word):
                if m.group(1):
                    interp = m.group(1)
                d = m.group(2)
                if d and int(d[1:]) >= 10:
                    cur_ap = apertures[int(d[1:])]
                continue
            m = re.match(r"(G0[123])?(?:X(-?\d+))?(?:Y(-?\d+))?(?:I(-?\d+))?(?:J(-?\d+))?(D0[123])?$", word)
            if not m:
                raise ValueError(f"cannot read gerber word {word!r}")
            if m.group(1):
                interp = m.group(1)
            nx = int(m.group(2)) / fmt_div if m.group(2) is not None else x
            ny = int(m.group(3)) / fmt_div if m.group(3) is not None else y
            i_ = int(m.group(4)) / fmt_div if m.group(4) is not None else 0.0
            j_ = int(m.group(5)) / fmt_div if m.group(5) is not None else 0.0
            dcode = m.group(6) or "D01"
            if dcode == "D02":
                if region:
                    if len(region_pts) >= 3:
                        self._poly(region_pts, polarity)
                    region_pts = [(nx, ny)]
            elif dcode == "D01":
                if interp == "G01":
                    path = [(nx, ny)]
                else:
                    path = self._arc_points((x, y), (nx, ny), (x + i_, y + j_), interp == "G02")
                if region:
                    if not region_pts:
                        region_pts = [(x, y)]
                    region_pts.extend(path)
                else:
                    if cur_ap[0] != "C":
                        raise ValueError("draws with a non-circular aperture are not supported")
                    prev = (x, y)
                    for p in path:
                        self._stroke(prev, p, cur_ap[1][0], polarity)
                        prev = p
            elif dcode == "D03":
                self._flash(cur_ap, nx, ny, polarity)
                if "P" in attrs and "N" in attrs:
                    comp, pin = attrs["P"][0], attrs["P"][1] if len(attrs["P"]) > 1 else ""
                    self.pads.append((attrs["N"][0], comp, pin, nx, ny))
            x, y = nx, ny


def board_extent(texts):
    """A bounding box (mm) wide enough to hold every coordinate in every file."""
    xs, ys = [], []
    for text in texts:
        m = re.search(r"%FSLAX\d(\d)Y", text)
        div = 10 ** int(m.group(1)) if m else 10 ** 6
        for a, b in re.findall(r"X(-?\d+)Y(-?\d+)", text):
            xs.append(int(a) / div)
            ys.append(int(b) / div)
    return min(xs) - MARGIN_MM - 3, max(xs) + MARGIN_MM + 3, min(ys) - MARGIN_MM - 3, max(ys) + MARGIN_MM + 3


def plated_holes(text):
    """Return [(x, y)] of plated holes from an Excellon file (metric, decimal coordinates)."""
    tools_plated, cur_plated, holes = {}, True, []
    next_is_plated = True
    cur = None
    for line in text.splitlines():
        line = line.strip()
        if "TA.AperFunction" in line:
            next_is_plated = "NonPlated" not in line
            continue
        m = re.match(r"T(\d+)C([\d.]+)", line)
        if m:
            tools_plated[int(m.group(1))] = next_is_plated
            continue
        m = re.match(r"T(\d+)$", line)
        if m:
            cur = int(m.group(1))
            cur_plated = tools_plated.get(cur, True)
            continue
        m = re.match(r"X(-?[\d.]+)Y(-?[\d.]+)", line)
        if m and cur is not None and cur_plated:
            if "." not in m.group(1):
                raise ValueError("drill coordinates without a decimal point are not supported")
            holes.append((float(m.group(1)), float(m.group(2))))
    if "NPTH" in text and not any("TA.AperFunction" in l for l in text.splitlines()):
        raise ValueError("drill file marks NPTH without per-tool attributes; cannot tell plated holes apart")
    return holes


def label(mask):
    """Connected-component labels (4-connected) of a boolean array. 0 = no copper."""
    h, w = mask.shape
    lab = np.zeros((h, w), dtype=np.int32)
    n = 0
    ys, xs = np.nonzero(mask)
    for sy, sx in zip(ys, xs):
        if lab[sy, sx]:
            continue
        n += 1
        lab[sy, sx] = n
        q = deque([(sy, sx)])
        while q:
            cy, cx = q.popleft()
            for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
                if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not lab[ny, nx]:
                    lab[ny, nx] = n
                    q.append((ny, nx))
    return lab


class DSU:
    def __init__(self):
        self.p = {}

    def find(self, a):
        self.p.setdefault(a, a)
        while self.p[a] != a:
            self.p[a] = self.p[self.p[a]]
            a = self.p[a]
        return a

    def union(self, a, b):
        self.p[self.find(a)] = self.find(b)


def check(files, verbose=True):
    """Return (ok, report_lines, opens, shorts)."""
    front, back, drills = pick_layers(files)
    xmin, xmax, ymin, ymax = board_extent([files[front], files[back]])
    size = (int((xmax - xmin) * PX_PER_MM) + 1, int((ymax - ymin) * PX_PER_MM) + 1)
    layers = {"F": Layer(files[front], (xmin, ymax), size), "B": Layer(files[back], (xmin, ymax), size)}
    labs = {k: label(np.array(v.img, dtype=bool)) for k, v in layers.items()}
    dsu = DSU()

    def node_at(side, x, y):
        px_ = int(round((x - xmin) * PX_PER_MM))
        py_ = int(round((ymax - y) * PX_PER_MM))
        v = labs[side][py_, px_]
        return (side, int(v)) if v else None

    joined = 0
    for d in drills:
        for x, y in plated_holes(files[d]):
            a, b = node_at("F", x, y), node_at("B", x, y)
            if a and b:
                dsu.union(a, b)
                joined += 1

    by_net = defaultdict(set)          # net -> {(comp, pin)}
    pad_island = {}
    for side, layer in layers.items():
        for net, comp, pin, x, y in layer.pads:
            node = node_at(side, x, y)
            if node is None:
                continue
            pad_island[(comp, pin)] = dsu.find(node)
            by_net[net].add((comp, pin))

    lines = [f"front copper: {front}", f"back copper:  {back}", f"plated holes joining the layers: {joined}"]
    opens, shorts = [], []
    island_nets = defaultdict(set)
    for net, pads in sorted(by_net.items()):
        if net in ("", "N/C") or net.startswith("unconnected-") or net.startswith("Net-("):
            continue
        groups = defaultdict(list)
        for p in pads:
            groups[pad_island[p]].append(p)
            island_nets[pad_island[p]].add(net)
        names = lambda ps: ", ".join(f"{c} pin {n}" for c, n in sorted(ps))
        if len(groups) == 1:
            lines.append(f"  OK     {net}: {len(pads)} pads, one piece of copper")
        else:
            biggest = max(groups.values(), key=len)
            stray = [p for g in groups.values() if g is not biggest for p in g]
            opens.append((net, stray))
            lines.append(f"  OPEN   {net}: {len(pads)} pads in {len(groups)} separate pieces. "
                         f"Not joined to the main piece: {names(stray)}")
    for isl, nets in island_nets.items():
        if len(nets) > 1:
            shorts.append(sorted(nets))
            lines.append(f"  SHORT  one piece of copper carries {', '.join(sorted(nets))}")
    ok = not opens and not shorts
    lines.append("RESULT: " + ("PASS -- every net is one piece of copper, and no two nets touch" if ok else
                               f"FAIL -- {len(opens)} open net(s), {len(shorts)} short(s)"))
    return ok, lines, opens, shorts


def self_test(repo):
    """Red on rev 1 (the fabricated boards), green on rev 1 with its missing ground fill drawn back in."""
    rev1 = repo / "gerbers" / "STM_Preamp_OPA627_Gerbers(1).zip"
    files = load_files(rev1)
    ok, lines, opens, _ = check(files)
    stray = {f"{c} pin {p}" for net, ps in opens if net == "GND" for c, p in ps}
    expected = {"C2 pin -", "C3 pin 2", "C4 pin 2", "IC1 pin 3", "IC1 pin 8", "JP1 pin 4"}
    print("\n".join(lines))
    red = (not ok) and stray == expected
    print(f"\nSELF-TEST 1 (rev 1 must FAIL with exactly fault 0d's six ground points): {'PASS' if red else 'FAIL'}")
    if not red:
        print(f"  got stray GND pads: {sorted(stray)}")
    # Draw Berard's polygon back into rev 1's bottom copper as a region and check it goes green.
    front, back, _ = pick_layers(files)
    fixed = dict(files)
    poly = ("G36*\nX5727700Y304800D02*\nX20942300Y304800D01*\nX20942300Y15544800D01*\n"
            "X5727700Y15544800D01*\nX5727700Y304800D01*\nG37*\n")
    # Clear a 0.3 mm gap round every non-GND bottom pad first, as a real fill would.
    clear = "%LPC*%\n%ADD90O,3.648000X2.124000*%\nD90*\n"
    for y in (10160000, 7620000, 2540000):
        clear += f"X18732500Y{y}D03*\n"
    clear += "%ADD91C,2.200000*%\nD91*\nX13652500Y5715000D03*\n%LPD*%\n"
    redraw = "%ADD92O,3.048000X1.524000*%\nD92*\n"
    for y in (10160000, 7620000, 2540000):
        redraw += f"X18732500Y{y}D03*\n"
    redraw += "%ADD93C,1.600000*%\nD93*\nX13652500Y5715000D03*\n"
    fixed[back] = files[back].replace("M02*", poly + clear + redraw + "M02*")
    ok2, lines2, _, _ = check(fixed)
    print("\n".join(lines2[-8:]))
    print(f"SELF-TEST 2 (rev 1 with its ground fill restored must PASS): {'PASS' if ok2 else 'FAIL'}")
    # The same fill with NO clearance round the other pads floods +9V, -9V and the output: must be SHORT.
    flooded = dict(files)
    flooded[back] = files[back].replace("M02*", poly + "M02*")
    ok3, lines3, _, shorts3 = check(flooded)
    shorted = {n for s in shorts3 for n in s}
    red3 = (not ok3) and {"GND", "+9V", "-9V"} <= shorted
    print("\n".join(l for l in lines3 if "SHORT" in l or "RESULT" in l))
    print(f"SELF-TEST 3 (a fill touching the supply pads must report a SHORT): {'PASS' if red3 else 'FAIL'}")
    return red and ok2 and red3


def main(argv):
    repo = Path(__file__).resolve().parents[2]
    if len(argv) == 2 and argv[1] == "--test":
        return 0 if self_test(repo) else 1
    if len(argv) != 2:
        print(__doc__)
        return 2
    try:
        files = load_files(argv[1])
        ok, lines, _, _ = check(files)
    except (OSError, ValueError, KeyError) as e:
        print(f"could not check {argv[1]}: {e}")
        return 2
    print("\n".join(lines))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
