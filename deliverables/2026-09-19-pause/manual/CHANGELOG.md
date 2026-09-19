# Change log for the consolidated manual

**What changed between the documentation as it stands and
`deliverables/2026-09-19-pause/manual/MANUAL.md`, written 2026-09-19.**

**Nothing in the existing documentation was edited.** Where this manual departs from a source file,
that departure is listed here, and the file and line that needs the fix is listed in
`INCONSISTENCIES.md` in this directory.

---

## 1. There was no single manual before this

**There is no file in the repository called "the manual", and there never has been.** What exists
is a set of documents that each own one kind of information, plus a bring-up procedure that carries
its own "partly superseded" banner.

| What was missing | Where it was scattered |
|---|---|
| **A start-to-finish operating procedure** | `docs/soft_launch_test_procedure.md` covers powering up from cold, stages 0 to 6, and says so in its banner. It stops there — no scanning, no sample work, no shutdown |
| **A sample and tip procedure** | `docs/gold_leaf_procedure.html` is a bench card for one day's work. Tip fitting is spread across `docs/INVENTORY.md`'s tip-holder row, `STATUS.md` safety rule 7 and `docs/NEXT_SESSION_PLAN.md` |
| **A shutdown procedure** | Only as prose in `STATUS.md`'s "where the instrument is left" blocks, one per session, each describing a different parked state |
| **A "which revision is fitted" statement** | Nowhere. It has to be reconstructed by reading `docs/INVENTORY.md`'s long rows and several session logs in date order |
| **A resume-after-a-break procedure** | The top block of `docs/NEXT_SESSION_PLAN.md`, written the morning of the move, is the only one and it is six numbered lines |
| **Data collection and analysis, as procedure** | `Code/pc/README.md` documents seven of the twelve tools; the analysis method exists only inside the tools' own docstrings and in `sessions/2026-09-17-charts.md` |

**`docs/PROJECT_HANDOFF_SUMMARY.md` is the closest thing to a manual and its body is explicitly
superseded** — `CLAUDE.md` section 3 says never to cite it against a newer document, though its
header banner is a live correction log and is read first.

**So the reading that prompted this work is right: there was no single existing manual.**

---

## 2. What this manual corrects

**Each of these is a place where following an existing document would give a reader a wrong idea of
the instrument. The manual states the corrected version; `INCONSISTENCIES.md` says which file and
line to change.**

| # | Was | Now | Source of the correction |
|---|---|---|---|
| 1 | `docs/COMMANDS.md` says `Code/pc/stm_approach.py` "is planned but not yet written" | **It exists, has 40 passing tests, and is the only approach route used at the bench since 2026-09-16** | The file itself; `Code/pc/README.md`; `sessions/data/2026-09-19-morning/README.md` |
| 2 | `docs/soft_launch_test_procedure.md` Stage 5 says to run `TEST` and listen for a buzz, with "nothing heard" meaning a dead disc | **There is no usable resonance once the disc is mounted. Judge the piezo with a meter, and prefer `TONE`, which parks Z at 0 V** | A 1 kHz to 11 kHz sweep on 2026-08-31 found no loudness peak; `docs/COMMANDS.md` and `CLAUDE.md` both carry this |
| 3 | `SETUP.md` tells every reader to type `python` | **On Windows type `py`** — `python` and `python3` are Store placeholders on Jacob's machine | `Code/pc/README.md`, from what actually happened on 2026-09-16 |
| 4 | `README.md` says the preamplifier is the blocker and is being rebuilt | **The preamplifier works, at about 4 pA in its box. The blocker is mechanical** | `STATUS.md`; `docs/FACTS.md` |
| 5 | `README.md` gives the coarse step as about 7.8 nm and the sample as gold foil on a magnetic disc | **3.9 to 7.8 nm depending on an unresolved lever ratio; gold leaf on copper tape on the plate, no puck** | `docs/FACTS.md`; `docs/INVENTORY.md` |
| 6 | `docs/ENGINEERING_REFERENCE.md` section 11 records the ADC full-scale conflict as "Resolved: 4.096" | **Resolved as 10.24 V.** 4.096 V is REFBUF; the span is 2.5 times REFBUF | The datasheet, 2026-09-07; `docs/FACTS.md`; two other places in the same file |
| 7 | `Code/pc/README.md` and `docs/ENGINEERING_REFERENCE.md` both say the PC tools print currents 2.5 times too large | **The tools are right. Do not change the constant** | Same as above. The end-to-end dummy junction result of 2026-09-16 agrees with the tools |
| 8 | `docs/ENGINEERING_REFERENCE.md` section 7b derives the suspension resonance from the droop | **That model does not apply.** These springs have initial tension, so the droop was never a spring extension | `docs/FACTS.md`, which retired the figure that came out of it; `STATUS.md` |
| 9 | `docs/COMMANDS.md` calls the motor direction provisional | **Settled at the bench 2026-09-17: negative approaches** | `docs/OPEN_QUESTIONS.md`; every later approach that found the gold |
| 10 | `docs/COMMANDS.md` states the body-proximity figure as a measured quantity | **The rule stands; the number is not established** — it came from the board whose amplifier reference floated | `STATUS.md` safety rule 9's own note |
| 11 | The firmware's own comments say X and Y are minus five to plus five volts | **±3 V.** Identical range bits to bias, which measures ±3 V | `docs/WIRING.md`; `docs/FACTS.md`; `CLAUDE.md` names the lines |
| 12 | The firmware's `TONE` comment says to sweep near 8.6 kHz | **Retired advice.** That is a free-air figure for a disc that is not ours | `docs/COMMANDS.md` |
| 13 | `docs/WIRING.md` describes the fitted piezo as an 18 mm buzzer disc | **The fitted part is a Jessinie `91410_30_JE`**, and the 18 mm figure has no provenance | `docs/INVENTORY.md`, `SAID` 2026-09-17 |
| 14 | `docs/BOM.md` says the Keystone 11301 is specified but not owned | **Two were received 2026-09-14 and one is in the instrument** | `docs/INVENTORY.md`, order screen seen |

---

## 3. What this manual explicitly does NOT change

**The brief asked that no conclusion be quietly upgraded. These are the statements the manual
carries forward unchanged, with their hedges intact.**

| Statement | Kept as |
|---|---|
| **No image has been produced** | Unchanged. Every feedback scan is matched or beaten by its own X-held control |
| **"A soft, pressed, sticky contact"** | Kept as **interpretation, not proof.** The contact potential between tungsten and gold is unmeasured, so electrostatics is not excluded |
| **The Z scale in nanometres** | Kept as **inherited and unmeasured.** The "about 6 to 13 counts per decade for tunnelling" comparison depends on it; the hysteresis result does not |
| **The trace/retrace anti-correlation** | Kept as **the loop hunting, with X motion the likely but unproven cause** — the correction made on 2026-09-19 morning, not the earlier "loop lag" |
| **The claim that an X-held control swung Z by 28,000 counts** | Kept **withdrawn and corrected.** That swing was the tool. The gold's own motion was measured separately the next morning and that measurement stands |
| **Safety rule 6, parking Z at midscale before the motor moves** | Kept as **a live disagreement.** Every motor move on 2026-09-19 parked Z at the retracted end instead. **That is Jacob and Nuh's to amend or keep, not ours** |
| **Safety rules 2 and 8** | Kept in force. Both have had their conditions met and **neither has been lifted**, which is a decision for Jacob and Nuh |
| **Whether the suspended platform touches the damping stack** | Kept **unmeasured.** It was read off a photograph as touching and Jacob corrected it within the hour |
| **`d`, the tip-to-pivot-line distance** | Kept **unmeasured, and the photographic route kept closed.** Three attempts gave answers more than a factor of two apart |

---

## 4. What is newly marked UNKNOWN

**Nothing in this manual invents a limit or a procedure.** These are gaps the manual names
explicitly because an operator would otherwise assume they are known.

| Newly flagged | Why it is flagged here |
|---|---|
| **What was taken apart in the move, and how it was packed** | It is the first thing section 11 depends on and nobody wrote it down |
| **Whether the two-turn back-off recorded before the move still describes the gap** | It applies to the tip and the sample that were fitted, and either may change |
| **Whether the new preamp box was metered end to end** | `docs/ENGINEERING_REFERENCE.md` contradicts itself on this. The manual treats it as open |
| **The net change to the tip-to-sample gap from the 2026-09-19 rebuilds** | The sample stack got thicker and the tip got shorter on the same day, by unmeasured amounts, in opposite directions. **The manual says not to assume they cancel** |
| **Where to park Z before a motor move** | See section 3 above. The manual states both practices and says the decision is owed |
| **What the tip holder's metal stake is made of** | Already open in `docs/INVENTORY.md`. The manual raises it to an operating check because a ten-second magnet test settles it |

---

## 5. What was preserved because it was hard-won

**The brief asked that useful detail not be thrown away to make things tidy.** These are the
passages carried into the manual in full rather than summarised, with a note on why each earned its
place.

| Preserved | Why |
|---|---|
| **The orange trap** at the DSUB2 splice | Joining orange to orange would put −15 V onto the amplifier output through 220 Ohms — about 68 mA into a part that limits in the tens of mA |
| **"Report what you see, not what you were told to expect"** | A correct splice once looked like a fault because an expected reading was wrong. Jacob reported what he saw and that is the only reason it was caught |
| **The row rules for DSUB1 and DSUB2** | They avoid counting pins, and the two connectors are opposite ways round |
| **The JP1 orientation rule** | The layout is asymmetric, so the numbering can be recovered with a meter and no reliance on silkscreen |
| **The LED5/LED6 phantom-powering exception** | With the supply off but USB in, LED1 to LED5 light and LED6 stays dark. Without this, a normal state reads as a fault |
| **Why `PREAMP−` must land on the preamplifier's own ground** | It is a sense wire carrying no current, and the whole reading is 0.4 mV |
| **The full out-of-range DAC table** | A tip hazard, not a typo, and the numbers make it obvious |
| **The blow test as a calibration of the electrostatic pull** | A gentle breath is 0.6 to 15 Pa, the same order as the pull at a micron gap. The test Jacob ran by eye proves the bias can move the leaf |
| **The gold-leaf handling detail** — never cut free leaf, the flip transfer, burnishing until it goes bright | Each of these is the difference between a usable sample and a ruined one |
| **The four analysis controls, and the detrending trap** | Undetrended, the same data gives +0.741 and looks like a breakthrough |
| **"A hard-to-read file is not an empty one"**, applied to the data directories | Every session data directory has a README that changes what its files mean |
| **The stick-slip warning about loose coin tubes** | Mass added to fix vibration can itself become a vibration source |

---

## 6. Structural changes

| | |
|---|---|
| **No second register of constants was created.** Numbers are cited inside prose, as `CLAUDE.md` section 3bb permits, and `docs/FACTS.md` is named as the canonical home | The one place this was hardest is the connection tables, which the brief asked for explicitly. **They carry a banner saying `docs/WIRING.md` is canonical and this is the copy that gets fixed** |
| **Safety rules are cited by `STATUS.md`'s numbers and never restated as a numbered list** | A second numbered list is exactly the defect that made `CLAUDE.md` section 4 unnumbered |
| **Revision history is separated from current state** — section 2 exists so that a document written in August is not read as describing today's hardware | Four tips, four gold builds and two preamp boards all have documents written about them |
| **The resume procedure is ordered so that every protective check precedes the risky step it protects** | `CLAUDE.md` section 3c exists because that ordering was got backwards once |
| **Figure slots are marked and empty rather than filled with descriptions** | Nothing in the manual describes a photograph that has not been opened |

---

## 7. Verification

```
python3 Code/pc/check_facts.py
```

**Exits 0 on everything in this directory.** It was run after each section was written, and it
caught two things in the manual's own text:

1. A troubleshooting heading reading "drops into constant-current mode" matched the retired
   `drops in` literal from the Keystone standoff row. **Reworded** — and the over-firing itself is
   logged as `INCONSISTENCIES.md` item C6.
2. A `safety rule 2` citation that shared no wording with the rule. **Reworded to name the sign of
   the tunnelling current**, which is what the rule is about.

3. **A third hit, at the end, is NOT in these files.** `deliverables/2026-09-19-pause/analysis/code/build_inventory.py`
   line 635 trips the retired `800 counts` row on the substring inside "1,800 counts per decade".
   **That is another agent's file and the same over-firing class as item 1**, and both are logged
   together in `INCONSISTENCIES.md` item C6. **As long as it is there, the checker exits 1 on the
   repository as a whole**, so whoever lands this work should clear it before committing.
