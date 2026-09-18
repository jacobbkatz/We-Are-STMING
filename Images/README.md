# What is in this folder, and what is NOT ours

**Read this before using any image here in anything that represents this project.**

## `Images/*.bmp` and `*.jpg` — MECH PANDA'S SCANS. NOT OUR DATA.

| File | What it is |
|---|---|
| `image_adc_1691722949755.bmp` | Atomic-resolution HOPG scan |
| `image_adc_1691722949755.jpg` | The same scan, JPEG |
| `image_adc_1691787217383_high_res.bmp` | Atomic-resolution HOPG scan, higher resolution |

**They are genuine atomic-resolution images** — opened and checked 2026-09-06, showing the hexagonal
HOPG lattice with visible creep at the start of each scan line and a shear across the frame
(`docs/INDEX.md`).

**They were produced by Mech Panda's instrument, not ours.** Their filenames carry
epoch-millisecond timestamps that decode to **2023-08-11** — **two and a half years before this
project began in July 2026.** They arrived with the upstream design as reference material and have
been in the repository since its first commit.

> ### This has now been asked twice, so it is written here rather than only in `docs/INDEX.md`.
>
> **2026-09-16:** they were considered for `docs/progress.html` and **deliberately left out**,
> because *"putting them on a page about our achievements would have read as our result"*
> (`sessions/2026-09-16-showcase.md`).
>
> **2026-09-18:** asked again, as *"those 3 images we had during the first run"*. **There was no
> such run.** They predate the project.

**Never put them in a progress page, a showcase, a report, a poster, an application or a
presentation about this project.** They are somebody else's result, at a resolution this instrument
has not yet reached, and presenting them as ours would read as fabrication to anyone who checked.

**Citing them as Mech Panda's reference work, clearly labelled, is fine and is good practice** —
that is what they are for.

## `Images/ours/` — our own hardware

Photographs of this instrument. See [`ours/README.md`](ours/README.md), which also records what has
been read off them and what has deliberately **not** been.

## Our own data

**This project has produced no image of a surface.** What it has produced is measurement data —
scans, sweeps, spectra — committed as CSV and log files under `sessions/data/`, with the analysis
that reads them. `STATUS.md` is the live record of what has and has not been achieved.
