# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(1205)
NMAX, V = 100_000, 10**9
tests = []

def add(T, t):
    n = len(t)
    assert 1 <= n <= NMAX and 1 <= T <= V
    assert all(0 <= x <= V for x in t)
    assert all(t[i] <= t[i + 1] for i in range(n - 1))
    tests.append(f"{n} {T}\n" + " ".join(map(str, t)) + "\n")

def rnd(n, lo, hi):
    return sorted(random.randint(lo, hi) for _ in range(n))

def gaps(n, start, maxgap, pzero):
    # times built from random gaps, many equal times when pzero is large
    t, cur = [], start
    for _ in range(n):
        t.append(cur)
        cur += 0 if random.random() < pzero else random.randint(1, maxgap)
    assert t[-1] <= V
    return t

# samples
add(10, [1, 5, 11, 12, 25])
add(3, [7, 7, 7, 9])
add(1, [0])
add(1, [2, 2, 3, 3, 3])
add(10**9, [0, 1, 10**9])
add(100, [0, 60, 99, 160, 200])
# hidden
add(5, [0, 5, 10, 15, 20])                       # gaps exactly T
add(1, [4, 4, 4, 4, 4, 4])
add(10**9, [10**9] * 3)
add(7, gaps(40, 0, 6, 0.3))
add(50, gaps(1500, 100, 30, 0.2))
add(3, rnd(2000, 0, 3000))
add(10**9, rnd(1000, 0, V))
# max size
add(1_000_000, rnd(NMAX, 0, V))
add(10**9, [0] * 90_000 + [10**9] * 10_000)
add(2, gaps(NMAX, 0, 2, 0.5))
add(500, gaps(60_000, 12345, 15, 0.1))
add(1, gaps(30_000, 0, 3, 0.6))

assert sum(len(t) for t in tests) < 2_900_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
