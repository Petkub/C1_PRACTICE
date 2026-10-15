# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(1204)
NMAX, V = 100_000, 10**9
tests = []

def add(k, a):
    n = len(a)
    assert 1 <= k <= n <= NMAX
    assert all(1 <= x <= V for x in a)
    tests.append(f"{n} {k}\n" + " ".join(map(str, a)) + "\n")

def rnd(n, hi):
    return [random.randint(1, hi) for _ in range(n)]

# samples
add(3, [4, 7, 1, 9, 2, 6, 3, 8])
add(5, [1, 2, 3, 4, 5])
add(1, [10**9])
add(4, [3, 1, 4, 1, 5, 9])
add(1, [9, 5, 9, 2])
add(2, [1, 2, 3, 4, 5, 6])
# hidden
add(2, [7, 8])
add(2, [5, 6, 7])
add(3, list(range(1, 13)))                 # N divisible by K
add(4, list(range(1, 14)))                 # last group of 1
add(7, rnd(50, 100))
add(6, rnd(1000, V))
add(999, rnd(1000, V))
# max size
add(317, rnd(NMAX, V))
add(1, rnd(NMAX, 9))
add(NMAX, rnd(NMAX, 9999))
add(NMAX - 1, rnd(NMAX, 999))
add(2, rnd(NMAX, 99))
add(50_001, rnd(NMAX, 99))

assert sum(len(t) for t in tests) < 2_900_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
