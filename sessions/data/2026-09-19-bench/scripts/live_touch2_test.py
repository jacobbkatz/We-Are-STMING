import live_touch2 as lt, random
random.seed(7)
st_ = {"t": 0.0, "bias": 32768, "contact_at": 5.0, "released_at": None}
cmds, beeps, lines = [], [], []
def write(s):
    cmds.append(s.strip())
    if s.startswith("BIAS"): st_["bias"] = int(s.split()[1])
def now(): return st_["t"]
def sleep(d):
    st_["t"] += d
    if st_["released_at"] is None and any("STOP" in l for l in lines): st_["released_at"] = st_["t"] + 10   # operator backs off 10 s later
def read():
    st_["t"] += 0.0003
    touching = st_["t"] >= st_["contact_at"] and (st_["released_at"] is None or st_["t"] < st_["released_at"])
    return int((5000 if touching and st_["bias"] == 38229 else 0) + random.gauss(0, 40))
res = lt.run(write, read, lambda n: beeps.append(n), now, sleep, lines.append, maxtime=120, wait=20)
ok = [("result clear", res == "clear"), ("stop beeps (6) then clear beeps (2)", beeps[:1] == [6] and beeps[-1] == 2),
      ("bias zeroed at contact", "BIAS 32768" in cmds[cmds.index("DACZ 32768") + 2:]),
      ("never moves Z except to midscale", all(c == "DACZ 32768" for c in cmds if c.startswith("DACZ"))),
      ("ends at bias 0", cmds[-2:] == ["BIAS 32768", "DACZ 32768"])]
for n, v in ok: print(("ok   " if v else "FAIL ") + n)
print(" | ".join(l for l in lines if "CONTACT" in l or "check" in l))
