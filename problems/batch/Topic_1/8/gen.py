# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(108)
G = 10**9
tests = []

def add(qs):
    assert 1 <= len(qs) <= 100_000
    for v in qs:
        assert len(v) == 4 and all(-G <= t <= G for t in v)
    tests.append(f"{len(qs)}\n" + "".join(" ".join(map(str, v)) + "\n" for v in qs))

def shifted(dx, dy, lim):
    # random start so that start and target are both inside [-lim, lim]
    a = random.randint(max(-lim, -lim - dx), min(lim, lim - dx))
    b = random.randint(max(-lim, -lim - dy), min(lim, lim - dy))
    return (a, b, a + dx, b + dy)

# samples
add([(0, 0, 1, 2), (0, 0, 1, 0), (0, 0, 4, 4)])
add([(5, 5, 5, 5), (-3, 2, 4, -1)])
add([(-100000, -100000, 100000, 100000)])
add([(0, 0, 6, 0), (2, 3, 2, 4), (-7, 0, 0, 0), (1, 1, 0, 0)])
add([(10, -10, -10, 10), (0, 0, 3, 0), (4, 4, 1, 3)])
# hidden, small differences (checked fully by the brute)
add([shifted(dx, dy, 50) for dx in range(-12, 13) for dy in range(-12, 13)])
add([shifted(dx, dy, G) for dx in range(-30, 31) for dy in range(-30, 31)])
add([shifted(s1 * 2, s2 * 2, 100) for s1 in (1, -1) for s2 in (1, -1)] +
    [shifted(s1 * p, s2 * r, G) for s1 in (1, -1) for s2 in (1, -1) for p, r in ((1, 0), (0, 1), (2, 2))])
add([shifted(random.randint(-300, 300), random.randint(-300, 300), G) for _ in range(3000)])
# hidden, big
add([(-G, -G, G, G), (G, G, -G, -G), (-G, 0, G, 0), (0, -G, 0, G), (-G, G, G, -G), (-G, -G, G, -G + 1),
     (-G, -G, G - 1, -G), (G, 0, -G, 1), (0, 0, G, G), (-G, -G, -G + 1, G)])
add([shifted(random.randint(-2 * G, 2 * G), random.randint(-2 * G, 2 * G), G) for _ in range(20_000)])
add([shifted(random.randint(-2 * G, 2 * G), random.choice([0, 1, 2, -1, -2, random.randint(-100, 100)]), G) for _ in range(10_000)])
add([shifted(dx, dx // 2 + random.randint(-3, 3), G) for dx in (random.randint(-2 * G, 2 * G) for _ in range(10_000))])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
