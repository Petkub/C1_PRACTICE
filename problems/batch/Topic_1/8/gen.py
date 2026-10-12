# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(104)
E = 10**18
tests = []

def add(qs):
    assert 1 <= len(qs) <= 100_000
    for k, c, l, r in qs:
        assert 1 <= k <= E and -E <= c <= E and -E <= l <= r <= E
    tests.append(f"{len(qs)}\n" + "".join(f"{k} {c} {l} {r}\n" for k, c, l, r in qs))

def small(n, mv, mk):
    qs = []
    for _ in range(n):
        l = random.randint(-mv, mv)
        r = random.randint(l, mv)
        qs.append((random.randint(1, mk), random.randint(-3 * mv, 3 * mv), l, r))
    return qs

def big(n):
    qs = []
    for _ in range(n):
        l = random.randint(-E, E)
        r = random.randint(l, E)
        k = random.choice([random.randint(1, 10), random.randint(1, 10**9), random.randint(1, E)])
        qs.append((k, random.randint(-E, E), l, r))
    return qs

# samples
add([(5, 3, 1, 20), (5, 3, -10, 2)])
add([(4, 0, 1, 3), (1, 5, -3, 3)])
add([(3, -1, -1, -1), (1_000_000, -999_999, -1_000_000, 1_000_000)])
add([(7, 100, -20, -1), (7, -100, -20, -1), (2, 1, -6, 6)])
add([(10, 7, 7, 7), (10, 7, 8, 16), (10, -3, -3, 7)])
# hidden, small (checked by the brute)
add(small(300, 30, 8))
add(small(300, 1000, 50))
add([(k, c, l, r) for k in range(1, 6) for c in range(-6, 7) for l in range(-6, 7) for r in range(l, 7)][:100000])
add([(1, 0, -E, -E), (1, 0, E, E), (2, 0, -E, -E), (3, E, -E, -E + 5), (E, E, E - 3, E), (E, -E, -E, -E + 2),
     (E, E, -E, -E + 3), (2, -E + 1, -E, -E + 1), (7, E, E - 20, E), (5, -E, E - 9, E)])
# hidden, big
add([(E, -E, -E, E), (E, E, -E, E - 1), (E, E - 1, -E, E), (1, 0, -E, E), (1, E, -E, E), (2, -E, -E, E), (E, 0, -E, E), (E, 1, -E, E), (E, -1, -E, E)])
add([(E - 1, -E, -E, E), (999_999_999_999_999_999, E, -E, E), (3, E, -E, E), (7, -E, -E, E), (2, -E + 1, -E, -E + 1)])
add(big(20_000))
add(big(8_000))
add(small(2000, 30_000, 10**6))
add([(k, random.randint(-E, E), -E, E) for k in (random.randint(1, 100) for _ in range(1000))])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
