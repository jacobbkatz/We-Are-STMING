# 2026-09-19 bench data

**Empty until the run happens.** This directory exists so tonight's files have a home and the
plan can name it.

## What goes here

| File | How |
|---|---|
| `still.csv` | `py Code/pc/stm_noise_spectrum.py 10 --out still.csv`, room quiet, tip clear, nobody within a metre |
| `stamp.csv` | the same again while someone stamps on the floor a couple of metres away |
| `console.md` | paste what the tool printed, including the `--compare` output |

**Keep the CSVs.** The 2026-09-18 run's raw samples were never kept, which is exactly why tonight's
cross-night comparison is unreliable and has to be hedged. **Two nights of raw samples make the
next comparison clean.**

## Conditions that make the numbers mean something

- **Tip clear and retracted.** The tip, the gold and the sample plate have all changed since
  2026-09-18; a clear-tip measurement is the only one that isolates the suspension.
- **45 minutes of warm-up** before believing any preamp number (`STATUS.md` safety rule 0).
- **LED1-LED4 dark** before and after. A reading taken with one lit is void.
- **Nobody within a metre.**

## What changed since the last noise run

**The suspension was loaded and the springs opened for the first time** — 54 quarters plus 10
nickels, 356.2 g, and the platform sagged enough that it had to be raised back up. Expected `f0`
about 2.1 to 2.4 Hz against 5 Hz noise. `STATUS.md` has the arithmetic and
`docs/NEXT_SESSION_PLAN.md` has the procedure.
