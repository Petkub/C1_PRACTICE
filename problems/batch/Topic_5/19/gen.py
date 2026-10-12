# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(519)
M = 10**9
tests = []

def add(s):
    n = len(s)
    assert 1 <= n <= 100_000
    assert all(1 <= x <= M for x in s)
    tests.append(f"{n}\n" + " ".join(map(str, s)) + "\n")

def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]

def mountains(n, maxrun):
    # alternating strictly rising and falling runs of random lengths
    s, v, up = [], 500_000, True
    while len(s) < n:
        for _ in range(random.randint(1, maxrun)):
            if len(s) == n:
                break
            v += random.randint(1, 3) if up else -random.randint(1, 3)
            s.append(v)
        up = not up
    return s

# samples
add([1, 3, 5, 4, 2])
add([7, 7, 7, 7])
add([10])
add([5, 4, 3, 3, 4, 5])
add([1, 2, 2, 1, 3, 1])
add([2, 4, 6, 8, 3, 1, 9])
# hidden
add([1, 2])
add([2, 1])
add([3, 3])
add(rnd(10, 1, 5))
add(rnd(50, 1, 3))
add(mountains(300, 20))
add(rnd(2000, 1, M))
# max
add(list(range(100_000, 0, -1)))                  # one long falling run
add(list(range(1, 50_001)) + list(range(50_000, 0, -1)))   # peak in the middle, equal pair at top
add(mountains(100_000, 1000))
add(rnd(100_000, 1, 10))
add([5] * 100_000)

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
