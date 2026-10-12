# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(616)
tests = []

def add(n, m, ops):
    assert 1 <= n <= 10**5 and 1 <= m <= 10**5 and 1 <= len(ops) <= 10**5
    h, w = n, m
    asked = 0
    lines = []
    for o in ops:
        if o[0] == "T":
            h, w = w, h
            lines.append("T")
        elif o[0] == "R":
            assert 1 <= o[1] <= h and 1 <= o[2] <= h
            lines.append(f"R {o[1]} {o[2]}")
        elif o[0] == "C":
            assert 1 <= o[1] <= w and 1 <= o[2] <= w
            lines.append(f"C {o[1]} {o[2]}")
        else:
            assert o[0] == "?" and 1 <= o[1] <= h and 1 <= o[2] <= w
            asked += 1
            lines.append(f"? {o[1]} {o[2]}")
    assert asked >= 1
    tests.append(f"{n} {m} {len(ops)}\n" + "".join(l + "\n" for l in lines))

def rops(n, m, q, weights=(3, 3, 1, 3), near=None):
    h, w = n, m
    ops = []
    for _ in range(q):
        t = random.choices("RCT?", weights)[0]
        pick = (lambda lim: random.randint(max(1, lim - near), lim)) if near else (lambda lim: random.randint(1, lim))
        if t == "T":
            ops.append(("T",))
            h, w = w, h
        elif t == "R":
            ops.append(("R", pick(h), pick(h)))
        elif t == "C":
            ops.append(("C", pick(w), pick(w)))
        else:
            ops.append(("?", pick(h), pick(w)))
    if not any(o[0] == "?" for o in ops):
        ops[-1] = ("?", 1, 1) if ops[-1][0] != "T" else ops[-1]
        ops.append(("?", 1, 1))
    return ops

# samples
add(2, 3, [("?", 1, 3), ("R", 1, 2), ("?", 1, 3), ("T",), ("?", 3, 1), ("C", 1, 2), ("?", 3, 1), ("?", 1, 2)])
add(1, 4, [("T",), ("R", 1, 4), ("?", 1, 1), ("?", 4, 1), ("C", 1, 1), ("?", 2, 1)])
add(3, 3, [("T",), ("T",), ("?", 2, 3), ("T",), ("?", 2, 3)])
add(1, 1, [("?", 1, 1)])
add(3, 2, [("C", 1, 2), ("R", 1, 3), ("T",), ("R", 1, 2), ("?", 1, 1), ("?", 2, 3)])
# hidden
add(10**5, 10**5, [("?", 10**5, 10**5), ("T",), ("?", 1, 10**5), ("R", 1, 10**5), ("?", 1, 1)])
add(10**5, 10**5, rops(10**5, 10**5, 100000, near=50))
add(10**5, 1, rops(10**5, 1, 30000))
add(1, 10**5, rops(1, 10**5, 30000, near=40))
add(99999, 100000, rops(99999, 100000, 30000, weights=(2, 2, 2, 4)))
add(1000, 7, rops(1000, 7, 20000))
add(4, 5, rops(4, 5, 12))
add(6, 6, rops(6, 6, 25))
add(30, 20, rops(30, 20, 200))
add(5, 9, [("T",)] * 7 + [("?", 9, 5), ("?", 1, 1)])
add(50, 60, rops(50, 60, 3000, weights=(1, 1, 5, 2)))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
