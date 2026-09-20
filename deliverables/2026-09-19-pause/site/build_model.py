#!/usr/bin/env python3
"""Pack the project's real printed-part meshes into one small file the website can draw.

    python3 deliverables/2026-09-19-pause/site/build_model.py

WHAT IT DOES, in plain language. `CAD/prints/` holds the 23 STL files we actually
printed the instrument from. This reads every one of them, shrinks the numbers so
they fit in a file small enough to publish, and writes them out as one file,
`model/parts.json`, with the geometry base64'd inside it. The page then draws them
in 3D and lets you spin them round and click one for its real measurements.

WHY ONE FILE. The publishing host serves a fixed list of file types and a raw `.bin`
is not one of them, so the vertices ride inside the JSON instead of beside it. It
costs a third more bytes and saves a round trip.

WHAT IT IS AND IS NOT. **Every shape here is the real printed part.** The POSITIONS
are not: the STL files are laid out for a printer, not for an assembly, and this
repository does not contain the assembly transforms. So the parts are arranged in
groups, deliberately spread out, and the page says so. Nothing here is a claim about
how far one part sits from another - only about what each part is and how big it is.

PRECISION. Vertices are stored as 16-bit integers with a scale factor per part, so
the worst error is about one part in 32,000 of that part's size - under 5 micrometres
on the largest piece here, far finer than the printer that made it.
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

# Group, display name, and what the part is. The descriptions come from
# CAD/prints/README.md and docs/; nothing here is invented.
PARTS = [
    ("scan-head", "BasePlate.stl", "Base plate",
     "The floor of the scan head. Everything else in the head is referenced to it, "
     "and it sits on the copper-covered plate you can see in the photographs."),
    ("scan-head", "PiezoPlate.stl", "Piezo plate",
     "Carries the piezo disc that moves the tip. Every scan on this page was made by "
     "bending this disc a few hundred converter counts at a time."),
    ("scan-head", "SamplePlate.stl", "Sample plate",
     "Holds the sample in front of the tip. On ours it was held on by two twisted "
     "rubber bands, which is the second row of what stopped us."),
    ("scan-head", "MotorSupport.stl", "Motor support",
     "Holds the 28BYJ-48 stepper that drives the coarse approach through a fine screw."),
    ("scan-head", "ThreadAdaptor.stl", "Thread adaptor",
     "Couples the stepper shaft to the fine screw. One turn of that screw is "
     "0.31750 mm, and one motor step is 1/2048 of a turn."),
    ("scan-head", "box_mount.stl", "Shield frame",
     "The frame the shield cover drops onto, 142 x 128 mm, the same footprint as the cover."),

    ("isolation", "new_body.stl", "Frame body",
     "The printed lower frame the whole instrument stands on."),
    ("isolation", "new_topframe.stl", "Top plate",
     "The plate at the top of the threaded columns. The suspension springs hang from it."),
    ("isolation", "Platform.stl", "Suspended platform",
     "The circular platform the scan head rides on, hanging on three springs. "
     "This is the part whose stillness the whole measurement depends on."),
    ("isolation", "Spring_hangers_and_extentions.stl", "Spring hangers",
     "The hangers and extensions the springs attach through."),
    ("isolation", "coin_weights.stl", "Coin weight holders",
     "Added mass for the platform. On the real instrument these were replaced by "
     "three paper quarter wrappers, which is one of the seven suspects for the drift."),
    ("isolation", "magnet_mount.stl", "Magnet mount",
     "Holds the eddy-current damping magnets under the platform."),

    ("enclosures", "6_shield_cover.stl", "Scan head shield",
     "142 x 128 x 112 mm. Drops over the whole scanning module and is copper taped, "
     "grounded at one point."),
    ("enclosures", "5_intermediate_baseplate.stl", "Intermediate base plate",
     "130 x 100 x 5 mm, fitting the 131 x 101 mm opening in the shield frame."),
    ("enclosures", "1_preamp_box_base.stl", "Preamplifier box",
     "35 x 29 x 21 mm, around one small PCB. The board inside is 20.6 x 15.2 mm. "
     "This is the box mounted as close to the tip as it physically fits."),
    ("enclosures", "1_preamp_box_lid.stl", "Preamplifier box lid", "Its lid."),
    ("enclosures", "1_preamp_box_base_v2_screwmount.stl", "Preamplifier box, screw mount",
     "A second version of the preamplifier box with a screw mount."),
    ("enclosures", "2_controller_box_base.stl", "Controller box",
     "129 x 114 x 40 mm, around the controller PCB with its four converters."),
    ("enclosures", "2_controller_box_lid.stl", "Controller box lid", "Its lid."),
    ("enclosures", "3_teensy_protoboard_box_base.stl", "Teensy box",
     "90 x 110 x 42 mm, around the Teensy 4.1 and its protoboard."),
    ("enclosures", "3_teensy_protoboard_box_lid.stl", "Teensy box lid", "Its lid."),
    ("enclosures", "4_scanhead_box_base.stl", "Scan head box (not used)",
     "130 x 134 x 88 mm. The alternative enclosure we did not use."),
    ("enclosures", "4_scanhead_box_lid.stl", "Scan head box lid (not used)", "Its lid."),
]


def read_stl(path: str) -> np.ndarray:
    """Triangle vertices from a binary STL, as (3n, 3) float32 in millimetres."""
    with open(path, "rb") as fh:
        blob = fh.read()
    n = struct.unpack("<I", blob[80:84])[0]
    if len(blob) != 84 + n * 50:
        raise SystemExit("%s is not a binary STL this script understands" % path)
    rec = np.frombuffer(blob, dtype=np.uint8, count=n * 50, offset=84).reshape(n, 50)
    # each 50-byte record: 3 floats of normal, 9 floats of vertices, 2 bytes spare
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
        # centre each part on its own middle, then quantise to int16
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
