# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(820)
tests = []

def add(L, T, ants):
    n = len(ants)
    assert 1 <= n <= 10**5 and 2 <= L <= 10**9 and 1 <= T <= 10**9
    assert len(set(p for p, _ in ants)) == n and all(0 < p < L and d in "LR" for p, d in ants)
    tests.append(f"{n} {L} {T}\n" + "".join(f"{p} {d}\n" for p, d in ants))

def rnd(n, L, T):
    ps = random.sample(range(1, L), n)
    return L, T, [(p, random.choice("LR")) for p in ps]

# samples
add(10, 3, [(2, "R"), (5, "L"), (8, "R")])
add(6, 4, [(4, "L"), (2, "R"), (5, "R")])
add(10, 2, [(7, "L"), (3, "R")])
add(5, 3, [(1, "R"), (4, "L")])
add(20, 6, [(9, "R"), (1, "L"), (12, "L"), (10, "L"), (17, "R"), (5, "R")])
# hidden
add(2, 1, [(1, "L")])
add(2, 1, [(1, "R")])
add(10**9, 10**9, [(10**9 - 1, "R"), (1, "L")])
add(10**9, 10**9 - 1, [(1, "R"), (2, "L")])
add(*rnd(10**5, 10**9, 10**9))
add(*rnd(30000, 10**9, 3 * 10**8))
add(*rnd(50000, 10**5, 1000))
add(*rnd(30000, 10**9, 10**4))
add(*rnd(50, 100, 37))
add(*rnd(99, 100, 60))
add(*rnd(200, 1000, 700))
add(*rnd(20, 30, 15))
add(1000, 500, [(i, "R" if i % 2 else "L") for i in range(1, 1000)])
add(100, 50, [(i, "R") for i in range(1, 50)] + [(i, "L") for i in range(51, 100)])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
