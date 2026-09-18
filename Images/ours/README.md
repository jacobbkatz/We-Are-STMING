
## 2026-09-18 — the rebuilt tip holder and the scan head face

Sent by Jacob from the bench, taken to settle **d**, the distance from the line through the two
side-by-side ball ends to the tip. **They are our own hardware** (`SAID`, Jacob, taken at his bench
the same evening).

| File | What it shows |
|---|---|
| `2026-09-18_scanhead_side.jpg` | Side view. The copper-taped preamp box above, the aluminium-taped head, the ball-end screws protruding, the copper-covered base plate |
| `2026-09-18_scanhead_face_1..4.jpg` | The head face straight on: the piezo disc recessed in its bore, the tip at the disc centre, the tip lead crossing the face, and three ball-end screws |

**Nothing has been read off these as a measurement.** `CLAUDE.md` is explicit that a photograph is
not a measurement of our hardware, after the 2026-09-09 session read a part marking off a shared
photo and edited five documents before asking whose board it was. Repeated by-eye estimates of d
from these frames spread over about ±1 mm, which is the same size as the quantity, so **no value
for d has been written into `docs/FACTS.md` or `docs/INVENTORY.md` from them.**

**Two things must be confirmed by Jacob before any number is taken from these:**

1. **Which two ball ends are the side-by-side pair.** Read from the frames as the TOP and BOTTOM
   ones, with the motor screw on the RIGHT — so the pivot line runs vertically in this view. If that
   is wrong, every distance taken from these photos is wrong.
2. **How far the tip protrudes from the face, against how far the ball ends stand proud.** The balls
   stand well clear of the face and the tip sits recessed inside the bore. The old tip stuck out
   **about 1.8 cm** (`docs/INVENTORY.md`); the tip in these frames looks far shorter, but it may
   simply be pointing at the camera. **If the tip now sits behind the plane of the three ball ends,
   the sample plate rests on the balls and can never reach it.**

### 2026-09-18: d CANNOT be measured from these photographs. Three attempts, three answers.

**Jacob confirmed the layout** (`SAID` 2026-09-18): the TOP and BOTTOM ball ends are the
side-by-side pair, so the pivot line runs vertically in these frames, and the motor screw is the
one on the RIGHT. That part is settled and is safe to rely on.

**Measuring d from the frames was then tried three times and failed three times:**

| Attempt | Method | Disc diameter it gave |
|---|---|---|
| 1 | By eye off a 50 px grid, cropped near the bore | ~425 px |
| 2 | By eye off a 100 px grid, whole face | ~210 px |
| 3 | Colour detection of the brass disc, `numpy` | 687 to 725 px, and inconsistent across the four frames |

**A factor of more than two between attempts.** The by-eye readings disagreed with each other, and
the automatic one caught the warm-lit aluminium foil along with the brass because the whole scene is
copper-toned. **No value for d has been taken from these photographs and none should be.**

**Four reasons it cannot work, recorded so nobody tries again:**

1. **The tip is not a point.** It is a substantial soldered structure inside the bore, clearly
   offset from the disc centre, and **which feature is the working tip cannot be told from the
   image.** Two candidates were marked and sent to Jacob as A and B; they sit on opposite sides of
   the disc centre and several millimetres apart.
2. **The scene has no colour contrast.** Brass disc, aluminium tape and copper tape under warm light
   all sit in the same hue band.
3. **The depth defeats the perspective.** The ball ends stand proud toward the camera and the tip is
   recessed in the bore. With about 15 mm between them, the camera must be square to **half a
   degree** for the apparent offset to stay under 0.13 mm. No hand-held photograph is that square.
4. **The threshold is 3 pixels.** Tunnelling needs d under about 0.13 mm, and the scale here is
   roughly 0.04 mm per pixel.

**What to ask instead, and it takes a minute at the bench:** which feature is the tip, and **how far
is it from the centre of the brass disc**, by ruler or caliper against the disc rim. Both are at the
same depth, so that measurement has none of the problems above, and the CAD already fixes the disc
centre at **1.000 mm** from the pivot line (`docs/FACTS.md`, piezo pocket offset, MESH). d then
follows.
