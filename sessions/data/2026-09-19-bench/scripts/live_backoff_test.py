import live_backoff as lb, random
random.seed(11)
s = {"t": 0.0, "gap": 20.0}          # gap in arbitrary units; operator turns in at 1/s, backs off at 0.3/s after beeps
beeps, lines, cmds = [], [], []
phase = {"p": 1}
def write(c): cmds.append(c.strip())
def now(): return s["t"]
def sleep(d): s["t"] += d
def read():
    s["t"] += 0.0003
    if phase["p"] == 1: s["gap"] -= 0.0003 * 1.0
    else: s["gap"] += 0.0003 * 0.3
    cur = 5000 * 10 ** (-s["gap"] / 0.5) if s["gap"] < 3 else 0
    return int(min(32767, cur) + random.gauss(0, 30))
def beep(n):
    beeps.append(n)
    if n == 6: phase["p"] = 2
res = lb.run(write, read, beep, now, sleep, lines.append, maxtime=200)
final_gap = s["gap"]
ok = [("clear", res == "clear"), ("6 beeps then ticks then 2", beeps[0] == 6 and beeps[-1] == 2 and 1 in beeps),
      ("stopped just outside detection (gap %.2f)" % final_gap, 0 < final_gap < 2.5),
      ("never moved Z off midscale", all(c == "DACZ 32768" for c in cmds if c.startswith("DACZ"))),
      ("bias left ON at -0.5 V", [c for c in cmds if c.startswith("BIAS")][-1] == "BIAS 38229")]
for n, v in ok: print(("ok   " if v else "FAIL ") + n)
