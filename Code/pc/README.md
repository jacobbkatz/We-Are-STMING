# PC-side tools

Python programs that talk to the Teensy over USB serial. Run them from the repository root.

```bash
pip install -r Code/pc/requirements.txt
```

| File | What it is |
|---|---|
| **`stm_console.py`** | **Start here.** Send any firmware command, one-shot or interactive |
| **`adc_stats.py`** | Sample the ADC over time and report mean, stdev, min, max, range |
| **`stm_approach.py`** | PC-side woodpecker coarse approach. **Never sends `APRH`** |
| `stm_approach_test.py` | 40 tests for the above, run against a simulated microscope |
| `stm_control.py` | The `STM` class the GUI is built on. A library, not a program |
| `stm_app.py` | Tkinter GUI. **Do not use — see the warning below** |
| `stm_control_test.py` | Unit tests for `stm_control.py` |

See `docs/COMMANDS.md` for every command the firmware understands.

## stm_console.py

```bash
python Code/pc/stm_console.py GSTS           # one command, then exit
python Code/pc/stm_console.py DACZ 32768
python Code/pc/stm_console.py                # interactive
```

Use this rather than a generic serial monitor. The firmware reads commands four bytes at a time
and anything sending per-keystroke loses the race, so the command is silently discarded. This
script sends each command as a single write.

In interactive mode, `free` releases the serial port so you can flash firmware without the Teensy
Loader asking for the PROGRAM button.

## adc_stats.py

```bash
python Code/pc/adc_stats.py -n 50 -i 9.0 --tag "what changed"
```

Holds the port open for the whole run, so the sample interval is real. It reads `GSTS` field 5,
which is a **raw** single conversion — not `ADCR`, which averages and would hide the isolated
bit-flips a marginal SPI link produces.

This is the tool for the preamp acceptance test. Conditions matter: bench clear, nobody within a
metre, no DAC commands, ten minutes. See `STATUS.md`.

If every sample comes back identical it says so, because a railed analog input and a stuck read
path look the same in the numbers.

## stm_approach.py

```bash
python Code/pc/stm_approach.py --z-retracted low --motor-toward-sample positive --dry-run
```

Coarse approach done from the PC, using the woodpecker method: only the piezo ever closes the gap,
and the motor only moves while Z is retracted. It thresholds on **absolute deviation** from a
measured baseline, so it works without knowing which way tunneling moves the reading — which is
exactly what the firmware's `APRH` gets wrong.

**It refuses to run** unless you tell it two things it cannot work out for itself:
`--z-retracted` (which end of the Z range pulls away from the sample) and `--motor-toward-sample`
(which sign of `MTMV` advances). Both are still UNKNOWN in this project — determine them with the
tip removed before using this for real. It also refuses if the resting ADC reading is railed, which
it currently is, so **it will not run until the preamp is fixed.**

Ctrl-C stops it at any point and retracts Z. `--dry-run` does everything except move the motor.

To check it still behaves after any change:

```bash
python Code/pc/stm_approach_test.py
```

40 tests against a simulated microscope. **If any fails, do not use the script.**

## stm_control.py has four verified bugs

Checked against the live source 2026-09-06. All four are also present in Mech Panda's copy — they
are upstream, not ours. **None is fixed.**

| Line | Bug | Effect |
|---|---|---|
| `stm_control.py:127` | `self.send_cmd('MTMV {steps}')` — **missing the `f` prefix** | It sends the literal text `MTMV {steps}`. The firmware reads `MTMV`, finds no digits, and moves **zero steps**. **This is why the GUI's motor control does nothing** |
| `stm_control.py:88` | `set_buffer_size()` is called unconditionally | That method is **Windows-only** in pyserial. On macOS or Linux, opening the port raises AttributeError and the GUI cannot connect at all |
| `stm_control.py:40-49` | `dac_to_dacz/x/y_volts` all use `10.0 / 2.0`, i.e. ±5 V | **All three are wrong.** Z is ±10 V; X and Y are ±3 V. Every voltage the GUI displays is incorrect |
| `stm_control.py:37` | `adc_to_amp` uses `10.24` V full scale | Wrong — it is **4.096**. Every current is 2.5x too large. See `docs/UPSTREAM_MECHPANDA.md` §1 |

A fifth item reported in the old handoff — `get_status()` returning `self.history[-1]` on an empty
list — is **unreachable dead code**, not a live bug: the method already returns at line 92 when
busy, so the branch at line 95 can never run. Recorded so nobody hunts for it.

## Do not use stm_app.py

The Tkinter GUI has buttons wired directly to the two most dangerous paths in the firmware:

- **"Approach"** sends `APRH`, whose signed comparison can drive the tip into the sample without
  ever triggering. Use `stm_approach.py` instead.
- **"ConstCurrentOn"** sends `CCON`, which snaps Z to midscale from wherever it was — up to a
  ~180 nm lurch. See `STATUS.md` fault 2.

Its motor control is broken independently of both. Use `stm_console.py` and `stm_approach.py`.

## Known issue

`stm_control.py` and `stm_console.py` hardcode the ADC full scale as **10.24 V**, while the
firmware driver uses **4.096**. That disagreement is unresolved — see the open questions in
`STATUS.md`. Any current figure printed by these tools depends on it.
