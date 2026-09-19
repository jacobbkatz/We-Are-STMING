# Running notes, bench 2026-09-19 UTC (evening of 2026-09-18 local), this laptop, COM3

Nuh's Claude "was buggin and wasnt uptodate" -> session run on Jacob's laptop instead (SAID).
Pulled 16 commits at session start (up to 756aa7d).

## Before power
- Bounce test (SAID, Jacob): pressed up/down: "probably about three but the dampaning stops the
  bounces after like three" -> read as ~3 bounces/s, dies in ~3 bounces. Asked to confirm; not
  contradicted. Predicted f0 2.1-2.4 Hz. Damping ratio ~0.12 if 3 bounces to ~10%.
- Plan's stamp test with tip clear cannot see mechanical gap noise (no junction) -> flagged.
- Paper slip: NOT DONE. SAID: "we are sturggling the get the paper in with out shaking the machine
  there is 100% a gap and this test isnt needed lets move on".
- Safety rule 0 contradiction: plan says 45 min warm-up citing rule 0; STATUS says rule 0 RETIRED
  2026-09-15 (2 min). CLAUDE.md sec 4 still states the 45 min version. Not fixed yet.

## Timeline (UTC)
- 01:01:36 GSTS uptime 457 s (power on ~00:54). LEDs dark (SAID, asked, "yes dac lights are off").
- 01:01:51 touch2.py Z 10000: 0 V -6 sd 40 | -0.5 V -4 sd 40 | +0.5 V -3 sd 41 | 0 V -4 sd 40
  (2000 ADCR each). TIP CLEAR. NOISE 40 counts = back to 09-17 level (09-18: 341-350).
- 01:08:15 still.csv (stm_noise_spectrum.py 10): ADCR sd 42; floor 0.60; 60 Hz line 10 (09-18: 87),
  300 Hz 5, 180 Hz 4. Bands (mech col) 2-10 0.0, 10-30 0.3, 30-100 1.2, 100-400 2.1.
- 01:08:51 stamp.csv (stamping ~2 m away, SAID arranged): sd 42; floor 0.39; 2-10 0.4, 10-30 0.4,
  30-100 1.2, 100-400 1.4. --compare: 2-30 Hz A 0.1 vs B 0.4 counts -> no difference.
  TIP CLEAR: this is an electrical/microphonic check only.
- SAID: tip "as close i can to the gold" by eye, without the continuity crash test.
- live_touch.py (laptop nA beeper, tested on a fake incl. red run): started 01:12:30, Z 10000,
  -0.5 V, threshold 1000 counts; hands on screws gave +-50-61 counts.
- 01:19:49 CONTACT at Z 10000: 4082 counts (12.7 nA) in one 200-read block, previous 6. Z -> 0
  at once; clear at Z 0 (0 +- 8). THE BEEP WAS NOT HEARD (SAID). Sound test after: Beep 1800 Hz,
  SystemExclamation, SystemHand played; SAID "we just heard a beep" (which one not stated).
- 01:21:03 Z 0: -0.5 V mean -6, +0.5 V 2, 0 V -25 (reads +-600: hands/people) -> not touching.
  SAID "it looks like we are on the thing" -> eye cannot resolve.
- 01:22:15 onset0.py: baseline Z0 -8 sd 40; NO CURRENT 0..50000. Gold sprang back after the hand
  released the screws (hypothesis).
- 01:24 approach: --z-retracted low --motor-toward-sample negative --motor-step 1 --max-steps 300
  --z-step 200; baseline -54, raw noise 180, threshold 1500. TUNNELING at Z 10000 after 88 steps,
  reading 32767. Step 87: nothing 10000..50000.
- SAID 01:24ish: full authority for an hour, nobody in the room, check back in ~20 min.
- 01:27:17 Z 0 check: mean 358 (backoff.py's "clear" criterion too loose).
- 01:28:12 here.py at Z 0: 10 s record mean 1059 sd 96 (765..1566) = 3.3 nA +- 0.3 -> STEADY.
  Flip: -0.5 V 1156 | +0.5 V -811 | 0 V -1 | -0.5 V 1033. REAL.
  I-V (interleaved, sample V: counts): -1.0:29166 -0.9:32767 -0.8:12148 -0.7:8078 -0.6:2486
  -0.5:2280 -0.4:1053 -0.3:750 -0.2:351 -0.1:177 0:-21 +0.1:-166 +0.2:-243 +0.3:-563 +0.4:-690
  +0.5:-1479 +0.6:-1345 +0.7:-2599 +0.8:-3334 +0.9:-5446 +1.0:-16541. Superlinear, asymmetric
  above ~0.6 V (sample negative larger). ~190 MOhm at 0.1 V.
  Slope Z 0 -> 3000 (10-count steps): ~2000 falling slowly to ~1400. NOT rising with Z.
- 01:29:43 lift.py (tested on fake): +0: I0 2087, +1: 1818, +2: 3112 (onsets at 0), +3: PINNED
  32767 at Z 0 -> abort. A RETRACT STEP PUSHED THE GOLD IN (third time over two sessions).
- 01:30:00 backoff.py 2 80 0: pinned to +14; +16..+76: 4308..23856 fluctuating; +78, +80 pinned.
  NOT CLEAR after +80 (83 retract steps total).
- 01:31:30 Z sweep at 3 biases: -0.5 V Z0 32767, Z10000 32767, Z20000 103, Z0 58; 0 V all ~0;
  +0.5 V Z0 -64, Z10000 -21048, Z20000 -73, Z0 -98. GSTS steps -5 (= -88 +3 +80).
- 01:32:11 zdir.py (-0.14 V, CAP 15000): Z50000 1577, Z49000 21158 -> up: 49000 32767,
  50000 29558; reps: Z50000 27047..31903. LEFT Z AT 50000 IN CONTACT (bias 0 V) - my error.
- 01:32:40 clearcheck.py: Z midscale, MTMV +200: Z32768 3, Z16000 -3, Z0 -7, Z48000 40,
  Z32768 -3 -> CLEAR EVERYWHERE. Positive retracts, confirmed again.
- 01:33 approach, --z-retracted unknown --motor-step 1 --max-steps 400 (running).

## Motor count this power-up
-88 (approach) +3 (lift) +80 (backoff) +200 (clearcheck) = +195 net, then the unknown approach.

## Continued (all with full authority, nobody in the room from ~01:24)
- 01:41 unknown-mode approach #1 (bias was 0 V - MY ERROR, clearcheck.py had zeroed it):
  contact at midscale after 166 steps, 7758 counts at 0 V -> metal contact.
  ALSO the 01:24 approach ran at 0 V (onset0.py ended with BIAS 32768). Both approaches could
  only see metal contact. The new tip may have been blunted.
- 01:41:49 clearcheck +200: clear everywhere (<= 72 counts at -0.14 V). Steps +229 net.
- BIAS 38229 set and confirmed by GSTS.
- 01:42 unknown-mode #2 (at -0.5 V): baseline at midscale 6087 (already in range), hit at Z 18168
  going LOW (+1785 over baseline) -> tool: "LOW moves toward". Contaminated by the high baseline.
- 01:43:00 at Z 50000/45000/40000: <= 23 counts -> clear.
- 01:43:26 zdir2.py: 50000 -> 0 and back, 4 reps: NO CURRENT ANYWHERE.
- 01:44 wander.py: 88 of 92 sweeps found >= 1000 at Z 50000 itself (first point). Stopped.
- 01:46:23 3-bias sweeps: erratic, 413..19781 at the same Z within a second; 0 V ~0.
- 01:46:54 clearcheck +200: clear. Steps +429 net.
- 01:47 junction spectrum of here_run1 (01:28 steady junction): 0.5-2 Hz lines 11-19 counts,
  3-12 Hz 1-8, 14-16 Hz 5-7, 60 Hz 7; 0.01/0.1/1 s block sd 80/69/52 -> mostly slow (<2 Hz).
- 01:47 approach #3 with the tool now setting -0.5 V itself: baseline 114; LOW segment nothing;
  HIGH segment's FIRST point (= midscale) 6274 -> tool said "HIGH toward". INVALID: a hit at the
  segment start carries no direction. TOOL FLAW -> fixed + test (red then green).
- 01:48:37 lockin.py survey: 10000:29870 16000:56 22000:975 28000:7838 32768:7446 38000:6330
  44000:82 50000:88. Lock-in Zc 22000: D1000 789 -> 1571 (+782 +- 531, 1.5 sigma, HIGH more);
  D3000 10004 -> 10682 (+678 +- 2281, nothing). Parked Z 2000.
- touchrec.py at Z 2000: PINNED 5 s continuously -> watchdog Z 50000.
- 01:49:42 Z 50000: mean 26-41 sd 43-45 over 3 s -> clear-ish (~0.1 nA).
- 01:50-01:51 slowscan.py 50000 -> 0 -> 50000 in 100s, 3 reps: NOTHING over 100 counts anywhere.
- 01:51 wander2.py (20 min, every 15 s): first 2 min: one onset (11250), else none; I at Z 50000
  18-178 counts.
- Direction evidence tonight is MIXED: LOW-toward: 01:24 approach hit at its lowest point; here.py
  current fell 2000 -> 1400 as Z rose 0 -> 3000; unknown #2; survey 10000 highest; Z 2000 pinned.
  HIGH-toward: lock-in 1.5 sigma; Z 50000 carries the only small current while nothing lower
  reaches 1000 (02:53 wander2). Every one of them is swamped by the gold moving more than the Z
  range in < 1 min. UNRESOLVED.
- Tool changes in Code/pc/stm_approach.py: --bias (default 38229) set before the baseline,
  refused within 0.05 V of zero unless --allow-zero-bias; unknown mode treats a hit at the
  segment's first point as contact at midscale; known mode warns when contact is already at the
  retracted end. 61 tests pass; each new test shown red first.

## After the checkpoint push (340031e)
- SAID ~01:58-02:00: "i just came in that could be the reason" (the 01:58 contact coincided with Jacob
  entering). "continue ima leave again do your best to get an image send me an email if you need me
  to come down jacob@quis.com".
- SAID ~02:03: shield cover? then "nevermind it would add to much weight and would push the plate
  into the magnet". Suggested instead: a cardboard box resting on the BENCH (not done).
- 01:59:05 +200, 01:59:40 +300 (margin). 02:00 unknown-mode approach 5 (tool sets -0.5 V):
  contact AT MIDSCALE after 2 steps, 32767. 02:01:51 +200 clear.
- scan2.py (direction as a parameter) + scan2_test.py: both directions hold a flat surface, follow a
  bump (479/514 of 600), wrong sign detected (clamped 211). NOT RUN ON HARDWARE.
- creeptrack.py (tested on sim: touches land in the right half, rate recovered): 02:02:40 start.
  Touches: 02:06:42 midscale (+100); 02:07:37 Z 40768 HIGH half (+100); 02:07:44 Z 6768 LOW half
  (+200); 02:07:53 Z 31768 low (+400); 02:08:00 Z 40768 HIGH (+100); more after (GSTS +400 unlogged).
  Stopped 02:08. Touches in BOTH halves within seconds.
- 02:08:23 clearcheck 0: Z32768 4994, others ~0. GSTS steps 2427.
- 02:09:05 +500: then 60 s of sweeps every ~4 s: EVERY one touched at midscale (first point).
- 02:10:19 all-Z at 3 biases: random large currents at many Z (19215 at 24000; 32767 at Z 40000 at
  0 V = metal; -32228 at midscale at +0.14 V; -30500 at 40000). CHATTERING CONTACT. Steps 2927.
- 02:10:xx EMAIL SENT to jacob@quis.com (his instruction): back the side screws off ~1/4 turn each
  (away from the tip), look at the motor-screw ball contact, leave, say "backed off".
  State while waiting: bias 0 V, Z midscale, no scripts.
- Hypothesis: the motor has little leverage on the gap (tip near the pivot line, d small) or the
  plate is not following the screw; the tip may be carrying the plate.

## After the email
- SAID ~02:17: "backed off, ball is touching the plate". 02:17:42 all Z (0..65000), 3 biases, twice:
  within +-16 counts, sd 36-54 -> CLEAR.
- SAID: "Becuase the tip is much shorter your lever ratio is much shorter now so itd make sense u
  have to turn it more, lets keep on going we dont really have anouther day for a while".
- Alarm test: Beep + SystemHand + SystemExclamation x3 -> SAID "just beeeps" (only Beep audible).
- live_touch2.py (Z midscale, direction-neutral; contact -> bias 0 V + 6 beeps; check after 20 s ->
  2 beeps clear), tested on sim. SAID "just manuelly backed it off" (before the hand-set; meaning
  not clarified), then "go".
- 02:21:30 armed. 02:22:36-37 SMOOTH RISE while Jacob turned: 104 -> 262 -> 566 -> 1314 counts
  (0.5 s) -> CONTACT, bias 0 V, six beeps. Jacob backed off 1/32 turn (asked). 02:23:00 check -1
  -> CLEAR, two beeps. SAID "backing off" arrived ~02:24 (after the clear).
- catch_and_scan.py (tested on sim both directions; first version failed its test because the
  creeping surface enters reach outside the loop's window -> retry loop added) started ~02:23:10:
  waits for a touch with the motor still, lock-in for direction, then 4 scans + 4 X-held controls.
- analyze_scans.py: checked on synthetic images (bump: trace/retrace ~+0.4, image-image +0.7;
  controls ~0).
- 02:37: no touch yet (14 min).
- 02:37 SAID "just came in sorry the turn was probably more than 1/32". Stopped cas1 (no touch in
  14 min).
- live_touch2 again: 02:42:11 armed; 02:44:27 CONTACT 1160; SAID back off "the tiniest hair";
  02:44:50 check -4 -> CLEAR.
- SAID: "also start sending me update emails every 5 mintues so i dont have to check status by
  coming down here". Emails to jacob@quis.com, thread 1a0b78e0847ba1ac: 02:45, 02:50, 02:52.
- catch_and_scan run 2 from ~02:45: first touch 02:50:21 Z 8768 (low): lock-in +-500 I(-)1452
  I(+)1400 diff -52 se 28 undecided; then 02:50:32 Z 25768 (low) -2 +- 26; then at MIDSCALE every
  3 s: +30+-32, +13+-22, -28+-23, +24+-15, -0+-16, +48+-42, +33+-36, +58+-25, +7+-19, -2+-19; the
  current at midscale wandered 1295..3581. NO Z EFFECT at +-500.
- 02:51 bigswing.py: midscale 2472; Z+-2000 807/489 (-318+-183); Z+-8000 45/-6; Z+-20000 32/138;
  X+-5000 4/-12 (-17+-7); X+-15000 94/33; Z+-20000 231/285; midscale after -10. Junction faded.
- CONCLUSION (hypothesis-level): the piezo barely controls this junction current. Suspects: the
  contact is not the tip apex (tip lead / holder brushing the gold stack or copper frame), the Z
  drive not reaching the piezo, or the mounting blocking Z motion.
- 02:52 email: recommend stopping; back off side screws 1/4 turn; look at the head from the side
  for the tip lead near the gold; then "wrap".
