# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(805)
tests = []

def add(P, O, K, calls):
    assert 1 <= len(calls) <= 10**4 and 1 <= P <= 10**4 and 1 <= O <= 10**4 and 0 <= K <= 10**9
    lines = [f"{len(calls)} {P} {O} {K}"]
    for (h, m, s), L in calls:
        assert 0 <= h <= 23 and 0 <= m <= 59 and 0 <= s <= 59 and 1 <= L <= 10**5
        lines.append(f"{h:02d}:{m:02d}:{s:02d} {L}")
    tests.append("\n".join(lines) + "\n")

def rt():
    return (random.randint(0, 23), random.randint(0, 59), random.randint(0, 59))

# samples
add(300, 100, 1, [((7, 59, 30), 90), ((19, 59, 59), 1)])
add(200, 50, 0, [((23, 58, 0), 121)])
add(5, 3, 10, [((12, 0, 0), 600), ((20, 0, 0), 1)])
add(1, 1, 0, [((9, 0, 0), 60), ((9, 0, 0), 61), ((8, 0, 0), 420)])
add(150, 75, 2, [((19, 58, 0), 240), ((7, 59, 59), 59)])
# hidden
add(10**4, 10**4, 10**9, [((0, 0, 0), 10**5)] * 10**4)          # all free
add(10**4, 9999, 0, [((7, 59, 1), 10**5)] * 10**4)             # max money
add(10**4, 1, 1666, [((20, 0, 0), 10**5)] * 3)                 # free ends inside a call
add(7, 3, 0, [((7, 59, 0), 60), ((7, 59, 1), 60), ((19, 59, 0), 60), ((20, 0, 0), 60), ((23, 59, 59), 2)])
add(1, 10**4, 5, [((random.randint(0, 23), 0, 0), 60 * random.randint(1, 3)) for _ in range(10)])
add(13, 29, 17, [(rt(), random.randint(1, 600)) for _ in range(200)])
add(100, 37, 3000, [(rt(), random.randint(1, 10**5)) for _ in range(300)])
add(4321, 1234, 777, [(rt(), random.randint(1, 10**5)) for _ in range(10**4)])
add(10**4, 1, 0, [(rt(), random.randint(1, 3000)) for _ in range(10**4)])
add(3, 10**4, 123456, [(rt(), random.randint(90000, 10**5)) for _ in range(10**4)])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
