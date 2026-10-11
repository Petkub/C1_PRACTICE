# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(802)
tests = []

def add(F, U, D, S, reqs):
    assert 2 <= F <= 10**6 and 1 <= len(reqs) <= 10**5
    assert 1 <= U <= 1000 and 1 <= D <= 1000 and 1 <= S <= 1000
    lines = [f"{F} {len(reqs)} {U} {D} {S}"]
    for a, b in reqs:
        assert 1 <= a <= F and 1 <= b <= F and a != b
        lines.append(f"{a} {b}")
    tests.append("\n".join(lines) + "\n")

def rnd(F, n):
    out = []
    for _ in range(n):
        a = random.randint(1, F)
        b = random.randint(1, F - 1)
        if b >= a:
            b += 1
        out.append((a, b))
    return out

# samples
add(6, 2, 3, 5, [(3, 5), (2, 1)])
add(4, 1, 1, 10, [(1, 2), (2, 4)])
add(10, 7, 2, 3, [(10, 1)])
add(5, 3, 3, 1, [(2, 4), (4, 2), (3, 5)])
add(8, 1, 2, 4, [(5, 3), (3, 5), (5, 3)])
# hidden
add(2, 1, 1, 1, [(2, 1)])
add(2, 1000, 1000, 1000, [(1, 2)])
add(10**6, 1000, 1000, 1000, [(10**6, 1), (1, 10**6)] * 50000)    # max time
add(10**6, 1, 1000, 1, [(1, 10**6)] * 100000)                      # long empty trips down
add(10**6, 5, 7, 9, rnd(10**6, 40000))
add(100, 3, 2, 4, rnd(100, 50000))
add(3, 1, 2, 3, rnd(3, 1000))
add(50, 9, 1, 2, rnd(50, 20))
add(1000, 1, 1, 1, [(7, 9), (9, 7), (500, 9), (7, 500)])            # ties 7 and 9
add(10, 2, 3, 4, [(10, 9), (9, 10), (8, 10)])                       # 10 most
add(10**6, 1000, 1, 1000, [(10**6 - i, 10**6 - i - 1) for i in range(1000)])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
