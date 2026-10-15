# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(1105)
V = 10**9
tests = []

def add(c):
    n = len(c)
    assert 1 <= n <= 100_000
    assert all(0 <= x <= V for x in c)
    tests.append(f"{n}\n" + " ".join(map(str, c)) + "\n")

def ri(lo, hi, n):
    return [random.randint(lo, hi) for _ in range(n)]

# samples
add([3, 0, 6, 1, 5])
add([4, 1000, 4, 4])
add([0, 0, 0])
add([1000000000])
add([2, 2, 2, 2, 2, 2])
add([10, 8, 5, 4, 3, 3, 1])
# hidden
add([0])
add([1])
add([1, 1, 1, 1])
add(ri(0, 10, 20))
add(ri(0, 60, 80))
add([random.choice([0, V]) for _ in range(50)])
add(ri(0, 3000, 2500))
add([100_000] * 100_000)                             # h = N
add([0] * 100_000)                                   # h = 0
p = list(range(1, 100_001)); random.shuffle(p); add(p)   # h = 50000
add([50_000] * 100_000)
add([4_999] * 5_000 + [5_001] * 5_000)
add(ri(0, 120_000, 60_000))
add(ri(0, V, 30_000))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
