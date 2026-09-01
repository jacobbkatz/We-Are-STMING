# PCB design files

Archives, so you can see what is in each without downloading it.

| File | Contains |
|---|---|
| `Altium_Scanning Tunneling Microscope_2023-11-04.zip` | Altium source for the controller board — ADC, connectors, DAC and power schematic sheets |
| `PDF_Scanning Tunneling Microscope_2023-11-04.zip` | The same schematics as PDF. **Start here if you just want to read the circuit** |
| `STMP_easyEDA.zip` | EasyEDA project for the controller board |

Manufacturing files are in [`../gerbers/`](../gerbers/). Verified pinouts, LED meanings, the power
tree and the output stage are in [`../docs/WIRING.md`](../docs/WIRING.md) — use that rather than
re-deriving them from the schematic.

The preamplifier is a separate board. Its Eagle source ships inside
`We-Are-STMING_PCB.zip` in the repository root, under `preamplifier/eagle/`, and is
**MIT licensed** by its original author.
