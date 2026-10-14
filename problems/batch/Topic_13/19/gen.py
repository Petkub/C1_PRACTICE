# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(1319)
MAXP, MAXQ = 10**6, 10**4
tests = []

def add(orders):
    n = len(orders)
    assert 1 <= n <= 100_000
    lines = [str(n)]
    for t, p, q in orders:
        assert t in ("BUY", "SELL") and 1 <= p <= MAXP and 1 <= q <= MAXQ
        lines.append(f"{t} {p} {q}")
    tests.append("\n".join(lines) + "\n")

def rnd(n, plo, phi, qmax, pbuy=0.5):
    return [("BUY" if random.random() < pbuy else "SELL", random.randint(plo, phi), random.randint(1, qmax))
            for _ in range(n)]

def walk(n, mid, spread, qmax):
    """prices around a slowly moving middle price"""
    res = []
    for _ in range(n):
        mid = min(MAXP - spread, max(spread + 1, mid + random.randint(-2, 2)))
        t = random.choice(("BUY", "SELL"))
        off = random.randint(-spread // 3, spread)
        p = mid - off if t == "BUY" else mid + off
        res.append((t, p, random.randint(1, qmax)))
    return res

# samples
add([("SELL", 100, 5), ("SELL", 90, 3), ("BUY", 95, 4), ("BUY", 120, 6), ("SELL", 80, 10)])
add([("BUY", 50, 2), ("BUY", 50, 3), ("BUY", 60, 1), ("SELL", 40, 4), ("SELL", 50, 5)])
add([("BUY", 7, 3)])
add([("BUY", MAXP, MAXQ), ("SELL", 1, MAXQ)])
add([("SELL", 10, 5), ("BUY", 10, 2), ("BUY", 12, 2), ("BUY", 9, 4), ("SELL", 9, 6), ("BUY", 10, 5)])
add([("SELL", 5, 1), ("SELL", 5, 1), ("SELL", 4, 1), ("BUY", 3, 2), ("BUY", 5, 4), ("SELL", 3, 1)])
# hidden (small)
add(rnd(30, 1, 10, 5))
add(rnd(500, 1, 20, 30))
add(rnd(3000, 1, 5, 100))                                   # many equal prices
add(walk(3000, 1000, 60, 50))
add([("BUY", MAXP, MAXQ) if i % 2 else ("SELL", 1, MAXQ) for i in range(2000)])
# large
first = [("BUY", random.randint(1, 499_999), random.randint(1, 50)) if random.random() < 0.5
         else ("SELL", random.randint(500_001, MAXP), random.randint(1, 50)) for _ in range(50_000)]
second = []
for _ in range(50_000):                                     # small orders hitting the best waiting prices
    if random.random() < 0.5:
        second.append(("BUY", random.randint(500_001, 520_000), random.randint(1, 20)))
    else:
        second.append(("SELL", random.randint(480_000, 499_999), random.randint(1, 20)))
add(first + second)
add(walk(50_000, 500, 200, MAXQ))
small = [("SELL", random.randint(1, 30_000), 1) for _ in range(30_000)]
small += [("BUY", MAXP, MAXQ) for _ in range(4)] + rnd(10_000, 1, MAXP, MAXQ)
add(small)                                                  # big orders sweeping many price levels

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
