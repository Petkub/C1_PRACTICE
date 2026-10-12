# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(1015)
E = 10**18
tests = []

def add(qs):
    assert 1 <= len(qs) <= 100_000
    for a1, a2, a3, b1, b2, b3 in qs:
        assert min(a1, a2, a3, b1, b2, b3) >= 0
        n = a1 + a2 + a3
        assert 1 <= n <= E and b1 + b2 + b3 == n
    tests.append(f"{len(qs)}\n" + "".join(" ".join(map(str, x)) + "\n" for x in qs))

def split(n):
    # three non-negative parts summing to n, sometimes lopsided or with zeros
    kind = random.randint(0, 3)
    if kind == 0:
        x, y = sorted((random.randint(0, n), random.randint(0, n)))
        p = [x, y - x, n - y]
    elif kind == 1:
        big = n - random.randint(0, min(n, 3))
        r = n - big
        s = random.randint(0, r)
        p = [big, s, r - s]
    elif kind == 2:
        s = random.randint(0, n)
        p = [s, n - s, 0]
    else:
        p = [n // 3, n // 3, n - 2 * (n // 3)]
    random.shuffle(p)
    return p

def query(nmin, nmax):
    n = random.randint(nmin, nmax)
    return tuple(split(n) + split(n))

# samples
add([(2, 1, 0, 0, 1, 2)])
add([(3, 0, 0, 0, 2, 1)])
add([(1, 1, 1, 1, 1, 1), (1, 0, 0, 0, 1, 0), (0, 1, 0, 0, 1, 0)])
add([(50, 30, 20, 10, 60, 30)])
add([(0, 0, 5, 5, 0, 0), (4, 0, 0, 4, 0, 0), (2, 2, 3, 3, 2, 2)])
# hidden, small (checked by the brute)
add([(a1, a2, n - a1 - a2, b1, b2, n - b1 - b2) for n in range(1, 6) for a1 in range(n + 1) for a2 in range(n - a1 + 1)
     for b1 in range(n + 1) for b2 in range(n - b1 + 1)])
add([query(6, 12) for _ in range(1500)])
add([query(13, 25) for _ in range(150)])
add([query(1, 4) for _ in range(500)] + [query(26, 40) for _ in range(20)])
# hidden, big
add([(E, 0, 0, 0, E, 0), (E, 0, 0, E, 0, 0), (E, 0, 0, 0, 0, E), (0, E, 0, 0, 0, E), (0, 0, E, E, 0, 0),
     (E - 1, 1, 0, 0, E - 1, 1), (E // 2, E // 2, 0, 0, E // 2, E // 2), (1, 0, 0, 0, 1, 0),
     (E // 3, E // 3, E - 2 * (E // 3), E // 3, E // 3, E - 2 * (E // 3)), (E - 2, 1, 1, 1, E - 2, 1)])
add([query(1, E) for _ in range(10_000)])
add([query(E - 10**6, E) for _ in range(10_000)])
add([query(1, 10**9) for _ in range(10_000)])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
