# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(1315)
MAXN, MAXV = 100_000, 10**9
tests = []


def add(h, b):
    n, m = len(h), len(b)
    assert 1 <= n <= MAXN and 1 <= m <= MAXN
    assert all(1 <= x <= MAXV for x in h) and all(1 <= x <= MAXV for x in b)
    tests.append(f"{n} {m}\n" + " ".join(map(str, h)) + "\n" + " ".join(map(str, b)) + "\n")


def rnd(n, m, lo, hi, blo=None, bhi=None):
    blo = lo if blo is None else blo
    bhi = hi if bhi is None else bhi
    return ([random.randint(lo, hi) for _ in range(n)],
            [random.randint(blo, bhi) for _ in range(m)])


# samples
add([5, 3, 7, 8, 3], [6, 4, 5, 2])
add([100, 100], [99, 100, 1000])
add([1, MAXV], [MAXV, MAXV, MAXV])
add([4, 9, 2, 9, 6, 1], [9, 8, 9, 3, 5, 10])
add([10, 20, 30, 40], [25, 25, 25, 50, 5])
# hidden (small)
add([1], [1])
add([7, 7, 7], [7, 6, 8, 7, 7])
add(*rnd(8, 10, 1, 10))
add(*rnd(100, 150, 1, 50))
add(*rnd(1000, 1000, 1, MAXV))
add(*rnd(2000, 3000, 1, 20, 1, 25))
add(*rnd(500, 2000, MAXV - 100, MAXV))             # more customers than tickets
# large
add(*rnd(MAXN, MAXN, 1, 999))
h = [random.randint(1, 9999) for _ in range(MAXN)]
add(h, [9999] * MAXN)                               # everyone buys the dearest ticket left
add(*rnd(15_000, 15_000, 1, MAXV))
h = [random.randint(5000, 9999) for _ in range(40_000)]
add(h, [random.randint(1, 9999) for _ in range(20_000)])   # many customers below every price

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
