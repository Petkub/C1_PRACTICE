# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(513)
M = 10**9
tests = []

def add(p):
    n = len(p)
    assert 1 <= n <= 100_000
    assert all(1 <= v <= M for v in p)
    tests.append(f"{n}\n" + " ".join(map(str, p)) + "\n")

def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]

def walk(n, start, step):
    p, v = [], start
    for _ in range(n):
        v = min(M, max(1, v + random.randint(-step, step)))
        p.append(v)
    return p

# samples
add([3, 8, 2, 5, 1, 9])
add([9, 7, 5, 3, 1])
add([1, 2, 3, 4, 5])
add([5])
add([1, 5, 2, 6, 3, 7, 4])
add([1, M, 1, M, 1])
# hidden
add([2, 2])
add([1, 3, 1])
add([5, 1, 9, 2, 10])                 # the best single trade 1 -> 10 is not part of the answer
add([1, 10, 9, 20])                   # one long trade 1 -> 20 beats two
add(rnd(10, 1, 20))
add(rnd(40, 1, 100))
add(walk(150, 500, 30))
add(rnd(150, 1, M))
# max
add(walk(100_000, 50_000, 100))
add(rnd(100_000, 1, 1000))
add(list(range(100_000, 0, -1)))     # strictly falling
add([1, M] * 50_000)
p = rnd(50_000, 400_000_000, 600_000_000)
p[10] = 1
p[30_000] = M
p[30_001] = 1
p[49_990] = M
add(p)

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
