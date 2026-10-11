# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(106)
G = 10**9
tests = []

def inside(r, x, y):
    x1, y1, x2, y2 = r
    return x1 < x < x2 and y1 < y < y2

def add(r, qs):
    x1, y1, x2, y2 = r
    assert -G <= x1 < x2 <= G and -G <= y1 < y2 <= G
    assert 1 <= len(qs) <= 100_000
    for a, b, c, d in qs:
        assert all(-G <= v <= G for v in (a, b, c, d))
        assert not inside(r, a, b) and not inside(r, c, d)
    tests.append(f"{x1} {y1} {x2} {y2}\n{len(qs)}\n" + "".join(f"{a} {b} {c} {d}\n" for a, b, c, d in qs))

def rand_point(r, lo, hi, bias):
    x1, y1, x2, y2 = r
    while True:
        if random.random() < bias:
            # a point in a column or row crossing the building (interesting cases)
            if random.random() < 0.5:
                x = random.randint(x1, x2)
                y = random.choice([random.randint(lo, y1), random.randint(y2, hi)])
            else:
                y = random.randint(y1, y2)
                x = random.choice([random.randint(lo, x1), random.randint(x2, hi)])
        else:
            x, y = random.randint(lo, hi), random.randint(lo, hi)
        if lo <= x <= hi and lo <= y <= hi and not inside(r, x, y):
            return x, y

def queries(r, n, lo, hi, bias=0.7):
    return [rand_point(r, lo, hi, bias) + rand_point(r, lo, hi, bias) for _ in range(n)]

# samples
add((0, 0, 4, 3), [(2, -1, 2, 5), (0, 0, 4, 3), (1, 0, 3, 3)])
add((0, 0, 2, 2), [(1, 0, 1, 2), (-1, 1, 3, 1), (1, 0, 1, 5)])
add((0, 0, 1, 5), [(0, 2, 1, 2), (-3, 3, 4, 3)])
add((-2, -2, 6, 3), [(5, -4, 5, 4), (-3, 0, 7, 0), (-3, 0, 7, 5), (0, 3, 0, 3)])
add((1, 1, 9, 9), [(5, 0, 5, 10), (0, 5, 10, 5), (2, 0, 8, 10), (8, 0, 2, 9)])
# hidden, small (checked by the brute)
for _ in range(3):
    x1, y1 = random.randint(-8, 5), random.randint(-8, 5)
    r = (x1, y1, x1 + random.randint(1, 9), y1 + random.randint(1, 9))
    add(r, queries(r, 400, -12, 14))
r = (-20, -5, 25, 30)
add(r, queries(r, 300, -30, 40, 0.9))
r = (0, 0, 2, 100)                       # one column of inside points
add(r, queries(r, 300, -5, 105, 0.9))
# hidden, big
r = (-G, -G, G, G)
add(r, [(0, -G, 0, G), (-G, 0, G, 0), (-G, -G, G, G), (1, -G, 2, G), (G - 1, G, -G + 1, -G), (-G, -G, -G, G)])
r = (-G, -5, G, 5)
add(r, [(0, -5, 0, 5), (-G + 1, 5, G - 1, -5), (-G, 0, G, 0), (3, -G, 4, G)])
r = (-123_456_789, -987_654_321, 876_543_210, 12_345_678)
add(r, queries(r, 50_000, -G, G, 0.8))
r = (-G + 1, -G + 1, G - 1, G - 1)
add(r, queries(r, 20_000, -G, G, 0.9))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
