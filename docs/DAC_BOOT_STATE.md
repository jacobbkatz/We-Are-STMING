# DAC boot state — read before Stage 3

Found while confirming the first successful flash. Two items, one is a safety note for
bringing up the analog supply, the other is a prime suspect if the DACs turn out dead in
Stage 4 or Stage 5.

Nothing here needs changing before you test. But if `TEST` is silent on all three axes,
come back to item 2 before you start suspecting the piezo or the ribbon.

---

## Verified from source

`STM::reset()` in `stm_firmware.hpp` resets each DAC:

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

and `AD5761::reset()` in `AD5761.cpp` is only these two writes:

```cpp
void AD5761::reset()
{
    write(CMD_SW_FULL_RESET, 0);
    delay(100);
    write(CMD_WR_CTRL_REG, _mode);
}
```

**A DAC data register is never written.** Not at boot, not anywhere in `reset()`. The
control register is configured and that is all. So after power-up each AD5761 output sits
at whatever its own power-up default is, until a `BIAS` / `DACX` / `DACY` / `DACZ` command
writes a data value.

This also means the four DAC fields in `GSTS` are `STMStatus` bookkeeping, not a readback.
They are zero after boot because the struct initialises them to zero. **They are not
evidence of what the chip outputs are doing.** Only a meter settles that.

## The two mode words, and how they differ from the library's own examples

Instantiated in `stm_firmware.hpp`:

```cpp
AD5761 dac_x    = AD5761(DAC_1, 0b0000000000000101);
AD5761 dac_y    = AD5761(DAC_2, 0b0000000000000101);
AD5761 dac_z    = AD5761(DAC_3, 0b0000000000000000);
AD5761 dac_bias = AD5761(DAC_4, 0b0000000000000101);
```

Documented as examples at the top of `AD5761.hpp`, in the same repo:

```cpp
// 0b0000000101000 -10V, +10V
// 0b0000000101101 -3 to 3V
```

Line the two up bit for bit:

| | D5 | D4 | D3 | D2 | D1 | D0 |
|---|---|---|---|---|---|---|
| header example, ±10 V | **1** | 0 | **1** | 0 | 0 | 0 |
| header example, ±3 V | **1** | 0 | **1** | 1 | 0 | 1 |
| actual `dac_z` | 0 | 0 | 0 | 0 | 0 | 0 |
| actual `dac_x/y/bias` | 0 | 0 | 0 | 1 | 0 | 1 |

The range bits `RA[2:0]` = D2:D0 match, which is what already told you X and Y are ±3 V.
But **D5 and D3 are set in both documented examples and clear in every mode the firmware
actually instantiates.**

## What D5 and D3 are — inference, confirm against the datasheet

This part is read from the AD5761 control register map, not from anything in your repo, so
treat it as inference. The corroboration is that it explains the D5/D3 discrepancy exactly.

| Bits | Field | `00` / `0` means |
|---|---|---|
| D10:D9 | CV[1:0], clear voltage | zero scale |
| D5 | IRO, internal reference enable | **internal reference off** |
| D4:D3 | PV[1:0], power-up voltage | zero scale |
| D2:D0 | RA[2:0], output range | (`000` = ±10 V, `101` = ±3 V) |

Under that map the header's examples have `IRO = 1` (internal reference on) and
`PV = 01` (power up to midscale). The firmware's actual modes have `IRO = 0` and
`PV = 00`.

---

## Item 1 — power-up output is zero scale, not 0 V

`PV = 00` and `CV = 00` both select zero scale, and nothing ever writes a data register.
So the moment the analog rails come up, before you type anything:

| DAC | Range | Sits at |
|---|---|---|
| Z | ±10 V | **−10 V** |
| X | ±3 V | −3 V |
| Y | ±3 V | −3 V |
| bias | ±3 V | −3 V |

The `soft_launch` procedure already says to keep the tip clear before running `TEST` in
Stage 5. **Move that precaution earlier.** Z goes to one extreme of its range the instant
analog power is applied in Stage 3, not when you run `TEST`. If a tip is installed and
anywhere near the sample when you switch the bench supply on, that full-range Z excursion
happens with no command from you.

Practical version: **have the tip out, or the sample well clear, before Stage 3, not
before Stage 5.**

To park the DACs somewhere sane once power is up, write midscale explicitly:

```
DACZ 32768
DACX 32768
DACY 32768
BIAS 32768
```

## Item 2 — the internal reference being off is CORRECT. Resolved, no action.

An earlier version of this note flagged `IRO = 0` (internal reference disabled) as a suspect
if the DACs turned out dead. **That is now settled and it is not a problem.** Leaving the
reasoning here so it does not get re-raised later.

`IRO = 0` means the AD5761 takes an **external** reference on its REF pin rather than using
its own internal 2.5 V. So the question was simply whether the controller board supplies one.

It does. Extracted from the EasyEDA PCB file (`PCB/STMP_easyEDA.zip`, PAD_NET records):

| Component | Pad | Net |
|---|---|---|
| U1 | 4 | VREF1 |
| U2 | 4 | VREF1 |
| U3 | 4 | VREF1 |
| U4 | 4 | VREF1 |
| U5 | 6 | VREF1 |
| C54 | 1 | VREF1 |

U1 through U4 are the four AD5761 DACs, all four taking VREF1 on the same pin. U5 sources it
and C54 decouples it. **The board supplies an external reference to every DAC, so `IRO = 0`
is the right setting and the firmware is correct as written.**

Do **not** set D5 to enable the internal reference. With an external reference already
driving the REF pins, switching the internal one on as well is a conflict, not a fix.

Item 1 above still stands unchanged.
