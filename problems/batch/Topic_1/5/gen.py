# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(1005)
G = 10**9
tests = []

def add(qs):
    assert 1 <= len(qs) <= 100_000
    for n, k, t in qs:
        assert 1 <= n <= G and 1 <= k <= G and 1 <= t <= G
    tests.append(f"{len(qs)}\n" + "".join(f"{n} {k} {t}\n" for n, k, t in qs))

# samples
add([(3, 2, 5), (4, 2, 5)])
add([(5, 3, 4)])
add([(1, 10, 7), (2, 2, 1), (6, 4, 10)])
add([(1, 1, 3), (7, 1, 2), (3, 6, 100)])
add([(1000000000, 1, 99999)])
# hidden, small (checked by the brute)
add([(n, k, 1) for n in range(1, 21) for k in range(1, 21)])
add([(n, k, random.randint(1, 1000)) for n in range(21, 41) for k in range(1, 41, 3)])
add([(random.randint(1, 60), random.randint(1, 130), random.randint(1, G)) for _ in range(300)])
add([(n, k, G) for n in (1, 2, 3, 59, 60) for k in (1, 2, 3, n - 1 if n > 1 else 1, n, n + 1, 2 * n - 1, 2 * n, 2 * n + 1, G)])
add([(n, k, random.randint(1, 50)) for n in range(1, 61, 7) for k in range(1, 125, 4)])
# hidden, big
add([(G, 1, G), (G, G, G), (1, G, G), (G - 1, G, G), (G, G - 1, G), (G, 2, G), (G, 3, G), (G // 2 + 1, G, G),
     (G // 2, G, G), (G, 1, 1), (999_999_999, 2, 999_999_937)])
add([(random.randint(1, G), random.randint(1, G), random.randint(1, G)) for _ in range(25_000)])
add([(random.randint(1, G), random.randint(1, 1000), random.randint(1, G)) for _ in range(25_000)])
add([(n, random.randint(n, G), random.randint(1, G)) for n in (random.randint(1, G) for _ in range(20_000))])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
