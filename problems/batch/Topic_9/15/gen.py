# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(912)
MAXV = 10**9
tests = []

def add(pts):
    assert 2 <= len(pts) <= 100000
    for x, y in pts:
        assert -MAXV <= x <= MAXV and -MAXV <= y <= MAXV
    tests.append(f"{len(pts)}\n" + "".join(f"{x} {y}\n" for x, y in pts))

def from_dirs(n, dirs, maxmul, zero_prob=0.0):
    pts = []
    for _ in range(n):
        if random.random() < zero_prob:
            pts.append((0, 0))
            continue
        a, b = random.choice(dirs)
        lim = maxmul
        if a: lim = min(lim, MAXV // abs(a))
        if b: lim = min(lim, MAXV // abs(b))
        k = random.randint(1, lim) * random.choice([1, -1])
        pts.append((a * k, b * k))
    return pts

# samples
add([(1, 2), (2, 4), (3, 6), (1, 1)])
add([(0, 0), (1, 2), (3, 5)])
add([(1, -2), (-1, 2), (2, -4), (-3, 6)])
add([(0, 5), (0, -3)])
add([(1, 0), (0, 1), (1, 1)])
add([(2, 3), (4, 6), (-6, -9), (3, 2), (0, 0)])
# hidden
add([(0, 0), (0, 0)])
add([(MAXV, MAXV), (-MAXV, -MAXV), (MAXV, -MAXV), (MAXV, MAXV - 1)])
add([(MAXV, 1), (1, MAXV), (MAXV - 1, MAXV), (MAXV, MAXV - 1)])          # products near 10^18
add([(0, 0)] * 100000)                                                  # answer 4999950000
add([(3, 0), (-5, 0), (0, 7), (0, -1), (0, 0), (2, 0), (0, 3)])         # axis directions
small_dirs = [(a, b) for a in range(-3, 4) for b in range(-3, 4) if (a, b) != (0, 0)]
add(from_dirs(100000, small_dirs[:6], 3000, 0.01))
add(from_dirs(30000, [(random.randint(-MAXV, MAXV), random.randint(-MAXV, MAXV)) for _ in range(200)], 1))
add([(random.randint(-MAXV, MAXV), random.randint(-MAXV, MAXV)) for _ in range(20000)])
add(from_dirs(10, small_dirs, 3, 0.2))
add(from_dirs(100, small_dirs, 5, 0.05))
add(from_dirs(2000, small_dirs, 50, 0.01))
add([(random.randint(-5, 5), random.randint(-5, 5)) for _ in range(3000)])
# coprime large directions that are NOT parallel but close (a/b vs a'/b')
add([(999999999, 999999998), (999999998, 999999997), (-999999999, -999999998), (1, 1), (999999997, 999999996)])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
