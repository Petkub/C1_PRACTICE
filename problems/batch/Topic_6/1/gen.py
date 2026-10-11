# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(601)
MAXV = 10**9
tests = []

def add(g):
    r, c = len(g), len(g[0])
    assert 1 <= r <= 300 and 1 <= c <= 300
    assert all(len(row) == c and all(0 <= x <= MAXV for x in row) for row in g)
    s = f"{r} {c}\n" + "".join(" ".join(map(str, row)) + "\n" for row in g)
    tests.append(s)

def rnd(r, c, lo, hi):
    return [[random.randint(lo, hi) for _ in range(c)] for _ in range(r)]

# samples
add([[1, 2, 0], [4, 9, 1], [0, 0, 3]])
add([[0, 0], [0, 0]])
add([[5, 1, 1, 1]])
add([[2], [7], [1]])
add([[1, 0, 1], [0, 0, 0], [1, 0, 1]])
# hidden
add([[0]])
add([[MAXV]])
add([[MAXV] * 300 for _ in range(300)])        # overflow, all ties
add(rnd(300, 300, 0, MAXV))
add(rnd(300, 1, 0, MAXV))
add(rnd(1, 300, 0, MAXV))
g = [[0] * 50 for _ in range(40)]               # big center must not be double counted
g[10][10] = 100; g[10][30] = 60; g[20][10] = 60
add(g)
g = [[1] * 30 for _ in range(30)]               # best row/col cell differs from best cross
for j in range(30): g[3][j] = 10
for i in range(30): g[i][7] = 10
g[3][7] = 0
add(g)
add(rnd(7, 9, 0, 3))
add(rnd(20, 15, 0, 1))
add(rnd(120, 200, 0, 1000))
g = rnd(60, 60, 0, 10)
g[59][59] = MAXV
add(g)

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
