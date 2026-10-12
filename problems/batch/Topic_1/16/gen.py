# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(1016)
tests = []

def add(k, qs):
    assert 1 <= k <= 60 and 1 <= len(qs) <= 100_000
    for t, v in qs:
        assert t in (1, 2) and 1 <= v <= 2**k
    tests.append(f"{k} {len(qs)}\n" + "".join(f"{t} {v}\n" for t, v in qs))

def rand_q(k, cnt):
    m = 2**k
    qs = []
    for _ in range(cnt):
        r = random.random()
        if r < 0.1:
            v = random.choice([1, 2, m, m - 1, m // 2, m // 2 + 1, max(1, m // 4)])
        else:
            v = random.randint(1, m)
        qs.append((random.randint(1, 2), max(1, v)))
    return qs

def all_q(k):
    m = 2**k
    return [(1, x) for x in range(1, m + 1)] + [(2, j) for j in range(1, m + 1)]

# samples
add(2, [(1, 3), (1, 2), (2, 2), (2, 1)])
add(3, [(1, 5), (1, 2), (2, 6), (2, 4)])
add(1, [(1, 1), (1, 2), (2, 1), (2, 2)])
add(4, [(1, 7), (1, 10), (1, 16), (2, 3), (2, 16)])
add(5, [(1, 20), (2, 20), (2, 32)])
# hidden, small (checked by the brute)
add(1, all_q(1))
add(3, all_q(3))
add(6, all_q(6))
add(10, all_q(10))
add(12, rand_q(12, 5000))
add(16, rand_q(16, 20_000))
add(20, rand_q(20, 30_000))
# hidden, big
add(60, [(1, 1), (1, 2**60), (1, 2**59), (1, 2**59 + 1), (2, 1), (2, 2**60), (2, 2**59), (2, 2**59 + 1), (1, 2), (2, 2)])
add(31, rand_q(31, 30_000))
add(60, rand_q(60, 40_000))
add(59, rand_q(59, 30_000))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
