# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(612)
tests = []

def add(g):
    n, m = len(g), len(g[0])
    assert 1 <= n <= 1000 and 1 <= m <= 1000
    assert all(len(row) == m and set(row) <= set("#.") for row in g)
    tests.append(f"{n} {m}\n" + "".join(row + "\n" for row in g))

def rnd(n, m, q):
    return ["".join("#" if random.random() < q else "." for _ in range(m)) for _ in range(n)]

def with_plus(g, ci, cj, arm):
    g = [list(r) for r in g]
    g[ci][cj] = "#"
    for t in range(1, arm + 1):
        g[ci - t][cj] = g[ci + t][cj] = g[ci][cj - t] = g[ci][cj + t] = "#"
    return ["".join(r) for r in g]

# samples
add([".#..#.", "######", ".#..#.", "......", "....#."])
add(["...", "..."])
add(["...", ".#.", "..."])
add(["..#..", ".###.", "#####", ".###.", "..#.."])
add(["####", "####", "####"])
# hidden
add(["#"])
add(["."])
add(["#" * 1000])
add(["#"] * 1000)
add(["#" * 1000 for _ in range(1000)])
add(rnd(1000, 1000, 0.97))
add(rnd(7, 8, 0.7))
add(rnd(30, 20, 0.8))
add(rnd(200, 300, 0.9))
g = rnd(300, 300, 0.5)
g = with_plus(g, 100, 100, 60)
g = with_plus(g, 200, 220, 60)
g = with_plus(g, 150, 150, 59)
add(g)
# big '#' block whose plus arms are cut by single holes
g = [["#"] * 400 for _ in range(400)]
for k in range(0, 400, 37):
    g[k][(k * 7) % 400] = "."
add(["".join(r) for r in g])
add(["." * 999 + "#"] + ["." * 1000] * 2)
add(["#." * 50] * 100)

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
