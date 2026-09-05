# Notes from Dan Berard's build

Reference notes taken from [dberard.com](https://dberard.com/home-built-stm/), September 2026.

**Our build is Mech Panda's `red-panda-stm`, not Berard's.** The preamplifier is the one part we
take from him. Everything here is **context and cross-reference**, not copied design — his
electronics, microcontroller and scan head geometry are all different from ours.

Read the applicability column before acting on any number.

---

## 1. The two things that changed our firmware assessment

### 1.1 Engaging the feedback loop crashes the tip. We have this bug.

Berard, on his coarse approach page:

> When the Z-feedback is switched on, the integral term first must be initialized to the current
> Z-value. Otherwise, the feedback will cause a small jump in the Z-piezo when it's switched on,
> **which crashes the tip!** Took me a while to figure out why I was still seeing craters in my
> scans!

**We have exactly this bug.** In `stm_firmware.hpp`:

```cpp
void turn_on_const_current(int target_adc) {
    this->dac_z_control_value = static_cast<double>(stm_status.dac_z);  // assigned...
    pTerm = 0.0;
    iTerm = 0.0;
}
int control_current(int adc_value) {
    ...
    int z = static_cast<int>(pTerm + iTerm) + 32768;   // ...never used. 32768 is hardcoded
```

`dac_z_control_value` is written and **never read anywhere in the codebase.** The output is
computed from a hardcoded midscale instead. So the first `control_current()` call after `CCON`
drives Z to approximately 32768 **regardless of where Z actually was.**

**Scale of the jump.** If Z sat at 15000 when you engage, that is a ~17000-count step. Using
Berard's measured 34 nm/V on a disc scanner over our ±10 V Z range, one count is roughly 0.01 nm,
so that is a **~180 nm lurch toward the sample**. Tunneling happens below 1 nm. The tip does not
survive that.

**Fix, not yet applied:** initialise `iTerm` so the loop's first output equals the current Z.
Concretely, seed `iTerm = stm_status.dac_z - 32768` in `turn_on_const_current()`, or use
`dac_z_control_value` as the output offset instead of the hardcoded constant. **Needs bench
testing before it is trusted.**

> **Operating rule until this is fixed: park Z where you want the loop to start before sending
> `CCON`, and expect a jump to midscale on engage. Do not send `CCON` with a tip in tunneling
> range.**

### 1.2 The motor stays energised, and that heats the scan head

Berard:

> The motor produces a substantial amount of heat, which can cause the scanner to **drift out of
> range within minutes**. The solution is simply to turn the motor off when it's not moving... I'm
> also running the motor on 3.3 V rather than 5 V to further reduce heating.

**Our firmware leaves all four coils driven after every move.** `EfficientStepper::step()` calls
`enable()` and never disables afterwards. `disable()` is called in exactly one place — inside
`approach()`, and only on success. So after any `MTMV`, the motor sits energised and warming until
something else disables it.

**Fix, not yet applied:** call `disable()` at the end of `step()`, or after each `MTMV`. This
motor is geared, so it holds position without holding current — that is the whole reason a geared
motor was chosen. **Needs bench testing.**

This is a strong candidate explanation if drift ever appears minutes into a session.

---

## 2. Coarse approach — the "woodpecker" method

Berard's sequence, and the reason it is safe:

1. Extend the Z-piezo slowly, searching for the surface.
2. Not found → fully retract Z.
3. Motor takes a few steps, moving **less than the Z-piezo travel**.
4. Repeat until the piezo finds the surface.
5. On contact, retract once more, then position so the surface sits near the **centre** of Z
   travel, leaving room to drift either way.

> **Only the Z-piezo ever closes the gap. The motor and the scanner never move at the same time.**
> That is what stops motor vibration from crashing the tip.

**Our `approach()` already implements this shape** — it steps the motor, then sweeps
`z_value` from 10000 to 50000 checking the ADC each step. That part is right.

What is still wrong with ours is the trigger, not the strategy: `read_adc() > target` is a
**signed** comparison against a baseline that has been negative all project. See `STATUS.md`.

### Step size — this changes our risk picture substantially

Berard: *"The fine screw moves 250 µm/revolution, and the STM body's lever reduction reduces the
motion by a factor of about 20. This gives a step size of 250 µm / 2048 / 20 = 6 nm."*

And in a comment, the geometry behind that factor of 20:

> The rear approach screw is 20 mm away from the scanner, and the two front screws are ~1 mm away
> along the front-to-rear axis, so the tip is moved ~20× less than the rear screw when the rear
> screw is turned.

That is the ordinary 3-screw lever: turn one screw, and the tip moves by the ratio of its distance
from the pivot line to the driven screw's distance.

**Applied to our numbers**, with the 1/4"-80 screws from `BOM.md`:

| | |
|---|---|
| 1/4"-80 pitch | 25.4 mm / 80 = **317.5 µm per revolution** |
| 28BYJ-48 | **2048 steps/rev**, measured on our unit |
| At the screw | 317.5 / 2048 = **155 nm per step** |
| **At the tip, if our lever ratio is also ~20** | **≈ 7.8 nm per step** |

**Compare this against the old estimate.** `sessions/2026-08-31-plan.md` guessed 244 nm/step from
an assumed M3 screw, against a ~1 µm Z range — about four steps per Z range, described at the time
as "tight". If the lever is real, we have roughly **90 steps per Z range** instead. That is the
difference between an approach with almost no margin and one with plenty.

> **VERIFY: our lever ratio is not measured.** Berard's ~20 comes from *his* scan head. Ours is
> Mech Panda's geometry. The screw positions are measurable from `CAD/prints/scan-head/` — the
> ratio is (distance from the front screw line to the tip) ÷ (distance from the front screw line
> to the rear screw). Even with no lever at all, 155 nm/step against a ~700 nm Z range is workable.

**Note a small inconsistency in Berard's own figures:** he says the fine screw moves 250 µm/rev,
but elsewhere confirms the screws are 1/4-80, which is 317.5 µm/rev. His 250 µm may be a different
screw or a rounding. We use the pitch arithmetic rather than his figure.

---

## 3. Scanner travel, for sizing scans

Berard calibrated his disc scanner against known atomic spacings:

| Axis | His figure | Over |
|---|---|---|
| Z | **~670 nm**, or **34 nm/V** | ~20 V |
| XY | **~1670 nm**, or **83 nm/V** | ~20 V |

Resonance ~3.4 kHz for his disc.

**What that implies for us**, treating his nm/V as a rough guide for a similar buzzer disc —
**inference, not measurement**:

| Our axis | Our range | Implied travel |
|---|---|---|
| Z, ±10 V | 20 V | **~680 nm** |
| X and Y, ±3 V | 6 V | **~500 nm** |

Our X/Y travel is about a third of his, because our DACs are configured for ±3 V while he drives
±10 V. Worth knowing before anyone is disappointed by the scan size. It is a resistor-and-range
choice, not a limitation of the disc.

---

## 4. Preamplifier

**Berard's original is an OPA124, not an OPA627.** From his electronics page:

> The preamplifier is an OPA124 op-amp with a 100 MΩ feedback resistor configured as a
> transimpedance amplifier... I chose the OPA124 for its low input bias current and low current
> noise. There are many others that would also work well: **OPA627 seems to be a popular choice in
> STM**; OPA129 would be good for measurements at very low currents.

So our OPA627 is a substitution Berard explicitly endorses, but `BOM.md` describing OPA627AU as
"Berard's design" overstates it. Corrected there.

Input bias current on the OPA124 is around **1 pA**. That is the scale the input node has to beat.
Our measured 37 nA offset is roughly **thirty thousand times** that.

### The PTFE standoff — now a real part number

> I've insulated the input node with a teflon standoff (**Keystone Electronics 11301**) and bent
> the op-amp's input pin off the surface of the PCB.

That closes a `CHOICE` item in our BOM, which previously said only "search for a PTFE standoff
terminal".

### A third candidate for our 37 nA

> I'm also using a guard ring on my preamp now, just **make sure to clean all the flux off the
> board after soldering or you might get huge leakage currents!**

Berard independently reports flux residue producing large leakage on this exact circuit. That sits
alongside our cyanoacrylate and floating-shield hypotheses. All three are surface conduction into
the input node, and **none of them is excluded by anything we have measured.**

The practical consequence is the same either way: whatever else is done, the input node area needs
a proper clean, and the 2026-08-31 rebuild rules already require a fresh IPA wash and second rinse.

### Shielding — independent support for the current plan

> I place a metal can over the STM during scanning to shield the tip and preamp. **Without the
> shield, the images produced by the STM are dominated by 60 Hz noise pickup.**

Shielding is part of his working design, not a refinement. Consistent with our 2026-08-31
measurement that a person within a metre injects 20–50 nA.

### Wiring to the tip — he does not use coax

> A short **40 AWG** wire connects the STM tip to the preamp input.

And for vibration isolation:

> I also use very fine 40 AWG wires to connect the scanner, preamplifier and sample bias to the
> electronics... to minimize vibration transmission.

Our BOM lists RG-178 or RG-316 coax as a `CHOICE` that "was never specified upstream". It now
appears upstream **did** specify, and chose plain 40 AWG wire — partly because stiff cable
transmits vibration. Berard's words: *"Ribbon cables are floppy and should help with vibration
isolation somewhat. Stiff cables are like mechanical antennas."*

Coax buys shielding on the input line; fine wire buys mechanical isolation and lower capacitance.
Recorded as a genuine design fork, not corrected in our BOM, since we have not tested either.

---

## 5. Sample mounting — relevant now that we are using gold foil

Berard's sample stage, from a comment:

> There's a piece of thin glass (microscope coverslip) glued to the aluminium base of the STM to
> insulate the sample from the grounded base. There's a steel nut glued on top of that as a
> spacer, and a magnet glued on top of that. The bias wire is soldered directly to the magnet.
> **Make sure to use a nickel-plated NdFeB magnet and make the solder joint quickly to avoid
> depoling the magnet.**
>
> To mount a sample, I glue it to a magnetic disc or coin and use a small blob of **conductive
> ink** to make an electrical connection between the disc and the sample. Then just place it on
> the magnet. This way you can easily swap out samples.

**For gold foil specifically:** the sample must be electrically continuous with the bias wire, so
the foil needs a conductive path to the magnetic disc — conductive ink, silver paint, or copper
tape. It also needs to be **flat and firmly attached**; loose foil will move under the tip and
looks exactly like drift.

Berard imaged gold successfully and resolved atomic terraces, but notes he **could not resolve
individual atoms on metals**, attributing it to acoustic noise. Graphite was much easier because it
is atomically flat. That is worth knowing before judging our first gold images: **atomic terraces
are the realistic target, not individual atoms.**

---

## 6. Tips

> I've just been cutting my tips from a **30 AWG tungsten wire** with wire cutters. The technique
> is to **pull the wire with a pair of pliers while cutting at an angle**... Since tungsten is
> harder than the wire cutters, the result isn't pretty, but does seem to work fine most of the
> time for atomic resolution on HOPG.

30 AWG is 0.255 mm, which matches the 0.25 mm tungsten wire in our BOM. Good confirmation.

Two things he adds:

- The cut-tip technique **gives mixed results for larger scans**, and works much better with
  **platinum iridium**, which is softer and more oxidation-resistant than tungsten.
- Electrochemical etching in **4 M KOH at 4 V** using the lamella technique gives much better tips,
  but leaves an oxide layer that is hard to remove.

Since we are moving to gold rather than HOPG, and gold is where he had the most trouble, **PtIr
wire is worth considering** if cut tungsten tips disappoint.

---

## 7. Things on his site that do NOT apply to us

Recorded so nobody wires our board from his page by mistake.

| His design | Ours |
|---|---|
| Teensy 3.1 | **Teensy 4.1** |
| DAC8814, 4-channel multiplying DAC, external REF102 reference | **Four AD5761 DACs**, ADR421 reference |
| His Teensy pin map (CS_DAC 20, LDAC 17, CS_ADC 21, CNV 4, BUSY 3) | **Completely different.** See `docs/WIRING.md` |
| Sigma-delta modulation to 20-bit effective resolution | Not implemented in our firmware |
| C# PC software | Our Python tools in `Code/pc/` |
| ±15 V piezo drive giving ~2 µm travel | Our Z is ±10 V, X/Y ±3 V |
| Analog PCB, his own layout | Mech Panda's controller board |

**One thing does match:** he also uses an **LTC2326-16** ADC, and a log lookup table for
linearising the tunneling current before the PI loop — the same approach as our `logTable.hpp`.
That is presumably where Mech Panda took it from.

He also drives **LED on pin 0 for serial activity and pin 1 for tunneling**. Our firmware defines
`SERIAL_LED 0` and `TUNNEL_LED 1` and never uses them — now we know why they exist.

---

## Attribution

Dan Berard's STM work is published at [dberard.com](https://dberard.com/home-built-stm/), © 2017
Daniel Berard. His preamplifier Eagle files are MIT licensed. This file is our reading notes for
cross-reference; the design we are building is Mech Panda's `red-panda-stm` with Berard's
preamplifier.
