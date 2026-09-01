# Soft Launch — Verified Test Procedure

I re-read every source file and checked each claim from the earlier draft. **Two corrections and
one critical new finding came out of it.** Everything below is now quoted from the code rather
than remembered.

Files checked: `main.cpp`, `stm_firmware.hpp`, `AD5761.cpp/.hpp`, `LTC2326_16.cpp/.hpp`,
`EfficientStepper.cpp/.hpp`, `logTable.hpp`, `stm_control.py`, `platformio.ini`.

---

# READ THIS FIRST

## 1. Your terminal must send the whole command at once. This is critical.

This is the thing most likely to waste your day, and I missed it in the first draft.

```cpp
void checkSerial(STM &stm)
{
  String serialString;
  if (Serial.available() > 0)          // triggers as soon as ONE character arrives
  {
    for (int i = 0; i < CMD_LENGTH; i++)   // then immediately reads FOUR
    {
      char inChar = Serial.read();
      serialString += inChar;
    }
    serialCommand(serialString, stm);
  }
}
```

The firmware starts reading as soon as **one** character is available, then immediately reads
four. If the other three haven't arrived yet, `Serial.read()` returns **-1** for each, which
becomes character 0xFF. The command string turns to garbage, matches nothing, and is silently
discarded.

**What this means practically:**

| Terminal | Works? | Why |
|---|---|---|
| Arduino Serial Monitor | **Yes** | Buffers your line, sends on Enter |
| CoolTerm using "Send String" | **Yes** | Sends the whole string at once |
| PuTTY / `screen` / minicom, typing live | **NO** | Sends each keystroke as you type it |
| Python `pyserial` script | **Yes** | Sends the whole write at once |

If you type `GSTS` letter by letter into `screen`, the `G` triggers the read and the other three
reads return -1. You get nothing back and it looks like a dead board.

**Use the Arduino Serial Monitor** if you have the Arduino IDE installed — simplest option that
definitely works. Set it to 115200 baud and "No line ending" or "Newline", either is fine.

## 2. Correction: X and Y are ±3 V, not ±5 V

The firmware comments are wrong. `AD5761.cpp` writes `_mode` straight into the AD5761 control
register:

```cpp
void AD5761::reset()
{
    write(CMD_SW_FULL_RESET, 0);
    delay(100);
    write(CMD_WR_CTRL_REG, _mode);   // the low 3 bits are the output range
}
```

The AD5761's range bits RA[2:0] are: `000` = ±10 V, `010` = ±5 V, `101` = ±3 V.

Now compare what's actually configured:

```cpp
AD5761 dac_x = AD5761(DAC_1, 0b0000000000000101);    // comment says -5 to 5V
AD5761 dac_y = AD5761(DAC_2, 0b0000000000000101);    // comment says -5 to 5V
AD5761 dac_z = AD5761(DAC_3, 0b0000000000000000);    // comment says -10 to 10V
AD5761 dac_bias = AD5761(DAC_4, 0b0000000000000101); // comment says -3 to 3V
```

X and Y use range bits `101`, the same as bias. So:

| DAC | Range bits | Actual range | Firmware comment |
|---|---|---|---|
| X | 101 | **±3 V** | says ±5 V — **wrong** |
| Y | 101 | **±3 V** | says ±5 V — **wrong** |
| Z | 000 | ±10 V | correct |
| bias | 101 | ±3 V | correct |

Nothing breaks because of this — the DACs do whatever the register says regardless of the
comment. But your **scan range is smaller than the comments imply**, and every voltage number the
GUI reports for X, Y and Z is wrong (it assumes ±5 V for all three).

## 3. The GUI's motor button does nothing

```python
def move_motor(self, steps):
    self.send_cmd('MTMV {steps}')      # missing the f prefix
```

Sends the literal text `MTMV {steps}`. `Serial.parseInt()` finds no digits and returns 0, so the
motor moves zero steps. Silently. Use the serial terminal for motor testing today.

## 4. Two more GUI bugs

```python
except:
    print('no response')
    return self.history[-1]        # IndexError if history is still empty
```

and

```python
self.stm_serial.set_buffer_size(rx_size=128000, tx_size=128000)   # Windows only
```

`set_buffer_size` doesn't exist on Mac or Linux pyserial and throws `AttributeError`.

## 5. There's a built-in piezo test, and it's the best test available today

```cpp
if (command == "TEST") { stm.test_piezo(); }
```

```cpp
void test_piezo()
{
    for (int i = 0; i < 500; i++) { set_dac_z(50000); delayMicroseconds(500);
                                    set_dac_z(00000); delayMicroseconds(500); }
    delay(1000);
    // then the same for X, then Y
}
```

500 cycles at 1 kHz per axis. **Given the ranges above**, the actual swings are:

- **Z**: code 0 → −10 V, code 50000 → +5.3 V. **A 15.3 V swing.**
- **X and Y**: code 0 → −3 V, code 50000 → +1.6 V. A 4.6 V swing.

The piezo is a buzzer, so at 1 kHz **you should hear it**. This is a real end-to-end test of
DAC → ribbon → controller → J1 → piezo with no tip and no sample. Details in Stage 5.

## 6. The ADC library's chip-select polarity looks inverted

```cpp
digitalWrite(_cs, HIGH);      // set HIGH before the transfer
val = SPI1.transfer16(0x00);
digitalWrite(_cs, LOW);       // LOW after
```

Chip select is normally active-low. This is backwards from convention — but that pin (38) goes to
the ADC's **RDL/SDI read-enable**, not a plain chip select, so it may be correct for this part.
Berard's original presumably worked.

**Don't change it preemptively.** If the ADC returns garbage in Stage 4, this is the first thing
to try swapping. Also note `beginTransaction` is never matched with `endTransaction`, in both this
and `AD5761::write` — untidy, generally harmless.

---

# Stage 0 — Before any power

The highest-consequence check in the project. Re-confirm if you're not certain:

- Yellow wire → IC1 pin 7: **beeps**
- Orange wire → IC1 pin 4: **beeps**
- Yellow → Orange directly: **silent**

---

# Stage 1 — Digital only, analog supply disconnected

**Goal:** prove the Teensy, USB link and firmware are alive with zero risk to anything analog.

## What runs automatically at power-on

```cpp
void setup()
{
  Serial.begin(115200);
  SPI.begin();
  SPI1.setSCK(27); SPI1.setCS(38); SPI1.setMISO(39);
  SPI1.begin();
  stm.reset();
}
```

`reset()` runs on **every** power-up before you type anything:

```cpp
void reset()
{
    stepper_motor.setSpeed(2);
    stepper_motor.reset();
    dac_x.reset(); dac_y.reset(); dac_z.reset(); dac_bias.reset();
    stm_status = STMStatus();
    ltc2326.convert();
}
```

Each `dac.reset()` does a software reset, **waits 100 ms**, then writes the range register. Four
DACs means **roughly half a second of boot time** before the board answers anything. If your first
command right after plugging in gets no reply, wait a second and retry.

## Steps

1. **USB only.** Bench supply not connected.
2. Confirm the computer sees a serial device.
3. Open the Arduino Serial Monitor (or another whole-line terminal — see finding 1) at
   **115200 baud**.
4. Send: `GSTS`

## What GSTS returns

```cpp
sprintf(buffer, "%d,%d,%d,%d,%d,%d,%d,%d,%d,%lu",
        bias, dac_z, dac_x, dac_y, adc, steps,
        is_approaching, is_const_current, is_scanning, time_millis);
```

Ten comma-separated fields:

| # | Field | Expected now |
|---|---|---|
| 1 | bias | 0 |
| 2 | dac_z | 0 |
| 3 | dac_x | 0 |
| 4 | dac_y | 0 |
| 5 | adc | live reading — see note |
| 6 | steps | 0 |
| 7 | is_approaching | 0 |
| 8 | is_const_current | 0 |
| 9 | is_scanning | 0 |
| 10 | time_millis | increases every call |

**On field 5:** the main loop calls `stm.update()` continuously, and `update()` calls
`read_adc_raw()` and stores the result. So the adc field is **live data, refreshed constantly** —
not a stale zero. With nothing connected to the tip it's meaningless as a measurement, but it
should be a plausible number and it should change slightly between reads (noise). A field 5 that
is *identically* 0 every single time may mean the ADC isn't converting.

**Pass:** ten fields, `time_millis` climbing between calls.

**Fail:**
- Nothing at all → check you're using a whole-line terminal (finding 1), then baud rate, then
  that the USB cable carries data.
- Garbled characters → wrong baud rate.
- `time_millis` never increases → the board is resetting repeatedly, check power.

---

# Stage 2 — Motor test, still no analog power

## The code path

```cpp
if (command == "MTMV") { int value = Serial.parseInt(); stm.move_motor(value); }
```

```cpp
void move_motor(int steps)
{
    stepper_motor.step(steps);
    stm_status.steps = stepper_motor.get_total_steps();
    stm_status.time_millis = millis();
}
```

```cpp
EfficientStepper stepper_motor = EfficientStepper(STEPS_PER_REVOLUTION, IN1, IN3, IN2, IN4);
```

`IN1..IN4` are pins 33, 34, 35, 36, and `EfficientStepper.cpp` passes them straight through
unchanged to the Arduino Stepper library. So the library gets pins in the order **33, 35, 34,
36** — the 1-3-2-4 coil mapping, done in software. **That is why your driver is wired straight
across.** Cross the wires too and the two swaps cancel: the motor buzzes and doesn't turn.

## Speed — it is meant to be slow

`reset()` sets `setSpeed(2)` — **2 RPM**. At 2048 steps/revolution:

- `MTMV 512` (quarter turn) ≈ **7.5 seconds**
- `MTMV 2048` (full turn) ≈ **30 seconds**

`step()` also **blocks** — the firmware does nothing else until the move completes, so `GSTS`
won't answer mid-move. Neither is a fault.

## Steps

1. Serial terminal, not the GUI.
2. Send `MTMV 512`.
3. Four driver LEDs chase in a rolling pattern; shaft turns about a quarter turn over ~7.5 s.
4. Send `GSTS` — field 6 (**steps**) should now read `512`.
5. Send `MTMV -512` — turns back, steps returns toward 0.

## Failure modes

| Symptom | Cause |
|---|---|
| Buzzes, doesn't turn | Wires crossed, undoing the software 1-3-2-4 mapping |
| Nothing, no LEDs | Driver minus terminal not on Teensy GND |
| LEDs chase, shaft still | Connector not seated, or mechanical bind |
| steps field never changes | Command not reaching the parser — see finding 1 |

## Expected behaviour later

`EfficientStepper::disable()` sets all four pins LOW to cut current and heat, and the approach
routine calls it on completion. After a successful approach the LEDs go dark and the motor goes
silent — correct, not a fault. `step()` calls `enable()` automatically next time.

---

# Stage 3 — Bringing up the analog supply

First stage with real consequences.

> **TIP OUT BEFORE THIS STAGE, not before Stage 5.** This was originally written as a Stage 5
> precaution and that is too late. `AD5761::reset()` configures the control register but never
> writes a DAC data register, so the DACs sit at their power-up default of zero scale. **Z is at
> −10 V from the instant the rails come up**, with no command from you. If a tip is installed and
> near the sample when you switch on, that full-range excursion happens on its own. See
> `DAC_BOOT_STATE.md`.

1. **Tip removed, or sample well clear.** See above.
2. **Set the voltage before connecting anything.** Roughly **±18 V** into V++/V−−, not ±15 V —
   the on-board regulators need headroom above their ±15 V output.
3. **Re-check polarity** against your labels.
4. **Set a low current limit** if you have one — a few hundred mA turns a missed short into "the
   supply limits" rather than "something cooks."
5. Connect to the board's power input (**U19**, the 3-pin JST — *not* J2, which is an output).
6. Power on. **Watch and smell for several seconds.** No smoke, no burning smell, nothing hot.
7. Check current draw — modest and stable, not pegged.
8. **Check LED5 and LED6.** See below. This is the fastest read on whether both rails came up.

**If anything smells wrong or current pegs, power off immediately.** Note what you saw and we'll
trace it rather than guessing under power.

## LED5 and LED6 are your rail instruments

Traced from the PCB file: **LED5 indicates V++ present, LED6 indicates V-- present.** They are
independent, one per leg of the bipolar supply.

| LED5 | LED6 | Reading |
|---|---|---|
| on | **on** | Both rails up. This is what you want |
| on | **off** | **STOP.** V++ present, V-- missing. Half-powered bipolar supply |
| off | off | Neither rail. Supply off, not connected, or not delivering |

**Important caveat so this is not misread:** with the bench supply **off** but USB connected,
LED1-5 light and LED6 stays dark. That is phantom powering from the Teensy backfeeding through
the SPI lines' ESD clamps into the 3.3V rail and on through U16 into V++, and it is **not** a
fault. It was confirmed by test: unplugging USB with the supply off made LED1-5 go dark.

So the LED5-on/LED6-off pattern only means a genuine fault **when the bench supply is switched
on**. With the supply off it is expected. Full detail in `PROJECT_HANDOFF_SUMMARY.md`.

LED1-4 are the four DACs' ALERT pins (U1-U4 pin 1), pulled up from the 3.3V rail. They are not
SYNC indicators.

## Once both rails are confirmed, park the DACs

The DACs power up at zero scale, not midscale. Before doing anything else, put them at 0 V:

```
DACZ 32768
DACX 32768
DACY 32768
BIAS 32768
```

Then `GSTS` to confirm the fields read back 32768. That takes Z off the −10 V rail.

---

# Stage 4 — DACs and ADC

## Values are raw DAC codes, not volts

0–65535, centre 32768. Using the **corrected** ranges from finding 2:

| Code | Bias (±3 V) | X or Y (±3 V) | Z (±10 V) |
|---|---|---|---|
| 0 | −3 V | −3 V | −10 V |
| 32768 | 0 V | 0 V | 0 V |
| 33314 | **+50 mV** | +50 mV | +166 mV |
| 65535 | +3 V | +3 V | +10 V |

33314 is the typical tunneling bias referenced in the project notes, and it works out to ~50 mV
on a ±3 V range — consistent.

The current conversion, from `stm_control.py`, confirms your hardware:

```python
def adc_to_amp(adc): return 1.0 * adc / 32768 * 10.24 / 100e6
```

That's your **100 MΩ** feedback resistor and a **10.24 V** ADC full scale.

## Steps

1. `GSTS` — confirm format still correct with analog power present.
2. `BIAS 33000` then `GSTS` — field 1 (**bias**) should read back `33000`.
   This proves the *firmware* registered the command. It does **not** prove the DAC chip output
   the right voltage — that needs a meter on the DAC output pin.
3. `ADCR`:

```cpp
if (command == "ADCR") { int val = stm.read_adc(); Serial.println(val); }
```

```cpp
int read_adc() { read_adc_raw(); return _get_adc_avg(); }
int _get_adc_avg() { return static_cast<int>(_adc_sum / 5.0); }
```

It returns a **5-sample rolling average**, so call it five or six times and let it settle before
judging. You want a plausible number that varies slightly.

**Always exactly 0, always 65535, or wild garbage** → the ADC isn't converting properly. Check
ribbon pin 6 (read-enable) and pin 38, and see finding 6 about CS polarity.

4. `BIAS 32768` to return bias to 0 V.

---

# Stage 5 — Piezo test with TEST

The most valuable test today. No tip, no sample, no approach.

## Before you run it

Z swings **−10 V to +5.3 V** at 1 kHz, 500 times. That's a big, fast swing — it's the author's own
test routine, so it's intended, but it is not gentle.

**Have the tip either not installed, or well clear of the sample.** Z is moving full range.

## Run it

Send: `TEST`

Then **listen**. Z first, one second pause, then X, pause, then Y. Each should produce an audible
1 kHz buzz for about a second.

> ### TEST LEAVES Z AT −10 V WHEN IT FINISHES. RE-PARK IMMEDIATELY.
>
> Confirmed by readback on 2026-08-29. `test_piezo()` ends each axis on `set_dac_*(00000)`:
>
> ```cpp
> for (int i = 0; i < 500; i++) { set_dac_z(50000); delayMicroseconds(500);
>                                 set_dac_z(00000); delayMicroseconds(500); }
> ```
>
> The loop's last write is code 0, and nothing restores midscale afterwards. `GSTS` immediately
> after a TEST read `32768,0,0,0,...` - bias still parked, but **Z, X and Y all sitting at zero
> scale**, which is **Z at −10 V, X and Y at −3 V**.
>
> This recreates exactly the power-on hazard described in `DAC_BOOT_STATE.md`, except it happens
> silently in the middle of a session when you may well have a tip installed.
>
> **Always send this straight after any TEST:**
>
> ```
> DACZ 32768
> DACX 32768
> DACY 32768
> ```
>
> Then `GSTS` to confirm all three read 32768 again.

| What you hear | Meaning |
|---|---|
| Three distinct buzzes | DAC → ribbon → J1 → piezo works on all three axes |
| Only some buzz | The silent axis has a wiring fault — trace that quadrant |
| Nothing | No signal reaching the piezo, or the disc is depolarised |
| Very weak | Partial connection, or a damaged disc |

X and Y will sound quieter than Z — they swing 4.6 V versus Z's 15.3 V. That's expected, not a
fault.

This exercises three of your four DACs end to end through real hardware. Nothing else today does
that. The bias DAC isn't covered here — you verified that by readback in Stage 4.

---

# Stage 6 — Preamp sanity check, tip disconnected

With the ±15 V rails up and the **tip physically disconnected** from the input standoff:

1. Probe the preamp output (OUT pin on the header) with a DC voltmeter or scope.
2. **Expected:** a stable DC voltage sitting still, typically near 0 V with no input current.
3. **Concerning:** railed to +15 V or −15 V (saturated or damaged), or oscillating rather than
   still (feedback or grounding problem).

Disconnecting the tip is deliberate — it separates "is the amplifier healthy" from "are we
tunneling yet."

---

# Explicitly not today

- **No `APRH`.** It drives Z while stepping the motor forward, hunting for a current threshold —
  it moves the tip toward the sample automatically.
- **No `SCST`.** Assumes a tip in tunneling range.
- **No `CCON`.** Assumes an established tunnel current.

Worth knowing for later: the PID gains **start at zero**, not at the INIT values.

```cpp
#define INIT_KP 2.0
#define INIT_KI 1.0
#define INIT_KD 1.0
...
double Kp = 0.0, Ki = 0.0, Kd = 0.0;
```

The INIT defines are only referenced in a commented-out line. So constant-current mode does
nothing until you set gains with `PIDS`.

---

# Command reference for today

| Send | Effect |
|---|---|
| `GSTS` | Ten-field status line |
| `MTMV 512` | Move stepper 512 steps (≈7.5 s at 2 RPM) |
| `MTMV -512` | Move back |
| `BIAS 33000` | Set bias DAC raw code |
| `BIAS 32768` | Bias back to 0 V |
| `ADCR` | One ADC read (5-sample average) |
| `TEST` | Buzz Z, X, Y in turn |
| `RSET` | Re-run the boot reset |
| `STOP` | Clear approaching / const-current / scanning flags |

All commands are **exactly four characters**, sent as one burst. Arguments follow after a space.

---

# Optional: fix the GUI before you use it

```python
# 1. missing f-string
def move_motor(self, steps):
    self.send_cmd(f'MTMV {steps}')

# 2. don't crash on an empty history
except Exception:
    print('no response')
    return self.history[-1] if self.history else self.status

# 3. Windows-only call
try:
    self.stm_serial.set_buffer_size(rx_size=128000, tx_size=128000)
except AttributeError:
    pass
```

There's also a latent bug in `start_scan()` — the `else` branch calls
`_process_full_line(data_line)` using a stale variable rather than `current_line`. Won't bite you
today, will when you start scanning.

And if you want the GUI's voltage readouts to be truthful, correct the X/Y/Z conversions per
finding 2 — they currently assume ±5 V for all three, when X and Y are ±3 V and Z is ±10 V.
