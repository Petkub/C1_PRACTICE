# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(607)
tests = []

def add(g, s):
    n, m = len(g), len(g[0])
    assert 1 <= n <= 1000 and 1 <= m <= 1000 and 0 <= s <= 10**7
    assert all(len(row) == m and row.isdigit() for row in g)
    tests.append(f"{n} {m} {s}\n" + "".join(row + "\n" for row in g))

def rnd(n, m, digits="0123456789", weights=None):
    return ["".join(random.choices(digits, weights=weights, k=m)) for _ in range(n)]

# samples
add(["0103", "0201", "1004", "3120"], 5)
add(["345", "939"], 2)
add(["000", "000"], 0)
add(["5"], 5)
add(["90009", "00000", "00900", "00000", "90009"], 9)
# hidden
add(["7"], 6)
add(["9" * 1000 for _ in range(1000)], 10**7)                # whole field: 9e6 stones
add(["9" * 500 for _ in range(500)], 8)                     # nothing
add(rnd(600, 600, "0123456789", [30, 1, 1, 1, 1, 1, 1, 1, 1, 1]), 400)
add(rnd(600, 600, "01", [97, 3]), 0)
add(rnd(500, 600), 2000)
add(rnd(1, 1000), 30)
add(rnd(1000, 1), 9)
add(rnd(300, 800, "0123", [80, 10, 5, 5]), 150)
add(rnd(8, 9, "0123", [50, 20, 20, 10]), 6)
add(rnd(12, 7), 40)
add(rnd(20, 25, "019", [70, 20, 10]), 25)
add(rnd(30, 30, "0123456789"), 9)
g = rnd(500, 500, "9")
g = [list(r) for r in g]
for i in range(100, 400):                                     # one hidden clear block of side 300
    for j in range(150, 450):
        g[i][j] = "0"
add(["".join(r) for r in g], 0)

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
