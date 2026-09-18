# Console outputs not saved to a file at the time

Transcribed verbatim from the Claude Code desktop session, `sessions/2026-09-18-bench.md`.
Times are UTC. Sample at -0.5 V is `BIAS 38229`; +0.5 V is `BIAS 27307`; 0 V is `BIAS 32768`.
Counts are ADC counts, 320.5 counts per nA (`docs/FACTS.md`). `ADCR` is the firmware's averaged
read; `GSTS` field 5 is a single raw conversion.

## First power-up, touch check (about 01:05)

`GSTS`: all DAC fields 0 (boot placeholders), adc -1211, uptime 307.0 s.
`DACZ 10000`, `BIAS 32768`, 10 x `ADCR`: 454 281 174 124 119 382 99 440 -292 -493 (mean +129)
`BIAS 38229`, 10 x `ADCR`: 41 -172 -411 340 220 -276 -643 -576 -256 -124 (mean -186)

## After the hand-set and re-power (about 01:31)

`GSTS`: uptime 25.7 s. `DACX/DACY 32768`, `DACZ 10000`.
`BIAS 32768`, 10 x `ADCR`: 180 -30 -186 604 70 -182 485 176 -44 345 (mean +142)
`BIAS 38229`, 10 x `ADCR`: 413 46 -32 77 -218 -160 -107 -151 -262 -48 (mean -44)

## After approach 2 (`flip1.log` has the bias flip itself)

```
01:35:39 watch.py 4 s at Z 10000, -0.5 V: 32767 on every read (n ~14,000)
01:35:53 DACZ 0, watch.py 2 s: 32767 on every read
BIAS 27307 -> ADCR -32768 ; BIAS 32768 -> ADCR 97
01:36:27 MTMV 500 (Z 0, bias 0 V); BIAS 38229; ADCR: -516 -609 170 205 329 ; GSTS steps 495
01:37:07 watch.py 60 s at Z 0, -0.5 V: 8 blocks, means -25 4 -14 -31 -33 -29 -40 -35, min about -2900, max about +4300
```

## Noise with the tip clear

```
01:41:42 noise.py (GSTS and ADCR interleaved), operator at ~76 cm: raw sd 1537 | ADCR sd 327
01:43:57 noise.py, operator away: raw sd 1536 | ADCR sd 334
         again:                   raw sd 1539 | ADCR sd 336
01:47:10 noise2.py, ADCR only: -0.5 V sd 341 (0.1 s block means sd 28) | 0 V sd 341 (block sd 22)
01:51:20 spectrum.py, ADCR, 4 s, n=14041, sd 344: median line amplitude 7.3 counts;
         strongest lines 60 Hz 87, 180 Hz 42, 65 Hz 23, 64 Hz 20, 31 Hz 20, 300 Hz 19
         band means: 2-10 Hz 9.3, 10-30 Hz 8.5, 30-100 Hz 10.0, 100-400 Hz 10.7, 400-1600 Hz 5.0
```
`settle2.log` and `settle3.log` continue the series to 01:59 (sd 343-350, no decay).

## zprobe.py, bias -0.05 V (`BIAS 33314`), 02:03:03

```
Z 10000: mean 495 | Z 10000: 397 | Z 5000: 32767 | Z 0: 1152 | Z 0: 1121 | Z 5000: 32767 -> stopped
```

## zmap.py, 02:03:31 (Z confined to 0..10000; 32 reads each)

```
bias 33314 (-0.05 V) | 0:731 1000:101 2000:5159 3000:5401 4000:4130 5000:3522 6000:32767 7000:29002 8000:32767 9000:32767 10000:32767 5000:2775 0:16547
bias 32768 (0 V)     | 0:362 1000:443 2000:8 3000:42 4000:16 5000:-16 6000:260 7000:57 8000:32767 9000:1013 10000:26131 5000:122 0:235
bias 32222 (+0.05 V) | 0:-24522 1000:-18802 2000:-112 3000:-15019 4000:-1420 5000:-977 6000:-4019 7000:-3013 8000:-32768 9000:-31300 10000:-32768 5000:-1793 0:-19623
```

## backoff.py, zcal.py, zcal2.py

```
02:04:02 backoff: start at Z 0 mean 32767 ; +25: mean -22 max|882| -> CLEAR
02:04:33 zcal (onset search 0..50000, 100-count steps): no onset anywhere
02:05:04 zcal2 (one step at a time, negative):
  step -0, -10, -20: no onset up to 50000
  step -24: onset Z 28500 (I 1624)
  step -25: onset Z 9250 (I 32767)
  step -26: onset Z 0 (I 32767)
  end: reading at Z 0 mean 7233 (no retract had been requested - operator error in the call)
02:06:57 backoff: start 32767 ; +5: mean 95 max|721| -> CLEAR
```

## biascheck.py, 02:33:48 (fast tracker, 3 s per block)

```
-0.5 V n=244 found=167 below=77 none=0   | onset mean 41077 sd 3741
   0 V n=255 found=200 below=51 none=4   | onset mean 40708 sd 3702
+0.5 V n=259 found=172 below=21 none=66  | onset mean 43781 sd 2006
   0 V n=250 found=5   below=2  none=243
-0.5 V n=238 found=170 below=65 none=3   | onset mean 36884 sd 4844
static -0.5 V 0:-24 10000:-40 15000:208 20000:-111 25000:-27 30000:-10
static +0.5 V 0:56 10000:-13 15000:4 20000:1 25000:11 30000:-6
static    0 V 0:28 10000:38 15000:1373 20000:8 25000:-28 30000:-6
```

## artefact.py, 02:34:42 (static I(Z), 1000-count steps, 20 ms settle, 32 reads)

```
static -0.5 V points 44, |I|>300 at: (8000, 1863) (10000, 2047) (14000, 1190) (43000, 32767) -> stopped
static    0 V points 51, |I|>300 at: (43000..46000, 32767) (48000, 3862)
static +0.5 V points 43, |I|>300 at: (4000,-1174) (5000,-1083) (6000,-456) (12000,-1377) (29000,-2076)
     (30000,-2930) (31000,-3538) (32000,-3174) (34000,-2767) (35000,-2795) (36000,-1342) (42000,-32768) -> stopped
0 V, Z 20000 -> +800 : immediate median 27 (max|594|), +5 ms -112, +20 ms 69
0 V, Z 24000 -> -4000: immediate median 34 (max|508|), +5 ms 2,    +20 ms -124
0 V, Z 20000 -> +4000: immediate median 6  (max|611|), +5 ms 20,   +20 ms -125
```

## park.py, 02:35:49

```
retracted +0:   worst |I| over Z 0..50000 = 188
retracted +25:  worst 32767
retracted +50:  worst 32767
retracted +75:  worst 281
retracted +100: worst 287
after +50 margin (total +150): worst 339
parked: Z/X/Y/bias midscale; reading -27
GSTS: steps 527, uptime 3901.1 s
```
