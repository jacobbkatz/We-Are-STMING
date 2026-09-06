# Session logs

One file per work session, named `YYYY-MM-DD.md`. Copy `TEMPLATE.md` to start a new one, or just
type `/wrap` and Claude will do it.

**Newer supersedes older.** Where two logs disagree, the later one is right. Where a log disagrees
with `docs/PROJECT_HANDOFF_SUMMARY.md`, the log is right — the handoff is known to be wrong in six
places.

`STATUS.md` in the repository root is the accumulated current state. **Read that first**; these
logs are the reasoning behind it and the record of what was ruled out.

| Session | Headline |
|---|---|
| [2026-09-06 plan](2026-09-06-plan.md) | **Bench plan for Nuh working alone.** Meter checks on the floating DAC reset pins, the shield, and tip isolation; the 30-minute DAC idle test; shield grounding with before/after captures; a new rail-scaling test; motor direction |
| [2026-09-06](2026-09-06.md) §13-22 | **Nuh at the bench, meter only, nothing powered.** All eight CLEAR#/RESET# pins measured **open on the physical board** — third independent confirmation, with controls. **The preamp shield was discontinuous and only partly grounded**, not "never grounded" as recorded: a ground wire had been added after 31 August and never written down. That would have made Block D3 return a false negative and pushed us into consuming the spare preamp board. **Shield stripped and rebuilt in all copper, seams soldered — continuity NOT yet verified** |
| [2026-09-06](2026-09-06.md) | **CLEAR# and RESET# are floating on all four DACs** — the best explanation yet for the configuration loss, and a four-wire fix if confirmed — later **confirmed from the manufacturing netlist**. The gerber archives turned out to contain complete netlists for both boards: **JP1's pinout is resolved and the "do not run a wire" rule is retired**. The 37 nA candidates ranked by impedance: contamination beats the floating shield. A new cheap test: the offset should scale with rail voltage if it is rail leakage |
| [2026-09-05](2026-09-05.md) | Cross-referenced Dan Berard's build against our source. **Two unfixed tip-crash risks found in firmware**, both confirmed present in Mech Panda's upstream too: `CCON` snaps Z to midscale, and the motor is left energised. Coarse approach step size is ~7.8 nm, not the 244 nm previously assumed. **`stm_approach.py` written and tested** (40 tests, never run on hardware). Mech Panda's repo has **no licence at all**. Sample decided: gold foil. **Third pass: the ADC full scale question is settled at 4.096 V from the controller schematic we already had** — every current figure the Python tools print is 2.5x too large. No public replication of this build exists. **Fourth pass:** Berard's scan head page closes tip mounting, sample mounting and the piezo reference part, and shows he quotes the lever ratio as both 20 and 30 — so the step size is 5–8 nm, not 7.8 |
| [2026-09-01](2026-09-01.md) | Repository restructured for two-computer working. **The preamp case shield was never grounded** — a second candidate for the 37 nA that a board rebuild would not fix |
| [2026-08-31](2026-08-31-results.md) | Preamp fault characterised: 37 nA leakage, loop closed not open. Bias path passes, first test ever. **Two new faults:** DACs lose configuration hourly, one JP1 ground open. ADC clock 40 MHz to 1 MHz. Piezo has no usable resonance when mounted |
| [2026-08-31 plan](2026-08-31-plan.md) | The plan that session ran against, including its Part 0 corrections to the handoff |

Sessions 1 and 2, on 2026-08-29 and 2026-08-30, predate this directory. They are written up as
Appendix A of `docs/PROJECT_HANDOFF_SUMMARY.md`.
