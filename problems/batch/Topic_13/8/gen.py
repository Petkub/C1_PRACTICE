# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(1308)
MAXN = 100_000
P = 10_000
tests = []


def add(k, p):
    n = len(p)
    assert 1 <= n <= MAXN
    assert -10**9 <= k <= 10**9
    assert all(-P <= x <= P for x in p)
    tests.append(f"{n} {k}\n" + " ".join(map(str, p)) + "\n")


def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]


def some_sum(p):
    """the sum of a random period, so the answer is at least 1"""
    l = random.randrange(len(p))
    r = random.randint(l, len(p) - 1)
    return sum(p[l:r + 1])


# samples
add(3, [2, 1, -1, 3, 0])
add(0, [0, 0, 0, 0])
add(10, [1, 2, 3])
add(-2, [3, -5, 2, -4, 2])
add(7, [7])
# hidden (small)
add(-7, [7])
add(0, [5, -5, 5, -5, 5, -5])
add(1, rnd(30, -1, 1))
a = rnd(200, -50, 50)
add(some_sum(a), a)
a = rnd(2000, -P, P)
add(some_sum(a), a)
add(0, rnd(3000, -2, 2))
# large
add(0, [0] * MAXN)                                          # every period works
add(10**9, [P] * MAXN)                                      # exactly one period: all days
add(-10**9, rnd(30_000, -P, P))                           # out of reach
add(1, rnd(MAXN, -1, 1))
a = rnd(MAXN, -P, P)
add(some_sum(a), a)
a = rnd(MAXN, -3, 4)
add(5, a)
a = [random.choice([2, -1]) for _ in range(MAXN)]
add(-1, a)

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
assert sum(len(t) for t in tests) < 3_000_000
print("total bytes", sum(len(t) for t in tests))
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
