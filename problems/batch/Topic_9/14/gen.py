# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(911)
MAXV = 10**18
MAXN = 20000
tests = []

def add(a, b):
    assert 1 <= len(a) <= MAXN and 1 <= len(b) <= MAXN
    for l, r in a + b:
        assert 1 <= l <= r <= MAXV
    lines = [f"{len(a)} {len(b)}"] + [f"{l} {r}" for l, r in a] + [f"{l} {r}" for l, r in b]
    tests.append("\n".join(lines) + "\n")

def rand_ranges(k, lo, hi, maxlen):
    out = []
    for _ in range(k):
        l = random.randint(lo, hi)
        r = min(hi, l + random.randint(0, maxlen))
        out.append((l, r))
    return out

# samples
add([(1, 5), (3, 8)], [(6, 10)])
add([(1, 2), (10, 10)], [(3, 9)])
add([(1, MAXV)], [(1, MAXV)])
add([(5, 5), (5, 5)], [(4, 6)])
add([(2, 4), (7, 9), (3, 8)], [(1, 2), (9, 12), (5, 5)])
# hidden
add([(1, 1)], [(2, 2)])
add([(1, 1)], [(1, 1)])
add([(1, MAXV)], [(MAXV, MAXV)])
add([(1, 3), (4, 6)], [(3, 4)])                                    # touching ranges, no overlap inside A
add([(i, i) for i in range(1, MAXN + 1)], [(1, MAXN)])
add([(1, MAXV - i) for i in range(4000)], [(MAXV - i, MAXV - i) for i in range(4000)])   # nested ranges
add(rand_ranges(10000, 1, MAXV, 10**15), rand_ranges(9000, 1, MAXV, 10**15))
add(rand_ranges(MAXN, 1, 10**6, 100), rand_ranges(MAXN, 1, 10**6, 100))
add(rand_ranges(4000, 1, MAXV, MAXV), rand_ranges(3000, 1, MAXV, MAXV))                 # huge overlaps
add([(2 * i + 1, 2 * i + 1) for i in range(MAXN)], [(2 * i + 2, 2 * i + 2) for i in range(12000)])  # interleaved
add(rand_ranges(8, 1, 30, 6), rand_ranges(6, 1, 30, 6))
add(rand_ranges(50, 1, 300, 20), rand_ranges(60, 1, 300, 20))
add(rand_ranges(300, 1, 10**9, 10**7), rand_ranges(200, 1, 10**9, 10**7))
add([(10**17 * k + 1, 10**17 * (k + 1)) for k in range(10)], [(5 * 10**16, 9 * 10**17 + 5)])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
