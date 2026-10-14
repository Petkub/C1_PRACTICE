# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(1119)
V = 10**9
tests = []

def add(h):
    n = len(h)
    assert 3 <= n <= 100_000
    assert all(1 <= x <= V for x in h)
    tests.append(f"{n}\n" + " ".join(map(str, h)) + "\n")

def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]

# samples
add([1, 2, 3, 4])
add([5, 9, 6])
add([7, 7, 7, 7, 7])
add([10, 1, 8, 3, 6, 15])
add([1, 1, 1, 1, V])
add([3, 100, 4, 101, 5, 102, 6])
# hidden (small: every seating tried)
add([1, V, 1])
add([V, V, V])
add([1, 2, 4, 8, 16, 32, 64, 128, 256, 512])
add([5, 5, 6, 100, 101, 101, 200, 201, 202])
add(rnd(10, 1, 5))
add(rnd(9, 1, V))
add(rnd(8, 1, 30))
# large
add(rnd(100_000, 1, V))
add([V] * 50_000)
clust = rnd(40_000, 1, 1000) + rnd(40_000, 5 * 10**8, 5 * 10**8 + 1000) + [3 * 10**8] # a lone middle value
random.shuffle(clust)
add(clust)
add(rnd(100_000, 1, 100))
sq = [i * i for i in range(1, 30_001)]                                   # widest gap at the top
random.shuffle(sq)
add(sq)

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
