# The five things that stood between this instrument and an image

**Written 2026-09-20, answering Jacob's question: "in this entire project what were the top five
things that held us back from an image, what needed to change?"**

**Ranked by how much each one actually blocked an image**, not by how much time went into it. Every
number traces to `docs/FACTS.md`, a session log, or `LEAD_VERIFICATION.md`.

---

## The short version — the five, and one possible fix each

| | What held us back | One possible fix |
|---|---|---|
| **1** | **The gap doesn't hold still** — ≥ 43,000 counts in 6.4 s with nothing moving. This is the blocker. **It is too slow to be vibration, so a better suspension is the wrong fix.** | **Box it and record for fifteen minutes before touching anything** — the cause is unknown among seven candidates, and the two cheapest to eliminate (room air, and the two unclamped cables running from the suspended platform to the fixed bench) cost nothing to test |
| **2** | **Soft sample** — gold leaf on backing paper, held by twisted rubber bands, and it moved when you blew on it | **Bond the gold to a rigid substrate with no paper under it, and clamp the plate mechanically instead of with rubber bands** |
| **3** | **Blunt tips, one bent** — while the etching setup already exists and has been used | **Etch a sharp tip with the setup you already own** |
| **4** | **No distance scale of your own** — section 3.25 records scans that covered ±0.6 nm, smaller than a single atom, and nobody could have known | **Measure `d` under a jeweller's loupe or a USB microscope** — minutes, no power, and it fixes the nanometre scale for every measurement this instrument will ever make |
| **5** | **The approach can't park in the window** — one motor step is at least 1.94 nm against a 0.17 nm window | **Settle the sign of the tunnelling current so `APRH` is safe to run, then hand the last stage of the approach from the motor to the piezo** |

**Each fix is one sentence because each is genuinely one action.** None of them needs a purchase and
none needs a laboratory. The rest of this document is the evidence behind each row.

---

## First, what was NOT the problem, because a lot of effort went there

**The electronics.** The measurement chain was proved against a known 100 MΩ resistor and agreed
with what Ohm's law required to **0.13 of a standard error** over 53 readings. The amplifier
resolves about **4 pA** of its own input current against the ~1 nA it has to find. With a live
junction the noise floor is **9 to 19 counts**, and a person stamping on the floor two metres away
moves one reading's spread from 131 to 132 pA.

**None of the five below is electronic.** Every one is mechanical, and that is worth knowing before
reading them: the part that is normally hardest for people doing this at home is the part that
works.

---

## 1. The gap does not hold still — and the motion is far too slow to be vibration

**The measurement.** With the motor stopped and nobody touching the instrument, only the piezo
sweeping: **≥ 43,000 Z counts in 6.4 seconds**, and **≥ 56,000 over about two minutes**. During
scans, **≥ 48,000 counts in 33 seconds**. The full Z range is 65,536 counts.

**An image needs the gap to stay inside a few hundred counts for a minute.** It was moving by most
of the range in seconds.

**This is the blocker, and everything else on this list is a candidate cause of it.**

> **The single most useful thing to understand about it: this is not vibration.** A 43,000-count
> excursion over 6.4 seconds is a slow, one-way movement. Acoustic and floor vibration are
> oscillations at tens of hertz — they would show as a band of jitter, not a march across the
> range. **So a better suspension is not the fix**, and `docs/NEXT_SESSION_PLAN.md` is right to say
> "do NOT add more mass": the height adjusters are already at maximum and another 0.8 to 1.2 kg
> buys 20% on the resonant frequency, for travel the instrument does not have. Chasing vibration
> would have been chasing the wrong physics.

**What it actually is: UNKNOWN, and SEVEN candidates have never been tested.** `STATUS.md` is the
canonical list and it grew on 2026-09-19 from four to seven:

1. the gold leaf on its paper
2. the sample plate on its rubber bands and ball contacts
3. thermal motion of the printed head
4. **air currents**
5. **the undressed cables** — an orange lead and a four-way bundle cross from the suspended platform
   to the fixed bench, and **no photograph shows either one clamped, taped or tied off.** A
   suspended stage is only as soft as its softest path to ground, and a cable is a path to ground —
   a nonlinear one, which can stick to the bench and then release
6. **the coin mass** — the wrappers stand tall and unrestrained on the platform, raising the centre
   of gravity and free to slide
7. **the spring-hook-in-eyebolt joints**

**Plus one that applies only to the 6.4-second excursion: relaxation after a motor move.** That
window opens 0.1 s after a 60-step retract ended — but the motion reverses and overshoots its
start, which relaxation does not do (`LEAD_VERIFICATION.md` V6).

> **Candidates 5 to 7 came from reading the photographs, and a photograph shows what is touching
> what, never what moved. None of the three is evidence.** They are things to look at during
> reassembly, not findings.

**Room air is the cheapest to test and has never been tried.** The cables are the second cheapest:
hang the platform, add a known small mass, and measure the droop with the cables connected and
again with them lifted clear.

**What needed to change:** a cardboard box over the instrument and a 15-minute recording, before
anything else. It costs nothing and it either eliminates air or promotes it to the leading
candidate. That test is first in the plan and has still not been run.

---

## 2. The sample was soft, unbonded, and held on with rubber bands

**A tunnelling gap is a fraction of a nanometre. Everything in the mechanical path has to be stiff
at that scale.** The sample path was not:

- **Gold leaf sitting on its backing paper** — roughly 50 to 100 micrometres of compressible
  cellulose **directly beneath the surface being measured**.
- **The leaf was not stuck down.** Jacob, after the 2026-09-18 session: the whole-plate sheet *"was
  moveing a bit if i blew on it"*. An unadhered leaf is also pulled toward the tip by the bias.
- **The plate is retained by two twisted rubber bands** hooked over screw heads.

**The measurements agree with this.** Pushing the tip in gave 23-28% of the predicted current
change while pulling out gave 40-71% — something absorbing the push. In and out did not retrace,
by 714 to 1,926 Z counts at every bias. **Both are what a compliant stack does and neither is what
a vacuum gap does.**

**What needed to change:** a rigid sample. Gold on a solid substrate or HOPG, bonded down with no
paper under it, and a mechanical retention that is not elastic. This is step 0 in the plan.

---

## 3. Every tip was a placeholder. One of them was bent

**From the record:** the tip fitted at ~03:00 on 2026-09-19 — *"new tip its gonna be very blunt but
that what we have for today"*. The one before it was **bent**, discovered only after a night of
measurements that were later re-read as the behaviour of a tip touching with its side.

**Why tip sharpness is not a detail here.** A tunnelling current should come from **one atom**. A
blunt tip presents many atoms in parallel, so the current is a sum over a patch, the distance
dependence flattens out, and the first thing to touch is a shoulder rather than a point. **A blunt
tip on a soft film produces exactly the pressed-contact signature that was measured** — the shallow
decay, the hysteresis, and the gradual onsets in 109 of 110 cycles.

**What needed to change:** etched tips, and this is the most fixable item on the list — **the
etching setup already exists and has been used.** There is a photograph of it running: a bench
supply through sodium hydroxide, outdoors, Jacob in chemical gloves. The capability was built and
then the bench sessions ran on blunt placeholders.

---

## 4. The instrument never had a distance scale of its own, so nobody knew how big a scan was

**The consequence, and it is the sharpest one on this list.** On 2026-09-17, after the Z scale was
re-derived mid-session, `sessions/2026-09-17-bench.md` §3.25 records that **every scan taken before
that point had covered about ±0.6 nm of sample — smaller than a single atom.**

**They were scanning a region smaller than the thing they were trying to image, and could not have
known.** The scans were then widened forty-fold.

**The root cause is one unmeasured distance:** `d`, how far the tip sits from the pivot line. It
sets the lever ratio between the coarse screw and the tip, and therefore nanometres per Z count.
Without it, every axis is in converter counts and no scan size means anything.

**What needed to change:** measure `d`. It needs a straightedge and no power. It was still not
measured when the instrument came apart; Jacob bounded it at **under 0.5 mm** on 2026-09-20, which
is a real constraint and not fine enough — the number that matters is nearer **26 micrometres** and
a straightedge cannot resolve that. **A jeweller's loupe or a USB microscope closes it in minutes.**

---

## 5. The coarse approach cannot stop inside the tunnelling window

**The arithmetic.** The window where a tunnelling current is big enough to see and small enough not
to saturate the amplifier spans about **1.7 decades of current — roughly 0.17 nm of gap.** One step
of the coarse motor moves the tip **at least 1.94 nm** — that is the figure at the TOP of the
range `d` has been bounded to, under 0.5 mm; `d` itself is still not resolved, and at the bottom
of that range the step is smaller. **The motor jumps
over the entire window in one step. There is no motor position inside it.**

That is not a fault, it is why the piezo exists — but it means the handover from motor to piezo has
to work, and it never did:

- **`APRH`, the automated approach, was never safe to run.** `approach()` compares `read_adc() >
  target` against a baseline that has been negative all project; if tunnelling drives the reading
  more negative it never triggers and the tip drives into the sample. **Safety rule 2, never
  lifted.** So every approach was done by hand.
- **The results, from the last session:** after every back-off the gold was **out of reach** at the
  first check; two 20-step motor finds located it and **neither held**; and +1,200 retract steps
  did not release a hard contact.

**What needed to change:** settle the sign of the tunnelling current so the automatic approach can
be trusted, and make the last stage of the approach a piezo approach with the motor stationary.

---

## The honest summary

**One sentence:** *the electronics were finished and the mechanics were not.*

**Two sentences:** the measurement chain was proved against theory, the amplifier resolves
picoamps, and a real tip-and-sample junction was made and characterised — **the instrument can
measure what it needs to measure.** What it cannot yet do is hold two pieces of metal a
half-nanometre apart for the length of a scan line, because the sample is soft, the tips are blunt,
the scale is unknown and the approach is too coarse to park in the right place.

**Ranked by cost to fix, cheapest first, which is nearly the reverse of the ranking above:**

| | Cost | Buys |
|---|---|---|
| Measure `d` with a loupe | minutes, no power | the nanometre scale for every future measurement, and it settles the 2026-09-17 junction retroactively |
| A box over the instrument, 15-minute recording | minutes, no power | eliminates or promotes air currents, the leading free candidate for the gap motion |
| Etch a sharp tip | an afternoon, with equipment already owned | the single biggest change to the junction's physics |
| A rigid, bonded sample | an afternoon | removes the compliance the push/pull and hysteresis measurements both point at |
| Piezo handover in the approach | firmware, and the current sign settled first | a gap that can be parked rather than crashed into |

**None of the five needs a purchase, and none of them needs a laboratory.**
