# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(1108)
V = 10**9
tests = []

def add(seg):
    n = len(seg)
    assert 1 <= n <= 100_000
    assert all(1 <= l <= r <= V for l, r in seg)
    tests.append(f"{n}\n" + "".join(f"{l} {r}\n" for l, r in seg))

def rseg(n, hi, maxlen):
    out = []
    for _ in range(n):
        l = random.randint(1, hi)
        r = min(hi, l + random.randint(0, maxlen))
        out.append((l, r))
    return out

# samples
add([(1, 3), (4, 6), (8, 10), (9, 9)])
add([(2, 5), (7, 8), (1, 10)])
add([(1, 1000000000)])
add([(5, 5), (5, 5)])
add([(10, 20), (1, 2), (3, 4), (30, 30), (22, 25)])
add([(1, 5), (2, 3), (6, 6), (8, 9)])
# hidden: small
add([(1, 1)])
add([(V, V), (1, 1), (V - 1, V - 1)])
add(rseg(8, 30, 4))
add(rseg(50, 300, 10))
add(rseg(300, 100_000, 400))
add(rseg(200, V, 10**7))                                     # big cells, merged by the slow brute
add([(1, V)] + rseg(299, V, 10**6))                          # one team covers everything
# hidden: large (input size kept < 3 MB)
add(rseg(100_000, 100_000, 3))                               # max N, dense
add(rseg(20_000, V, 20_000))                                 # many pieces, big total
seg = [(i, i) for i in range(1, 30_001)]
random.shuffle(seg)
add(seg)                                                     # single cells touching: one piece
seg = [(2 * i - 1, 2 * i - 1) for i in range(1, 30_001)]
random.shuffle(seg)
add(seg)                                                     # gaps of one cell: 30000 pieces
seg = [(i, V - i) for i in range(1, 5_001)] + [(V // 2 + k, V // 2 + k) for k in range(5_000)]
random.shuffle(seg)
add(seg)                                                     # nested
seg = []
x = 1
for _ in range(10_000):
    l = x + random.randint(0, 1)
    r = l + random.randint(0, 99_000)
    seg.append((l, min(V, r)))
    x = r + 1
random.shuffle(seg)
add(seg)                                                     # long chain of touching/one-gap segments

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
