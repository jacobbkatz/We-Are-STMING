# Bench data, evening of 2026-09-17 local (UTC 2026-09-18 01:00-02:40)

Recorded by `sessions/2026-09-18-bench.md`. Times are UTC. `ADCR` averaged reads unless said
otherwise; 320.5 counts per nA. Sample -0.5 V is `BIAS 38229`.

| File | What |
|---|---|
| `console_outputs.md` | **Everything not saved to a file at the time**, transcribed: touch checks, noise, spectrum, the Z probes, the calibration steps, the bias check, the static scans, the park |
| `approach1.log` | `stm_approach.py`, 600 steps, no contact |
| `approach2.log` | After the hand-set: contact after 5 steps at Z 25,800 |
| `flip1.log` | The bias flip at the onset, 01:35 |
| `approach3.log`, `char1.log`, `char1.csv` | Contact after 135 steps at Z 10,200; `characterize.py` then found current already pinned at Z 10,000 and aborted |
| `zcal3_run1.*` | Three one-step-at-a-time passes with onset slope scans, then an X/Y check |
| `track_run1.*` | 90 s of repeated slow onset searches at a fixed motor position |
| `ft_run1.*`, `ft_long1.*` | **The fast tracker** (`scripts/fasttrack.py`). **See the caveat below** |
| `lash_run1.log` | Fast-tracker medians after single motor steps. The run was stopped by hand; no CSV was written |
| `settle2.log`, `settle3.log` | Noise with the tip clear, 01:47-01:59 |
| `scripts/` | **Scratch scripts that produced these files, kept as provenance, not tools.** They hard-code `COM3` and this machine's paths. `characterize_test.py`, `zcal3_test.py` and `fasttrack_test.py` are their simulated-junction tests |

> **Caveat on the fast-tracker files.** They record the Z at which the current first passed 1,000
> counts on a fast climb. **The same "onsets" appeared with the bias at 0 V**, and a static scan
> showed that is because the tip snaps into **hard metallic contact**, which carries current from
> the DAC offset alone. **So they locate snap-in events, not a tunnelling onset**, and their
> wobble statistics, spectrum and X/Y numbers are provisional. A Z-step transient was tested
> directly and is under the 1,000-count threshold, so they are not pure artefact either.
