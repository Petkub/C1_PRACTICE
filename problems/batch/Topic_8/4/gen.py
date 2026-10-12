# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(804)
tests = []

def add(C, S, days):
    assert 1 <= C <= 10**9 and 0 <= S <= C and 1 <= len(days) <= 10**5
    lines = [f"{C} {S} {len(days)}"]
    for a, b in days:
        assert 0 <= a <= 10**9 and 0 <= b <= 10**9
        lines.append(f"{a} {b}")
    tests.append("\n".join(lines) + "\n")

def rnd(n, ma, mb):
    return [(random.randint(0, ma), random.randint(0, mb)) for _ in range(n)]

# samples
add(10, 3, [(5, 4), (9, 2), (0, 10), (2, 1)])
add(7, 2, [(5, 7)])
add(5, 5, [(3, 0), (0, 6), (10, 5)])
add(100, 0, [(0, 0), (0, 1), (40, 30), (100, 70)])
add(20, 20, [(0, 20), (0, 0), (25, 21)])
# hidden
add(1, 0, [(0, 0)])
add(1, 1, [(10**9, 10**9)])
add(10**9, 0, [(10**9, 0)] * 10**5)                 # max overflow
add(10**9, 10**9, [(0, 10**9)] * 30000)              # empty from day 2, much buying
add(10**9, 10**9, [(10**9, 10**9 - 1)] * 20000)      # w + a reaches 2e9
add(10**9, 500, rnd(20000, 10**9, 10**9))
add(1000, 0, rnd(30000, 1000, 1000))
add(50, 25, rnd(30, 40, 40))
add(12, 6, [(6, 12), (12, 12), (13, 0), (0, 13), (6, 5)])   # exact full / exact empty
add(10**6, 123, rnd(5000, 3 * 10**5, 3 * 10**5))
add(9, 4, rnd(12, 6, 6))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
