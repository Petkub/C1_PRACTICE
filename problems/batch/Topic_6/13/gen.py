# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(613)
tests = []

def add(n, m, ops):
    assert 1 <= n <= 1000 and 1 <= m <= 1000 and 1 <= len(ops) <= 100000
    for r1, c1, r2, c2 in ops:
        assert 1 <= r1 <= r2 <= n and 1 <= c1 <= c2 <= m
    tests.append(f"{n} {m} {len(ops)}\n" + "".join(f"{a} {b} {c} {d}\n" for a, b, c, d in ops))

def rop(n, m, maxh=None, maxw=None):
    h = random.randint(1, maxh or n)
    w = random.randint(1, maxw or m)
    r1 = random.randint(1, n - h + 1)
    c1 = random.randint(1, m - w + 1)
    return (r1, c1, r1 + h - 1, c1 + w - 1)

# samples
add(4, 5, [(1, 1, 2, 3), (2, 2, 4, 4), (2, 3, 3, 5)])
add(2, 3, [(1, 1, 2, 3), (1, 1, 2, 3)])
add(1, 1, [(1, 1, 1, 1)])
add(1, 8, [(1, 2, 1, 4), (1, 6, 1, 7), (1, 4, 1, 6)])
add(3, 3, [(1, 1, 1, 1), (3, 3, 3, 3), (2, 2, 2, 2)])
# hidden
add(1, 1, [(1, 1, 1, 1)] * 5)
add(1000, 1000, [(1, 1, 1000, 1000)] * 100000)                  # every op covers the whole wall
add(1000, 1000, [rop(1000, 1000) for _ in range(50000)])
add(1000, 1000, [rop(1000, 1000, 50, 50) for _ in range(20000)])
add(1000, 1000, [(500, 500, 500, 500)])
add(1000, 1, [rop(1000, 1) for _ in range(3000)])
add(1, 1000, [rop(1, 1000) for _ in range(3000)])
add(6, 7, [rop(6, 7, 3, 3) for _ in range(5)])
add(10, 10, [rop(10, 10) for _ in range(12)])
add(30, 40, [rop(30, 40, 10, 10) for _ in range(40)])
add(200, 300, [rop(200, 300) for _ in range(500)])
add(1000, 1000, [(i, i, 1000, 1000) for i in range(1, 1001)])   # nested squares, corner reaches 1000
add(1000, 1000, [(1, j, 1000, j) for j in range(1, 1001, 2)])   # every second column once

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
