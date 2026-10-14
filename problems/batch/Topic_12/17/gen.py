# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(1217)
V = 10**9
tests = []

def add(h):
    n = len(h)
    assert 1 <= n <= 100_000
    assert all(1 <= x <= V for x in h)
    tests.append(f"{n}\n" + " ".join(map(str, h)) + "\n")

def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]

# samples
add([2, 1, 5, 6, 2, 3])
add([2, 4, 2, 4, 2, 4, 2])
add([V])
add([5, 4, 3, 2, 1])
add([V, V, V])
add([3, 1, 3, 3, 2, 3, 3, 1])
# hidden (small)
add([1])
add([1, V])
add(list(range(1, 11)))
add(rnd(8, 1, 3))
add(rnd(10, 1, V))
add(rnd(300, 1, 20))
add([7, 7, 7, 1, 7, 7, 7, 7, 1, 7, 7] * 20)
add(rnd(2000, 1, V))
# large
add(list(range(1, 100_001)))                                  # best is about 50 000 x 50 001
add([V] * 50_000)
add(rnd(60_000, 1, V))
add(rnd(100_000, 1, 1000))
add([1 + (i % 100) for i in range(100_000)][::-1])            # saw teeth with long equal levels
add([25_001 - abs(i - 25_000) for i in range(50_001)])      # one wide mountain

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
