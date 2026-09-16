# PC-side tools

Python programs that talk to the Teensy over USB serial. Run them from the repository root.

```bash
pip install -r Code/pc/requirements.txt
```

### First time on a Mac — added 2026-09-15

**No driver is needed.** The Teensy is a USB CDC device and macOS has it built in. It appears as
`/dev/tty.usbmodem…`, but **you never have to name the port**: `stm_console.py` finds it by PJRC's
vendor ID, `0x16C0`.

**Recent macOS refuses `pip install` into the system Python** with an
`externally-managed-environment` error. Use a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pyserial
```

**`pyserial` alone is enough for `stm_console.py`.** `numpy` and `matplotlib` are only needed by
`adc_stats.py` and the GUI.

**If `find_teensy()` returns nothing**, the board is not enumerating: check the USB cable is a data
cable and not charge-only, which is the usual cause.

### First time on Windows — added 2026-09-16, followed on Jacob's machine the same day

**Written from a cloud session, then followed for real on Jacob's Windows machine on 2026-09-16 by
Claude Code desktop, and corrected from what actually happened.** See
`sessions/2026-09-16-bench.md`. Nuh's machine is the one that had run the instrument before.

**Claude has to run on the computer the Teensy is plugged into.** Claude Code on the web runs in a
cloud container and can see only the repository; it cannot open a USB port. Use Claude Code
desktop or the CLI on this machine.

**No driver is needed on Windows 10 or 11.** The Teensy appears as a COM port on its own, and
`stm_console.py` finds it by PJRC's vendor ID, so the port never has to be named.

> **On Windows, type `py` wherever this project says `python` or `python3`.** Found 2026-09-16.
> On Jacob's machine `python` and `python3` are **Microsoft Store placeholders**, not Python. They
> print *"Python was not found; run without arguments to install from the Microsoft Store"* even
> though Python 3.13 is installed. **`py` is the Python launcher and it works.** The placeholder
> appears when Python's own folder is not on the PATH, which is what the installer tick box below
> controls. **`py` works either way**, so the commands below use it.

1. **Check what is there.** Press the Windows key, type `cmd`, press Enter, then:
   ```
   git --version
   py --version
   ```
   "is not recognized" means that one is missing. **Do not trust `python --version`**: the
   "Python was not found" message comes from the Store placeholder, and says nothing about whether
   Python is installed.
2. **Git**: https://git-scm.com/download/win, accept every default.
3. **Python**: https://www.python.org/downloads/windows/. On the installer's first screen tick
   "Add python.exe to PATH" before Install.
4. **After any installer, fully quit and reopen the terminal AND Claude Code desktop.** A program
   that was already open cannot see a newly installed tool. **This happened on 2026-09-16:** Git
   was installed and registered on the machine's PATH, but the open Claude session reported it
   missing, and winget then said it was already installed.
5. **Get the repository and the one library the console needs:**
   ```
   git clone https://github.com/jacobbkatz/We-Are-STMING
   cd We-Are-STMING
   py -m pip install pyserial
   ```
   **No GitHub sign-in is needed to clone**: the repository is public (checked 2026-09-16 with no
   credentials). **Pushing does need a sign-in.** The folder can be anywhere, and every command in
   this project runs from inside it. Jacob's copy is in a folder on the OneDrive desktop.
   `py -m pip` installs into the same Python that `py` runs, which avoids the classic mismatch.
   A warning that `pyserial-miniterm.exe` "is not on PATH" is harmless.
6. **Prove the tools run before going near the bench**, with nothing plugged in:
   ```
   py Code/pc/stm_console.py GSTS
   ```
   **The pass, seen 2026-09-16, is exactly `No Teensy found. Ports seen:` with nothing after it.**
   It exits with code 1, which is normal for this check. An error mentioning `serial` or "module
   not found" means pyserial went into a different Python; rerun `py -m pip install pyserial`.

**The automatic start-of-session check needs Git's bash.** `.claude/settings.json` runs
`bash .claude/session-start.sh`, and on Jacob's machine `bash` is not on the PATH. Git's copy is
inside the Git install folder, under `bin`. **Whether Claude Code desktop finds it on its own is
UNKNOWN.** If a session opens without printing `=== We-Are-STMING: sync check ===`, Claude should
pull by hand and run `py Code/pc/check_facts.py` before starting work. **The commit guard does work
here**: Git runs it with its own bash, and since 2026-09-16 it picks whichever of `python3`,
`python` or `py` actually runs.

**`pyserial` alone is enough for `stm_console.py`.** `numpy` and `matplotlib` are only needed by
`adc_stats.py` and the GUI.

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
(which sign of `MTMV` advances). **The motor sign is PROVISIONALLY `negative`, found 2026-09-16** —
see `docs/OPEN_QUESTIONS.md` for why only provisional; the Z direction is still UNKNOWN. **The
example above uses `positive` only to show the syntax — do not copy it.** Determine both with the
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
| ~~`stm_control.py:37`~~ | `adc_to_amp` uses `10.24` V full scale | **NOT A BUG — corrected 2026-09-07. The datasheet gives ±10.24 V. Leave it alone.** 4.096 V is REFBUF; the input span is 2.5 × REFBUF |

A fifth item reported in the old handoff — `get_status()` returning `self.history[-1]` on an empty
list — is **unreachable dead code**, not a live bug: the method already returns at line 92 when
busy, so the branch at line 95 can never run. Recorded so nobody hunts for it.

## Do not use stm_app.py

The Tkinter GUI has buttons wired directly to the two most dangerous paths in the firmware:

- **"Approach"** sends `APRH`, whose signed comparison can drive the tip into the sample without
  ever triggering. Use `stm_approach.py` instead.
- **"ConstCurrentOn"** sends `CCON`, which snaps Z to midscale from wherever it was — up to a
  ~180 nm lurch. See `STATUS.md` fault 2. **Fixed in the firmware on 2026-09-16, uploaded and
  bench-tested**, so `CCON` now starts from the current Z. The GUI stays off-limits either way, for the
  `APRH` button above.

Its motor control is broken independently of both. Use `stm_console.py` and `stm_approach.py`.

## Known issue

`stm_control.py` and `stm_console.py` hardcode the ADC full scale as **10.24 V**, while the
firmware driver's `_ref_buffer_volts` is **4.096**, which is the **REFBUF** voltage, not the input
span. **Resolved 2026-09-07 from the datasheet: the input full scale is ±10.24 V = 2.5 × REFBUF, so
the PC tools are correct.** The older text below argued for 4.096 and was wrong — the schematic
shows the LTC2326 running on its own internal reference. See `docs/UPSTREAM_MECHPANDA.md` §1.

**Every current these tools print is therefore 2.5x too large.** The constant is deliberately not
changed yet, because it should land with the meter calibration that proves it.
