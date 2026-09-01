# Finding the −15 V break — bench procedure

For the FNIRSI DST-201. Written to be followed at the bench, in order.

**What we know going in:**

- U18 **generates −15 V correctly** (pad 2 = −18 V in, pad 3 = −15 V out, measured 2026-08-29)
- The preamp end (JP1 pin 5) has **no −15 V** — it floats positive and creeps back up after
  the meter loads it
- So the rail exists at its source and is missing at its destination. **Something between them
  is broken.**

---

## Board map

Positions in mm from the lower-left corner of the component area. Board is about 103 x 88 mm.

```
        LEFT                                              RIGHT
  y=72  .                    U16(54)      U22(73)      U19(91)  <- power JST
  y=67  H1(17) ribbon
  y=63  .                                          LED5(88) LED6(92)
  y=52  .                                                   U18(91)  <- -15V REG
  y=43  U1(6)   U3(21)   U2(35)   U4(49)   U5(60)
  y=38  .                                                   U17(91)  <- +15V reg
  y=17  U9(14)          U10(37)           U13(63)
  y=0   J1/DSUB1(18)                    J2/DSUB2(74)
```

**Orientation landmarks:** the two TO-220 regulators (U17, U18) and the 3-pin power JST (U19)
are all on the **right edge**. The ribbon header H1 is **top left**. J1 is **bottom left**, J2 is
**bottom right**.

**The rail has to travel from U18 on the right edge all the way to U1 on the left.** That is the
run we are testing.

---

## The −15 V capacitors, ordered by distance from U18

This ordering is the whole method. Walk outward until the rail disappears, and the break is
between the last good point and the first bad one.

| Order | Cap | Distance from U18 | Sits next to |
|---|---|---|---|
| 1 | **C62** | **6 mm** | U18 itself |
| 2 | **C47** | 43 mm | J2 / DSUB2 |
| 3 | **C20** | 47 mm | U4 |
| 4 | C19 | 48 mm | U4 |
| 5 | **C34** | 54 mm | U13 |
| 6 | **C8** | 59 mm | U2 |
| 7 | C7 | 60 mm | U2 |
| 8 | **C45** | 73 mm | U10 |
| 9 | **C14** | 73 mm | U3 |
| 10 | C13 | 74 mm | U3 |
| 11 | **C2** | 89 mm | U1 |
| 12 | C1 | 90 mm | U1 |
| 13 | **C44** | 92 mm | U9 |

The bolded ones are enough. The others are the second capacitor of a pair on the same chip and
add nothing unless you get an odd result.

---

# METHOD A — Continuity, power OFF. Do this one first.

Safer, faster, and more definitive than voltage probing. A copper net either connects or it
does not.

## A1. Shut down properly

1. **Switch off both bench supplies.**
2. **UNPLUG THE USB FROM THE TEENSY.**

> **The USB step is not optional.** With USB connected the board is phantom-powered through the
> Teensy's I/O pins, so it is not at 0 V and every resistance reading is invalid. We hit this on
> 2026-08-29 and it also loads the Teensy's pins through their ESD diodes. Unplug it.

3. Unplug the preamp cable from **J2** so you can reach J2's pins.
4. Leave the scan head plugged into J1 or not, does not matter for this.

## A2. Set up the DST-201

1. Probes: **black into COM**, **red into the VΩ jack**.
2. Select **continuity** (the beeper / diode symbol group). Resistance (Ω) works too if you
   prefer reading numbers.
3. **Validate the meter and leads before trusting anything:** touch the two probe tips
   together. You should get a **beep and a reading near 0 Ω**. If it does not beep, fix that
   before going further — a broken lead will look exactly like a broken trace.

## A3. Anchor on U18 pad 3

**U18 pad 3 is the leg you measured yesterday that read −15 V.** That is your reference point
for every test below.

If it helps: U18 is the TO-220 on the right edge. Pad 1 = AGND, pad 2 = V-- input,
pad 3 = −15 V output.

**Hold the black probe on U18 pad 3 for the entire sequence.** If your meter came with an
alligator-clip lead, use it here so you only have one probe to place.

## A4. Walk outward

For each capacitor in the order in the table, touch the red probe to **each of its two pads**.
One pad is on the −15 V net and one is on AGND, so you are looking for **exactly one of the two
pads to beep**.

| What you get | Meaning |
|---|---|
| **One pad beeps, the other does not** | Rail is intact this far. **Move to the next capacitor** |
| **Neither pad beeps** | **BREAK FOUND.** It is between this cap and the last one that beeped |
| Both pads beep | Stop and tell me. That is a short between −15 V and AGND, a different fault |

Work down the list: **C62 → C47 → C20 → C34 → C8 → C45 → C14 → C2 → C44.**

## A5. Also check J2 directly

J2's pin rows split conveniently:

- **Row of 4 (pins 6-9): all AGND**
- **Row of 5 (pins 1-5): BIAS, PREAMP−, PREAMP+, −15 V, +15 V**

Keep the black probe on U18 pad 3 and touch the red probe to **each of the five pins in the row
of 5**. You do not need to count pins.

| Result | Meaning |
|---|---|
| **Exactly one pin beeps** | The board delivers −15 V to J2. **The break is in the J2 CABLE**, not the board |
| **No pin beeps** | The break is **on the board**, between U18 and J2 |

---

# METHOD B — Voltage, power ON. Only if Method A is inconclusive.

## B1. Setup

1. Reconnect USB and the supplies, power on.
2. DST-201 to **DC voltage**. It is auto-ranging and 19999-count, so no range picking needed.
3. **Black probe on a solid AGND** — any pin in J1's **row of 5**, they are all AGND. An
   alligator clip here is worth it.

## B2. Walk the same list

Red probe to the −15 V pad of each capacitor, in the same order.

| Reading | Meaning |
|---|---|
| **−15 V, steady** | Rail is good here. Next capacitor |
| **Positive, and it sags when probed then recovers** | **Floating. Break is before this point** |
| 0 V and stays there | Also bad, note it and tell me |

**Do not leave the board powered longer than the measurement needs.** A floating positive on the
negative rail is out of spec for every chip on that net.

---

# What to write down

Just the point where it changes:

```
Last capacitor that was GOOD:  C____
First capacitor that was BAD:  C____
J2 row-of-5: did any pin beep?  YES / NO
```

That pair of capacitors localises the break to one segment of copper, and their positions in the
table above tell us roughly where on the board to look for it.

---

# Interpreting the result

| Pattern | Diagnosis |
|---|---|
| C62 good, everything else bad | Break right at U18's output. Check U18's solder joints first |
| Good out to C47/C20, bad further left | Break in the middle of the board run |
| **All capacitors good, J2 row-of-5 has no beep** | Board is fine, break is at the **J2 connector** |
| **All capacitors good AND one J2 pin beeps** | **Board is entirely fine.** Break is in the **J2 cable**. And that means the DACs DO have −15 V, so the dead DAC output is a **separate** fault - next suspect is the 40 MHz SPI bus over the ribbon |

That last row is the important fork. If the board's −15 V distribution turns out to be perfect,
we have two independent problems rather than one, and the DAC investigation restarts from
scratch with the SPI bus as the lead suspect.

---

# Useful later: the DST-201 has a scope

1 MHz analog bandwidth, 5 MSa/s. If this turns into an SPI investigation, that scope can look at
SCLK, SDI and the SYNC lines on the ribbon header H1 (top left of the board).

Be aware of the limitation: **the firmware clocks SPI at 40 MHz**
(`SPISettings(40000000, MSBFIRST, SPI_MODE2)` in `AD5761.cpp`). A 1 MHz scope cannot show that
waveform properly. It **can** still show whether the SYNC lines are toggling at all, which is a
useful yes/no. If we need real SPI waveforms we would first drop the clock in firmware to
something the scope can see, which is a one-line change and worth doing anyway - 40 MHz over a
ribbon cable is aggressive.
