# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(905)
C = 10**9
tests = []

def add(pts, ops):
    n, m = len(pts), len(ops)
    assert 1 <= n <= 100_000 and 1 <= m <= 100_000
    lines = [f"{n} {m}"]
    for x, y in pts:
        assert -C <= x <= C and -C <= y <= C
        lines.append(f"{x} {y}")
    for o in ops:
        if isinstance(o, tuple):
            assert -10_000 <= o[0] <= 10_000 and -10_000 <= o[1] <= 10_000
            lines.append(f"T {o[0]} {o[1]}")
        else:
            assert o in "RXY"
            lines.append(o)
    tests.append("\n".join(lines) + "\n")

def rpts(n, lim):
    return [(random.randint(-lim, lim), random.randint(-lim, lim)) for _ in range(n)]

def rops(m, ptrans, lim):
    out = []
    for _ in range(m):
        if random.random() < ptrans:
            out.append((random.randint(-lim, lim), random.randint(-lim, lim)))
        else:
            out.append(random.choice("RXY"))
    return out

# samples
add([(1, 2)], ["R", (5, 0), "X"])
add([(3, -4), (0, 0)], ["R", "R", (-1, -1)])
add([(2, 7), (-5, 1)], ["X", "Y"])
add([(1, 0), (0, 1)], [(2, 3), "R", "R"])
add([(10, -10)], ["Y", (-3, 4), "R", "X"])
# hidden
add([(0, 0)], ["R"])
add([(C, C), (-C, -C), (C, -C)], [(10_000, 10_000)] * 1000)
add(rpts(10, C) + [(C, C), (-C, -C)], [(10_000, -10_000)] * 50_000 + ["R", "R"] + [(10_000, 10_000)] * 49_998)
add(rpts(100_000, 9), rops(100_000, 0.2, 9999))
add(rpts(15_000, C), rops(20_000, 0.5, 10_000))
add(rpts(50, 1000), rops(200, 0.3, 50))
add(rpts(7, 20), ["R", "X", "R", "Y", "R"])
add(rpts(5, 10), rops(10, 0.5, 5))
add(rpts(300, C), rops(300, 0.5, 10_000))
add(rpts(10, 50), ["X"] * 7)

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
