# Draft reply to Dr. Percy Zahl

**Status: UNSENT. Written 2026-09-22 by Claude, for Jacob to cut and send under his own name.**

**Read this section before sending.**

- **Every number below traces to `docs/FACTS.md`, a session log, or `LEAD_VERIFICATION.md`**, and
  each was checked against its source while this was written.
- **One figure is deliberately vague** — the thermal sensitivity. It is a bracket, not a
  measurement, because two of its inputs are unknown (our filament's expansion coefficient, and how
  much printed material is in the loop). **It is written as a bracket in the letter too.** Do not
  tighten it before the datasheet is in hand.
- **Two things are asked of him.** Cut one if the letter feels long; the first is the more useful.
- **It is longer than his reply.** That is deliberate — he asked seven questions and most of them
  have answers, and an expert who gets a real answer usually gives another. **But if you would
  rather send four paragraphs, cut sections 2 and 4 and keep the rest.**

---

## The letter

Dear Dr. Zahl,

Thank you — this was more useful than you probably intended, because one of your suggestions put
back something we had dropped, and another produced a test we had not thought of.

Taking your questions in order.

**Is there anything 3D printed in the tip-sample loop?** Yes — essentially all of it. The path runs
tungsten tip, a soldered metal shaft, a cyanoacrylate joint, the brass piezo disc, two printed
plates, three steel ball-ended screws, the printed sample plate, copper tape, about 50 to 100
micrometres of backing paper, then the gold. The plates are PETG-CF, chosen over PLA for exactly
the reason you would expect, but they are still plastic.

**Soft materials and parts under load?** Three that concern us. The sample plate is held against
its three ball screws by rubber bands, twisted — one at the scan head end, two at the motor end.
The backing paper sits directly beneath the surface we are measuring. And the suspended platform
hangs on spring hooks sitting in eyebolts, which is metal sliding on metal under load and free to
stick and release. Your phrase about joints and stressed points creeping for a long time describes
the first and third of those precisely, and both are already on our candidate list.

**Is it a micrometer drive?** No. Coarse setting is by hand on two 1/4-80 screws, which is about
0.88 micrometres per degree of turn. The motorised axis is a 28BYJ-48 stepper on a screw — 155
nanometres of screw travel per step — reduced by a lever whose ratio is over 80, so under about 2
nanometres at the tip. The lever ratio is a bound rather than a number because the one distance it
depends on is still unmeasured; that measurement is now the first thing we do when we go back.

**Are the electrical signals stable in time?** Yes, and we can put a number on it rather than an
assurance. With the tip clear of the sample and the Z axis parked, the amplifier read between
minus 24 and plus 16 counts over eight minutes — about plus or minus 75 picoamps, against the
roughly 1 nanoamp we are looking for. It is worth being explicit about what the 43,000 counts
actually is, because it is not a drifting signal: we sweep the piezo and record the Z position at
which the current crosses a threshold, so it is a position measurement. Propagating that amplifier
offset through our own measured current-versus-Z slope, it could move the crossing point by about
60 counts. Against 43,000. So the electronics are not it.

**Piezo creep.** This is the part where you have earned your keep. It had been on our candidate
list in September and fell off when the list was rewritten, and nobody noticed. It also matters
more than an ordinary candidate would, because the piezo is the ruler — if its displacement per
count is itself drifting, we would see exactly this reading with a gap that never moved. We have
never measured our scanner's travel, linearity, hysteresis or creep. It is back on the list.

One piece of our own data cuts against it for the fastest motion, and you may find it interesting:
that 6.4-second excursion reverses direction and overshoots its own starting point. Creep and
settling decay one way. So creep after a step does not fit that particular event, though it is not
excluded for the slower ones, and thermal drift in a room does reverse as the heating cycles.

**The test your message produced.** We have 705 to 1,868 counts of hysteresis between going in and
coming out, at every bias we tried. We had only ever read that as a soft, pressed contact. Your
mentioning creep made us ask whether it is the scanner's own hysteresis instead — and the scanner
explains something the contact reading does not, which is that the hysteresis shows no trend with
bias. The discriminator is cheap: piezo hysteresis should scale with the size of the Z excursion
and contact compliance should not, so we will run the same in-and-out cycle at full, half and
quarter amplitude. It needs no new equipment.

**On temperature, you are right and we are not equipped.** We have never once logged the room
temperature beside a measurement, which in hindsight is an obvious gap. We are fixing the procedure
first: the instrument goes under an enclosure standing on the bench rather than on the suspended
platform, it sits for hours rather than the fifteen minutes we had planned, and we get something
that can log temperature unattended next to it.

The arithmetic supports your instinct, though I want to be honest that it is a bracket rather than
a number. Our entire Z travel is under about half a micrometre. Depending on how much unmatched
plastic is actually in the loop and what its expansion coefficient really is — we have not measured
either — something like half a kelvin to a couple of kelvin would walk the tip through the whole of
it. That is a wide bracket, but even its comfortable end says a tenth of a degree matters, which is
not a regime we have been treating with any respect.

Two things I would genuinely value your view on.

First: with a disc scanner and no position sensor, is there any practical way to separate the
scanner's own creep from real motion of the gap? Everything we can think of uses the piezo to
measure the piezo.

Second, and more bluntly: given the tip-sample loop is mostly printed plastic, is that
disqualifying for holding a junction, or is it a thermal design problem that can be engineered
around? We would rather hear that we need to rebuild the head in metal now than spend another two
months isolating our way toward a floor we cannot get under.

Thank you again — the systematic framing is what we were missing more than any single suspect.

Best,
Jacob Katz

---

## Sources for every figure in the letter, for checking

| In the letter | Value | Where it comes from |
|---|---|---|
| Loop materials and order | tungsten, stake, CA joint, brass disc, printed plates, steel balls, printed plate, copper tape, paper, gold | `docs/INVENTORY.md`, tip holder and sample plate rows |
| Backing paper thickness | 50 to 100 um | `docs/INVENTORY.md`, sample plate row |
| Print material | PETG-CF | `docs/FACTS.md`; `SAID` Jacob 2026-09-07 and again 2026-09-22 |
| Rubber band count and placement | 3, twisted 3 times: one at the head end, two at the motor end | `docs/INVENTORY.md`; `SAID` Jacob 2026-09-21 |
| Side screws | 1/4-80, 0.88 um per degree | `sessions/2026-09-19-morning.md` §3.2 |
| Motor screw travel | 155 nm per step | `docs/FACTS.md` |
| Lever ratio | over 80 | `docs/FACTS.md` — **a bound, from `d` under 0.5 mm** |
| Tip travel per motor step | **under** 1.94 nm | `docs/FACTS.md` — **a ceiling, not a value** |
| Amplifier stability, tip clear | −24 to +16 counts over 8.0 minutes | `sessions/2026-09-19-morning.md` §3.2, `creep_watch_run1.log` |
| Counts to picoamps | 3.125 pA per count | `docs/FACTS.md` |
| Arrival threshold | 300 counts, about 940 pA | `sessions/2026-09-19-morning.md` §3.2 |
| Current versus Z slope | a decade per ~1,800 Z counts | `docs/FACTS.md`, "The junction and the gap" |
| **60 counts** | **CALC 2026-09-22** | 75 pA on 940 pA is 0.033 decades; times 1,800 counts per decade |
| Gap motion | ≥ 43,000 counts in 6.4 s | `docs/FACTS.md` |
| Reversal and overshoot | the 6.4 s window reverses and overshoots its start | `deliverables/2026-09-19-pause/LEAD_VERIFICATION.md` V6 |
| In/out hysteresis | 705 to 1,868 counts, every bias, no V² trend | `docs/FACTS.md` |
| Scanner never characterised | travel, linearity, hysteresis, creep all unmeasured | `docs/ENGINEERING_REFERENCE.md` §12 |
| Z full range | under ~0.51 um | `docs/FACTS.md` — **a ceiling from our own geometry** |
| Thermal bracket | half a kelvin to a couple of kelvin | **CALC 2026-09-22, and NOT a measurement** — both inputs unknown. See `sessions/2026-09-22.md` §3 and §6 |

**No coefficient of thermal expansion appears in the letter as a number, on purpose.** The
manufacturer's datasheet could not be fetched from the container this was written in, and this
project has already taken three wrong web-sourced answers on one part number
(`CLAUDE.md` §7). **Get the parameter table before tightening that bracket.**
