# PC-side tools

Python programs that talk to the Teensy over USB serial. Run them from the repository root.

```bash
pip install -r Code/pc/requirements.txt
```

| File | What it is |
|---|---|
| **`stm_console.py`** | **Start here.** Send any firmware command, one-shot or interactive |
| **`adc_stats.py`** | Sample the ADC over time and report mean, stdev, min, max, range |
| `stm_control.py` | The `STM` class the GUI is built on. A library, not a program |
| `stm_app.py` | Tkinter GUI. **Motor control in it is known broken** — use `stm_console.py` |
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

## Known issue

`stm_app.py`'s motor control is broken. Do not use it. `stm_control.py` and `stm_console.py` also
hardcode the ADC full scale as **10.24 V**, while the firmware driver uses **4.096**. That
disagreement is unresolved — see the open questions in `STATUS.md`. Any current figure printed by
these tools depends on it.
