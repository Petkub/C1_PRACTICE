# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(105)
E = 10**18
tests = []

def add(qs):
    assert 1 <= len(qs) <= 100_000
    for a, b, x in qs:
        assert 1 <= a <= E and 1 <= b <= E and -E <= x <= E
    tests.append(f"{len(qs)}\n" + "".join(f"{a} {b} {x}\n" for a, b, x in qs))

def reachable(a, b, maxn):
    # a random position the frog really visits (n <= maxn), so tests are not all -1
    n = random.randint(0, maxn)
    k = n // 2
    return k * (a - b) + (a if n % 2 else 0)

def small(n, m):
    qs = []
    for _ in range(n):
        a, b = random.randint(1, m), random.randint(1, m)
        if random.random() < 0.5:
            x = reachable(a, b, 3 * m)
            if abs(x) > E:
                x = 0
        else:
            x = random.randint(-4 * m, 4 * m)
        qs.append((a, b, x))
    return qs

def big(n):
    qs = []
    for _ in range(n):
        a = random.choice([random.randint(1, E), random.randint(1, 10**9)])
        b = a + random.choice([-1, 1, 0, random.randint(-10**6, 10**6), random.randint(-E, E)])
        b = min(max(b, 1), E)
        d = a - b
        r = random.random()
        if r < 0.4 and d != 0:
            # x = k*d (+ a), with k as large as allowed
            odd = random.random() < 0.5
            base = a if odd else 0
            lim = (E - base) // abs(d) if d > 0 else (E + base) // abs(d)
            k = random.randint(0, max(0, lim))
            x = k * d + base
            if abs(x) > E:
                x = base
        elif r < 0.6 and d != 0:
            x = random.randint(-E // abs(d), E // abs(d)) * d + random.choice([0, a, 1, -1])
            x = min(max(x, -E), E)
        else:
            x = random.randint(-E, E)
        qs.append((a, b, x))
    return qs

# samples
add([(5, 3, 9), (5, 3, 4), (5, 3, 3)])
add([(3, 5, -4), (2, 2, 2), (2, 2, 1)])
add([(4, 1, 0), (4, 1, 4), (4, 1, -3), (1, 4, -3), (1, 4, -2)])
add([(7, 7, 0), (10, 4, 22), (10, 4, 16), (6, 10, -10)])
add([(1, 1000, -999), (1, 1000, -998), (1000, 1, 1999)])
# hidden, small (checked by the brute)
add(small(500, 10))
add(small(500, 60))
add([(a, b, x) for a in range(1, 7) for b in range(1, 7) for x in range(-12, 13)])
add([(1, 1, 0), (1, 1, 1), (1, 1, -1), (1, 2, -1), (1, 2, 1), (2, 1, 1), (2, 1, 0), (3, 1, 1), (3, 1, 2)])
# hidden, big
add([(E, 1, E), (E, 1, 0), (1, E, -E + 1), (1, E, 1 - E), (E, E, E), (E, E, -E), (E, E, 0),
     (1, 2, -E), (2, 1, E), (1, 2, E), (E, E - 1, E), (E - 1, E, -E), (E, E - 1, -E), (1, 2, -E + 1)])
add([(E, E - 1, -E + 1), (E, E - 1, 1 - E), (E, E - 1, E - 1), (E - 1, E, -E + 1), (E - 1, E, E - 1), (E, 2, E - 1)])
add(big(30_000))
add(big(30_000))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
