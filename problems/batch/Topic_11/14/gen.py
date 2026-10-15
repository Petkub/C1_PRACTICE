# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(1414)
V = 10**9
tests = []

def add(a, b):
    n, m = len(a), len(b)
    assert 1 <= n <= 100_000 and 1 <= m <= 100_000
    assert all(1 <= x <= V for x in a) and all(1 <= x <= V for x in b)
    tests.append(f"{n} {m}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, b)) + "\n")

def rnd(k, lo, hi):
    return [random.randint(lo, hi) for _ in range(k)]

# samples
add([20, 5, 13], [9, 30, 17, 1])
add([10, 4], [7, 13, 1])
add([V], [1])
add([5, 8, 8], [8, 3])
add([50, 60, 70], [55, 65])
# hidden: small
add([1], [1])
add([1], [V])
add([100, 1], [50])                       # same distance on both sides, smallest a wins
add([30], [36, 24, 36, 24])               # same a, smaller b wins
add(rnd(10, 1, 100), rnd(10, 1, 100))
add(rnd(2000, 1, V), rnd(2000, 1, V))
add(rnd(1000, 1, 50) , rnd(1500, 51, 200))   # every a below every b
add(rnd(1500, 500, 600), rnd(800, 1, 499))    # every a above every b
# ties with even gaps: a = multiples of 10, b = odd multiples of 5
add([10 * random.randint(1, 10**8) for _ in range(2000)], [10 * random.randint(1, 10**8) + 5 for _ in range(2000)])
# max: both shops full (all-pairs is too slow); smaller values keep the files small
add(rnd(100_000, 1, 99_999), rnd(100_000, 1, 99_999))
add(rnd(30_000, 1, V), rnd(20_000, 1, V))
add([2 * random.randint(1, 5 * 10**8) for _ in range(15_000)], [2 * random.randint(1, 5 * 10**8) - 1 for _ in range(15_000)])
add([V] * 20_000, rnd(1000, 1, V // 2))
add(rnd(50_000, 1, 30_000), [random.choice([1, V]) for _ in range(1000)])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
