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

WHICH PARTS, and a mistake made twice. Twelve of them are on the 3MF plates in
CAD/prints/print-plates/. The enclosures are not on any of those plates, and on
2026-09-20 that was read as "they were never printed" and they were all dropped.
THAT WAS WRONG, and the photographs say so plainly: the copper-taped preamp box,
the Faraday shield cover held in one hand, the controller in its box and the Teensy
in its printed tray are all in Images/ours/. A plate file is not an inventory.

What Jacob actually caught the first time was that the model showed
`4_scanhead_box`, which CAD/prints/README.md calls the REJECTED alternative - its
corner ears are 142.8 mm and the shield cover's outside is 142.00 mm, so it does not
even fit. The fix was to swap it for `6_shield_cover`, not to delete the enclosures.
`4_scanhead_box_base` and `4_scanhead_box_lid` are the only two printable files in
this repository that are deliberately NOT here.

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

# Sizes and descriptions come from CAD/prints/README.md and docs/. Nothing is invented.
# The twelve scan-head and isolation parts are evidenced by the 3MF plates in
# CAD/prints/print-plates/. The enclosures are evidenced by the photographs of them in
# Images/ours/ and by Jacob, 2026-09-20. `4_scanhead_box` is excluded: README.md calls
# it the rejected alternative and it does not fit inside the shield cover.
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

    ("enclosures", "6_shield_cover.stl", "Shield cover",
     "The Faraday shield that drops over the whole scanning module, 142 by 128 by "
     "112 mm. Wrapped in copper tape and grounded at one point. This is the one in "
     "the photograph being held in one hand."),
    ("enclosures", "5_intermediate_baseplate.stl", "Intermediate base plate",
     "Fits the 131 by 101 mm opening in the shield frame, under the scan head."),
    ("enclosures", "1_preamp_box_base.stl", "Preamp box",
     "The small box around the preamplifier board alone, 35 by 29 by 21 mm. The "
     "board inside it is 20.6 by 15.2 mm. Ours: the same two files are in "
     "our_preamp_cad_files/."),
    ("enclosures", "1_preamp_box_lid.stl", "Preamp box lid",
     "Screwed down with M2. The lid has the clearance hole and the base has a "
     "narrower pillar the screw cuts its own thread into, which is how every box "
     "here closes."),
    ("enclosures", "2_controller_box_base.stl", "Controller box",
     "Holds the controller PCB with the four converters on it, 129 by 114 by 40 mm."),
    ("enclosures", "2_controller_box_lid.stl", "Controller box lid",
     "M3, self-tapping into the base posts."),
    ("enclosures", "3_teensy_protoboard_box_base.stl", "Teensy box",
     "Holds the Teensy 4.1 on its hand-wired protoboard carrier, 90 by 110 by 42 mm. "
     "The yellow 26-way ribbon leaves it for the controller box."),
    ("enclosures", "3_teensy_protoboard_box_lid.stl", "Teensy box lid",
     "M3, self-tapping. Ø3.4 clearance in the lid, Ø2.5 pillar in the base."),
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
