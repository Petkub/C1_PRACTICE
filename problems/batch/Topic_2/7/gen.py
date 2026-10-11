# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(207)
MAXV = 10**9
tests = []

def add(qs):
    assert 1 <= len(qs) <= 100_000
    for n, k in qs:
        assert 1 <= n <= MAXV and 1 <= k <= MAXV
    tests.append(f"{len(qs)}\n" + "".join(f"{n} {k}\n" for n, k in qs))

# samples
add([(8, 3), (5, 1), (4, 10)])
add([(8, 2)])
add([(1, 1), (6, 3), (12, 4)])
add([(10, 1), (9, 2), (7, 7)])
add([(20, 3), (15, 6)])
# hidden: small, brute checks all
add([(n, k) for n in range(1, 41) for k in range(1, 41)])
add([(random.randint(1, 10**4), random.randint(1, 50)) for _ in range(1000)])
add([(random.randint(1, 10**4), random.randint(1, 10**4)) for _ in range(1000)])
add([(10**6, 1), (10**6, 2), (10**6, 999_999), (10**6, 10**6), (10**6, 500_000), (999_999, 1000)])
add([(MAXV, 1)])
add([(MAXV, MAXV)])
add([(MAXV, MAXV - 1), (MAXV, MAXV // 2), (MAXV, 2), (MAXV - 1, 1), (MAXV, 1), (1, MAXV)])
add([(MAXV, 3), (MAXV, 31_623), (MAXV, 333_333_334), (MAXV, 499_999_999), (MAXV, 500_000_001)])
# hidden: big T (brute too slow)
add([(MAXV - random.randint(0, 10), random.randint(1, 3)) for _ in range(100_000)])
add([(random.randint(1, MAXV), random.randint(1, MAXV)) for _ in range(20_000)])
add([(random.randint(MAXV // 2, MAXV), random.randint(1, 10**5)) for _ in range(15_000)])
add([(random.randint(1, MAXV), random.randint(1, 100)) for _ in range(15_000)])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
