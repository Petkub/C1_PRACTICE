# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(619)
tests = []

def add(g):
    n, m = len(g), len(g[0])
    assert 1 <= n <= 500 and 1 <= m <= 500
    assert all(len(r) == m and set(r) <= set(".#") for r in g)
    tests.append(f"{n} {m}\n" + "".join(r + "\n" for r in g))

def rnd(n, m, q):
    return ["".join("#" if random.random() < q else "." for _ in range(m)) for _ in range(n)]

# samples
add(["...", ".#."])
add(["##", "##"])
add(["."])
add(["...", "...", "..."])
add(["..#..", ".....", "#...#", "..#.."])
# hidden
add(["#"])
add(["." * 500])
add(["."] * 500)
add(["." * 500 for _ in range(500)])                  # largest answer
add(rnd(500, 500, 0.001))
add(rnd(500, 500, 0.05))
add(rnd(500, 500, 0.5))
add(rnd(7, 9, 0.2))
add(rnd(20, 15, 0.1))
add(rnd(60, 80, 0.03))
add(rnd(150, 150, 0.01))
add(["." * 500 if i % 2 == 0 else "#" * 500 for i in range(500)])
add(["." * 499 + "#" for _ in range(499)] + ["#" * 500])
g = [["."] * 500 for _ in range(500)]
g[250][250] = "#"
add(["".join(r) for r in g])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
