# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(1109)
V = 10**9
tests = []

def add(W, w):
    n = len(w)
    assert 1 <= n <= 100_000
    assert 1 <= W <= V and all(1 <= x <= W for x in w)
    tests.append(f"{n} {W}\n" + " ".join(map(str, w)) + "\n")

def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]

# samples
add(100, [70, 50, 30, 80])
add(10, [10, 10, 10])
add(5, [5])
add(6, [1, 2, 3, 4, 5])
add(4, [2, 2, 2, 2])
add(20, [20, 1, 19, 2, 10, 10])
# hidden: small (checked by exhaustive search)
add(10, [1, 2, 8, 9])                         # neighbours after sorting pair badly
add(10, [5, 5, 5, 6, 6, 4])
add(V, [V, 1, 999999999, 2, 500000000, 500000000])
add(100, rnd(12, 1, 100))
add(50, rnd(14, 10, 40))
add(V, rnd(16, 1, V))
add(30, rnd(18, 1, 30))
# hidden: medium and large (medium checked by the O(N^2) brute)
add(1000, rnd(2000, 1, 1000))
add(V, rnd(100_000, 1, V))                                  # max N
add(V, [V] * 30_000)                                        # nobody can share
add(2, [1] * 99_999)                                        # odd count of light people
add(V, rnd(20_000, 1, V // 2 - 1) + rnd(10_000, V // 2 + 1, V))
add(999_999_999, rnd(30_000, 499_999_000, 500_001_000))     # pairs only just fit or not

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
