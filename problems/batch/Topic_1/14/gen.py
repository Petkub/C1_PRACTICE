# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(1114)
G = 10**9
tests = []

def add(qs):
    assert 1 <= len(qs) <= 100_000
    for n, k, m in qs:
        assert 1 <= n <= G and 1 <= k <= G and 1 <= m <= G
    tests.append(f"{len(qs)}\n" + "".join(f"{n} {k} {m}\n" for n, k, m in qs))

def edge(nmax, kmax):
    # n where the number of exchanges just changes: n = k + t (k - m) + {-1, 0, 1}
    k = random.randint(2, kmax)
    m = random.randint(1, k - 1)
    tmax = (nmax - k) // (k - m)
    if tmax < 0:
        return (random.randint(1, nmax), k, m)
    t = random.randint(0, tmax)
    n = k + t * (k - m) + random.randint(-1, 1)
    return (max(1, min(nmax, n)), k, m)

def slow(nmax):
    # many exchanges that each give back almost everything (bad for exchanging in batches)
    k = random.randint(nmax // 4, nmax // 2)
    return (random.randint(nmax - 1000, nmax), k, k - random.randint(1, 2))

def any_big():
    kind = random.randint(0, 4)
    if kind == 0:
        return (random.randint(1, G), random.randint(1, G), random.randint(1, G))
    if kind == 1:
        k = random.randint(2, 1000)
        return (random.randint(1, G), k, random.randint(1, k - 1))
    if kind == 2:
        return edge(G, G)
    if kind == 3:
        k = random.randint(1, G)
        return (random.randint(k, G), k, random.randint(k, G))      # never stops
    return slow(G)

# samples
add([(10, 3, 1), (2, 3, 1)])
add([(5, 2, 2), (6, 4, 3)])
add([(1, 5, 9), (9, 3, 2), (3, 3, 1), (3, 3, 3)])
add([(G, 2, 1)])
add([(G, G // 2, G // 2 - 1), (100, 7, 3), (1, 1, 1)])
# hidden, small (checked by the brute)
add([(n, k, m) for n in range(1, 61) for k in range(1, 31) for m in range(1, 31)])
add([(random.randint(1, 10**6), k, random.randint(1, k - 1)) for k in (random.randint(2, 1000) for _ in range(300))])
add([edge(10**5, 300) for _ in range(3000)])
add([(random.randint(1, 10**4), random.randint(1, 50), random.randint(1, 60)) for _ in range(5000)])
# hidden, big
add([(G, 1, 1), (G, 2, 1), (G, G, 1), (G, G, G), (G - 1, G, 1), (G, G, G - 1), (G, G - 1, G - 2), (1, G, G),
     (G, G // 2, G // 2 - 1), (G, G // 2 + 1, G // 2), (G, 3, 2), (G, 3, 1), (G, 1000, 999), (G, 2, 2), (G, 1, G)])
add([slow(G) for _ in range(20_000)])
add([any_big() for _ in range(20_000)])
add([any_big() for _ in range(20_000)])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
