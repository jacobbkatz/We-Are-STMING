# We-Are-STMING
We Are STMing — 3D-Printed Scanning Tunneling Microscope

A low-cost, 3D-printed Scanning Tunneling Microscope (STM), built from open-source designs and documented for builders with no prior electronics or soldering experience.

This project combines two open-source lineages:

Mech Panda's red-panda-stm — 3D-printed mechanics, firmware, and controller PCB design
Dan Berard's home-built STM — scan head, tip preparation, and preamplifier design

The goal is a fully open, reproducible STM that anyone with a 3D printer and basic tools can build, verify, and understand end to end.

Status

🚧 Actively in progress. Currently finishing PCB assembly and hand-wiring. First tunneling current expected soon.

Hardware Overview
System	Details
Frame	3D-printed in PETG-CF for stiffness and dimensional stability. PA-CF was tried first for its lower thermal expansion, but proved too difficult to print reliably at the tolerances this design needs.
Vibration isolation	Platform suspended on tension springs, with eddy-current damping — an aluminum plate moving through fixed magnets, no contact.
Coarse approach	28BYJ-48 stepper motor driven through a ULN2003 driver board.
Scanner	Piezoelectric disc actuator with a cut tungsten tip (0.25 mm wire, cut at 45°).
Preamplifier	OPA627-based transimpedance amplifier with a 100 MΩ feedback resistor, mounted close to the tip to preserve the picoamp-level tunneling signal. Connected to the tip via short, thin coaxial cable (RG-178).
Controller	Teensy 4.1, driving four AD5761 DACs (X, Y, Z, and sample bias) over SPI, and reading tunneling current via an LTC2326-16 ADC on a second SPI bus.
Assembly options	Available as a hand-wired protoboard build or a custom fabricated controller PCB, connected via a 26-pin ribbon cable.
Power	±15 V dual-rail supply for the analog electronics.
What's in This Repo
Assembly manual — step-by-step build instructions, written for beginners, with verified wiring diagrams and pinout tables
Wiring reference — Teensy pin maps and ribbon cable pinouts, cross-checked against both the firmware source and the PCB's manufacturing netlist (not guessed or assumed)
Firmware — based on the red-panda-stm control code (Teensy 4.1 / PlatformIO)
PCB design files — controller board and preamplifier board Gerbers
Parts and tools list — including notes on what's genuinely unspecified in the original designs (exact fastener sizes, spring rate, magnet dimensions), flagged rather than guessed
Why This Design

This build follows the philosophy of both source projects: get real atomic-resolution imaging out of a machine built primarily from a 3D printer, off-the-shelf electronics, and hand soldering, without requiring a machine shop or specialized fabrication.

Everything here is documented so someone with no prior STM, electronics, or soldering background can follow it — including the reasoning behind each part choice, not just the instructions.

Acknowledgments

This project would not exist without the prior open-source work of:

Dan Berard — dberard.com/home-built-stm
Mech Panda — red-panda-stm

Thank you also to Dr. Percy Zahl (Brookhaven National Laboratory, CFN) for guidance on vibration isolation and scan head design.

Contributing

This is an active build log as much as a finished project. Corrections, suggestions, and questions are welcome, especially from anyone who has built a similar instrument. Open an issue or reach out directly.
