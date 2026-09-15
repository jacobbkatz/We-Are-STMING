# Current status

**Last updated:** 2026-09-15 (evening, third session of this run)
**Updated by:** Jacob at the bench, with Claude remote. **THE INPUT NODE IS BUILT AND THE SPARE PREAMP BOARD HAS BEEN POWERED FOR THE FIRST TIME.** It reads **about 6 pA at 10 minutes on ±15 V**, against a target of 1 nA — **the first valid input current this project has ever measured.** The warm-up drift does not reproduce. See [`sessions/2026-09-15-bench.md`](sessions/2026-09-15-bench.md), which is a **different session** from [`sessions/2026-09-15.md`](sessions/2026-09-15.md) and does not supersede it. **The 45-minute reading is still owed.** Earlier the same run: Part B passed and the board was washed. The first time any preamp board in this project has been cleaned. See [`sessions/2026-09-15.md`](sessions/2026-09-15.md), which is the second session of the same night as [`sessions/2026-09-14.md`](sessions/2026-09-14.md).

> ## NEXT THING THAT HAPPENS — read before touching the board
>
> **The board was washed late on 2026-09-14 and left to dry overnight on a lint-free pad. Confirm it
> is bone dry before powering anything.** If in doubt, give it longer.
>
> **Then Part C, the current-limited smoke test** — `docs/NEXT_SESSION_PLAN.md`. It has moved: it
> now runs **after the wash and before the input node is built**, so a fault is found while the
> board is still bare and reworkable. Bench supply only, **never the controller**.
>
> ## THE TIMED RUN — started 17:49 UTC, 2026-09-15
>
> **Second power-on, after the supply glitch. Rails at 15 V and −15 V, limit 20 mA.**
> **Supply current 4 mA**, against 3 mA at the 5 V rails — a small rise with supply voltage is
> ordinary and the two channels still match.
>
> | Minute | OUT lead | Input current | Supply current |
> |---|---|---|---|
> | 0 | **5 mV**, wandering slightly | **~50 pA** | 4 mA |
> | ~2, settled | **0.9 mV** | **~9 pA** | — |
> | **5** | **−0.3 mV** | **~3 pA**, sign meaningless at this level | **4 mA** |
> | **10** | **−0.6 mV** | **~6 pA** | **4 mA** |
> | ~~20~~ | ~~—~~ | **NOT TAKEN** | — |
> | ~~45~~ | ~~—~~ | **NOT TAKEN — this is the one safety rule 14 wants** | — |
> | ~~60~~ | ~~—~~ | **NOT TAKEN** | — |
> | 5 | | | |
> | 10 | | | |
> | 20 | | | |
> | 45 | | | |
> | 60 | | | |
>
> ### The drift question is already answering itself
>
> **Minute 0: 5 mV. Minute 2: 0.9 mV. Minute 5: −0.3 mV.** The reading is **falling and has crossed
> zero**, not climbing. It is settling toward the amplifier's own input offset voltage, which is
> where a working transimpedance amplifier with no input current should end up.
>
> **The sign flip means nothing at this level.** A few tenths of a mV is inside both the meter's last
> digit and the op-amp's own offset voltage. **Do not chase the sign until the magnitude is large
> enough to carry one.**
>
> **Compare with the old board: about 25,000 counts of climb over an hour, roughly 7.8 V at the
> output.** This board has moved about 5 mV in the wrong direction for that story, in the first five
> minutes. **Not yet conclusive at 5 of 60 minutes**, but the two behaviours are already nothing
> alike.
>
> **The gloved-touch response repeats at 0.05 V**, so the 500 pA figure is reproducible rather than a
> one-off.

> ### A gloved touch on the standoff — an accidental but useful control
>
> **`BENCH` 2026-09-15. Jacob brushed the standoff with a nitrile glove.** The output jumped to
> **0.05 V**, which is **500 pA**, and **came back down to 0.9 mV, about 9 pA**, on its own.
>
> **Two things follow, and the second is the important one.**
>
> **The node behaves correctly.** It responds to injected charge and then recovers, which is exactly
> what a working high-impedance input does. Nothing was left behind: no new leakage path, no sticky
> offset.
>
> **It is strong evidence that the old board's body sensitivity was its floating reference.** Safety
> rule 9 records **20 to 50 nA from a person within a metre**, measured on a board whose +IN floated,
> and the rule already carries a "basis in doubt" note from 2026-09-13. **Here, DIRECT CONTACT
> through a glove produced 0.5 nA** — between 40 and 100 times less, from a far more aggressive
> stimulus than standing nearby. **Keep the rule**, because 500 pA is still half a tunneling current
> and the shield matters. **But the 20 to 50 nA figure looks like an artefact of the floating
> reference, not a property of this circuit.**
>
> **Do not repeat it deliberately.** Two reasons, neither about the reading: the standoff is held by
> a springy resistor lead about 2 mm from IC1's grounded leg, so a knock can short the input to
> ground; and **a nitrile glove is an excellent static generator** while the input is a JFET gate
> that 100 MΩ does nothing to protect.

> **The run was stopped at 10 minutes and the board powered down**, by Jacob's choice, to break for
> lunch. **Minute zero was 17:49 UTC.** The scheduled reminders for 20, 45 and 60 minutes were
> cancelled.
>
> **THE 45-MINUTE READING IS STILL OWED.** Safety rule 14 wants the output under 0.1 V at 45 minutes
> on the bench supply, and on tonight's evidence it should pass by a factor of about a thousand —
> **but it has not been taken, and an untaken measurement is not a result.** Re-power and finish it.
>
> **What this run is for is no longer the offset.** That is settled at tens of pA and cannot
> meaningfully improve. **It is for the drift question** — whether the warm-up climb recorded on the
> old board was real or was its floating reference. A flat line here answers it.

> ## AT ±15 V: 3 pA — THEN THE READING STARTED WANDERING AND THE POWER WAS CUT
>
> **`BENCH` 2026-09-15, in order:**
>
> | When | OUT lead | Input current |
> |---|---|---|
> | ±5 V, ~2 min | **3.5 mV**, stable | **~35 pA** |
> | **±15 V, 1 min** | **0.3 mV**, flickering ±1 mV | **~3 pA**, ±10 pA |
>
> **3 pA is within about 3× of the op-amp's own input bias current of ~1 pA.** The board is at the
> floor of what the part can do. **The reading went DOWN when the rails went up**, which is the right
> direction and is consistent with 5 V rails being the very bottom of the part's supply range.
>
> > **Checker note.** The line above previously wrote the rails with a plus-minus sign, and
> > `check_facts.py` flagged it against the RETIRED DAC-range row, which is about the **X/Y DAC
> > range**, not about supply rails. A false
> > positive, reworded rather than excused. **The checker's qualifier narrowing did not save it**, and
> > that is the over-firing side of the defect already logged under Known code issues.
>
> **Then, shortly after the 1-minute reading, Jacob reported the voltages "started floating" and cut
> the power.**
>
> > **RESOLVED MINUTES LATER, and it was NOT the board.** Jacob: *"resetting it fixed the issue,
> > voltages came back to 15 volts and -15 volts."* **It was the bench supply's own output rails that
> > wandered**, not the meter and not the preamp. A power cycle of the supply restored them.
> > **The board is exonerated for this event.** **Why the supply did it is still unknown** — a loose
> > lead at its terminals and the supply's own glitch are both live, and the 20 mA limit is not a
> > likely cause, since the board draws about 3 mA and never approaches it. **If it recurs, capture
> > what the supply's display and its constant-current indicator do at that moment.**
> >
> > **No damage is expected.** The limit was 20 mA throughout and a wandering rail in constant-voltage
> > mode sags rather than overshoots.
> >
> > **The warm-up clock restarts from the new power-on** — safety rule 0 counts from when the board
> > was last powered, and it was unpowered in between.
>
> **The original wording is kept below because it was written before the cause was known.** His exact words are recorded here because the
> wording matters and was not reconciled at the bench: it is not known whether the wander was on the
> **meter** reading the OUT lead or on the **supply's own displays**, nor how large it was.
>
> **Enumerated causes, none yet tested** — a lost probe or clip; a JP1 lead losing contact at the
> board, which is exactly what "floating" looks like if it is the **white** ground lead; the input
> node shifting, since it is held only by the resistor lead in tension; real drift at the input; or
> a part failing. **The supply current at the moment it happened is the discriminator and was not
> captured.**
>
> **Do not simply re-power.** An intermittent **ground** with the rails applied is the one state here
> that can actually damage the amplifier, because the reference jumps while current has somewhere
> else to go. **Find the loose connection first, unpowered.**
>
> **The two readings above stand.** They were taken before the disturbance and the control had
> already been done.

> ## THE MEASUREMENT. 35 pA — 2026-09-15, and the rebuild worked
>
> **`BENCH`, Jacob: the OUT lead reads 3.5 mV, stable, at ±5 V supplies.** Through the 100 MΩ that is
> **about 35 pA of input current** — see [`docs/FACTS.md`](docs/FACTS.md).
>
> **This is the first input current this project has ever measured on an amplifier whose 0 V
> reference is connected to anything.**
> **For scale, safety rule 14 wants PAD1 under 0.1 V after 45 minutes on the bench supply**, and
> 0.1 V through 100 MΩ is 1 nA. **35 pA is about thirty times better than that**, and roughly 3% of a
> tunneling current, so a real signal would sit far above this floor. The chip's own input bias
> current is ~1 pA, so the board is within about 35× of the physical floor of the part.
>
> **The control was taken first, and this is why the reading is believable.** The same meter on the
> +15 V lead read 5.0 V before the zero was accepted. `CLAUDE.md`'s "take a control measurement"
> rule, applied at the bench.
>
> **What this does NOT yet establish, and none of it is a quibble:**
>
> - **It is a two-minute reading at ±5 V.** Safety rule 0 wants **45 minutes**, and the old board's
>   reading climbed for over an hour. **Repeat it at ±15 V on the timed schedule before anyone calls
>   this settled.**
> - **There is no tip lead and no box.** The original fault was measured on a board that had both.
>   **This clears the rebuilt board, not the whole measurement chain.**
> - **It does not prove the missing ground pour caused the old fault.** The old "119 nA" was never a
>   valid current, so there is nothing to compare against. What it proves is that **the rebuilt board
>   is clean**, which is the thing that was actually needed.
> - **Safety rule 14 is half cleared at most.** C2 is still the reused, over-heated tantalum and must
>   be replaced before this board meets the controller.
>
> **Not retired: the ~119 nA.** It sits in about ten live documents and is already flagged in place
> as never having been a valid current. Adding it to the RETIRED table would fire the checker across
> all of them for a figure that is correctly captioned where it stands. **Deliberate decision, not an
> oversight.**

> ## FIRST POWER-ON IN THE PROJECT'S HISTORY — 2026-09-15, bench supply
>
> **The spare preamp board has been powered for the first time. Both channels at 5.0 V, 20 mA limit,
> and both read 3 mA.** `BENCH`, Jacob.
>
> **That is a pass on every criterion the smoke test has:** neither channel at the limit, and the two
> match, which is what a working op-amp does — its current runs from the positive rail straight
> through to the negative one. **A short from either rail would have pinned a channel at 20 mA. A
> badly leaking C2 would have shown as extra current on the −15 V channel alone.** Neither happened.
>
> **A lead on IC1's identity, not a conclusion.** `docs/OPEN_QUESTIONS.md` has carried "which op-amp
> is actually fitted" since 2026-09-09. **3 mA sits close to the 2.5 mA typical quiescent current of
> the OPA124**, read from its datasheet on 2026-09-09 and the only such figure this repository
> holds. **This does NOT establish the part.** The OPA627's own figure is unknown here — ti.com and
> three mirrors are blocked from this network — and without both numbers the comparison decides
> nothing. **Get the OPA627 figure when the network allows, then this reading may close the
> question for free.**

> ## THE ±18 V FIGURE IS THE CONTROLLER'S, NOT THE PREAMP'S — flagged 2026-09-15
>
> **Jacob had the bench supply set to 18 V per channel before powering the preamp board directly.**
> That number is correct and it is in our own documents — `docs/WIRING.md` §212 and
> `docs/COMPONENTS.md` §308 both say to feed **±18 V into the controller**, because its regulators
> need headroom. **It is the wrong number for the preamp board**, which the controller feeds at
> **±15 V**, and which our own parts notes give a supply range topping out at **±18 V**. Powering it
> at 18 V puts it exactly on its stated limit with no margin, and bench supplies can overshoot at
> switch-on.
>
> **Nothing was damaged: it was caught before the outputs went on.** The bench page now carries the
> warning at the top of its powered section. **Any future instruction to power the preamp from a
> bench supply must say 15.0 V and say why**, because the 18 V figure is the one a reader will find
> first if they grep for a supply voltage.

> ## CONTINUITY READINGS ON THE BUILT NODE — 2026-09-15, verbatim, NOTHING POWERED
>
> **Jacob, at the bench, reported exactly this:** `1: beep · 2: no beep · 3: no beep · 4: no beep ·
> 5: 220 ohms · 6: all open`.
>
> **Every value is a pass. No reading indicates a fault.** But **the numbering does not map onto the
> eight checks in [`docs/preamp_input_node_tests.html`](docs/preamp_input_node_tests.html)** and was
> not reconciled at the time: six items were reported against eight checks, and the `220 ohms` sits
> at item 5 where that page puts the −15 V silence check and puts 220 Ω at item 7. **The 220 Ω is
> almost certainly PAD1 to hole 3, which is R1** — there is no plausible 220 Ω path from the
> standoff to the −15 V rail — so the likely explanation is that the three "silent to a supply lead"
> rows were merged into the single `all open`.
>
> **Recorded as reported rather than as interpreted.** If a later session needs the individual
> rows, **re-measure; do not assume this mapping.** This is the same gap as the Part B readings of
> 2026-09-15, which were reported as "all as expected" and lost.

> **RESOLVED LATER THE SAME EVENING: IT WENT IN, AND THE INPUT NODE IS BUILT.** Jacob: *"I got it
> to work, the tension in the resistor wire holds the standoff in place after I solder both
> together."* **The hole does not grip the part** — retention is the 100 MOhm's own lead in
> tension, **resting on the board surface rather than sitting in the hole** — confirmed at the bench
> and the part confirmed as the 11301 from its bag. **Nothing was glued, drilled or forced.**
> **`docs/FACTS.md` is corrected: the 11301 does NOT enter our Ø2.108 mm hole**, which retires the
> previously stated "drops in with clearance" claim and every copy of it. **The bench page for what
> happens next — eight unpowered checks, the current-limited ramp, then the timed hour — is
> [`docs/preamp_input_node_tests.html`](docs/preamp_input_node_tests.html).** **Part C and the D5
> measurement have merged**, because with the feedback resistor fitted the output no longer sits at a
> rail. How it went in after it
> would not, and whether the pin is inside the hole at all, are **still unanswered** and matter for
> any future board. **The earlier stop notice follows, kept because its four candidate causes are
> still the right list for next time.**

> **~~STOPPED 2026-09-15, at the bench: THE STANDOFF DOES NOT GO IN.~~** Jacob offered it up and it
> did not enter the hole. **Nothing was forced and nothing was drilled**, which is what Part D0 says
> to do. **The previously stated clearance figure is now corrected in `docs/FACTS.md`** —
> the four candidate causes and their tests are in `docs/OPEN_QUESTIONS.md`, top row. **The first
> thing to rule out is that the part in hand is one of the two 11311 we also own**, which needs
> Ø3.45 mm and is already known not to fit. **Do all fit testing on a bare spare board, not on the
> repaired one.** Part C, the smoke test, does not involve the standoff and can still run.

> **Two things that are NOT true any more:** there are **no calipers** (nothing needs them), and
> **the distilled-water rinse is dropped** — we have no oven or dehydrator, and water under IC1
> would be a leakage path that mimics the warm-up drift we cannot yet explain.

> ## READ THIS FIRST — 2026-09-13, MEASURED
>
> **IC1 pin 3, the preamp op-amp's non-inverting input — the transimpedance amplifier's 0 V
> reference — is connected to nothing, on BOTH preamp boards.** Beep-tested on both. On the spare,
> confirmed through a scraped underside via: the via beeps to pin 3 and is silent to JP1 pin 1.
>
> **Cause.** Berard's Eagle board file has a ground copper pour across the underside. **The KiCad
> gerbers JLCPCB built our boards from have no pour at all** — zero filled regions in any layer. Six
> points that should be ground each end at a dead via: **C2 −, C3, C4, IC1 pin 3, IC1 pin 8 and JP1
> pin 4.** Only C1 − is joined to JP1 pin 1. **JP1 pin 4 "unrouted" (Nuh, 2026-08-31) was the first
> visible symptom of this same defect.** See fault 0d.
>
> **What it means.** **Every preamp reading in this project was taken with the amplifier's reference
> floating.** PAD1 = 11.905 V is a real reading, but **it cannot be converted to an input current**,
> so **the "~119 nA leakage" is unproven** — it may or may not exist. The warm-up drift, the noise
> figures, the three sweeps and the coax bisection are in the same position. The superglue and flux
> candidates are **neither confirmed nor ruled out**.
>
> **UPDATE 2026-09-14 — the spare board is repaired and verified.** All four ground wires are on and
> **IC1 pin 3 beeps to hole 1**: the first time in this project the amplifier's reference has been
> connected to anything. Eight continuity readings and one capacitance reading, all pass — the table
> is in [`sessions/2026-09-14.md`](sessions/2026-09-14.md) §3.1. **The +15 V clearance hazard at C3's
> via is closed: not bridged.** C2 reads 4.7 µF in circuit, so it survived the two-iron rework.
>
> **It is still unpowered, and it stays that way until the lead free ends are checked and the
> current-limited smoke test is run** (`docs/NEXT_SESSION_PLAN.md` Parts B and C). **C2 is still the
> reused part: it is replaced before this board ever meets the controller** — safety rule 14.
>
> **The old board is untouched and its +IN still floats**, so everything in the paragraph above this
> one still stands for every historical measurement.
>
> C2 was fitted reversed (as designed) and has been **rotated, reusing the original part**. Four leads
> are on (JP1 holes 1, 2, 3, 5; hole 4 empty on purpose — no copper). The to-scale bench drawing is
> `docs/preamp_ground_repair_map.html`.
>
> **Before the spare board ever connects to the controller:** C2 replaced with a fresh part, and PAD1
> under 0.1 V after 45 minutes on the bench supply. Safety rule 14.

> ## IF YOU READ ONE THING BEFORE THE NEXT BENCH SESSION — written 2026-09-09
>
> **Update 2026-09-13:** the order arrived except the standoff (SAID — VERIFY item by item). **The
> ~~cleaning kit is still not in the room: 91% IPA is there, 99% is not.~~ **SUPERSEDED 2026-09-14
> late: the 99% IPA is in the room** (Jacob), alongside the DI water, foam swabs and soft brush.
> **The cleaning kit is complete and the input node is no longer gated.** Soldering at JP1 had gone
> ahead already (that flux can stay). Copper tape and the 4.7 uF 1812 ceramics remain unbought.
>
>
> **The flux arrives 2026-09-11. The things that remove it were NOT ordered** — no 99% IPA, no
> distilled water, no brushes, lint-free wipes or foam swabs. **Rosin left on the preamp board is a
> leakage path at the exact node the 119 nA fault sits on. Do not solder the preamp until the
> cleaning kit is in the room.** **Copper tape** for the shield is also still unbought.
>
> **When the screws arrive: M2×6, NOT M2×8.** The box pilot is 5.00 mm deep and blind; an M2×8
> bottoms out and cracks the boss. **Calipers on the board first** — its thickness is assumed, not
> measured. Drive slowly, stop at snug; the thread is plastic.
>
> **The piezo scanner is built and working.** Closed — do not re-open it, do not buy Sn42/Bi58
> paste, do not spend bench time on the seat-versus-disc question.
>
> **The bench procedure lives in [`docs/NEXT_SESSION_PLAN.md`](docs/NEXT_SESSION_PLAN.md).** It
> already existed but **nothing had ever updated it** — it sat two days stale and neither of us knew
> it was there. **`/wrap` now updates it as step 3, `/catchup` reads it, and `check_facts.py` fails
> if it is older than the newest session log**, which blocks the commit. **One correction in it was
> a hazard:** H1 said to print the ORIGINAL box base while describing the expected result as the v2
> geometry it forbids — a good print would have looked faulty, and the obvious recovery is to print
> the one that puts a pillar under the input node.

> **Two changes of state, both from Jacob rather than from any file.**
>
> **1. The piezo scanner is BUILT AND WORKING.** `SAID` 2026-09-09, Jacob. **Settled — do not
> re-open it.** The Sn42/Bi58 paste is not to be bought, the iron-temperature question is moot, and
> the Ø20.500 seat versus 25-27 mm disc conflict is **closed by construction: a working scanner
> exists, so whatever went in fits.** No bench time on any of it. Quadrant-to-axis mapping was never
> recorded and does not need to be — it falls out of the first image and is fixed in software.
>
> **2. Four items ordered, arriving 2026-09-11:** the **Chip Quik RMA791 rosin flux jar** (ROL0 —
> the correct flux), a **manual syringe dispenser** to load from it, an **800 pc M2 screw
> assortment**, and **assorted heat shrink**. **Use the M2×6 — an M2×8 bottoms out** in the box's
> 5.00 mm blind pilot (measured from the mesh, see [`docs/FACTS.md`](docs/FACTS.md)).
>
> ~~**THE CLEANING SUPPLIES WERE NOT BOUGHT.** No 99% IPA, distilled water, brushes, lint-free wipes
> or foam swabs.~~ **SUPERSEDED — all of them are in the room as of 2026-09-14 late.** The reason the
> rule existed stands: rosin flux left on this board is a leakage path at the node the project is
> blocked on, **so wash the board and clean locally after building the node.**
> **Copper tape is now the only other unbought item.**

> **3. Three defects found in the instruction files themselves**, after Jacob reported the model
> behaving worse since the 2026-09-08 audit.
>
> > **CORRECTED 2026-09-09 (final). These defects were real and worth fixing, but they did NOT
> > cause the behaviour Jacob reported, and presenting them as the answer was a mis-attribution.**
> > Every observed failure happened with the correct information already visible. **See
> > [`sessions/2026-09-09-jacob.md`](sessions/2026-09-09-jacob.md) §17 for the diagnosis that was
> > actually tested against the evidence.** Keep the fixes; do not believe the causal claim.
>
> `CLAUDE.md` had nearly doubled in four days, and:
>
> - **Two `safety rule 10` citations in this file meant rule 13** — the DAC modulo-wrap tip hazard.
>   Rules were inserted above it and the citations never moved. **Both corrected.**
> - **`CLAUDE.md` §4 was a second, shorter, differently-numbered safety list** claiming to be a copy
>   of this one. Its 7 was `CCON`; ours is the tip-holder meter check. It also omitted four hazards,
>   including the DAC wrap and the 45-minute warm-up. **It is now unnumbered and points here. This
>   file's list is the only citable one.**
> - **`CLAUDE.md` forbade restating any number outside `docs/FACTS.md`** — a rule the repository has
>   never followed (`10.24 V` is in 11 live documents) and which the 2026-09-08 audit had already
>   decided against in writing. **Rewritten to match the decision.**
>
> **`check_facts.py` now verifies every "safety rule N" citation resolves AND matches its rule's
> wording**, and is regression-tested against both original miscitations. 40 approach tests pass.
>
> **4. A deeper pass then found four more defects in `.claude/session-start.sh`** — the script whose
> output every session reads before it opens a single file. **All four were live.**
>
> - **It named the wrong session log.** `ls | sort | tail -1` is a lexical sort, and `-` sorts
>   before `.`, so **`2026-09-09-jacob.md` sorts BEFORE `2026-09-09.md`**. Whenever two logs share a
>   date the hook named the earlier one. **This is the likeliest single cause of sessions not
>   knowing recent context.** Fixed here and in `CLAUDE.md` §2, which said "the newest file",
>   singular.
> - **It blamed a retired value for every checker failure** — including for the checker *crashing*,
>   whose stderr it discarded. `check_facts.py` reports four different problems.
> - **It was hardcoded to `main`** and would have merged `origin/main` into a feature branch unasked.
> - **It printed this file's header by line number**, and had drifted to cutting off mid-sentence.
>
> **Each fix is commented at its site in the hook.** See
> [`sessions/2026-09-09-jacob.md`](sessions/2026-09-09-jacob.md) §15.
>
> **5. A third, systematic pass found the root cause one level below all of that, and found that
> the §15 fix was itself incomplete.** `sessions/README.md` states the convention as **"one file per
> work session, named `YYYY-MM-DD.md`" — and four logs have broken it since the first session.**
> The convention was never true, and **eight** separate mechanisms were written against it. §15
> fixed two of them and reported the problem solved.
>
> - **Nuh's log for today, `sessions/2026-09-09.md`, was missing from `sessions/README.md`** — so it
>   was invisible to **both** discovery mechanisms at once. **Now indexed, and `check_facts.py`
>   fails if any log is unindexed.**
> - **`/wrap` and `CLAUDE.md` §5 both said "if a file for today already exists, add to it".** Today
>   that file was Nuh's. **Following it literally writes one person's session into the other's log.**
>   Both now say to check whose it is first.
> - **`/wrap` said to REMOVE a fixed fault or a dead rule.** This project strikes through and keeps,
>   because **twice a retraction has itself been wrong.** Changed.
> - **`check_facts.py` skipped `sessions/README.md` and `sessions/TEMPLATE.md`** though neither is
>   history. Switching them on found **three retired `37 nA` values** in the index, read as current.
>
> **Every check has now been proved able to fail** by re-introducing each fault: 9 of 9 checker
> assertions, both hook behaviours, 40 unit tests. **`CLAUDE.md` §7 gains four rules** aimed at the
> stopping-rule failure that made this take three passes. See
> [`sessions/2026-09-09-jacob.md`](sessions/2026-09-09-jacob.md) §16.
>
> **6. The diagnosis, finally tested against the evidence — and the first three passes had the cause
> wrong.** Jacob reported that **Nuh had seen the same decline**, which rules out anything specific
> to one session. **None of the defects in items 3-5 explains any observed failure:** the start-up
> hook named the *right* log for the question asked, and the answer was **the first row of a table
> that had just been printed in full.**
>
> **Ruled out by evidence:** the model changed (`get_session` — `claude-opus-5`, effort high, no
> fallback, **checked on two separate days**); context exhaustion (318k of 1M, and the misread was
> the session's first exchange); the repository; `CLAUDE.md`'s length.
>
> **The actual mechanism, in nine errors across three sessions and both people's work:** act on the
> first plausible reading, write it in as fact, skip the cheap check that would have disconfirmed
> it. Nuh's session put `OPA124U` into **five documents** from a photograph of **Berard's** board;
> a 2.03 mm *length* was read as a *diameter* and called a clearance fit; this session read
> "solder" as piezo paste with the flux row on screen, and pushed a commit while the checker was
> failing.
>
> **A fifth written rule would have been worthless** — §1, §3d and §7 already say it. **So what was
> added is mechanism:** a **pre-commit hook that refuses a commit while `check_facts.py` fails**
> (auto-installed on both computers via `core.hooksPath`), and **a checker that detects its own
> blind spots** — generalising Nuh's finding that a badly worded RETIRED qualifier let it
> **report clean while three files carried the wrong number**. **Two recommendations Nuh wrote down
> on 2026-09-09 and nobody applied are now applied.**
>
> **Not claimed as fixed.** No mechanism can ask "whose board is that photo of". See
> [`sessions/2026-09-09-jacob.md`](sessions/2026-09-09-jacob.md) §17.

See [`sessions/2026-09-09-jacob.md`](sessions/2026-09-09-jacob.md) sections 11, 12, 14, 15, 16 and 17, and
[`docs/PREAMP_SHOPPING_LIST.md`](docs/PREAMP_SHOPPING_LIST.md).

Earlier on 2026-09-09 (later): Jacob, remote. C2's
reverse connection re-verified independently, and **established that it cannot cause the 119 nA**
(fault 1d). **We do not own the Keystone 11301** — we own the 11311, which does not fit; `BOM.md`
and the shopping list were both wrong. New **[`docs/INVENTORY.md`](docs/INVENTORY.md)** and
**`CLAUDE.md` §3d**: what we physically own is not derivable from any design file — ask, never
infer. See [`sessions/2026-09-09-jacob.md`](sessions/2026-09-09-jacob.md).

Earlier on 2026-09-09: Nuh. **Documentation only — no hardware was powered and nothing was
measured.** Worked out the materials and technique for finishing the preamp, and in doing so
found that **the box already fits the board**, that **box v2 must not be printed**, and that
**C2 is reverse-connected in the source design**. See [`sessions/2026-09-09.md`](sessions/2026-09-09.md)
and the purchase list in [`docs/PREAMP_SHOPPING_LIST.md`](docs/PREAMP_SHOPPING_LIST.md).
**Corrected 2026-09-09 (later): the standoff also has to be bought.** Otherwise consumables only —
the flux (our no-clean one is the wrong type for a 100 MΩ input), cleaning supplies and hook-up
wire. The solder we own is fine. **The Keystone 11301 is NOT in the drawer** — we own the 11311,
which does not fit. See [`docs/INVENTORY.md`](docs/INVENTORY.md).

Before that, 2026-09-08: Jacob, remote. Repository audit and migration: `docs/FACTS.md` and
`Code/pc/check_facts.py` added, superseded documents archived with banners. See
[`sessions/2026-09-08.md`](sessions/2026-09-08.md).
**The hardware state below is unchanged from 2026-09-07**, when Nuh was at the bench with the
board powered — **the first hardware measurements since 31 August** — followed by Jacob, remote,
with a component-level datasheet pass and a second-pass audit.

> **Three documents to read before planning any bench work.**
> - **`docs/FACTS.md`** — the canonical value of every number that matters, with provenance, and a
>   RETIRED table of values that are now wrong. **If a number here and a number elsewhere disagree,
>   this file wins.** `python3 Code/pc/check_facts.py` enforces it and runs at every session start.
> - **`docs/COMPONENTS.md`** — every part with the specs that matter, cross-checked against the
>   actual design. Answers "what voltage can this pin take", "is this op-amp stable", "could the
>   Teensy damage this input" without searching.
> - **`docs/NEXT_SESSION_PLAN.md`** — the prioritised procedure for the next session, written to be
>   executed with no memory of any conversation.

Earlier on 2026-09-07: Jacob, remote, working from a photo of the rebuilt preamp box.

> ## READ THIS BEFORE ANY NUMBER IN THIS FILE
>
> **On 2026-09-07 a meter was put directly on the preamp output for the first time. Two things
> were found that invalidate a great deal of what follows:**
>
> 1. **The preamp output is +11.905 V, not 3.73 V.** The input current is about **119 nA**, not
>    37 nA. Every "37 nA" below is wrong.
> 2. **`PREAMP-`, the ADC's differential reference, is FLOATING.** Every ADC reading this project
>    has ever taken was measured against an undefined, drifting node.
>    **Worse than that, established 2026-09-07 from the datasheet: the LTC2326-16 is
>    pseudo-differential and requires IN− to stay within ±500 mV of GND. Ours sits near 2.7 V —
>    five times outside the allowed range. The converter has been operated outside its specified
>    input conditions for the life of the project.** No pre-bond ADC number can be rehabilitated by
>    rescaling.
>
> **Do not trust any current figure derived from ADC counts until the reference is fixed.**
> Meter readings are still good. See `sessions/2026-09-07.md` §17-27.
>
> ### 3. THE ADC FULL SCALE IS 10.24 V. The 4.096 V correction was WRONG.
>
> **Datasheet read 2026-09-07.** The LTC2326-16 has a **±10.24 V true bipolar input range**.
> REFBUF is 4.096 V, and **the input span is 2.5 × REFBUF**. The driver constant
> `_ref_buffer_volts = 4.096f` is the REFBUF voltage, exactly as its name says — not the input
> span. **`stm_control.py` and `stm_console.py` were right. Do not change them.**
>
> | | Was recorded | Actually |
> |---|---|---|
> | Volts per count | 0.125 mV | **0.3125 mV** |
> | 1 nA in counts | 800 | **320** |
> | Maximum measurable current | 40.96 nA | **102.4 nA** |
>
> **This resolves the contradiction in `sessions/2026-09-07.md` §21 completely.** At 0.3125 mV per
> count, the settled ~29,500 counts is **9.22 V** differential. PAD1 measures 11.905 V. So
> `PREAMP-` sits at about **2.7 V** — and Nuh's meter read it as "2 V and dropping". Everything
> reconciles, and **the ADC is not saturated and not over range.**
>
> **It also means the offset never changed.** 31 August's 29,873 counts is ~9.33 V differential,
> about 12 V at the op-amp, about **119 nA** — the same as today. The "37 nA" was a scale error,
> not a smaller fault.
>
> **Also confirmed from the same datasheet:** output format is **two's complement** (closes that
> open question), and the inputs are **pseudo-differential**, so `PREAMP-` is not a wide-range
> input and should sit near ground.
>
> **Still NOT known: the absolute maximum input rating.** Every datasheet host is blocked from this
> session. **See the revised action order below — the plan no longer depends on it.**

> **Before recording anything here as unknown, read `CLAUDE.md` §3b and check `docs/INDEX.md`.**
> Four items in this file's history were marked unknown while the answer sat in a repository file.

> This file is the single source of truth for where the build is right now.
> It is rewritten at the end of every work session. If anything else in the repo
> disagrees with this file, **this file wins** — see `CLAUDE.md` for the full rule.

---

## Where we are in one line

> **Rewritten 2026-09-13.** Stages 0 through 5 pass and the bias path passes. **The preamplifier is
> the blocker, and it has never been measured working as designed:** its reference input (IC1 pin 3)
> has been floating on both boards because the fabricated boards have no ground pour (fault 0d). The
> spare board is being repaired with wires. **Whether any real input leakage exists is unknown until
> the repaired board is measured.**

~~Stages 0 through 5 pass and the bias path passes. **The preamplifier is the blocker.** Its 119 nA
offset has **two remaining candidate causes** — cyanoacrylate contamination and flux residue, both
surface conduction into the input node. The third, the case shield, has been **rebuilt** and is
about to be tested properly for the first time.~~ **Superseded 2026-09-13:** every one of those
readings was taken with IC1 +IN floating. The candidates stay open; none was ever tested by a valid
measurement.

**On 2026-09-06 the shield was found to be discontinuous and only partly grounded**, which would
have made the planned shield test return a false negative and pushed us into consuming the spare
preamp board for nothing. It was stripped and rebuilt in all copper with soldered seams.
**The rebuild has not been verified with a meter yet — do that first.**

Two unfixed firmware faults were found on 2026-09-05 that will damage a tip if hit: **`CCON` snaps
Z to midscale**, and **the motor is left energised** and heats the scan head.

> ### Physical state of the preamp right now — read before planning any measurement
>
> Established 2026-09-07 from a photograph and Jacob's description.
>
> | | |
> |---|---|
> | **The box is OPEN** | Lid off, and the back cut away for probe access. **An open box is not a shield** |
> | **The tip coax is CUT** | Severed to get the module out. The input node no longer includes the cable, tip holder or tip — **which makes a bisection test possible for the first time** |
> | **The board is glued in and cannot be removed** | Heavily superglued to three standoffs printed as part of the box |
> | **The PTFE standoff is also glued to the board** | With cyanoacrylate. **This is the new leading candidate for the 119 nA** — see fault 1, candidate A0 |
> | **The bias HAS been on the whole time** | **Corrected 2026-09-07.** An earlier version of this box said there was no bias. Wrong. The sample plate is wired and biased; it is simply parked away from the tip holder, not near it |
> | **No tip is fitted** | Only the tip holder. **Nothing can be crashed**, so bias sweeps, Z sweeps and rail scaling are all zero-risk right now |
> | **The piezo is superglued into its socket** | **A third CA site**, and this one is at the scan head, next to the tip holder — which is part of the input node |
> | **The spare board is bare** | Not assembled. **Do not glue it in** — see safety rule 10 |
> | **3D prints are PETG-CF** | Confirmed by Jacob 2026-09-07. Closes the PA-CF/PETG-CF conflict opened by the slicer files |

> **New on 2026-09-06, second pass.** A verification audit found the first pass had stopped early.
> The five `.3mf` slicer files, the CAD render and the reference images had never been opened; two
> numbers in the reference were wrong. Highlights, all detailed below or in the reference:
> **safety rule 13** (an out-of-range DAC command silently jumps to the opposite rail),
> **fault 4b** (U13's unused op-amp channel floats next to the bias buffer),
> **the measurable-current ceiling is 41 nA, so the 119 nA fault is eating 91% of the ADC's range**,
> and **H1 pins 24 and 26 are spare ribbon conductors** — exactly the two wires the DAC fix needs.
>
> **New on 2026-09-06: `docs/ENGINEERING_REFERENCE.md`.** A repository-wide audit that pulls the
> cross-subsystem picture into one place — the grounding map, **the copper-vs-aluminium tape
> rule**, what a scan command becomes in nanometres, what a tunneling current becomes on screen,
> and an impact map for "if I change this, what else has to be rechecked". Every value in it
> carries a confidence tag. It does not replace this file; it explains how the pieces relate.
>
> The same audit **measured the printed parts** and closed two long-standing unknowns: all
> plate-to-plate and motor-mount screws are **M3**, and every printed box is held by a screw that
> **self-taps into a bare printed pillar** (dia 2.5 for M3, dia 1.6 on the preamp box for M2).
> Drive those slowly and stop at snug — over-tightening strips the pillar and the lid stops
> clamping onto its shield. `CAD/prints/README.md` has the table.

---

## Stage table

| Stage | Status | Notes |
|---|---|---|
| 0 Continuity | PASS | |
| 1 Serial, `GSTS` | PASS | |
| 2 Motor | PASS | |
| 3 Analog rails | PASS | LED5 and LED6 lit |
| 4 DACs and ADC | PASS | |
| 5 Piezo drive | PASS | −10 V at the scan head for `DACZ 65535`. **The scanner itself is now built and working** — Jacob, 2026-09-09 |
| Bias path to sample | PASS | −3 V at the sample holder for `BIAS 65535`, gain −1 as per schematic |
| 6 Preamp | **FAIL** | PAD1 = 11.905 V on 2026-09-07. **Not a valid current measurement: IC1 +IN floats on both boards** (fault 0d, 2026-09-13). The "~119 nA" is unproven |
| **Spare preamp board** | **GROUND REPAIR + PART B PASS, WASHED, DRYING — still never powered** | 2026-09-14: 4 of 4 wires on, all four ground points beep to hole 1, no shorts, C2 reads 4.7 µF in circuit. **Part B passed the same evening — all six lead free-end readings as expected** (`docs/preamp_partB_probe_map.html`). **Then washed in 99% IPA and left to dry overnight**, the first preamp board in this project to be cleaned. **Next is Part C, the smoke test** — the first time this board is powered by anything, and only once it is dry. **C2 is still the reused part** — safety rule 14 before the controller |
| **Measurement chain** | **NEW FAIL** | **`PREAMP-` floating** — the ADC's reference is undefined. **Not over range after all:** span is ±10.24 V and the differential is ~9.2 V |
| **Preamp box** shielding | **REBUILT, unverified** | All copper, seams soldered, one ground wire, 2026-09-06. **Continuity not yet metered — VERIFY first thing** |
| DAC config stability | **FAIL** | All four DACs drop config roughly hourly |
| JP1 grounds | **FAIL on the old board, FIXED on the spare** | Pin 4 is one of **six** GND points left unconnected by the missing ground pour (fault 0d). **On the spare, four are now wired, verified 2026-09-14**; IC1 pin 8 is skipped by design (no-connect on an OPA627) and hole 4 is left empty. The spare uses hole 1 only |

---

## Open faults

### 0. THE MEASUREMENT CHAIN IS BROKEN — fix this before anything else

**Found 2026-09-07 with a meter. This outranks every other fault in this file, because it is the
instrument all the others were diagnosed with.**

| Point | What it is | Measured |
|---|---|---|
| **PAD1** | Preamp op-amp output | **+11.905 V** |
| **R23** | ADC input path, controller | **+11.914 V** |
| **DSUB2 pin 2 (brown)** | **`PREAMP-`, the ADC's negative reference** | **"2 V and dropping" — FLOATING** |

**0a. `PREAMP-` is floating.** The LTC2326-16 measures `PREAMP+` **minus** `PREAMP-`. It does not
measure against ground. `PREAMP-` should carry the preamp's own ground back on its own wire —
Berard's method for rejecting cable noise. It is connected to nothing, so **every ADC reading in
this project has been referenced to a drifting, undefined node.**

> **This is the same fault as fault 5 below** — "one JP1 ground pin is open", recorded 2026-08-31
> and filed as a loose end for a future rebuild. It is not a loose end. It is the reference the
> whole instrument measures against. **And it is repairable without a rebuild.**

**0b. RESOLVED 2026-09-07 — the ADC is NOT over range.** Span is **±10.24 V**, and with `PREAMP-` floating near 2.7 V the differential is about 9.2 V, inside it. **It only goes over range if `PREAMP-` is bonded while PAD1 is still at 11.9 V** — which is why that step is now last. PAD1
and R23 differ by 9 mV, so there is **no attenuation anywhere** — confirming the netlist finding
that the buffers have gain exactly 1. `docs/UPSTREAM_MECHPANDA.md` §5 warned this could happen and
said to check the absolute-maximum rating first. **Nobody did, and it has been in this state for
weeks.** Whether the converter is damaged is UNKNOWN.

**0d. NEW 2026-09-13, MEASURED — THE PREAMP BOARDS HAVE NO GROUND POUR, SO IC1's REFERENCE INPUT
FLOATS.** This sits underneath 0a, 0b and 0c and outranks them: those describe the ADC's reference;
this is the preamp's own.

| Check, unpowered, beep mode | Spare board | Old board |
|---|---|---|
| C1's grounded end ↔ JP1 pin 1 (control) | beep | — |
| **IC1 pin 3 (+IN) ↔ JP1 pin 1** | **silent** | **silent** |
| C2's ground end ↔ JP1 pin 1 | silent | silent |
| Scraped pin-3 via ↔ IC1 pin 3 / ↔ JP1 pin 1 | beep / **silent** | not done |
| Scraped C4-ground via ↔ C4 pad / ↔ JP1 pin 1 | beep / silent | not done |

**Why.** Berard's Eagle board (`tunnelAmp.brd`) gives the `GND` net a polygon on the bottom layer
covering everything except the input-node strip. **The gerbers we fabricated from contain no filled
region on any layer.** In those files only **C1 − and JP1 pin 1** are joined by copper. **C2 −, C3
pad 2, C4 pad 2, IC1 pin 3, IC1 pin 8 and JP1 pin 4** each end at a tented via whose stub leads
nowhere. Coordinates and the trace are in `sessions/2026-09-13.md` §3.6. The gerbers' X2 net labels
still say `GND` for every one of them, which is why every document in this repository believed they
were connected. **An upstream conversion defect, not a build fault.**

**Consequences.**

1. **No preamp reading in this project measured input current.** With +IN floating, PAD1 follows
   wherever that node drifts. Faults 1 and 1c, the noise figures, the 45-minute warm-up measured
   after power-on (safety rule 0) and the figure for a person within a metre of the board (safety
   rule 9) all rest on those readings. **Basis in doubt — kept until a repaired board is measured.**
2. **C2, C3 and C4 decoupled nothing** on either board. Only C1 was working.
3. **The old board's reversed C2 was probably never reverse-biased** — its ground end floats.
   Derived from the copper and the beep test, not measured with power.
4. **C3's ground-via stub ends 0.076 mm from JP1 pin 2's +15 V pad** on the underside. Untested
   whether they touch. Check before grounding C3.

**Repair on the spare, in progress.** Short 40 AWG magnet wires from each dead via to JP1 pin 1's
underside joint. **Done:** IC1 pin 3, C4. **To do:** C2 (via → dot 2's joint), C3 (right half of the
via only → hole 1). **Not verified yet.** Procedure: `docs/NEXT_SESSION_PLAN.md`. The permanent fix
is a board reorder with the pour filled.

**0c. RESOLVED 2026-09-07 — the contradiction was a wrong constant, not a mystery.**
It was recorded as: with 11.9 V on its input the ADC should be pinned at 32767, yet it reads
~30,000 and wanders, behaving as though full scale were about 13 V.

**Full scale is ±10.24 V.** So ~29,500 counts is **9.22 V**, PAD1 is 11.905 V, and `PREAMP-` sits
at about **2.7 V** — which is what the meter read. **Nothing is saturated and nothing is over
range.** The "about 13 V" estimate was the right instinct pointing at a constant that was wrong.

---

### 1. Preamp — ~119 nA input leakage (the blocker)

> **BASIS IN DOUBT, 2026-09-13.** Everything in this fault was measured on a board whose IC1 +IN was
> floating (fault 0d). **The 11.905 V is real; the 119 nA is a conversion that assumed +IN at 0 V.**
> The candidates below are neither confirmed nor ruled out, and the rail-leak "failed test" is not
> evidence either way. **Kept in full, unedited, until the repaired spare board is measured.**

> **Corrected 2026-09-07, twice.** This fault was recorded all project as **37 nA / 3.73 V**,
> derived from ADC counts using a full-scale constant that was wrong. A meter on PAD1 reads
> **11.905 V**, which through the 100 MΩ feedback resistor is **about 119 nA**.
>
> **The offset never actually changed.** Rescaling 31 August's 29,873 counts at the correct
> 0.3125 mV per count gives 9.33 V differential, about 12 V at the op-amp — **the same ~119 nA**.
> The "37 nA" was an arithmetic error carried for a week, not a smaller fault that grew.
>
> **119 nA is above the instrument's own ceiling of 102.4 nA.** Even with a perfect reference the
> ADC cannot measure the present offset; it would simply pin. The leak has to fall by **more than
> 100x** to leave room for a 1 nA tunnelling signal.

**The feedback loop is closed, not open.** It settles rather than ramping, and that is the whole
diagnosis — an amplifier with an open feedback resistor behaves as an integrator and would have
pinned within two minutes. Do not let any older document tell you otherwise.

**11.905 V on a +15 V supply is close to an OPA627's output limit, so the amplifier may be
saturated.** If it is pinned it cannot respond to anything — which would make the three null
results of 2026-09-07 artefacts rather than evidence. See fault 1c.

**Candidate causes.**

| Candidate | Found | Status |
|---|---|---|
| **A0. Cyanoacrylate AT THE BASE OF THE PTFE STANDOFF.** The standoff would not fit through the board hole, so it was glued down. That standoff's only job is to hold the input node off the board on the best insulator available — **and CA bonds straight across it** | **2026-09-07** | **LEADING.** A solid contact path at **0 mm** from the node, not a vapour path at a distance. See below |
| **A. Cyanoacrylate contamination / bloom.** CA blooms while curing and deposited a conductive haze over the board, input node included. The board is also **heavily** glued to three printed standoffs, the nearest **4.8 mm** from the input pad | 2026-08-31 | Live |
| **B. The case shield is floating.** | 2026-09-01 | **ELIMINATED as an offset source, 2026-09-07, by measurement.** The rebuilt shield did not move the mean. Still a plausible **noise** contributor; continuity still unverified |
| **C. Flux residue.** Berard independently reports "huge leakage currents" from flux left on this exact circuit | 2026-09-05 | Live. Addressed by the existing rebuild clean, but not excluded on the current board |
| **D. The coax or the tip holder.** | **2026-09-07** | **ELIMINATED, by measurement.** With the coax centre, tip holder and tip all removed from the input node, the offset returned to its full settled value. **The leak is on the preamp board** |
| **E. Cyanoacrylate at the piezo socket.** The disc was glued into its socket — a **third** CA site, at the scan head and right next to the tip holder, which is part of the input node | **2026-09-07** | Live. Berard's warning in safety rule 7 was already that glue must not bridge the tip standoff to the grounded brass electrode. **We now know glue was used exactly there.** Meter-check it |

> ### A0: the glue at the PTFE standoff, and what the output SIGN says
>
> **Superglue was used twice on this build, and the first use is the serious one.** A small amount
> bonds the PTFE standoff to the board; a large amount bonds the board into the box. The standoff
> exists to insulate the input node from the board surface. Cured CA is hygroscopic and
> `sessions/2026-08-31-results.md` already says it "conducts at exactly the level measured".
>
> **The sign of the output points somewhere specific.** For a transimpedance amplifier, a leak to
> the **negative** rail pulls current out of the virtual-ground node, so the op-amp must supply it
> back through the feedback resistor — which drives the output **positive**. The measured output is
> positive, and `IC1` pin 4 is the −15 V rail sitting **2.54 mm** from the input pad.
>
> ### THE RAIL-LEAK MODEL FAILED ITS OWN TEST, 2026-09-07
>
> The prediction was explicit: reduce the −15 V rail and the leak must fall in proportion.
>
> | | |
> |---|---|
> | Rail reduced from −15.237 V to **−9.264 V** | a 39% cut |
> | Predicted ADC reading | **~19,000 counts** |
> | **Measured** | **30,175 counts** |
>
> **No proportional response.** A resistor obeys Ohm's law immediately; this did not. There was a
> slow ~8% downward drift over minutes, more consistent with a thermal side effect than a leakage
> path.
>
> **This undermines the mechanism that A0, A and C all depend on.** Every one of them is surface
> conduction, and surface conduction needs a voltage at the far end. Bias, Z and the negative rail
> have all now been swept with no proportional response, and a path to ground cannot drive current
> into a virtual ground. **There may be no voltage left to drive a surface leak.**
>
> **But see fault 1c before acting on that.** The instrument those sweeps were taken with has a
> floating reference.

### 1c. Three results from 2026-09-07 are IN DOUBT

Recorded prominently so nobody treats them as settled.

| Result | Why it is in doubt |
|---|---|
| **Bias sweep: no response** | The ADC's reference floats (fault 0a). The reading may be dominated by the reference rather than the preamp |
| **Z sweep: no response** | Same |
| **Rail scaling: no proportional response** | Same, **and** the amplifier may be saturated at +11.9 V and unable to respond to anything |

**All three must be repeated with a meter on PAD1, after the reference is fixed.**

**What is NOT in doubt** is anything taken with a meter: PAD1 at 11.905 V, R23 at 11.914 V, the
floating `PREAMP-`, and the rail voltages.
> And `IC1` pin 3 is GND, directly between pins 2 and 4, which guards a straight-line surface path.
> So the leak more likely goes over or around the pins, which is what a blob of glue and a standoff
> would do.
>
> **The test: scale the rails independently, not together.** If the offset follows the negative
> rail and ignores the positive one, this candidate is confirmed.

> ### Every other voltage in the instrument has the WRONG SIGN — added 2026-09-07
>
> This is the sharpest argument the project has, and it came out of correcting a mistake: the bias
> has been on the whole time, not off. Working out what that implies narrowed things rather than
> widening them.
>
> Nothing had commanded a DAC before the 2026-08-31 capture, so by `docs/DAC_BOOT_STATE.md` every
> DAC sat at **zero scale**, and the inverting output stages flip each one:
>
> | Source | Where it sits | Would drive the preamp output | Matches the measured **+11.905 V**? |
> |---|---|---|---|
> | Sample holder, via bias | DAC −3 V → holder **+3 V** | negative | **No** |
> | Piezo electrodes, DSUB1 | DAC −10 V → DSUB1 **+10 V** | negative | **No** |
> | Preamp **+15 V** rail | **+15 V** | negative | **No** |
> | **Preamp −15 V rail** | **−15 V** | **positive** | **YES** |
>
> **A leak from any positive source pushes current INTO the virtual-ground input, which drives the
> output negative. The output is positive. So the source must be negative — and the only negative
> voltage anywhere near the input node is the preamp's own −15 V rail.**
>
> That is on the preamp board, which is exactly where the glued PTFE standoff sits, 2.54 mm from
> `IC1` pin 4.
>
> **Caveats, and they matter.** This rests on the ADC being signed two's complement (INFERRED, not
> confirmed) — if it were unsigned every row flips. It assumes no DAC was commanded earlier in that
> session, which is not recorded. And the hourly DAC configuration loss means the real outputs are
> never certain.
>
> **But every caveat is cheap to close, and with no tip fitted all three tests are zero-risk:**
> sweep the bias and watch the offset; sweep Z and watch the offset; scale each rail separately.
> **If the offset ignores bias and Z but follows the negative rail, the diagnosis is complete —
> and the signed-ADC question is settled at the same time.**

> ### WARNING added 2026-09-07 (late): the noise figures may be void entirely
>
> Computed against the datasheets for the first time: the measured **195 mV RMS** (623 counts at
> the corrected 0.3125 mV) is about **1,700x** the 100 MΩ resistor's Johnson noise and roughly
> **10,000x** the OPA627's own contribution. **Neither device explains it.**
>
> **The prime suspect is the floating `PREAMP−` wandering — that is, the "noise" may not be the
> preamp at all.** It also fits the hour-long warm-up. **If so, every noise figure in this project
> is void, including "the shield nearly halved the noise".**
>
> **Two-minute test:** watch PAD1 on a meter while the ADC scatters. See
> `docs/NEXT_SESSION_PLAN.md` M2.

> ### The noise is several hundred times the theoretical floor
>
> The 100 MΩ feedback resistor's own Johnson noise is about **12.9 fA/√Hz**, which over the
> transimpedance bandwidth gives roughly **1 pA RMS**. The measured noise was **780 pA RMS**.
>
> That is far too much to be the resistor, and it points at **pickup** — and the shield was
> discontinuous when that capture was taken. **So the offset and the noise may have different
> causes:** contamination for the DC, the broken shield for the noise.
>
> **Consequence for the shield test: record the standard deviation, not just the mean.** The old
> plan only compares offsets against 29873 counts. The shield should show up most clearly in the
> noise, and there is a lot of room to demonstrate an improvement even if the DC offset does not
> move at all.

> ### The board cannot be removed, and cleaning is therefore partial
>
> It is heavily glued to three standoffs that are printed as part of the box. The top surface can
> be cleaned — worth doing, since the input pad is a top-side SMD pad and bloom is a surface
> deposit. **Underneath cannot.** So a clean-and-remeasure that shows no improvement **does not
> clear the superglue.** Replacing the board also means a new box print.

**Ranking them by impedance, added 2026-09-06.** For surface leakage to push current into the
preamp's input, that input is a **virtual ground**, so the current is set by whatever voltage sits
at the far end of the leakage path divided by its resistance:

| Source at the far end | Path resistance needed for 119 nA | Plausible for a surface path? |
|---|---|---|
| A ±15 V supply rail | **405 MOhm** | **Yes** — very typical of a contaminated surface |
| A 0.5 V galvanic cell on the shield | **13 MOhm** | Low. That is a poor insulator, not a contaminated one |

**This favours the contamination hypotheses (A and C) over the shield (B) as the DC offset
source.** It does not clear the shield — a floating shield is still a real noise problem and still
needs grounding — but the arithmetic says the offset more likely comes from a rail leaking to the
input node across a dirty surface.

**A cheap discriminating test follows:** if the offset is rail-to-input leakage, it should **scale
with the rail voltage**. Drop the supply from ±15 V to ±10 V and the offset should fall by about a
third. If it does not move, the source is not the rails.

**Test order revised 2026-09-07.** Two cheaper and more decisive tests now come before the shield
work: **the coax bisection** (candidate D, one reading, made possible by the cut) and **independent
rail scaling** (candidate A0). Both are reversible, neither consumes the spare board. The shield
test follows — and it still requires the continuity check first, **and a closed box.**

> **The preamp box is currently OPEN. The lid is off and the back has been cut away for probe
> access.** An open box is not a shield. Offset numbers taken in that state are measurements of an
> **unshielded** preamp and must be labelled as such. A D3 result taken with the box open would
> understate the shield and could wrongly send us to consume the spare board.

- **IPA will not remove cured CA.** It needs acetone or a nitromethane debonder, neither
  attractive around an air-wired node.
- **Rebuild rules** are in `sessions/2026-08-31-results.md` section 6.
- **Acceptance test**, used for either fix:
  `python adc_stats.py -n 50 -i 9.0 --tag "<what changed>"`, bench clear, nobody within a metre,
  ten minutes. Settling near 0 counts means fixed. A few thousand counts means a large
  improvement with some residual leakage. Settling near 29873 again means that candidate was not
  the cause. Ramping to a rail means a genuinely open feedback path, which would be a build error.

### 1b. Preamp BOX shield — rebuilt 2026-09-06, continuity not yet verified

> ## THERE ARE TWO SEPARATE SHIELDS. DO NOT CONFUSE THEM.
>
> | | What it is | Status |
> |---|---|---|
> | **Preamp box shield** | `1_preamp_box` — **35 × 29 × 21 mm**, around the **preamp board only** (the board is 20.6 × 15.2 mm) | **Rebuilt 2026-09-06.** All copper, seams soldered, one ground wire. **Continuity NOT yet metered** |
> | **Scan head shield cover** | `6_shield_cover.stl` — **142 × 128 × 112 mm**, drops over the **whole scanning module**. Also wants copper tape and one ground bond | **Printed, wrapped in copper, and grounded.** Reported by Jacob, 2026-09-06. Not independently metered — if 60 Hz ever dominates an image, re-check this before assuming anything else |
>
> **Everywhere in this file, "the shield" means the PREAMP BOX** unless it says otherwise. The two
> carry the identical instruction — copper tape, grounded at one point — which is exactly why they
> get mixed up.
>
> **The sizes settle it:** 142 × 128 × 112 mm versus 35 × 29 × 21 mm. Measured from the STLs, in
> `CAD/prints/README.md`.
>
> Berard uses both: the preamp sits in its own box on the head, **and** a metal can goes over the
> whole instrument during scanning. He is explicit that without the outer one, *"the images
> produced by the STM are dominated by 60 Hz noise pickup"*.

**Metered on 2026-09-06. Both earlier descriptions of this were wrong.**

The shield was neither "floating" (as `sessions/2026-09-01.md` recorded from a verbal report and
never measured) nor grounded. It was **discontinuous and partially grounded**:

| Check, as found | Result |
|---|---|
| Continuity across the shield tape | **Beeps in places, open in others.** Not one conductor |
| Copper tape touching aluminium tape | **Yes, in many places** |
| Shield to circuit ground | **Beeps in places, not others** |

A ground wire had been added to the **outside** of the box **after 31 August** — late in a session,
to see whether the preamp might not need rebuilding — and was never written down. It grounded
whichever tape patches it reached; the rest stayed floating. Aluminium tape adhesive is an
insulator, which is the likely reason the overlaps did not conduct.

> **This would have produced a false negative.** Block D3 tests "ground the shield and re-measure",
> and a null result sends the project into consuming the only spare preamp board. With a
> discontinuous shield that test would really have been "one patch grounded", and could have read
> "no improvement" even if the floating shield were genuinely the cause.

**What was done, 2026-09-06:** aluminium tape stripped completely, box re-covered in **copper only**,
**seams soldered**, one ground wire attached. All on the outside of the box, so the air-wired
100 MOhm resistor and the IC1 pin 2 input node were never approached.

**The galvanic cell is now eliminated by construction** — there is no dissimilar metal left in the
assembly. It was never disproved; it was removed.

> **VERIFY BEFORE ANY OTHER PREAMP WORK.** The acceptance test was not run:
> **every point on the shield must beep to the ground wire** — near the wire, the far corner, and
> across every seam. Until that passes, a D3 result still means nothing.

**Rules that still apply:**

1. Bond the shield to circuit ground **at one point only.** Multiple bonds create a ground loop.
2. **Solder to copper.** Aluminium cannot be soldered, and a pressure contact on aluminium grows
   an insulating oxide skin and fails later.
3. **Do not reintroduce aluminium tape.** `docs/START_HERE_gotchas.md` says the two are not
   interchangeable because of solderability; the galvanic couple and the non-conducting overlaps
   are two further independent reasons.
4. **Never assume tape conducts to itself.** Check continuity across every seam with a meter.

### 1d. C2 is reverse-connected in the source design — CHECK BEFORE POWERING THE PREAMP

> **UPDATE 2026-09-13, MEASURED on the spare board.** C1's stripe is on its far pad (correct);
> **C2's stripe was on its far pad — reversed, exactly as designed.** C2 marking `475V` = 4.7 µF,
> **35 V** (AVX voltage code). **Rotated at the bench with two irons, reusing the original part** (no
> spare accessible). Afterwards 4.65 µF on the board. Vishay TN-0004 says a tantalum held over 3 s
> should be replaced with a fresh one, so **the reused part is temporary: replace it with a fresh part
> — the 4.7 µF 50 V 1812 ceramic — before this board connects to the controller** (safety rule 14).
>
> **Old board:** stripes not checked. **Its C2 ground end floats** (fault 0d), so it was probably
> never reverse-biased by the rail. The warnings below about weeks at 15 V reverse were written before
> that was known.

**Found 2026-09-09, in the design files. Not measured on hardware.**

The preamp's Eagle source and its gerber pin attributes agree: **`C2`'s tantalum anode sits on the
−15 V rail and its cathode on ground.** Ground is the more positive node, so as drawn the part is
**reverse-biased by the full rail voltage.** C1, on the positive rail, is correct.

A tantalum's reverse rating is a small fraction of its forward rating — typically quoted around
10%, often capped near 1 V. At 15 V reverse it leaks, self-heats, and this is the classic tantalum
short-and-ignite failure.

**This is an upstream design error, in the board we fabricated from. Nobody here caused it.**

> ### It cannot explain the 119 nA. Established 2026-09-09.
>
> **The input node is galvanically isolated.** `N$4` has exactly one connection in the whole
> design — `IC1.-IN`. One pad, no track, no via. C2 connects the −15 V net to GND and touches
> neither.
>
> **And C2's pads sit at −15 V and 0 V whichever way the part faces.** The copper, the soldermask
> and any contamination on them see an identical voltage map either way, so the surface-leakage
> picture toward the input pad is unchanged. The only thing polarity alters is leakage *inside*
> the capacitor, anode to cathode, which flows −15 V to GND entirely within the supply loop.
>
> **Nor the other symptoms.** The 45-minute warm-up drift does not fit: C2 sits 7.1 mm from IC1,
> a 6032 part on a 20 x 15 mm board settles thermally in a minute or two, and raising it 1 degree
> would need roughly 10 mW, about 0.7 mA of leakage, which would be obvious on the supply. The
> rail measured -15.237 V on 2026-09-07, healthy. The OPA627's PSRR is over 100 dB.
>
> **So this is a reliability item, not a lead.** Do not let it delay the rebuild, and do not
> re-rank the 119 nA candidates because of it.

> **UNKNOWN: how C2 is actually fitted on our physical board.** Nobody has looked.
>
> **Two things established 2026-09-09 that sharpen this, and one that de-escalates it:**
>
> - **There is no polarity marking on the silkscreen.** Both C1 and C2 pads carry an identical
>   plain rectangle (aperture D16 in `tunnelAmp-F_Silkscreen.gbr`); the Eagle footprint's anode
>   stripe sits on layer 51 (tDocu) and is never plotted. So "they fitted it against the
>   silkscreen and got it right" **is not available as an explanation** — there was nothing to
>   fit it against.
> - **JLCPCB raised this at order time.** Jacob, 2026-09-09: they could not determine the polarity
>   of C1 and C2 and asked. **How it was answered is UNKNOWN** — it is in the order email, not in
>   this repository. See `docs/INVENTORY.md`.
> - **It cannot be causing the 119 nA**, so it does not block the fault investigation. See below.

**The check — two minutes, board unpowered.** On an SMD tantalum the printed stripe marks the
**anode**. (On an aluminium electrolytic it marks the cathode. They are opposite.) Buzz each C2
terminal to JP1 pin 1:

| Result | Verdict |
|---|---|
| **Striped end beeps to ground** | Correct. Nothing to do |
| **Unstriped end beeps to ground** | **Reverse-biased. Fix before powering** |

> **C1 IS CORRECT. DO NOT ROTATE OR REPLACE C1.** Its anode is on +15 V, which is right. Only C2
> is in question. Rotating both would reverse-bias the good one and create the fault on the
> positive rail.

**If reversed:** replace C2 with a **4.7 µF 50 V X7R ceramic**, **1812 package** — a two-pad
rework, and a ceramic is not polarized so it cannot recur. **1812, not 1206/1210:** the pads are
2.750 x 1.800 mm at 5.250 mm centres, so the gap is 2.500 mm; a 3.2 mm part lands only 0.35 mm on
each pad, an 1812 lands a full 1 mm.

**Prefer replacing to rotating.** Rotating the tantalum works electrically and costs nothing, but
if it has been reverse-biased it has sat at 15 V reverse for weeks, and a tantalum that survives
that has a degraded dielectric. Rotating puts a stressed part back on the rail.

**A 6032 tantalum has two large thermal pads.** Removing it wants hot air or two irons; one iron
is how pads lift, on the small board that carries our input node. Clean thoroughly afterwards.

**Worth checking on the old board too.** It has been powered for weeks, and a reverse-biased
tantalum on the negative rail is a candidate for rail behaviour nobody has explained.

---

### 2. `CCON` jumps Z to midscale and will crash a tip

**Found 2026-09-05 by cross-referencing Dan Berard's write-up against our source. Not yet fixed.**

`turn_on_const_current()` assigns `dac_z_control_value = stm_status.dac_z` and **nothing ever reads
it.** `control_current()` computes `int z = (pTerm + iTerm) + 32768` with midscale hardcoded, so
the first call after `CCON` drives Z to roughly 32768 **wherever Z actually was.**

From Z = 15000 that is a ~17000-count step, roughly **180 nm toward the sample** using Berard's
34 nm/V disc figure. Tunneling happens under 1 nm. Berard documents this exact failure on his own
build: *"the feedback will cause a small jump in the Z-piezo when it's switched on, which crashes
the tip!"*

> **Rule until fixed: never send `CCON` with a tip in tunneling range.** Expect Z to snap to
> midscale on engage.

**Fix, not applied and not bench-tested:** seed `iTerm = stm_status.dac_z - 32768` in
`turn_on_const_current()`, so the loop's first output equals the current Z. See
`docs/UPSTREAM_BERARD.md` §1.1.

### 3. The stepper motor is left energised, which heats the scan head

**Found 2026-09-05, same source. Not yet fixed.**

`EfficientStepper::step()` calls `enable()` and never disables afterwards. `disable()` is called in
exactly one place — inside `approach()`, on success only. After any `MTMV` the motor sits powered
and warming.

Berard: *"The motor produces a substantial amount of heat, which can cause the scanner to drift out
of range within minutes."* The 28BYJ-48 is geared and holds position without holding current, which
is why a geared motor was chosen in the first place.

**Prime suspect if drift ever appears minutes into a session.** Fix is to call `disable()` at the
end of `step()`. Not applied, needs bench testing.

### 4. DACs lose configuration — NOT time-triggered, and lit at every power-on

All four go at once. LED1–LED4 light. Every DAC output goes dead. `RSET` restores it.

> **Two things measured at the bench on 2026-09-07:**
>
> **The idle test passed.** 30 minutes powered with **no commands sent at all**, then LED1–LED4
> checked: **still dark.** Idle time alone does not trigger it. Something we *do* provokes it.
> This question has been ambiguous since 31 August and is now settled.
>
> **They are lit at EVERY power-on, before any command is sent.** Nuh reports this happens without
> exception. That matters because `main.cpp` `setup()` calls `stm.reset()`, which calls `.reset()`
> on all four DACs — **the firmware does configure them at boot, and that configuration fails every
> single time.**
>
> **Untested hypothesis for the power-on half:** the Teensy is powered by USB and boots within
> milliseconds, while the DACs' 3.3 V comes from U16 off the bench supply. Plug USB in first and
> the firmware writes its configuration to chips that are barely powered. **The two-minute test:
> bench supply ON first, wait, then plug in USB. If LED1–4 come up dark, that is the answer and the
> fix is free.** These may be two separate faults with two separate causes.

**Software cannot detect this.** The ALERT pins go to the LEDs and nowhere else, they are not
wired to the Teensy, and there is no DAC readback because H1 carries no MISO for the DAC bus.
`GSTS` will happily report `dac_z = 65535` while the chip outputs nothing — the status fields are
firmware bookkeeping, not measurements.

> **Rule: look at LED1–LED4 immediately before and immediately after every measurement.
> Any reading taken with one lit is void.** This cost an hour on 2026-08-31.

> ## RE-RANKED 2026-09-07 (late): the floating-pin hypothesis is very likely WRONG
>
> **The AD5761R's `RESET` pin has an internal pull-up and may be left floating. So does `LDAC`.**
> Read from the datasheet 2026-09-07. The 20 unconnected pads found in the netlist are **by design
> and permitted**. The hypothesis below required those pins to be genuinely undriven. They are not.
>
> **The correct explanation was already in this repository.** `docs/PROJECT_HANDOFF_SUMMARY.md`
> lines 476–495, under "THE OPERATING RULE THAT MATTERS MOST", explains it completely as **power
> sequencing**: USB boots the Teensy in milliseconds, `setup()` writes DAC config into chips whose
> analog supply is not up, and the writes go nowhere. `setup()` never runs again because USB keeps
> the Teensy alive.
>
> **Nuh's 2026-09-07 data fits it exactly** — lit at **every** power-on without exception, cleared
> by `RSET`, and **not** triggered by 30 minutes of idle.
>
> **So: do not solder the two-wire fix.** It is very likely unnecessary. **The fix is operational
> and already written down: send `RSET` after powering the analog supply, every time**, or power the
> analog supply before connecting USB.
>
> Still **[UNVERIFIED]**: whether `CLR` specifically also has an internal pull-up. One datasheet
> page. It does not change the conclusion, which rests on the power-on evidence.

### 4a. The superseded floating-pin hypothesis — moved out 2026-09-08

For a week the leading explanation was that CLEAR# and RESET# float and glitch together. **The
AD5761R datasheet removed its basis: `RESET` and `LDAC` have internal pull-ups and may be left
floating.** The 20 unconnected pads are permitted by design.

**The full text, with its netlist evidence and the three independent confirmations that the pins
are physically open, is preserved verbatim in `sessions/2026-09-06.md`** under "Appendix, moved
here 2026-09-08". It was moved out of this file because a live-state document should not carry a
dead hypothesis inline.

### 4b. U13's unused op-amp channel is left floating — a new lead, not a confirmed fault

**Found 2026-09-06 in the same netlist recount.** U13 is an **OPA2227P dual op-amp**. Channel A is
the **bias buffer that drives the sample**. Channel B — pins 5 (+IN), 6 (−IN) and 7 (OUT) — is
connected to **nothing at all**.

That is a recognised design defect rather than a normal spare. An op-amp channel with floating
inputs can drift to a rail or oscillate, and it shares a die and both supply pins with the channel
next to it. Whatever it does couples into the bias line, and the bias line goes straight to the
tunnel junction.

**The same package is wired correctly elsewhere on this board**, which is the evidence that this is
an oversight: on U9 and U10, channel B's non-inverting input is tied to AGND. On U13 it is open.

| | |
|---|---|
| **Confidence** | The pins are open: **CONFIRMED** from the netlist. That it is *causing* a problem: **UNKNOWN** |
| **Predicted symptom** | Noise or slow drift on the bias line that does not track the commanded bias |
| **Test** | Scope U13 pin 7 with the board powered. A quiet DC level is fine; a rail or an oscillation is not |
| **Fix** | Two short wires: **pin 6 to pin 7**, and **pin 5 to AGND**. That makes it a unity-gain follower on 0 V, which is the standard treatment. Low risk, no track cutting |

Not on the critical path — the preamp is — but it is cheap, and bias noise is the kind of thing
that would otherwise be blamed on the preamp.

### 5. One JP1 ground pin is open — PROMOTED 2026-09-07, this is fault 0a

> **EXPLAINED 2026-09-13.** Pin 4 is not a one-off routing defect. It is one of six GND points left
> unconnected because the fabricated boards have no ground pour — see fault 0d. **On the spare board
> hole 4 is left empty**; a single ground lead goes in hole 1, and at the DSUB2 splice **green (AGND)
> and brown (`PREAMP−`) both join that lead.** The bond described below is for the old board only,
> and is moot while that board's +IN floats.

> **This is no longer a loose end. It is `PREAMP-`, the ADC's differential reference.**
>
> On 2026-09-07 DSUB2 pin 2 (brown, `PREAMP-`) measured **"2 V and dropping"** — the signature of
> a node connected to nothing. That is the negative input of the differential pair the ADC
> measures against. **Every ADC reading in this project has been referenced to it.**
>
> The 2026-08-31 observation of "two pins wander" was correct and complete. The two are the output
> (legitimately at 11.9 V) and this floating ground return. Only the ranking was wrong.
>
> **Fix it first, before anything else.** See "Next actions".

Measured empirically on 2026-08-31: two pins wander when only one should. The handoff document
retracted this finding once; **the retraction was wrong.**

**The numbering is now known**, extracted from the preamp gerber's embedded netlist on
2026-09-06:

| Pin | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Net | GND | **+supply** | **OUTPUT** | GND | **−supply** |

**Orientation rule, unambiguous because the layout is asymmetric:** the **negative supply sits at
the very end** of the row; the **positive supply is one in from the other end**. The middle pin is
always the output. So measure the two supplies and the numbering follows, with no reliance on
silkscreen.

> **This retires the earlier "do not run a wire between JP1 pins" rule.** That existed only because
> the numbering might be mirrored, making a supposed ground actually −15 V. Pins 1 and 4 are both
> GND on the board, so once they are identified by the rule above, bonding the open one to the good
> one is electrically correct. See `docs/WIRING.md` §10.

This was previously filed as "resolves itself when the board is rebuilt". **That was wrong twice
over** — it is the measurement reference, and it is repairable without a rebuild.

**Next step, and it is the top of the whole list:**

1. Continuity, unpowered: **JP1 pin 1 → ground**, and **JP1 pin 4 → ground**. One will be open.
2. Continuity: **the brown DSUB2 wire → JP1 pins 1 and 4.** That says whether the break is on the
   board or in the cable.
3. **Bond the open ground.** Pins 1 and 4 are both GND on the board, so this is electrically
   correct — the old prohibition was retired on 2026-09-06.
4. Re-measure everything.

---

## Next actions, in order

### Current list, 2026-09-14 — the spare board's ground repair is done

**The full bench procedure is in `docs/NEXT_SESSION_PLAN.md`. This is the summary.**

> **~~1. Finish the ground repair.~~ ~~2. Verify it.~~ DONE 2026-09-14.** All four wires on, eight
> continuity readings and one capacitance reading, all pass. IC1 pin 3 beeps to hole 1.
> `sessions/2026-09-14.md` §3.1 has the table.

1. ~~**Continuity at the four lead free ends.**~~ **DONE 2026-09-14 late, all six readings as
   expected.** Probe map: `docs/preamp_partB_probe_map.html`. **Lead colours recorded for the first
   time:** hole 1 GND white, hole 2 +15 V grey, hole 3 OUT orange, hole 4 empty, hole 5 −15 V tan
   (`docs/INVENTORY.md`). **These are the preamp's own jumper leads and do NOT match the J1/J2
   colours in `docs/WIRING.md`.**

1b. ~~**Wash the board.**~~ **DONE 2026-09-14 late.** 99% IPA, drying overnight on a lint-free pad.
   **The distilled-water rinse was dropped** — no oven or dehydrator exists, and without a bake
   water under IC1 or the 1812s is a leakage path that would **mimic the warm-up drift we cannot yet
   explain.** Two things about the wash were not recorded: **whether it was bathed or brushed**, and
   **what the lint-free pad actually is** — a plain wipe is fine, a treated or pre-moistened one
   would leave residue on a just-cleaned input node. See `sessions/2026-09-15.md` §3.3.
2. **The current-limited smoke test** on the bench supply, Part C — **but only once the board is
   confirmed dry.** Both channels 5.0 V, **20 mA limit**, each output metered before anything is
   connected, then 10 minutes at 15 V with C2 not warm. **Not the controller.**
   > **"Both currents within 1 mA of each other" is RETIRED, 2026-09-14**, at Jacob's objection.
   > Our supplies cannot resolve it, and **it could never have changed a decision: C2 is replaced
   > before the controller regardless** (safety rule 14), so a *mildly* degraded C2 is not a finding.
   > **The pass is: neither channel at the limit, neither climbing, nothing warm.** No resolution
   > needed. A multimeter in series with one supply lead beats the supply's own display if a real
   > number is ever wanted.
3. ~~**Fit the standoff after the wash — it drops in.**~~ **DONE 2026-09-15, and the fit claim was
   wrong.** The 11301 **does not enter our Ø2.108 mm hole** — offered up at the bench and it would
   not go. **The node was built anyway, with the standoff resting on the board surface**, held by
   the 100 MOhm's own lead in tension. **Nothing was glued, drilled or forced**, so safety rule 10
   holds. **Its through-board diameter is UNKNOWN** — no calipers — and the retired 2.032 mm figure
   came from a distributor table. **Do not drill this hole**: the node is now built over it, we do
   not know the target size, and it is 2.54 mm from the board edge at the input node. **Any future
   board order should draw this hole at Keystone's recommended Ø2.184 mm.**
4. **Buy:** 99% IPA, distilled water, foam swabs, a soft brush; **the 4.7 µF 50 V 1812 ceramics**
   to replace the reused C2; copper tape with conductive adhesive.
5. **Then Part D:** wash the board, fit the standoff, build the input node, and take **the first
   valid preamp measurement this project has ever had** — PAD1 on a meter, bench supply, no box, no
   tip lead, readings at 1, 5, 10, 20, 45 and 60 minutes.
6. **Optional, and still the quickest way to learn whether the 119 nA was ever real:** on the old
   board, wire IC1 pin 3 to its JP1 pin 1 — **pin 3 only, not C2** — power it and meter PAD1.

### The list below was written 2026-09-07 and refreshed 2026-09-09

**Items 1, 5 and 6 are moot as written** (struck through below): they measure the old board, whose
+IN floats. Items 2–4 continue in the current list above.

> **Reordered 2026-09-07 (late).** The previous order had "bond the open ground" ahead of "check
> the ADC's absolute maximum". **That was backwards and it put the converter at risk** — see
> `CLAUDE.md` §3c, which exists because of it.
>
> **The order below does not depend on the absolute-maximum rating at all**, because the preamp
> rebuild can be validated with a meter at PAD1, which does not involve the ADC.

### Purchase blocker, added 2026-09-09 — read before planning a soldering session

**The flux arrives 2026-09-11. The things that remove it were NOT ordered.** No 99% IPA, distilled
water, soft brushes, lint-free wipes or foam swabs. **Rosin flux left on this board is a leakage
path at the exact node the 119 nA fault sits on.**

~~**Do not solder the preamp until the cleaning kit is in the room.**~~ **CLOSED 2026-09-14 late:
the kit is complete** — 99% IPA, DI water, foam swabs and soft brush are all in the room.
Still unbought: **copper
tape with conductive adhesive** for the shield — aluminium will not do. See
[`docs/PREAMP_SHOPPING_LIST.md`](docs/PREAMP_SHOPPING_LIST.md).

**When the screws arrive: use the M2x6, not the M2x8.** The box pilot is 5.00 mm deep and blind;
an M2x8 bottoms out and cracks the boss. **Calipers on the board first** — its thickness is assumed,
not measured. Drive slowly, stop at snug; the thread is plastic.

### One required unpowered check, added 2026-09-09 — do it before anything is switched on

**A. ~~Check C2's polarity.~~ DONE 2026-09-13 on the spare board: reversed, then rotated** (fault 1d). The old board's is still unchecked. Original text: Two minutes with the beeper and a magnifier, board unpowered. See
fault 1d. **Not a blocker** — established 2026-09-09 that it cannot cause the 119 nA, and the
board has already run powered for weeks on a healthy rail. But a reverse-biased tantalum is a
known degradation mode, JLCPCB flagged the polarity at order time, and there is **no polarity
marking on the silkscreen** to have guided them. **C1 is correct — do not touch C1.**

**B. While the magnifier is out, read the op-amp's package marking.** Optional, and it blocks
nothing. **OPA627AU is expected** — that is Mech Panda's part and our parts follow Mech Panda; the
Eagle source says `OPA124U` only because the PCB is Berard's design. **Both work here**, ~1 pA bias
current either way. Reading it just pins the stability margin (~7x vs ~2x).

### Then these — none of them touch the ADC

1. ~~**Measure PAD1 with a meter at 10 minutes and again at 60 minutes after power-on.**~~
   **MOOT 2026-09-13:** the old board's +IN floats, so its PAD1 drift is not the preamp's.
   Replaced by the 45-minute readings on the repaired spare. Original text kept:
   Five minutes of work, and it settles what the hour-long warm-up actually is.
   - **PAD1 steady while the ADC counts climb** → the drift is the floating `PREAMP-` charging,
     not the preamp. The preamp is fine to measure early, and the "wait an hour" rule only applies
     to ADC readings.
   - **PAD1 climbing too** → the drift is real and in the preamp, and every future measurement must
     wait it out.

2. **Reprint the preamp box — but print the ORIGINAL base, not v2. Corrected 2026-09-08.**
   The old *physical* box still cannot be reused: it is full of cured CA. That reason stands.
   **The geometry reason was wrong.**
   > **The box already fits the board.** Both the box's threaded standoffs and the board's two
   > mounting holes are **11.430 mm apart** — Ø2.261 mm clearance over Ø1.600 mm M2 pilots.
   > The retired `5.93 mm` figure was wrong: it was measured between the Ø2.108 mm **PTFE standoff hole** and one
   > mounting hole; the board has **three** non-plated holes and the third, at (4.127, 1.905), was
   > missed. See `docs/FACTS.md`.
   >
   > **Do not print `1_preamp_box_base_v2_screwmount.stl`.** Its added boss at (4.04, 9.12) lands
   > on the PTFE standoff hole — it would put a screw and a carbon-fibre-filled pillar at the
   > input node. §0.3 of the rebuild guide.
   **Consequence: the rebuilt board mounts on two M2 screws and needs no glue.** Check the print
   with calipers before relying on this.

3. **Rebuild the preamp on the spare board.** The leak is on the board — measured, not inferred,
   by the coax bisection. Rules in `sessions/2026-08-31-results.md` §6, plus:
   - **No cyanoacrylate anywhere.** Screws into the new box's pilots.
   - **Do not glue the PTFE standoff.** Keystone 11301, per `docs/UPSTREAM_BERARD.md` §4.
     **We do not own the 11301 — corrected 2026-09-09.** What we have is the **11311** (2 off),
     which needs a Ø3.45 mm hole against our Ø2.108 mm and **would not fit at the bench.**
     **Do not open the hole to suit it** — that leaves 0.815 mm of board to the edge. The 11301
     is on order. See `docs/INVENTORY.md`.
   - **Clean the flux thoroughly** — Berard's own warning, and still a live candidate.
   - **Tip lead in fine wire, not coax** — decided 2026-09-07.

4. **Validate the rebuild with a meter at PAD1, before it goes in any box.**
   **This is a complete acceptance test and it does not involve the ADC**, so the floating
   reference does not block it.

   | PAD1 reading | Input current | Verdict |
   |---|---|---|
   | 11.9 V | 119 nA | unchanged — the fault is not what we think |
   | ~1 V | 10 nA | large improvement, still unusable |
   | **< 0.1 V** | **< 1 nA** | **target.** Leaves the full range for signal |
   | a few mV | tens of pA | what a clean build should actually give |

   **Then box it and measure again.** That isolates the box's own contribution — a number this
   project has never had.

### Then, and only once PAD1 is small

5. ~~**Find and bond the open ground.**~~ **SUPERSEDED 2026-09-13:** pin 4 has no copper at all
   (fault 0d). On the spare, ground and `PREAMP−` both join a single lead in hole 1 at the DSUB2
   splice. The waiting rule below still applies to that splice. Original text kept:
   Continuity from JP1 pin 1 to ground and JP1 pin 4 to ground;
   one will be open. Then continuity from the DSUB2 `PREAMP-` wire to each, to tell whether the
   break is on the board or in the cable. Both pins are GND on the board, so bonding is correct.
   > **Why this waits.** With PAD1 at 11.9 V, bonding `PREAMP-` to ground puts the full 11.9 V
   > across a ±10.24 V input — **16% over range**, and **the absolute maximum rating is still
   > unverified.** Once PAD1 is under 0.1 V there is no question to answer. **Do it in that order
   > and the risk disappears rather than being managed.**

6. ~~**Repeat the bias, Z and rail sweeps with a meter on PAD1**~~ **MOOT for the old board
   2026-09-13** (+IN floats). Worth doing on the repaired spare once it reads small. Original text: not through the ADC. All three are
   in doubt (`sessions/2026-09-07.md` §22) because they were taken through an instrument with a
   floating reference.

7. **Verify the rebuilt shield's continuity** — every point to the ground wire, near the wire, the
   far corner, across every soldered seam.

8. **The AD5761R internal pull-up question.** The one datasheet question still open — but see
   fault 4: the handoff already explains the power-on symptom without needing it.

9. **The four five-minute checks:** calipers on the piezo disc and its Ø20.500 pocket; a ruler on
   the spring droop; a scope on U13 pin 7; a ruler on the scan head lever.

10. **Then the rest:** the DAC config characterisation, counts-to-amps calibration against the now
    known 10.24 V scale, and the ≥100 MΩ dummy junction.

### Only when the preamp is working

**`Code/pc/stm_approach.py`** is written and tested (40 tests, 2026-09-05) but has **never run on
hardware**. It needs both direction answers first: which Z direction approaches the sample, and
which sign of `MTMV` advances.

---

## Standing safety rules — do not violate these

0. **Added 2026-09-07. No preamp measurement is valid until the board has been powered for at
   least 45 minutes.** The offset climbs about **25,000 counts — roughly 30 nA — over more than an
   hour** after power-on, decelerating throughout. Measured at 10 minutes it reads 3,969 counts;
   at 75 minutes, ~29,500. **No procedure in this project has ever mentioned this**, so every
   historical figure sits at an unknown point on that curve. A reading taken early will look like a
   spectacular improvement and is worthless.
   > **Basis in doubt, 2026-09-13:** the climb was measured on a board whose IC1 +IN floats (fault
   > 0d), so it may be that node settling rather than the preamp. **Keep waiting 45 minutes** on the
   > repaired spare until its own readings show whether the rule is needed.

0b. ~~**Added 2026-09-07. Do not rebuild the preamp board, and do not rebuild the tip lead.** The
   instrument that would tell you whether a rebuild helped has a floating reference — see fault 0.
   Rebuilding into that consumes the only spare board and teaches nothing. **Fix the measurement
   chain first.**~~ **SUPERSEDED 2026-09-13 for the preamp board:** Nuh decided at the bench to go
   ahead with the rebuild, because the rebuild is judged with a meter at PAD1 on a bench supply, not
   through the ADC. **The tip-lead half still stands:** do not rebuild the tip lead until the bare
   board has been measured.

0c. **Added 2026-09-07. Do not trust any current derived from ADC counts.** Use a meter on PAD1
   until fault 0 is fixed. Meter readings are sound; ADC readings are referenced to a floating node
   and the converter is being driven past its input span.
   > **Extended 2026-09-13:** on the **old board**, a meter on PAD1 does not give a current either,
   > because IC1 +IN floats (fault 0d). A PAD1 reading means input current only on a board whose
   > pin 3 beeps to JP1 pin 1.

1. **Check LED1–LED4 before and after every measurement.** No software substitute exists.
2. **Do not run `APRH`** until the sign of the tunneling current is known. `approach()` tests
   `read_adc() > target` against a baseline that has been negative all project, so if tunneling
   drives the reading more negative it will never trigger and the tip will drive into the sample.
3. **Do not raise either SPI clock above 1 MHz.** Both buses were at 40 MHz and the ribbon cannot
   carry it.
4. ~~**Do not run a wire between JP1 pins** on the old board.~~ **RETIRED 2026-09-06.** This rule
   existed only because a mirrored pin numbering could make a supposed ground actually −15 V. The
   numbering is now known from the preamp gerber netlist and is identifiable with a meter — see
   fault 5. **This rule and fault 5 contradicted each other inside this file for a day; fault 5 is
   the correct one.**
5. **Do not use cyanoacrylate** anywhere near the preamp, or in the same enclosure, ever.
   Mount with screws or nylon standoffs first, 2-part epoxy second, foam tape third.
6. **Park Z at midscale (32768) before moving the motor.** `RSET` and `TEST` both slam Z to a
   rail, so re-park after either.
7. **Before first imaging, meter-check the tip holder against the brass piezo electrode.** Berard
   warns that glue must not bridge the tip standoff to the grounded brass plate. That path is a
   shunt across the preamp input — it costs signal and adds noise. It is **not** an offset source,
   so it is not a candidate for the 119 nA, but it must be open before imaging.
8. **Never send `CCON` with a tip in tunneling range** until the integral-init bug in fault 2 is
   fixed. Engaging the loop snaps Z to midscale.
9. **No preamp measurement is valid while anyone is leaning over the board.** A person within a
   metre injects 20 to 50 nA, which is twenty to fifty times a tunneling current.
   > **Basis in doubt, 2026-09-13:** the 20–50 nA figure came from a board with IC1 +IN floating,
   > which makes it far more sensitive to a nearby body than a working amplifier. **Keep the rule** —
   > body pickup on a 100 MΩ input node is real — but the number is not established.
10. **Do not glue the spare preamp board to anything — not the box, and not the PTFE standoff.**
    Added 2026-09-07. Superglue was used twice on the current board: a little to stick the PTFE
    standoff down, and a lot to bond the board into the box. **Both are now suspects**, and the
    first sits directly across the insulator that holds the input node. Gluing the spare the same
    way reproduces the fault and makes the rebuild untestable.
    - **Measure the spare bare first** — on nylon or PTFE standoffs, no box, nothing glued. There
      has never been a measurement of this preamp outside its box, so **the project has no
      baseline.** That single reading is worth more than the whole D1/D2/D3 sequence.
    - **The box print does NOT need fixing — corrected 2026-09-08.** Both its threaded standoffs
      and the board's two mounting holes are **11.430 mm apart** and they match exactly. The old
      retired `5.93 mm` figure was wrong — it paired the PTFE standoff hole with a mounting hole. Reprint the **original**
      base for cleanliness only. See `docs/FACTS.md` and §0.3.
11. **Do not bring the sample plate near the tip holder** until the offset is understood.
    **Corrected 2026-09-07** — an earlier version of this rule said the bias was off. It is not;
    it has been on throughout, with the plate simply parked away from the tip. The rule that
    matters is the physical separation, not the bias.
    - **Do not fit a tip either.** Without one, nothing can be crashed, and every test below —
      bias sweep, Z sweep, rail scaling — is zero-risk. That is worth preserving until the offset
      is understood.
12. **A multimeter cannot clear a suspect leakage path in this project.** What matters here is
    100 MΩ to 10 GΩ. A typical DMM tops out around 20–60 MΩ, so **"OL" only proves ">60 MΩ"** and
    leaves the entire dangerous range unmeasured. **Never read OL as "ruled out."** The instrument
    that reaches into that range is the rail-scaling test.
13. **Type DAC commands carefully. An out-of-range value does not error — it silently jumps the
    axis to the opposite rail.** Found 2026-09-06 by reading the driver. `set_dac_z(int)` hands its
    value to `AD5761::write(uint8_t, uint16_t)`, so anything outside 0–65535 wraps modulo 65536
    with no warning:

    | You type | Firmware actually sends | DAC output |
    |---|---|---|
    | `DACZ 65535` | 65535 | +10 V, as expected |
    | **`DACZ 70000`** | **4464** | **−8.6 V.** You asked for the top rail and got most of the way to the bottom one |
    | **`DACZ -1`** | **65535** | **+10 V.** You asked for below zero and got the top rail |
    | **`DACZ`** with no number | **0** | **−10 V.** `parseInt()` times out and returns zero |

    From midscale, each of those is a jump of roughly 8 to 10 V — **hundreds of nanometres**, far
    more than a tunneling gap. **Keep every DAC argument between 0 and 65535, and never send a
    bare `DACZ` / `DACX` / `DACY`.** There is no clamp anywhere in the path: not in `main.cpp`, not
    in `set_dac_*`, not in the driver.
14. **Added 2026-09-13. Do not connect the spare preamp board to the controller until two things
    are true.** (a) **C2 has been replaced with a fresh part** — the 4.7 µF 50 V 1812 ceramic. The
    tantalum on it now was desoldered and refitted, and Vishay says a tantalum heated past 3 s should
    be replaced; the controller's supply, unlike the 20 mA-limited bench supply, can drive a shorted
    tantalum hard. (b) **PAD1 reads under 0.1 V after 45 minutes on the bench supply.** Its
    `PREAMP−` is now grounded at the board, so a high PAD1 would put the ADC past its ±10.24 V range.
    **Do not power it at all until the ground-repair checks in `docs/NEXT_SESSION_PLAN.md` pass.**

---

## Open questions

**`docs/OPEN_QUESTIONS.md` is the single authoritative register.** This section lists only the
handful that gate work right now, and is pruned every session. **Anything resolved is removed from
here** — it stays recorded in `docs/OPEN_QUESTIONS.md` and in the session log that closed it.

| Question | Why it blocks |
|---|---|
| **Is there any real input leakage at all?** New 2026-09-13 | **The top question.** Every reading so far was taken with IC1 +IN floating (fault 0d). Answered by the repaired spare board at 45 minutes, or faster by grounding the old board's pin 3 |
| **Does C3's ground-via stub touch JP1 pin 2's pad?** New 2026-09-13 | The gerbers put them 0.076 mm apart. C3's ground pad ↔ hole 2 must be silent before C3 is grounded, or +15 V gets shorted to ground |
| **Is any partial top-side wire left on the spare board?** New 2026-09-13 | Wires 3 and 4 were first attempted on top and abandoned. A loose bare end near R1 or hole 2 is a short |
| ~~**Where is the break in the `PREAMP−` return — board, cable, or connector?**~~ **ANSWERED 2026-09-13** | On the board: JP1 pin 4 has no copper (fault 0d). Solved on the spare by wiring |
| ~~**Is the warm-up drift the preamp or the floating reference?**~~ **SUPERSEDED 2026-09-13** | Probably neither: IC1 +IN floats. Re-measure on the repaired spare |
| ~~**Is the recorded noise real, or is it the reference?**~~ **SUPERSEDED 2026-09-13** | Same. Every noise figure was taken with +IN floating |
| ~~**Is the OPA627 saturated at +11.905 V?**~~ **SUPERSEDED 2026-09-13** | With +IN floating the question does not have a meaningful answer on the old board |
| **Does the rebuilt preamp box shield conduct end to end?** | Two minutes with a meter, never done. Every shield conclusion rests on it |
| **Is the ~119 nA the CA contamination, or something else?** | The rail-leak mechanism failed its own test. Drives whether the rebuild is the right fix |
| **Which Z direction approaches the sample, and which sign of `MTMV` advances?** | `Code/pc/stm_approach.py` refuses to run without both |
| ~~**Does the piezo disc fit its Ø20.500 mm seat?**~~ **CLOSED 2026-09-09 by construction** | The scanner is built and works. **Do not spend bench time on this.** The nm/V figures still want a real calibration eventually, but that is a scan-calibration job, not a fit question |

> **Closed since this table was last pruned**, and now only in `docs/OPEN_QUESTIONS.md`:
> the ADC full scale (±10.24 V), the output format (two's complement), whether the ADC is damaged
> (very unlikely — it was never over range), why it reads ~30,000 counts (wrong constant), whether
> the AD5761R has internal pull-ups (**yes**), the sample material (gold foil), and the motor step
> size (~4–8 nm).

---|---|
| **Where is the break in the `PREAMP-` return — board, cable, or connector?** | **The top question.** It is the ADC's reference and it is floating. Three continuity checks, unpowered. See Group 0 |
| ~~**Is the ADC damaged?**~~ **Very unlikely** | It was never over range: span ±10.24 V, differential ~9.2 V. **The absolute maximum is still unverified** (every datasheet host is blocked from the remote session) but it no longer gates anything — the action order avoids the over-range case entirely |
| ~~**Why does the ADC read ~30,000 counts?**~~ **RESOLVED 2026-09-07** | Full scale is **±10.24 V**, so ~29,500 counts is **9.22 V**. PAD1 is 11.905 V, so `PREAMP-` sits at about **2.7 V** — and the meter read it as "2 V and dropping". Everything reconciles |
| **Is the OPA627 saturated at +11.905 V?** | If it is pinned, the bias, Z and rail sweeps of 2026-09-07 measured nothing. Decides whether three results stand or are discarded |
| **What causes the 45-minute warm-up drift?** | ~30 nA of climb after power-on. Thermal, moisture in the CA, charge in the PTFE, or the floating node charging. **Untested** |
| **Does the rebuilt preamp box shield actually conduct end to end?** | **VERIFY, two minutes with a meter.** Still not done |
| **Does the AD5761R have internal pull-ups on CLEAR#/RESET#?** | The only fact left that decides whether the four-wire DAC fix is worth doing. **Datasheet question, still nobody has looked** |
| Is the ~119 nA the CA contamination, or something else entirely? | **The rail-leak mechanism failed its own test**, and bias and Z show nothing. There may be no voltage left to drive a surface leak. Decides whether the spare board gets consumed |
| Is the DAC configuration loss startup-only, or does it recur mid-session? | 2026-08-31 recorded it recurring every 30 to 60 minutes, which requires checking LED1–LED4 around every measurement. If it is startup-only, one `RSET` at the start is enough. **Currently ambiguous, needs settling at the bench** |
| ~~Is there a sample material?~~ | **Answered 2026-09-05: gold foil.** It must be mounted flat on a magnetic disc with a conductive path to the bias magnet — see `docs/UPSTREAM_BERARD.md` §5. Expect atomic terraces, not individual atoms; Berard could not resolve single atoms on metals |
| How far does one motor step move the tip, in nm? | **Largely answered 2026-09-05, superseded estimate was 244 nm: roughly 4 to 8 nm.** From the 1/4"-80 pitch and 2048 steps/rev, with a lever reduction Berard quotes as **either 20 or 30 on different pages** — 7.8 nm at 20, 5.2 nm at 30. **Nothing depends on resolving it**: both give 90–130 steps per Z range. **VERIFY our own ratio** — ours is Mech Panda's geometry. Replaces the old 244 nm estimate. See `docs/UPSTREAM_BERARD.md` §2b |
| Which Z direction is toward the sample | Only resolvable at first tunneling, or from the CAD. Park Z at midscale meanwhile. **`stm_approach.py` requires this answer before it will run** |
| Which sign of `MTMV` advances toward the sample | Determinable by eye with the tip removed. **`stm_approach.py` requires this too** |
| ~~ADC full scale: 4.096 or 10.24 V?~~ **CLOSED 2026-09-07** | **±10.24 V**, from the datasheet. REFBUF is 4.096 V and the input span is 2.5 × REFBUF. The PC tools were right. **Two's complement also confirmed from the same page** |
| DST-201 DC input impedance | Needed to finish some of the high-impedance arithmetic |

---

## Known code issues, deliberately not fixed yet

| Where | Issue |
|---|---|
| `stm_firmware.hpp` `approach()` | Signed `>` comparison against a negative baseline. **Routed around** — use `Code/pc/stm_approach.py`, which never sends `APRH`. Left unfixed deliberately |
| ~~`stm_control.py:37`, `stm_console.py`~~ | ~~ADC full scale hardcoded as `10.24`, "wrong"~~ **NOT A BUG. Corrected 2026-09-07: the datasheet gives ±10.24 V. These tools were right and must NOT be changed.** The 4.096 figure is REFBUF, not the input span |
| `LTC2326_16.cpp` `read_volts()` | **Broken upstream**: multiplies raw counts by the REFBUF constant instead of scaling by full scale. Returns nonsense. Never called, so harmless. Do not use it |
| `stm_firmware.hpp` | Duplicate `LTC2326_16` object at file scope and as a class member, same pins |
| `AD5761.cpp` `write()` | Missing `SPI.endTransaction()` |
| `stm_control.py:127` | `send_cmd('MTMV {steps}')` — **missing the `f` prefix**, so it sends the literal text and the motor moves **zero steps**. This is why the GUI's motor control does nothing. Upstream bug, verified 2026-09-06 |
| `stm_control.py:88` | `set_buffer_size()` is **Windows-only** in pyserial. On macOS or Linux the GUI cannot open the port at all |
| `stm_control.py:40-49` | All three axis voltage conversions use ±5 V. Z is **±10 V**, X and Y are **±3 V**. Every voltage the GUI displays is wrong |
| `stm_firmware.hpp:497-498` | Comments say X and Y are ±5 V. They are **±3 V** — same mode bits as bias, which measures ±3 V. Comment only, the behaviour is correct |
| `AD5761.cpp` `write()` | **`reg_data` is `uint16_t`, so every DAC command wraps modulo 65536 with no error.** See safety rule 13 — this is a tip hazard, not a cosmetic issue. Found 2026-09-06 |
| `main.cpp` `SCST` handler | **Seven integers parsed straight from serial with no bounds check.** `y_resolution` indexes `scan_image_adc[2048]` and `scan_image_z[2048]`, so **`y_resolution > 2048` writes past the end of both arrays.** `sample_per_pixel = 0` divides by zero. Keep y_resolution ≤ 2048. Found 2026-09-06 |
| `AD5761.cpp` `write_volt()` | **Never called, and wrong if it were.** `(voltage/2.5 + 4)/8 * 65536` assumes the ±10 V range, so it is wrong for X, Y and bias (±3 V); and at exactly +10 V it computes 65536, which wraps to 0 and outputs −10 V. Same class of trap as `read_volts()`. Do not use it. Found 2026-09-06 |
| `AD5761.hpp` header comments | Document the mode words as `0b0000000101000` (±10 V) and `0b0000000101101` (±3 V). The firmware actually writes `0b0…000` and `0b0…101`. **Only the low three bits agree.** The firmware's words are the ones measured to work; the header's comments are stale. Found 2026-09-06 |
| `checkSerial()` in `main.cpp` | Fires on **one** available byte then reads four without waiting, and leaves the terminator in the buffer after an argument-less command. `stm_console.py` already works around both — it sends one write, and a newline **only when there is an argument**. **Anything else (Arduino Serial Monitor, a hand-typed terminal) will desynchronise**: after `RSET` or `ADCR` the stray newline eats the first character of your next command |

| `check_facts.py:394-396` | **A RETIRED row is silently dead if its replacement's first number also appears in the stale line.** `num = re.search(r'[\d.]+', replacement)` then skips any line containing that number, on the assumption the line is a correction table. **Found 2026-09-14** while retiring `0.076 mm interference` → `0.076 mm CLEARANCE`: both carry `0.076`, so the row could never fire. Worked around by wording that replacement with no shared number, and the row is now regression-tested. **The same weakness makes the `±5 V` → `±3 V` row nearly dead**, because its replacement's first token is `3` and almost every line contains a 3. Not yet fixed |
| `check_facts.py` EXCUSES | **`~~` excuses the whole line**, so in a `docs/OPEN_QUESTIONS.md` table row where only the *question* is struck through and the *answer* cell is live and wrong, nothing is flagged. **This is how the retired press-fit claim survived in two rows until 2026-09-14.** Not yet fixed |
| `check_facts.py` hint text | Tells you to "add a word like `was`" — but bare `was` is **not** in EXCUSES, so following the hint does not clear the warning. Use `corrected`, `retired`, `superseded` or `wrong` |

`logTable[abs(adc)]` is **safe** — the table is `[32769]`. Do not "fix" it.
