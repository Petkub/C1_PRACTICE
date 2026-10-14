# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(1218)
V = 10**9
tests = []

def add(k, t):
    n = len(t)
    assert 1 <= n <= 100_000 and 0 <= k <= 2 * V
    assert all(-V <= x <= V for x in t)
    tests.append(f"{n} {k}\n" + " ".join(map(str, t)) + "\n")

def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]

def walk(n, step, lo, hi):
    x, t = random.randint(lo, hi), []
    for _ in range(n):
        x = min(hi, max(lo, x + random.randint(-step, step)))
        t.append(x)
    return t

# samples
add(2, [1, 3, 2, 4, 4, 3, 6, 5])
add(0, [5, 5, 7, 7, 5, 5])
add(0, [-V])
add(2 * V, [-V, V, -5])
add(1, [-3, -2, -2, -1, 0, 1, 2])
add(5, [4, 9, 1, 6, 2, 7, 3])
# hidden (small)
add(0, [1, 2])
add(2 * V - 1, [V, -V])
add(3, [0, 3, 0, 3, 10, 13, 10, 13, 20])          # two equally long runs: earliest start
add(random.randint(0, 3), rnd(10, -3, 3))
add(random.randint(0, 5), rnd(40, -5, 5))
add(10, walk(300, 3, -50, 50))
add(V, rnd(2000, -V, V))
# large
add(0, [0] * 100_000)                              # everything is one run
add(100, rnd(100_000, -50, 50))                    # the whole array fits
add(1000, list(range(-49_999, 50_001, 1)))         # increasing: every window has the same length
add(40, walk(100_000, 3, -1000, 1000))
add(0, [random.randint(1, 3) for _ in range(100_000)])
add(15 * 10**8, rnd(70_000, -V, V))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
