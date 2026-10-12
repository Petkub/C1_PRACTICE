# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(604)
MAXA = 10**9
tests = []

def add(g):
    r, c = len(g), len(g[0])
    assert 1 <= r <= 300 and 1 <= c <= 300
    assert all(len(row) == c and all(-MAXA <= x <= MAXA for x in row) for row in g)
    tests.append(f"{r} {c}\n" + "".join(" ".join(map(str, row)) + "\n" for row in g))

def rnd(r, c, lo, hi):
    return [[random.randint(lo, hi) for _ in range(c)] for _ in range(r)]

# samples
add([[1, -2, 3], [-4, 5, -6], [7, -8, -9]])
add([[-5, -1, -7], [-2, -3, -4]])
add([[42]])
add([[3, -1, 4, -1, 5]])
add([[2, -7], [-3, 4], [6, -1], [5, 8]])
# hidden
add([[MAXA] * 3 for _ in range(3)])
add([[-MAXA]])
add([[random.randint(-9, 9)] for _ in range(7)])
add(rnd(4, 6, -20, 20))
add(rnd(8, 5, -100, 100))
add(rnd(30, 40, -1000, 1000))
add([[-MAXA] * 300 for _ in range(300)])                 # every diagonal negative
add(rnd(300, 300, MAXA - 1000, MAXA))                    # big positive sums
add(rnd(200, 300, -999, 999))
add(rnd(300, 50, -99, 100))
# a single heavy anti-diagonal hidden in negatives
g = rnd(60, 80, -50, -1)
for i in range(60):
    j = 70 - i
    if 0 <= j < 80:
        g[i][j] = 10**7
add(g)
# heavy corner cells only
g = [[-10**6] * 50 for _ in range(40)]
g[39][0] = 5
g[0][49] = 6
g[0][0] = 7
add(g)

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
