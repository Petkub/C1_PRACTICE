# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(807)
tests = []

def add(N, ops):
    assert 1 <= N <= 2000 and 1 <= len(ops) <= 20000
    nb = 0
    for t, x in ops:
        if t == "B":
            nb += 1
            assert 1 <= x <= N
        else:
            assert t == "C" and 1 <= x <= nb
    tests.append(f"{N} {len(ops)}\n" + "".join(f"{t} {x}\n" for t, x in ops))

def rnd(N, Q, kmax, pc):
    ops, nb = [], 0
    for _ in range(Q):
        if nb > 0 and random.random() < pc:
            ops.append(("C", random.randint(max(1, nb - 30), nb) if random.random() < 0.8 else random.randint(1, nb)))
        else:
            nb += 1
            ops.append(("B", random.randint(1, kmax)))
    return ops

# samples
add(10, [("B", 3), ("B", 2), ("B", 4), ("B", 2), ("C", 2), ("B", 2)])
add(5, [("B", 3), ("B", 3), ("C", 2), ("C", 1), ("C", 1), ("B", 5)])
add(5, [("B", 2), ("B", 2), ("C", 1), ("B", 3)])
add(1, [("B", 1), ("B", 1), ("C", 1), ("C", 2), ("B", 1)])
add(8, [("B", 1), ("B", 1), ("B", 1), ("C", 2), ("B", 2)])
# hidden
add(1, [("B", 1)])
add(2000, [("B", 1)] * 2000 + [("C", j) for j in range(1, 2001, 2)] + [("B", 2)] * 100 + [("B", 1)] * 1000)
ops = [("B", 999), ("B", 1), ("C", 1)]
for i in range(9998):
    ops.append(("B", 1001) if i % 2 == 0 else ("B", 1000))     # fails after scanning everything / fits at 1001
    if i % 2 == 1:
        ops[-1:] = [("B", 999), ("C", 2 + i + 1)]                # books 1..999 then cancels it again
ops.append(("B", 999))
add(2000, ops[:20000])
add(2000, [("B", 1)] + [("B", 999), ("B", 999), ("C", 2), ("C", 3)] * 4999 + [("B", 1000), ("B", 1000), ("B", 2000)])
add(2000, rnd(2000, 20000, 60, 0.45))
add(2000, rnd(2000, 20000, 1000, 0.5))
add(300, rnd(300, 20000, 10, 0.4))
add(50, rnd(50, 200, 8, 0.4))
add(15, rnd(15, 60, 5, 0.35))
add(2000, [("B", 2000), ("B", 1), ("C", 1), ("C", 1), ("B", 1), ("B", 1999), ("B", 1)])
add(30, rnd(30, 100, 30, 0.3))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
