# PCB design files

Archives, so you can see what is in each without downloading it.

| File | Contains |
|---|---|
| `Altium_Scanning Tunneling Microscope_2023-11-04.zip` | Altium source for the controller board — ADC, connectors, DAC and power schematic sheets |
| `PDF_Scanning Tunneling Microscope_2023-11-04.zip` | The same schematics as PDF. **Start here if you just want to read the circuit** |
| `STMP_easyEDA.zip` | EasyEDA project for the controller board |
| `preamp_rev2/` | **KiCad 10 project for preamp rev 2**, made by Nuh 2026-10-13 from Berard's Eagle board. **UNTESTED** — its gerbers and the full account are in [`../gerbers/README.md`](../gerbers/README.md). Open `preamp_rev2..kicad_pro` in KiCad 10 (the double dot is in the project's name; KiCad needs all three files named alike). The schematic file is empty: only the board was imported. `LICENSE_Berard_MIT.txt` travels with it because the layout is his |

Manufacturing files are in [`../gerbers/`](../gerbers/). Verified pinouts, LED meanings, the power
tree and the output stage are in [`../docs/WIRING.md`](../docs/WIRING.md) — use that rather than
re-deriving them from the schematic.

The preamplifier is a separate board. Its Eagle source ships inside
`We-Are-STMING_PCB.zip` in the repository root, under `preamplifier/eagle/`, and is
**MIT licensed** by its original author.
