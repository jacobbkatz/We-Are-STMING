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
| [2026-09-05](2026-09-05.md) | Cross-referenced Dan Berard's build against our source. **Two unfixed tip-crash risks found in firmware**: `CCON` snaps Z to midscale, and the motor is left energised. Coarse approach step size is ~7.8 nm, not the 244 nm previously assumed. Sample decided: gold foil |
| [2026-09-01](2026-09-01.md) | Repository restructured for two-computer working. **The preamp case shield was never grounded** — a second candidate for the 37 nA that a board rebuild would not fix |
| [2026-08-31](2026-08-31-results.md) | Preamp fault characterised: 37 nA leakage, loop closed not open. Bias path passes, first test ever. **Two new faults:** DACs lose configuration hourly, one JP1 ground open. ADC clock 40 MHz to 1 MHz. Piezo has no usable resonance when mounted |
| [2026-08-31 plan](2026-08-31-plan.md) | The plan that session ran against, including its Part 0 corrections to the handoff |

Sessions 1 and 2, on 2026-08-29 and 2026-08-30, predate this directory. They are written up as
Appendix A of `docs/PROJECT_HANDOFF_SUMMARY.md`.
