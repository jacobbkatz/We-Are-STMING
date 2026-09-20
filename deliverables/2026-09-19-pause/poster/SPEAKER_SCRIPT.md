# What to say at the poster

**For Jacob and Nuh, 2026-09-19.** Two scripts: **a two-to-three minute walk-through** for somebody
who stops and wants the whole thing, and **a twenty-second version** for somebody passing.

**It is written against the poster's six panels, in order:**

| | |
|---|---|
| **01** | We built the whole thing |
| **02** | The measurement chain agrees with theory |
| **03** | A real junction, with a barrier's signature |
| **04** | We found the limit, and measured it |
| **05** | We built controls designed to kill our own results |
| **06** | One junction is still undecided - and we know the measurement |

**Read it out loud once before the event.** It is written the way people talk, not the way the
poster is written, so it should sound like you. Change any word that does not.

**Three things to hold on to.**

1. **Lead with what you built and what it does.** The first thirty seconds decide whether they
   stay, and they are not "sorry we did not get an image" seconds. Every number on this poster is
   something that worked.
2. **The one limitation is stated confidently, once, as a measurement.** Nobody has ever thought
   less of a team that could say exactly what stopped them, to the count.
3. **"We have not measured that" is a complete answer** and a good one. `QUESTIONS_AND_ANSWERS.md`
   in this folder has the hard questions, with answers you can defend.

---

## The two-to-three minute version

> **Stage directions are in square brackets.** They are for you, not to be read out.

[Stand beside panel 01, the photographs.]

**"We built a scanning tunnelling microscope. Nuh and I are both first-year students - neither of us
writes code, and before this project neither of us had really soldered anything. We built it in my
basement, on a wooden bench, in a house where people are walking around and nobody controls the
air. Not a lab, not a clean room. That matters, and I will come back to it.**

**There was no kit. We designed it, ordered the boards, printed the frame, wrote the firmware, and
brought every stage up on its own before trusting the next one."**

[Panel 02, the straight line.]

**"A tunnelling microscope holds a sharp tip about a nanometre above a surface and measures the
current that crosses the gap - around a billionth of an amp. So the first question is whether you
can measure a billionth of an amp at all.**

**We took the tip and the sample out and clipped a known hundred-megohm resistor in their place.
With a known resistor, Ohm's law tells you what the reading has to be before you take it. We
predicted minus three thousand two hundred counts per volt. We measured minus three thousand two
hundred and five, give or take thirty-seven - agreement to about a tenth of one standard error.
Twelve stages had to be right at once for those points to land on that line."**

[Panel 03, the curve.]

**"Then we made a real junction between a tungsten tip and the gold. The current climbs about four
times faster than the voltage does - which rules out a plain short, because a short would be a
straight line, and rules out an open circuit, because there are tens of nanoamps. It reverses when
we reverse the voltage, on two separate nights. So there is a barrier there: something the
electrons have to cross.**

**And the electronics are not what limits us. With a junction live the noise is nine to nineteen
counts, and somebody stamping on the floor two metres away changes a reading by one picoamp in a
hundred and thirty. The building is not getting in electrically - we proved that with numbers."**

[Panel 04, the big chart of the gap moving.]

**"What we do not have is an image. The good part is that we know exactly why, and this is my
favourite measurement on the poster.**

**We stopped the motor, took our hands off the instrument, and just watched where the surface was.
It moved more than forty-three thousand counts in six seconds - most of the range of the piezo -
and then it went out of reach altogether for nearly two minutes. Over the five seconds one image
takes, the gap wanders four hundred to seventeen hundred counts. The structure in anything that
ever looked like an image is thirty to four hundred and sixty counts.**

**So the thing we are trying to measure is smaller than the way the gap moves while we are
measuring it. That is a number, not an excuse - and it is what the basement is doing. A commercial
instrument sits on an air table in a temperature-controlled room, and that is exactly the problem
those rooms exist to remove. We measured what our room costs, in our own units, and we have five
candidates for what is doing it."**

[Panel 05, the two little square images and the dot chart.]

**"The reason we have not fooled ourselves is this panel. Every scan we ran, we ran again with the
sideways sweep switched off. The tip never travels across the surface, so a control like that
cannot contain the surface - anything that shows up in both is the instrument talking to itself.**

**Like for like, our scans repeat at plus nought point nought four and the controls at plus nought
point nought seven. Indistinguishable, and neither is different from zero. That one test settles
the imaging question, and running it was the right call."**

[Panel 06, the three little line charts.]

**"And this is the one we have deliberately left open.**

**One measurement still looks like a surface: three places twelve thousand counts apart, where the
passes at one place agreed with each other and disagreed with the other places - about one chance
in three hundred on a permutation test. But we ran two hundred and nine reproducibility tests on
this data, so the honest threshold is about one in four thousand, and we fixed that number before
we judged anything. It did not repeat, and an X-held control that cannot contain a surface scored
one in fifty on the same statistic. That is our own false-positive rate, and knowing it is worth
more than any single positive would have been.**

**The other open one is whether our best junction was tunnelling at all. We did the arithmetic
rather than guess. One motor step moves the fine screw a hundred and fifty-five nanometres, and
tunnelling needs a tenth of a nanometre per decade of current - so the lever between the motor and
the tip would have to be about fifteen hundred to one, which puts the tip within twenty-six microns
of the pivot line. Jacob measured that distance as well as anyone can with a straightedge: under
half a millimetre. That does not resolve twenty-six microns - nothing by eye does. So it stays
undecided, and what closes it is an eyepiece or an optical comparator, in minutes, with the power
off."**

[Close, stepping back to the whole poster.]

**"So: every subsystem a tunnelling microscope needs is built, working and calibrated. What is left
is mechanical - and we measured it rather than guessing at it."**

---

## The twenty-second version

**"We built a scanning tunnelling microscope in my basement - two first-year students, no coding
experience, and the first soldering either of us has done. The electronics are finished and
calibrated: we measure about a billionth of an amp, and the whole chain agrees with Ohm's law to a
tenth of a standard error. No image yet, because the gap moves more than the signal does - and we
measured exactly how much. That is the part we are fixing."**

---

## If they only ask one question, it will be this one

**"How did the current change as you moved the tip?"** That is what somebody who knows what an STM
is will ask, and it is panel 06. **Do not guess at it. Say:**

**"On the last junction we tested, a decade of current per about seventeen hundred counts - where
tunnelling would need something like ten. That one was a pressed contact and we say so. The
junction two nights earlier was about seven times steeper, and for that one to have been a vacuum
gap the tip would have to sit within twenty-six microns of the pivot line. We could only measure
that distance to under half a millimetre, so we cannot say - and the measurement that settles it is
optical and takes minutes."**

**That answer is the strongest thing you can say to that person.** It shows you measured the right
quantity, did the arithmetic, and let it go where it went. **Claiming tunnelling collapses on this
same question, and takes the calibration, the noise work and the controls down with it.**

> **The poster wins over this page.** `d` was argued about on the evening of 2026-09-19 and again on
> the 20th. `deliverables/2026-09-19-pause/LEAD_VERIFICATION.md` V11 and V12 carry the arithmetic,
> and `docs/FACTS.md` marks `d` itself **CONTESTED - do not use**.

---

## Things to have ready in your head

| If they ask | Say |
|---|---|
| **"How long did this take?"** | About eight weeks from ordering boards to a working junction. First power-on was 29 August; the last bench session was 19 September. |
| **"What is yours and what is copied?"** | The mechanics, the controller board and the firmware follow Mech Panda's open-source `red-panda-stm`; the scan head and the preamplifier follow Dan Berard's home-built STM. **The electronics bring-up, the software, the calibration and the controls are ours.** **Say this without being asked** - it costs nothing and it is the right thing to do. |
| **"Who is supervising you?"** | Nobody. Self-directed: no faculty advisor, no grant, no lab. |
| **"Can I see the data?"** | All of it is in the repository, including the results we withdrew. |
| **Anything you do not know** | "We have not measured that", and then where the answer would come from. Never fill the gap on your feet. |

---

## Two sentences worth memorising word for word

**The claim:** *"Every subsystem a tunnelling microscope needs is built, working and calibrated.
What is left is mechanical - and we measured it."*

**The limit:** *"The thing we are trying to measure is smaller than the way the gap moves while we
are measuring it. Four hundred to seventeen hundred counts of drift, against thirty to four hundred
and sixty counts of signal."*
