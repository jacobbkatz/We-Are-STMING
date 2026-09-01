# Firmware command reference

Every command the Teensy understands, derived from `Code/teensy/src/main.cpp` and
`Code/teensy/src/stm_firmware.hpp`.

---

## How to send them

```bash
python Code/pc/stm_console.py GSTS          # one command and exit
python Code/pc/stm_console.py DACZ 32768
python Code/pc/stm_console.py               # interactive
```

**Use `stm_console.py`, not a generic serial monitor.** The firmware's `checkSerial()` starts
reading as soon as one byte arrives and then immediately reads four. Anything that sends
per-keystroke — PlatformIO's monitor, PuTTY, screen, minicom — loses that race and the command is
**silently discarded**. `stm_console.py` sends each command as a single write.

**Every command is exactly four characters.** Arguments follow, separated by spaces.

Holding the serial port open blocks `teensy_reboot` during upload, which makes the Teensy Loader
ask for the PROGRAM button on every flash. In interactive mode, type `free` to release the port
before uploading.

---

## Commands

### Status and reading

| Command | Arguments | Replies | What it does |
|---|---|---|---|
| `GSTS` | — | yes | Ten comma-separated fields, see below |
| `ADCR` | — | yes | One ADC reading, **5-sample rolling average** |
| `IVGE` | — | yes | Dump the last IV curve |

**`GSTS` returns:** `bias, dac_z, dac_x, dac_y, adc, steps, is_approaching, is_const_current,
is_scanning, time_millis`

> **`GSTS` field 5 (`adc`) is a RAW single conversion. `ADCR` is a 5-sample average.**
> Use `GSTS` for noise work, because averaging hides exactly the isolated bit-flips a marginal
> SPI link produces. Use `ADCR` for a settled value.

> **The other `GSTS` fields are firmware bookkeeping, not measurements.** It will report
> `dac_z = 65535` while the chip outputs nothing, because there is no DAC readback. See
> `docs/WIRING.md` section 3.

### Setting outputs

| Command | Arguments | Range | Notes |
|---|---|---|---|
| `DACX` | value | 0–65535, 32768 = 0 V | X piezo, **±3 V** |
| `DACY` | value | 0–65535, 32768 = 0 V | Y piezo, **±3 V** |
| `DACZ` | value | 0–65535, 32768 = 0 V | Z piezo, **±10 V** |
| `BIAS` | value | 0–65535, 32768 = 0 V | Sample bias, **±3 V**. Inverts: 65535 gives −3 V at the holder |

All four are silent — they reply with nothing.

### Motor

| Command | Arguments | Notes |
|---|---|---|
| `MTMV` | steps | Blocks while moving. ~68.3 steps/s, so 512 steps takes about 7.5 s |

2048 steps per revolution, verified by measurement.

### Reset

| Command | What it does |
|---|---|
| `RSET` | Full reset: all four DACs, the stepper, and the status struct |

> **`RSET` slams Z to a rail.** `AD5761::reset()` sends a software full reset, which is zero
> scale. It also zeroes the bias, the step counter, and every setpoint. **Re-park Z at 32768
> after every `RSET`.** The same applies after `TEST`.

### Piezo test

| Command | Arguments | Blocks for | Notes |
|---|---|---|---|
| `TEST` | — | ~3.5 s | 1 kHz square on Z, then X, then Y. **Leaves the axis at a rail** |
| `TONE` | freq_hz duration_ms | the duration | Square wave on Z, symmetric about midscale, **parks at 0 V on exit** |

**Prefer `TONE`** — it parks Z at 0 V instead of leaving it at a rail.

> **There is no usable resonance to hunt for.** A sweep on 2026-08-31 found no loudness peak
> between 1 kHz and 11 kHz once the disc is mounted. The old advice to use `TONE 8600` as a
> standard check is retired. Judge the piezo with a meter, not by ear.

Note `play_tone()` computes `half_us = 500000/freq - 25`, subtracting a fixed 25 µs guess for the
SPI write. At 8600 Hz that correction is 43% of the half period, so **the actual output frequency
at the top of the range may be off by some percent.**

### Approach

| Command | Arguments | Notes |
|---|---|---|
| `APRH` | adc_target step_interval | **Do not use. See the warning** |

> ### Do not run `APRH`
>
> Two reasons, both in the source:
>
> 1. `approach()` tests `read_adc() > target`, a **signed** comparison, against a baseline that
>    has been negative for the whole project. **If tunneling drives the reading more negative, it
>    never triggers** and the motor keeps driving the tip into the sample.
> 2. The second argument is the **step interval, not a step count.** Max travel is hardcoded at
>    10000 steps in `main.cpp`, about 4.9 motor revolutions.
>
> Use a PC-side approach loop instead, with the threshold on absolute deviation from baseline.
> `Code/pc/stm_approach.py` is planned but **not yet written.**

### Constant current and scanning

| Command | Arguments | Notes |
|---|---|---|
| `CCON` | adc_target | Turn on constant-current mode |
| `CCOF` | — | Turn it off |
| `PIDS` | Kp Ki Kd | Set PID gains. They default to 0.0 |
| `SCST` | x_start x_end x_res y_start y_end y_res samples_per_pixel | Start a scan. Blocks for a long time |
| `IVME` | bias_start bias_end bias_step | Sweep bias and record an IV curve, max 1000 points |
| `STOP` | — | Clear the approaching, constant-current and scanning flags |

`SCST` streams scan lines back as `A,<row>,<values...>` for the ADC and `Z,<row>,<values...>` for
the Z heights, then prints `D` when done.

---

## Which commands block

The firmware is single-threaded. While a blocking command runs, `loop()` never reads serial, so
anything you send lands in the buffer and gets misread as garbage. `stm_console.py` waits these
out for you.

| Command | Blocks for |
|---|---|
| `TEST` | ~3.5 s |
| `TONE` | the requested duration |
| `MTMV` | steps ÷ 68.3 seconds |
| `APRH` | up to ~120 s |
| `IVME` | up to ~60 s |
| `SCST` | minutes |

Only `GSTS`, `ADCR` and `IVGE` reply with anything. Everything else is silent, so waiting for a
response from them just burns the timeout.

---

## Before every measurement

1. **Look at LED1–LED4.** If any is lit, the DACs have lost configuration and **the reading is
   void.** Send `RSET`, then re-park Z at 32768.
2. **Check nobody is within a metre of the preamp.** A person injects 20–50 nA; a tunneling
   current is about 1 nA.
3. **Look at LED1–LED4 again afterwards.** The configuration can drop during the measurement.
