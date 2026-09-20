# LinkedIn post — drafts

**Written 2026-09-19 for Jacob.** Every number is from `docs/FACTS.md` or
`deliverables/2026-09-19-pause/LEAD_VERIFICATION.md`. **Nothing here claims an image or claims
tunnelling was demonstrated**, and the one genuinely open question is stated as open.

**Pick one, edit freely, post whichever sounds like you.** Suggested image: the photograph of you
holding the scanning module (`deliverables/2026-09-19-pause/photos/prepared/13_poster_module_portrait.jpg`),
or the signal-chain figure (`figures/png/fig07_signal_chain.png`) if you would rather lead with the
instrument than with a face.

---

## Draft A — the main one, ~200 words

> Two of us spent this summer building a scanning tunnelling microscope in a basement.
>
> Neither of us had written code before. Neither of us had really soldered before. We are both
> first-year students. The instrument sits on a wooden bench on a concrete floor, in a house where
> people walk around, with no control of the air — about as far from a clean room as you can get.
>
> It works. The amplifier resolves about 4 picoamps of its own input current. We put a known 100 MΩ
> resistor where the tip goes and swept it: the chain reported −3,205 ± 37 counts per volt against
> the −3,200 Ohm's law requires — agreement to 0.13 of a standard error, over 53 readings. We made a
> real tip-and-sample junction on gold leaf and measured a current that is not ohmic, is symmetric
> in both bias directions, and falls from 59 MΩ to 16 MΩ as the voltage rises. That rules out both a
> short circuit and an open one.
>
> We have not produced an image. What stops us is mechanical: with the motor off and nobody touching
> it, the gap moves by most of the piezo's range within seconds. We measured that, which is the part
> I am proudest of — we know exactly what is in the way.
>
> Everything is open: [repo link]

---

## Draft B — shorter, ~120 words, for a busier feed

> This summer two first-year students built a scanning tunnelling microscope in a basement. Neither
> of us had coded or really soldered before.
>
> The electronics work. We proved the whole measurement chain against a known resistor and it agreed
> with theory to 0.13 of a standard error. We made a real junction on gold leaf with a
> current–voltage curve that rules out both a short and an open circuit.
>
> We did not get an image. With the motor off and nobody touching it, the gap moves by most of the
> piezo's range in seconds — and measuring that, rather than guessing at it, is the result.
>
> Every raw file, every failed approach and every retracted claim is public: [repo link]

---

## Draft C — leads on the methods, for a technical audience

> We built a scanning tunnelling microscope in a basement and did not get an image. Here is the part
> worth sharing.
>
> After every scan we ran the same scan again with the lateral sweep switched off. That control
> cannot contain surface structure — so anything appearing in both is the instrument, not the
> sample. Our scans reproduced no better than those controls did. That is how we know we had no
> image, and it is why we never fooled ourselves.
>
> Re-deriving our own published statistics this week, we found two of them were computed across
> aborted files and withdrew both. The conclusion survived on other evidence. We keep the withdrawn
> claims in the record rather than quietly deleting them.
>
> Two first-year students, no prior coding or soldering. The blocker is mechanical and we measured
> it: the gap moves by most of the piezo's range in seconds with nothing touching the instrument.
>
> [repo link]

---

## What is deliberately NOT in any draft, and why

| Not said | Why |
|---|---|
| "We achieved tunnelling" / "we detected tunnelling current" | **Not demonstrated.** The 2026-09-19 junction was a pressed contact — a decade of current per ~1,650 Z counts where tunnelling needs ~6-13, with mechanical hysteresis in every run |
| "We imaged atoms" or anything implying an image | **No image has ever been produced** |
| A distance in nanometres | This instrument has **never established a distance scale from its own hardware**. The nm-per-count figure in circulation is inherited from another builder's scanner |
| "We failed" | The limitation is measured and located. That is a result, not a failure |

## The one thing you COULD add, if you want the honest cliffhanger

**Only if you are comfortable with a technical follow-up question**, because it is genuinely
unresolved rather than rhetorical:

> One junction we made in September is still undecided. Whether it was true tunnelling or a pressed
> contact turns on a single distance inside the scan head, about a fortieth of a millimetre, that we
> have bounded but not yet resolved — and it needs a microscope, not electronics. It is the first
> thing we will do when the instrument is reassembled.

**This is accurate, with one correction made after the first draft.** `docs/OPEN_QUESTIONS.md`:
*"this one distance decides whether we are tunnelling or pressing through a soft contact."*

**The threshold is about 26 micrometres, not the 0.13 mm this file first said.** 0.13 mm is a
different test — whether the gap wobbles too much to hold at all, not how fast the current decays.
On the decay test 0.13 mm is still five times too slow. **Jacob measured the distance at the bench
on 2026-09-20 and it is under 0.5 mm**, which narrows the question without settling it: 26 um sits
inside that bound, in its bottom 5%. **Do not say "a straightedge closes it"** — a straightedge and
an eye are what produced the 0.5 mm bound; resolving 26 um needs a loupe, a USB microscope or an
optical comparator. Full working in `deliverables/2026-09-19-pause/JUNCTIONS.md` and
`LEAD_VERIFICATION.md` V11-V12.

## Before posting

- **Add the repository link**, and check you are happy for it to be public.
- **The photograph is of you** — if you use one with Nuh in it, ask him first.
- **Tag Nuh**, and consider crediting the two open-source designs the build follows: Mech Panda's
  `red-panda-stm` and Dan Berard's home-built STM.
