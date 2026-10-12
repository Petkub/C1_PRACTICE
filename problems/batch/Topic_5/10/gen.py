# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(506)
C = 100_000
tests = []

def add(c, k):
    n = len(c)
    assert 1 <= k <= n <= 100_000
    assert all(1 <= x <= C for x in c)
    tests.append(f"{n} {k}\n" + " ".join(map(str, c)) + "\n")

def rnd(n, m):
    return [random.randint(1, m) for _ in range(n)]

# samples
add([5, 2, 5, 7, 7, 2], 3)
add([1, 2, 1, 2, 1], 2)
add([9], 1)
add([4, 4, 4, 4], 3)
add([3, 1, 3, 2, 1, 4, 2, 2], 4)
# hidden
add([1, 1, 2, 3], 4)
add([100000, 1, 100000], 2)
add(rnd(10, 3), 4)
add(rnd(50, 10), 7)
add(rnd(300, 40), 25)
add(rnd(2000, 500), 300)
# max: best window only near the end
c = [random.randint(1, 50) for _ in range(99_000)] + list(range(1, 1001))
add(c, 1000)
add(rnd(100_000, C), 50_000)
add(rnd(100_000, 30_000), 40_000)
add(list(range(1, 100_001)), 100_000)
add([7] * 100_000, 1)
c = [(i % 1000) + 1 for i in range(100_000)]
add(c, 77_777)                       # every window has all 1000 values -> l = 1

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
