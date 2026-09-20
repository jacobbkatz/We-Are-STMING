#!/usr/bin/env python3
"""Pack the project's real printed-part meshes into one small file the website can draw.

    python3 deliverables/2026-09-19-pause/site/build_model.py

WHAT IT DOES, in plain language. This reads the STL files for the twelve parts the
instrument was actually printed from, shrinks the numbers so they fit in a file
small enough to publish, and writes them out as one file,
`model/parts.json`, with the geometry base64'd inside it. The page then draws them
in 3D and lets you spin them round and click one for its real measurements.

WHY ONE FILE. The publishing host serves a fixed list of file types and a raw `.bin`
is not one of them, so the vertices ride inside the JSON instead of beside it. It
costs a third more bytes and saves a round trip.

WHICH PARTS. Only the twelve that appear in CAD/prints/print-plates/, which are the
plates the instrument was printed from. The enclosures in CAD/prints/enclosures/
belong to the upstream distribution and are not on any plate, so they are not shown:
the shield cover there is Mech Panda's, and on our instrument the shielding is
copper tape.

WHAT IT IS AND IS NOT. **Every shape here is a real printed part.** The POSITIONS
are not: the STL files are laid out for a printer, not for an assembly, and this
repository does not contain the assembly transforms. So the parts are arranged in
groups, deliberately spread out, and the page says so. Nothing here is a claim about
how far one part sits from another - only about what each part is and how big it is.

PRECISION. Vertices are 16-bit integers with a scale factor per part: worst error
about 5 micrometers on the largest piece, far finer than the printer that made it.
"""
from __future__ import annotations

import base64
import json
import os
import struct

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
PRINTS = os.path.join(ROOT, "CAD", "prints")
OUT = os.path.join(HERE, "model")

# Descriptions come from CAD/prints/README.md and docs/. Nothing here is invented.
# WHICH PARTS THESE ARE, and how we know. CAD/prints/print-plates/ holds the 3MF
# plates the instrument was actually printed from, and the object list inside them
# is the evidence: twelve distinct parts across five plates. The enclosures in
# CAD/prints/enclosures/ are the upstream distribution's and are NOT on any plate,
# so they are not here - Jacob, 2026-09-20: the shield cover in particular is Mech
# Panda's, not what is on our instrument, where the shielding is copper tape.
# Descriptions come from CAD/prints/README.md and docs/. Nothing here is invented.
PARTS = [
    ("scan-head", "BasePlate.stl", "Base plate",
     "The floor of the scan head. Everything else in the head is positioned from it, "
     "and it sits on the copper-covered plate you can see in the photographs."),
    ("scan-head", "PiezoPlate.stl", "Piezo plate",
     "Carries the piezo disc that moves the tip. Every scan on this page was made by "
     "bending this disc a few hundred converter counts at a time."),
    ("scan-head", "SamplePlate.stl", "Sample plate",
     "Holds the sample in front of the tip. On ours it was held on by two twisted "
     "rubber bands, which is the second row of what stopped us."),
    ("scan-head", "MotorSupport.stl", "Motor support",
     "Holds the stepper motor that drives the coarse approach through a fine screw."),
    ("scan-head", "ThreadAdaptor.stl", "Thread adaptor",
     "Couples the motor shaft to the fine screw. One turn of that screw is "
     "0.3175 mm, and one motor step is one 2,048th of a turn."),
    ("scan-head", "box_mount.stl", "Shield frame",
     "The frame a shield sits on, 142 by 128 mm. On our instrument the shielding "
     "itself is copper tape rather than a printed cover."),

    ("isolation", "new_body.stl", "Frame body",
     "The printed lower frame the whole instrument stands on."),
    ("isolation", "new_topframe.stl", "Top plate",
     "The plate at the top of the threaded columns. The suspension springs hang from it."),
    ("isolation", "Platform.stl", "Suspended platform",
     "The round platform the scan head rides on, hanging on three springs. This is "
     "the part whose stillness the whole measurement depends on."),
    ("isolation", "Spring_hangers_and_extentions.stl", "Spring hangers",
     "The hangers and extensions the springs attach through. Ten were printed."),
    ("isolation", "coin_weights.stl", "Coin weight holders",
     "Added mass for the platform. Three were printed. On the real instrument they "
     "were replaced by three paper quarter wrappers, which is one of the seven "
     "suspects for the drift."),
    ("isolation", "magnet_mount.stl", "Magnet mount",
     "Holds the eddy-current damping magnets under the platform."),
]


def read_stl(path: str) -> np.ndarray:
    """Triangle vertices from a binary STL, as (3n, 3) float32 in millimeters."""
    with open(path, "rb") as fh:
        blob = fh.read()
    n = struct.unpack("<I", blob[80:84])[0]
    if len(blob) != 84 + n * 50:
        raise SystemExit("%s is not a binary STL this script understands" % path)
    rec = np.frombuffer(blob, dtype=np.uint8, count=n * 50, offset=84).reshape(n, 50)
    # 50-byte record: 3 normal floats, 9 vertex floats, 2 spare
    verts = rec[:, 12:48].copy().view(np.float32).reshape(n * 3, 3)
    return np.asarray(verts, dtype=np.float64)


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    chunks, index, offset = [], [], 0
    for group, fname, name, blurb in PARTS:
        sub = {"scan-head": "scan-head", "isolation": "isolation",
               "enclosures": "enclosures"}[group]
        path = os.path.join(PRINTS, sub, fname)
        v = read_stl(path)
        lo, hi = v.min(axis=0), v.max(axis=0)
        size = hi - lo
        centre = (hi + lo) / 2.0
        local = v - centre
        scale = float(np.abs(local).max()) / 32000.0 or 1.0
        q = np.round(local / scale).astype(np.int16)
        chunks.append(q.tobytes())
        index.append({
            "name": name, "group": group, "file": "CAD/prints/%s/%s" % (sub, fname),
            "about": blurb,
            "tris": int(len(v) // 3), "offset": offset, "count": int(len(v)),
            "scale": scale,
            "size": [round(float(x), 2) for x in size],
        })
        offset += len(v)
    blob = b"".join(chunks)
    doc = {"parts": index, "vertices": offset,
           "note": ("Shapes are the real printed parts, read from the STL files in "
                    "CAD/prints/. Positions on screen are an arrangement, not an "
                    "assembly: this repository does not hold the assembly transforms."),
           "data": base64.b64encode(blob).decode("ascii")}
    path = os.path.join(OUT, "parts.json")
    json.dump(doc, open(path, "w"), separators=(",", ":"))
    old = os.path.join(OUT, "parts.bin")
    if os.path.exists(old):
        os.remove(old)
    print("%d parts, %d triangles, parts.json %.2f MB (geometry %.2f MB raw)"
          % (len(index), offset // 3, os.path.getsize(path) / 1e6, len(blob) / 1e6))


if __name__ == "__main__":
    main()
