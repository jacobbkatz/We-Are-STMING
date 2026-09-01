# Manufacturing files

Send these to a board house.

| File | Board | Notes |
|---|---|---|
| `Gerber_PCB1_all_red.zip` | **Controller** | 15 files: copper, silkscreen, mask, paste, outline, drill, plus flying-probe test data |
| `STM_Preamp_OPA627_Gerbers(1).zip` | **Preamplifier** | 11 files. 20.625 × 15.23 mm, 2-layer |

We paid **$321.44 for 5 assembled controller boards** at JLCPCB in 2026, about $64 each.

## Two things about the preamp board

**The 100 MΩ feedback resistor is not on the board.** The R2 footprint has **no copper at all**,
just bare drilled holes. That is deliberate — at picoamp currents, leakage across the board
surface would swallow the signal, so the input node is built in the air on a PTFE standoff.

**PAD1 is the amplifier output, not the tip input.** It is wired to the op-amp's pin 6. Solder the
tip there and the microscope will never see a tunneling current. See
[`../docs/WIRING.md`](../docs/WIRING.md) section 10.

## Through-hole parts are not placed

JLCPCB does not fit them. Even on an assembled controller board you solder these yourself: the
OPA2227P and LT1469IN8 op-amps, both TO-220 regulators, both DB9 sockets, the JST XH power header
and the 26-pin box header. Buy DIP-8 sockets rather than soldering the op-amps in directly.
