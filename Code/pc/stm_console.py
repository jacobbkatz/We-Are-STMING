#!/usr/bin/env python3
"""
Minimal serial console for the red-panda-stm Teensy firmware.

Two firmware quirks drive the whole design of this script:

1. checkSerial() starts reading as soon as ONE byte is available, then
   immediately reads four. Anything that sends per-keystroke (PlatformIO's
   monitor, PuTTY, screen, minicom) loses the race and the command is
   silently discarded. So every command goes out as a single write().

2. Holding the port open blocks teensy_reboot during upload, which makes the
   Teensy Loader fall back to asking for the PROGRAM button on every flash.
   So one-shot mode opens the port, talks, and closes it again. Interactive
   mode releases the port with 'free' before you upload.

Usage:
    python stm_console.py GSTS
    python stm_console.py MTMV 512
    python stm_console.py BIAS 33000
    python stm_console.py              # interactive
"""

import argparse
import sys
import time

import serial
from serial.tools import list_ports

# Only these three ever print anything back. Everything else acts silently, so
# waiting on a reply from them just burns the timeout.
REPLY_COMMANDS = {"GSTS", "ADCR", "IVGE"}

# Silent commands that also BLOCK the firmware loop while they run. We have to
# wait them out anyway, or the next command lands while loop() is still stuck
# and gets read as garbage.
#   MTMV: setSpeed(2) at 2048 steps/rev = 68.3 steps/s, duration set by count.
#   TEST: 500 cycles x 1 ms on each of Z, X, Y, plus two 1 s pauses = ~3.5 s.
STEPS_PER_SECOND = 2.0 * 2048 / 60.0
BLOCKING_COMMANDS = {"TEST": 3.5, "APRH": 120.0, "IVME": 60.0, "SCST": 300.0}
DEFAULT_TIMEOUT = 3.0


def blocking_duration(command, args):
    """Seconds the firmware will be unresponsive, or None if it replies."""
    command = command.upper()
    if command == "TONE":
        # play_tone() loops for the requested duration with interrupts on and
        # never reads serial, so the firmware is unresponsive for that long.
        try:
            return int(args[1]) / 1000.0
        except (IndexError, ValueError):
            return 2.0
    if command == "MTMV":
        try:
            return abs(int(args[0])) / STEPS_PER_SECOND
        except (IndexError, ValueError):
            return 30.0
    return BLOCKING_COMMANDS.get(command)

# Corrected DAC ranges. The firmware comments claim X/Y are +/-5 V; the
# AD5761 range bits actually configured are 101 = +/-3 V. Z is 000 = +/-10 V.
DAC_FULL_SCALE = {"bias": 3.0, "dac_z": 10.0, "dac_x": 3.0, "dac_y": 3.0}

STATUS_FIELDS = [
    "bias", "dac_z", "dac_x", "dac_y", "adc",
    "steps", "is_approaching", "is_const_current", "is_scanning", "time_millis",
]


# From stm_control.py: 100 MOhm feedback resistor, 10.24 V ADC full scale.
def adc_to_amp(adc):
    return 1.0 * adc / 32768 * 10.24 / 100e6


def code_to_volts(code, full_scale):
    """DAC code 0-65535, centre 32768 = 0 V."""
    return (code - 32768) / 32768.0 * full_scale


def find_teensy():
    """PJRC vendor ID is 0x16C0. PID 0x0483 is a running sketch."""
    for p in list_ports.comports():
        if p.vid == 0x16C0:
            return p.device
    ports = list_ports.comports()
    if len(ports) == 1:
        return ports[0].device
    return None


def build_frame(command, args):
    """One write, and a newline only when there is an argument.

    Serial.parseInt() consumes the non-digit that terminates the number, so a
    trailing newline is eaten cleanly. On a no-argument command parseInt is
    never called, and a stray newline would sit in the buffer and corrupt the
    next command, so we leave it off.
    """
    command = command.upper()
    if len(command) != 4:
        raise ValueError("commands are exactly 4 characters, got %r" % command)
    if not args:
        return command.encode()
    return (command + " " + " ".join(str(a) for a in args) + "\n").encode()


def send(port, command, args, timeout=None):
    frame = build_frame(command, args)

    port.reset_input_buffer()
    port.write(frame)
    port.flush()

    if command.upper() not in REPLY_COMMANDS:
        # Silent command. If it also blocks, wait it out with a little margin
        # so the next command does not arrive mid-move.
        busy = blocking_duration(command, args)
        if busy:
            print("  (firmware busy ~%.1f s, waiting)" % busy)
            time.sleep(busy + 1.5)
        else:
            time.sleep(0.2)
        return ""

    if timeout is None:
        timeout = DEFAULT_TIMEOUT
    deadline = time.time() + timeout
    buf = b""
    while time.time() < deadline:
        chunk = port.read(256)
        if chunk:
            buf += chunk
            if buf.endswith(b"\n"):
                break
        elif buf:
            break
    return buf.decode("ascii", "replace").strip()


def describe_status(line):
    parts = line.split(",")
    if len(parts) != len(STATUS_FIELDS):
        return None
    try:
        vals = [int(p) for p in parts]
    except ValueError:
        return None

    out = []
    for name, val in zip(STATUS_FIELDS, vals):
        if name in DAC_FULL_SCALE:
            volts = code_to_volts(val, DAC_FULL_SCALE[name])
            out.append("  %-16s %6d   -> %+.3f V commanded" % (name, val, volts))
        elif name == "adc":
            out.append("  %-16s %6d   (%.3g A)" % (name, val, adc_to_amp(val)))
        elif name == "time_millis":
            out.append("  %-16s %6d   (uptime %.1f s)" % (name, val, val / 1000.0))
        else:
            out.append("  %-16s %6d" % (name, val))

    # The DAC fields are STMStatus bookkeeping, not a readback from the chip.
    # reset() writes the control register but never a DAC data register, so
    # after boot these are the struct's initial zeros and say nothing about
    # what the AD5761 outputs are actually doing. Only a meter settles that.
    if vals[0] == vals[1] == vals[2] == vals[3] == 0:
        out.append("")
        out.append("  note: all four DAC fields are 0, the STMStatus boot value.")
        out.append("  Nothing has commanded a DAC yet, so these are placeholders,")
        out.append("  not measurements. See DAC_BOOT_STATE.md before powering analog.")
    return "\n".join(out)


def report(command, response):
    if not response:
        if command.upper() in REPLY_COMMANDS:
            print("(no response)")
            print("  This command should always answer. If the port is right,")
            print("  check nothing else has it open and that the board has booted")
            print("  (reset() runs 4 DAC resets, ~0.5 s, before it answers).")
        else:
            print("  sent (this command replies with nothing; confirm with GSTS)")
        return
    print(response)
    if command.upper() == "GSTS":
        pretty = describe_status(response)
        if pretty:
            print(pretty)


def interactive(portname):
    print("STM console on %s.  Ctrl-C or 'quit' to exit." % portname)
    print("Commands are 4 chars: GSTS MTMV BIAS ADCR TEST TONE RSET STOP DACX DACY DACZ")
    print("'free' closes the port so you can upload; it reopens on the next command.\n")

    port = serial.Serial(portname, 115200, timeout=0.2)
    time.sleep(1.0)
    try:
        while True:
            try:
                raw = input("stm> ").strip()
            except EOFError:
                break
            if not raw:
                continue
            if raw.lower() in ("quit", "exit"):
                break
            if raw.lower() == "free":
                if port and port.is_open:
                    port.close()
                    print("port released, safe to upload")
                continue

            if port is None or not port.is_open:
                port = serial.Serial(portname, 115200, timeout=0.2)
                time.sleep(1.0)

            bits = raw.split()
            try:
                response = send(port, bits[0], bits[1:])
            except ValueError as e:
                print("error:", e)
                continue
            report(bits[0], response)
    except KeyboardInterrupt:
        print()
    finally:
        if port and port.is_open:
            port.close()
        print("port closed")


def main():
    ap = argparse.ArgumentParser(description="Serial console for red-panda-stm Teensy firmware")
    ap.add_argument("command", nargs="?", help="4-character command, e.g. GSTS")
    ap.add_argument("args", nargs="*", help="numeric arguments")
    ap.add_argument("-p", "--port", help="serial port (auto-detects the Teensy by VID 0x16C0)")
    ap.add_argument("-t", "--timeout", type=float, help="override read timeout in seconds")
    ap.add_argument("-n", "--repeat", type=int, default=1, help="send the command N times")
    opts = ap.parse_args()

    portname = opts.port or find_teensy()
    if not portname:
        print("No Teensy found. Ports seen:")
        for p in list_ports.comports():
            print("  %s  %s" % (p.device, p.description))
        return 1

    if not opts.command:
        interactive(portname)
        return 0

    try:
        port = serial.Serial(portname, 115200, timeout=0.2)
    except serial.SerialException as e:
        print("Could not open %s: %s" % (portname, e))
        print("Something else has the port. A leftover PlatformIO 'device monitor'")
        print("is the usual culprit, and it also blocks teensy_reboot during upload.")
        return 1

    with port:
        time.sleep(1.0)
        for i in range(opts.repeat):
            response = send(port, opts.command, opts.args, opts.timeout)
            if opts.repeat > 1:
                print("[%d/%d] " % (i + 1, opts.repeat), end="")
            report(opts.command, response)
            if i + 1 < opts.repeat:
                time.sleep(0.3)
    return 0


if __name__ == "__main__":
    sys.exit(main())
