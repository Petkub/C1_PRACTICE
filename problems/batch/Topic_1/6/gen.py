# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(1006)
G = 10**9
tests = []

def add(qs):
    assert 1 <= len(qs) <= 100_000
    for a, b, c, d in qs:
        assert all(-G <= v <= G for v in (a, b, c, d)) and b != 0 and d != 0
    tests.append(f"{len(qs)}\n" + "".join(f"{a} {b} {c} {d}\n" for a, b, c, d in qs))

def nz(lo, hi):
    while True:
        v = random.randint(lo, hi)
        if v != 0:
            return v

def flip(a, b):
    # same value, random sign placement
    return (-a, -b) if random.random() < 0.5 else (a, b)

def near(m):
    # two fractions that are equal or extremely close, with values up to m
    x = random.randint(3, m)
    kind = random.randint(0, 3)
    if kind == 0:
        a, b, c, d = x, x - 1, x - 1, x - 2
    elif kind == 1:
        p, q = random.randint(1, 1000), random.randint(1, 1000)
        k1, k2 = random.randint(1, m // 1000), random.randint(1, m // 1000)
        a, b, c, d = p * k1, q * k1, p * k2, q * k2
    elif kind == 2:
        a, b, c, d = 1, x, 1, x - 1
    else:
        a, b, c, d = x - 1, x, x - 2, x - 1
    if random.random() < 0.5:
        a, c = -a, -c
    if random.random() < 0.5:
        a, b, c, d = c, d, a, b
    a, b = flip(a, b)
    c, d = flip(c, d)
    return (a, b, c, d)

# samples
add([(1, 2, 2, 4), (3, 4, 2, 3), (-1, 3, 1, -2)])
add([(2, -3, -4, 6), (5, -7, 0, 1), (0, 5, 0, -3)])
add([(-3, -4, 3, 4), (-7, 2, -10, 3), (7, -2, 10, -3)])
add([(1, 1000000000, -1, -999999999)])
add([(999, 1000, 998, 999), (-5, 1, 5, -1), (6, -4, -3, 2)])
# hidden, small
R = range(-4, 5)
add([(a, b, c, d) for a in R for b in R for c in R for d in R if b != 0 and d != 0])
add([(random.randint(-30, 30), nz(-30, 30), random.randint(-30, 30), nz(-30, 30)) for _ in range(5000)])
add([near(1000) for _ in range(5000)])
# hidden, big
add([(G, G - 1, G - 1, G - 2), (G - 1, G - 2, G, G - 1), (-G, G - 1, -(G - 1), G - 2), (G, -(G - 1), G - 1, -(G - 2)),
     (G, 1, G, 1), (-G, 1, G, -1), (G, -1, -G, 1), (G, -1, G, 1), (-G, -G, G, G), (1, G, 1, -G), (0, -G, 0, G),
     (G, G, -G, -G), (-G, -1, G, 1), (G - 1, G, G - 2, G - 1), (1, G, 1, G - 1), (-1, G, -1, G - 1)])
add([near(G) for _ in range(12_000)])
add([near(G) for _ in range(12_000)])
add([(random.randint(-G, G), nz(-G, G), random.randint(-G, G), nz(-G, G)) for _ in range(12_000)])
add([(random.randint(-G, G), nz(-10, 10), random.randint(-G, G), nz(-10, 10)) for _ in range(12_000)])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
