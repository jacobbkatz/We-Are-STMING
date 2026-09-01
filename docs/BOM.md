# Bill of Materials

Everything we needed to build the microscope, roughly in the order we bought it.

**How to read this.** Parts marked **CONFIRMED** come from a design file, a datasheet, or a label
we could read. Parts marked **CHOICE** are ones the original designers never specified, so I've
given what we went with. Parts marked **UNKNOWN** aren't documented anywhere that we could find,
and you'll have to measure or decide yourself.

Prices are indicative. Nothing here is affiliate linked.

---

## 1. Controller PCB, assembled parts

**CONFIRMED.** I pulled this straight out of the JLCPCB assembly BOM: 116 components across 28
line items. If you order the board assembled, all of this arrives populated except the
hand-solder parts in section 2.

### Integrated circuits

| Ref | Part | Package | Qty | What it does |
|---|---|---|---|---|
| U1 to U4 | **AD5761RBRUZ** | TSSOP-16 | 4 | 16-bit DACs for X, Y, Z and bias |
| U15 | **LTC2326HMS-16** | MSOP-16 | 1 | 16-bit ADC, reads the tunneling current |
| U5 | **ADR421BRZ** | SOIC-8 | 1 | Precision voltage reference |
| U9, U10, U13 | **OPA2227P** | PDIP-8 | 3 | Dual op-amps, signal conditioning |
| U21 | **LT1469IN8** | PDIP-8 | 1 | Dual op-amp |
| U16 | **BD733L5FP-CE2** | TO-252 | 1 | 3.3 V regulator |
| U17 | **SL7815** | TO-220 | 1 | **+15 V** regulator |
| U18 | **L7915CV** | TO-220 | 1 | **-15 V** regulator |
| U22 | **MC7805CDTG** | DPAK | 1 | 5 V regulator |

> **On the ADC.** The firmware visible on screen in Mech Panda's video reads `LTC2328`. The BOM and
> the board we received are **LTC2326**. We're trusting the BOM, since that's the chip physically
> on the board and the repo's library is `LTC2326_16`.

### Passives

| Value | Package | Qty | Part |
|---|---|---|---|
| 100 nF | 0603 | 25 | CL10B104KA8NNNC |
| 10 uF | 0603 | 14 | GRM188R61E106MA73D |
| 4.7 nF | 0603 | 7 | 0603B472K500NT |
| 3.3 nF | 0603 | 4 | CL10B332KB8NNNC |
| 2.2 uF | 0603 | 2 | CL10A225KO8NNNC |
| 0.33 uF | 0603 | 2 | FCC0603B334K500CT |
| 1 uF | 0603 | 2 | CL10A105KB8NNNC |
| 4.7 uF | 0603 | 1 | CL10A475KO8NNNC |
| 100 uF | SMD can | 1 | F931D107MNC |
| 47 uF | 1210 | 1 | CS3225X7R476K100NRL |
| 3 kohm | 0603 | 16 | ARG03DTC3001 |
| 10 kohm | 0603 | 7 | 0603WAF1002T5E |
| 220 ohm | 0603 | 5 | ERJU3RD2200V |
| 470 ohm | 0603 | 4 | 0603WAF4700T5E |
| 100 ohm | 0603 | 1 | 0603WAF1000T5E |
| Red LED | 0603 | 6 | 19-217/R6C-AL1M2VY/3T |

### Connectors on the board

| Ref | Part | Qty | Notes |
|---|---|---|---|
| H1 | 26-pin box header, 2x13 | 1 | Ribbon to the Teensy |
| DSUB1, DSUB2 | **RDED-9SE-LNA(4-40)** | 2 | DB9 sockets for scanner and preamp |
| U19 | **B3B-XH-AM** | 1 | **JST XH 3-pin, this is the power input** |

> **U19 is a JST XH 3-pin connector.** This answers a question we had open for a while: what
> actually plugs into the power input. You want a **JST XH 3-pin female housing with crimped
> leads**, sold as pre-made pigtails for a couple of dollars. Pin 1 is V--, pin 2 is ground, pin 3
> is V++.

**Cost.** The BOM file records **$321.44 for 5 assembled boards** at JLCPCB in 2026, so about $64
each.

---

## 2. Hand-soldered parts, check this section

JLCPCB doesn't place through-hole parts. Even on an assembled board, you solder these yourself:

| Ref | Part | Package |
|---|---|---|
| U9, U10, U13 | OPA2227P | PDIP-8 |
| U21 | LT1469IN8 | PDIP-8 |
| U17, U18 | SL7815, L7915CV | TO-220 |
| DSUB1, DSUB2 | DB9 sockets | through-hole |
| U19 | JST XH header | through-hole |
| H1 | 26-pin box header | through-hole |

Buy **four DIP-8 sockets** rather than soldering the op-amps straight in. They cost pennies, they
keep soldering heat off the chip, and they let you swap a dead op-amp without desoldering.

---

## 3. Preamplifier board

| Item | Spec | Qty | Status |
|---|---|---|---|
| PCB | 20.625 x 15.23 mm, 2-layer | 1 | CONFIRMED, Gerbers included |
| **Op-amp** | **OPA627AU**, SOIC-8 | 1 | CONFIRMED, Berard's design |
| **Feedback resistor** | **100 Mohm** | 1 | CONFIRMED value |
| Tantalum capacitor | 4.7 uF 35 V | 1 to 2 | CONFIRMED from a label we could read |
| **PTFE standoff terminal** | for a 2.1 mm hole | 1 | CHOICE, see below |
| 5-pin header | 2.54 mm pitch | 1 | for JP1 |

### About the 100 Mohm resistor

**It doesn't come on the board**, and the R2 footprint has **no copper at all**, just bare drilled
holes. That's deliberate. At picoamp currents, leakage across the board surface would swallow the
signal, so the input node gets built **in the air** instead.

You'll need:

- a **100 Mohm resistor**. Search DigiKey or Mouser for "100 Mohm resistor". Through-hole axial is
  easiest to air-wire. Berard's library caches an `HMC0603JT100M` (0603 chip) as a lead, but the
  through-hole version is much easier to work with here.
- a **PTFE standoff terminal**. Search "PTFE standoff terminal" or "Teflon insulated turret". It's
  a metal post in an insulating body that press-fits the bare hole and holds the junction off the
  board. Keystone make them. Buy two or three.

**PAD1 is the amplifier output, not the tip input.** The tip wire goes to the standoff.

---

## 4. Microcontroller and motor

| Item | Spec | Qty | Status |
|---|---|---|---|
| **Teensy 4.1** | PJRC | 1 | CONFIRMED |
| Protoboard | about 70 x 90 mm | 1 | CHOICE, our enclosure is sized for this |
| Female header strips | 2.54 mm | 2 | for plug-in breakouts |
| **Stepper motor** | **28BYJ-48, 5 V** | 1 | CONFIRMED, label photographed |
| **Driver board** | **ULN2003** module | 1 | CONFIRMED |
| Ribbon cable | 26-conductor, 1.27 mm | 1 | CONFIRMED |
| IDC connectors | 2x13, 26-pin | 2 | to crimp on the ribbon |
| Dupont jumper wires | assorted | 1 pack | motor driver to Teensy |
| USB micro-B cable | data capable | 1 | Teensy to computer |

> Get a **data** USB cable, not a charge-only one. This wastes more beginner hours than anything
> else on this list.

---

## 5. Scanner and tip

| Item | Spec | Qty | Status |
|---|---|---|---|
| **Piezo buzzer disc** | about 25 to 27 mm brass, 15 to 17 mm ceramic | 5+ | CONFIRMED size, part number UNKNOWN |
| **Tungsten wire** | **0.25 mm high purity**, 1 m | 1 | CONFIRMED from packaging |
| **Magnet wire** | enamelled, ultra-fine, 0.05 to 0.1 mm | 1 spool | CONFIRMED as "ultra-fine" |
| **Low-temp solder paste** | **Sn42/Bi58, about 138 C** | 1 syringe | CONFIRMED as low-temp |
| Miniature coax | **RG-178** or RG-316 | about 1 m | CHOICE, never specified |
| **Sample, mounted HOPG** | **PACS-0200 / 00-601-0104** | 1 | CONFIRMED from a photographed label |

> **Buy at least five piezo discs.** The original designer destroyed 4 or 5 by overheating them
> before he got one working. They cost cents. The low-temp paste plus ultra-fine wire is what
> fixed it, because fine wire has almost no thermal mass, so the joint forms before heat reaches
> the ceramic.

---

## 6. Mechanical hardware

| Item | Spec | Qty | Status |
|---|---|---|---|
| **Fine-adjust screws** | **McMaster 97424A590**, 1/4"-80, 1" long | 3 | CONFIRMED from CAD metadata |
| **Brass inserts** | **McMaster 98625A960**, 0.438" long, for 1/4"-80 | 3 | CONFIRMED from CAD metadata |
| **Threaded rod** | **M8 x 1.25** | 3 | CONFIRMED from CAD part name |
| **Spring top caps** | **M20 x 2** thread | 3 | CONFIRMED from CAD part name |
| **Extension springs** | about 300 mm | 3 | CONFIRMED length, rate UNKNOWN |
| Preload springs | small extension springs | 3 | for the scan head plates |
| **Damping magnets** | rectangular | **18** | CONFIRMED count, size UNKNOWN |
| Disc magnets | small, for the sample pocket | 4 | CONFIRMED count, size UNKNOWN |
| Aluminium plate | for eddy-current damping | 1 | thickness UNKNOWN |
| Heat-set inserts | brass, for PA-CF or PETG-CF | about 10 | sizes UNKNOWN |
| M3 screws | assorted 8 to 16 mm | about 30 | enclosures and plates |
| M2 screws | 6 to 8 mm | about 8 | **preamp box only** |
| M3 nuts and washers | | about 20 | |

> The 1/4"-80 thread is the whole trick behind the approach mechanism. **80 threads per inch means
> one full turn advances only 0.0125 inches**, which is what lets you approach by hand without
> crashing the tip.

---

## 7. Shielding and consumables

| Item | Spec | Notes |
|---|---|---|
| **Copper tape** | about 50 mm wide, **conductive adhesive** | use this anywhere you need to solder a ground wire |
| Aluminium tape | about 50 mm wide | cheaper for covering area, **can't be soldered** |
| Solder | 63/37 rosin core, 0.6 to 0.8 mm | everything except the piezo |
| Flux | no-clean, pen or tub | |
| Isopropyl alcohol | 99% | cleaning before building the preamp input |
| Foam block | open-cell | supports the wire loops crossing to the isolated stage |
| PETG-CF filament | about 1 kg | see section 10 |

> **Copper and aluminium tape are not interchangeable.** Copper takes solder, so you can bond a
> ground wire straight to it. Aluminium can't be soldered because of the oxide layer, and its
> adhesive is usually non-conductive, so overlapping strips may not even connect to each other.
> Use copper anywhere that needs a ground connection.

---

## 8. Power supply

| Item | Spec | Status |
|---|---|---|
| Bench supply | **dual adjustable output**, at least +/-18 V, about 500 mA | CHOICE |
| 5 V source | for the motor driver | CHOICE, Teensy VIN works |
| JST XH 3-pin pigtail | to mate with U19 | CONFIRMED connector type |

The regulators need input above their output, so feed **V++ and V-- at roughly +/-18 V**, not
+/-15 V. The +/-15 V appears on J2 as an **output** to the preamplifier.

**A single-output supply can't do this.** You need two independently adjustable channels, or two
separate supplies stacked in series with the junction as ground.

---

## 9. Tools

| Tool | Notes |
|---|---|
| Temperature-controlled soldering iron | fine tip, and the temperature control genuinely matters for the piezo |
| **Multimeter with continuity beep** | the most useful tool in this whole build |
| Fine flush cutters | for cutting the tungsten tip |
| Tweezers | fine tipped |
| Wire strippers | down to 30 AWG |
| 3D printer | Mech Panda used a Bambu X1C, anything that handles PETG-CF works |
| Calipers | for checking printed parts |
| Oscilloscope | **optional**, a multimeter is enough to get running |

---

## 10. 3D printing

**We used PETG-CF.** Mech Panda used PA-CF, but we tried it first and couldn't print it reliably at
these tolerances, so we settled on PETG-CF as the practical middle ground. It's stiff and
dimensionally stable and prints without a hardened chamber.

**Don't use plain PLA.** It creeps under sustained load and moves with temperature, and that shows
up directly as drift in your images.

Budget roughly 500 to 800 g of filament for the full set of parts.

---

## What we still don't know

These aren't oversights. They aren't stated in any source we could find, and guessing would be
worse than admitting it:

- Plate-to-plate and motor-mount screw sizes
- Spring rate, though we know the length is 300 mm
- Individual magnet dimensions, though we know there are 18
- Piezo disc part number and supplier
- The adhesive bonding the piezo disc to its plate
- Coax type and length
- Iron temperature and dwell time for the piezo joints

If you work any of these out while building, please open an issue. Closing those gaps is most of
what this project is for.
