# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(503)
V = 10**9
K = 10**18
tests = []

def add(a, ops):
    n, q = len(a), len(ops)
    assert 1 <= n <= 100_000 and 1 <= q <= 100
    assert all(-V <= x <= V for x in a)
    assert all(c in "LR" and 0 <= k <= K for c, k in ops)
    tests.append(f"{n} {q}\n" + " ".join(map(str, a)) + "\n" + "".join(f"{c} {k}\n" for c, k in ops))

def rops(q, kmax):
    return [(random.choice("LR"), random.randint(0, kmax)) for _ in range(q)]

# samples
add([1, 2, 3, 4, 5], [("L", 2), ("R", 1)])
add([10, 20, 30], [("L", 7)])
add([-5], [("R", 999999999999999999)])
add([4, 8, 15, 16, 23, 42], [("R", 3), ("R", 4), ("L", 0)])
add([1, 2, 3, 4], [("R", 1), ("L", 5), ("R", 999999999999999999)])
# hidden
add([7, 8], [("L", 1)])
add([1, 2, 3], [("R", 0)] * 3)
add(list(range(1, 11)), [("L", 10), ("R", 20)])
add(list(range(1, 21)), rops(30, 50))
add([random.randint(-100, 100) for _ in range(37)], rops(100, 1000))
add([random.randint(-V, V) for _ in range(1000)], rops(100, 5000))
add([random.randint(-1000, 1000) for _ in range(99_991)], rops(100, K))
add(list(range(1, 100_001)), [("L", K)] * 100)
add(list(range(100_000, 0, -1)), [("R", K)] * 50 + [("L", K - 1)] * 50)
add([V, -V, 0] * 700, rops(100, K))
add(list(range(1, 100_001)), [("L", 3 * 10**17 + 12_345)] + rops(99, K))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
