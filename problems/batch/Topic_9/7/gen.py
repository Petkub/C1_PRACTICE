# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(907)
tests = []

def add(a, b):
    p, q = len(a), len(a[0])
    assert p >= 1 and q >= 1 and p * q <= 50000
    assert all(len(r) == q for r in a)
    assert len(b) == q and all(len(r) == p for r in b)
    for m in (a, b):
        for r in m:
            for x in r:
                assert -1000 <= x <= 1000
    lines = [f"{p} {q}"] + [" ".join(map(str, r)) for r in a] + [" ".join(map(str, r)) for r in b]
    tests.append("\n".join(lines) + "\n")

def rnd(p, q, lo=-1000, hi=1000):
    return [[random.randint(lo, hi) for _ in range(q)] for _ in range(p)]

# samples
add([[1, 2], [3, 4]], [[5, 6], [7, 8]])
add([[1], [2], [3]], [[4, 5, 6]])
add([[1, -2, 3]], [[4], [5], [-6]])
add([[-7]], [[0]])
add([[2, 0, -1], [1, 3, 2]], [[1, 4], [0, -2], [5, 1]])
# hidden
add([[1000]], [[1000]])
add([[1000]] * 50000, [[1000] * 50000])                        # biggest sum, p large q = 1
add(rnd(25000, 2, -1000, -990), rnd(2, 25000, 990, 1000))      # big negative
add(rnd(223, 224), rnd(224, 223))
add(rnd(1, 50000, -9, 9), rnd(50000, 1, -9, 9))                # p = 1
add(rnd(5000, 10, -3, 3), rnd(10, 5000, -3, 3))
add(rnd(3, 3), rnd(3, 3))
add(rnd(7, 2), rnd(2, 7))
add(rnd(30, 40), rnd(40, 30))
add(rnd(200, 5), rnd(5, 200))
alt = [[1000 if (i + k) % 2 == 0 else -1000 for k in range(4)] for i in range(2000)]
add(alt, [[1000 if (k + j) % 2 == 0 else -1000 for j in range(2000)] for k in range(4)])
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
