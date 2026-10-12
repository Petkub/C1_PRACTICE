# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(920)
MAXN = 50000
MAXV = 1000
tests = []

def add(mats, qs):
    n, q = len(mats), len(qs)
    assert 1 <= n <= MAXN and 1 <= q <= MAXN
    for a, b, c, d in mats:
        assert all(-MAXV <= x <= MAXV for x in (a, b, c, d))
        assert a * d - b * c in (1, -1)
    for l, r in qs:
        assert 1 <= l <= r <= n
    lines = [f"{n} {q}"] + [f"{a} {b} {c} {d}" for a, b, c, d in mats] + [f"{l} {r}" for l, r in qs]
    tests.append("\n".join(lines) + "\n")

def mul(x, y):
    a, b, c, d = x
    e, f, g, h = y
    return (a * e + b * g, a * f + b * h, c * e + d * g, c * f + d * h)

def rand_mat(bound, steps=6):
    # random product of shears, rotations and reflections, kept inside the bound
    while True:
        m = (1, 0, 0, 1)
        for _ in range(random.randint(1, steps)):
            kind = random.randrange(6)
            k = random.choice([-1, 1]) * random.randint(1, max(1, bound))
            g = [(1, k, 0, 1), (1, 0, k, 1), (0, -1, 1, 0), (0, 1, 1, 0), (1, 0, 0, -1), (-1, 0, 0, -1)][kind]
            m = mul(m, g)
        if all(abs(x) <= bound for x in m):
            return m

def big_mat():
    # [[k m + 1, k], [m, 1]] with large entries, then random signs / swaps
    while True:
        k = random.randint(1, 1000)
        m = random.randint(1, 1000 // k)
        if k * m + 1 <= MAXV:
            break
    x = (k * m + 1, k, m, 1)
    for g in random.sample([(0, 1, 1, 0), (-1, 0, 0, -1), (1, 0, 0, -1), (0, -1, 1, 0)], random.randint(0, 2)):
        x = mul(x, g) if random.random() < 0.5 else mul(g, x)
    return x

def rand_queries(n, q):
    out = []
    for _ in range(q):
        l = random.randint(1, n)
        r = random.randint(l, n)
        out.append((l, r))
    return out

def long_queries(n, q, slack):
    return [(random.randint(1, slack), random.randint(n - slack + 1, n)) for _ in range(q)]

# samples
add([(1, 1, 0, 1), (0, -1, 1, 0), (2, 1, 1, 1)], [(1, 3), (1, 2)])
add([(0, 1, 1, 0), (1, 2, 0, 1)], [(1, 2)])
add([(1000, 999, 1, 1)] * 3, [(1, 3)])
add([(2, 1, 1, 1), (1, 0, -1, 1), (0, 1, 1, 0)], [(1, 3), (2, 3)])
add([(1, -7, 0, 1)], [(1, 1)])
# hidden
add([(1000, -999, -1, 1)], [(1, 1)])
add([(1, 0, 0, 1), (1, 0, 0, 1)], [(1, 1), (1, 2), (2, 2)])
mats = [rand_mat(3) for _ in range(10)]
add(mats, [(l, r) for l in range(1, 11) for r in range(l, 11)])                 # every range
add([rand_mat(3) for _ in range(50)], rand_queries(50, 200))
add([big_mat() for _ in range(300)], rand_queries(300, 1000))
add([(0, -1, 1, 0)] * 1000, [(l, l + 4 * k - 1) for l, k in ((1, 250), (5, 1), (17, 100), (2, 3))]
    + [(3, 4), (10, 12), (1, 1000)])                                             # rotations: I, -I, ...
add([rand_mat(1000, 3) if random.random() < 0.5 else big_mat() for _ in range(2000)], rand_queries(2000, 2000))
add([random.choice([(0, 1, 1, 0), (1, 0, 0, -1), (1, 1, 1, 0), (0, 1, 1, 1)]) for _ in range(5000)],
    [(1, random.randint(1, 5000)) for _ in range(2500)] + [(i, i) for i in random.sample(range(1, 5001), 2500)])
# big tests: answering each question by direct multiplication is too slow
add([(1, 1, 1, 0)] * 30000, rand_queries(30000, 20000))                          # Fibonacci matrices
add([rand_mat(2) for _ in range(MAXN)], long_queries(MAXN, MAXN, 100) )
add([big_mat() for _ in range(MAXN)], long_queries(MAXN, 10000, 5000))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
