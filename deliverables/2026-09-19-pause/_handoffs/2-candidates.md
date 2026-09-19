# Handoff — Subagent 2, candidate images and the motion hypothesis

**2026-09-19.** Owns and wrote only `deliverables/2026-09-19-pause/candidates/**`.
**No raw file was modified.** `sessions/data/` was read only.

---

## 1. Files reviewed

**Read in full:** `CLAUDE.md`; `deliverables/2026-09-19-pause/BRIEF.md`; `STATUS.md` top blocks;
`sessions/2026-09-17-bench.md` (all of §3.19–3.27, §4–9); `sessions/2026-09-19-bench.md` (all);
`sessions/2026-09-19-morning.md` (all); all four `sessions/data/*/README.md`;
`deliverables/2026-09-19-pause/LEAD_VERIFICATION.md` §V4.

**Code read:** `Code/pc/stm_y_control.py`, `sessions/data/2026-09-19-bench/scripts/scan2.py`,
`.../analyze_scans.py`, `.../run_img_wide.py`.

**Data examined — 51 recordings, every raster scan, line repeat, three-Y run and control in the
project**, inventoried in `candidates/work/inventory.csv`. Plus four long fixed-point records
(`still.csv`, `stamp.csv`, `here_run1.csv`, `touchrec_run1.csv`) and five Z-test CSVs.

---

## 2. Work completed

| Script | What it does |
|---|---|
| `code/stmload.py` | shared loaders and statistics; documents the raster storage convention |
| `code/01_inventory.py` | inventory of all 51 recordings with shapes and detrended RMS |
| `code/02_time_vs_position.py` | **the position-versus-time discriminator** on all 34 raster files |
| `code/03_wide_profile.py` | the ±15,000 profile; three-Y discrimination; **cross-night comparison** |
| `code/04_0917_wide_place_test.py` | **the place test §3.25 said had never been run**, from 2026-09-17 data |
| `code/05_direction_asymmetry.py` | forward/backward asymmetry (**conclusion overturned by 08/09 — see §5**) |
| `code/06_motion_and_timing.py` | within-pass spectra, line-to-line walk, gap motion, coherent-line search |
| `code/07_chance.py` | **three permutation/surrogate nulls** and the 201-test search budget |
| `code/08_lag_fairness.py` | the fairness test that overturned 05 |
| `code/09_lag_aware.py` | the lag search put under a surrogate null |
| `code/10_gallery_figures.py` | all nine gallery PNGs |
| `code/11_truncation_audit.py` | **the coordinator's two requests**: defect-class audit and three-Y re-verification |
| `code/12_start_of_pass_transient.py` | **the finding that closes candidate A** |

---

## 3. Outputs, and the exact command that reproduces each

All commands run **from the repository root**. Console output for each is saved in
`candidates/work/NN_output.txt`.

```
python3 deliverables/2026-09-19-pause/candidates/code/01_inventory.py
python3 deliverables/2026-09-19-pause/candidates/code/02_time_vs_position.py
python3 deliverables/2026-09-19-pause/candidates/code/03_wide_profile.py
python3 deliverables/2026-09-19-pause/candidates/code/04_0917_wide_place_test.py
python3 deliverables/2026-09-19-pause/candidates/code/05_direction_asymmetry.py
python3 deliverables/2026-09-19-pause/candidates/code/06_motion_and_timing.py
python3 deliverables/2026-09-19-pause/candidates/code/07_chance.py          # ~2 min
python3 deliverables/2026-09-19-pause/candidates/code/08_lag_fairness.py
python3 deliverables/2026-09-19-pause/candidates/code/09_lag_aware.py       # ~1 min
python3 deliverables/2026-09-19-pause/candidates/code/10_gallery_figures.py
python3 deliverables/2026-09-19-pause/candidates/code/11_truncation_audit.py
python3 deliverables/2026-09-19-pause/candidates/code/12_start_of_pass_transient.py
```

Needs `numpy` and `matplotlib` only. `07` and `09` seed `numpy.random.default_rng(20260919)`, so
they are bit-reproducible.

**Deliverables:** `candidates/GALLERY.md`, `candidates/VERDICT.md`, `candidates/gallery/*.png`
(9 figures, raw and processed side by side, captioned), `candidates/work/*.csv` (the numbers behind
every claim).

---

## 4. Evidence for each finding — path, rows, numbers

### F1. Candidate A is closed: it is the loop recovering from the X flyback
`sessions/data/2026-09-17-bench/line_repeated_wide.csv`, 12 forward passes (rows 1–24; the `back`
rows are byte-identical in 12 of 12 pairs — the known scratch-tool bug).

| | |
|---|---|
| published / replicated | consecutive r +0.515 / **+0.647**; split-half +0.923 / **+0.923**; profile 636 / **636 counts** |
| drop 1 leading point | r **+0.317**, profile 339 |
| **drop 2 leading points** | **r +0.048**, profile 233 |
| tilt of the 12 passes | **−0.105 Z counts per X count** |
| X flyback (col 21 → col 1, 47768 → 17768) | **30,000 counts** |
| predicted recovery = tilt × flyback | **3,144 counts**; observed in first two pixels **2,465** |
| a mid-line step | **−236 counts** |
| first jump per pass | +671 → +2,364, **+137 counts per pass** |

**Predicted absence, verified twice:** `scan_wide_25nm_1/2.csv` raster continuously (no flyback) →
observed start jumps **+78, +37**; `ycontrol_run1.csv` / `ycontrol_run2_ysep12000.csv` fly back but
have tilt **−0.0009 / +0.0079** → predicted **28 / 238**, observed **−99 / +47**.
`code/12_start_of_pass_transient.py`, `work/start_of_pass_transient.csv`, `gallery/09`.

### F2. The ±15,000 place test — which §3.25 said had never been run — is answerable from 2026-09-17 data
`scan_wide_25nm_1.csv` and `_2.csv`: two complete 2D images, same 9 Y places (17768…47768, 3750
apart), same X grid (17768…47768, 1500 apart). Forward passes: **same place +0.216 ± 0.228 (n=9),
different place +0.074 ± 0.063 (n=72), permutation p = 0.24**. Backward: **+0.104 vs −0.010,
p = 0.28**. `code/04`, `code/07` null N2.
**Power limit, stated:** with 9 pairs this only excludes a difference bigger than about **+0.47**.

### F3. Candidate B — the "3.9 sigma" was never 3.9 sigma, and its control reaches p = 0.02
All five three-Y files verified from raw CSVs, shapes checked first: **every one is 3 places × 6
passes × 21 points, no truncation**, and every published number reproduces exactly (+0.374 ± 0.097,
+0.056 ± 0.094, +0.070 ± 0.084, +0.032 ± 0.035, +0.164 ± 0.082). **The non-reproduction is real.**
Under 20,000 place-label permutations: run 2 **p = 0.0036**; run 4 **p = 0.26**;
**`ycontrol_xheld_run1.csv`, an X-HELD CONTROL, p = 0.020**. `code/07` null N1, `code/11` part 3.

### F4. A SECOND instance of the truncation defect, in the wide images
`sessions/2026-09-19-bench.md` §3.16's *"image to image +0.56 to +0.86, matched by the X-held
controls' +0.56"*: `img_scan_0.csv` has **1 line**, `img_scan_1.csv` has **2 lines**. Both scan
correlations were computed over **21 and 42 points**, not 231. **Neither was an image-to-image
correlation.** There are not two full wide scan images, so **no like-for-like scan figure exists**;
the controls' +0.56 is a genuine 231-point number. `code/11` part 2, `work/truncation_audit.csv`.
The lead's cas9 finding is independently confirmed: **as published +0.20/+0.21/+0.70 over
231/21/21 points; like for like +0.20 and −0.06, mean +0.07 against the scans' +0.04.**
**Defect-class audit:** short files in three groups (`cas9` ×1, `img_` ×2, `tuned_s3k` ×4);
**2026-09-17 is clean** — every set it compared against itself is uniform length, and its other
figures are per-file statistics no truncation can touch.

### F5. The wide images carry a real, X-dependent, roughly line-periodic signal
`img_scan_2.csv` r_pos **−0.854** at zero shift, **+0.829** at −10 px; `img_scan_1.csv` **−0.917**
→ **+0.929** at +9 px; symmetric in sign, lowest at zero. **X-held controls `img_xheld_0/1.csv`:
+0.241 → +0.316 and +0.153 → +0.176, nothing at any shift.** So **X motion is required** — a
control-backed upgrade of `sessions/2026-09-19-morning.md` §6's "likely but unproven".
Not topography: a surface gives the same height at the same X in both directions. `code/08`,
`gallery/05`.

### F6. The 2026-09-17 narrow scans and the 2026-09-19 feedback scans are matched by their controls
Pooled position-locking (`code/02`, `work/time_vs_position.csv`):

| set | lines | r_pos | r_time |
|---|---|---|---|
| ±400 real scans (10 files) | 102 | **−0.069 ± 0.049** | −0.056 ± 0.058 |
| ±400 X-HELD CONTROL | 8 | **+0.170 ± 0.118** | +0.190 ± 0.156 |
| ±1500 real scans (4 files) | 44 | −0.066 ± 0.137 | −0.235 ± 0.122 |
| ±1500 X-HELD CONTROLS | 34 | −0.053 ± 0.144 | −0.267 ± 0.117 |

### F7. Gap motion dominates every image statistic
Onset Z per cycle, `sessions/data/2026-09-19-morning/`: span **2,828–13,508 counts**; steady drift
**+9.6 to −67.7 counts/s**; **scatter after removing the drift 396, 637, 849, 1,358 and 1,722
counts.** Against an image taking ~5 s and a corrugation of **29–458 counts** across 21 scan files.
`code/06`, `work/onsets_*.csv`, `gallery/08`.

### F8. No coherent spectral line, in any long fixed-point record
Split-half coherence, peaks kept only if present in both halves within a factor of 2.5:
`here_run1.csv` (junction, 46,328 samples at 3,448 Hz) **none**; `touchrec_run1.csv` **none**;
`still.csv` (tip clear, control) one line at 63.6 Hz; `stamp.csv` **none**. Confirms and extends
`sessions/2026-09-19-morning.md` §6. **Nothing for a scanner to synchronise to.**

### F9. Chance accounting
**201 reproducibility tests** counted; Bonferroni 5% is **p < 2.5 × 10⁻⁴** (~3.7σ); ~10 p < 0.05
results expected from noise. **Nothing reaches it as evidence of a surface.** `code/07`.

### F10. Four files are absent from their own directory's README
`sessions/data/2026-09-17-bench/README.md` does not list `scan_wide_25nm_1.csv`,
`scan_wide_25nm_2.csv`, `line_repeated_wide.csv` or `line_three_y_positions.csv`. **Those four are
the project's strongest candidate and the data that answers it.** Likeliest reason §3.25 believed
the place test had never been run. **For the lead — `sessions/` is read-only to me.**

---

## 5. Where I was wrong before I was right — recorded because it matters

`code/05_direction_asymmetry.py` originally concluded that the 636-count profile is a
forward-direction artefact because it matches the forward mean shape of the 2D images (+0.760) and
not the backward (−0.265). **That argument was unsound and I wrote it before checking.**
`code/08_lag_fairness.py`, written to check it, found the backward match reaches **+0.848 at a
shift of +4 pixels** — higher than the forward match — which is exactly what a real feature looks
like through a trace/retrace offset. `code/09_lag_aware.py` then put a null under the lag search
and found that **the best-of-13-lags correlation is +0.51 ± 0.15 for phase-randomised noise**, so
neither number is far from chance and the lag test settles nothing either way.

**Both scripts' printed conclusions have been corrected in place and now point at each other.**
The candidate is closed by F1, not by the direction argument.

---

## 6. Uncertainties, blockers, remaining work

1. **Candidate B cannot be settled with existing data.** Run 2 (+0.374) and run 4 (+0.056) are half
   an hour apart and the gap moved by most of the Z range in between. **"It did not repeat" and
   "the surface moved out from under it" are not distinguishable here.** This is the strongest form
   of Jacob's hypothesis and I cannot refute it. `VERDICT.md` §5 gives the one measurement that
   would.
2. **The place test's power is limited** (F2): ±0.47 at 2σ. A weak genuine surface signal is not
   excluded by it.
3. **The mechanism of the wide images' mirrored signal is unidentified.** Loop hunting, X-piezo
   coupling into Z, and **the tip ploughing a compliant sample** are all consistent. The third
   would be a real measurement of the gold's compliance. `VERDICT.md` §5 gives the two-speed
   experiment that separates all three.
4. **Pixel timing for the wide images is inherited, not measured.** 10.8 ms/pixel comes from the
   same night's `cas9` scans; no timing was logged for `img_*`. The "~4–5 Hz" rests on it; the
   **periodicity in pixels does not**, and that is what the argument uses.
5. **The Z scale is inherited.** Every number here is in Z DAC counts and scale-free. I made no
   conversion to nanometres.
6. **Left undone:** I did not analyse `bigswing_run1.csv`, `lockin_run1.csv`, `slowscan_run1.csv`,
   `zdir*_run1.csv`, `lift_run1.csv` or `onset0_run1.csv` — they are Z/bias characterisation, not
   candidate images, and Subagent 1 owns the data inventory.

---

## 7. For the lead specifically

- **`STATUS.md` and `sessions/2026-09-19-bench.md` §3.16 need the same correction you are already
  making for §3.14** — the wide images' "+0.56 to +0.86" has the identical truncation defect and is
  worse (F4). I have not touched either file.
- **`sessions/2026-09-17-bench.md` §3.25's "UNDETERMINED" on the 636-count profile can be retired**
  (F1, F2). This is a change to a recorded conclusion and it moves toward *less* claim.
- **`sessions/data/2026-09-17-bench/README.md` is missing four files** (F10).
- **The min-length truncation is in committed scratch code** and is the defect class. If any of it
  is ever promoted to `Code/pc/`, it must refuse a shape mismatch rather than truncate, and the
  check must be **shown red against a one-line file first** (`CLAUDE.md` §7 rule 2).

`python3 Code/pc/check_facts.py` exits 0 with this work in place.
