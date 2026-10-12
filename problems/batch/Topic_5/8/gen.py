# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(504)
V = 10**9
tests = []

def add(h, qs):
    n, q = len(h), len(qs)
    assert 1 <= n <= 100_000 and 1 <= q <= 100_000
    assert all(0 <= x <= V for x in h)
    assert all(1 <= l <= n and 1 <= r <= n for l, r in qs)
    tests.append(f"{n} {q}\n" + " ".join(map(str, h)) + "\n" + "".join(f"{l} {r}\n" for l, r in qs))

def rq(n, q):
    return [(random.randint(1, n), random.randint(1, n)) for _ in range(q)]

# samples
add([10, 30, 20, 50], [(1, 4), (4, 1), (2, 2)])
add([1, 5, 5, 9], [(2, 4), (4, 1)])
add([7], [(1, 1)])
add([3, 8, 2, 6, 6, 1], [(1, 6), (6, 1), (3, 4), (5, 2)])
add([0, 1000000000, 0], [(1, 3), (3, 1), (2, 1)])
# hidden
add([4, 4, 4, 4], [(1, 4), (4, 1), (2, 3)])
add(list(range(1, 51)), [(1, 50), (50, 1)] + rq(50, 20))
add([random.randint(0, 20) for _ in range(30)], rq(30, 50))
add([random.randint(0, 1000) for _ in range(300)], rq(300, 300))
add([random.randint(0, V) for _ in range(2000)], rq(2000, 2000))
# max: zigzag 0, 1e9 -> answers about 5e13
h = [0 if i % 2 == 0 else V for i in range(100_000)]
qs = [(1, 100_000), (100_000, 1)] * 25_000
add(h, qs)
# max: small heights, random queries
add([random.randint(0, 999) for _ in range(100_000)], rq(100_000, 60_000))
# max: long walks on a smooth mountain
h = []
x = 500_000_000
for i in range(50_000):
    x = max(0, min(V, x + random.randint(-1000, 1000)))
    h.append(x)
qs = [(random.randint(1, 50), random.randint(49_950, 50_000)) if random.random() < 0.5
      else (random.randint(49_950, 50_000), random.randint(1, 50)) for _ in range(20_000)]
add(h, qs)
add([V] * 1000, rq(1000, 1000))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
