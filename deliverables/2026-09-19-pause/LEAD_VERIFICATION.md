# Lead verification log

**The lead's own checks, run independently of the subagents.** Nothing here is taken from an
agent's summary. Where an agent later reports the same quantity, this file is what its number is
checked against, not the other way round.

Each entry says what was checked, how, what came out, and whether the project's existing claim
survives.

---

## V1. The end-to-end calibration — the project's strongest single result. **VERIFIED**

**The claim, from `docs/FACTS.md` and `sessions/2026-09-16-bench.md` §3.4:** a 100 MΩ dummy junction
clipped between the bias wire and the tip holder gives **−3,205 ± 37 counts per volt against −3,200
predicted**, **320.5 counts per nA**, **R² 0.993**, across 53 readings.

**How I checked it.** There is **no CSV for 2026-09-16** — `sessions/data/` starts at 2026-09-17 —
so the eight-row table in the session log is the primary record. I transcribed all 53 individual
readings out of that table by hand and refit them from scratch, with my own least-squares code, in
the lead scratchpad. This was done before Subagent 1 reported anything.

| Quantity | Session log | My independent refit | Agrees |
|---|---|---|---|
| Slope, counts per volt on the bias wire | −3,205 ± 37 | **−3,204.8 ± 36.5** | yes |
| Counts per nA | 320.5 | **320.5** | yes |
| Intercept | +58, about 1.3 standard errors from zero | **+58.0 ± 45.3, 1.28 SE** | yes |
| R² | 0.993 | **0.9934** | yes |
| Residual scatter per reading | 320 counts | **320 counts** | yes |
| Ratio to the predicted −3,200 | 1.0016 | **1.0015** | yes |
| Every group mean within | 1.4 standard errors | **worst is 1.29 SE**, at +0.711 V | yes |

**n = 53, and they are NOT 53 independent observations.** They are repeated `ADCR` reads at eight
bias settings — five to ten reads per setting, about 1.4 s apart. The independent unit here is the
**bias setting, n = 8** (of which three are the same 0 V point revisited). The slope's standard
error is computed from the scatter of individual reads, which is the right thing for the fit, but
nobody should quote "53 measurements" as 53 independent tests of the chain.

**The 0.13 sigma figure on `docs/showcase.html` is also correct.** (−3,204.8 − (−3,200)) / 36.5 =
**0.13**. That claim survives.

### What this does NOT establish, and the session log already said so

**The slope is the ratio of the feedback resistor to the dummy resistor**, both nominal 100 MΩ,
divided by the volts per count. **Neither resistor's tolerance is recorded.** So the agreement to
0.16% confirms the scale *to within those two tolerances* — it is substantially a measurement that
the two resistors match each other, not an independent confirmation of 320 counts per nA. A pair of
5% resistors that happen to be cut from the same reel would produce exactly this result.

**This is a real limit on the headline claim and it must appear wherever the claim does** — poster,
report and showcase alike. It does not weaken the qualitative result, which is that **the entire
current path works end to end**: bias DAC, buffer, wire, a known resistance, tip holder, tip lead,
standoff, preamp, cable, converter, firmware and PC tools. That is unaffected by resistor tolerance.

**The 320-count residual scatter is not a noise figure.** Cover off, clips and a jumper on the input
node. It is about 25× the quietest capture of that session.

**Reproduce:** the transcription and fit are in
`deliverables/2026-09-19-pause/analysis/` only if Subagent 1 also did it; my own copy is a
scratchpad script, and the 53 numbers themselves are in `sessions/2026-09-16-bench.md` §3.4, which
is the durable record. Anyone can redo this from that table in ten minutes.
