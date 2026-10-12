# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(607)
tests = []

def add(g):
    r, c = len(g), len(g[0])
    assert 1 <= r <= 500 and 1 <= c <= 500
    assert all(len(row) == c and set(row) <= set("./\\") for row in g)
    tests.append(f"{r} {c}\n" + "".join(row + "\n" for row in g))

def rnd(r, c, p):
    return ["".join(random.choice("/\\") if random.random() < p else "." for _ in range(c)) for _ in range(r)]

def snake(r, c):
    # one long path: the laser of row 1 sweeps the grid row by row
    g = [["."] * c for _ in range(r)]
    for i in range(0, r - 1, 2):
        g[i][c - 1] = "\\"
        g[i + 1][c - 1] = "/"
        if i + 2 < r:
            g[i + 1][0] = "/"
            g[i + 2][0] = "\\"
    return ["".join(row) for row in g]

# samples
add([".\\.", "...", "./."])
add(["\\.\\", "./.", "\\.\\", "..."])
add(["/"])
add(["./\\", "\\/."])
add(["....", "../.", "/\\.."])
# hidden
add(["."])
add(["\\"])
add(rnd(1, 500, 0.3))
add(rnd(500, 1, 0.3))
add(rnd(6, 7, 0.4))
add(rnd(12, 10, 0.3))
add(rnd(500, 500, 0.05))
add(rnd(500, 500, 0.5))
add(rnd(500, 500, 1.0))
add(rnd(499, 500, 0.002))
add(snake(500, 500))
add(snake(7, 9))
add(rnd(50, 300, 0.2))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
