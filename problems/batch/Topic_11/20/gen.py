# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(1120)
tests = []

def add(cap, apps):
    F, n = len(cap), len(apps)
    assert 1 <= F <= 100 and 1 <= n <= 100_000
    assert all(1 <= c <= n for c in cap)
    lines = [f"{F} {n}", " ".join(map(str, cap))]
    for s, ch in apps:
        assert 0 <= s <= 10**6
        assert 1 <= len(ch) <= 4 and len(set(ch)) == len(ch) and all(1 <= f <= F for f in ch)
        lines.append(f"{s} {len(ch)} " + " ".join(map(str, ch)))
    tests.append("\n".join(lines) + "\n")

def rnd(F, n, smax, kmax, cmax, skew=False):
    cap = [random.randint(1, min(cmax, n)) for _ in range(F)]
    apps = []
    for _ in range(n):
        k = random.randint(1, min(kmax, F))
        if skew:   # popular faculties are chosen more often
            ch = []
            while len(ch) < k:
                f = min(F, int(random.expovariate(3 / F)) + 1)
                if f not in ch:
                    ch.append(f)
        else:
            ch = random.sample(range(1, F + 1), k)
        apps.append((random.randint(0, smax), ch))
    return cap, apps

# samples
add([2, 1], [(90, [1, 2]), (85, [1]), (85, [2, 1]), (80, [1, 2])])
add([1, 2], [(50, [1, 2]), (50, [1, 2]), (50, [1]), (40, [1, 2])])
add([2, 1, 2], [(60, [3]), (75, [1, 3]), (60, [2, 3]), (75, [2]), (60, [2]), (40, [3, 1])])
add([1, 1], [(0, [1, 2]), (0, [1]), (0, [1, 2])])
add([1], [(0, [1])])
# hidden (small)
add([1], [(5, [1]), (5, [1]), (5, [1]), (6, [1])])
add([1, 1, 1], [(10, [2, 1]), (9, [2, 3]), (9, [2]), (8, [1, 3]), (8, [3, 1]), (7, [1, 2, 3])])
add([3, 3], [(0, [2, 1])] * 7)
add(*rnd(3, 12, 5, 3, 2))
add(*rnd(5, 40, 10, 4, 4))
add(*rnd(8, 200, 30, 4, 10, skew=True))
add(*rnd(4, 300, 10**6, 4, 60))
# large
add(*rnd(100, 100_000, 999, 2, 1500, skew=True))
add(*rnd(100, 40_000, 10**6, 4, 600))
add(*rnd(100, 30_000, 0, 4, 300, skew=True))                  # everyone tied
add(*rnd(5, 20_000, 50, 4, 3000))
cap = [random.randint(1, 3) for _ in range(100)]                # tiny capacities, all tied in pairs
apps = []
for s in range(10_000):
    ch = random.sample(range(1, 101), 4)
    apps += [(s, ch), (s, ch[:])]
add(cap, apps)

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
