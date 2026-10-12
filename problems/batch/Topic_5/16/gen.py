# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(516)
M = 10**9
tests = []

def add(a):
    n = len(a)
    assert 3 <= n <= 100_000
    assert all(-M <= x <= M for x in a)
    tests.append(f"{n}\n" + " ".join(map(str, a)) + "\n")

def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]

def fix_total(a, mult):
    # change the last element so that the total is a multiple of 3 (if mult) or not
    s = sum(a) - a[-1]
    for d in range(0, 10):
        for v in (a[-1] - d, a[-1] + d):
            if -M <= v <= M and ((s + v) % 3 == 0) == mult:
                a[-1] = v
                return a
    raise AssertionError

def zero_walk(n, step):
    # small steps so that the prefix sums hit t and 2t many times
    return fix_total(rnd(n, -step, step), True)

# samples
add([1, 2, 3, 0, 3])
add([1, 1, 1, 2])
add([4, 4, 4])
add([0, 0, 0, 0, 0])
add([1, -1, 1, -1, 1, -1])
add([0, -3, -3, -1, 1, 0, -3])
# hidden
add([1, 2, 3])
add([M, M, M])
add([-M, -M, -M, 0])
add([3, -3, 0])
add(zero_walk(10, 2))
add(zero_walk(60, 1))
add(zero_walk(500, 3))
add(fix_total(rnd(2000, -1, 1), False))
# max
add([0] * 100_000)                                    # answer C(99999, 2)
add(zero_walk(100_000, 1))
a = [M] * 30_000 + [-M] * 30_000 + [M] * 30_000       # t = 10^13, prefix sums above 2^31
add(a)
add(fix_total(rnd(80_000, -M, M), True))
add([1] + [1, -1] * 49_998 + [1, 1])                  # t = 1, prefix sums 1, 2, 1, 2, ...

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
