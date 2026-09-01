# Start Here: Things That Tripped Us Up

I went back through this whole project as if I were seeing it for the first time and wrote down
everything that misled me. Several of these cost real money or real hardware if you get them
wrong.

Read this before you solder anything.

---

## The five that will actually cost you hardware

### 1. PAD1 on the preamp is the output, not the tip input

It's the only obvious pad on the board, it sits near the edge, and it looks exactly like where
you'd attach the tip. It's wired to the op-amp's **pin 6, which is the output.**

Solder the tip there and the microscope will never see a tunneling current.

**The tip goes to an insulated standoff** pressed into a bare hole near the R2 silkscreen. That
standoff is where the 100 Mohm resistor, the tip wire, and a link to the op-amp's input all meet
in mid-air.

### 2. The +/-15 V pins on J2 are outputs

J2 pin 5 is +15 V and pin 4 is -15 V, so it looks like the obvious place to connect a bench
supply. It isn't. The board **generates** those rails and sends them out to the preamplifier.

Connect a supply there and you're pushing voltage backwards into regulator outputs.

**Power goes into U19**, the small 3-pin JST XH connector. Pin 1 is V--, pin 2 is ground, pin 3 is
V++.

### 3. Feed the board +/-18 V, not +/-15 V

The regulators need input above their output, so set your supply to roughly **+/-18 V**. Feed it
+/-15 V and the regulators drop out, giving you low unstable rails that look like a dozen other
problems.

### 4. The 100 Mohm resistor doesn't come on the board

It ships unpopulated, and the R2 footprint has **no copper at all**, just bare drilled holes. That's
deliberate, not a manufacturing fault. Buy the resistor and a PTFE standoff separately.

### 5. A single-output bench supply can't power this

You need +15 V and -15 V at the same time, relative to the same ground. One output has two
terminals and makes one voltage, so it physically can't straddle ground.

Either get a supply with **two independently adjustable channels**, or stack two separate supplies
in series and call the junction ground.

---

## Names that mislead

### box_mount.stl isn't a mount for a box

It's the **rectangular frame** the scan head sits in. Nothing in the name tells you that. The
opening is 131.00 x 101.00 mm and it's 5 mm thick.

### new_body.stl and new_topframe.stl

These are the **bottom and top of the isolation tower**, joined by the three M8 threaded rods. The
"new_" prefix is left over from the original author's revisions and doesn't mean anything.

### The numbers on our enclosure files aren't an assembly order

`1_preamp_box` through `6_shield_cover` are just labels. You don't build them in that sequence,
and parts 4 and 6 are **alternatives to each other**, covered below.

### Platform.stl is a circle, not a square

Its bounding box reads 200 x 200, so it looks square in any file listing. It's actually a
**circular disc, 200 mm diameter by 6 mm.** Scale or cut based on the bounding box and you'll be
wrong.

### The BasePlate hole grid isn't centred

It's a 3x3 grid of M3 holes, but it sits **7.5 mm off centre in X.** Offsets from the part centre
are X = -37.5, -7.5, +22.5 and Y = -27, 0, +27.

Assume it's centred, drill a mating part, and none of the nine holes will line up. This one caught
me while designing the intermediate baseplate.

---

## Choices the files don't make for you

### There are two scan-head enclosures. Use 6_shield_cover

`4_scanhead_box` and `6_shield_cover` do the same job in different ways. **They're alternatives,
not a set.**

- **`6_shield_cover`** matches how the original is built: the head sits open on its baseplate and a
  shield drops over the whole thing. **This is the one we're using.**
- **`4_scanhead_box`** is an earlier enclosed-box approach, kept for reference. Its corner ears are
  142.8 mm wide, so it won't fit inside the shield cover anyway.

### The preamp box is the only part using M2 screws

Everything else here is M3. Buy one bag of hardware and it'll be wrong for exactly one box. Get a
small M2 assortment too.

### Three BOM files exist in the upstream sources

Use the one marked **FIXED**. The others are earlier revisions.

---

## Wiring that looks wrong but isn't

### Wire the motor driver straight across, whatever you read online

Plenty of sources say a 28BYJ-48 needs its coils driven 1-3-2-4. That's true, **and the firmware
already does it.** The code declares the motor as `EfficientStepper(steps, IN1, IN3, IN2, IN4)`,
which performs the swap in software.

So wire it plainly: Teensy 33 to IN1, 34 to IN2, 35 to IN3, 36 to IN4. Swap the wires as well and
the two swaps cancel out, and the motor buzzes instead of turning.

### Ribbon pin 6 does get connected

It's labelled ADC_SDI, which sounds like a data input a read-only ADC wouldn't need. On this chip
that pin is actually **RDL, a read-enable**, effectively the ADC's chip-select.

**Wire ribbon pin 6 to Teensy pin 38.** We had this wrong at first and left it disconnected.

### Ribbon pins 24 and 26 connect to nothing

They're genuinely dead on the board. Leave them alone.

### The motor doesn't go through the ribbon cable

There's no motor circuitry anywhere on the controller PCB. The ULN2003 driver wires **directly to
the Teensy**, separate from the ribbon.

### The Teensy pin labelled 5V is a power input

On the Teensy 4.1 that pin is VIN. It sits at roughly 5 V when USB-powered, so you can run the
motor driver from it, which is what Mech Panda appears to do. The catch is that the motor's current
spikes then ride on the same rail as your microcontroller and can reset it mid-scan. A separate 5 V
supply avoids that.

### The four scanner wires have no colour code

All four piezo quadrant wires are identical bare enamelled copper. There's no way to recover which
quadrant is +X from any file or photo, so **you have to track it yourself as you solder, or work it
out empirically afterwards.** Label them as you go.

If your first image comes out rotated or mirrored, this is why, and it's fixable in software.

---

## Material and process

### Don't use PLA

Mech Panda used PA-CF. We tried PA-CF, couldn't print it reliably at these tolerances, and settled
on **PETG-CF**. Either is fine. **PLA is not.** It creeps under sustained load and moves with
temperature, and that shows up directly as drift in your images.

### Buy five piezo discs, not one

The original designer destroyed 4 or 5 by overheating them. The disc still looks fine and still
reads fine on a multimeter after it's ruined, it just stops moving. Use **low-temperature solder
paste, Sn42/Bi58 at about 138 C**, not ordinary solder, and pre-tin the wire away from the disc.

### Copper tape and aluminium tape aren't interchangeable

Copper takes solder, so you can bond a ground wire straight to it. **Aluminium tape can't be
soldered** because of the oxide layer, and its adhesive is usually non-conductive, so overlapping
strips may not connect to each other at all.

Use copper anywhere that needs a ground connection.

**There is a second reason not to mix them, added 2026-09-01.** Copper and aluminium in contact,
with atmospheric humidity as the electrolyte, form a **galvanic cell** — a few hundred millivolts
of DC sitting on your shield. Into a 100 MOhm transimpedance input that is not a trivial amount.

And **ground the shield.** An ungrounded conductive enclosure floats, couples capacitively to
everything near it, and can be **worse than no shield at all**. Bond it to circuit ground at one
point only — several bonds around an enclosure make a ground loop. We shielded our preamp box and
never grounded it, and it is currently a leading suspect for the offset that is blocking the
build.

### Get a USB data cable

A charge-only cable connects the Teensy to nothing. This wastes more first-day hours than anything
else in the project.

---

## How we mark uncertainty

Items marked **VERIFY** in the assembly manual are **genuinely undocumented in every source we
checked**, not things we didn't get around to writing. Screw sizes, spring rates and magnet
dimensions are all in that category. We flag them rather than guess on purpose, because a
confident wrong number is worse than an admitted gap.

If you work one of them out while building, please open an issue. Closing those gaps is most of
what this project is for.
