# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(608)
AL = "abcdefghijklmnopqrstuvwxyz"
tests = []

def add(g, t):
    n, m = len(g), len(g[0])
    assert 1 <= n <= 300 and 1 <= m <= 300 and 1 <= t <= 10**9
    assert all(len(row) == m and all(ch in AL for ch in row) for row in g)
    tests.append(f"{n} {m} {t}\n" + "".join(row + "\n" for row in g))

def rnd(n, m, al=AL):
    return ["".join(random.choice(al) for _ in range(m)) for _ in range(n)]

def seq(n, m):
    return ["".join(AL[(i * m + j) % 26] for j in range(m)) for i in range(n)]

# samples
add(seq(4, 4), 1)
add(["abc", "hxd", "gfe"], 10)
add(["abcde", "fghij"], 3)
add(["abcd"], 5)
add(seq(5, 6), 2)
# hidden (small T: brute simulates step by step)
add(["q"], 7)
add(["ab", "cd"], 1)
add(rnd(7, 1), 3)
add(rnd(6, 9), 5)
add(rnd(9, 7), 13)
add(rnd(10, 10), 36)
add(rnd(11, 12), 1)
add(rnd(3, 8), 18)
# hidden (big T)
add(rnd(300, 300), 10**9)
add(rnd(300, 299), 999999937)
add(rnd(1, 300), 10**9)
add(rnd(300, 2), 123456789)
add(seq(300, 300), 1196)          # 4 * 299 = ring 1 length: ring 1 returns home
add(rnd(150, 300), 987654321)

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
