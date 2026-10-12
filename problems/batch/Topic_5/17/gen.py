# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(507)
V = 10**9
tests = []

def add(h):
    n = len(h)
    assert 1 <= n <= 100_000
    assert all(1 <= x <= V for x in h) and len(set(h)) == n
    tests.append(f"{n}\n" + " ".join(map(str, h)) + "\n")

def distinct(n, hi):
    return random.sample(range(1, hi + 1), n)

def interleave(n, m, hi):
    # the m smallest values stay in order; the rest are placed randomly between them
    vals = sorted(distinct(n, hi))
    small, big = vals[:m], vals[m:]
    random.shuffle(big)
    slots = sorted(random.sample(range(n), m))
    out, si, bi = [], 0, 0
    for p in range(n):
        if si < m and p == slots[si]:
            out.append(small[si]); si += 1
        else:
            out.append(big[bi]); bi += 1
    return out

# samples
add([3, 1, 4, 2, 5])
add([10, 20, 30])
add([7])
add([5, 4, 3, 2, 1])
add([4, 1, 5, 2, 6, 3])
add([1000000000, 1])
# hidden (small: checked by BFS)
add([2, 3, 1])
add([1, 3, 2])
add([6, 1, 7, 2, 8, 3, 5, 4])
add([2, 1, 3, 4, 5, 6, 7, 8])
add(distinct(8, 20))
add(distinct(7, V))
add(interleave(8, 5, 100))
# large
add(list(range(1, 100_001)))                                       # 0
add(list(range(2, 100_001)) + [1])                                 # n - 1
add(interleave(100_000, 37_000, 1_000_000))
add(distinct(30_000, V))
add(interleave(50_000, 49_999, V))
add([i * 2 for i in range(1, 25_001)] + [i * 2 - 1 for i in range(1, 25_001)])   # evens then odds

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
