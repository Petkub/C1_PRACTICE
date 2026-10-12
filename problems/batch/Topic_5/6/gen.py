# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(506)
M = 10**9
tests = []

def add(a):
    n = len(a)
    assert 2 <= n <= 100_000
    assert all(-M <= x <= M for x in a)
    tests.append(f"{n}\n" + " ".join(map(str, a)) + "\n")

def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]

# samples
add([3, 1, 4, 1, 5])
add([2, -2, 2, -2])
add([1, 2, 1])
add([7, 7])
add([-M, 1, 1, M])
add([5, -3, 0, 0, 2, -4])
# hidden
add([0, 0])
add([M, M])
add([-M, -M, -M])
add(rnd(8, -10, 10))
add(rnd(30, 0, 100))
add(rnd(200, -1000, 1000))
add([1] * 1000)                                  # split exactly in the middle
add([0] * 1000)                                  # every k gives 0, answer k = 1
# max N, huge values: sums need long long
add([M] * 30_000 + [-M] * 30_000)
add(rnd(80_000, -M, M))
add([-M] * 49_999 + [M])                         # best split is at the very end
add(rnd(100_000, -1000, 1000))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
