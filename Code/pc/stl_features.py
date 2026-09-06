#!/usr/bin/env python3
"""
Extract dimensions and hole patterns from the project's STL files.

Written because the printed parts' real geometry -- hole positions, diameters,
plate thicknesses -- existed only inside binary meshes and had never been
measured. `CAD/prints/README.md` carries the output.

    python3 Code/pc/stl_features.py                     # every part
    python3 Code/pc/stl_features.py CAD/prints/scan-head/BasePlate.stl

How it finds a hole. A hole through a printed part is a vertical cylindrical
wall, so its triangles all stand on end: their normals point sideways, with no
Z component. This walks the mesh, keeps only those side-facing triangles,
groups the ones that touch each other into surfaces, and fits a circle to each
surface. A real bore fits a circle with essentially zero error. A flat side of
the part, or a rounded corner, does not -- so it is thrown away.

Why it can be trusted: an STL's vertices sit exactly on the surface the CAD
tool exported, and the fit is least-squares over all of them. The BasePlate's
nine holes come back as 3.200 mm and 7.000 mm with a fit error of 0.0000. The
fit error is printed for every feature and is the number to look at before
quoting a diameter -- see the note printed after the results.

What it cannot see: holes drilled sideways (the axis has to be Z), and any
feature that is not round. Both come back as "no vertical circular features",
which means "not measured", never "not there".
"""

import math
import struct
import sys
import glob


# A triangle counts as a wall if its normal is this close to horizontal.
# 0.05 is about 3 degrees off vertical, which passes a printed bore's facets
# and rejects the near-flat surfaces some exporters produce.
WALL_NZ = 0.05


def read_facets(path):
    """Return a list of triangles, each ((x,y,z), (x,y,z), (x,y,z))."""
    data = open(path, 'rb').read()
    if data[:5].lower() == b'solid' and b'facet' in data[:2000]:
        verts = []
        for line in data.decode('ascii', 'replace').splitlines():
            p = line.split()
            if len(p) == 4 and p[0] == 'vertex':
                verts.append((float(p[1]), float(p[2]), float(p[3])))
        return [tuple(verts[i:i + 3]) for i in range(0, len(verts) - 2, 3)]
    count = struct.unpack('<I', data[80:84])[0]
    tris = []
    off = 84
    for _ in range(count):
        f = struct.unpack('<12f', data[off:off + 48])
        tris.append(((f[3], f[4], f[5]), (f[6], f[7], f[8]), (f[9], f[10], f[11])))
        off += 50
    return tris


def read_stl(path):
    """Every vertex, as (x, y, z)."""
    out = []
    for t in read_facets(path):
        out.extend(t)
    return out


def bbox(verts):
    xs = [v[0] for v in verts]
    ys = [v[1] for v in verts]
    zs = [v[2] for v in verts]
    return (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs))


def facet_normal(tri):
    """Unit normal from the vertices. The normal stored in the file is ignored,
    because exporters have been known to write zeros there."""
    (ax, ay, az), (bx, by, bz), (cx, cy, cz) = tri
    ux, uy, uz = bx - ax, by - ay, bz - az
    vx, vy, vz = cx - ax, cy - ay, cz - az
    nx = uy * vz - uz * vy
    ny = uz * vx - ux * vz
    nz = ux * vy - uy * vx
    mag = math.sqrt(nx * nx + ny * ny + nz * nz)
    if mag == 0.0:
        return None
    return (nx / mag, ny / mag, nz / mag)


def _solve3(m):
    """Gaussian elimination on a 3x4 augmented matrix. None if singular."""
    m = [row[:] for row in m]
    for i in range(3):
        piv = max(range(i, 3), key=lambda r: abs(m[r][i]))
        if abs(m[piv][i]) < 1e-12:
            return None
        m[i], m[piv] = m[piv], m[i]
        for r in range(3):
            if r != i:
                f = m[r][i] / m[i][i]
                for c in range(i, 4):
                    m[r][c] -= f * m[i][c]
    return [m[i][3] / m[i][i] for i in range(3)]


def lsq_circle(points):
    """Least-squares circle (Kasa). Returns (cx, cy, radius, max_residual).

    Why not just average the points and measure out from there: the centroid
    of a coarse polygon's vertices is not its centre, and being off by even
    0.1 mm smears one true diameter into a range of apparent ones. That is
    what made the preamp box lid look like a 1.9-to-2.7 mm hole when it is
    exactly 2.300. The residual is the honesty check -- a real circular
    feature fits to about zero.
    """
    n = len(points)
    if n < 3:
        return None
    sx = sy = sxx = syy = sxy = sxz = syz = sz = 0.0
    for p in points:
        x, y = p[0], p[1]
        z = x * x + y * y
        sx += x
        sy += y
        sxx += x * x
        syy += y * y
        sxy += x * y
        sz += z
        sxz += x * z
        syz += y * z
    sol = _solve3([[sxx, sxy, sx, sxz],
                   [sxy, syy, sy, syz],
                   [sx, sy, float(n), sz]])
    if sol is None:
        return None
    cx, cy = sol[0] / 2.0, sol[1] / 2.0
    under = sol[2] + cx * cx + cy * cy
    if under <= 0:
        return None
    r = math.sqrt(under)
    resid = max(abs(math.hypot(p[0] - cx, p[1] - cy) - r) for p in points)
    return cx, cy, r, resid


def max_angular_gap(points, cx, cy):
    """Largest empty angle around (cx, cy). A full bore is small, an arc large."""
    angles = sorted(math.atan2(p[1] - cy, p[0] - cx) for p in points)
    if len(angles) < 2:
        return 2 * math.pi
    gaps = [angles[i + 1] - angles[i] for i in range(len(angles) - 1)]
    gaps.append(angles[0] + 2 * math.pi - angles[-1])
    return max(gaps)


def wall_surfaces(tris, places=4, axis=2):
    """Split the triangles that stand parallel to `axis` into touching surfaces.

    axis is 0, 1 or 2 for X, Y or Z. A hole bored along that axis has walls
    whose normals have no component along it, so those are the triangles kept.

    Union-find over shared vertices. Two triangles join the same surface only
    if they share a corner, so a bore's wall and the outside of the part never
    merge -- which is exactly the failure that made an earlier version of this
    script miss every hole in the small boxes.
    """
    parent = {}

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    walls = []
    for t in tris:
        n = facet_normal(t)
        if n is None or abs(n[axis]) > WALL_NZ:
            continue
        keys = [(round(v[0], places), round(v[1], places), round(v[2], places))
                for v in t]
        for k in keys:
            parent.setdefault(k, k)
        union(keys[0], keys[1])
        union(keys[1], keys[2])
        walls.append((keys, t))

    groups = {}
    for keys, t in walls:
        groups.setdefault(find(keys[0]), []).extend(t)
    return list(groups.values())


AXIS_NAME = ('X', 'Y', 'Z')


def find_holes(source, min_pts=6, axis=2):
    """Circular features bored along `axis` (0=X, 1=Y, 2=Z; default Z).

    Returns (c1, c2, dia, lo, hi, fit_err), where c1/c2 are the centre in the
    two axes that are not `axis`, and lo/hi are the span along `axis`. For the
    default Z axis that reads as (cx, cy, dia, z_lo, z_hi, err).

    Takes a path, or the triangles from read_facets(). It needs triangles, not
    loose vertices, so a bare vertex list is refused rather than silently
    measured wrong.

    **Run all three axes before saying a part has no holes.** SamplePlate looks
    featureless on Z and has four bores on Y.
    """
    if isinstance(source, str):
        tris = read_facets(source)
    else:
        tris = list(source)
        if tris and not (isinstance(tris[0], (tuple, list)) and len(tris[0]) == 3
                         and isinstance(tris[0][0], (tuple, list))):
            raise TypeError("find_holes needs triangles from read_facets(), "
                            "not a flat vertex list")

    a, b = [i for i in (0, 1, 2) if i != axis]
    holes = []
    for pts in wall_surfaces(tris, axis=axis):
        uniq = sorted(set((round(p[a], 4), round(p[b], 4)) for p in pts))
        if len(uniq) < min_pts:
            continue
        fit = lsq_circle(uniq)
        if fit is None:
            continue
        ca, cb, r, resid = fit
        if r < 0.3 or r > 60:
            continue
        if resid > 0.02 * r + 0.02:
            continue                                   # not round
        if max_angular_gap(uniq, ca, cb) > math.pi / 2:
            continue                                   # an arc, not a bore
        along = [p[axis] for p in pts]
        holes.append((ca, cb, 2 * r, min(along), max(along), resid))
    holes.sort(key=lambda h: (-h[1], h[0], h[2]))
    return holes


def report(path):
    tris = read_facets(path)
    verts = [v for t in tris for v in t]
    x0, x1, y0, y1, z0, z1 = bbox(verts)
    print("=" * 72)
    print("%s" % path.split('/')[-1])
    print("  bounding box   %.2f x %.2f x %.2f mm   (%d triangles)"
          % (x1 - x0, y1 - y0, z1 - z0, len(tris)))
    print("  origin corner  X %.2f..%.2f   Y %.2f..%.2f   Z %.2f..%.2f"
          % (x0, x1, y0, y1, z0, z1))
    centre = ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)
    found_any = False
    for axis in (2, 0, 1):
        holes = find_holes(tris, axis=axis)
        if not holes:
            continue
        found_any = True
        a, b = [i for i in (0, 1, 2) if i != axis]
        an, bn, cn = AXIS_NAME[a], AXIS_NAME[b], AXIS_NAME[axis]
        print("  %d bores along %s (a stepped hole appears as two rows: same"
              % (len(holes), cn))
        print("  %s/%s, different diameter and span -- that is a counterbore):"
              % (an, bn))
        print("    %9s %9s %9s   %-14s %s"
              % (an, bn, "dia mm", cn + " span", "fit err"))
        for ca, cb, dia, lo, hi, resid in holes:
            print("    %9.2f %9.2f %9.3f   %-14s %.4f"
                  % (ca, cb, dia, "%.2f..%.2f" % (lo, hi), resid))
        # Offsets from the part centre, which is how the gotchas document
        # describes the BasePlate grid.
        print("    offsets from the part centre (%s %.2f, %s %.2f):"
              % (an, centre[a], bn, centre[b]))
        print("      %s: %s" % (an, sorted({round(h[0] - centre[a], 1) for h in holes})))
        print("      %s: %s" % (bn, sorted({round(h[1] - centre[b], 1) for h in holes})))
    if not found_any:
        print("  no circular features on any axis -- NOT MEASURED, which is not")
        print("  the same as 'no holes'. Non-round pockets are invisible here.")


def main(argv):
    paths = argv[1:] or sorted(glob.glob('CAD/prints/*/*.stl'))
    if not paths:
        print("No STLs found. Run this from the repository root.")
        return 1
    for p in paths:
        try:
            report(p)
        except Exception as e:
            print("%s: ERROR %s" % (p, e))
    print("=" * 72)
    print("Every feature above is a least-squares fit to vertices that sit on")
    print("the real surface, so a genuine bore reports its true diameter with a")
    print("fit error near zero -- the BasePlate reads 3.200 and 7.000 at 0.0000.")
    print("READ THE FIT ERROR COLUMN before quoting any number as a size.")
    print("Above about 0.01 mm, two features have merged into one measurement.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
