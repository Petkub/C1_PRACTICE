# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(1020)
E = 10**18
G = 10**9
tests = []

def add(qs):
    assert 1 <= len(qs) <= 100_000
    for a, b, n in qs:
        assert 1 <= a <= G and 1 <= b <= G and 1 <= n <= E
    tests.append(f"{len(qs)}\n" + "".join(f"{a} {b} {n}\n" for a, b, n in qs))

def edge_n(a, b):
    # n close to the start or the end of some block k*b .. k*a + a - 1 (a < b), or far beyond the last block
    lo, hi = min(a, b), max(a, b)
    kmax = (lo - 1) // (hi - lo) if hi > lo else 0
    if kmax == 0:
        base = random.choice([lo - 1, random.randint(1, E)])
    else:
        k = random.randint(1, kmax)
        base = random.choice([k * hi, k * lo + lo - 1, random.randint(kmax * hi, E)])
    return max(1, min(E, base + random.randint(-2, 2)))

def big_pair():
    kind = random.randint(0, 4)
    if kind == 0:
        a, b = random.randint(1, G), random.randint(1, G)
    elif kind == 1:
        a = random.randint(G // 2, G)
        b = a + random.randint(1, 3)
    elif kind == 2:
        a = random.randint(1, G)
        b = min(G, a + random.randint(1, 1000))
    elif kind == 3:
        a = random.randint(1, G)
        b = a
    else:
        a = random.randint(1, 1000)
        b = random.randint(1, 1000)
    if b > G:
        b = G
    return (a, b) if random.random() < 0.5 else (b, a)

# samples
add([(3, 4, 12), (6, 6, 10)])
add([(10, 7, 30), (7, 10, 12)])
add([(1, 2, 10), (2, 1, 1), (1, 1, 5), (5, G, E)])
add([(G - 1, G, E)])
add([(100, 101, 5000), (100, 150, 250), (12, 8, 50), (G, 1, E)])
# hidden, small (checked by the brute)
add([(a, b, n) for a in range(1, 26) for b in range(1, 26) for n in range(1, 81)])
add([(random.randint(1, 1000), random.randint(1, 1000), random.randint(1, 100_000)) for _ in range(1000)])
add([(a, a + random.randint(1, 3), random.randint(1, 10**6)) if random.random() < 0.5 else
     (a + random.randint(1, 3), a, random.randint(1, 10**6)) for a in (random.randint(1, 3000) for _ in range(150))])
qs = []
for _ in range(2000):
    a, b = random.randint(2, 300), random.randint(2, 300)
    qs.append((a, b, min(edge_n(a, b), 100_000)))
add(qs)
qs = []
for _ in range(3000):
    a = random.randint(1, 60)
    b = random.choice([a, a + 1, a - 1, random.randint(1, 60)])
    b = max(1, b)
    qs.append((a, b, min(edge_n(a, b), 5000)))
add(qs)
# hidden, big
add([(G, G, E), (1, 1, E), (1, G, E), (G, 1, E), (G - 1, G, E), (G, G - 1, E), (G - 1, G, 1), (G - 1, G, G - 2),
     (G - 1, G, G), (G - 1, G, 2 * G - 2), (G - 1, G, 2 * G - 3), (G // 2, G, E), (G // 2 + 1, G, E), (G // 2, G, G),
     (2, 3, E), (G - 2, G, E), (G - 2, G, (G // 2 - 2) * G), (G - 2, G, (G // 2 - 2) * G - 1),
     (G - 2, G, (G // 2 - 2) * (G - 2) + G - 3), (G - 2, G, (G // 2 - 2) * (G - 2) + G - 4)])
add([(a, b, edge_n(a, b)) for a, b in (big_pair() for _ in range(12_000))])
add([(a, b, random.randint(1, E)) for a, b in (big_pair() for _ in range(12_000))])
add([(a, b, edge_n(a, b)) for a, b in (big_pair() for _ in range(12_000))])
add([(a, b, random.randint(1, min(E, 2 * max(a, b) ** 2 // max(1, abs(a - b)) + 1))) for a, b in (big_pair() for _ in range(12_000))])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
