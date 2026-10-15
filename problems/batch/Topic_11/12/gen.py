# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(1212)
V = 10**9
tests = []

def add(rows, cmds):
    n, m, q = len(rows), len(rows[0]), len(cmds)
    assert 1 <= n <= 1000 and 1 <= m <= 10 and 1 <= q <= 10
    assert all(len(r) == m and all(-V <= x <= V for x in r) for r in rows)
    assert all(1 <= c <= m and d in "AD" for c, d in cmds)
    s = f"{n} {m}\n" + "".join(" ".join(map(str, r)) + "\n" for r in rows)
    s += f"{q}\n" + "".join(f"{c} {d}\n" for c, d in cmds)
    tests.append(s)

def table(n, m, lo, hi):
    return [[random.randint(lo, hi) for _ in range(m)] for _ in range(n)]

def cmds(q, m):
    return [(random.randint(1, m), random.choice("AD")) for _ in range(q)]

# samples
add([[3, 10], [1, 20], [3, 5], [2, 7]], [(1, "A")])
add([[1, 50, 7], [2, 40, 7], [1, 30, 8], [2, 20, 8]], [(1, "D"), (3, "A")])
add([[-5]], [(1, "D")])
add([[0, 1, 2], [0, 2, 1], [0, 1, 1]], [(2, "A")])
add([[-3, 4], [-1, -4]], [(1, "D")])
# hidden
add([[V, -V], [-V, V]], [(1, "A")])
add([[7, 7, 7]] * 1 + [[7, 7, 8], [7, 7, 7], [7, 6, 7]], [(1, "D"), (2, "D"), (3, "A")])
# every row has the same key: nothing may move
add([[5, i] for i in range(1, 11)], [(1, "D")] * 3 + [(1, "A")] * 3)
add(table(30, 3, 1, 3), cmds(10, 3))
add(table(200, 5, -2, 2), cmds(10, 5))
# many equal keys, descending sort after ascending (breaks reverse-of-ascending)
rows = [[random.randint(1, 4), i] for i in range(1, 1001)]
add(rows, [(1, "A"), (1, "D")])
add(table(1000, 10, 1, 5), cmds(10, 10))
add(table(1000, 10, -V, V), cmds(10, 10))
add([[random.choice([-V, 0, V]) for _ in range(10)] for _ in range(1000)], cmds(10, 10))
add(table(1000, 1, -3, 3), [(1, "D"), (1, "A"), (1, "D")])
add(table(999, 4, 0, 1), [(4, "A"), (3, "A"), (2, "A"), (1, "A")])
add([[i, -i] for i in range(1000, 0, -1)], [(2, "D"), (1, "D")])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
