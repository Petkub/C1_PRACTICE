# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(606)
AL = "abcdefghijklmnopqrstuvwxyz_"
tests = []

def spiral(r, c):
    seen = [[False] * c for _ in range(r)]
    order = []
    di, dj = [0, 1, 0, -1], [1, 0, -1, 0]
    i = j = d = 0
    for k in range(r * c):
        order.append((i, j))
        seen[i][j] = True
        if k == r * c - 1:
            break
        ni, nj = i + di[d], j + dj[d]
        if not (0 <= ni < r and 0 <= nj < c) or seen[ni][nj]:
            d = (d + 1) % 4
            ni, nj = i + di[d], j + dj[d]
        i, j = ni, nj
    return order

def add(r, c, plain):
    assert r >= 1 and c >= 1 and r * c <= 300000 and len(plain) == r * c
    assert all(ch in AL for ch in plain)
    enc = "".join(plain[i * c + j] for i, j in spiral(r, c))
    tests.append(f"{r} {c}\n{enc}\n")

def rnd(n):
    return "".join(random.choice(AL) for _ in range(n))

# samples
add(3, 4, "meet_at_noon")
add(1, 5, "hello")
add(4, 1, "abcd")
add(4, 4, "abcdefghijklmnop")
add(2, 3, "posn_c")
add(3, 5, "spiral_is_cool_")
# hidden
add(1, 1, "z")
add(2, 2, "abcd")
add(5, 3, rnd(15))
add(3, 7, rnd(21))
add(6, 6, rnd(36))
add(7, 2, rnd(14))
add(2, 9, rnd(18))
add(547, 548, rnd(547 * 548))
add(1, 300000, rnd(300000))
add(300000, 1, rnd(300000))
add(3, 100000, rnd(300000))
add(99999, 3, rnd(299997))
add(500, 600, "".join(AL[(i * 7 + i // 600) % 27] for i in range(300000)))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
