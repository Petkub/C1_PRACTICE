# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(801)
tests = []

def add(start, legs):
    H, M, S = start
    assert 0 <= H <= 23 and 0 <= M <= 59 and 0 <= S <= 59
    assert 1 <= len(legs) <= 10000
    lines = [f"{H:02d}:{M:02d}:{S:02d}", str(len(legs))]
    for h, m, s in legs:
        assert 0 <= h <= 10**6 and 0 <= m <= 59 and 0 <= s <= 59
        lines.append(f"{h}:{m:02d}:{s:02d}")
    tests.append("\n".join(lines) + "\n")

# samples
add((22, 30, 0), [(1, 0, 0), (0, 45, 30)])
add((20, 0, 0), [(2, 30, 0), (1, 29, 59)])
add((23, 59, 59), [(0, 0, 1)])
add((7, 15, 40), [(50, 0, 0), (0, 44, 20), (0, 0, 0)])
add((0, 0, 0), [(24, 0, 0), (47, 59, 59), (0, 0, 1)])
# hidden
add((0, 0, 0), [(0, 0, 0)])
add((12, 0, 0), [(0, 59, 59), (0, 0, 1)])
add((23, 0, 0), [(0, 59, 59)] * 1)
add((23, 59, 59), [(10**6, 59, 59)] * 10000)
add((5, 6, 7), [(10**6, 0, 0)] * 10000)
add((0, 0, 1), [(0, 59, 59)] * 10000)
add((13, 13, 13), [(0, 0, 59)] * 9999 + [(0, 0, 1)])
for n, hmax in [(10, 30), (1000, 100), (5000, 10**6), (10000, 10**6), (10000, 0)]:
    st = (random.randint(0, 23), random.randint(0, 59), random.randint(0, 59))
    add(st, [(random.randint(0, hmax), random.randint(0, 59), random.randint(0, 59)) for _ in range(n)])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
