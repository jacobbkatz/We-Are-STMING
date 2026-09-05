# What other people building these have found

Searched 2026-09-05 for anyone replicating Mech Panda's STM, and for solutions to the questions
still open in `docs/OPEN_QUESTIONS.md`.

**Nothing here is our design or upstream's.** These are other people's choices, recorded because
several of them answer things nobody in our own lineage wrote down. Treat every item as a lead to
test, not a specification.

---

## 1. No public replication of Mech Panda's build was found

Searched for build logs, forum threads and repositories from anyone who has built the
`red-panda-stm` design. **None turned up.** What exists is the original video, the GitHub repo,
and coverage that describes rather than reproduces it.

Two consequences worth being clear about:

- **We may be the first people to build this from the files**, which is consistent with the repo
  having no BOM, no build tutorial, and no issues closed against these problems.
- **There is no community to check our findings against.** The DAC configuration loss, the
  ungrounded shield, the `CCON` jump — nobody else has reported any of them, and nobody else has
  ruled them out either.

That also means the corrections in this repository may be the only public record of them.

## 2. Piezo wiring: conductive epoxy instead of solder

The most useful thing found, because it addresses an UNKNOWN in our BOM and a hazard that has
already destroyed discs.

An independent DIY STM, [`jherkenhoff/STM`](https://github.com/jherkenhoff/STM), attaches wires to
the piezo quadrants with **conductive epoxy (MG Chemicals 9410)** rather than solder, specifically
to avoid depolarising the ceramic.

Corroborating this from piezo manufacturers' own handling guidance:

- **Depolarisation occurs if the internal buzzer temperature exceeds about 210 °C.**
- Manufacturers list conductive adhesive alongside soldering as a normal connection method, and
  note that epoxy takes longer to set but gives a good connection.
- Where soldering is used, low temperature and short dwell are the whole trick.

**How this bears on our build.** `docs/BOM.md` currently specifies Sn42/Bi58 low-temperature paste
at ~138 °C, on the reasoning that the original designer destroyed four or five discs by
overheating. That reasoning stands. Conductive epoxy is a **second option that removes the heat
entirely**, at the cost of cure time and a slightly more awkward joint.

Recorded, not adopted. **We have not tested it**, and our low-temp paste approach has not failed
yet — it simply has not been tried on a disc that survived.

## 3. Cutting the quadrants

Two independent descriptions of how the disc's top electrode is divided into four:

- **Scalpel**, carefully scraping the upper silver electrode into four segments without damaging
  the ceramic beneath (`jherkenhoff/STM`).
- **Ruler and razor blade** to cut the silver into four equal quadrants; **the white ceramic layer
  underneath does not need to be cut** (descriptions of John Alexander's original unimorph disc
  scanner, which is where this whole scanner design originates).

Berard, asked about using a Dremel for this, replied that a Dremel would be difficult without a
jig and that **a diamond scribe works a little better than an X-acto knife**.

**Only the electrode is cut, not the ceramic.** That is the part worth knowing before anyone
presses too hard.

## 4. A standoff chosen for resistivity

`jherkenhoff/STM` uses a **10 mm ceramic standoff (Essentra Components CER-3)** under the piezo,
chosen explicitly for high resistivity to reduce tunneling-current leakage.

That is the same reasoning behind our PTFE standoff (Keystone 11301, from Berard). Two independent
builds arriving at "insulate the input node on a deliberately high-resistivity post" is worth
noting given that **surface leakage is currently our blocking fault.**

## 5. Vibration isolation: Viton keeps coming up

- `jherkenhoff/STM`: a stack of steel plates (15 mm, 12 mm, 8 mm, all 100 mm diameter) separated
  by **Viton O-rings**, on a 150 mm aluminium baseplate, targeting a resonance of a few Hz.
- Berard: three 5" × ½" steel plates separated by **three small pieces of Viton cut from an
  O-ring**, on MDF and aluminium, suspended on three 2 ft springs.

Our design uses springs and eddy-current damping and does not use Viton anywhere. **Not a
correction** — just a note that two other builds independently reached for the same material for
the plate stack, if damping ever turns out to be a problem.

## 6. Scanner origin

The unimorph disc scanner is **John Alexander's** invention, not Berard's and not Mech Panda's.
Berard credits him directly. Alexander's original page is the source for the quadrant-cutting
method and the disc scanner geometry, and is the upstream of our upstream's upstream.

Worth knowing if a scanner question ever outruns what Berard documented.

---

## Sources

- [`jherkenhoff/STM`](https://github.com/jherkenhoff/STM) — independent DIY STM, BeagleBone-based
- [Dan Berard, Home-Built STM](https://dberard.com/home-built-stm/) — and his comment replies
- Piezo handling guidance from PI, Piezo.com, APC International and Sonitron on depolarisation
  temperature and conductive-adhesive attachment
- [Hackaday's coverage of Mech Panda's build](https://hackaday.com/2024/09/30/building-a-3d-printed-scanning-tunneling-microscope/)
  — **blocked by this environment's network proxy**, so its comment thread has not been read. It
  is the most likely place for replication reports and is worth someone opening by hand.
