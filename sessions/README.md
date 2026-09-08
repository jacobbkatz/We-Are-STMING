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
| [2026-09-08](2026-09-08.md) | **Repository audit and migration. Nothing measured, no hardware powered.** Jacob flagged the repository as convoluted; it was measured before anything was changed — 12,586 lines across 34 files, with the real problem being **duplication, not size**. Two values corrected on 2026-09-07 still sat wrong in **six live documents**. New **`docs/FACTS.md`** (one canonical value per number, with a RETIRED table) and **`Code/pc/check_facts.py`**, which runs at every session start and on its first run found **a live code bug**: `stm_approach.py` still defaulted to the retired 4.096 V full scale and would have printed every current **2.5x too small** on the first real approach. Superseded material archived with banners, `sessions/` additive only. **Two of the audit's own recommendations were reversed on inspection** — archiving the cold-start procedure, and merging the `CLAUDE.md` rules. Sections **37 and 38 were misfiled into `2026-09-07.md` and moved here verbatim** |
| [2026-09-07](2026-09-07.md) §17-27 | **Nuh at the bench — first hardware measurements since 31 August, and they overturn the project's headline number.** A meter on PAD1 reads **+11.905 V**, not the assumed 3.73 V: the leak is **~119 nA, not 37 nA**. R23 confirms at 11.914 V, so there is no attenuation and **the ADC is being driven ~3x past its ±4.096 V span** [**corrected 2026-09-08: the span is ±10.24 V, not ±4.096 V — see `docs/FACTS.md`. The "~3x past span" conclusion does not follow from the corrected number and should not be carried forward; what the ADC actually sees is the differential PREAMP+ minus PREAMP-, and PREAMP- is floating, so it is not known**]. Worse: **`PREAMP-`, the ADC's differential reference, is FLOATING** — every ADC reading in the project has been referenced to a drifting node, and this is the same "one JP1 ground is open" fault filed as a loose end on 31 August. **The leak is on the preamp board** (coax, tip holder and tip eliminated by measurement). The **rail-scaling prediction failed** — a 39% cut in the −15 V rail produced no proportional change. **The board takes 45+ minutes to settle** after power-on, ~30 nA of drift nobody had controlled for. **The DAC dropout is not time-triggered.** Three of the session's own results are in doubt because of the floating reference |
| [2026-09-07 audit](2026-09-07.md#second-pass-technical-audit-2026-09-07-late) | **Component-level datasheet pass and second-pass audit.** New `docs/COMPONENTS.md` and `docs/NEXT_SESSION_PLAN.md`. **The DAC floating-pin hypothesis is very likely dead** — RESET has an internal pull-up, and the power-sequencing explanation was in the handoff all along. **`PREAMP−` floating is a spec violation**, not just an inconvenience: the ADC needs IN− within ±500 mV of GND and ours sits at 2.7 V. **The noise may be void entirely** — it is 1,700x the Johnson floor and 10,000x the op-amp's, so it is probably the floating reference. The TIA has **no compensation capacitor** and its real bandwidth is ~5 kHz. 119 nA vs the OPA627's 1 pA rules the op-amp out |
| [2026-09-07](2026-09-07.md) | **Superglue was used twice, and the first use is the serious one** — a little bonds the **PTFE standoff to the board**, straight across the insulator that holds the input node. New leading candidate for the 37 nA. The **output sign says the leak is to the negative rail** (~402 MOhm needed; `IC1` pin 4 is 2.54 mm away). The **cut coax enables a free bisection test**. The noise is **several hundred times** the Johnson floor. Print material settled: **PETG-CF**. **Addendum:** the bias was on all along (my error) — and working that through gives the sign table showing **every other voltage in the instrument has the wrong sign**, leaving only the −15 V rail. **The piezo is superglued into its socket too** — a third CA site, and a possible mechanical stiffening of the scanner |
| [2026-09-06 plan](2026-09-06-plan.md) | **Bench plan for Nuh working alone.** Meter checks on the floating DAC reset pins, the shield, and tip isolation; the 30-minute DAC idle test; shield grounding with before/after captures; a new rail-scaling test; motor direction |
| [2026-09-06](2026-09-06.md) §13-22 | **Nuh at the bench, meter only, nothing powered.** All eight CLEAR#/RESET# pins measured **open on the physical board** — third independent confirmation, with controls. **The preamp shield was discontinuous and only partly grounded**, not "never grounded" as recorded: a ground wire had been added after 31 August and never written down. That would have made Block D3 return a false negative and pushed us into consuming the spare preamp board. **Shield stripped and rebuilt in all copper, seams soldered — continuity NOT yet verified** |
| [2026-09-06](2026-09-06.md) | **CLEAR# and RESET# are floating on all four DACs** — the best explanation yet for the configuration loss, and a four-wire fix if confirmed — later **confirmed from the manufacturing netlist**. The gerber archives turned out to contain complete netlists for both boards: **JP1's pinout is resolved and the "do not run a wire" rule is retired**. The 37 nA candidates ranked by impedance: contamination beats the floating shield. A new cheap test: the offset should scale with rail voltage if it is rail leakage |
| [2026-09-05](2026-09-05.md) | Cross-referenced Dan Berard's build against our source. **Two unfixed tip-crash risks found in firmware**, both confirmed present in Mech Panda's upstream too: `CCON` snaps Z to midscale, and the motor is left energised. Coarse approach step size is ~7.8 nm, not the 244 nm previously assumed. **`stm_approach.py` written and tested** (40 tests, never run on hardware). Mech Panda's repo has **no licence at all**. Sample decided: gold foil. **Third pass: the ADC full scale question is settled at 4.096 V from the controller schematic we already had** — every current figure the Python tools print is 2.5x too large. No public replication of this build exists. **Fourth pass:** Berard's scan head page closes tip mounting, sample mounting and the piezo reference part, and shows he quotes the lever ratio as both 20 and 30 — so the step size is 5–8 nm, not 7.8 |
| [2026-09-01](2026-09-01.md) | Repository restructured for two-computer working. **The preamp case shield was never grounded** — a second candidate for the 37 nA that a board rebuild would not fix |
| [2026-08-31](2026-08-31-results.md) | Preamp fault characterised: 37 nA leakage, loop closed not open. Bias path passes, first test ever. **Two new faults:** DACs lose configuration hourly, one JP1 ground open. ADC clock 40 MHz to 1 MHz. Piezo has no usable resonance when mounted |
| [2026-08-31 plan](2026-08-31-plan.md) | The plan that session ran against, including its Part 0 corrections to the handoff |

## A stray branch on the remote

`origin/session-2026-08-31` holds two commits by Nuh from 31 August, on a **separate history**
(it descends from Mech Panda's original repository, not from ours):

| | |
|---|---|
| `d8069d5` | Session 3: ADC clock fix, bias path verified, preamp fault identified |
| `0f9515d` | **Resolve JP1 pinout from the preamp Gerbers: pin 4 is unrouted** |

**All of its content is already on `main`**, verified file by file on 2026-09-06 — it arrived via
Jacob's manual upload on 1 September, at the reorganised paths. The only differences are those path
updates and line endings.

**It is safe to delete, but has been left alone** because it is Nuh's branch and both of us were
not present. Delete it together, or leave it as an archive — but **do not push to it**, or work
will diverge onto a history `main` cannot see. That is how the JP1 finding nearly went unnoticed:
it was on `main` all along, in the handoff's header, and a later session re-derived it from scratch.

---

Sessions 1 and 2, on 2026-08-29 and 2026-08-30, predate this directory. They are written up as
Appendix A of `docs/PROJECT_HANDOFF_SUMMARY.md`.
