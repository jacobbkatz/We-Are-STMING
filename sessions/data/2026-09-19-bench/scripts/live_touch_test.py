import random, live_touch as lt
random.seed(4)
cmds = []; beeps = []; lines = []
state = {"z": None, "t": 0.0}
def write(s):
    cmds.append(s.strip())
    if s.startswith("DACZ"): state["z"] = int(s.split()[1])
def now():
    state["t"] += 0.05; return state["t"]
def read():
    # surface approaches: current appears once t > 3 s at Z HOME; at Z 0 it is 10x smaller
    base = 0 if state["t"] < 3 else 3000 * (state["t"] - 3)
    if state["z"] == 0: base /= 10.0
    return int(base + random.gauss(0, 40))
lat = lt.run(write, read, lambda: beeps.append(state["t"]), now=now, out=lines.append, maxtime=8)
first_contact = next(i for i, l in enumerate(lines) if "CONTACT" in l)
ok = [
  ("latched", lat),
  ("Z pulled to 0 at contact", "DACZ 0" in cmds[:cmds.index("DACZ 0") + 1]),
  ("beeped", len(beeps) >= 1),
  ("stays latched after the drop", all("LATCHED" in l for l in lines[first_contact + 1:-1])),
  ("ends Z 0 and bias 0 V", cmds[-2:] == ["DACZ 0", "BIAS 32768"]),
  ("no Z command toward the sample after contact", all(c in ("DACZ 0", "BIAS 32768") for c in cmds[cmds.index("DACZ 0"):])),
]
for name, v in ok: print(("ok   " if v else "FAIL ") + name)
print(lines[first_contact])
raise SystemExit(0 if all(v for _, v in ok) else 1)
