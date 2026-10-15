# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(1206)
tests = []

def add(L, cars):
    n = len(cars)
    assert 1 <= n <= 100_000
    assert 0 <= L <= n
    for i, (a, d) in enumerate(cars):
        assert 0 <= a <= 10**9 and 1 <= d <= 10**4
        if i > 0:
            assert cars[i - 1][0] <= a
    tests.append(f"{n} {L}\n" + "".join(f"{a} {d}\n" for a, d in cars))

def rnd(n, L, amax, dmax, dmin=1):
    ts = sorted(random.randint(0, amax) for _ in range(n))
    return L, [(t, random.randint(dmin, dmax)) for t in ts]

# samples
add(1, [(0, 3), (1, 2), (2, 1), (3, 2), (3, 1)])
add(0, [(0, 2), (2, 2), (3, 1), (4, 5)])
add(2, [(5, 1), (5, 2), (5, 3), (5, 4)])
add(1, [(0, 5), (10, 1), (10, 1)])
add(0, [(10**9, 10**4)])
# hidden (small)
add(0, [(0, 1)])
add(1, [(0, 1), (0, 1), (1, 1), (1, 1), (2, 1), (2, 1)])        # finish and arrival at the same minute
add(3, [(7, 2)] * 3 + [(9, 4)] * 3)
add(*rnd(10, 2, 20, 5))
add(*rnd(30, 0, 60, 6))
add(*rnd(40, 3, 50, 8))
add(*rnd(60, 60, 100, 10))
add(*rnd(200, 5, 1000, 20))
# large
add(*rnd(100_000, 30, 1_000_000, 30))
add(*rnd(30_000, 30_000, 10**9, 10**4, 9_000))                     # nobody leaves, big times
add(40_000, [(0, 10_000)] * 40_000)                                # all at once
add(*rnd(30_000, 1, 10**9, 10**4))
add(*rnd(40_000, 3, 1_000_000, 50))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
