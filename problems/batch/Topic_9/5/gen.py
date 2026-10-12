# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(905)
tests = []

def add(n, r, s):
    assert 1 <= n <= 100
    for rel in (r, s):
        assert 0 <= len(rel) <= n * n
        assert len(set(rel)) == len(rel)
        for a, b in rel:
            assert 1 <= a <= n and 1 <= b <= n
    lines = [str(n), str(len(r))] + [f"{a} {b}" for a, b in r] + [str(len(s))] + [f"{a} {b}" for a, b in s]
    tests.append("\n".join(lines) + "\n")

def rand_rel(n, p):
    rel = [(a, b) for a in range(1, n + 1) for b in range(1, n + 1) if random.random() < p]
    random.shuffle(rel)
    return rel

# samples
add(3, [(1, 2), (2, 3)], [(2, 1), (3, 3), (2, 2)])
add(2, [(1, 2)], [(1, 2)])
add(3, [(1, 1), (1, 2)], [(1, 3), (2, 3)])
add(1, [(1, 1)], [(1, 1)])
add(3, [], [(1, 2), (2, 3)])
# hidden
add(4, [(4, 1), (3, 2), (1, 4)], [(1, 2), (1, 3), (2, 4), (4, 4)])
add(1, [], [])
add(5, [(1, 2), (2, 3), (3, 4)], [])
add(100, [(i, i) for i in range(1, 101)], rand_rel(100, 0.05))            # identity first
add(100, rand_rel(100, 0.05), [(i, i) for i in range(1, 101)])            # identity second
full = [(a, b) for a in range(1, 101) for b in range(1, 101)]
add(100, full, full)
add(100, [(1, b) for b in range(1, 101)], [(b, 1) for b in range(1, 101)])  # one pair from 100 paths
add(100, [(a, 1) for a in range(1, 101)], [(1, c) for c in range(1, 101)])  # all pairs through b = 1
perm1 = list(range(1, 101)); random.shuffle(perm1)
perm2 = list(range(1, 101)); random.shuffle(perm2)
add(100, [(i + 1, perm1[i]) for i in range(100)], [(i + 1, perm2[i]) for i in range(100)])
add(100, [(a, b) for a in range(1, 101) for b in range(1, 101) if a < b],
    [(a, b) for a in range(1, 101) for b in range(1, 101) if a < b])        # strict order composed
add(100, [(a, b) for a in range(1, 51) for b in range(1, 51)],
    [(a, b) for a in range(51, 101) for b in range(51, 101)])               # never meet
for n, p in ((6, 0.3), (20, 0.1), (100, 0.01), (100, 0.2)):
    add(n, rand_rel(n, p), rand_rel(n, p))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
