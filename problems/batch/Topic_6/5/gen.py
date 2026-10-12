# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(605)
MOVES = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
tests = []

def add(g):
    n = len(g)
    assert 1 <= n <= 200
    assert all(len(row) == n for row in g)
    assert sorted(x for row in g for x in row) == list(range(1, n * n + 1))
    tests.append(f"{n}\n" + "".join(" ".join(map(str, row)) + "\n" for row in g))

def tour(n, si, sj):
    """Warnsdorff's rule with random tie-breaking; returns a grid or None."""
    g = [[0] * n for _ in range(n)]
    i, j = si, sj
    g[i][j] = 1

    def deg(a, b):
        return sum(1 for di, dj in MOVES
                   if 0 <= a + di < n and 0 <= b + dj < n and g[a + di][b + dj] == 0)

    for k in range(2, n * n + 1):
        cand = [(i + di, j + dj) for di, dj in MOVES
                if 0 <= i + di < n and 0 <= j + dj < n and g[i + di][j + dj] == 0]
        if not cand:
            return None
        random.shuffle(cand)
        c2 = (n - 1) / 2          # ties: prefer the cell farther from the centre
        i, j = min(cand, key=lambda p: (deg(*p), -abs(p[0] - c2) - abs(p[1] - c2)))
        g[i][j] = k
    return g

def find_tour(n, closed=None):
    while True:
        t = tour(n, random.randrange(n), random.randrange(n))
        if t is None:
            continue
        if closed is None or is_closed(t) == closed:
            return t

def pos(g):
    n = len(g)
    p = {}
    for i in range(n):
        for j in range(n):
            p[g[i][j]] = (i, j)
    return p

def is_closed(g):
    p = pos(g)
    (a, b), (c, d) = p[1], p[len(g) ** 2]
    return sorted((abs(a - c), abs(b - d))) == [1, 2]

def swap_values(g, x, y):
    g = [row[:] for row in g]
    p = pos(g)
    (a, b), (c, d) = p[x], p[y]
    g[a][b], g[c][d] = y, x
    return g

def row_major(n):
    return [[i * n + j + 1 for j in range(n)] for i in range(n)]

# samples
t5 = find_tour(5)
add(t5)
add(swap_values(t5, 7, 8))
add(find_tour(6, closed=True))
add([[1]])
add([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
add([[1, 4, 7], [6, 9, 2], [3, 8, 5]])            # 3x3: fails only at the centre
# hidden
add([[1, 2], [3, 4]])
add(find_tour(5))
add(find_tour(8, closed=True))
add(find_tour(8, closed=False))
add(find_tour(30))
t = find_tour(100)
add(t)
add(swap_values(t, 9999, 10000))                  # broken only at the very end
t = find_tour(200)
add(t)
add(swap_values(t, 1, 40000))
add(find_tour(199))
t = find_tour(150)
add(swap_values(t, 12000, 15000))
add(row_major(200))
t = find_tour(12, closed=True)
add(t)
add(swap_values(t, 1, 2))                         # broken at the very start

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
