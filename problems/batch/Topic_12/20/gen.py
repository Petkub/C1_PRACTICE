# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(1220)
V = 10**9
tests = []

def add(h):
    n = len(h)
    assert 1 <= n <= 200_000
    assert all(1 <= x <= V for x in h)
    tests.append(f"{n}\n" + " ".join(map(str, h)) + "\n")

def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]

# samples
add([2, 4, 1, 2, 5])
add([3, 3, 3, 3])
add([7])
add([1, V])
add([5, 1, 2, 3, 4, 5])
add([4, 2, 4, 1, 1, 4, 3])
# hidden (small)
add([V, V])
add([3, 1, 3, 1, 3, 1, 3])
add(rnd(8, 1, 3))
add(rnd(12, 1, 6))
add(rnd(60, 1, 4))
add(rnd(500, 1, V))
add(rnd(3000, 1, 30))
# large
add([7] * 200_000)                                         # every pair: about 2 * 10^10
add([1 + (200_000 - i) // 4000 for i in range(200_000)])   # falling in long equal steps
add(rnd(50_000, 1, V))
add(rnd(200_000, 1, 20))
add([1 + min(i, 199_999 - i) // 1000 for i in range(200_000)])   # up then down
add([(1 if i % 2 else 50) + random.randint(0, 1) for i in range(100_000)])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
