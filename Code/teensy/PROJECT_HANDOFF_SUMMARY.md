# We Are STMing — Project Handoff Summary

For briefing a fresh Claude instance. This covers what the project is, what's been verified,
and exactly where things stand right now.

> ## READ `SESSION_2026-08-31_RESULTS.md` FIRST
>
> Session 3 (2026-08-31) contradicts **six** claims in this document, all backed by
> measurements. Where the two disagree, that file is newer and correct. In particular:
>
> - **Stage 6 is NOT an open feedback loop.** It is 37 nA of input leakage from cyanoacrylate
>   contamination. The preamp is being rebuilt
> - **The ADC bus was running at 40 MHz**, not the "library default" this document records.
>   Now 1 MHz
> - **NEW FAULT: all four DACs lose configuration roughly hourly, and software cannot detect
>   it.** Check LED1-4 before AND after every measurement. This cost an hour on 2026-08-31
> - **The bias path to the sample holder PASSES**, tested for the first time
> - **The mounted piezo has no usable resonance.** `TONE 8600` is retired as a check
> - **One JP1 ground pin really is open.** The retraction in A.5.8 over-corrected

---

## What this is

A 3D-printed Scanning Tunneling Microscope, built by two beginners with no prior electronics or
soldering experience, based on two open-source designs:

- **Mech Panda's red-panda-stm** — 3D-printed mechanics, Teensy 4.1 firmware, controller PCB
- **Dan Berard's Home-Built STM** — scan head concept, tip prep, transimpedance preamplifier

GitHub: `github.com/jacobbkatz/We-Are-STMING`

Hardware is fully built and wired. **Today's session is the first-ever firmware flash and power-up
test** — nothing has been powered before this.

---

## Hardware, as built

- Controller: **fabricated PCB** (JLCPCB-assembled), 103.38 x 88.08 mm
- Teensy 4.1: on a **hand-wired protoboard**, joined to the controller PCB by a 26-pin ribbon
- Motor driver: **separate ULN2003 board**, not on the controller PCB
- Print material: **PETG-CF** (PA-CF was tried first, too hard to print reliably)
- Isolation: springs + **eddy-current damping** (aluminium plate through fixed magnets) — no
  heavy plate stack
- Preamp: OPA627AU, **100 MOhm feedback resistor, air-wired** (see below)
- Enclosures: custom-designed, printed, all dimensioned from the real Gerber/STL files

---

## Verified electrical facts — do not re-derive, do not contradict without strong evidence

All traced from the actual Gerber files (copper layers + manufacturing netlist + drill data) and
cross-checked against the firmware source. Several early drafts had errors that were caught and
fixed — the numbers below are the corrected, final versions.

### Controller board power
- **Power goes IN at U19**, a 3-pin JST XH connector (V++, AGND, V--), roughly **+/-18 V**
- On-board regulators make +/-15 V, 3.3 V, 5 V from that
- **J2's +/-15 V pins are OUTPUTS feeding the preamp, not power inputs.** Do not connect a
  supply to J2.

### Controller board LEDs — what each of the six actually indicates
Traced from the EasyEDA PCB file (`PCB/STMP_easyEDA.zip`), PAD_NET records. All six are the
same red indicator part. Exact connections:

| LED | Fed from | Through | Sinks into | Indicates |
|---|---|---|---|---|
| LED1 | **3.3V rail** | R1 | U1 pin 1 | DAC 1 ALERT asserted |
| LED2 | **3.3V rail** | R2 | U2 pin 1 | DAC 2 ALERT asserted |
| LED3 | **3.3V rail** | R3 | U3 pin 1 | DAC 3 ALERT asserted |
| LED4 | **3.3V rail** | R4 | U4 pin 1 | DAC 4 ALERT asserted |
| LED5 | **V++** | R27 | AGND | positive input rail present |
| LED6 | AGND | R33 | **V--** | negative input rail present |

Pin 1 being ALERT is read off the standard AD5761 pinout, and the surrounding pins corroborate
it strongly: pad 4 = VREF1, 5 = AGND, 6 = -15V, 7 = XOUT, 8 = +15V, 12 = SDI, 13 = SYNC1,
14 = SCLK, 15 = 3.3V, 16 = AGND. Ten pins match the datasheet pinout exactly, so pin 1 = ALERT
is reliable. **LED1-4 are not SYNC indicators** (SYNC1 is pad 13, not pad 1).

### Power tree, from the same source
| Regulator | In | Out |
|---|---|---|
| U19 | 3-pin JST input | V++, AGND, V-- |
| U17 | V++ | +15V |
| U18 | V-- | -15V |
| U16 | V++ | **3.3V** |
| U22 | V++ | 5V |

Note that **the 3.3V rail is derived from V++ by U16.** There is no 3.3V or 5V on the H1 ribbon
(all odd pins AGND, even pins signal, 24/26 dead), so with the bench supply off the 3.3V rail
has no legitimate source.

### Reading LED1-5 lit with the bench supply switched OFF — expected, not a fault
Observed on 2026-08-29: LED1 through LED5 lit, LED6 dark, bench supply connected but **off**,
Teensy powered over USB. This is **phantom powering (parasitic backfeed) from the Teensy** and
is fully explained:

1. The Teensy drives SCLK (pad 14), SDI (pad 12) and SYNC1-4 (pad 13) into U1-U4 at 3.3 V.
2. Those digital inputs have ESD clamp diodes to their own digital supply, which is pad 15,
   **the board's 3.3V net**. With that rail at 0 V the clamps forward-bias and pull the whole
   3.3V net up to roughly 3.3 − 0.6 ≈ **2.7 V**.
3. That phantom 2.7 V feeds R1-R4, so **LED1-4 glow.**
4. It also reaches U16's output pin. Current flows backward through U16 to its input, raising
   **V++ to roughly 2.1 V**, which lights **LED5** through R27.
5. **Nothing can phantom-generate a negative rail.** Backfeed only pushes positive, so V-- stays
   at 0 and **LED6 stays dark.**

That predicts exactly the pattern observed.

**CONFIRMED by test, 2026-08-29.** With the bench supply off throughout, the USB was unplugged
and LED1 through LED5 all went dark. Reconnecting USB brought them straight back on, steady, no
flashing. The Teensy is the only thing lighting them. Phantom powering is the correct
explanation and there is no board fault here.

Not damaging at these currents (a few mA through LED paths), and it disappears the moment real
analog power is applied. Do not chase it as a fault.

**Side benefit of that test: the firmware survived a full power cycle.** Uptime went from
~1700 s to 53 s and `steps` reset to 0, so `setup()` and `stm.reset()` re-ran from a cold boot.
That closes out any remaining doubt about whether the flash actually took - it is in flash, not
a leftover RAM image.

**When the supply IS on, the reading is different:** LED5 and LED6 should BOTH be lit. LED5 on
with LED6 dark **while the supply is on** would be a genuine half-powered bipolar rail, and that
is worth stopping for. Usual causes: only one leg switched on, supply not in dual/tracking mode,
the V-- pin of the U19 JST not seated, or a fault in the negative leg.

### CONNECTOR NAMING - read this before hunting for anything on the board

**"J1" and "J2" are documentation names. They are NOT printed on the controller PCB.** This
caused several wasted measurements on 2026-08-29 and 30. Every designator prefix that actually
exists on the controller board is: `C`, `DSUB`, `H`, `LED`, `R`, `U`. **There is no `J` or `JP`
silkscreen on it at all.**

| Name in the docs | Actual silkscreen | Which board | What it is | Where |
|---|---|---|---|---|
| **J1** | **DSUB1** | Controller | DB9 to scan head / piezo | bottom **left** |
| **J2** | **DSUB2** | Controller | DB9 to preamp | bottom **right** |
| **JP1** | JP1 | **PREAMP board** | 5-pin header, ±15 V in and signal out | separate PCB |
| **JP2** | - | - | **Does not exist anywhere in this project** | - |
| - | **H1** | Controller | 26-pin ribbon to Teensy | top **left** |
| - | **U19** | Controller | 3-pin JST power input | **right edge** |

JP1 being on a **physically different board** is the main source of the confusion. It is fed
±15 V from the controller through the DSUB2 cable.

### Controller board physical layout (mm from lower-left of the component area, board ~103 x 88)

```
        LEFT                                              RIGHT
  y=72  .                    U16(54)      U22(73)      U19(91)  <- power JST
  y=67  H1(17) ribbon
  y=63  .                                          LED5(88) LED6(92)
  y=52  .                                                   U18(91)  <- -15V reg
  y=43  U1(6)   U3(21)   U2(35)   U4(49)   U5(60)   <- the four DACs + reference
  y=38  .                                                   U17(91)  <- +15V reg
  y=17  U9(14)          U10(37)           U13(63)   <- output op-amps
  y=0   DSUB1(18)                       DSUB2(74)
```

Both TO-220 regulators and the power input are on the **right edge**. The DACs run across the
middle. The −15 V rail has to cross about 90 mm to reach U1.

### CABLE WIRE COLOURS - JUXINICE DB9-male-to-bare-wire

Both DSUB connectors use this cable (JUXINICE DB9 male to bare wire, 3 ft). Manufacturer's
standard core colour mapping:

| DB9 pin | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| Colour | Black | Brown | Red | **Orange** | **Yellow** | Green | Blue | Grey | White |

#### DSUB2 cable (preamp) - colour to function

| Colour | Pin | Function |
|---|---|---|
| Black | 1 | BIAS (to sample holder) |
| Brown | 2 | PREAMP− |
| Red | 3 | PREAMP+ |
| **Orange** | **4** | **−15 V** |
| **Yellow** | **5** | **+15 V** |
| Green | 6 | AGND |
| Blue | 7 | AGND |
| Grey | 8 | AGND |
| White | 9 | AGND |

#### DSUB1 cable (scan head / piezo) - colour to function

| Colour | Pin | Function |
|---|---|---|
| Black | 1 | AGND |
| Brown | 2 | AGND |
| Red | 3 | AGND |
| Orange | 4 | AGND |
| Yellow | 5 | AGND |
| **Green** | **6** | **Z−Y** |
| **Blue** | **7** | **Z+Y** |
| **Grey** | **8** | **Z−X** |
| **White** | **9** | **Z+X** |

**Note the colours mean completely different things on the two cables.** Orange is −15 V on the
preamp cable and plain AGND on the scan head cable. Do not carry an assumption across.

#### This mapping is independently confirmed by the Stage 0 continuity check

The Stage 0 test done in an earlier session found:

- **Yellow wire -> IC1 pin 7: beeps**
- **Orange wire -> IC1 pin 4: beeps**
- Yellow -> Orange directly: silent

IC1 is the OPA627 on the preamp. On a standard 8-pin op-amp, **pin 7 = V+ and pin 4 = V−**. So
yellow reaching V+ and orange reaching V− matches the colour table exactly: yellow = pin 5 =
+15 V, orange = pin 4 = −15 V. Two independent sources agree.

**Important consequence:** at Stage 0 the orange conductor had good continuity all the way from
the cable to the op-amp's negative supply pin. So the cable itself was sound at that point. If
−15 V is missing at the preamp now, suspicion shifts toward the **DB9 connector mating** rather
than the wire.

### DSUB1 = J1 (scanner DB9)
pin 9 = Z+X, pin 8 = Z-X, pin 7 = Z+Y, pin 6 = Z-Y, pins 1-5 = AGND

**Handy property: the row of 5 is entirely AGND, the row of 4 is entirely Z signals.** So you
never need to count pins or worry about DB9 numbering being mirrored between plug and socket.
Black probe anywhere in the row of 5, red probe anywhere in the row of 4.

### J2 (preamp DB9)
pin 1 = BIAS (to sample holder), pin 2 = PREAMP-, pin 3 = PREAMP+, pin 4 = -15V out,
pin 5 = +15V out, pins 6-9 = AGND

### Preamp board (JP1 header, verified TWICE independently — Gerber net-name attributes AND the
underside silkscreen photo agree)
Held with GND nearest the C1 capacitor:
- pin 1 = GND
- pin 2 = +15 V rail (net internally named "+9V", a leftover label — actual voltage is +15V)
- pin 3 = OUT (net "N$2") — **there is a series resistor (R1) between the op-amp output and this
  pin.** PAD1 sits directly on the op-amp output; JP1 pin 3 is downstream of R1.
- pin 4 = GND
- pin 5 = -15 V rail (net internally "-9V")

### The preamp input node is deliberately air-wired
IC1 (OPA627) pin 2, the inverting input, has **zero copper connected to it on either layer** —
by design, to avoid leakage at picoamp signal levels. The 100 MOhm resistor, the tip's coax
centre conductor, and a link wire to IC1 pin 2 all meet on an **insulated (PTFE) standoff**
pressed into a bare 2.108mm hole near the R2 silkscreen. **PAD1 is the output, NOT the tip
input** — this was a repeated point of confusion, now resolved.

### Teensy <-> ribbon (26-pin, H1) — full pinout
All 13 odd pins = AGND. Even pins:
pin2=ADC_CNV->T19, pin4=ADC_BUSY->T18, **pin6=ADC_SDI(read-enable)->T38** (this one is NOT a
dead/unused pin as first assumed — it's the ADC's RDL read-enable and must be wired),
pin8=ADC_SCK->T27, pin10=ADC_SDO->T39, pin12=SCLK->T13, pin14=SDI->T11, pin16=SYNC4(bias)->T10,
pin18=SYNC2(Y)->T9, pin20=SYNC3(Z)->T8, pin22=SYNC1(X)->T7. Pins 24/26 = dead, unconnected.

**Gotcha: Teensy pin 13 is SCLK AND the onboard LED.** Ribbon pin 12 carries SCLK to T13, which
is also the Teensy 4.1's built-in LED. So that LED sits on the SPI clock net feeding the DACs.
**It is an SCLK activity indicator, not a health indicator.** It dims when that net is loaded and
flickers with SPI traffic. Do not read board health into it.

### Never meter the board with USB connected
Resistance measurements are only valid on a genuinely unpowered circuit. With USB connected the
controller board is **phantom-powered** through the Teensy's I/O pins (see the LED section
below), so:

1. The readings are meaningless, because the circuit is not at 0 V.
2. The meter creates a drain path, and the current to feed it flows through the Teensy's ESD
   clamp diodes, loading its 3.3 V regulator. Observed 2026-08-29 as the onboard LED dimming and
   flickering while probing V++/AGND.

**Unplug USB before any resistance measurement on this board.** No damage resulted from the one
occurrence (uptime stayed continuous at ~1937 s, so the Teensy never even browned out), but it is
not a thing to repeat.

Corroborating detail from the same session: with the supply leads connected but the supply
**off**, LED5 sat visibly **dimmer** than LED1-4. Unplugging the leads made it jump to full
brightness. The switched-off supply was loading V++ and draining the phantom voltage. Further
confirmation that the backfeed explanation is correct.

### Stepper motor — wired STRAIGHT, not crossed
Teensy 33->IN1, 34->IN2, 35->IN3, 36->IN4, driver minus->Teensy GND, driver plus->Teensy 5V/VIN
(matches how Mech Panda's own build appears to be powered, confirmed from his video).
**The 1-3-2-4 coil order is handled IN SOFTWARE** —
`EfficientStepper(steps, IN1, IN3, IN2, IN4)` passes pins in that order to the underlying
Stepper library. Do not also cross the physical wires — that would cancel the software mapping
and make the motor buzz instead of turn. **The motor does NOT go through the ribbon cable** —
there is no motor circuitry anywhere on the controller PCB.

### DAC output ranges — CORRECTED, firmware comments are wrong
```
AD5761 dac_x = AD5761(DAC_1, 0b0000000000000101);   // comment says +/-5V, ACTUALLY +/-3V
AD5761 dac_y = AD5761(DAC_2, 0b0000000000000101);   // comment says +/-5V, ACTUALLY +/-3V
AD5761 dac_z = AD5761(DAC_3, 0b0000000000000000);   // +/-10V, comment correct
AD5761 dac_bias = AD5761(DAC_4, 0b0000000000000101); // +/-3V, comment correct
```
The AD5761 range bits `101` = +/-3V (not +/-5V as the code comments claim). X and Y are
therefore +/-3V. This means the GUI's voltage readouts for X/Y/Z are all wrong (it assumes
+/-5V for all three). DAC codes: 0-65535, centre=32768=0V.

---

## Firmware behavior — verified from actual source, not assumed

- `setup()` calls `stm.reset()` automatically on every boot — resets all 4 DACs (each with a
  100ms delay, so ~0.5s total boot time), sets motor speed to 2 RPM, zeroes status.
- **Serial commands are exactly 4 characters**, and `checkSerial()` starts reading as soon as
  ONE character is available, then reads 4 total. **If you type commands live into a raw
  terminal (screen/PuTTY/minicom), it will fail** because the read races ahead of your
  keystrokes and returns garbage. Must use a terminal that sends the whole line at once
  (Arduino Serial Monitor works; a Python script with one `.write()` call works).
- Motor moves at 2 RPM (slow, ~7.5s for a quarter turn at `MTMV 512`) and **blocks** — no other
  commands processed mid-move.
- `TEST` command (`stm.test_piezo()`) drives Z, then X, then Y through 500 cycles at 1kHz each,
  audible as a buzz — genuinely useful end-to-end test of DAC->ribbon->J1->piezo with no tip/
  sample needed. Z swings -10V to +5.3V (loud), X/Y swing -3V to +1.6V (quieter, expected).
- PID gains start at **0.0, 0.0, 0.0**, not the `INIT_KP/KI/KD` defines (2.0/1.0/1.0) — those
  are only referenced in a commented-out line. Constant-current mode does nothing until `PIDS`
  is sent.
- `ADCR`/`read_adc()` returns a 5-sample rolling average, not a single reading.
- ADC chip-select polarity in `LTC2326_16.cpp` looks inverted from normal convention (CS set
  HIGH before transfer, LOW after) — flagged as possibly intentional since pin 38 is actually
  the ADC's RDL/read-enable rather than a plain CS, not "fixed" preemptively.

## Known GUI bugs (stm_control.py) — do not use GUI motor control today
1. `move_motor()` missing an f-string prefix — sends literal text `MTMV {steps}`, motor does
   nothing. Use raw serial commands instead.
2. `get_status()` exception handler references `self.history[-1]` which throws IndexError if
   history is empty (first-run crash risk).
3. `set_buffer_size()` call is Windows-only pyserial, throws AttributeError on Mac/Linux.
4. Latent bug in `start_scan()` using a stale loop variable — not relevant yet, will matter when
   scanning starts.

---

## Where today's session is RIGHT NOW

**RESOLVED. Firmware is flashed and running. Stages 1 and 2 pass.**

### The repeated button-press prompts were a host-side problem, not the board

Root cause: an **orphaned PlatformIO Home session** left over from a closed VS Code window kept
a `platformio device monitor` process alive, and that process held COM3 open. PlatformIO's
`teensy_reboot` step needs to reach the Teensy to request auto-reboot into the bootloader. With
the port locked it cannot, so the Teensy Loader falls back to its only remaining option and asks
for the PROGRAM button. Every upload, indefinitely.

Evidence: opening COM3 returned `PermissionError(13, 'Access is denied')` while the monitor was
alive, and succeeded immediately after it was killed. Two PIO Home sessions were running (ports
45425 and 45385) against a single open VS Code window.

**The firmware had actually flashed successfully on an early press.** At the time this was
diagnosed the board reported ~1000 seconds of continuous uptime from one boot, so it had been
running correctly the whole time the Loader was asking for another press.

### Avoiding it again

- **Do not use the PlatformIO serial monitor for this project.** It breaks two things at once:
  it holds the port, which causes the button loop, and it sends one keystroke at a time, which
  loses the 4-character race in `checkSerial()` described as finding 1 in the soft launch doc.
  Typing `GSTS` into it returns nothing even on a healthy board.
- If the button prompt reappears, check for a stale monitor before touching hardware:
  `Get-WmiObject Win32_Process | Where-Object { $_.CommandLine -match 'device monitor' }`
- Closing all VS Code windows clears orphaned PIO Home sessions.

### Stage 1 result: PASS

`GSTS` returns the correct ten fields with `time_millis` climbing between calls.

```
0,0,0,0,0,0,0,0,0,1001248
```

Field 5 (adc) reads 0, and `ADCR` also returns 0. **Expected at this stage, not a fault** since
the LTC2326 runs off the analog rails and the bench supply is not connected. Re-check in Stage 4.

### Stage 2 result: PASS, with one open calibration question

`MTMV 512` moved the steps field 0 -> 512, `MTMV -512` returned it to 0. Uptime advanced 11.4 s
across a move that should block for 7.5 s, so the firmware genuinely sat in `step()` for the
expected duration rather than returning instantly. Repeated twice, same result both times.

**Visually confirmed:** the four ULN2003 driver LEDs cycled in a rolling pattern, and the shaft
rotated. That rules out the two worst failure modes from the soft launch table:

| Ruled out | Why |
|---|---|
| Wires crossed, cancelling the software 1-3-2-4 mapping | That buzzes without a clean rolling LED sequence |
| Driver minus not on Teensy GND | That leaves all four LEDs dark |

So the motor path works end to end: serial -> parser -> `EfficientStepper` -> pins 33/35/34/36
-> ULN2003 -> coils -> shaft. No tip was installed for this test.

### Steps per revolution: RESOLVED, 2048 is correct

Measured with tape on the rotating part and a fixed reference. `MTMV 512` moved the mark **one
quarter turn clockwise**, so 512 / 0.25 = **2048 steps per revolution**. `STEPS_PER_REVOLUTION
2048` in `stm_firmware.hpp` is right and needs no change. Consistent with a 28BYJ-48, which is
about 2038 full steps per output revolution and normally rounded to 2048.

### Reverse direction: works, backlash negligible

Measured against the tape reference. `MTMV 512` forward gave a clean quarter turn clockwise,
`MTMV -512` **returned the tape to its original position.** Both directions drive correctly and
any backlash is below what is visible at this measurement resolution.

An earlier draft of this section recorded a large reverse-direction shortfall. That was wrong:
at the time, no reverse move had actually been watched with the tape in place, and the
impression came from the earlier unwatched runs. The measured result above supersedes it.

Practical effect: the retract-clearance concern is much smaller than first written. Still sound
practice to over-retract and to make final moves to a position from a consistent direction, but
there is no measured backlash figure that needs compensating for.

**Stage 2 is fully closed.** Serial -> parser -> `EfficientStepper` -> pins 33/35/34/36 ->
ULN2003 -> coils -> shaft, verified in both directions, with the step count calibrated.

### Stage 3 result: PASS. Both rails up.

Two independent supplies wired in series, ±18 V, 200 mA limit. Series stack verified before
connecting (A+ to junction = 18 V, junction to B− = 18 V, A+ to B− = 36 V), junction tied to
**U19 pin 2 = AGND**. Powered on with no smoke, smell or heat.

**LED5 and LED6 both lit for the first time.** Both rails confirmed present.

**Current draw: V++ = 60 mA, V-- = 36 mA.** The asymmetry is correct and expected, not a
measurement artifact: **V++ feeds three regulators (U17 -> +15 V, U16 -> 3.3 V, U22 -> 5 V) while
V-- feeds only one (U18 -> −15 V)**. All the digital rails hang off the positive leg.

### Stage 4 result: PASS. ADC works.

All four DACs parked at midscale and read back correctly (`32768,32768,32768,32768`).

**The ADC returns real, varying data:** −2393, −3005, −3520, −4287, −3982, −2340, −2856, −2545
across eight consecutive `ADCR` calls with no tip installed.

**Important false alarm, recorded so it is not repeated.** Immediately after the rails came up
the ADC read **exactly −32768 on eight consecutive calls**, with zero variation. That was
diagnosed at the time as a digital fault in the read path, and the `LTC2326_16.cpp` RDL polarity
(finding 6 of the soft launch doc) was named as the cause. **That diagnosis was wrong.**

What was actually happening: the preamp was **railed at negative saturation while still settling
after power-up**. An OPA627 with a 100 MOhm feedback resistor and a floating input (no tip) has a
very long settling time. Roughly 200 seconds later the same reading had come down to −6284 and
was drifting normally.

The reasoning that failed was "a constant reading with no noise must be digital." **At full-scale
saturation the ADC clips, which removes the noise too**, so a railed analog input produces exactly
the same pinned constant a digital fault would.

**Do not change the RDL polarity in `LTC2326_16.cpp`. It is correct as written.**

Practical lesson: **give the preamp several minutes to settle after applying rails** before
judging any ADC reading.

### THE OPERATING RULE THAT MATTERS MOST

> # ALWAYS SEND `RSET` AFTER POWERING ON THE ANALOG SUPPLY.
> # IF LED1-4 ARE LIT, THE DACs ARE DEAD. `RSET` FIXES IT.

**LED1-4 are your DAC status indicators. Dark = configured and working. Lit = dead.**
Check them before trusting any measurement.

### Root cause of "the DACs are dead": a power-ordering trap (2026-08-30)

This wasted most of two sessions. It is not a wiring fault, not a bad solder joint, and not
(mainly) the SPI clock.

**The Teensy is USB-powered and boots independently of the analog supply.**

1. Connect USB -> Teensy boots instantly -> `setup()` runs `stm.reset()`, writing DAC config
2. If the **analog supply is off at that moment**, the DACs are unpowered. Those writes go nowhere
3. You switch the supplies on. The DACs power up **unconfigured**, ALERT asserted, LED1-4 lit
4. **`setup()` never runs again.** Cycling the analog supply does NOT reboot the Teensy, because
   USB keeps it alive
5. The DACs stay dead indefinitely until something sends `RSET`

**Every symptom across all three sessions follows from this**, including the one time it appeared
to fix itself: a **reflash** reboots the Teensy *after* the analog rails are already up, so
`setup()` runs with the DACs powered and configuration succeeds.

#### Two ways to avoid it

1. **Send `RSET` after powering up the analog supply.** Simplest, always works
2. Power the analog supply on **before** connecting USB

#### Worth fixing in firmware eventually

`setup()` runs once and never re-checks. Options: re-run `stm.reset()` on a schedule, poll the
ALERT lines, or add a settling delay after `SPI.begin()`. None of it is needed as long as the
`RSET` rule is followed.

### Contributing cause: SPI clock was 40 MHz. Fixed at 1 MHz.

**All four DACs were dead because the SPI bus ran at 40 MHz across the ribbon cable.**

```cpp
// lib/AD5761/AD5761.hpp  -- BEFORE
SPISettings _spi_settings = SPISettings(40000000, MSBFIRST, SPI_MODE2);
// AFTER
SPISettings _spi_settings = SPISettings(1000000, MSBFIRST, SPI_MODE2);
```

**Confirmation was immediate and unambiguous: LED1-4 went dark.** Those are the four DACs' ALERT
pins (U1-U4 pin 1). They had been lit through every session, meaning all four chips were
asserting a fault because they never received a valid control-register write. One reflash at
1 MHz and all four went out.

#### Why continuity testing could never have found this

Two full sessions were spent on continuity, and every single test passed - bare board, populated
board, ribbon, connector matings, cables. **That was not wasted, but it could not have succeeded**,
because:

> **Continuity proves a DC path exists. It says nothing about whether a 40 MHz edge arrives with
> its timing intact.**

The path was electrically perfect and still could not carry the signal. 40 MHz across a 26-pin
ribbon, through hand-soldered bridges, into a hand-wired protoboard, is far outside what that
physical construction supports.

#### Why the ADC worked the whole time and the DACs did not

This was the clue that should have been read earlier. The two devices are on **different SPI
buses**:

| | Bus | Teensy pins | Clock | Worked? |
|---|---|---|---|---|
| **LTC2326 ADC** | **SPI1** | SCK 27, MISO 39, CS 38 | library default | **Yes, always** |
| **AD5761 DACs** | **SPI** | SCLK 13, SDI 11 | **40 MHz, set explicitly** | **No** |

`ADCR` returning real varying data proved the ribbon and the solder bridges were sound as a
construction technique. It proved nothing about the DAC lines, which are different wires, different
bridges, and critically a **different clock rate**. The user made exactly this point - that bridges
elsewhere in the build demonstrably work - and following it up is what led to the fix.

#### The reasoning that got there

By elimination. Everything shared by all four DACs was tested and found good:

| Shared resource | Verdict |
|---|---|
| VREF1 | 2.5 V exactly, measured at C54 |
| +15 V | Confirmed at U17 pad 3 and via U5 |
| −15 V | Confirmed at U18 pad 3 and at 9 capacitors across the board |
| 3.3 V | Confirmed by LED1-4 being lit through R1-R4 |
| Ribbon continuity | Every line tested Teensy pin to H1 pin |
| Firmware write command | `CMD_WR_UPDATE_DAC_REG` is correct |

Four identical chips behaving identically was never four failures. It was always one shared cause,
and once every static shared resource was eliminated, the only thing left was the one property
continuity cannot measure: **signal integrity at speed.**

#### Note for later

1 MHz is conservative and there is no reason to raise it. Scan speed is limited by the mechanics
and the PID loop, not by DAC update rate. **If you ever do raise it, raise it gradually and re-test**,
because the failure mode is silent - the DACs simply stop accepting writes with no error anywhere.

1 MHz is also slow enough for the FNIRSI DST-201's 1 MHz scope to observe, should the bus ever need
looking at again.

### Stage 5: PASS (2026-08-30). All three axes verified with a meter.

Measured at the **scan head end of the DSUB1 cable**, so this proves the whole chain: SPI -> DAC
-> U9/U10 -> R6/R9/R14/R19 -> DSUB1 -> connector -> cable -> piezo.

Wire colours on the DSUB1 cable: **Black-Yellow (pins 1-5) = AGND. Green = Z−Y, Blue = Z+Y,
Grey = Z−X, White = Z+X.**

| Commanded | White (Z+X) | Grey (Z−X) | Blue (Z+Y) | Green (Z−Y) |
|---|---|---|---|---|
| **Z = 65535** | −10 V | −10 V | −10 V | −10 V |
| **X = 65535** | −3 V | +3 V | 0 | 0 |
| **Y = 65535** | 0 | 0 | −3 V | +3 V |

Every value matches the schematic prediction. U9/U10 are inverting summing amps with R5=R7=R8=3k,
so **gain is exactly −1** and a positive command gives a negative output.

**This also empirically confirms the ±3 V range finding.** Z reads ±10 V (range bits `000`) while
X and Y read ±3 V (range bits `101`). The firmware comments claiming ±5 V for X and Y are wrong,
and there are now measurements proving it, not just a datasheet reading.

#### Do not use sound as a test on this piezo

The disc is an **18 mm buzzer element with a resonant frequency of 8.6 kHz**. `test_piezo()` drives
it at **1 kHz**, roughly one eighth of resonance, where it barely moves air. Audible response is
therefore weak and unreliable regardless of whether everything works. Considerable time was lost
treating ears as the instrument. **Use a meter.**

(Disc spec: 18 mm copper/brass, 1.5-30 V, resonance 8.6 ± 0.7 kHz, capacitance 15 nF ± 30%. The
15 nF is the capacitive load the output op-amps drive - irrelevant at 1 kHz, worth remembering at
scan rates.)

### Preamp power: ALL GOOD. Verified 2026-08-30.

Chased at length on a false premise. Final state, all measured **against controller-board ground**:

| Point | Reading |
|---|---|
| IC1 pin 7 (op-amp V+) | **+15 V** correct |
| IC1 pin 4 (op-amp V−) | **−15 V** correct |
| A JP1 ground pin | **0.000 V solid** - ground is connected |

**Polarity is correct at the chip and ground is present.** Earlier readings suggesting otherwise
were taken with JP1 pin 1 as the reference, and **JP1's pin numbering in the older notes is
mirrored relative to how it was being counted.** Every measurement referenced to a JP1 pin was
therefore unreliable.

> **LESSON, worth more than any single finding here: when readings drift and do not make sense,
> verify your ground reference before anything else.** Multiple hours across two sessions were
> spent measuring against a node that was not ground.

### Stage 6: THE REMAINING FAULT. Preamp feedback loop appears open.

Measured at IC1 (OPA627) against controller ground:

| Pin | Function | Reading | Should be |
|---|---|---|---|
| **3** | +IN | **0 V** | 0 V ✅ |
| **2** | **−IN** | **constant 1.4 V** | **0 V, matching pin 3** ❌ |
| 6 | OUT | floating / railed ~11.9 V earlier | near 0 V ❌ |

**Pin 2 sitting 1.4 V away from pin 3 is the diagnosis.** In a working transimpedance amplifier the
feedback loop forces the inverting input to virtual ground, essentially equal to the non-inverting
input. A 1.4 V difference means **the loop is not closed.**

This is not explained by the tip being absent. Input bias current on an OPA627 is a few picoamps,
which through 100 MOhm is a fraction of a millivolt, and the feedback resistor remains connected
whether or not a tip is fitted.

#### Where to look next session

The input node is **deliberately air-wired on a PTFE standoff** with zero copper, to avoid leakage
at picoamp levels. Three things meet there:

1. the **100 MOhm feedback resistor**
2. the **tip coax centre conductor**
3. a **link wire to IC1 pin 2**

Any one of those coming adrift opens the loop, and that construction is fragile by design. After
the handling this build has had, a lifted connection there is the leading candidate.

**Check, in order:**
- Visual inspection of the standoff under magnification. Look for a lifted or broken wire
- Continuity from IC1 pin 2 to the standoff junction
- The 100 MOhm resistor itself. Note the DST-201 may not read 100 MOhm - if it reads open, that
  may be a range limit rather than a failed part, so do not condemn it on that alone
- Confirm PAD1 is **not** being used as the input. It is the op-amp **output**, downstream of R1.
  This was a repeated point of confusion in earlier sessions

### Stage 5 first attempt: FAIL (before the SPI fix)

`TEST` produced no audible buzz on any axis. Follow-up measurements with a meter, scan head
unplugged from J1, Z commanded to both extremes:

| Z commanded | J1 row-of-4 (Z signals) |
|---|---|
| 65535 (+10 V) | ~0 V |
| 0 (−10 V) | ~0 V |

The output stage is dead in both directions.

#### Confirmed WORKING (do not re-test these)

| Item | Evidence |
|---|---|
| **VREF1 = exactly 2.5 V** | Measured across C54. All four DACs share it |
| **+15 V rail** | JP1 pin 2 = +15 V. Also proven by U5 producing VREF1 from it |
| **3.3 V rail** | LED1-4 are lit through R1-R4 off that rail |
| **V++ / V-- inputs** | LED5 and LED6 both lit |
| **U18, the −15 V regulator** | **pad 2 = −18 V in, pad 3 = −15 V out. U18 IS WORKING.** |
| DAC write path in firmware | `set_dac_z()` uses `CMD_WR_UPDATE_DAC_REG`, which is correct |

#### Confirmed BROKEN

| Symptom | Detail |
|---|---|
| **−15 V absent at the preamp** | JP1 pin 5 sits at a **positive**, floating voltage. It decayed 23 V -> 7 V while the meter loaded it, then **recovered to 8.3 V** when released. That is a floating node, not a supply |
| **No DAC output** | J1 dead at both Z extremes |
| **All four DACs asserting ALERT** | LED1-4 still lit under full, correct power |

#### Why the floating node reads POSITIVE

With nothing driving the −15 V net at that point, every chip on it (U1-U4 pad 6, U9/U10 pad 4,
U13 pad 4, U21 pad 4) still has a healthy +15 V on its other supply pin. They leak internally
from positive supply into the floating negative pin and **drag it upward**. A meter that can pull
a "rail" down and have it creep back is measuring capacitance, not a supply.

**This is out of spec for those chips** - V− above ground while V+ is at +15 V. Do not leave the
board powered in this state longer than a measurement requires.

#### The live hypothesis for tomorrow: a BREAK IN THE −15 V NET

U18 **generates** −15 V correctly, but it is **absent at the preamp end**. So the rail is not
reaching everything it should. The single most economical explanation is a break in the −15 V
distribution downstream of U18, which would simultaneously explain:

- the preamp having no −15 V (via DSUB2 pad 4 and the J2 cable)
- the DACs not outputting (U1-U4 all need −15 V on pad 6)
- all four DACs asserting ALERT (a shared supply fault, not four chip failures)

One break, every symptom. The alternative is two independent faults (a bad J2 cable *and*
something separate killing the DACs), which is less likely.

#### THE decisive test to run first tomorrow

**Measure −15 V at points progressively further from U18.** Every one of these capacitors is on
the −15 V net and they are easy probe points:

```
C1.1  C2.1  C7.1  C8.1  C13.1  C14.1  C19.1  C20.1
C34.1  C44.1  C45.1  C47.1  C62.2
```

Also check **U9 pad 4** and **U3 pad 6** (a DAC's negative supply pin) directly.

| Finding | Meaning |
|---|---|
| −15 V at U18 pad 3 but **floating positive** at the caps and at U3 pad 6 | **Break in the −15 V net on the board.** Trace it from U18 outward. One fault, explains everything |
| **−15 V present** at U3 pad 6 and U9 pad 4 | The DACs have their rail. The −15 V hypothesis is dead for the DAC problem, and we have **two separate issues**: a broken J2 cable −15 V conductor, and something else killing the DAC output. Next suspect then becomes the SPI bus |

### Regulator and part reference, from the schematic

| Ref | Part | Package | Function | LCSC |
|---|---|---|---|---|
| U17 | **SL7815** | TO-220 | V++ -> +15 V | C458979 |
| U18 | **L7915CV** (ST) | TO-220 | V-- -> −15 V | C154950 |
| U16 | **BD733L5FP-CE2** (ROHM) | TO-252 | V++ -> 3.3 V | C509724 |
| U22 | **MC7805CDTG** (onsemi) | DPAK | V++ -> 5 V | C897464 |
| U19 | B3B-XH-AM | JST XH 3-pin | Power input | - |
| U9, U10 | dual op-amp, 8 MHz GBP, 2.3 V/us, ±2.5 to 18 V | - | X/Y/Z output stages | - |

### TEST leaves the DACs at zero scale

`test_piezo()` ends each axis on `set_dac_*(00000)` and never restores midscale. `GSTS` straight
after a TEST read `32768,0,0,0,...`, so **Z was left at −10 V and X and Y at −3 V**. This silently
recreates the power-on hazard mid-session. Always re-park with `DACZ 32768` / `DACX 32768` /
`DACY 32768` after any TEST. Written up in the Stage 5 section of the soft launch doc.

**It does not affect `APRH`.** The approach loop only ever calls `move_motor(step_interval)` in
one direction and never reverses:

```cpp
if (stepper_motor.get_total_steps() < approach_config.max_steps)
{
    move_motor(approach_config.step_interval);
    ...
}
```

So backlash is taken up once at the start and does not accumulate during an approach.

**Where it does bite, and this one matters:** a **retract moves less than commanded**, because
the direction reversal eats some of the travel before the output shaft moves at all. The `steps`
counter still counts every commanded step regardless.

That means after a retract you have **less clearance than the step count implies**, which is the
dangerous direction. Retracting 200 steps and assuming 200 steps of clearance, then approaching
200 steps, moves the tip further toward the sample than it started.

Two rules that follow:

1. **Over-retract.** Treat a retract as delivering less than commanded, never more.
2. **Always make the final move to any position from the same direction.** Standard machinist
   practice for backlash, and it applies directly here.

Worth measuring the backlash figure before serious approach work: `MTMV 512` one way, `MTMV -512`
back, and the angular shortfall from the original mark converts as
`backlash_steps = (shortfall_degrees / 360) x 2048`.

### New tool: `Code/pc/stm_console.py`

Replaces the PlatformIO monitor. Sends each command as a single `write()` so the 4-character race
cannot happen, auto-detects the Teensy by USB VID 0x16C0, and in one-shot mode opens and closes
the port per command so it can never block an upload.

```
python stm_console.py GSTS
python stm_console.py MTMV 512
python stm_console.py            # interactive, 'free' releases the port
```

It decodes `GSTS` using the corrected ranges (X/Y +/-3 V, Z +/-10 V), knows which commands reply
and which are silent, and waits out blocking commands instead of racing them.

### New finding before Stage 3: see `DAC_BOOT_STATE.md`

`AD5761::reset()` configures the control register but **never writes a DAC data register**, so
outputs sit at their power-up default. The instantiated mode words have bits D5 and D3 clear
where `AD5761.hpp`'s own documented examples set them. Two consequences:

1. **Z sits at −10 V the moment analog power is applied**, not 0 V. The tip clearance precaution
   currently written for Stage 5 needs to apply from **Stage 3 power-on** instead.
2. D5 appears to be the internal reference enable and is off. If `TEST` is silent on all three
   axes, investigate the reference before suspecting the piezo. Silent on one axis only is
   wiring, not this.

---

## The staged test plan for today (once firmware is confirmed running)

Full detail is in the `soft_launch_test_procedure.md` file already produced — summary:

- **Stage 0:** continuity re-check (yellow->IC1 pin7 beeps, orange->IC1 pin4 beeps, yellow-
  orange silent) — already done in an earlier session
- **Stage 1:** USB only, `GSTS`, expect a 10-field CSV status line
- **Stage 2:** USB only, `MTMV 512` via serial (not GUI), motor should turn ~7.5s for a quarter
  turn, LEDs chase
- **Stage 3:** bring up analog supply (+/-18V into U19), watch/smell for problems, low current
  limit recommended
- **Stage 4:** `BIAS 33000` + `GSTS` readback, `ADCR` sanity check
- **Stage 5:** `TEST` command — should audibly buzz Z/X/Y in turn, best available end-to-end
  piezo wiring check
- **Stage 6:** preamp output DC check with tip disconnected, should sit near 0V and stable

Explicitly NOT attempted today: `APRH` (approach), `SCST` (scan), `CCON` (constant current) —
all assume a tip safely positioned, which hasn't happened yet.

---

## Style/communication preferences established in this project

- No em-dashes in written docs
- Plain, direct language; avoid corporate/AI-sounding phrasing
- Every technical claim should be traced to a real source (Gerber file, firmware source,
  photo) — flag clearly when something is inference vs. verified fact
- User wants brevity and directness; dislikes padding
- Prefers structured comparisons/tables over prose when presenting options

---
---

# APPENDIX A: COMPLETE SESSION RECORD, 2026-08-29 and 2026-08-30

Exhaustive knowledge transfer covering two full bring-up sessions. Written so that someone
(human or AI) with no access to the original conversation can continue the work without loss of
context. Includes every finding, every wrong turn, and the reasoning behind both.

**Read sections 5 (false trails) and 7 (operating rules) before touching the hardware.** More time
was lost to the items in those two sections than to any real fault.

---

## A.0 STATE AT A GLANCE

| Stage | Status | Notes |
|---|---|---|
| 0 - Continuity | PASS | Done in an earlier session, re-confirmed indirectly |
| 1 - `GSTS` | **PASS** | Ten fields, `time_millis` climbing |
| 2 - Motor | **PASS** | Both directions, 2048 steps/rev measured, backlash negligible |
| 3 - Analog rails | **PASS** | LED5 + LED6 lit, 60 mA / 37 mA |
| 4 - DACs and ADC | **PASS** | Readback correct, ADC returns real varying data |
| 5 - Piezo drive | **PASS** | All three axes measured at the scan head end. Re-confirmed 2026-08-31 |
| **Bias to sample holder** | **PASS** | **NEW 2026-08-31.** -3 V measured for +3 V commanded, inverts |
| 6 - Preamp | **FAIL** | ~~Feedback loop open~~ **SUPERSEDED. Loop is CLOSED.** 37 nA input leakage from CA contamination. Rebuilding. See `SESSION_2026-08-31_RESULTS.md` s3.1 |
| **DAC config stability** | **FAIL** | **NEW FAULT 2026-08-31.** All four drop config ~hourly. Invisible to software |
| **JP1 grounds** | **FAIL** | **NEW 2026-08-31.** One ground pin genuinely open. A.5.8's retraction was wrong |

**Two faults were found and fixed. One remains.**

| Fault | Status |
|---|---|
| Repeated "press PROGRAM button" prompts | **FIXED** - orphaned serial monitor held COM3 |
| All four DACs dead | **FIXED** - two causes, see A.3.12 and A.3.20 |
| Preamp feedback loop open | **OPEN** - the only remaining fault |

---

## A.1 SESSION 1 (2026-08-29): CHRONOLOGICAL RECORD

### A.1.1 Starting situation

The user opened by asking for help with a Teensy upload that had requested the PROGRAM button
**four times**. The prior handoff had recorded three presses and speculated the Loader UI was
confused. Nothing had been confirmed running.

### A.1.2 Diagnosis of the button-press loop

Steps taken:

1. Enumerated serial ports: **COM3 present**.
2. Enumerated USB devices: `USB\VID_16C0&PID_0483&MI_00` and `&MI_02`, Status OK.
   - **VID_16C0 = PJRC.** **PID_0483 = running sketch.** PID_0478 would be HalfKay bootloader.
   - So the board was **not** sitting in the bootloader waiting for anything.
3. Attempted to open COM3 from Python: **`PermissionError(13, 'Access is denied.')`**
4. Enumerated processes. Found:
   - `platformio.exe` (pid 39268)
   - **two `platformio device monitor` processes (pids 23944, 56076)**
   - `teensy.exe` (pid 6104), the Teensy Loader GUI
   - **two PlatformIO Home sessions** on ports 45425 and 45385 with different session IDs,
     against a **single** open VS Code window
5. Killed the two monitor processes. COM3 opened immediately afterwards.

**Root cause:** a PlatformIO Home session orphaned from a previously closed VS Code window kept a
`device monitor` alive, holding COM3. PlatformIO's `teensy_reboot` step needs to reach the Teensy
to request auto-reboot into the bootloader; with the port locked it cannot, so the Teensy Loader
falls back to asking for the PROGRAM button. Every upload, indefinitely.

**Verification later in session 2:** after the monitor was gone, an upload completed with **zero
button presses**. Diagnosis confirmed.

### A.1.3 Firmware confirmed running

`GSTS` returned `0,0,0,0,0,0,0,0,0,583282` and repeated calls showed `time_millis` climbing.
Uptime was ~583 seconds from a single boot, meaning **the firmware had flashed successfully on an
early button press and had been running correctly the whole time** the Loader was asking for more
presses.

### A.1.4 `stm_console.py` created

Written to `Code/pc/stm_console.py`. Rationale: the PlatformIO serial monitor is wrong for this
project in **two independent ways**:

1. It **holds the port**, which causes the button-press loop.
2. It **sends one keystroke at a time**, which loses the 4-character race in `checkSerial()`
   (finding 1 of the soft launch doc). Typing `GSTS` into it returns nothing even on a healthy
   board.

Design decisions in the tool:

- Every command goes out as a **single `write()`** so the 4-char race cannot occur.
- **One-shot mode opens and closes the port per command**, so it can never block an upload.
- Auto-detects the Teensy by **USB VID 0x16C0**.
- Knows which commands reply (`GSTS`, `ADCR`, `IVGE`) and which are silent, so it does not wait
  on a reply that will never come.
- Knows which commands **block** the firmware and waits them out. `MTMV` duration is computed
  from the step count at 2 RPM (68.27 steps/s); `TEST` is 3.5 s.
- Appends a newline **only when there is an argument**. `Serial.parseInt()` consumes the
  terminating non-digit, so a trailing newline is eaten cleanly; on a no-argument command
  parseInt is never called and a stray newline would corrupt the next command.
- Decodes `GSTS` using the **corrected** DAC ranges (X/Y ±3 V, Z ±10 V).
- Prints a warning when all four DAC fields read 0, because those are `STMStatus` boot
  placeholders and not a readback from the chips.

Usage:
```
python stm_console.py GSTS
python stm_console.py MTMV 512
python stm_console.py DACZ 65535
python stm_console.py GSTS -n 8        # repeat
python stm_console.py                   # interactive; 'free' releases the port
```

### A.1.5 `DAC_BOOT_STATE.md` created

Two findings, from reading `AD5761.cpp` and `stm_firmware.hpp`:

**Finding 1 (stands):** `AD5761::reset()` performs only:
```cpp
write(CMD_SW_FULL_RESET, 0);
delay(100);
write(CMD_WR_CTRL_REG, _mode);
```
**It never writes a DAC data register.** So outputs sit at the AD5761's power-up default. The
mode words instantiated have bits D5 and D3 **clear**, where `AD5761.hpp`'s own documented
examples (`0b0000000101000`, `0b0000000101101`) set them.

Reading the control register map: D10:D9 = CV (clear voltage), D5 = IRO (internal reference),
D4:D3 = PV (power-up voltage), D2:D0 = RA (range). With PV = 00 and CV = 00 both selecting zero
scale, **Z sits at -10 V the instant the analog rails come up**, before any command.

Consequence: the tip-clearance precaution, originally written for Stage 5, was **moved to Stage 3**
in `soft_launch_test_procedure.md`.

**Finding 2 (RETRACTED, see A.5.1):** IRO = 0 was flagged as a possible cause of dead DACs. This
was later disproved.

### A.1.6 Stage 2, motor

`MTMV 512` moved `steps` 0 -> 512; `MTMV -512` returned it to 0. Uptime advanced 11.4 s across a
move that should block for 7.5 s, confirming the firmware genuinely sat in `step()`.

**User confirmed no tip was installed** and it never had been. This remained true for both
sessions.

Visual confirmation: **the four ULN2003 driver LEDs cycled in a rolling pattern and the shaft
turned.** That rules out the two worst failure modes from the soft launch table (crossed wires
would buzz without a clean sequence; a missing driver ground would leave all four LEDs dark).

**Calibration:** tape was placed on a rotating part with a fixed reference. `MTMV 512` moved the
mark **one quarter turn clockwise**, so 512 / 0.25 = **2048 steps per revolution**.
`STEPS_PER_REVOLUTION 2048` is correct. Consistent with a 28BYJ-48 (~2038, rounded to 2048).

**Backlash:** `MTMV -512` **returned the tape to its original position**, so backlash is below
visible resolution. An earlier draft of the handoff recorded a large reverse shortfall; that was
written before any reverse move had actually been observed with the tape in place and was
**retracted**.

Method notes worth keeping: measure in **one direction only** to avoid backlash contaminating the
result; photograph from the same position to avoid parallax; and the precision needed is low
because the question is 2048 vs 1024 vs 4096 (factor-of-two errors), not 2038 vs 2048.

### A.1.7 The main-PCB LED investigation

User reported: motor driver and Teensy LEDs on; **main PCB LED1-5 on, LED6 off**.

All six LEDs were traced from `PCB/STMP_easyEDA.zip` (PAD_NET records). See A.4.4 for the final
table. Initial claim that LED1-4 were **SYNC** indicators was **wrong and corrected** (see A.5.2):
they connect to U1-U4 **pin 1 (ALERT)**, fed from the 3.3 V rail through R1-R4.

An alarm was raised that LED5-on/LED6-off meant V-- was missing. The user then clarified the
bench supply was **switched off**, which invalidated the alarm (see A.5.3).

### A.1.8 Phantom powering, explained and confirmed

With the supply off but USB connected, LED1-5 lit and LED6 dark. Mechanism:

1. The Teensy drives SCLK (H1 pin 12), SDI (pin 14) and SYNC1-4 into U1-U4 at 3.3 V.
2. Those digital inputs have **ESD clamp diodes to their digital supply, pad 15, which is the
   board's 3.3V net**. With that rail at 0 V the clamps forward-bias and pull the entire 3.3V net
   up to roughly **3.3 - 0.6 = 2.7 V**.
3. That phantom 2.7 V feeds R1-R4, so **LED1-4 glow**.
4. It also reaches U16's **output** pin; current flows backward through U16 to its input, raising
   **V++ to about 2.1 V**, lighting **LED5** through R27.
5. **Nothing can phantom-generate a negative rail.** Backfeed only pushes positive, so V-- stays
   at 0 and **LED6 stays dark**.

**Confirmed by test.** With the supply off, USB was unplugged: **LED1-5 all went dark.**
Reconnecting USB brought them straight back on, steady, no flashing.

**Corroborating detail:** with the supply leads connected but the supply off, LED5 was visibly
**dimmer** than LED1-4; unplugging the leads made it jump to full brightness. The switched-off
supply was loading V++ and draining the phantom voltage.

**Side benefit:** uptime went 1700 s -> 53 s and `steps` reset to 0, proving the firmware survived
a full cold boot and is genuinely in flash, not a RAM image.

### A.1.9 Teensy pin 13 gotcha discovered

**Teensy pin 13 is SCLK and also the onboard LED.** Ribbon pin 12 carries SCLK to T13, which is
the Teensy 4.1's built-in LED pin. **That LED is an SCLK-activity indicator, not a health
indicator.** It dims when the net is loaded. Do not read board health into it.

### A.1.10 Metering with USB connected: a mistake and its correction

The user was advised to do a resistance check on V++/AGND but **was not told to unplug USB first**.
While probing, the Teensy's onboard LED began dimming and flickering.

**Cause:** with USB connected the board is phantom-powered, so (a) it is not at 0 V and every
resistance reading is invalid, and (b) the meter creates a drain path whose current flows through
the Teensy's ESD clamp diodes, loading its 3.3 V regulator.

**No damage resulted** (uptime stayed continuous at ~1937 s, so the Teensy never even browned
out). **Rule added: unplug USB before any resistance measurement on this board.**

### A.1.11 Stage 3, analog bring-up

Two independent supplies wired in series. The series requirement was explained explicitly: supply
A negative ties to supply B positive, and **that junction is AGND and goes to U19 pin 2 (the
middle pin)**. Without it there is no defined midpoint, and the analog return current would try to
flow through the ribbon's thin ground wires and out through the USB cable, which can damage the
ribbon, the Teensy, or the USB port.

User verified before connecting: A+ to junction = 18 V, junction to B- = 18 V, A+ to B- = 36 V.

Powered on at ±18 V with a 200 mA limit. **No smoke, smell or heat. LED5 and LED6 both lit for the
first time.**

**Current draw: V++ = 60 mA, V-- = 36 mA.** The asymmetry is correct and expected, not a
measurement artifact: **V++ feeds three regulators (U17 -> +15 V, U16 -> 3.3 V, U22 -> 5 V) while
V-- feeds only one (U18 -> -15 V)**. All digital rails hang off the positive leg.

### A.1.12 Stage 4, DACs and ADC

All four DACs parked at midscale; `GSTS` read back `32768,32768,32768,32768`.

ADC went from 0 to **-32768** and stayed there across eight `ADCR` calls with zero variation.

**This was misdiagnosed** as a digital fault in the read path, with `LTC2326_16.cpp`'s RDL
polarity named as the cause. **That diagnosis was wrong** (see A.5.4). The preamp was railed at
negative saturation while still settling after power-up; roughly 200 seconds later the same
reading had come down to -6284 and was drifting normally. Later `ADCR` calls returned genuinely
varying values (-2393, -3005, -3520, -4287, -3982, -2340, -2856, -2545).

**Do not change the RDL polarity in `LTC2326_16.cpp`. It is correct as written.**

### A.1.13 `TEST` leaves the DACs at zero scale

Discovered by readback. `test_piezo()` ends each axis on `set_dac_*(00000)` and nothing restores
midscale. `GSTS` straight after a TEST read `32768,0,0,0,...`: bias still parked but **Z at -10 V
and X and Y at -3 V**. This silently recreates the power-on hazard mid-session.

Documented in the Stage 5 section of `soft_launch_test_procedure.md`. Always re-park with
`DACZ 32768` / `DACX 32768` / `DACY 32768` after any `TEST`.

### A.1.14 Stage 5 first attempt: no audible piezo output

User heard nothing. Investigation moved to DC measurement. The signal chain was traced from the
PCB file:

```
U3 (DAC Z) --ZOUT--> R8 --> U9 pin 6 (inv input) --> U9 pin 7 (out) --> R6 --> DSUB1 pin 9 (Z+X)
```

Component values extracted from the schematic: **R5 = R7 = R8 = 3 k, R6 = 220 R**. U9 channel B is
an **inverting summing amplifier** with its non-inverting input (pin 5) tied to AGND, so
**gain is exactly -1 per input** and a positive command produces a negative output. R6 at 220 R is
negligible against a 10 MOhm meter, so no divider effect.

Measurements at DSUB1 read approximately 0 V at both Z extremes.

Two measurement errors occurred during this phase:
- The first attempt measured **the piezo/cable side** of the unplugged connector rather than the
  board side.
- Later attempts on the board still read zero. **This turned out to be correct**: the DACs were
  unconfigured at the time (see A.3.20), so there genuinely was no output.

### A.1.15 The -15 V hypothesis and its collapse

Reasoning: U9 needs -15 V on pad 4 and **U3 (the DAC) needs -15 V on pad 6**, but U5 (the
reference) needs only +15 V (pad 2). So a missing -15 V rail would explain VREF1 being fine while
every DAC output was dead, and would explain LED6 being lit (LED6 shows **V--**, the raw input;
U18 makes -15 V from it and can fail independently).

User measured U18: **pad 2 = -18 V in, pad 3 = -15 V out.** U18 is **working**.

The user's message "we got values as expect" was **misread as confirming the failure prediction**
rather than confirming health, leading to a premature "U18 has failed" conclusion that was
**retracted** (see A.5.5).

---

## A.2 SESSION 1 ARTIFACTS

Files created or modified in session 1:

| File | Action |
|---|---|
| `Code/pc/stm_console.py` | **Created.** Serial tool, see A.1.4 |
| `Code/teensy/DAC_BOOT_STATE.md` | **Created.** DAC power-up state, VREF1 resolution |
| `Code/teensy/PROJECT_HANDOFF_SUMMARY.md` | Updated throughout |
| `Code/teensy/soft_launch_test_procedure.md` | Stage 3 rewritten (tip-out moved earlier, LED5/LED6 check added, DAC parking added); Stage 5 TEST re-park warning added |

Processes killed: PlatformIO `device monitor` pids 23944 and 56076; Teensy Loader GUI pid 6104
(stale dialog).

---

## A.3 SESSION 2 (2026-08-30): CHRONOLOGICAL RECORD

### A.3.1 Meter identified

User's meter is a **FNIRSI DST-201**. Looked up: 3-in-1 handheld **multimeter + oscilloscope +
signal generator**. 19999-count TRMS. Oscilloscope: **1 MHz analog bandwidth, 5 MSa/s**, ±400 V
protection. Signal generator: 13 waveforms, 0-10 kHz, 0.1-3.0 V. Multimeter functions include
AC/DC voltage, AC/DC current, resistance, capacitance, **diode/continuity**, frequency,
**temperature**, data hold. 2.8" TFT, USB-C powered, 3000 mAh.

Sources:
- https://www.fnirsi.com/products/dst-210-dst-201
- https://manuals.plus/m/63b175d51a35308d6658adb396cca5e043901a447ca5cd89162f2eb35f93623b

### A.3.2 `FIND_THE_15V_BREAK.md` created

A bench procedure to locate a break in the -15 V distribution by walking outward from U18. Method:
anchor the black probe on U18 pad 3, then test continuity to each -15 V capacitor in order of
increasing distance. The break is between the last good point and the first bad one.

The capacitor ordering (distance from U18) was derived from component coordinates in the PCB file:

| Order | Cap | From U18 | Adjacent to |
|---|---|---|---|
| 1 | C62 | 6 mm | U18 |
| 2 | C47 | 43 mm | DSUB2 |
| 3 | C20 | 47 mm | U4 |
| 4 | C19 | 48 mm | U4 |
| 5 | C34 | 54 mm | U13 |
| 6 | C8 | 59 mm | U2 |
| 7 | C7 | 60 mm | U2 |
| 8 | C45 | 73 mm | U10 |
| 9 | C14 | 73 mm | U3 |
| 10 | C13 | 74 mm | U3 |
| 11 | C2 | 89 mm | U1 |
| 12 | C1 | 90 mm | U1 |
| 13 | C44 | 92 mm | U9 |

**Result: all nine tested capacitors were good.** The -15 V rail is intact across the entire
board, including immediately adjacent to every DAC. This killed the -15 V hypothesis for the DAC
fault.

### A.3.3 Connector naming resolved

User asked what J1, J2, JP1 and JP2 are. Investigation of the PCB file showed the only designator
prefixes present are `C`, `DSUB`, `H`, `LED`, `R`, `U`. **There is no `J` or `JP` silkscreen on the
controller board at all.** See A.4.2 for the full mapping. This had caused several wasted
measurements.

### A.3.4 Cable colour code obtained

User supplied the product listing for the cables used on both DSUB connectors: **JUXINICE DB9
male to bare wire, 3 ft**, with the manufacturer's standard core colour mapping. See A.4.5.

**Cross-check:** the Stage 0 continuity results from an earlier session (yellow -> IC1 pin 7 beeps,
orange -> IC1 pin 4 beeps, yellow -> orange silent) match the colour table exactly, since on an
8-pin op-amp pin 7 = V+ and pin 4 = V-. Two independent sources agree.

### A.3.5 Preamp board files are NOT in this repo

Confirmed by search. `PCB/` contains only the controller board (Altium zip, PDF zip, EasyEDA zip
for "Scanning Tunneling Microscope" / STMP). **Dan Berard's preamp design is not present.** The
JP1 pinout in the older notes came from Gerbers and a silkscreen photo held in an earlier session.
This means JP1 pin numbering **cannot be verified from the repo** and proved unreliable (see
A.5.8).

### A.3.6 Cable continuity: all good

User tested and all passed:
- yellow -> JP1 pin 2 (beep)
- green -> JP1 pin 4 (beep)
- orange -> JP1 pin 5 (beep)
- DB9 pin 5 -> yellow (beep)
- DB9 pin 4 -> orange (beep)
- On the board's DSUB2, only pin 4 has continuity to U18 pad 3 (correct: only pin 4 should)

### A.3.7 Spare bare PCB used as a reference

User tested an unpopulated spare board and found only DSUB2 pin 4 has continuity to the U18 pad 3
location. This confirmed (a) the PCB routing is correct by design, (b) it matches the netlist
analysis being used, and (c) the populated board's copper matches the bare board.

**Good technique, worth reusing.**

### A.3.8 A false alarm about current draw

User reported "0.037A and 0,6amps". This was read as 0.6 A, a 10x increase over the previous
60 mA, and an urgent power-down was recommended on the basis that ~11 W was being dissipated
somewhere. **The user had meant 0.06 A.** Current draw was unchanged and healthy. Alarm withdrawn.

### A.3.9 Rails confirmed at source

U17 pad 3 = +15 V, U18 pad 3 = -15 V, measured with the preamp connected. Both regulators working.

### A.3.10 The user's key objection

When solder bridges were blamed for an open connection, the user pushed back:

> "wait wait we have solder bridges all in this settup including the ribbon cable which we already
> know works"

**This objection was correct and it led directly to the breakthrough.** Following it up revealed
that "the ribbon works" is a much narrower claim than it appears.

### A.3.11 The ADC/DAC bus distinction

The two devices are on **completely different SPI buses**:

| | Bus | Teensy pins | Clock | Proven working? |
|---|---|---|---|---|
| **LTC2326 ADC** | **SPI1** | SCK 27, MISO 39, CS 38, plus CNV 19 and BUSY 18 | library default | **Yes** - `ADCR` returns real varying data |
| **AD5761 DACs** | **SPI** | SCLK 13, SDI 11, SYNC on 7/8/9/10 | **40 MHz, set explicitly** | **No** |

`ADCR` working proved the ribbon and solder bridges were sound **as a construction technique**. It
proved nothing about the DAC lines, which are different wires, different bridges, and critically a
**40x faster clock**. And `GSTS` working proves nothing about either, since that is just USB.

### A.3.12 SPI clock reduced from 40 MHz to 1 MHz

```cpp
// lib/AD5761/AD5761.hpp
// BEFORE
SPISettings _spi_settings = SPISettings(40000000, MSBFIRST, SPI_MODE2);
// AFTER
SPISettings _spi_settings = SPISettings(1000000, MSBFIRST, SPI_MODE2);
```

Rationale: 40 MHz across a 26-pin ribbon, through hand-soldered bridges, into a hand-wired
protoboard, is far outside what that physical construction supports. **Continuity proves a DC path
exists; it says nothing about whether a 40 MHz edge arrives with its timing intact.** Two sessions
of continuity testing all passed and could never have found this.

1 MHz is also slow enough for the DST-201's 1 MHz scope to observe.

**Result: LED1-4 went dark for the first time in the project.** All four DACs accepted their
control-register writes.

**Do not raise the clock back.** Scan speed is limited by mechanics and the PID loop, not DAC
update rate. If ever raised, do it gradually and retest, because **the failure mode is silent** -
the DACs simply stop accepting writes with no error anywhere.

### A.3.13 Upload behaviour confirmed fixed

The first upload attempt failed with "No Teensy boards were found" because **USB had been unplugged
for continuity testing and not reconnected**. Once reconnected, the upload completed **with no
button press at all**, confirming the session 1 diagnosis of the button-press loop.

### A.3.14 Piezo specification obtained

User supplied the disc spec: **18 mm copper/brass buzzer element, 1.5-30 V, resonant frequency
8.6 ± 0.7 kHz, capacitance 15,000 pF ± 30% (15 nF), -20 to +70 C.**

**This is important. `test_piezo()` drives at 1 kHz, roughly one eighth of resonance, where the
disc barely moves air.** Audible response is therefore weak and unreliable regardless of whether
everything works. Considerable time in both sessions was lost treating ears as the instrument.

The 15 nF is also the capacitive load the output op-amps drive: irrelevant at 1 kHz, worth
remembering at scan rates.

### A.3.15 A video was supplied that could not be used

User referenced `Code/teensy/IMG_7846.mov` (23 MB). **Video cannot be processed**, and no ffmpeg
was available to extract a frame. A still image would have been usable. The file remains in the
repo.

### A.3.16 The RSET flex test

To hunt a suspected intermittent joint, `RSET` was sent every 2 s for 90 s (45 total) while the
user pressed and wiggled the ribbon connector at both ends, the individual solder bridges, and the
cable.

**Result: the LEDs flickered in a repetitive pattern, untouched. Poking did nothing.**

**Interpretation: the flicker was the RSET loop itself, not a fault.** Each `RSET` runs
`AD5761::reset()`, which does a software full reset (ALERT asserts, LED on) then writes the
control register (ALERT clears, LED off). So every `RSET` blinks the LEDs on for ~100 ms. The
"repetitive pattern" was the 2-second interval.

**This killed the intermittent-solder-joint theory** and simultaneously proved the configuration
writes were landing.

The user also heard **clicking** during this loop. That is the piezo responding to DAC output
steps, since `stm.reset()` drops all four DACs to zero scale, which is a large voltage jump. This
confirmed the piezo genuinely moves when the DACs are configured.

### A.3.17 The DSUB1 measurement contradiction resolved

Once the DACs were confirmed configured (LED1-4 dark), DSUB1 was measured again and read
**-10 V on all four signal pins** with Z at 65535. This resolved a contradiction that had
consumed a lot of time.

**The earlier zero readings were correct measurements taken during windows when the DACs were
unconfigured.** Not a probing error, not a dead op-amp.

Along the way, several probing hypotheses were raised and are worth recording as **not the cause**:
recessed female DB9 sockets preventing probe contact; a large series resistor dividing the signal
(R6 is only 220 R); and capacitor squeal (MLCCs are piezoelectric and can sing at 1 kHz) being
mistaken for the piezo. The last was a reasonable hypothesis that turned out to be wrong.

### A.3.18 Stage 5 PASS: all three axes verified

Measured at the **scan head end of the DSUB1 cable**, which proves the entire chain including the
connector mating and the cable run.

| Commanded | White (Z+X) | Grey (Z-X) | Blue (Z+Y) | Green (Z-Y) |
|---|---|---|---|---|
| all at midscale | ~0 | ~0 | ~0 | ~0 |
| **Z = 65535** | **-10 V** | **-10 V** | **-10 V** | **-10 V** |
| **X = 65535** | **-3 V** | **+3 V** | 0 | 0 |
| **Y = 65535** | 0 | 0 | **-3 V** | **+3 V** |

**The signature method used here is worth reusing:** because every J1 signal pin contains Z,
driving Z moves all four together; driving X moves exactly two in **opposite** directions; driving
Y moves the **other** two. This identifies each axis without needing to know which physical pin is
which, which mattered given repeated DB9 numbering confusion.

**This also empirically confirms the ±3 V range finding.** Z reads ±10 V (range bits `000`) while
X and Y read ±3 V (range bits `101`). The firmware comments claiming ±5 V for X and Y are wrong,
and there are now **measurements** proving it rather than only a datasheet reading.

### A.3.19 An expectation error worth recording

During the X test the expected value was stated as ±10 V. **That was wrong**: X and Y run on the
±3 V range. The measured ±3 V was correct and complete, not a shortfall.

### A.3.20 ROOT CAUSE: the power-ordering trap

After the successful Stage 5 measurements, the board was power-cycled and **the DACs went dead
again (LED1-4 lit)**. This revealed the deeper cause, which is **not** the SPI clock:

1. The Teensy is **USB-powered** and boots the instant USB is connected.
2. `setup()` immediately runs `stm.reset()`, writing DAC configuration.
3. If the **analog supply is off at that moment**, the DACs are unpowered and those writes go
   nowhere.
4. The supplies are then switched on. The DACs power up **unconfigured**, ALERT asserted,
   LED1-4 lit.
5. **`setup()` never runs again.** Cycling the analog supply does **not** reboot the Teensy,
   because USB keeps it alive.
6. The DACs stay dead indefinitely until something sends `RSET`.

**Every symptom across all three sessions follows from this**, including the one time it appeared
to fix itself: a **reflash reboots the Teensy after the analog rails are already up**, so
`setup()` runs with the DACs powered and configuration succeeds.

Fixes: **send `RSET` after powering up the analog supply**, or power the analog supply on **before**
connecting USB.

A firmware fix was discussed but not implemented: re-run `stm.reset()` on a schedule, poll the
ALERT lines, or add a settling delay after `SPI.begin()`. None is needed while the `RSET` rule is
followed.

### A.3.21 Preamp investigation

Sequence of findings, several of which reversed:

1. JP1 pin 2 and pin 5 both read floating values that drifted while probed and recovered when
   released. Concluded both rails were missing at the preamp.
2. Protoboard pads were measured: the pad where **yellow** lands reads **+15 V**, the pad where
   **orange** lands reads **-15 V**. So the rails **do** arrive at the protoboard. Board, DSUB2
   mating and cable all confirmed good.
3. Brown (PREAMP-) read floating; **red (PREAMP+) read a constant 11.9 V**, i.e. the preamp output
   railed near the positive rail.
4. Measured against **controller-board ground** rather than against a JP1 pin, one JP1 pin read
   **-15 V** and another read **+15 V**, while pin1-referenced measurements were floating.
5. Concluded the preamp's **ground was open**. **The user challenged this** ("our green ground is
   working no?"). Re-measured: a JP1 pin read **0.000 V solid**. **Ground is connected. The
   conclusion was wrong.**
6. Verified at the chip: **IC1 pin 7 = +15 V, IC1 pin 4 = -15 V.** Polarity correct, no damage.
   **JP1's pin numbering in the older notes is mirrored relative to how it was being counted**,
   which is why pin-referenced measurements looked wrong.

**Lesson, worth more than any single finding: when readings drift and do not make sense, verify
your ground reference before anything else.** Hours across two sessions were spent measuring
against JP1 pin 1, which was not ground.

### A.3.22 Stage 6: the remaining fault

Measured at IC1 (OPA627) against controller ground:

| Pin | Function | Reading | Should be |
|---|---|---|---|
| **3** | +IN | **0 V** | 0 V, correct |
| **2** | **-IN** | **constant 1.4 V** | **0 V, matching pin 3** |
| 6 | OUT | floating / earlier railed ~11.9 V | near 0 V |

**Pin 2 sitting 1.4 V away from pin 3 is the diagnosis.** In a working transimpedance amplifier the
feedback loop forces the inverting input to virtual ground, essentially equal to the
non-inverting input. A 1.4 V difference means **the loop is not closed.**

**This is not explained by the absent tip.** OPA627 input bias current is a few picoamps, which
through 100 MOhm is a fraction of a millivolt, and the feedback resistor remains connected whether
or not a tip is fitted. A rejected hypothesis was that a floating input alone rails the output;
the numbers do not support it.

### A.3.23 `TONE` command added

At the user's request ("buzz the buzzer, maybe play a few different notes"), a tone generator was
added. See A.6.2. A C major scale, a resonance sweep from 1 kHz to 12 kHz, Twinkle Twinkle, and an
arpeggio were played. **Whether the sweep audibly peaked at 8.6 kHz was not reported back and
remains unconfirmed.**

---

## A.4 COMPLETE VERIFIED REFERENCE DATA

### A.4.1 Firmware pin assignments (from source)

```cpp
#define CS_ADC 38    // ADC chip select / LTC2326 RDL
#define ADC_MISO 39
#define CNV 19
#define BUSY 18
#define SERIAL_LED 0 // defined but NEVER USED anywhere in the codebase
#define TUNNEL_LED 1 // defined but NEVER USED anywhere in the codebase
#define DAC_1 7   // dac_x
#define DAC_3 8   // dac_z
#define DAC_2 9   // dac_y
#define DAC_4 10  // dac_bias
#define IN1 33
#define IN2 34
#define IN3 35
#define IN4 36
#define STEPS_PER_REVOLUTION 2048   // VERIFIED CORRECT by measurement
```
```cpp
SPI1.setSCK(27); SPI1.setCS(38); SPI1.setMISO(39);   // ADC bus
// SPI (DAC bus) uses Teensy 4.1 defaults: MOSI 11, MISO 12, SCK 13
```

### A.4.2 Connector naming (CRITICAL, caused repeated confusion)

| Name in docs | Actual silkscreen | Board | What | Position |
|---|---|---|---|---|
| **J1** | **DSUB1** | Controller | DB9 to scan head / piezo | bottom **left** |
| **J2** | **DSUB2** | Controller | DB9 to preamp | bottom **right** |
| **JP1** | JP1 | **PREAMP board** | 5-pin header, ±15 V in and signal out | separate PCB |
| **JP2** | - | - | **Does not exist anywhere in this project** | - |
| - | **H1** | Controller | 26-pin ribbon to Teensy | top **left** |
| - | **U19** | Controller | 3-pin JST power input | **right edge** |

### A.4.3 Full H1 ribbon pinout (verified against firmware and PCB)

| Teensy | H1 pin | Net | Purpose |
|---|---|---|---|
| 19 | 2 | ADC_CNV | start conversion |
| 18 | 4 | ADC_BUSY | conversion status (input) |
| 38 | 6 | ADC_SDI | LTC2326 **RDL read-enable** |
| 27 | 8 | ADC_SCK | SPI1 clock |
| 39 | 10 | ADC_SDO | SPI1 data in |
| **13** | **12** | **SCLK** | SPI clock, **all four DACs** (also the onboard LED) |
| **11** | **14** | **SDI** | SPI data, **all four DACs** |
| 10 | 16 | SYNC4 | U4, bias DAC |
| 9 | 18 | SYNC2 | U2, Y DAC |
| 8 | 20 | SYNC3 | U3, Z DAC |
| 7 | 22 | SYNC1 | U1, X DAC |
| - | 1,3,5..23,25 | AGND | all 13 odd pins |
| - | **24, 26** | - | **unconnected by design** |

**Note pins 8 and 9 are deliberately "swapped" relative to axis order.** That is correct.

**There is no MISO on the DAC bus.** Teensy pin 12 is not wired to the ribbon and H1 has no DAC
data-return line, so **the DACs can never be read back** to confirm they received anything. This is
a large part of why diagnosis was so difficult.

Motor pins 33/34/35/36 go straight to the ULN2003 and **do not touch the ribbon**.

### A.4.4 Controller board LEDs

| LED | Fed from | Through | Sinks into | Indicates |
|---|---|---|---|---|
| LED1 | **3.3V rail** | R1 | U1 pin 1 | DAC 1 (X) ALERT asserted |
| LED2 | **3.3V rail** | R2 | U2 pin 1 | DAC 2 (Y) ALERT asserted |
| LED3 | **3.3V rail** | R3 | U3 pin 1 | DAC 3 (Z) ALERT asserted |
| LED4 | **3.3V rail** | R4 | U4 pin 1 | DAC 4 (bias) ALERT asserted |
| LED5 | **V++** | R27 | AGND | positive input rail present |
| LED6 | AGND | R33 | **V--** | negative input rail present |

**LED1-4 dark = DACs configured and working. Lit = DACs dead.** This is the single most useful
indicator on the board.

Pin 1 = ALERT is read from the AD5761 pinout, corroborated by ten surrounding pins matching the
datasheet exactly (pad 4 = VREF1, 5 = AGND, 6 = -15V, 7 = VOUT, 8 = +15V, 12 = SDI, 13 = SYNC,
14 = SCLK, 15 = 3.3V, 16 = AGND).

### A.4.5 Cable wire colours (JUXINICE DB9 male to bare wire)

| DB9 pin | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| Colour | Black | Brown | Red | **Orange** | **Yellow** | Green | Blue | Grey | White |

**DSUB2 cable (preamp):**

| Colour | Pin | Function |
|---|---|---|
| Black | 1 | BIAS |
| Brown | 2 | PREAMP- |
| Red | 3 | PREAMP+ |
| **Orange** | **4** | **-15 V** |
| **Yellow** | **5** | **+15 V** |
| Green, Blue, Grey, White | 6-9 | AGND |

**DSUB1 cable (scan head):**

| Colour | Pin | Function |
|---|---|---|
| Black, Brown, Red, Orange, Yellow | 1-5 | AGND |
| **Green** | 6 | **Z-Y** |
| **Blue** | 7 | **Z+Y** |
| **Grey** | 8 | **Z-X** |
| **White** | 9 | **Z+X** |

**The colours mean completely different things on the two cables.** Orange is -15 V on the preamp
cable and plain AGND on the scan head cable.

### A.4.6 Connector row properties (avoids all pin counting)

| Connector | Row of 5 | Row of 4 |
|---|---|---|
| **DSUB1** | **all AGND** | Z signals |
| **DSUB2** | BIAS, PREAMP±, -15 V, +15 V | **all AGND** |
| **H1** | odd pins, all AGND | even pins, signals |

### A.4.7 Power tree

| Regulator | Part | Package | In | Out | LCSC |
|---|---|---|---|---|---|
| U19 | B3B-XH-AM | JST XH 3-pin | - | V++, AGND, V-- | - |
| U17 | **SL7815** | TO-220 | V++ | +15 V | C458979 |
| U18 | **L7915CV** (ST) | TO-220 | V-- | -15 V | C154950 |
| U16 | **BD733L5FP-CE2** (ROHM) | TO-252 | V++ | 3.3 V | C509724 |
| U22 | **MC7805CDTG** (onsemi) | DPAK | V++ | 5 V | C897464 |

U18 pinout: pad 1 = AGND, pad 2 = V-- (in), pad 3 = -15 V (out).
U17 pinout: pad 1 = V++ (in), pad 2 = AGND, pad 3 = +15 V (out).
**The pin orders differ between them.** That is correct: negative regulators (7915-style) use a
different pinout from positive ones (7815-style).

U9 and U10 are dual op-amps: 8 MHz GBP, 2.3 V/us slew, ±2.5 to 18 V, 3.7 mA per channel.

### A.4.8 Output stage

```
U3 (DAC Z) --ZOUT--> R8 --> U9 pin 6 --> U9 pin 7 --> R6 --> DSUB1 pin 9 (Z+X)
U1 (DAC X) --XOUT--> R7 -----^
```

- **R5 = R7 = R8 = R10 = R11 = R12 = R13 = R15 = R17 = R18 = R21 = R22 = 3 k**
- **R6 = R9 = R14 = R19 = 220 R** (series into the DB9)
- U9 channel B: non-inverting input (pin 5) tied to AGND, so it is an **inverting summing amp with
  gain exactly -1 per input**. A positive command gives a negative output.
- U9 channel A produces Z-X as a difference amp.
- U10 does the same for the Y pair.

U9 pinout: 1 = OUT A, 2 = -IN A, 3 = +IN A, 4 = -15V, 5 = AGND (+IN B), 6 = -IN B, 7 = OUT B,
8 = +15V. U10 identical.

### A.4.9 Board physical layout (mm from lower-left of the component area, board ~103 x 88)

```
        LEFT                                              RIGHT
  y=72  .                    U16(54)      U22(73)      U19(91)  <- power JST
  y=67  H1(17) ribbon
  y=63  .                                          LED5(88) LED6(92)
  y=52  .                                                   U18(91)  <- -15V reg
  y=43  U1(6)   U3(21)   U2(35)   U4(49)   U5(60)   <- four DACs + reference
  y=38  .                                                   U17(91)  <- +15V reg
  y=17  U9(14)          U10(37)           U13(63)   <- output op-amps
  y=0   DSUB1(18)                       DSUB2(74)
```

Both TO-220 regulators and the power input are on the **right edge**. The DACs run across the
middle. The -15 V rail crosses about 90 mm to reach U1.

### A.4.10 DAC identity

| Chip | Output net | SYNC | Teensy pin | Axis | Range bits | Range |
|---|---|---|---|---|---|---|
| U1 | XOUT | SYNC1 | 7 | X | `101` | **±3 V** |
| U2 | YOUT | SYNC2 | 9 | Y | `101` | **±3 V** |
| U3 | ZOUT | SYNC3 | 8 | Z | `000` | **±10 V** |
| U4 | SAMPLE | SYNC4 | 10 | bias | `101` | ±3 V |

DAC codes 0-65535, centre 32768 = 0 V. **Firmware comments claiming ±5 V for X and Y are wrong**
and this is now confirmed by measurement, not only by reading range bits.

### A.4.11 VREF1

| Component | Pad | Net |
|---|---|---|
| U5 | 6 | VREF1 (source) |
| U1, U2, U3, U4 | 4 | VREF1 |
| C54 | 1 | VREF1 |

**Measured: exactly 2.5 V across C54.** U5 is powered from +15 V (pad 2), which is why VREF1 was
healthy even while other things were suspected.

### A.4.12 Piezo element

18 mm copper/brass buzzer disc. **Resonant frequency 8.6 ± 0.7 kHz.** Capacitance 15,000 pF ± 30%.
Working voltage 1.5-30 V. Operating temperature -20 to +70 C. Pre-wired.

---

## A.5 FALSE TRAILS AND CORRECTIONS (READ THIS SECTION)

Every one of these was stated confidently and later proved wrong. They are recorded so nobody
re-runs them.

### A.5.1 "The DAC internal reference is disabled and may be the fault" - WRONG

Claimed because IRO = 0 in the instantiated mode words while `AD5761.hpp`'s own documented
examples set that bit. **Disproved:** the PCB has a `VREF1` net feeding pad 4 of U1, U2, U3 and
U4, sourced by U5 and decoupled by C54, and it measures exactly 2.5 V. The board supplies an
external reference, so `IRO = 0` is **correct**. **Do not enable the internal reference** - with an
external reference already driving the REF pins that is a conflict, not a fix.

### A.5.2 "LED1-4 are SYNC/chip-select indicators" - WRONG

They connect to U1-U4 **pin 1 (ALERT)**, not pin 13 (SYNC). Asserted without checking the pad
number. Corrected from the PCB netlist.

### A.5.3 "LED5 on with LED6 off means V-- is missing" - WRONG IN CONTEXT

True only when the bench supply is **on**. With the supply **off** and USB connected, LED1-5 lit
and LED6 dark is **expected phantom powering**, not a fault. See A.1.8.

### A.5.4 "The ADC is stuck at -32768, so the read path has a digital fault" - WRONG

Reasoning used: "a constant reading with no noise must be digital." **The flaw: at full-scale
saturation the ADC clips, which removes the noise too**, so a railed analog input produces exactly
the same pinned constant a digital fault would. The preamp was simply still settling after
power-up. **Do not change the RDL polarity in `LTC2326_16.cpp`.**

### A.5.5 "U18 has failed" - WRONG

Based on **misreading the user's message**. They wrote "we got values as expect" meaning *as
expected if healthy* (pad 2 = -18 V **and** pad 3 = -15 V). It was read as confirming a failure
prediction. **U18 works.**

### A.5.6 "There is a break in the -15 V net on the board" - WRONG

All nine -15 V capacitors tested good, U18 pad 3 to DSUB2 pin 4 is continuous, and the bare spare
board confirms the routing. The -15 V distribution is intact.

### A.5.7 "The solder bridges are cracked and intermittent" - WRONG

The RSET flex test produced flickering that turned out to be **the RSET loop itself** (each RSET
resets then reconfigures each DAC, blinking ALERT for ~100 ms). Poking changed nothing. There is
no mechanically intermittent joint.

### A.5.8 "The preamp's ground is open" - WRONG

Concluded because JP1 pin1-referenced measurements floated. **The user challenged it** and a
re-measurement against controller ground found a JP1 pin at **0.000 V solid**. Ground is
connected. The real problem was that **JP1's pin numbering in the older notes is mirrored**
relative to how it was being counted, so every pin-referenced measurement was unreliable.

### A.5.9 "The buzz was capacitor squeal, not the piezo" - WRONG

A reasonable hypothesis (MLCCs are piezoelectric and audibly sing at 1 kHz) but disproved: the
clicking heard during the RSET loop is the piezo responding to DAC output steps, and the piezo
does move when the DACs are configured.

### A.5.10 "Expect ±10 V on the X test" - WRONG

X and Y run on the **±3 V** range. The measured ±3 V was correct and complete.

### A.5.11 "Current draw jumped to 0.6 A, power down immediately" - WRONG

User had written 0.06 A. No fault. Alarm withdrawn.

### A.5.12 Backlash recorded before it was measured - CORRECTED

An early draft recorded a large reverse-direction shortfall. At that point **no reverse move had
been watched with the tape in place**. When actually measured, the tape returned to its original
position and backlash is negligible.

---

## A.6 CODE CHANGES MADE

### A.6.1 SPI clock (`lib/AD5761/AD5761.hpp`)

40 MHz -> 1 MHz, with an explanatory comment block. See A.3.12.

### A.6.2 `TONE` command (new)

Added to `src/stm_firmware.hpp` inside the `STM` class:

```cpp
void play_tone(int freq_hz, int duration_ms)
{
    if (freq_hz < 20 || freq_hz > 20000 || duration_ms <= 0) { return; }
    long half_us = (500000L / freq_hz) - 25;   // minus rough SPI write time
    if (half_us < 1) { half_us = 1; }
    long cycles = ((long)duration_ms * 1000L) / (half_us * 2);
    for (long i = 0; i < cycles; i++)
    {
        set_dac_z(50000);
        delayMicroseconds(half_us);
        set_dac_z(15536);      // symmetric about midscale, no DC offset
        delayMicroseconds(half_us);
    }
    set_dac_z(32768);          // park at 0 V, never leave Z at a rail
}
```

And in `src/main.cpp`:
```cpp
if (command == "TONE")
{
  int freq = Serial.parseInt();
  int ms = Serial.parseInt();
  stm.play_tone(freq, ms);
}
```

Usage: `TONE <freq_hz> <duration_ms>`

**Why it is better than `TEST` for checking the piezo:**

| | `TEST` | `TONE` |
|---|---|---|
| Frequency | fixed 1 kHz | 20 Hz to 20 kHz |
| Can reach 8.6 kHz resonance | no | **yes** |
| DC offset | asymmetric | symmetric |
| Leaves Z at | **-10 V (hazard)** | **0 V, parked** |

**Recommended standard piezo check: `TONE 8600 500`.**

Both changes are additive. `TEST` still behaves exactly as before, including its hazard.

### A.6.3 Changes considered but NOT made

- **Firmware fix for the power-ordering trap.** Options discussed: re-run `stm.reset()` on a
  schedule, poll the ALERT lines, add a settling delay after `SPI.begin()`. Not implemented
  because the `RSET` rule covers it.
- **Enabling the AD5761 internal reference (setting D5).** Explicitly rejected, see A.5.1.
- **Changing the RDL/CS polarity in `LTC2326_16.cpp`.** Explicitly rejected, see A.5.4.
- **Raising the SPI clock back above 1 MHz.** Rejected; no benefit and the failure mode is silent.
- **GUI bug fixes in `stm_control.py`.** Still outstanding, see A.8.

---

## A.7 OPERATING RULES

1. **After powering on the analog supply, send `RSET`.** Otherwise the DACs are unconfigured.
2. **LED1-4 lit = DACs dead. Dark = working.** Check before trusting any measurement.
3. **Re-park after every `TEST` AND after every `RSET`**: `DACZ 32768`, `DACX 32768`,
   `DACY 32768`. Both leave Z at a rail. `AD5761::reset()` writes PV=00, which selects zero
   scale, so `RSET` is just as much of a full-scale Z excursion as `TEST` is. Corrected
   2026-08-31.
4. **Unplug USB before any resistance or continuity measurement**, or phantom powering makes the
   readings invalid and loads the Teensy's ESD diodes.
5. **Never use the PlatformIO serial monitor.** It holds the port (causing the button-press loop)
   and sends per-keystroke (breaking the 4-char parser). Use `stm_console.py`.
6. **Tip stays out until Stage 6 passes.** Z sits at -10 V at power-on and after every `TEST`.
7. **Power off before unplugging any DB9.** Its pins carry amplifier outputs at up to ±10 V.
8. **When readings drift and make no sense, verify your ground reference first.**
9. **Do not judge the piezo by ear at ANY frequency. Use a meter.** Swept 1 kHz to 11 kHz on
   2026-08-31: pitch tracked the command, **no loudness peak anywhere**. The 8.6 kHz figure is a
   free-air buzzer spec and does not survive the disc being clamped into the scan head and
   mass-loaded by the tip holder. `TONE` is still better than `TEST` because it parks Z at 0 V
   instead of a rail, but not for the resonance reason.
10. **Row-of-5 / row-of-4 trick:** on DSUB1 the row of 5 is all AGND; on DSUB2 the row of 4 is all
    AGND. Avoids DB9 numbering being mirrored between plug and socket.
11. **CHECK LED1-4 IMMEDIATELY BEFORE AND AFTER EVERY MEASUREMENT.** Added 2026-08-31. The DACs
    drop their configuration roughly hourly and **software cannot detect it** - the ALERT pins go
    to the LEDs only, they are not wired to the Teensy, and there is no DAC readback. `GSTS` will
    happily report `dac_z = 65535` while the chip outputs nothing. Any reading taken with one of
    those LEDs lit is void. An hour was lost to this on 2026-08-31, diagnosing a "dead bias path"
    that turned out to be a perfectly healthy board with unconfigured DACs.
12. **Take a control measurement.** Before believing any negative result, command a KNOWN-GOOD
    channel and measure it the same way. That single step is what exposed the false bias fault.

---

## A.8 OUTSTANDING WORK

### A.8.1 The one open fault

**Stage 6: the preamp feedback loop is open.** IC1 pin 2 sits at a constant 1.4 V while pin 3 is
at 0 V.

The input node is **deliberately air-wired on a PTFE standoff** with zero copper, to avoid leakage
at picoamp levels. Three things meet there:

1. the **100 MOhm feedback resistor**
2. the **tip coax centre conductor**
3. a **link wire to IC1 pin 2**

Any one coming adrift opens the loop, and that construction is fragile by design.

**Check in this order:**
- Visual inspection of the standoff under magnification, looking for a lifted or broken wire
- Continuity from IC1 pin 2 to the standoff junction
- The 100 MOhm resistor itself. **The DST-201 may not read 100 MOhm; if it reads open, that may be
  a range limit rather than a failed part.** Do not condemn it on that alone
- Confirm **PAD1 is not being used as the input**. It is the op-amp **output**, downstream of R1.
  This was a repeated point of confusion in earlier sessions

### A.8.2 Unverified / unreported

- **Whether the 8.6 kHz resonance sweep was audibly louder than the other tones.** The `TONE`
  demo was played but the result was never reported. Worth repeating as a piezo health check.
- **Whether `IMG_7846.mov` shows anything useful.** It could not be processed.
- **The exact JP1 pin numbering.** The preamp board files are not in this repo, and the numbering
  in the older notes is mirrored relative to how it was being counted. **Identify JP1 pins
  empirically** by measuring each against controller ground: +15 V, -15 V, OUT (railed or
  wandering), and two grounds at 0.000 V.

### A.8.3 After Stage 6 passes

1. Re-run Stage 5 as a regression check (`TONE 8600 500` is better than `TEST`)
2. Stage 6 proper: preamp output stable near 0 V with the tip disconnected
3. **Only then install a tip**
4. Set PID gains with `PIDS`. **They initialise to 0.0, 0.0, 0.0**, not the `INIT_KP/KI/KD` defines
   (2.0/1.0/1.0), which are only referenced in a commented-out line. Constant-current mode does
   nothing until `PIDS` is sent
5. Fix the GUI bugs in `stm_control.py` before using it:
   - `move_motor()` missing the f-string prefix, so it sends literal `MTMV {steps}`
   - `get_status()` exception handler references `self.history[-1]`, IndexError on first run
   - `set_buffer_size()` is Windows-only pyserial, AttributeError on Mac/Linux
   - `start_scan()` uses a stale loop variable in the `else` branch
   - X/Y/Z voltage conversions assume ±5 V for all three; actual is ±3/±3/±10
6. **`APRH` last.** It drives Z while stepping the motor forward hunting for a current threshold,
   which moves the tip toward the sample automatically

### A.8.4 Housekeeping

- A duplicate `red-panda-stm/` folder exists inside the project root with its own `.git`. It is
  the upstream clone. The user confirmed it can be ignored. **Note there are two copies of
  `Code/pc/stm_control.py`;** the live one is the top-level `Code/pc/`.
- `IMG_7846.mov` (23 MB) sits in `Code/teensy/` and is probably worth moving or removing.
- Two PlatformIO Home sessions were seen running against one VS Code window. Closing all VS Code
  windows clears orphaned sessions.

---

## A.9 DIAGNOSTIC TECHNIQUES WORTH REUSING

1. **Use a bare/unpopulated board as a routing reference.** The user's spare PCB confirmed the
   expected copper connections independently of any populated-board fault.
2. **Use a known-good signal as a control.** +15 V was proven working, so it validated probe
   technique before trusting a -15 V reading.
3. **Signature testing instead of pin counting.** Driving Z moves all four DSUB1 signal pins; X
   moves two in opposite directions; Y moves the other two. Identifies axes without knowing which
   physical pin is which.
4. **Row properties instead of pin numbers.** See A.4.6.
5. **Bracket a suspect segment.** Measure both sides of a joint under power; voltage on one side
   and not the other is a confirmed open.
6. **Distinguish "floating" from "connected" by behaviour**, not value: a floating node drifts,
   sags when the meter loads it, and recovers when released. A real rail is rock solid.
7. **Physics check on resistance-vs-open:** with almost no load current, contact resistance
   cannot drop 15 V to nothing. V = IR, and if I is near zero there is no drop regardless of R. A
   floating reading therefore means an **open**, not a bad contact.
8. **Continuity is not sufficient.** It proves a DC path exists. It says nothing about signal
   integrity at speed (the 40 MHz problem), and it can pass under probe pressure on a joint that
   is open at rest.
9. **Time-correlation vs stimulus-correlation.** The ADC readings drifted monotonically with
   *time* (preamp settling) rather than with the commanded Z value. Checking which variable a
   change tracks avoids false causation.

---

## A.10 STYLE AND COMMUNICATION PREFERENCES (carried from the original handoff, still current)

- No em-dashes in written docs
- Plain, direct language; avoid corporate or AI-sounding phrasing
- Every technical claim traced to a real source (Gerber, PCB netlist, firmware source, photo,
  datasheet), and **flag clearly when something is inference rather than verified fact**
- Brevity and directness; the user dislikes padding
- Structured comparisons and tables preferred over prose
- The user asks good clarifying questions and **pushes back correctly**. Two of the biggest
  breakthroughs in these sessions came directly from user objections (the solder-bridge objection
  in A.3.10 and the ground objection in A.5.8). **Take the pushback seriously.**
