# STM v2 at UCSD: procurement budget (lean scenario)

Prepared for Prof. Oscar Vasquez, 2026-10-21. Prices checked 2026-10-21, USD. The spreadsheet `STM_v2_budget.xlsx` has the live formulas; `STM_v2_budget.pdf` is a printable copy.

## Summary

This is the lean purchase list for a second STM, built at UCSD. Its target is atomic resolution on HOPG in air, and its minimum bar is stable tunnelling. It rests on four assumptions:

- UCSD labs supply the Pt/Ir tip wire and the HOPG.
- The whole structure is 3D printed, with no machining.
- The electronics repeat v1's JLCPCB order: two controller boards and two preamps, fully placed.
- Money goes only to what a lab doesn't readily have: the piezo and its driver, batteries and other specialty parts.

**Total: $2,018.69, which is $18.69 over the $2,000 ceiling.** That includes shipping, tariffs, 7.75% tax and a 10% contingency. The 35% tariff on the JLCPCB order is the largest single add-on.

**Using steel balls instead of sapphire for the slider contacts brings the total to $1,907.24, under the ceiling.**

The earlier full-build scenario came to $3,006.93, or $2,626.74 after its cuts. It assumed metal, machining, and buying the tips and HOPG. It is not included here.

Of the $1,227.07 in parts:

- $546.46 is current prices read from vendor or aggregator pages on 21 October.
- $491.24 is v1 invoice prices, almost all of it the JLCPCB repeat order.
- $189.37 is estimates, mostly the high-voltage driver, which isn't designed yet.

## Total build-up

| Line | Amount |
|---|---|
| Purchased components | $1,227.07 |
| Vendor shipping | $219.00 |
| Tariffs and import duties | $229.00 |
| Carrier import fee (PiezoDrive) | $65.00 |
| Sales and use tax (7.75%) | $95.10 |
| Subtotal | $1,835.17 |
| Contingency (10%) | $183.52 |
| **Total** | **$2,018.69** |
| With steel balls instead of sapphire | $1,907.24 |
| Screw drive instead of stick-slip (merchandise) | −$104.99 |
| Commercial PDu150 driver instead of DIY (merchandise) | +$727.08 |

## Purchases, with links

Every line links to where it would be bought. Four lines have no exact product page, for these reasons:

- **HV-02 transformer:** the link is a price placeholder for the wrong voltage.
- **HV-03 driver parts:** the circuit isn't drawn yet.
- **JLCPCB lines:** they link to the ordering site, since a custom PCB has no page until gerbers are uploaded.

| ID | Item | Vendor / link | Qty | Extended | Evidence |
|---|---|---|---|---|---|
| PZ-01 | Piezo tube scanner, 30 mm x 6 mm, quartered electrodes | [PiezoDrive](https://www.piezodrive.com/product/tb3006-n-29um-range-piezo-tube-scanner/) | 1 | $131.00 | Verified - vendor page |
| PZ-02 | Piezo stack for the stick-slip coarse approach | [PiezoDrive](https://www.piezodrive.com/product/150v-5x5x10mm-piezo-stack-actuator-sa050510/) | 1 | $68.00 | Verified - vendor page |
| HV-01 | High-voltage op-amp, one per channel (5 tube + 1 stick-slip + 1 spare) | [LCSC](https://www.lcsc.com/product-detail/C50636.html) | 7 | $47.07 | Verified - vendor page |
| HV-02 | Transformer for the +/-45-50 V rails | [Jameco](https://www.jameco.com/z/182M18-Hammond-Manufacturing-Toroidal-Transformer-120VA-50Hz-Dual-Secondary-36VCT-3-33A-Series-18V-6-66A-Parallel_2575671.html) | 1 | $67.85 | Estimated |
| HV-03 | Rectifier, filter caps, HV regulators, heatsinks, HV connectors | LCSC (no direct link) | 1 | $40.00 | Estimated |
| HV-04 | HV driver bare PCB (rides the JLCPCB order) | [JLCPCB](https://jlcpcb.com/) | 5 | $10.00 | Estimated |
| EL-01 | Controller board, fully assembled (v1 design) | [JLCPCB](https://jlcpcb.com/) | 2 | $419.28 | Historical - v1 receipt |
| EL-02 | Preamp board, fully assembled (rev 2 gerbers) | [JLCPCB](https://jlcpcb.com/) | 2 | $60.34 | Historical - v1 receipt |
| EL-03 | Bare controller PCBs (as in the v1 order) | [JLCPCB](https://jlcpcb.com/) | 3 | $5.04 | Historical - v1 receipt |
| EL-04 | Bare preamp PCBs (as in the v1 order) | [JLCPCB](https://jlcpcb.com/) | 3 | $2.40 | Historical - v1 receipt |
| EL-05 | Dual op-amp U21, bought separately in v1 alongside the JLCPCB order | [DigiKey](https://www.digikey.com/en/products/detail/analog-devices-inc/LT1469IN8-PBF/962892) | 2 | $36.52 | Estimated |
| EL-06 | Microcontroller | [SparkFun](https://www.sparkfun.com/teensy-4-1.html) | 1 | $31.50 | Verified - vendor page |
| PA-01 | 1 GOhm feedback resistor, soldered across the op-amp pins | [DigiKey](https://www.digikey.com/en/products/detail/ohmite/SM104031007FE/824190) | 2 | $11.46 | Verified - aggregator listing |
| PA-02 | PTFE standoff terminal for the air-wired input node | [DigiKey](https://octopart.com/part/keystone/11301) | 2 | $4.18 | Historical - v1 receipt |
| PA-03 | 9 V lithium batteries for the analog supply (two give +/-9 V) | [BatteryMart](https://www.batterymart.com/p-energizer-la522-9volt-lithium-battery.html) | 2 | $43.90 | Verified - vendor page |
| PA-04 | 9 V battery holder | [DigiKey](https://octopart.com/part/keystone/1294) | 2 | $5.98 | Verified - aggregator listing |
| PA-05 | Temperature sensor, +/-0.1 C (head and preamp) | [Adafruit](https://adafruit.com/product/4821) | 2 | $23.00 | Verified - vendor page |
| ME-01 | 3D-printing filament for head, sample plate and approach body | [Prusa Research](https://www.prusa3d.com/product/prusament-petg-carbon-fiber-black-1kg/) | 1 | $54.99 | Verified - vendor page |
| ME-02 | Sapphire balls as stick-slip contacts | [Edmund Optics](https://www.edmundoptics.com/p/20mm-diameter-sapphire-ball-lens/5174/) | 3 | $84.75 | Verified - vendor page |
| ME-03 | Precision-ground rod for slider guides | [OnlineMetals](https://www.onlinemetals.com/en/buy/tool-steel-drill-rod-w1) | 1 | $4.82 | Verified - vendor page |
| ME-04 | Hardened steel balls for kinematic pivots | [Walmart](https://www.walmart.com/ip/533082272) | 1 | $9.99 | Verified - vendor page |
| ME-05 | Magnetic stainless sample discs, 12 mm (HOPG carrier) | [Ted Pella](https://www.tedpella.com/AFM_html/AFM.aspx) | 1 | $30.00 | Verified - vendor page |
| ME-06 | Sorbothane isolation pads, 0.5 in, 50 duro, 6x6 in | [Isolate It](https://www.isolateit.com/products/sorbothane-acoustic-and-vibration-isolation-square-6-x-6-pads) | 1 | $35.00 | Estimated |

**Filament (ME-01).** One 1 kg spool of Prusament PETG-CF is priced at $54.99 from Prusa. MatterHackers lists the same spool at $89.99. Nylon-CF is the alternative, and the material choice is still open.

**JLCPCB.** These lines use v1's 2026-07-15 invoice prices. JLCPCB only quotes after the gerbers and BOM are uploaded, so the order couldn't be re-quoted from here. Part prices have moved since then. For example, the LT1469 is now $23.77 and out of stock at LCSC.

## Vendor orders

| Vendor | Merchandise | Order total (shipping, tariff, tax) |
|---|---|---|
| PiezoDrive | $199.00 | $294.32 |
| LCSC | $87.07 | $146.51 |
| Jameco | $67.85 | $81.11 |
| JLCPCB | $497.06 | $759.85 |
| DigiKey | $58.14 | $75.79 |
| SparkFun | $31.50 | $41.94 |
| BatteryMart | $43.90 | $53.30 |
| Adafruit | $23.00 | $30.78 |
| Prusa Research | $54.99 | $69.25 |
| Edmund Optics | $84.75 | $101.32 |
| OnlineMetals | $4.82 | $15.19 |
| Walmart | $9.99 | $10.76 |
| Ted Pella | $30.00 | $44.33 |
| Isolate It | $35.00 | $45.71 |
| Carrier import processing fee (PiezoDrive) | $0.00 | $65.00 |
| ALL ORDERS | $1,227.07 | $1,835.17 |

## In-kind and campus (not in the total)

| Item | Treatment | Reference value if bought |
|---|---|---|
| Pt/Ir tip wire | In-kind from a UCSD lab | $277.20 |
| HOPG sample | In-kind from a UCSD lab | $77.00 |
| Machining | Not needed | — |
| 3D printer time | Campus (assumed) | — |
| Granite base or optical breadboard | Campus (assumed) | $75.15 |
| Bench power supply (+/-15 V class) | Campus (assumed) | — |
| Oscilloscope, multimeter, soldering station, hot air | Campus (assumed) | — |
| Silver epoxy or silver paint for mounting HOPG | Campus (assumed) | $133.13 |
| Wire (40 AWG magnet wire, 30 AWG Kynar), coax, hook-up wire | Campus (assumed) | — |
| Connectors, headers, DIP sockets, ribbon/USB/DB9 cables | Campus (assumed) | — |
| Fasteners, springs, small magnets, BeCu or steel shim for clips | Campus (assumed) | — |
| Consumables: IPA, acetone, flux, solder, wipes, gloves, tape, copper tape | Campus (assumed) | — |
| Tools: flush cutters, tweezers, ESD strap | Campus (assumed) | — |
| Shield enclosures | Campus (assumed) | — |

## Unresolved

| ID | What is unknown | Effect | What would resolve it |
|---|---|---|---|
| U1 | **HV driver design**. Not drawn; only the op-amps are priced exactly | Could move +/-$50; commercial PDu150 modules instead add about $727 | Draw the schematic, then itemize with links |
| U2 | **JLCPCB price today**. Can't re-quote without uploading gerbers and BOM | Part prices have moved; likely +/-10% on $497 | Upload the v1 files to JLCPCB for a quote |
| U3 | **Campus items really free**. Printers, supply, scope, epoxy, wire, stock not confirmed | Bench supply ~$43+, epoxy $133 if a lab can't lend | Confirm with Prof. Vasquez's lab |
| U4 | **Printed structure vs Zahl's advice**. Zahl: no plastics in the mechanical loop | Metal parts would bring back machining or stock cost | Decide with the advisers; ceramic/metal inserts at the tip-sample loop |
| U5 | **Filament choice**. PETG-CF vs nylon-CF | Nylon-CF is similar or a bit more | Pick based on the campus printer |
| U6 | **Approach choice**. Stick-slip vs spring-preloaded screw | Steel balls instead of sapphire: -$84.75 | Decide with the advisers |
| U7 | **PiezoDrive shipping and duty**. No rate shown; DAP | +/- $50 | Ask PiezoDrive for a delivered quote |
| U8 | **Sorbothane price**. Variant price not displayed | +/- $10 | Check the cart |

## Notes

- **Zahl's advice.** Dr. Zahl advised against plastics in the mechanical loop. The printed structure goes against that, so it is flagged as U4.
- **Prof. Vasquez's suggestion.** The tube piezo is his suggestion, not a confirmed diagnosis of v1's instability.
- **What v1 cost.** v1 actually cost $1,375.93 across 47 purchases.
- **Sites that couldn't be reached:**
  - DigiKey, Mouser and McMaster block this environment, so their prices come from aggregator listings.
  - Thorlabs and Amazon product pages didn't load.
  - The UCSD mailbox and the Amazon account used for v1 weren't reachable.

