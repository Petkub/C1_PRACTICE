# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(904)
MAXN = 200_000
tests = []

def add(f, h):
    n = len(f)
    assert 1 <= n <= MAXN and len(h) == n
    assert all(1 <= v <= n for v in f + h)
    tests.append(f"{n}\n" + " ".join(map(str, f)) + "\n" + " ".join(map(str, h)) + "\n")

def solvable(n, rng_vals):
    # f with a limited range, h inside the range of f
    f = [random.choice(rng_vals) for _ in range(n)]
    rf = sorted(set(f))
    h = [random.choice(rf) for _ in range(n)]
    return f, h

# samples
add([2, 3, 2], [2, 3, 2])
add([2, 2, 3, 3], [2, 1, 3, 2])
add([1], [1])
add([3, 1, 2], [1, 2, 3])
add([4, 4, 4, 4, 4], [4, 4, 4, 4, 4])
# hidden
add([1, 1], [2, 1])
add([2, 1], [1, 2])
n = 100_000
perm = list(range(1, n + 1)); random.shuffle(perm)
add(perm, [random.randint(1, n) for _ in range(n)])          # bijective f: always solvable
f = [1] * MAXN; f[-1] = 2
add(f, [2] * MAXN)                                                # only preimage of 2 is the last one
f = [random.randint(2, 10) for _ in range(n)]
h = [random.randint(2, 10) for _ in range(n)]; h[-1] = 1
add(f, h)                                                      # fails only at the very end
add(*solvable(50_000, list(range(1, 11))))
add(*solvable(1000, list(range(500, 1001))))
for sz in (5, 8, 10):
    add(*solvable(sz, list(range(1, sz + 1))))
f = [random.randint(1, 8) for _ in range(8)]
add(f, [random.randint(1, 8) for _ in range(8)])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
