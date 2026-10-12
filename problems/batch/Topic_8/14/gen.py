# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random, string

random.seed(814)
tests = []
ALNUM = string.ascii_uppercase + string.digits

def add(W, K, fares, taps):
    M, N = len(fares), len(taps)
    assert 1 <= M <= 100 and 1 <= W <= 10**6 and 0 <= K <= 10 and 1 <= N <= 100000
    assert all(1 <= f <= 1000 for f in fares)
    for t, c, l in taps:
        assert 0 <= t <= 10**9 and 1 <= len(c) <= 8 and all(ch in ALNUM for ch in c) and 1 <= l <= M
    assert all(taps[i][0] <= taps[i + 1][0] for i in range(N - 1))
    tests.append(f"{M} {W} {K}\n" + " ".join(map(str, fares)) + f"\n{N}\n"
                 + "".join(f"{t} {c} {l}\n" for t, c, l in taps))

def ids(n):
    out = set()
    while len(out) < n:
        out.add("".join(random.choice(ALNUM) for _ in range(random.randint(1, 8))))
    return sorted(out)

def rnd(N, cards, M, gap, W):
    cs = ids(cards)
    t, taps = 0, []
    for _ in range(N):
        t += random.randint(0, gap)
        taps.append((t, random.choice(cs), random.randint(1, M)))
    assert t <= 10**9
    return taps

# samples
add(60, 2, [20, 30, 45], [(0, "P", 1), (10, "P", 2), (40, "P", 1), (100, "P", 3)])
add(100, 1, [50, 20, 20], [(0, "A", 1), (5, "A", 2), (9, "A", 3), (9, "B7", 3)])
add(30, 0, [15, 25], [(0, "X", 1), (0, "X", 2), (0, "Y", 2), (31, "Y", 1)])
add(30, 3, [10, 40], [(0, "C", 1), (30, "C", 2), (31, "D", 1), (62, "D", 2)])
add(5, 1, [7], [(3, "Z", 1)])
# hidden
add(60, 2, [20, 30, 45], [(0, "P", 1), (10, "P", 2), (15, "Q", 2), (40, "P", 1), (76, "Q", 1), (100, "P", 3)])
add(30, 3, [10, 40, 25, 60], [(0, "C1", 1), (10, "C2", 2), (20, "C1", 3), (30, "C1", 2), (31, "C1", 4),
                              (40, "C2", 4), (41, "C2", 1)])
add(1, 10, [1000] * 100, [(10**9, "Q" * 8, 100)])
add(1000, 10, list(range(10, 120, 10)), [(i, "UP", i + 1) for i in range(11)] * 1 + [(11, "UP", 1)])   # climbing fares
add(10**6, 10, [random.randint(1, 1000) for _ in range(100)], [(i // 3, "A", random.randint(1, 100)) for i in range(100000)])   # one card
add(90, 3, [random.randint(10, 60) for _ in range(12)], rnd(25000, 300, 12, 2, 90))
add(45, 2, [random.randint(1, 1000) for _ in range(5)], rnd(25000, 10000, 5, 1, 45))
add(10**6, 10, [1000] * 100, [(i * 10000, c, 1 + i % 100) for i, c in enumerate(ids(30000))])   # all different cards
short = [a + b for a in ALNUM for b in ALNUM][:400]
mx, t = [], 0
for _ in range(50000):                                           # many cards, short card codes
    t += random.randint(0, 1)
    mx.append((t, random.choice(short), random.randint(1, 9)))
add(30, 2, [random.randint(1, 1000) for _ in range(9)], mx)
add(60, 4, [random.randint(1, 50) for _ in range(6)], rnd(2000, 20, 6, 15, 60))
add(20, 2, [5, 9, 3, 12], rnd(60, 4, 4, 6, 20))
add(10, 1, [3, 8, 6], rnd(40, 3, 3, 4, 10))
add(15, 0, [4, 6, 2], rnd(30, 3, 3, 5, 15))
add(50, 10, [7, 7, 7, 7], rnd(50, 2, 4, 9, 50))
add(1000, 3, [100, 200, 300, 400, 500],
    [(0, "K", 5), (1, "K", 4), (2, "K", 3), (3, "K", 2), (4, "K", 1), (1000, "K", 1), (1001, "K", 2), (2001, "K", 3), (2002, "K", 3)])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
