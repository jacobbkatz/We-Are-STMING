"""Build the data inventory: every raw bench file, what made it, and under what conditions.

    python3 deliverables/2026-09-19-pause/analysis/code/build_inventory.py

Writes deliverables/2026-09-19-pause/analysis/data_inventory.csv and DATA_INVENTORY.md.

Two kinds of information go into each row, and they are kept apart on purpose:

  MECHANICAL, read from the file itself: size, rows, columns, distinct values in the
  setting columns, whether it is empty or short. Nothing here can be wrong about the file.

  CURATED, transcribed from sessions/data/<session>/README.md and the session log named
  at the top of it. This is where bias, tip, Z parking and scan settings come from. Where
  a README or log does not state a setting, the field is UNKNOWN. NOTHING IS INFERRED
  FROM A DESIGN FILE OR FROM ANOTHER RUN (CLAUDE.md section 3d).

The CURATED block below is the only hand-written part of this script and every entry
names where it came from.
"""
import csv
import os
import statistics as st
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ANALYSIS, DATA, REPO, SESSIONS, read_rows, fnum, section

# ---------------------------------------------------------------- session-level facts
#
# Source for each: the session's own data README.md header and the session log it names.
SESSION_META = {
    "2026-09-17-bench": dict(
        log="sessions/2026-09-17-bench.md",
        when="2026-09-17 evening local, UTC 2026-09-17",
        machine="Jacob's Windows machine, COM3",
        tip="the blunt bent placeholder tip (identified as bent only on 2026-09-19)",
        sample="crumpled gold leaf; SAID at the end: the junction was probably on the "
               "COPPER beside it, not the gold (3.27)",
        holder="the original tip holder, before the 2026-09-18 rebuild",
        adcr_sd_clear="46 counts",
        tool="Code/pc/stm_feedback_scan.py and scratch variants of it; NO scripts/ "
             "directory was kept for this session",
        z_direction="HIGH toward the sample was the finding of the night, FOR THAT TIP",
        note="Z scale from this session (250 Z counts per motor step) was declared "
             "SUSPECT the next night: the staircase ran inside its own measured slack"),
    "2026-09-18-bench": dict(
        log="sessions/2026-09-18-bench.md",
        when="evening of 2026-09-17 local, 01:00-02:40 UTC 2026-09-18",
        machine="Jacob's Windows machine, COM3",
        tip="the same blunt placeholder, tip holder REBUILT that day (~2.2 mm further back)",
        sample="all-gold plate, continuity to the bias wire confirmed",
        holder="rebuilt",
        adcr_sd_clear="341-350 counts - about eight times the night before and the night "
                      "after; cause never found",
        tool="scratch scripts in scripts/, hardcoded to COM3 and Jacob's Desktop",
        z_direction="HIGH toward the sample (inherited from 2026-09-17, same tip)",
        note="the fast-tracker files (ft_*, lash_*) locate SNAP-IN events, not a "
             "tunnelling onset: the same onsets appeared with the bias at 0 V"),
    "2026-09-19-bench": dict(
        log="sessions/2026-09-19-bench.md",
        when="evening of 2026-09-18 local, 00:54-04:00 UTC 2026-09-19",
        machine="Jacob's laptop, COM3 (Nuh's computer was tried and abandoned)",
        tip="TWO TIPS. Everything before ~03:00 UTC used a tip Jacob then said was BENT; "
            "everything after used a new, 'very blunt' tip",
        sample="the 2026-09-19 copper-framed gold-leaf-on-paper stack",
        holder="unchanged from 2026-09-18",
        adcr_sd_clear="40-42 counts before the tip change, 34-36 after",
        tool="scratch scripts in scripts/, plus Code/pc/stm_y_control.py and "
             "Code/pc/stm_noise_spectrum.py",
        z_direction="UNRESOLVED for the bent tip; settled HIGH-toward for the new tip "
                    "at 03:48 (lock-in +6305 +- 1484, 4.2 sigma)",
        note="two approaches ran with the sample at 0 V by mistake and can only have "
             "seen metal contact - the session log calls this CLAUDE'S ERROR"),
    "2026-09-19-morning": dict(
        log="sessions/2026-09-19-morning.md",
        when="2026-09-19, about 11:15-13:30 UTC",
        machine="Jacob's laptop, COM3",
        tip="the 'very blunt' tip fitted ~03:00 UTC 2026-09-19, unchanged all morning, "
            "pressed into the gold with Z retracted for ~9, ~35, <=3.4 and ~5 minutes",
        sample="unchanged: the 2026-09-19 leaf-on-paper sandwich, edge-anchored",
        holder="unchanged",
        adcr_sd_clear="33.5-37.1 counts at power-up",
        tool="scratch scripts in scripts/; 14 of 20 have a --test self-test, six do not",
        z_direction="HIGH extends toward the sample; Z 0 is fully retracted; NEGATIVE "
                    "MTMV approaches",
        note="the approach sweeps in apz_*, release_watch_* and where_* ran in 1,000-"
             "count Z steps, not the 250 their scripts set - a default-argument bug. "
             "Every onset they record is a multiple of 1,000"),
}

# ---------------------------------------------------------------- per-file curated facts
#
# (session, filename): dict. 'what' and every setting is transcribed from the session's
# data README.md unless a different source is named in 'src'. UNKNOWN means the record
# does not state it - it is never inferred.
U = "UNKNOWN"
SRC = ("38229 = sample -0.5 V. NOT in the session log or the data README: read from "
       "the producing script's own source, which is committed in that session's "
       "scripts/ directory (%s)")
C = {}


def add(sess, name, what, bias="UNKNOWN", z="UNKNOWN", settings="", produced_by="UNKNOWN",
        passage="", excluded="", caveat=""):
    C[(sess, name)] = dict(what=what, bias=bias, z_parking=z, settings=settings,
                           produced_by=produced_by, passage=passage,
                           excluded=excluded, caveat=caveat)


S17 = "2026-09-17-bench"
# The bias of every 2026-09-17 scan is NOT written beside the scans. It is recorded in
# that session's "code changes" section instead: stm_feedback_scan.py "read a bias
# argument, printed it in its banner, and then ignored it - it wrote BIAS 38229
# unconditionally... Every scan before that ran at -0.5 V whatever was typed"
# (sessions/2026-09-17-bench.md, "What this session changed in the code"). The fix is
# visible in Code/pc/stm_feedback_scan.py lines 206-211, whose comment names the same
# defect. So the bias IS on record; it just is not where a reader would look.
_S17_BIAS = ("38229 = sample -0.5 V. NOT stated beside the scans: the tool ignored its "
             "own bias argument and wrote 38229 unconditionally until it was fixed after "
             "this session (sessions/2026-09-17-bench.md code-changes section; the fix is "
             "commented at Code/pc/stm_feedback_scan.py:206-211)")
_scan_note = ("cell = the Z DAC code the feedback loop needed to hold the setpoint; "
              "column header = X DAC code; first column = Y DAC code; two rows per line "
              "(fwd and back)")
for n, w, s in [
    ("scan_slow_1.csv", "first image, before the read timeout was fixed", "38-60 s"),
    ("scan_slow_2.csv", "second image, before the read timeout was fixed", "38-60 s"),
    ("scan_fast_1.csv", "one of four images of the same patch", "4.5-6.2 s each"),
    ("scan_fast_2.csv", "one of four images of the same patch", "4.5-6.2 s each"),
    ("scan_fast_3.csv", "one of four images of the same patch", "4.5-6.2 s each"),
    ("scan_fast_4.csv", "one of four images of the same patch", "4.5-6.2 s each"),
    ("diag_scan_normal_1.csv", "diagnostic scan, 15 loop corrections per pixel", ""),
    ("diag_scan_normal_2.csv", "diagnostic scan, 15 loop corrections per pixel", ""),
    ("diag_scan_x_held.csv", "THE CONTROL: identical timing, X never moved", ""),
    ("scan_slow_dwell_1.csv", "250 loop corrections per pixel", "60-88 s"),
    ("scan_slow_dwell_2.csv", "250 loop corrections per pixel", "60-88 s"),
    ("scan_wide_slow_1.csv", "wide scan, +-4000 X counts, slow loop", ""),
    ("scan_wide_slow_2.csv", "wide scan, +-4000 X counts, slow loop", ""),
    ("scan_wide_25nm_1.csv",
     "wide image, +-15000 X counts - and see the note below: these two ARE the "
     "+-15000 three-place test that sessions/2026-09-17-bench.md 3.25 records as "
     "never run", ""),
    ("scan_wide_25nm_2.csv",
     "wide image, +-15000 X counts, the repeat of the file above", ""),
]:
    add(S17, n, w, bias=_S17_BIAS, z="loop-controlled, clamped 12000-48000",
        settings="; ".join(x for x in (s, _scan_note) if x),
        produced_by="Code/pc/stm_feedback_scan.py or a diagnostic variant",
        passage="sessions/2026-09-17-bench.md 3.22-3.24; "
                "sessions/data/2026-09-17-bench/README.md")
add(S17, "diag_line_repeated.csv", "one line scanned ten times, +-400 X", bias=_S17_BIAS,
    z="loop-controlled", settings=_scan_note,
    produced_by="a scratch diagnostic variant of stm_feedback_scan.py",
    passage="sessions/2026-09-17-bench.md 3.24 H2",
    caveat="every fwd and back array is BYTE-IDENTICAL: the scratch tool stored the "
           "forward pass twice. Any trace-versus-retrace figure from this file is "
           "meaningless (sessions/2026-09-17-bench.md 3.25)")
add(S17, "line_repeated_wide.csv", "one line, 12 passes, +-15000 X", bias=_S17_BIAS,
    z="loop-controlled", settings=_scan_note,
    produced_by="a scratch diagnostic variant of stm_feedback_scan.py",
    passage="sessions/2026-09-17-bench.md 3.25; CLOSED 2026-09-19, "
            "deliverables/2026-09-19-pause/candidates/VERDICT.md and STATUS.md",
    caveat="TWO things. (1) same byte-identical fwd/back defect as "
           "diag_line_repeated.csv. (2) its 636-count reproducible profile, carried as "
           "UNDETERMINED since 2026-09-17, is CLOSED: it is the feedback loop recovering "
           "from the 30,000-count X flyback between passes on a surface tilted at -0.105 "
           "Z counts per X count, which predicts a 3,144-count Z error at every pass "
           "start. Dropping two pixels of twenty-one takes the consecutive-pass "
           "correlation from +0.65 to +0.05. Found by subagent 2 at this pause point")
add(S17, "line_three_y_positions.csv", "one line at three separated Y positions, +-8000 X",
    bias=_S17_BIAS, z="loop-controlled",
    settings="first column = Y offset, second = pass number, 5 passes per place",
    produced_by="a scratch three-Y control",
    passage="sessions/2026-09-17-bench.md 3.25 CORRECTION",
    caveat="the CORRECTION in 3.25 records that this control was run at the WRONG WIDTH "
           "(+-8000 against the wide scans' +-15000) and so had no power to "
           "discriminate. The +-15000 version of the same test WAS run and is "
           "scan_wide_25nm_1/2.csv in this directory - found 2026-09-19, and those two "
           "files had been missing from this directory's README table")

S18 = "2026-09-18-bench"
add(S18, "console_outputs.md", "everything not saved to a file at the time, transcribed: "
    "touch checks, noise, spectrum, Z probes, calibration steps, bias check, static "
    "scans, the park", bias="various, stated in the file", z="various",
    settings="prose, not a data file", produced_by="hand transcription",
    passage="sessions/2026-09-18-bench.md throughout")
add(S18, "approach1.log", "stm_approach.py, 600 steps, no contact",
    bias="UNKNOWN - the tool did not set a bias at this date", z="10000 retracted",
    settings="--motor-step 5 --max-steps 600 --z-step 200; baseline 250, "
             "single-conversion noise 1436, auto threshold 8614",
    produced_by="Code/pc/stm_approach.py", passage="sessions/2026-09-18-bench.md 3.2")
add(S18, "approach2.log", "after the hand-set: contact after 5 steps at Z 25,800, "
    "20,878 counts", bias="UNKNOWN - tool did not set one", z="10000 retracted",
    settings="--max-steps 3500; noise 1821, threshold 10923",
    produced_by="Code/pc/stm_approach.py", passage="sessions/2026-09-18-bench.md 3.4")
add(S18, "flip1.log", "the bias flip at the onset, 01:35:06",
    bias="alternating -0.5 / +0.5 / 0 V", z="crept 10000 -> 11900 in 50-count steps",
    settings="the control that makes it a junction: the reading follows the bias sign",
    produced_by="scripts/bias_flip.py", passage="sessions/2026-09-18-bench.md 3.4")
add(S18, "approach3.log", "contact after 135 steps at Z 10,200, 11,693 counts",
    bias="NOT SET BY THE TOOL and not recorded. Code/pc/stm_approach.py did not set a "
         "bias until it was fixed on 2026-09-19, so the bias was whatever the previous "
         "command left. The session log does not say what that was", z="10000 retracted", settings="--motor-step 3 --max-steps 900 --threshold 6000",
    produced_by="Code/pc/stm_approach.py", passage="sessions/2026-09-18-bench.md 3.6")
add(S18, "char1.log", "characterize.py: found the current already pinned at Z 10,000 "
    "and aborted", bias="38229 = sample -0.5 V", z="10000",
    settings="200 baseline reads, all 32,767 (railed)",
    produced_by="scripts/characterize.py", passage="sessions/2026-09-18-bench.md 3.6")
add(S18, "char1.csv", "the 200 baseline readings characterize.py aborted on",
    bias="38229 = sample -0.5 V", z="10000",
    settings="columns t, phase, z, bias, value",
    produced_by="scripts/characterize.py", passage="sessions/2026-09-18-bench.md 3.6",
    caveat="every value is 32,767 - the ADC rail. It records a railed contact, not a "
           "measurement of current")
add(S18, "zcal3_run1.log", "three one-step-at-a-time passes with onset slope scans, "
    "then an X/Y check", bias=SRC % "scripts/zcal3.py:97 rig.bias(38229)", z="swept 0-50000 after each step",
    settings="one motor step per pass entry", produced_by="scripts/zcal3.py",
    passage="sessions/2026-09-18-bench.md 3.7")
add(S18, "zcal3_run1.csv", "the slope scan taken at each onset of zcal3_run1",
    bias=SRC % "scripts/zcal3.py:97 rig.bias(38229)", z="swept in 25-count steps at each onset",
    settings="columns t (HH:MM:SS), tag (p<pass>_s<step>), z, mean",
    produced_by="scripts/zcal3.py", passage="sessions/2026-09-18-bench.md 3.7",
    caveat="holds only the slope scans, not the full sweeps; the session log's table is "
           "the fuller record")
add(S18, "track_run1.log", "90 s of repeated slow onset searches at a FIXED motor position",
    bias=SRC % "scripts/track.py:13 rig.bias(38229)", z="swept each search", settings="the still-motor control",
    produced_by="scripts/track.py", passage="sessions/2026-09-18-bench.md 3.7")
add(S18, "track_run1.csv", "the 276 searches behind track_run1.log",
    bias=SRC % "scripts/track.py:13 rig.bias(38229)",
    z="swept each search", settings="columns t, onset_z (None if nothing found), motor_adj",
    produced_by="scripts/track.py", passage="sessions/2026-09-18-bench.md 3.7")
for n, w in (("ft_run1.log", "the fast tracker, first run"),
             ("ft_run1.json", "the fast tracker's raw points, first run"),
             ("ft_long1.log", "the fast tracker, five minutes"),
             ("ft_long1.json", "the fast tracker's raw points, five minutes")):
    add(S18, n, w, bias=SRC % "scripts/ft_run.py:17 and scripts/ft_long.py:22, rig.bias(38229)",
        z="short fast climbs to 1,000 counts",
        settings="JSON keys A, X, Y, B - hold A, an X sweep, a Y sweep, hold B; "
                 "each point is [t, z, flag]",
        produced_by="scripts/fasttrack.py, scripts/ft_run.py, scripts/ft_long.py",
        passage="sessions/2026-09-18-bench.md 3.8",
        caveat="THE DATA README'S OWN CAVEAT: these record where the current first passed "
               "1,000 counts on a fast climb, and the same onsets appeared with the bias "
               "at 0 V. They locate SNAP-IN events, not a tunnelling onset. Their wobble "
               "statistics, spectrum and X/Y numbers are PROVISIONAL")
add(S18, "lash_run1.log", "fast-tracker medians after single motor steps",
    bias=SRC % "scripts/lash.py:31 rig.bias(38229)", z="short fast climbs", settings="stopped by hand, so NO CSV was written",
    produced_by="scripts/lash.py", passage="sessions/2026-09-18-bench.md 3.8",
    caveat="same fast-tracker caveat; and the run was stopped by hand so the log is the "
           "only record")
add(S18, "settle2.log", "noise with the tip clear, 01:47-01:59", bias="-0.5 V and 0 V",
    z="retracted, tip clear", settings="ADCR only",
    produced_by="scripts/settle_wait.py", passage="sessions/2026-09-18-bench.md 3.5")
add(S18, "settle3.log", "noise with the tip clear, later in the same window",
    bias="-0.5 V and 0 V", z="retracted, tip clear", settings="ADCR only",
    produced_by="scripts/settle_wait.py", passage="sessions/2026-09-18-bench.md 3.5")

S19B = "2026-09-19-bench"
add(S19B, "still.csv", "10 s noise spectrum, room still, tip clear",
    bias="UNKNOWN - the tool does not set a bias and reads only", z="tip clear",
    settings="columns t_s, adcr; ADCR sd 42",
    produced_by="Code/pc/stm_noise_spectrum.py 10 --out still.csv",
    passage="sessions/2026-09-19-bench.md 3.3",
    caveat="WITH THE TIP CLEAR this can only test electrical and microphonic pickup. "
           "There is no junction for floor vibration to act on")
add(S19B, "stamp.csv", "the same 10 s while someone stamped about 2 m away",
    bias="UNKNOWN - read-only tool", z="tip clear",
    settings="columns t_s, adcr; ADCR sd 42, no difference from still.csv",
    produced_by="Code/pc/stm_noise_spectrum.py 10 --out stamp.csv",
    passage="sessions/2026-09-19-bench.md 3.3", caveat="same tip-clear caveat as still.csv")
add(S19B, "live_touch.log", "the laptop nano-amp beeper during the hand-set; contact "
    "01:19:49 at 4,082 counts", bias="38229 = sample -0.5 V", z="held at 10000",
    settings="latches and pulls Z back at 1,000 counts",
    produced_by="scripts/live_touch.py", passage="sessions/2026-09-19-bench.md 3.4")
for n, w in (("onset0_run1.log", "piezo-only onset search summary"),
             ("onset0_run1.csv", "the 16,416 readings behind it")):
    add(S19B, n, w, bias="38229 = sample -0.5 V", z="swept 0 to 50000",
        settings="columns t, tag (base/onset), z, bias, value",
        produced_by="scripts/onset0.py", passage="sessions/2026-09-19-bench.md 3.4",
        caveat="this script ended by ZEROING THE BIAS, which is what left the next "
               "approach running at 0 V")
add(S19B, "approach1_zero_bias.log", "approach at 0 V bias; contact at the first sweep "
    "point after 88 steps", bias="0 V - THE ERROR", z="10000",
    settings="--z-retracted low --motor-toward-sample negative --motor-step 1 "
             "--max-steps 300 --z-step 200",
    produced_by="Code/pc/stm_approach.py", passage="sessions/2026-09-19-bench.md 3.5, 4",
    excluded="the session log records it as CLAUDE'S ERROR: with the sample at 0 V the "
             "threshold could only trip on metal contact, so this cannot show a "
             "tunnelling onset")
for n, w in (("here_run1.log", "the printed summary of the steady junction"),
             ("here_run1.csv", "the raw points: a 10 s record, the bias flip, an I-V and "
                               "a Z 0-3000 sweep")):
    add(S19B, n, w, bias="38229 = sample -0.5 V for the record and the sweep; 21 codes "
        "for the I-V; alternating for the flip", z="0 for the record, 0-3000 for the sweep",
        settings="columns t, tag (rec/flip/iv/slope), z, bias, value; rec is 35,000 "
                 "readings over 10.3 s at about 3,400 per second",
        produced_by="scripts/here.py", passage="sessions/2026-09-19-bench.md 3.6",
        caveat="taken with the tip Jacob identified as BENT about 90 minutes later. "
               "Nothing in it transfers to the tip fitted at ~03:00")
for n, w in (("lift_run1.log", "single retract steps, checking after each"),
             ("lift_run1.csv", "the readings behind them"),
             ("backoff2_0919.log", "80 further retract steps, still not clear")):
    add(S19B, n, w, bias="38229 = sample -0.5 V", z="0, then swept",
        settings="columns t, tag, z, bias, value",
        produced_by="scripts/lift.py, scripts/backoff.py",
        passage="sessions/2026-09-19-bench.md 3.7")
for n, w in (("zdir_run1.log", "Z sweeps at -0.14 V to find the direction"),
             ("zdir_run1.csv", "the sweep points")):
    add(S19B, n, w, bias="sample -0.14 V", z="swept 50000 -> 0 -> 50000",
        settings="columns t, leg, z, mean", produced_by="scripts/zdir.py",
        passage="sessions/2026-09-19-bench.md 3.9, 4",
        caveat="this script had NO WATCHDOG and ended with Z parked in contact at 50,000 "
               "while 27,000-32,000 counts flowed - listed as a fault in the session log")
add(S19B, "approach2_unknown_zero_bias.log", "direction-finding approach, ALSO at 0 V; "
    "contact at midscale after 166 steps", bias="0 V - THE ERROR", z="midscale",
    settings="direction-finding mode", produced_by="Code/pc/stm_approach.py",
    passage="sessions/2026-09-19-bench.md 3.9, 4",
    excluded="0 V bias: only metal contact could trip it")
add(S19B, "approach3_unknown.log", "direction-finding at -0.5 V: reported LOW",
    bias="38229 = sample -0.5 V", z="midscale", settings="direction-finding mode",
    produced_by="Code/pc/stm_approach.py", passage="sessions/2026-09-19-bench.md 3.9",
    caveat="its baseline was already 6,087 counts, so the direction it reported is not "
           "trustworthy")
add(S19B, "approach4_unknown_tool_bias.log", "direction-finding with the tool setting the "
    "bias: reported HIGH", bias="set by the tool", z="midscale",
    settings="direction-finding mode", produced_by="Code/pc/stm_approach.py",
    passage="sessions/2026-09-19-bench.md 3.9, 7",
    excluded="INVALID: the hit was midscale itself, so the tool reported a direction from "
             "no evidence. The tool was fixed afterwards")
add(S19B, "approach5_unknown.log",
    "a further direction-finding approach: contact ALREADY PRESENT at midscale after "
    "2 motor steps, 32,767 counts against a baseline of 73, so the direction could not "
    "be told and the run stopped",
    bias="38229 = sample -0.50 V - the log prints it in its own banner",
    z="parks at 32768 for every motor step, searching toward 10000 and toward 50000",
    settings="direction-finding mode, motor step -1 per cycle, up to 700 steps; "
             "baseline 73 counts, noise 170 counts RMS, threshold 1,500 counts",
    produced_by="Code/pc/stm_approach.py",
    passage="NOT NAMED IN ANY SESSION LOG OR IN THE DATA README. Everything above is "
            "read from the log file itself, which prints its own settings",
    caveat="the only data file in the four directories that no prose document mentions")
for n, w in (("zdir2_run1.log", "four sweeps 50000 -> 0 -> 50000: nothing"),
             ("zdir2_run1.csv", "the 808 sweep points")):
    add(S19B, n, w, bias=SRC % "scripts/zdir2.py:17 BIAS 38229",
        z="swept 50000 -> 0 -> 50000, four times",
        settings="columns t (unix), tag (down0..up3), z, mean",
        produced_by="scripts/zdir2.py", passage="sessions/2026-09-19-bench.md 3.8")
add(S19B, "wander_run1.log", "sweeps from Z 50000: current at 50000 itself on 88 of 92",
    bias=SRC % "scripts/wander.py:13 BIAS 38229", z="swept from 50000",
    settings="stopped by hand; NO CSV was written", produced_by="scripts/wander.py",
    passage="sessions/2026-09-19-bench.md 3.8")
for n, w in (("lockin_run1.log", "survey and the Z-toggle lock-in at Z 22000"),
             ("lockin_run1.csv", "the 120 lock-in points")):
    add(S19B, n, w, bias="38229 = sample -0.5 V", z="22000, toggled +-D",
        settings="columns t (unix), zc, d, i_low, i_high",
        produced_by="scripts/lockin.py", passage="sessions/2026-09-19-bench.md 3.8, 3.9")
for n, w in (("touchrec_run1.log", "fixed Z 2000: pinned for 5 s, the watchdog fired"),
             ("touchrec_run1.csv", "the 17,088 readings")):
    add(S19B, n, w, bias=SRC % "scripts/touchrec.py:13 BIAS 38229",
        z="2000, fixed", settings="columns t, value",
        produced_by="scripts/touchrec.py", passage="sessions/2026-09-19-bench.md 3.8",
        caveat="every value is 32,767 - the ADC rail. sd 0. It records a railed contact")
for n, w in (("slowscan_run1.log", "three slow sweeps 50000 -> 0 -> 50000: nothing over "
                                   "100 counts"),
             ("slowscan_run1.csv", "the 3,006 sweep points")):
    add(S19B, n, w, bias=SRC % "scripts/slowscan.py:16 BIAS 38229",
        z="swept in 100-count steps",
        settings="columns t (unix), leg (down0..up2), z, mean",
        produced_by="scripts/slowscan.py", passage="sessions/2026-09-19-bench.md 3.8")
for n, w in (("wander2_run1.log", "a sweep every 15 s for four minutes"),
             ("wander2_run2.log", "the same again; the gold came back into hard contact "
                                  "after about ten minutes")):
    add(S19B, n, w, bias="-0.5 V, with +0.5 V and 0 V checks", z="swept 50000 down in "
        "250-count steps", settings="stopped by hand, so NO CSV was written; the "
        "two-minute summary lines are the whole record",
        produced_by="scripts/wander2.py", passage="sessions/2026-09-19-bench.md 3.10")
add(S19B, "claude_running_notes.md", "Claude's timeline written during the session, "
    "including console output not saved elsewhere", bias="various", z="various",
    settings="prose, not a data file", produced_by="hand",
    passage="sessions/2026-09-19-bench.md throughout")
add(S19B, "creeptrack_run1.log", "motor still, both halves of Z swept every 5 s, +100 "
    "retract at each touch",
    bias=SRC % "scripts/creeptrack.py:36 dev.set_bias(38229)", z="both halves swept",
    settings="stopped as a runaway", produced_by="scripts/creeptrack.py",
    passage="sessions/2026-09-19-bench.md 3.12")
add(S19B, "live_touch2_run1.log", "beeper hand-set 02:21-02:23: the smooth rise "
    "104 -> 262 -> 566 -> 1314 counts", bias="-0.5 V, cut to 0 V at 1,000 counts",
    z="midscale (direction-neutral)", settings="re-checks every 20 s",
    produced_by="scripts/live_touch2.py", passage="sessions/2026-09-19-bench.md 3.12")
add(S19B, "live_touch2_run2.log", "beeper hand-set 02:42-02:44, 'the tiniest hair'",
    bias="-0.5 V, cut to 0 V at 1,000 counts", z="midscale",
    settings="re-checks every 20 s", produced_by="scripts/live_touch2.py",
    passage="sessions/2026-09-19-bench.md 3.12")
for n, w in (("cas2.log", "catch-and-scan run 2: the gold arrived 02:50:21 by creep; "
                          "ten +-500 lock-ins all undecided"),
             ("catch_and_scan_run2.log", "the same run, second copy of the log")):
    add(S19B, n, w, bias="38229 = sample -0.5 V", z="swept, then lock-in at the touch",
        settings="lock-in at +-500 counts",
        produced_by="scripts/catch_and_scan.py",
        passage="sessions/2026-09-19-bench.md 3.12",
        caveat="taken with the BENT tip")
add(S19B, "bigswing_run1.csv", "Z +-2000/+-8000/+-20000 and X +-5000/+-15000 toggles at "
    "02:51; the junction faded during it", bias="38229 = sample -0.5 V",
    z="toggled about the touch point",
    settings="columns t (unix), axis (Z/X), amp, i_minus, i_plus",
    produced_by="scripts/bigswing.py", passage="sessions/2026-09-19-bench.md 3.12",
    caveat="BENT tip, and the junction faded during the test, so the later rows are not "
           "comparable with the earlier ones")
for n in ("cas3.log", "cas4.log", "cas5.log", "cas6.log", "cas7.log"):
    add(S19B, n, "catch-and-scan run waiting after a new-tip hand-set: NO TOUCH",
        bias="38229 = sample -0.5 V", z="swept",
        settings="runs 5 and 6 were stopped for re-sets",
        produced_by="scripts/catch_and_scan.py",
        passage="sessions/data/2026-09-19-bench/README.md",
        caveat="THE FILE IS ZERO BYTES. The tool prints only on a touch, so an empty file "
               "is the record of 'nothing happened'. It is not a truncated file, but it "
               "also carries no timestamp, no duration and no settings")
for n, w in (("live_touch4.log", "new-tip beeper hand-set, 03:06, three hair back-offs"),
             ("live_touch5.log", "new-tip beeper hand-set, 03:21, three hair back-offs")):
    add(S19B, n, w, bias="-0.5 V, cut to 0 V at 1,000 counts", z="midscale",
        settings="the NEW very blunt tip", produced_by="scripts/live_touch2.py",
        passage="sessions/2026-09-19-bench.md 3.13")
add(S19B, "approach_newtip.log", "1-step motor approach with the new tip, 78 steps, "
    "nothing (stopped)", bias="set by the tool (fixed after the 0 V error)",
    z="10000 retracted", settings="--motor-step 1",
    produced_by="Code/pc/stm_approach.py", passage="sessions/2026-09-19-bench.md 3.13")
for n, w in (("live_backoff1.log", "the live back-off, 03:39: ticks while touching, "
                                   "clear on silence"),
             ("live_backoff2.log", "the live back-off again, slower, 03:41")):
    add(S19B, n, w, bias="38229 = sample -0.5 V", z="held", settings="the NEW blunt tip",
        produced_by="scripts/live_backoff.py", passage="sessions/2026-09-19-bench.md 3.13")
add(S19B, "approach_big.log", "5-step motor approach: hard contact at midscale after "
    "60 steps", bias="set by the tool", z="midscale",
    settings="--motor-step 5", produced_by="Code/pc/stm_approach.py",
    passage="sessions/2026-09-19-bench.md 3.13")
add(S19B, "cas8.log", "the lock-in at the hard contact of approach_big: all readings "
    "railed, direction undecided", bias="38229 = sample -0.5 V", z="midscale",
    settings="lock-in +-2000", produced_by="scripts/catch_and_scan.py",
    passage="sessions/2026-09-19-bench.md 3.13")
for n in sorted(os.listdir(os.path.join(DATA, S19B))):
    if n.startswith("cas8_chmap_"):
        kind = "X-HELD CONTROL" if "xheld" in n else "constant-height current map"
        add(S19B, n, "%s taken at the railed contact" % kind,
            bias="38229 = sample -0.5 V", z="fixed at the contact",
            settings="cell = averaged CURRENT in ADC counts at a fixed Z, NOT a Z code; "
                     "21 X points, 11 Y lines, 8 reads per pixel",
            produced_by="scripts/chmap.py", passage="sessions/2026-09-19-bench.md 3.13",
            excluded="SATURATED: every pixel is at the ADC rail (32,767). The data "
                     "README calls these saturated and they carry no information about "
                     "the surface")
add(S19B, "cas9.log", "the run that settled the Z direction (HIGH toward, 4.2 sigma) and "
    "then took 4 feedback scans and 4 X-held controls",
    bias="38229 = sample -0.5 V", z="touch at 40768, then loop-controlled",
    settings="lock-in +-2000: I(-) 26237, I(+) 32542, diff +6305 +- 1484; the log carries "
             "the loop's own saturated and clamped counters per run",
    produced_by="scripts/catch_and_scan.py", passage="sessions/2026-09-19-bench.md 3.14")
for i in range(4):
    add(S19B, "cas9_scan%d.csv" % i, "constant-current feedback scan %d of 4" % i,
        bias="38229 = sample -0.5 V, setpoint 1,000 counts",
        z="loop-controlled, clamp 12000-48000",
        settings="+-1500 X and Y, 21 x 11 pixels, loop tuned to 100 counts per decade; "
                 + _scan_note,
        produced_by="scripts/scan2.py via scripts/catch_and_scan.py",
        passage="sessions/2026-09-19-bench.md 3.14")
    add(S19B, "cas9_xheld%d.csv" % i, "X-HELD CONTROL %d of 4: identical timing, X never "
        "moved" % i, bias="38229 = sample -0.5 V, setpoint 1,000 counts",
        z="loop-controlled, clamp 12000-48000",
        settings="same as the scan it follows; " + _scan_note,
        produced_by="scripts/scan2.py via scripts/catch_and_scan.py",
        passage="sessions/2026-09-19-bench.md 3.14",
        caveat=("control 2 ABORTED after one line (saturated 47), so it contributes one "
                "line, not eleven" if i == 2 else
                "control 1 began at the loop's 12,000 lower clamp and climbed back blind; "
                "the '28,000-count swing' once read off it was THE TOOL, not the gold, and "
                "is RETIRED in docs/FACTS.md" if i == 1 else ""))
for i, (n, w) in enumerate([
        ("ycontrol_run1", "three-Y control, +-3000 Y, scanning"),
        ("ycontrol_xheld_run1", "three-Y control, +-3000 Y, X HELD"),
        ("ycontrol_run2", "three-Y control, +-12000 Y, scanning"),
        ("ycontrol_run3", "three-Y control, +-12000 Y, X HELD"),
        ("ycontrol_run4", "three-Y control, +-12000 Y, scanning, REPEAT of run 2")]):
    add(S19B, n + ".log", w + " (printed summary)",
        bias="38229 = sample -0.5 V, setpoint 1,000 counts (3.12 nA)",
        z="loop-controlled, Z window widened to 60000 at the top",
        settings="21 X points at +-15000, 3 places, 6 passes each, loop 100 counts per "
                 "decade; the log's first line gives the onset Z",
        produced_by="Code/pc/stm_y_control.py via scripts/run_ycontrol*.py",
        passage="sessions/2026-09-19-bench.md 3.15",
        caveat="the tool prints a '287-419 count wobble' comparison that belongs to the "
               "2026-09-17 junction, not to this one")
for n, w in (("ycontrol_run1.csv", "three-Y control, +-3000 Y, scanning"),
             ("ycontrol_xheld_run1.csv", "three-Y control, +-3000 Y, X HELD"),
             ("ycontrol_run2_ysep12000.csv", "three-Y control, +-12000 Y, scanning"),
             ("ycontrol_run3_ysep12000_xheld.csv", "three-Y control, +-12000 Y, X HELD"),
             ("ycontrol_run4_ysep12000_repeat.csv",
              "three-Y control, +-12000 Y, scanning, REPEAT")):
    add(S19B, n, w, bias="38229 = sample -0.5 V, setpoint 1,000 counts",
        z="loop-controlled, top clamp 60000",
        settings="first column = Y offset, second = pass number, then 21 X DAC codes; "
                 "3 places x 6 passes = 18 rows",
        produced_by="Code/pc/stm_y_control.py via scripts/run_ycontrol*.py",
        passage="sessions/2026-09-19-bench.md 3.15",
        caveat="15 of the 90 lines across the three +-12000 runs are blind loop ramps "
               "(sessions/2026-09-19-morning.md 6)")
add(S19B, "approach_known1.log", "--z-retracted low approach: tunnelling at Z 45,200 "
    "after 0 steps", bias="set by the tool", z="low = retracted for this tip",
    settings="known-direction mode", produced_by="Code/pc/stm_approach.py",
    passage="sessions/data/2026-09-19-bench/README.md")
for i in range(3):
    add(S19B, "img_scan_%d.csv" % i, "wide constant-current image %d of 3" % i,
        bias="38229 = sample -0.5 V, setpoint 1,000 counts",
        z="loop-controlled, top clamp raised to 60000",
        settings="+-15000 X and Y, 21 x 11 pixels; " + _scan_note,
        produced_by="scripts/scan2.py via scripts/run_img_wide.py",
        passage="sessions/2026-09-19-bench.md 3.16",
        caveat=("ABORTED after %d forward line(s) of 11" % (i + 1)) if i < 2 else
               "ran all 11 lines; the session log reports 14.5%% saturation for it")
for i in range(2):
    add(S19B, "img_xheld_%d.csv" % i, "X-HELD CONTROL %d of 2 for the wide images" % i,
        bias="38229 = sample -0.5 V, setpoint 1,000 counts",
        z="loop-controlled, top clamp 60000",
        settings="same as the images; " + _scan_note,
        produced_by="scripts/scan2.py via scripts/run_img_wide.py",
        passage="sessions/2026-09-19-bench.md 3.16")

S19M = "2026-09-19-morning"
_zt = ("columns t, cycle, phase, z, adc; phases start/find/pre/in/out/out2/snap/lost; "
       "cycle 0 is the find; Z steps of 4 counts, 5 averaged reads per point")
add(S19M, "baseline_run1.log", "power-up baseline: GSTS, ADCR at 0/-0.5/+0.5/0 V with "
    "Z 0, then a gentle walk to midscale. Tip clear",
    bias="0, -0.5, +0.5, 0 V in turn", z="0, then walked to 32768 in 64-count steps",
    settings="200 reads per bias; sd 33.5-37.1 counts",
    produced_by="scripts/baseline.py", passage="sessions/2026-09-19-morning.md 3.1")
add(S19M, "live_backoff_run1.log", "hand-set 1, live back-off at Z midscale: contact "
    "11:24:40, clear 11:24:55", bias="38229 = sample -0.5 V", z="midscale",
    settings="the laptop ticks while touching",
    produced_by="scripts/live_backoff.py (via Code/pc)",
    passage="sessions/2026-09-19-morning.md 3.2")
add(S19M, "creep_watch_run1.log", "8.0 minutes at Z midscale with nothing moving: no "
    "current", bias="38229 = sample -0.5 V", z="midscale, fixed",
    settings="20-read averages continuously; 17 printed at -24 to +16 counts",
    produced_by="scripts/creep_watch.py", passage="sessions/2026-09-19-morning.md 3.2",
    caveat="ITS CSV WAS LOST: the script wrote the CSV only on a clean exit and the task "
           "was stopped. The log is the whole record")
add(S19M, "ztest_run1.log", "first Z test: nothing in Z 32768-62000",
    bias="38229 = sample -0.5 V", z="walked 32768 -> 62000",
    settings="found no contact", produced_by="scripts/ztest.py",
    passage="sessions/2026-09-19-morning.md 3.2")
add(S19M, "ztest_1789817796.csv", "the points of that first, empty Z test",
    bias="38229 = sample -0.5 V", z="walked 32768 -> 62000", settings=_zt,
    produced_by="scripts/ztest.py", passage="sessions/2026-09-19-morning.md 3.2",
    excluded="status LOST - no contact was found, so it has no cycles and no results")
add(S19M, "approach_run1.log", "111 single motor steps toward the sample, nothing "
    "(stopped by hand for hand-set 2)", bias="set by the tool", z="0 retracted",
    settings="single steps", produced_by="Code/pc/stm_approach.py",
    passage="sessions/2026-09-19-morning.md 3.2")
add(S19M, "touch_and_hold_run1.log", "hand-set 2 WITHOUT a hand back-off: contact "
    "11:44:36, railed at Z 0 from 11:44:38", bias="38229 = sample -0.5 V", z="pulled to 0",
    settings="the motor was to do the back-off; it did not",
    produced_by="scripts/touch_and_hold.py", passage="sessions/2026-09-19-morning.md 3.3")
for n, w in (("backoff_motor_run1.log", "+80 single retract steps: still railed"),
             ("backoff_motor_run2.log", "+300 single retract steps: still railed")):
    add(S19M, n, w, bias="38229 = sample -0.5 V", z="0",
        settings="single retract steps, checking after each",
        produced_by="scripts/backoff_motor.py",
        passage="sessions/2026-09-19-morning.md 3.3")
for n, w in (("live_backoff_z0_run1.log", "hand-set 3, back-off with Z held at 0: clear "
                                          "11:53:35"),
             ("live_backoff_z0_run2.log", "hand-set 4: clear 12:50:00"),
             ("live_backoff_z0_run3.log", "hand-set 5: clear 13:12:01")):
    add(S19M, n, w, bias="38229 = sample -0.5 V", z="held at 0 (fully retracted)",
        settings="ticks while touching, silence when clear",
        produced_by="scripts/live_backoff_z0.py",
        passage="sessions/2026-09-19-morning.md 3.4, 3.8, 3.13",
        caveat="this script has NO self-test (it reuses the tested live_backoff.py)")
for n, w in (("stairs_run1.log", "two full finds 11:55:42-11:56:19: nothing in Z 0-62000"),
             ("stairs_1789818942.csv", "the two find attempts, both empty")):
    add(S19M, n, w, bias="38229 = sample -0.5 V", z="swept 0 -> 62000 in 16-count steps",
        settings="columns t, motor_steps, repeat, onset_z, adc",
        produced_by="scripts/stairs.py", passage="sessions/2026-09-19-morning.md 3.4",
        caveat="the CSV has TWO data rows and both have an empty onset_z and adc: the "
               "record of finding nothing")
for n, w in (("fastwood_run1.log", "650 single approach steps with a 1,000-count sweep: "
                                   "nothing"),
             ("fastwood_1789819103.csv", "the 651 rows behind it, none with a hit")):
    add(S19M, n, w, bias="38229 = sample -0.5 V", z="swept after each step",
        settings="columns t, steps, z_hit, adc; 0.69 s per step",
        produced_by="scripts/fastwood.py", passage="sessions/2026-09-19-morning.md 3.5")
add(S19M, "zjump_run1.log", "read check and Z-jump transient test: 2 of 4 upward "
    "0 -> 28,000 jumps put 3,714 (0 V) and 1,026 (-0.5 V) counts on the next read",
    bias="0 V and -0.5 V", z="jumped 0 -> 28000 and 0 -> 60000, and downward",
    settings="reads alive, sd 29-56, no dropped replies",
    produced_by="scripts/zjump.py", passage="sessions/2026-09-19-morning.md 3.5",
    caveat="this script has NO self-test")
add(S19M, "nudge_run1.log", "nudges judged with the hand OFF: 11 IN events at random Z, "
    "FAR within one or two sweeps", bias="38229 = sample -0.5 V", z="full sweep each time",
    settings="a full sweep every ~0.4 s; verdicts FAR / PAST / IN RANGE",
    produced_by="scripts/nudge.py", passage="sessions/2026-09-19-morning.md 3.6",
    caveat="the log prints only CHANGES of state, so how many nudges there were is NOT "
           "RECORDED and some IN events may be one nudge")
add(S19M, "touchtest_run1.log", "touching the screw head WITHOUT turning, bias flipping: "
    "no effect at all", bias="alternating +-0.5 V", z="20000",
    settings="hands off: bias-flip signal -0.1 +- 6.2 counts, read sd 46.5, 153 periods; "
             "touching: -0.8 +- 6.1, sd 46.3, 88 periods",
    produced_by="scripts/touchtest.py", passage="sessions/2026-09-19-morning.md 3.6",
    caveat="this script has NO self-test")
for n, w in (("fastwood_run2_chunk20.log", "20-step chunks: found at Z 51,000 after 200 "
                                           "steps"),
             ("fastwood_1789820034.csv", "the 11 rows behind it, one with a hit")):
    add(S19M, n, w, bias="38229 = sample -0.5 V", z="swept after each chunk",
        settings="columns t, steps, z_hit, adc; chunks of 20 motor steps",
        produced_by="scripts/fastwood.py", passage="sessions/2026-09-19-morning.md 3.7")
for n, w in (("ztest_run2.log", "30 s later: in contact even at Z 0 (STUCK)"),
             ("ztest_1789820073.csv", "the 45 points of that stuck attempt")):
    add(S19M, n, w, bias="38229 = sample -0.5 V", z="0 upward", settings=_zt,
        produced_by="scripts/ztest.py", passage="sessions/2026-09-19-morning.md 3.7",
        excluded="status STUCK: still in contact with Z fully retracted, so no cycles ran "
                 "and it has no results")
for n, w in (("apz_run1.log", "20-step chunks then the Z test the instant it found the "
                              "gold"),
             ("apz_approach_1789822231.csv", "the approach part: found at Z 17,000 after "
                                             "9 chunks (180 steps)"),
             ("apz_ztest_1789822231.csv", "the Z-test part: 30 cycles, 27 ending at Z 0 "
                                          "in contact")):
    add(S19M, n, w, bias="38229 = sample -0.5 V", z="0 upward",
        settings=_zt + "; the approach CSV has columns t, chunks, z_hit, adc",
        produced_by="scripts/approach_then_ztest.py",
        passage="sessions/2026-09-19-morning.md 3.8",
        excluded="THE Z-TEST FIGURES ARE EXCLUDED FROM THE RESULTS: the gold was moving "
                 "through the whole run and followed the retracting tip in at "
                 "~14,000-16,000 counts per second",
        caveat="its sweep ran at 1,000-count steps, not the 250 the script set (the "
               "default-argument bug)")
add(S19M, "release_watch_run1.log", "released, then watched with the motor and hands "
    "still: 19,000 -> 42,000 -> FAR -> back at ~6,000-8,000",
    bias="38229 = sample -0.5 V", z="full sweep every 3 s",
    settings="1,000-count Z steps (the bug); 'FAR' means beyond Z 62,000",
    produced_by="scripts/release_and_watch.py",
    passage="sessions/2026-09-19-morning.md 3.9",
    caveat="NO CSV - stopped to start the Z test. This log is the ONLY record of the "
           "headline gap-motion measurement")
for n, w in (("ztest_run3.log", "THE Z TEST: 30 cycles at sample -0.5 V"),
             ("ztest_1789822585.csv", "its 24,379 points")):
    add(S19M, n, w, bias="38229 = sample -0.5 V", z="cycled in and out about the contact",
        settings=_zt + "; 30 cycles", produced_by="scripts/ztest.py",
        passage="sessions/2026-09-19-morning.md 3.10")
add(S19M, "bias_series_run1.log", "the Z test repeated at -0.1, +0.5, +0.1 and -0.5 V, "
    "20 cycles each", bias="33860, 27307, 31676, 38229 in that order",
    z="cycled in and out", settings="20 cycles per bias, back to back",
    produced_by="scripts/bias_series.py", passage="sessions/2026-09-19-morning.md 3.11")
for n, code, v in (("bias_m01V_1789822770.csv", 33860, "-0.1 V"),
                   ("bias_p05V_1789822770.csv", 27307, "+0.5 V"),
                   ("bias_p01V_1789822770.csv", 31676, "+0.1 V"),
                   ("bias_m05V_1789822770.csv", 38229, "-0.5 V")):
    add(S19M, n, "Z test at sample %s, 20 cycles" % v,
        bias="%d = sample %s" % (code, v), z="cycled in and out",
        settings=_zt + "; 20 cycles", produced_by="scripts/bias_series.py",
        passage="sessions/2026-09-19-morning.md 3.11")
add(S19M, "tuned_scans_run1.log", "scans with the loop constant set to 1,800: all six "
    "aborted, two at the top clamp and four at the bottom",
    bias="38229 = sample -0.5 V", z="loop-controlled",
    settings="scan2.scan with COUNTS_PER_DECADE = 1800, each scan followed by an X-held "
             "control", produced_by="scripts/tuned_scans.py",
    passage="sessions/2026-09-19-morning.md 3.12")
for i in range(3):
    add(S19M, "tuned_s3k_scan%d.csv" % i, "tuned constant-current scan %d of 3" % i,
        bias="38229 = sample -0.5 V", z="loop-controlled, clamp 12000-48000",
        settings="+-3000 X, 21 x 11 pixels, loop constant 1,800 counts per decade; "
                 + _scan_note,
        produced_by="scripts/tuned_scans.py", passage="sessions/2026-09-19-morning.md 3.12",
        excluded="ALL SIX TUNED IMAGES ABORTED at a clamp. The session log's conclusion "
                 "is 'the tuned loop never held on hardware today'")
    add(S19M, "tuned_s3k_xheld%d.csv" % i, "X-HELD CONTROL %d of 3 for the tuned scans" % i,
        bias="38229 = sample -0.5 V", z="loop-controlled, clamp 12000-48000",
        settings="same as the scan it follows; " + _scan_note,
        produced_by="scripts/tuned_scans.py", passage="sessions/2026-09-19-morning.md 3.12",
        excluded="aborted at a clamp, like the scans")
for n, w in (("where_run1.log", "contact even at Z 0 from 13:07:11, rising"),
             ("where_run2.log", "the same check again, 13:09")):
    add(S19M, n, w, bias="38229 = sample -0.5 V", z="0 and swept",
        settings="prints the reading at Z 0 and the onset per sweep",
        produced_by="scripts/where.py", passage="sessions/2026-09-19-morning.md 3.12",
        caveat="NO self-test; and its sweep ran at 1,000-count steps (the bug)")
for n, w in (("release_watch_run2.log", "+1,200 retract steps in 20-step chunks: still "
                                        "railed"),
             ("release_watch_1789823258.csv", "its CSV - header only, no rows")):
    add(S19M, n, w, bias="38229 = sample -0.5 V", z="0",
        settings="columns t, state, onset_z",
        produced_by="scripts/release_and_watch.py",
        passage="sessions/2026-09-19-morning.md 3.12",
        caveat="the CSV holds a header and NO DATA ROWS because the release never "
               "cleared, so the watch phase never ran")
add(S19M, "passive_z0_run1.log", "Z 0, nothing moving, railed until hand-set 5",
    bias="38229 = sample -0.5 V", z="0", settings="passive log",
    produced_by="scripts/passive_z0.py", passage="sessions/2026-09-19-morning.md 3.12",
    caveat="NO CSV - stopped for the hand-set; and the script has NO self-test")
add(S19M, "swing_log_run1.log", "full sweeps every 5 s with the motor still: FAR on "
    "every sweep for 11.8 minutes", bias="38229 = sample -0.5 V",
    z="full sweep every 5 s",
    settings="the log prints only CHANGES of state, so its single FAR line is the whole "
             "record", produced_by="scripts/swing_log.py",
    passage="sessions/2026-09-19-morning.md 3.14",
    caveat="NO CSV - stopped for the shutdown. And a sweep in which every read failed "
           "would also score FAR; the reads were healthy before and after, so that is "
           "unlikely but not excluded")
add(S19M, "storage_backoff_watch.log", "the watcher started for the storage back-off; it "
    "lost the port when the USB came out",
    bias=SRC % "scripts/live_backoff_z0.py imports 2026-09-19-bench/scripts/"
               "live_backoff.py, which writes BIAS 38229 at line 18",
    z="held at 0 (live_backoff_z0.py sets live_backoff.MID = 0)",
    settings="ends in a SerialException, which was expected",
    produced_by="a watcher script", passage="sessions/2026-09-19-morning.md 3.14, 10",
    caveat="THE LAST RECORD OF THE ELECTRICAL STATE before power-down")



# ---------------------------------------------------------------- markdown

def _md(text):
    """Escape the characters that break a markdown table cell."""
    return (text or "").replace("|", "/").replace("\n", " ").strip()


def write_markdown(rows):
    out = os.path.join(ANALYSIS, "DATA_INVENTORY.md")
    by = {}
    for r in rows:
        by.setdefault(r["session"], []).append(r)
    L = []
    A = L.append
    A("# Data inventory - every raw bench file in this repository")
    A("")
    A("**Generated by `deliverables/2026-09-19-pause/analysis/code/build_inventory.py`.** "
      "Re-run it with")
    A("")
    A("```bash")
    A("python3 deliverables/2026-09-19-pause/analysis/code/build_inventory.py")
    A("```")
    A("")
    A("The machine-readable version is `data_inventory.csv` in this directory, with one "
      "row per file and")
    A("the same fields. **Nothing in `sessions/data/` was modified.**")
    A("")
    A("## What is here")
    A("")
    A("| | |")
    A("|---|---|")
    A("| Files inventoried | **%d** across four session directories |" % len(rows))
    A("| Of those, raw data | **%d** (%d `.csv`, %d `.log`, %d `.json`) |"
      % (sum(1 for r in rows if r["kind"] in ("csv", "log", "json")),
         sum(1 for r in rows if r["kind"] == "csv"),
         sum(1 for r in rows if r["kind"] == "log"),
         sum(1 for r in rows if r["kind"] == "json")))
    A("| The rest | %d transcribed console notes (`.md`) that are prose, not data |"
      % sum(1 for r in rows if r["kind"] == "md"))
    A("| Scripts kept as provenance | **82** in the four `scripts/` directories |")
    A("| Files the session logs EXCLUDE from results | **%d** |"
      % sum(1 for r in rows if r["excluded_why"]))
    A("| Files carrying a caveat that changes how they may be read | **%d** |"
      % sum(1 for r in rows if r["caveat"]))
    A("| Empty files (zero bytes) | **%d** |" % sum(1 for r in rows if r["bytes"] == 0))
    A("")
    A("> **A count to correct.** The brief for this work says 161 data files. The four "
      "directories hold")
    A("> **163** (78 `.csv` + 83 `.log` + 2 `.json`), plus 4 `README.md`, 2 transcribed "
      "console notes and")
    A("> 82 scripts: **251 files in total**. `SOURCE_INVENTORY.md`'s own per-directory "
      "numbers already sum")
    A("> to 163; only the brief's prose says 161.")
    A("")
    A("## Where each file's settings came from")
    A("")
    A("**Not one data file is missing its bias or its Z parking** - but for a fifth of them "
      "the setting is")
    A("not where a reader would look for it. This is the failure mode `CLAUDE.md` section 3b "
      "is about, and")
    A("it is worth naming because the answer was already in the repository every time.")
    A("")
    A("| Where the bias had to be read from | Files |")
    A("|---|---|")
    for label, key in (("The session's data `README.md` or its session log - "
                        "where you would look", "session data README"),
                       ("**The producing script's own source**, committed in that "
                        "session's `scripts/` directory", "producing script"),
                       ("**The session log's code-changes section**, not the scan record "
                        "- see the note below", "code-changes"),
                       ("**The data file's own printed banner**", "own header"),
                       ("**Not recorded anywhere**", "genuinely unknown")):
        n = sum(1 for r in rows if key in r["metadata_source"])
        A("| %s | **%d** |" % (label, n))
    A("")
    A("**The 2026-09-17 scans are the sharpest case.** Their bias is not written beside "
      "them anywhere. It is")
    A("recoverable because `sessions/2026-09-17-bench.md` records, in its code-changes "
      "section, that")
    A("`stm_feedback_scan.py` *\"read a bias argument, printed it in its banner, and then "
      "ignored it - it")
    A("wrote `BIAS 38229` unconditionally... Every scan before that ran at -0.5 V whatever "
      "was typed\"*.")
    A("The fix is commented at `Code/pc/stm_feedback_scan.py:206-211`. So **every "
      "2026-09-17 scan was")
    A("taken at sample -0.5 V**, and the bug that made it so is also what makes it "
      "knowable. Credit for")
    A("finding it goes to the 2026-09-17 review team, who are named in that log.")
    A("")
    A("**The one genuine gap** is `sessions/data/2026-09-18-bench/approach3.log`: "
      "`stm_approach.py` did not")
    A("set a bias at that date, so the sample sat at whatever the previous command left, "
      "and no document")
    A("says what that was. **UNKNOWN.**")
    A("")
    A("## The four sessions, and why they cannot simply be pooled")
    A("")
    for sname in SESSIONS:
        m = SESSION_META[sname]
        A("### `%s` - %d files" % (sname, len(by[sname])))
        A("")
        A("| | |")
        A("|---|---|")
        A("| Session log | [`%s`](../../../%s) |" % (m["log"], m["log"]))
        A("| When | %s |" % m["when"])
        A("| Machine | %s |" % m["machine"])
        A("| **Tip** | %s |" % m["tip"])
        A("| **Sample** | %s |" % m["sample"])
        A("| Tip holder | %s |" % m["holder"])
        A("| ADC scatter, tip clear | %s |" % m["adcr_sd_clear"])
        A("| Z direction in force | %s |" % m["z_direction"])
        A("| Tools | %s |" % m["tool"])
        A("| **Read this before using the data** | %s |" % m["note"])
        A("")
    A("## Every file")
    A("")
    A("Columns: what the file is, what made it, the sample bias and Z parking it was taken "
      "under, the")
    A("run settings, and the session-log passage that describes it. `data_inventory.csv` "
      "carries the same")
    A("rows plus the raw column lists and the distinct values found in each setting column.")
    A("")
    for sname in SESSIONS:
        A("### `%s`" % sname)
        A("")
        A("| File | Rows | What it is | Bias | Z parking | Settings | Described in |")
        A("|---|---|---|---|---|---|---|")
        for r in sorted(by[sname], key=lambda r: r["file"]):
            A("| `%s` | %s | %s | %s | %s | %s | %s |"
              % (r["file"], r["rows"], _md(r["what_it_is"]), _md(r["bias"]),
                 _md(r["z_parking"]), _md(r["run_settings"]),
                 _md(r["session_log_passage"])))
        A("")
    A("## Files the session logs EXCLUDE from the results, and why")
    A("")
    A("These are not bad files. Each was taken deliberately and each is excluded for a "
      "reason the session")
    A("log states. **Using any of them as a result would contradict the record.**")
    A("")
    A("| File | Why it is excluded |")
    A("|---|---|")
    for r in rows:
        if r["excluded_why"]:
            A("| `%s/%s` | %s |" % (r["session"], r["file"], _md(r["excluded_why"])))
    A("")
    A("## Files that carry a caveat")
    A("")
    A("| File | Caveat |")
    A("|---|---|")
    for r in rows:
        if r["caveat"]:
            A("| `%s/%s` | %s |" % (r["session"], r["file"], _md(r["caveat"])))
    A("")
    A("## Empty, truncated and header-only files")
    A("")
    A("**Nothing in these four directories is corrupt.** Every `.csv` parses, every "
      "`.log` is readable text,")
    A("and both `.json` files load. What there is instead is files that are *short "
      "because the run was*")
    A("*short*, and the difference matters when a reader meets a two-row CSV.")
    A("")
    A("| File | Bytes | What it means |")
    A("|---|---|---|")
    for r in sorted(rows, key=lambda r: r["bytes"]):
        if r["bytes"] > 260:
            continue
        A("| `%s/%s` | %d | %s |"
          % (r["session"], r["file"], r["bytes"], _md(r["caveat"] or r["what_it_is"])))
    A("")
    A("## What the scripts directories contain")
    A("")
    A("| Session | Scripts | Note |")
    A("|---|---|---|")
    A("| `2026-09-17-bench` | **0** | **No scripts were kept for this session.** The scans "
      "came from `Code/pc/stm_feedback_scan.py` and from scratch variants of it that no "
      "longer exist. The diagnostic that stored the forward pass twice is one of those, "
      "and cannot now be inspected |")
    A("| `2026-09-18-bench` | 25 | Hardcode `COM3` and Jacob's Desktop path; **3** are "
      "`*_test.py` simulated-junction tests (`characterize_test.py`, `zcal3_test.py`, "
      "`fasttrack_test.py`), so 22 driving scripts share 3 tests |")
    A("| `2026-09-19-bench` | 37 | Same; **8** are `*_test.py` simulated-junction tests "
      "(`catch_and_scan_test.py`, `creeptrack_test.py`, `lift_test.py`, "
      "`live_backoff_test.py`, `live_touch_test.py`, `live_touch2_test.py`, "
      "`onset0_test.py`, `scan2_test.py`) |")
    A("| `2026-09-19-morning` | 20 | a different pattern: the test is INSIDE the script. "
      "14 carry a working `--test` self-test on simulated junctions; "
      "**six do not** (`live_backoff_z0.py`, `zjump.py`, `where.py`, `passive_z0.py`, "
      "`touchtest.py`, `final.py`). All twenty refuse options they do not recognise |")
    A("")
    A("**`scripts/final.py` was never run** - Jacob powered down first - so there is no "
      "tip-clear baseline")
    A("and no parked state recorded for the shutdown "
      "(`sessions/data/2026-09-19-morning/README.md`).")
    A("")
    with open(out, "w") as f:
        f.write("\n".join(L) + "\n")
    print("  wrote %s (%d lines)" % (os.path.relpath(out, REPO), len(L)))

# ---------------------------------------------------------------- mechanical scan

def describe(path):
    """Everything that can be read from the file itself."""
    size = os.path.getsize(path)
    ext = os.path.splitext(path)[1].lower()
    out = dict(bytes=size, kind=ext.lstrip("."), rows="", columns="", distinct="")
    if size == 0:
        out["rows"] = 0
        out["columns"] = "EMPTY FILE"
        return out
    if ext == ".csv":
        try:
            fields, rows = read_rows(path)
        except Exception as exc:                                  # pragma: no cover
            out["columns"] = "UNREADABLE: %s" % exc
            return out
        out["rows"] = len(rows)
        if fields and fields[0] in ("y", "y_offset"):
            out["columns"] = "%s, %s, then %d X DAC codes %s..%s" % (
                fields[0], fields[1], len(fields) - 2, fields[2], fields[-1])
            out["distinct"] = "%d pass rows" % len(rows)
        else:
            out["columns"] = ", ".join(fields)
            bits = []
            for k in ("bias", "z", "phase", "tag", "leg", "axis", "state", "dir"):
                if k in (fields or []):
                    vals = sorted({r[k] for r in rows if r.get(k) not in (None, "")})
                    bits.append("%s: %s" % (k, ", ".join(vals[:8]) +
                                            (" ... (%d values)" % len(vals)
                                             if len(vals) > 8 else "")))
            if "t" in (fields or []) and rows:
                t0, t1 = fnum(rows[0]["t"]), fnum(rows[-1]["t"])
                if t0 is not None and t1 is not None and t1 > t0:
                    bits.append("t spans %.2f" % (t1 - t0))
            out["distinct"] = "; ".join(bits)
    elif ext == ".json":
        import json
        try:
            d = json.load(open(path))
        except Exception as exc:                                  # pragma: no cover
            out["columns"] = "UNREADABLE: %s" % exc
            return out
        if isinstance(d, dict):
            out["columns"] = "JSON object, keys: " + ", ".join(d)
            out["rows"] = sum(len(v) for v in d.values() if hasattr(v, "__len__"))
        else:
            out["columns"] = "JSON array"
            out["rows"] = len(d)
    else:                                       # .log, .md
        with open(path, errors="replace") as f:
            lines = f.read().splitlines()
        out["rows"] = len(lines)
        out["columns"] = "free text"
        if lines:
            out["distinct"] = "first line: " + lines[0][:90]
    return out


def main():
    section("BUILDING THE INVENTORY")
    rows = []
    for sess in SESSIONS:
        d = os.path.join(DATA, sess)
        for name in sorted(os.listdir(d)):
            p = os.path.join(d, name)
            if not os.path.isfile(p) or name == "README.md":
                continue
            m = describe(p)
            c = C.get((sess, name), {})
            if not c:
                c = dict(what="NOT DESCRIBED in the session data README or the session "
                                "log - see the gaps table",
                         bias=U, z_parking=U, settings="", produced_by=U,
                         passage="NONE FOUND", excluded="", caveat="")
            sm = SESSION_META[sess]
            rows.append(dict(
                session=sess, file=name,
                path="sessions/data/%s/%s" % (sess, name),
                kind=m["kind"], bytes=m["bytes"], rows=m["rows"],
                columns=m["columns"], distinct_settings_in_file=m["distinct"],
                what_it_is=c["what"], produced_by=c["produced_by"],
                bias=c["bias"], z_parking=c["z_parking"],
                run_settings=c["settings"],
                session_log_passage=c["passage"],
                tip=sm["tip"], sample=sm["sample"],
                session_log=sm["log"], session_when=sm["when"],
                excluded_why=c["excluded"], caveat=c["caveat"],
                metadata_complete=("no" if (c["bias"] == U or c["z_parking"] == U
                                            or c["produced_by"] == U
                                            or c["passage"] in ("", "NONE FOUND"))
                                   else "yes")))
    for r in rows:
        b = r["bias"]
        if "producing script" in b:
            r["metadata_source"] = "recovered from the producing script's source"
        elif "its own banner" in b or "prints it in its own banner" in b:
            r["metadata_source"] = "read from the data file's own header"
        elif "NOT stated beside the scans" in b:
            r["metadata_source"] = ("recovered from the session log's code-changes "
                                    "section, not from the scan record")
        elif "NOT SET BY THE TOOL" in b:
            r["metadata_source"] = "NOT RECORDED ANYWHERE - genuinely unknown"
        else:
            r["metadata_source"] = "session data README or session log"
        del r["metadata_complete"]
    out = os.path.join(ANALYSIS, "data_inventory.csv")
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print("  %d data files inventoried -> %s" % (len(rows), os.path.relpath(out, REPO)))
    write_markdown(rows)
    by = {}
    for r in rows:
        by.setdefault(r["session"], []).append(r)
    for sname in SESSIONS:
        rs = by[sname]
        print("    %-22s %3d files  (%2d csv, %2d log, %d json, %d md)"
              % (sname, len(rs),
                 sum(1 for r in rs if r["kind"] == "csv"),
                 sum(1 for r in rs if r["kind"] == "log"),
                 sum(1 for r in rs if r["kind"] == "json"),
                 sum(1 for r in rs if r["kind"] == "md")))
    for label, key in (("session data README or session log", "session data README"),
                       ("recovered from the producing script's source", "producing script"),
                       ("read from the data file's own header", "own header"),
                       ("recovered from the session log's code-changes section, "
                        "not from the scan record", "code-changes"),
                       ("NOT RECORDED ANYWHERE - genuinely unknown", "genuinely unknown")):
        n = sum(1 for r in rows if key in r["metadata_source"])
        print("  bias provenance - %-70s %3d" % (label[:70], n))
    print("  empty files: %s"
          % ", ".join(r["path"] for r in rows if r["bytes"] == 0))
    print("  files the session logs exclude from results: %d"
          % sum(1 for r in rows if r["excluded_why"]))
    print("  files carrying a caveat: %d" % sum(1 for r in rows if r["caveat"]))
    return rows


if __name__ == "__main__":
    main()
