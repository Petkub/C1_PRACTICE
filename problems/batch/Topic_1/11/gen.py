# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(1011)
E = 10**18
tests = []

def add(qs):
    assert 1 <= len(qs) <= 100_000
    for n, a, b in qs:
        assert 1 <= n <= E and 1 <= a <= b <= E
    tests.append(f"{len(qs)}\n" + "".join(f"{n} {a} {b}\n" for n, a, b in qs))

def rnd_big():
    n = random.randint(1, E)
    kind = random.randint(0, 3)
    if kind == 0:
        a = random.randint(1, E)
        b = random.randint(a, E)
    elif kind == 1:
        # around n / t for a small t: answers near the border between possible and impossible
        t = random.randint(1, 50)
        a = max(1, n // t + random.randint(-2, 2))
        b = min(E, a + random.randint(0, 3))
    elif kind == 2:
        a = random.randint(1, 10**9)
        b = a + random.randint(0, 10**9)
    else:
        a = random.randint(1, n)
        b = min(E, a + random.randint(0, a // 1000 + 1))
    return (n, a, b)

# samples
add([(10, 3, 4), (10, 2, 5)])
add([(7, 4, 5), (5, 4, 5)])
add([(1, 1, 1), (12, 5, 6), (13, 5, 6), (13, 6, 7)])
add([(100, 7, 30), (100, 101, 200), (100, 33, 34)])
add([(1000000000000, 3, 7)])
# hidden, small (checked by the brute)
add([(n, a, b) for n in range(1, 41) for a in range(1, 41) for b in range(a, 41)])
add([(random.randint(1, 3000), a, a + random.randint(0, 50)) for a in (random.randint(1, 300) for _ in range(2000))])
add([(n, a, b) for n in range(950, 1001) for a in range(1, 60, 4) for b in (a, a + 1, 2 * a - 1, 2 * a)])
add([(n, a, a + random.randint(0, 3)) for n, a in ((n, max(1, n // random.randint(1, 30) + random.randint(-1, 1)))
     for n in (random.randint(10**5, 10**6) for _ in range(300)))])
add([(random.randint(1, 200), random.randint(1, 20), random.randint(20, 200)) for _ in range(1000)])
# hidden, big
add([(E, 1, 1), (E, 1, E), (E, E, E), (1, E, E), (E - 1, E, E), (E, 2, 3), (E, 3, 3), (E, E // 2, E // 2),
     (E, E // 2 + 1, E), (E, E // 3, E // 3 + 1), (E - 1, E // 2, E // 2), (E, 7, 7), (E, 999_999_999, 1_000_000_000)])
add([rnd_big() for _ in range(15_000)])
add([rnd_big() for _ in range(15_000)])
add([rnd_big() for _ in range(15_000)])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
