# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(1106)
V = 10**9
tests = []

def add(a, b):
    n = len(a)
    assert 1 <= n <= 100_000 and len(b) == n
    assert all(1 <= x <= V for x in a + b)
    tests.append(f"{n}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, b)) + "\n")

def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]

# samples
add([160, 175, 150], [158, 149, 170])
add([100, 200, 300, 400], [390, 110, 290, 210])
add([5], [1000000000])
add([7, 7, 7, 7], [7, 7, 7, 7])
add([1, 2, 3], [10, 20, 30])
add([12, 40, 33, 8, 25, 19], [30, 9, 41, 22, 15, 36])
# hidden: small (checked by brute force)
add([1, 100], [99, 2])
add(rnd(5, 1, 20), rnd(5, 1, 20))
add(rnd(7, 1, 1000), rnd(7, 1, 1000))
add(rnd(8, 1, V), rnd(8, 1, V))
add([1, 2, 3, 4, 5, 6, 7, 8], [8, 7, 6, 5, 4, 3, 2, 1])
add([50, 50, 60, 60, 70, 70, 80, 80], [55, 55, 65, 65, 75, 75, 85, 45])
# hidden: large
add(rnd(1000, 1, 1000), rnd(1000, 1, 1000))
add(rnd(100_000, 1, 999_999), rnd(100_000, 1, 999_999))     # max N (input size kept < 3 MB)
add(rnd(30_000, 1, V), rnd(30_000, 1, V))
a = sorted(rnd(20_000, 1, V))
b = sorted(rnd(20_000, 1, V), reverse=True)
add(a, b)                                   # given in opposite orders
add([1] * 10_000, [V] * 10_000)             # 999999999
a = [random.randint(1, V - 3) for _ in range(5_000)]
b = [x + random.randint(0, 3) for x in a]
random.shuffle(b)
add(a, b)                                   # small answer after reordering

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
