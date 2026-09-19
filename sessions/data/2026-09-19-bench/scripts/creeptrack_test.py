import creeptrack as ct
class Sim:
    """Surface creeps toward the tip at `rate` counts/s; motor +1 moves it away by `per`;
    `toward` says which Z end extends. Current ~ 10**((reach - gap)/cpd) above threshold."""
    def __init__(s, toward, rate=300.0, per=250.0):
        s.toward, s.rate, s.per, s.t, s.z, s.gap0, s.motor_total = toward, rate, per, 0.0, ct.MID, 40000.0, 0
    def set_z(s, z): s.z = z; s.t += 0.002
    def set_bias(s, c): pass
    def motor(s, n): s.motor_total += n; s.t += 0.5
    def gap(s):
        reach = (s.z - ct.MID) * s.toward          # how far the tip reaches past midscale toward the gold
        return s.gap0 - s.rate * s.t + s.per * s.motor_total - reach
    def read_med(s, n):
        s.t += 0.0003 * n
        g = s.gap()
        return 3000 * 10 ** min(6, -g / 200.0) if g < 600 else 5
    def now(s): return s.t
    def sleep(s, d): s.t += d
for toward in (+1, -1):
    s = Sim(toward); lines = []
    touches = ct.run(s, s.read_med, s.now, s.sleep, 600, 5, 100, lines.append)
    halves = [h for _, _, h in touches]
    want = "high" if toward > 0 else "low"
    ok = len(touches) >= 3 and all(h == want for h in halves)
    print("toward %+d: %d touches, halves %s -> %s" % (toward, len(touches), sorted(set(halves)), "ok" if ok else "FAIL"))
    iv = [b[0] - a[0] for a, b in zip(touches, touches[1:])]
    print("   intervals (s):", iv[:6], "-> implied rate %.0f counts/s (true 300)" % (100 * 250 / (sum(iv) / len(iv))) if iv else "")
