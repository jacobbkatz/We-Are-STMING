# We-Are-STMING

**We Are STMing — 3D-Printed Scanning Tunneling Microscope**

A low-cost, 3D-printed Scanning Tunneling Microscope (STM), built from open-source designs and
documented for builders with no prior electronics or soldering experience.

This project combines two open-source lineages:

- **Mech Panda's `red-panda-stm`** — 3D-printed mechanics, firmware, and controller PCB design
- **Dan Berard's [home-built STM](https://dberard.com/home-built-stm/)** — scan head, tip
  preparation, and preamplifier design

The goal Nuh Shaheer and I share is a reproducible STM that anyone with a 3D printer and basic
tools can build, verify, and understand end to end.

---

## Status

**Actively in progress.** Bring-up stages 0 through 5 pass, and the sample bias path passes. The
preamplifier is currently the blocker and is being rebuilt.

**[`STATUS.md`](STATUS.md) is the live state of the build** — always current, rewritten at the end
of every work session. Read that rather than this paragraph, which will go stale.

---

## Start here

| If you want to | Read |
|---|---|
| Know where the build is right now | [`STATUS.md`](STATUS.md) |
| Build one yourself | [`docs/START_HERE_gotchas.md`](docs/START_HERE_gotchas.md), then [`docs/BOM.md`](docs/BOM.md) |
| Set up a computer to work on this | [`SETUP.md`](SETUP.md) |
| Follow the bring-up tests | [`docs/soft_launch_test_procedure.md`](docs/soft_launch_test_procedure.md) |
| Wire something up, or check a pinout | [`docs/WIRING.md`](docs/WIRING.md) |
| Send a command to the board | [`docs/COMMANDS.md`](docs/COMMANDS.md) |
| Help us close a gap | [`docs/OPEN_QUESTIONS.md`](docs/OPEN_QUESTIONS.md) |
| See what happened in past work sessions | [`sessions/`](sessions/) |

**`docs/START_HERE_gotchas.md` is not optional if you are building one.** Several of the things in
it cost real hardware if you get them wrong — including which pad the tip goes to, and which
connector is a power input rather than an output.

---

## Hardware overview

| System | Details |
|---|---|
| Frame | 3D-printed in PETG-CF for stiffness and dimensional stability. PA-CF was tried first for its lower thermal expansion but proved too difficult to print reliably at these tolerances. **Not PLA** — it creeps, and that shows up directly as drift |
| Vibration isolation | Platform suspended on tension springs, with eddy-current damping — an aluminium plate moving through fixed magnets, no contact |
| Coarse approach | 28BYJ-48 stepper motor through a ULN2003 driver board, wired directly to the Teensy |
| Scanner | Piezoelectric disc actuator with a cut tungsten tip, 0.25 mm wire cut at 45° |
| Preamplifier | OPA627-based transimpedance amplifier with a 100 MΩ feedback resistor, mounted close to the tip to preserve the picoamp-level tunneling signal |
| Controller | Teensy 4.1 driving four AD5761 DACs over SPI — X, Y and sample bias at ±3 V, Z at ±10 V — and reading tunneling current via an LTC2326-16 ADC on a second SPI bus |
| Power | ±18 V in to the controller board, which generates the ±15 V rails it sends out to the preamplifier |

---

## Repository layout

```
STATUS.md      Live state of the build. Read this first
CLAUDE.md      Working protocol, followed automatically by Claude Code
SETUP.md       How to set up a computer to work on this project
sessions/      One log per work session, newest supersedes older
docs/          Gotchas, BOM, wiring, commands, and project history
Code/teensy/   Teensy 4.1 firmware (PlatformIO)
Code/pc/       Python tools that talk to the board over serial
CAD/           Fusion 360 source
PCB/           Controller board design files
gerbers/       Manufacturing files for the controller and preamp boards
our_preamp_cad_files/   Our preamp enclosure
```

---

## How we work on this

This is built by two people on two computers, both using Claude Code, with **GitHub as the single
source of truth.** Each session pulls the latest state at the start and pushes back at the end, so
neither machine works from stale findings. The protocol is in [`CLAUDE.md`](CLAUDE.md); the
one-time setup is in [`SETUP.md`](SETUP.md).

That matters more here than it sounds. Several findings in this project were later proven wrong,
and acting on a superseded one has already cost hardware time. `STATUS.md` and the dated session
logs exist so that the newest correction always wins.

---

## Why this design

This build follows the philosophy of both source projects: get real atomic-resolution imaging out
of a machine built primarily from a 3D printer, off-the-shelf electronics, and hand soldering,
without requiring a machine shop or specialised fabrication.

Everything here is documented so someone with no prior STM, electronics, or soldering background
can follow it — including the reasoning behind each part choice, not just the instructions. Where
something genuinely isn't documented in any source we could find, it is marked **UNKNOWN** or
**VERIFY** rather than guessed. A confident wrong number is worse than an admitted gap.

---

## Acknowledgments

This project would not exist without the prior open-source work of:

- **Dan Berard** — [dberard.com/home-built-stm](https://dberard.com/home-built-stm/)
- **Mech Panda** — `red-panda-stm`

Thank you also to Dr. Percy Zahl (Brookhaven National Laboratory, CFN) for guidance on vibration
isolation and scan head design.

---

## Contributing

This is an active build log as much as a finished project. Corrections, suggestions and questions
are welcome, especially from anyone who has built a similar instrument.

The **What we still don't know** section of [`docs/BOM.md`](docs/BOM.md) and the open questions in
[`STATUS.md`](STATUS.md) are the most useful places to help. If you work one of them out while
building, please open an issue — closing those gaps is most of what this project is for.
