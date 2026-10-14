# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(1207)
tests = []

def add(v):
    n = len(v)
    assert 1 <= n <= 100_000
    assert all(1 <= x <= 10**9 for x in v)
    tests.append(f"{n}\n" + " ".join(map(str, v)) + "\n")

def rnd(n, vmax):
    return [random.randint(1, vmax) for _ in range(n)]

# samples
add([2, 7, 3, 9, 4])
add([4, 9, 1, 4])
add([7])
add([1, 2, 3, 4, 5, 6])
add([5, 5, 5, 5, 5])
add([3, 8, 8, 3, 8, 3, 8])
# hidden (small)
add([1, 10**9])
add([10**9] * 3)
add([6, 1, 1, 6, 1, 6])
add(rnd(15, 9))
add(rnd(40, 3))
add(rnd(500, 1000))
add(list(range(1, 2001)) + list(range(2000, 0, -1)))
# large
add([10**9] * 100_000)                                   # totals 5 * 10^13
add(rnd(100_000, 9))
add(rnd(60_000, 10**9))
v = rnd(30_000, 10**9); add(v + v[::-1])                 # palindrome: ties at both ends all the time

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
