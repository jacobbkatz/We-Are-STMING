# Session plan, 2026-08-31

Budget: 3 to 4 hours. Written against `PROJECT_HANDOFF_SUMMARY.md` plus a fresh read of the
firmware, the two SPI drivers, `stm_console.py` and the EasyEDA schematic sheets.

---

# PART 0. Corrections to the handoff, read before starting

Nine things in the handoff are either wrong against the source, or missing. Two of them change
what you should do today.

## 0.1 The ADC bus also runs at 40 MHz. The handoff says otherwise.

Handoff A.3.11 lists the ADC clock as "library default" and uses that to explain why the ADC
worked while the DACs did not. That is wrong.

```
lib/LTC2326/LTC2326_16.hpp:58
const SPISettings _spi_settings = SPISettings(40000000, MSBFIRST, SPI_MODE2);
```

The ADC has been running at **40 MHz over the same ribbon** that could not carry 40 MHz to the
DACs. The real difference between the two buses is not clock rate. It is that a DAC that misses a
write goes silently dead and lights an ALERT LED, while an ADC that misses a bit **still returns a
number that looks like data**.

Every ADC reading recorded so far was taken at 40 MHz. They may be fine. They have never been
checked. This is now Goal 2.

## 0.2 The Stage 6 "open feedback loop" diagnosis has a second explanation, and it is more likely

The handoff reads IC1 pin 2 at a constant 1.4 V against pin 3 at 0 V and concludes the feedback
loop is open.

Run the numbers on that. A typical handheld meter presents about 10 MOhm. If the input node were
genuinely open and floating, the only current into it would be the OPA627's input bias current, a
few pA. Through 10 MOhm that is **under a millivolt**, not 1.4 V. To hold 1.4 V across a 10 MOhm
meter something must push about **140 nA** into that node, which is roughly 30,000 times the
op-amp's input bias current.

There is exactly one plausible 140 nA source there: the output, railed at the +11.9 V that was
measured earlier, feeding back through the 100 MOhm resistor. That forms a divider:

```
11.9 V x 10 MOhm / (100 MOhm + 10 MOhm) = 1.08 V     measured 1.4 V
```

Right magnitude, and the gap closes entirely if the output is a little higher than 11.9 V or the
resistor is under its marked value.

**If that is what is happening, the 100 MOhm feedback resistor is intact, not open.** Without it
there is no path at all from the railed output back to pin 2 and the meter would read near zero.
The 1.4 V is weak evidence *for* a connected feedback resistor.

This flips the suspect list. The handoff's leading candidate is a lifted wire at the PTFE standoff.
A likelier candidate is a **leakage path from the input node to one of the supply rails**, of order
100 nA, most often flux residue, fingerprints, or moisture across the standoff. That forces the
output to rail in order to source the leakage through Rf, which produces every symptom seen.

Note also that a leak from the input node **to ground** would not rail the output. Only a leak to a
rail does. That narrows it usefully.

Assumption flagged: this depends on the DST-201 presenting about 10 MOhm on DC volts. Verify from
its manual. The qualitative conclusion, a resistive path from a railed output back to pin 2, holds
for any meter impedance well below 100 MOhm.

Test T3 below settles amp-alive versus amp-dead in five minutes, before any of this matters.

## 0.3 "Z sits at -10 V at power on" describes the DAC, not the piezo, and the hazard direction is unproven

`DAC_BOOT_STATE.md` and operating rule 6 treat the power-on state as a tip hazard. But the output
stage is an inverting summing amp with gain exactly -1, which is measured, not assumed. So:

| | DAC code | DAC output | Voltage at DSUB1 |
|---|---|---|---|
| Power-on / post-RSET (zero scale) | 0 | -10 V | **+10 V** |
| Midscale | 32768 | 0 V | 0 V |
| Full scale | 65535 | +10 V | -10 V |

Now read `approach()`. It sweeps Z from code 10000 up to 50000 hunting for current, which at
DSUB1 is +6.8 V sweeping down to -5.3 V. The sweep direction has to be the direction that moves the
tip **toward** the sample, or the routine is nonsense.

**Inference, not fact:** if that holds, increasing Z code extends toward the sample, and the
power-on zero-scale state is therefore **maximum retract**, the safest position, not a hazard. The
handoff has this backwards.

Do not act on either version. Act on the rule that is safe under both:

> **Park Z at midscale (32768) whenever the coarse motor moves.** That keeps half the Z range
> available in each direction no matter which sign is which.

Resolve the polarity properly the first time you see real tunneling current, when it becomes
obvious in one measurement.

## 0.4 RSET drops all four DACs to zero scale, same as TEST

`AD5761::reset()` does a software full reset then writes the control register with PV = 00, which
selects zero scale. It never writes a data register. So every `RSET` slams Z to a rail exactly the
way `TEST` does.

Operating rule 3 in the handoff only requires re-parking after `TEST`. It should say **after
`RSET` too**. This matters the moment a tip is installed, because rule 1 tells you to send `RSET`
on every power-up.

## 0.5 `APRH` does not take the arguments the handoff implies

```cpp
// src/main.cpp
int adc_target = Serial.parseInt();
int steps      = Serial.parseInt();
stm.start_approach(adc_target, 10000, steps);   // signature: (target, max_steps, step_interval)
```

The second argument you type is the **step interval per iteration**, not a step count. Maximum
travel is hardcoded at **10000 steps, about 4.9 motor revolutions**, and you cannot change it from
the serial interface.

## 0.6 `approach()` compares signed ADC counts with `>`, and the measured baseline is negative

```cpp
if (read_adc() > approach_config.target_dac)
```

Recorded no-tip baseline readings are **-2393, -3005, -3520, -4287, -3982, -2340, -2856, -2545**.
All negative. Nobody has established which way the reading moves when current flows.

If tunneling drives the reading **more negative**, this test never fires and the routine drives the
tip 10000 steps into the sample without stopping.

**This is the single most dangerous unverified assumption in the codebase.** Do not run `APRH`
until the sign is known. Today's answer is not to patch it but to avoid it: see Goal 6.

## 0.7 Two different ADC full-scale constants exist in the tree

| Location | Constant |
|---|---|
| `lib/LTC2326/LTC2326_16.hpp:59` | `_ref_buffer_volts = 4.096f` |
| `Code/pc/stm_control.py:37` and `stm_console.py` | `10.24` |

They cannot both be right, and this constant is what converts ADC counts to amps, which is what
sets your approach threshold. Unresolved. Calibrate it empirically (T7).

Separately, `LTC2326_16::read_volts()` returns `val * 4.096` and is missing the `/ 32768`. It is
never called, so nothing is broken today, but do not start calling it.

## 0.8 `GSTS` field 5 is a raw ADC sample. `ADCR` is a 5-sample average.

Not stated anywhere in the handoff, and it matters for measuring noise.

- `loop()` calls `update()`, which stores `read_adc_raw()` into `stm_status.adc`
- `ADCR` calls `read_adc()`, which returns the 5-sample rolling average

**Use `GSTS` for noise measurements, `ADCR` for a settled value.** Averaging five samples hides
exactly the corruption T6 is looking for.

## 0.9 Smaller items, no action needed today

| Item | Location | Impact |
|---|---|---|
| `SPI.beginTransaction` with no matching `endTransaction` | `lib/AD5761/AD5761.cpp:52` | None now, latent trap if anything else joins the DAC bus |
| Two `LTC2326_16` objects on the same pins, one file-scope and one class member | `src/stm_firmware.hpp:42` and `:503` | Member shadows the global, global is dead code, both constructors touch pins 38/19/18 |
| `stm_console.py` does not know `TONE` blocks | `BLOCKING_COMMANDS` | Next command lands mid-tone and is read as garbage. 2 minute fix |
| `logTable[abs(adc)]` bounds | `src/logTable.hpp` is `[32769]` | **Safe.** abs(-32768) = 32768 is in range. Do not "fix" this |

## 0.10 Missing information

1. **No sample material is mentioned anywhere in the project.** No HOPG, no gold on mica, no
   graphite. You cannot image without one. Confirm before planning a next session around imaging.
2. **The coarse approach step size in nanometres is unknown.** 2048 steps per motor revolution is
   measured, but the screw pitch and any lever reduction are not recorded, so nobody knows how far
   one motor step moves the tip. **One motor step must move less than the Z piezo range or the
   approach crashes the tip regardless of how good the electronics are.** Rough estimate: an M3
   screw at 0.5 mm pitch driven directly gives 244 nm per step, against a disc-scanner Z range
   likely around 1 um. That is only about four steps per Z range, which is tight. Any lever
   reduction improves it. Measure or derive this before the first approach.
3. DST-201 DC input impedance, needed to finish the reasoning in 0.2.
4. Whether a tip has been prepared at all. The handoff says one has never been installed.

---

# PART 1. Current assessment

## Where the project is

**Late integration, early validation.** Not prototyping, and not yet debugging in the general
sense. Every subsystem has been individually proven except one, and the remaining work is about
trusting measurements rather than finding faults.

| Chain | Status |
|---|---|
| USB, serial, command parser | Proven |
| Motor, driver, coil order, step calibration | Proven both directions, 2048 steps/rev measured |
| Analog rails, both legs, all four regulators | Proven, currents sane |
| SPI to all four DACs | Proven after the 40 MHz to 1 MHz fix |
| DAC to output amps to DSUB1 to piezo | Proven with a meter at the far end of the cable, all three axes |
| Preamp power and ground | Proven at the chip |
| **Preamp signal path** | **Open fault, the one blocker** |
| ADC digital path | Returns varying numbers, **never validated** |
| Current calibration, counts to amps | Never established |
| Bias to sample holder | **Never metered** |
| Approach, scan, PID | Never run, and the approach trigger sign is unverified |

## Highest priority unresolved issues, ranked

1. **Preamp feedback loop.** Blocks everything. Nothing downstream can be tested without it.
2. **Whether the ADC is telling the truth at 40 MHz.** Silent corruption would poison every current
   measurement from here to the first image, and it is cheap to rule out.
3. **The approach trigger sign.** A tip-destroying bug sitting in code that is one command away
   from being run.
4. **The counts-to-amps constant.** Without it you cannot pick an approach threshold, only guess.
5. **The bias path to the sample.** An untested link that fails identically to a bad tip.

## What today is really about

Two sessions were spent chasing faults. Today should be spent **converting "it appears to work"
into "it is measured"**, and closing the one real fault. That is what makes the first approach
survivable.

---

# PART 2. Goals, ranked

| # | Goal | Why it matters | Impact | Time | Depends on | P(success) |
|---|---|---|---|---|---|---|
| 1 | **Close Stage 6.** Preamp output stable near 0 V, tip disconnected | Only open fault, blocks the whole project | Unblocks everything downstream | 45 to 75 min | Magnifier, iron, clip leads, one 100k to 1M resistor, IPA | **85% diagnosed, 55% repaired today** |
| 2 | **Establish whether the ADC is trustworthy** at 40 MHz vs 1 MHz | ADC bus runs the clock that killed the DACs, and a corrupted ADC looks exactly like a working one | Removes a silent risk that would waste a future session | 30 min | Reflash working | 90% |
| 3 | **Measure the ADC noise floor and baseline** | You cannot choose an approach threshold without knowing the noise band | Makes a first approach possible at all | 20 min | Goal 2 | 95% |
| 4 | **Verify the bias path to the sample holder** with a meter | Never tested. A dead bias path produces no tunneling and is indistinguishable from a bad tip | Closes the last untested wiring link | 15 min | Analog power up | 90% |
| 5 | **Dummy junction test.** Known resistor across the junction, measure current end to end | Proves the whole current path with no tip and zero crash risk, and calibrates counts per amp | Turns Goals 1 to 4 into one end-to-end number | 30 min | Goal 1 fixed, plus a 1M to 10M resistor | 70% given Goal 1 |
| 6 | **PC-side manual approach tool**, abortable, human threshold | Removes the `APRH` sign bug from the critical path without touching firmware | Makes the first approach safe to attempt next session | 30 min | None, can be written any time | 85% |
| 7 | **Commit and update the docs** | Two sessions of firmware fixes are still uncommitted | Protects the work | 20 min | None | 99% |

Goals 1 to 4 plus 7 fit inside 3 hours if the preamp cooperates. 5 and 6 are the fourth hour.

---

# PART 3. Timeline

Times are from T+0:00, the moment the bench is set up.

## Block A. T+0:00 to 0:20. Bring-up and regression.

Do this in order. It re-establishes a known-good baseline and closes one open question for free.

1. **Commit first.** `lib/AD5761/AD5761.hpp`, `src/main.cpp` and `src/stm_firmware.hpp` carry two
   sessions of fixes and are uncommitted. Five minutes of insurance against a bad edit later.
2. Confirm no stale PlatformIO monitor holds the port:
   `Get-WmiObject Win32_Process | Where-Object { $_.CommandLine -match 'device monitor' }`
3. **Analog supply on first, then USB.** That ordering makes the power-ordering trap impossible.
   Confirm LED5 and LED6 both lit.
4. `python stm_console.py RSET`, then confirm **LED1 to LED4 all dark**. If any is lit, stop and
   resend. Nothing below is valid with a lit ALERT LED.
5. Re-park: `DACX 32768`, `DACY 32768`, `DACZ 32768`, `BIAS 32768`.
6. `GSTS`. Expect ten fields, uptime climbing.
7. **T2, the resonance sweep.** Closes handoff item A.8.2, which has been open since 2026-08-30.

**Success looks like:** LED1-4 dark, LED5-6 lit, GSTS answering, tone audible.
**Move on regardless at T+0:20.**

## Block B. T+0:20 to 1:25. The preamp. The blocker.

**Hard stop at T+1:25.** If it is not fixed by then, record where you got to and move to Block C.
Everything in C and D is worth doing either way.

1. **T3 first, always.** The follower test. Five minutes, and it splits the problem cleanly into
   "amp is dead" or "amp is fine and the fault is in the input network". Do not inspect anything
   under magnification before running it. Two sessions were lost to inspecting before measuring.
2. Branch on the T3 result:
   - **Output goes to near 0 V.** The OPA627 is healthy. Fault is in the high-impedance input
     network. Go to T4, then clean and inspect the standoff.
   - **Output stays railed.** The amp is damaged or its supplies are wrong under load. Recheck
     pins 7 and 4 with the strap still fitted, then plan an OPA627 replacement. Do not spend the
     rest of the block on the standoff.
3. If the amp is healthy, work the input node in this order, **cheapest and least invasive first**:
   - **Clean before you resolder.** Flux residue and fingerprints across a picoamp node are a
     100 nA leak, and per 0.2 that is the leading hypothesis. IPA, soft brush, then dry
     thoroughly. Warm air helps. Re-measure after it is properly dry, not while damp.
   - Only then inspect under magnification for a lifted wire.
   - Only then reflow.
4. Re-run T3 and T5 after every single change, one change at a time. Two changes between
   measurements and you learn nothing.

**Success looks like:** IC1 pin 6 sits within a few tens of mV of 0 V, stable, tip disconnected,
and pin 2 tracks pin 3.

**Decision point at T+1:25:** fixed, or diagnosed with a part to order. Either is an acceptable
outcome. Grinding past the stop is not.

## Block C. T+1:25 to 2:10. Do I trust the ADC.

Runs whether or not Block B succeeded. If the preamp is still broken the input is garbage, but the
question here is about the digital path, and a railed or floating input is actually a **usefully
constant** signal to measure noise against.

1. **T6.** 50 GSTS samples at 40 MHz, reflash the ADC driver to 1 MHz, 50 more. Compare.
2. **T7** if and only if the preamp is fixed. Calibrate counts per volt.
3. Decide and record the counts-to-amps constant, or record that it is still unknown and why.

**Success looks like:** a number for the ADC noise floor in counts, and a documented decision on
the SPI clock backed by data.

## Block D. T+2:10 to 2:50. The current path end to end.

1. **T8, bias path.** 15 minutes, no dependencies beyond analog power. Do it even if the preamp is
   dead.
2. **T9, dummy junction.** Only if the preamp is fixed. This is the payoff test of the whole day.

**Success looks like:** a measured, predicted-in-advance current reading through a known resistor.
That single number validates bias, sample holder, tip holder, preamp, cable, ADC front end and ADC
in one shot.

## Block E. T+2:50 to 3:20. Approach safety. Optional fourth hour.

Write `Code/pc/stm_approach.py`. Do **not** patch `approach()` in firmware today.

Reasoning: a PC-side loop of `MTMV 4` then `GSTS` is abortable with Ctrl-C, prints every reading,
lets a human set and change the threshold live, and needs no reflash to change behaviour. The
firmware routine is none of those things, and per 0.6 its trigger test may be backwards.

Minimum viable version:
- step by a small fixed number of motor steps
- read ADC after each step
- print the reading and the running baseline delta
- stop on **absolute deviation from baseline**, not on a signed comparison, which sidesteps 0.6
- hard cap on total steps, set from the command line
- Ctrl-C stops immediately

## Block F. T+3:20 to 3:45. Write up and commit.

1. Update `PROJECT_HANDOFF_SUMMARY.md` with today's results, including the Part 0 corrections.
2. Commit everything.
3. Write the top three items for next session while they are still fresh.

## If you only have 3 hours

Cut Block E. Compress Block F to 15 minutes. Blocks A to D are the session.

---

# PART 4. Testing strategy

## T1. Power-up regression

| | |
|---|---|
| **Objective** | Confirm nothing regressed since 2026-08-30 and establish a known-good baseline |
| **Setup** | Analog supply on **before** USB. Tip out. Meter on DSUB1 not required |
| **Procedure** | `RSET`, check LED1-4 dark, park all four DACs at 32768, `GSTS` |
| **Expected** | LED1-4 dark, LED5-6 lit, ten CSV fields, uptime climbing |
| **Failure** | Any of LED1-4 lit after RSET |
| **If it fails** | Resend RSET once. Still lit means the SPI fix regressed or a DAC is genuinely faulty. Check that the 1 MHz `SPISettings` is still in `AD5761.hpp` before suspecting hardware |
| **Conclusion either way** | Pass means the whole digital and DAC chain is intact and today's measurements start from solid ground |

## T2. Resonance sweep, closes A.8.2

| | |
|---|---|
| **Objective** | Answer the question left open on 2026-08-30: does the piezo audibly peak near 8.6 kHz |
| **Setup** | Quiet room. Scan head connected. Tip out |
| **Procedure** | `TONE 1000 400`, `TONE 4000 400`, `TONE 6000 400`, `TONE 8000 400`, `TONE 8600 400`, `TONE 9200 400`, `TONE 11000 400`. Leave 2 s between them, because `stm_console.py` does not know `TONE` blocks and will return early |
| **Expected** | A clear loudness peak somewhere in the 8000 to 9200 band |
| **Failure** | Flat across the sweep, or silent throughout |
| **Conclusions** | **Peak found:** the disc, its wiring and the whole Z drive chain are mechanically alive. Strongest single confirmation available without a tip. **Flat but audible:** driving something, but possibly not the disc. Suspect a capacitor singing, per A.5.9. **Silent:** contradicts the Stage 5 meter results, so suspect the scan head connection rather than the electronics |
| **Next action** | Record the frequency of the peak. It is the mechanical resonance of the assembled head, which is worth knowing later when picking scan rates |
| **Cheap fix first** | Add `"TONE"` to `BLOCKING_COMMANDS` in `stm_console.py` with the duration parsed from the argument. Two minutes, and it makes this test scriptable |

## T3. Preamp follower test. THE decisive one.

| | |
|---|---|
| **Objective** | Split the fault cleanly: is the OPA627 alive, or is the fault in the input network |
| **Why first** | It is the only test that distinguishes those two without touching the fragile air-wired node, and every other Stage 6 action depends on the answer |
| **Setup** | Preamp powered, tip disconnected, meter black lead on **controller board ground**, not on a JP1 pin. Handoff A.5.8 lost hours to exactly that |
| **Procedure** | Clip a **100k to 1M resistor** from IC1 pin 6 (output) to IC1 pin 2 (inverting input). Wait 10 s. Measure pin 6 against controller ground |
| **Why a resistor and not a wire** | A hard short makes a unity-gain follower, which is valid, but with the tip coax capacitance still hanging on the node it can oscillate. A resistor damps that and the DC conclusion is identical |
| **Expected if the amp is healthy** | Pin 6 goes to within a few mV of 0 V, because the strap is now a low-impedance feedback path around an amp whose +IN is at 0 V |
| **Expected if the amp is damaged** | Pin 6 stays railed |
| **Conclusions** | **Goes to 0 V:** OPA627 is fine, supplies are fine, and the fault is entirely in the 100 MOhm / standoff / coax network. Move to T4 and cleaning. This is the good outcome and it is also the most likely one given the reasoning in 0.2. **Stays railed:** the amp is damaged, or its supplies collapse under load. Re-measure pins 7 and 4 **with the strap fitted**, because a supply that is fine unloaded can sag when the output actually drives. If the supplies hold and it stays railed, order an OPA627 and stop working this fault today |
| **Failure conditions** | Reading wanders instead of settling. That means the strap is not making contact, or the meter is on a JP1 pin instead of board ground |

## T4. Is the 100 MOhm resistor actually connected

| | |
|---|---|
| **Objective** | Decide whether Rf is intact, without trusting a meter to read 100 MOhm |
| **Setup** | T3 strap **removed**. Preamp powered, tip out, meter on board ground |
| **Procedure** | Measure IC1 pin 6 and IC1 pin 2, **in the same sitting, minutes apart at most**. Record both. Then compute the ratio pin2 / pin6 |
| **Expected if Rf is intact** | Ratio is roughly `Zmeter / (100M + Zmeter)`, about 0.09 for a 10 MOhm meter. The recorded numbers, 1.4 V on pin 2 against about 11.9 V on pin 6, give 0.12, which is in that region |
| **Expected if Rf is open** | Pin 2 reads near zero regardless of what pin 6 is doing, because the meter has nothing to pull against |
| **Conclusions** | **Ratio in the expected region:** Rf is connected. Stop suspecting the resistor, and stop suspecting a fully open standoff. The fault is a leakage path, and cleaning is the fix. **Pin 2 near zero:** genuinely open node, and the handoff's original diagnosis stands. Inspect and resolder |
| **Note** | The two handoff readings were taken in different sessions, which is why this needs redoing together. Do not reuse the old numbers |
| **Direct resistance check** | Optional, USB unplugged and power off. If the DST-201 reads open at 100 MOhm that is probably its range limit, not a dead part. Do not condemn the resistor on that alone |

## T5. Stage 6 proper, the acceptance test

| | |
|---|---|
| **Objective** | The actual Stage 6 pass condition |
| **Setup** | All straps removed, tip disconnected, preamp powered, board ground reference |
| **Procedure** | Power up, **wait at least 5 minutes** for settling, then measure IC1 pin 6 and pin 2. Also read `ADCR` a few times |
| **Why the wait** | Handoff A.1.12: an OPA627 with 100 MOhm feedback and a floating input takes minutes to settle. A reading taken at 30 seconds caused a completely wrong diagnosis last time |
| **Expected** | Pin 6 within tens of mV of 0 V and stable. Pin 2 essentially equal to pin 3. ADC reading small and varying rather than pinned |
| **Failure** | Output railed, or output slowly drifting toward a rail |
| **Conclusions** | **Stable near 0 V:** Stage 6 passes. The project is unblocked. **Slow drift toward a rail:** a leakage path remains, smaller than before. Clean again and re-dry. **Immediately railed:** the repair did not take |
| **Record** | The settling time as well as the final value. It is a useful health signature for later comparison |

## T6. Is the ADC telling the truth at 40 MHz

| | |
|---|---|
| **Objective** | Determine whether the 40 MHz ADC clock is corrupting readings over the same ribbon that failed the DACs at 40 MHz |
| **Why it matters** | Corrupted ADC data looks exactly like working ADC data. The DACs at least announced their failure with four LEDs. This is the same class of fault with no indicator |
| **Setup** | Input as static as you can make it. A railed preamp is fine and is actually the quietest input available. Do not change anything about the analog side between the two runs |
| **Procedure** | 1. `python stm_console.py GSTS -n 50`, capture field 5. **Use GSTS, not ADCR:** per 0.8, ADCR averages five samples and would hide exactly what you are looking for. 2. Edit `lib/LTC2326/LTC2326_16.hpp:58` to `SPISettings(1000000, MSBFIRST, SPI_MODE2)`. 3. Reflash. 4. Repeat the 50 samples. 5. Compare mean, standard deviation, and worst outlier |
| **Expected if 40 MHz is fine** | Both runs have similar mean and similar spread. Conclusion recorded, doubt closed |
| **Expected if 40 MHz is corrupting** | The 1 MHz run is noticeably tighter, or the 40 MHz run has occasional wild outliers that vanish. Corrupted SPI bits usually show as **large isolated jumps**, often powers of two, rather than as a wider Gaussian. Look for that signature specifically |
| **Conclusions** | **Tighter at 1 MHz:** keep 1 MHz, and treat every ADC number recorded before today as suspect. **No difference:** keep 1 MHz anyway. There is no benefit to 40 MHz here, the ADC is read at most a few thousand times a second, and matching the DAC bus removes a variable permanently |
| **Next action** | Whichever way it goes, leave the clock at 1 MHz and write the result into the handoff |
| **Tooling** | Worth 10 minutes to write `Code/pc/adc_stats.py` that collects N samples and prints mean, stdev, min, max. You will use it again for T7 and T9 |

## T7. Preamp to ADC transfer calibration

| | |
|---|---|
| **Objective** | Resolve the 4.096 versus 10.24 conflict from 0.7 and get a real counts-per-volt figure |
| **Prerequisite** | Preamp fixed, T5 passed |
| **Setup** | Meter on DSUB2 pin 3, the **red** wire, PREAMP+, against board ground. Note the DSUB2 row of 4 is all AGND, so you can take ground from there without counting pins |
| **Procedure** | Read the preamp output voltage on the meter and `ADCR` from the firmware **at the same time**, at two or more different output levels. Getting different levels without a tip is the hard part. Easiest method: take one point during power-up settling while the output is still drifting, and another after it settles. Two well-separated points give the slope |
| **Expected** | A consistent counts-per-volt slope. Compare against 32768 counts per 4.096 V (8000 counts/V) and 32768 per 10.24 V (3200 counts/V) |
| **Failure** | Slope matches neither, or is not repeatable |
| **Conclusions** | **Matches one of them:** that constant is correct, fix the other, and current readings become meaningful. **Matches neither:** there is gain in the ADC front end. U21 is an LT1469 dual op-amp with 470 R / 3.3 nF filters into U15, and its gain has not been traced from the schematic. Use the measured slope and note the discrepancy for later tracing |
| **Note** | This is the number that lets you convert an approach threshold into an actual current in amps. Without it every threshold is a guess |

## T8. Bias path to the sample holder

| | |
|---|---|
| **Objective** | Verify the one wiring link nobody has ever metered |
| **Why it matters** | Stage 4 confirmed the bias DAC via `GSTS`, but that field is firmware bookkeeping, not a readback. There is no MISO on the DAC bus, so nothing has ever confirmed the bias voltage exists outside the chip |
| **Setup** | Meter at the **sample holder**, or at DSUB2 pin 1, the **black** wire, against board ground. Analog power on, tip out |
| **Procedure** | Send `BIAS 32768`, measure. Then `BIAS 43690`, measure. Then `BIAS 21846`, measure |
| **Expected magnitudes** | 32768 is 0 V. 43690 is 1.0 V at the DAC. 21846 is -1.0 V at the DAC |
| **Expected sign, inference not fact** | The schematic shows U13 as an OPA2227P with R30 and R31 at 3k and R32 at 220 R, the same pattern as the X, Y and Z output stages, which are measured inverting with gain -1. **If the bias path is built the same way, +1.0 V commanded gives -1.0 V at the sample.** This is inferred from component values and designator grouping, not from a traced netlist. The measurement settles it |
| **Failure** | 0 V at all three settings, or a value that does not scale with the command |
| **Conclusions** | **Scales correctly:** the bias path works and the sign is now known, which you need for T9 and for every future IV curve. **Dead:** trace U13 and DSUB2 pin 1. Note this would have looked exactly like a bad tip during a first approach, which is why it is worth 15 minutes now |

## T9. Dummy junction. The payoff test.

| | |
|---|---|
| **Objective** | Prove the entire current path end to end and calibrate counts per amp, with no tip and no crash risk |
| **Prerequisites** | T5 passed, T8 passed, and a resistor somewhere between 1M and 100M. 10M is ideal |
| **Concept** | Replace the tunnel junction with a known resistor. The preamp cannot tell the difference. This is a standard bring-up test for any transimpedance front end |
| **Setup** | Clip the resistor between the **sample holder** (bias) and the **tip holder** (preamp input). Do it at the holders, which are designed to be connected and disconnected, **not** at the PTFE standoff. The whole point is to avoid touching the fragile node |
| **Procedure** | 1. `BIAS 32768`, record baseline ADC. 2. `BIAS` to a value giving about 0.1 V at the sample, record ADC. 3. Repeat for about 0.5 V. 4. Reverse the sign and repeat |
| **Predict before you measure** | With a 10M dummy and 0.1 V across it, the current is 10 nA. Through a 100 MOhm feedback resistor that is 1.0 V at the preamp output. **Write your prediction down before reading the meter.** Predicting first is what makes a mismatch informative |
| **Expected** | ADC changes in proportion to bias, linearly, and reverses when bias reverses |
| **Failure** | No change with bias, or a change that does not scale |
| **Conclusions** | **Scales linearly:** the complete chain works, bias through sample holder through junction through tip holder through coax through preamp through DSUB2 through the ADC front end into the ADC. That is the entire measurement system validated in one test. You also get counts per amp directly, which resolves 0.7 completely. **And critically, you learn the sign**, which is the answer to 0.6 and the thing that makes a first approach safe. **No change:** the fault is between the holders and the preamp input, which points back at the standoff and the coax |
| **This test is worth more than everything else in Block D combined.** If time is short, drop T8's third measurement, not this |

---

# PART 5. Risk analysis

## Biggest technical risks

| Risk | Likelihood | Consequence | Mitigation |
|---|---|---|---|
| **The OPA627 is damaged** | Medium | Blocks the project until a part arrives, probably days | T3 answers this in 5 minutes. Run it first. Order a spare today regardless of the result, it is a cheap part and the input node is fragile by design |
| **The preamp fault is a leak that comes back** | Medium | Looks fixed, then fails intermittently later, which is the worst kind of fault to debug | After cleaning, re-measure after a full 5 minute settle, and again 20 minutes later. A leak that is drying out will drift |
| **The ADC has been returning corrupted data all along** | Low to medium | Every recorded current reading is void, and thresholds set from them are meaningless | T6, 30 minutes |
| **`APRH` gets run** | Low but catastrophic | Drives the tip 10000 steps into the sample. See 0.6 | Do not type it. Goal 6 replaces it |
| **One motor step is larger than the Z piezo range** | Unknown, unmeasured | Makes any approach a crash no matter how good the electronics are. See 0.10 item 2 | Derive the number before the next session. Not today's job but do not forget it |

## Things likely to eat unexpected time

1. **Chasing the preamp past the hard stop.** This is the single most likely way to lose the
   session. Two previous sessions ran long on exactly this subsystem. **Set a timer for T+1:25.**
2. **Reflashing.** Every firmware change costs a rebuild, an upload and a re-park. Batch the edits
   for T6 and anything else into **one** flash rather than three.
3. **Measuring against the wrong ground.** Cost hours across two sessions per A.5.8. Black lead on
   controller board ground, every time, no exceptions.
4. **Judging a settling preamp too early.** Cost a completely wrong diagnosis per A.5.4 and A.1.12.
   Five minutes minimum before believing any preamp or ADC reading after power-up.
5. **Changing two things between measurements.** Then neither result means anything and you repeat
   both.

## Easy mistakes to avoid

| Mistake | Why it bites |
|---|---|
| Forgetting `RSET` after analog power-up | LED1-4 lit, DACs dead, every reading meaningless. Handoff rule 1 |
| Forgetting to re-park after `RSET` or `TEST` | Both leave Z at a rail. See 0.4 |
| Metering with USB connected | Phantom powering invalidates resistance readings and loads the Teensy. Handoff rule 4 |
| Using the PlatformIO monitor | Holds the port, causes the PROGRAM button loop, and loses the 4-character race. Handoff rule 5 |
| Using `ADCR` for noise measurements | It averages five samples. Use `GSTS`. See 0.8 |
| Trusting `GSTS` DAC fields as a readback | There is no MISO on the DAC bus. Those fields are firmware bookkeeping only |
| Judging the piezo by ear at 1 kHz | Resonance is 8.6 kHz. Use `TONE`. Handoff rule 9 |
| Reusing a measurement from a previous session in a ratio | T4 specifically needs both readings taken together |

## Assumptions to verify before acting on them

| Assumption | How to check | Blocking? |
|---|---|---|
| DST-201 presents about 10 MOhm on DC volts | Its manual | No, only affects the arithmetic in 0.2, not the direction |
| Increasing Z code extends toward the sample | Inferred from the direction of the `approach()` sweep. Confirm at first tunneling | **Yes, before a tip goes in** |
| The bias path inverts, gain -1 | T8 measures it | Yes, before T9 |
| The counts-to-amps constant | T7 and T9 | Yes, before setting any threshold |
| A sample material exists | Ask | Yes, before planning to image |

---

# PART 6. Stretch goals

Ranked by value if Blocks A to D finish early.

| Rank | Goal | Value | Time |
|---|---|---|---|
| 1 | **`stm_approach.py`, the PC-side manual approach** | Highest. Directly removes the biggest tip-destroying risk in the project and is the gate on the next session | 30 min |
| 2 | **Derive the coarse step size in nm** from the CAD and the screw pitch | High. This is the number that decides whether an approach is physically survivable, and it is currently unknown | 30 min, mostly reading CAD |
| 3 | **Fix the four known GUI bugs** in `stm_control.py` | Medium. Needed eventually, blocks nothing today. Listed in handoff A.8.3 item 5 | 30 min |
| 4 | **Tip preparation**, cut or etched | Medium. Independent of all electronics work, and a good use of time if a part is on order | 45 min |
| 5 | **Housekeeping.** Remove `IMG_7846.mov` (23 MB) from the repo, remove the duplicate `ltc2326` object, add `endTransaction` | Low individually, but cheap and it stops the tree accumulating noise | 20 min |
| 6 | **Set PID gains and test `CCON` against the dummy junction** | Speculative but interesting. A fixed resistor gives a constant current, so the loop should drive Z to a steady value and hold. Tests the PID path with nothing at risk | 30 min |

Stretch 6 is genuinely clever if you get there. A dummy junction is a stable current source, so
constant-current mode against it is a completely safe way to find out whether the PID loop works
before a real tip is anywhere near a sample.

---

# PART 7. End of session deliverables

## Working and verified

- Stage 6 either **passed** with a measured stable preamp output, or **definitively diagnosed**
  with a named part to replace
- ADC SPI clock decision made **from data**, not assumption, and the clock set to 1 MHz
- ADC noise floor known in counts, so an approach threshold can be chosen rather than guessed
- Bias path to the sample holder measured, with its sign established
- If the preamp is fixed: one end-to-end current measurement through a known resistor, predicted
  before it was measured

## Data collected

| Measurement | Units | Why kept |
|---|---|---|
| Piezo resonance peak | Hz | Mechanical health signature, informs scan rates |
| IC1 pin 6 and pin 2, before and after repair | V | Stage 6 acceptance record |
| Preamp settling time from power-up | s | Prevents another premature diagnosis |
| ADC mean, stdev, min, max at 40 MHz and 1 MHz, 50 samples each | counts | Sets the approach threshold, closes the 40 MHz question |
| Bias command versus voltage at the sample holder, 3 points | codes and V | Establishes bias sign and scale |
| Dummy junction current versus bias, 4 points | codes and A | Counts per amp, and the current sign |

## Code

- `lib/LTC2326/LTC2326_16.hpp` SPI clock at 1 MHz with a comment explaining why, matching the
  existing comment style in `AD5761.hpp`
- `stm_console.py` knows `TONE` blocks
- `Code/pc/adc_stats.py`, new
- `Code/pc/stm_approach.py`, new, if Block E happens
- Everything committed. The tree currently has two sessions of uncommitted firmware fixes

## Documentation

- `PROJECT_HANDOFF_SUMMARY.md` updated with today's results **and** the Part 0 corrections,
  particularly the ADC clock error in A.3.11, the Stage 6 reinterpretation, and the Z direction
  question
- A short "next session, first three things" note written while it is fresh

## What will still be open

| Item | Why it is not today's job |
|---|---|
| Z direction, toward or away from the sample | Only resolvable at first tunneling, or from the CAD |
| Coarse step size in nm | Needs CAD work, not bench work |
| `approach()` sign bug in firmware | Being routed around rather than fixed. Fix it when the sign is known from T9 |
| The four GUI bugs | Blocks nothing until scanning starts |
| Sample material | Needs an answer from you, not from the bench |
| First approach and first image | Not realistic today, and attempting it would risk the tip and the sample for no information gain |

---

# What today is not

**Do not attempt a first approach.** The tip has never been installed, the preamp is not yet
fixed, the trigger sign is unverified, the counts-to-amps constant is unknown, and the coarse step
size in nanometres is undocumented. Every one of those is a reason to wait, and today's plan
resolves three of them.

A session that ends with a fixed preamp, a trustworthy ADC and a measured current through a dummy
junction has made the first approach **possible**. That is the win available today.
