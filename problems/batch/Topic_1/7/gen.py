# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(1007)
E = 10**18
tests = []

def add(qs):
    assert 1 <= len(qs) <= 100_000
    for d, k, c in qs:
        assert 1 <= d <= E and 1 <= k <= E and 1 <= c <= E
    tests.append(f"{len(qs)}\n" + "".join(f"{d} {k} {c}\n" for d, k, c in qs))

def mid(m):
    # random query with up to about m stations before D
    k = random.randint(1, E // m)
    d = random.randint(1, m * k)
    c = random.choice([random.randint(1, 3 * k), random.randint(1, d), k * random.randint(1, 5), k - 1 if k > 1 else 1])
    return (d, k, c)

# samples
add([(10, 3, 4), (10, 3, 10)])
add([(20, 6, 5), (5, 6, 5)])
add([(100, 7, 20), (31, 10, 10), (50, 10, 25)])
add([(1000000000000, 1, 1), (12, 4, 4), (12, 5, 4)])
add([(40, 10, 9), (40, 10, 39), (40, 10, 40), (41, 10, 20)])
# hidden, small (checked by the brute)
add([(d, k, c) for d in range(1, 31) for k in range(1, 31) for c in range(1, 31)])
add([(random.randint(1, 2000), random.randint(1, 60), random.randint(1, 300)) for _ in range(2000)])
add([mid(1000) for _ in range(500)])
add([mid(3000) for _ in range(300)])
add([(d, k, c) for d in (99, 100, 101) for k in range(1, 101, 3) for c in range(k - 1, 101, 7) if c >= 1])
# hidden, big
add([(E, 1, 1), (E, 1, E), (E, E, E - 1), (E, E, 1), (E - 1, E, E - 1), (E, E - 1, E - 1), (E, 2, 3), (E, 3, 2),
     (E, E // 2, E // 2), (E, E // 2, E // 2 + 1), (E, E // 3, E // 2), (E, 7, 13), (1, 1, 1), (1, E, 1), (2, E, 1)])
add([(random.randint(1, E), random.randint(1, E), random.randint(1, E)) for _ in range(12_000)])
add([(random.randint(E // 2, E), random.randint(1, 10**6), random.randint(1, 10**7)) for _ in range(12_000)])
add([(random.randint(1, E), k, k * random.randint(1, 100) + random.randint(0, 1) * random.randint(0, k - 1))
     for k in (random.randint(1, 10**15) for _ in range(12_000))])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
