# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(602)
MAXV = 10**9
tests = []

def add(g):
    r, c = len(g), len(g[0])
    assert 1 <= r <= 300 and 1 <= c <= 300
    assert all(len(row) == c and all(0 <= x <= MAXV for x in row) for row in g)
    tests.append(f"{r} {c}\n" + "".join(" ".join(map(str, row)) + "\n" for row in g))

def rnd(r, c, lo, hi):
    return [[random.randint(lo, hi) for _ in range(c)] for _ in range(r)]

# samples
add([[1, 2, 3, 6], [4, 1, 1, 2], [5, 2, 0, 1]])
add([[1, 2, 1], [3, 7, 1], [1, 2, 7]])
add([[0]])
add([[3, 3, 3], [3, 3, 3]])
add([[4, 1, 5, 2, 9]])
# hidden
add([[MAXV]])
add([[7] * 300 for _ in range(300)])          # all equal: none
add(rnd(300, 300, 0, MAXV))
add(rnd(300, 300, 0, 2))
add([[random.randint(0, 5)] for _ in range(300)])
add([[(i + j) % 2 * 5 for j in range(40)] for i in range(40)])   # checkerboard: diagonal neighbours equal
add([[i * 100 + j for j in range(100)] for i in range(100)])     # only bottom-right corner
add([[MAXV - (i + j) for j in range(50)] for i in range(50)])    # only top-left corner
add([[1, 0], [0, 1]])
add([[2, 0], [0, 1]])
add(rnd(6, 7, 0, 3))
add(rnd(30, 20, 0, 1000))
add(rnd(200, 300, 0, 9))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
