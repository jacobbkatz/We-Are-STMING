"""Bias-flip confirmation of a candidate contact.

Creeps Z from the retracted end toward the sample at -0.5 V sample bias until
the reading crosses ONSET counts (2 of 3 reads), then at that Z reads the ADC
at -0.5 V, +0.5 V and 0 V sample, then retracts. Z is retracted on every exit.
A real junction follows the bias; noise does not.
"""
import sys
import time

import serial

sys.path.insert(0, r"C:\Users\jacob\OneDrive\Desktop\CUsersyournameSTM\Code\pc")
from stm_approach import Device  # noqa: E402

Z_RETRACT = 10000
Z_LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 27000   # never go past this
Z_STEP = int(sys.argv[2]) if len(sys.argv) > 2 else 50
ONSET = int(sys.argv[3]) if len(sys.argv) > 3 else 3000
BIAS_NEG = 38229    # sample -0.5 V
BIAS_POS = 27307    # sample +0.5 V
BIAS_ZERO = 32768


def bias(port, code):
    port.reset_input_buffer()
    port.write(("BIAS %d\n" % code).encode())
    port.flush()
    time.sleep(0.05)


def reads(dev, n):
    out = []
    for _ in range(n):
        v = dev.read_adc()
        if v is not None:
            out.append(v)
    return out


port = serial.Serial("COM3", 115200, timeout=0.2)
dev = Device(port)
try:
    bias(port, BIAS_NEG)
    dev.set_z(Z_RETRACT)
    time.sleep(0.3)
    base = reads(dev, 5)
    print("baseline at Z %d, -0.5 V: %s" % (Z_RETRACT, base))
    b = sum(base) / float(len(base))
    found = None
    z = Z_RETRACT
    while z <= Z_LIMIT:
        dev.set_z(z)
        r = reads(dev, 3)
        hits = sum(1 for v in r if abs(v - b) >= ONSET)
        if hits >= 2:
            found = z
            print("onset at Z %d: %s" % (z, r))
            break
        z += Z_STEP
    if found is None:
        print("no onset up to Z %d" % Z_LIMIT)
    else:
        t0 = time.time()
        neg = reads(dev, 5)
        bias(port, BIAS_POS)
        pos = reads(dev, 5)
        bias(port, BIAS_ZERO)
        zero = reads(dev, 5)
        bias(port, BIAS_NEG)
        neg2 = reads(dev, 5)
        print("at Z %d, over %.1f s:" % (found, time.time() - t0))
        print("  sample -0.5 V: %s" % neg)
        print("  sample +0.5 V: %s" % pos)
        print("  sample  0   V: %s" % zero)
        print("  sample -0.5 V: %s" % neg2)
finally:
    dev.set_z(Z_RETRACT)
    time.sleep(0.05)
    print("Z retracted to %d" % Z_RETRACT)
    port.close()
