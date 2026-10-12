# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(512)
M = 10**9
tests = []

def add(x):
    n = len(x)
    assert 1 <= n <= 100_000
    assert all(-M <= v <= M for v in x)
    tests.append(f"{n}\n" + " ".join(map(str, x)) + "\n")

def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]

# samples
add([1, 5, 2])
add([10, 2, 6, 4])
add([-7])
add([3, 3])
add([1, 1, 1, 9, 9, 9])
add([4, 4, 4, 4, 100])
# hidden
add([0, 1])
add([5, -5])
add(rnd(7, -20, 20))
add(rnd(10, 0, 30))
add(rnd(100, -300, 300))
add(rnd(400, 1, 2000))
add([2] * 200 + [1000] * 200)                       # every P in [2, 1000]
# max
add([-M] * 30_000 + [M] * 30_000)                   # 2 * 10^9 + 1 positions, D = 6 * 10^13
add(rnd(80_000, -M, M))
add(rnd(50_001, -M, M))
add([M] * 9_999 + [-M])
add(rnd(100_000, -100, 100))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
