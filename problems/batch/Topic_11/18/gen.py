# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(1118)
V = 10**9
tests = []

def add(a):
    n = len(a)
    assert 1 <= n <= 100_000
    assert all(-V <= x <= V for x in a) and len(set(a)) == n
    tests.append(f"{n}\n" + " ".join(map(str, a)) + "\n")

def distinct(n, lo=-V, hi=V):
    return random.sample(range(lo, hi + 1), n)

def one_cycle(vals):
    """arrange sorted vals so that all of them form a single cycle"""
    s = sorted(vals)
    n = len(s)
    order = list(range(n))
    random.shuffle(order)
    a = [0] * n
    for k in range(n):
        a[order[k]] = s[order[(k + 1) % n]]
    return a

def few_wrong(n, k):
    """sorted, then k random swaps"""
    a = sorted(distinct(n))
    for _ in range(k):
        i, j = random.randrange(n), random.randrange(n)
        a[i], a[j] = a[j], a[i]
    return a

# samples
add([40, 10, 30, 20])
add([-5, 0, 7])
add([42])
add([6, 5, 4, 3, 2, 1])
add([20, -4, 7, 13, 0, 100, -50])
add([V, -V])
# hidden (small: BFS)
add([2, 3, 4, 5, 6, 7, 8, 1])
add([2, 1, 4, 3, 6, 5, 8, 7])
add(one_cycle(distinct(8, -20, 20)))
add(distinct(7, -V, V))
add(distinct(8, -10, 10))
# medium (selection sort)
add(distinct(3000))
add(few_wrong(5000, 40))
# large
add(distinct(100_000))
add(list(range(-15_000, 15_000)))                              # already sorted
add(one_cycle(range(-49_999, 50_001)))                         # one cycle: n - 1
add(list(range(25_000, -25_000, -1)))                          # reversed: n / 2
pairs = list(range(1, 60_001))
for i in range(0, 60_000, 2):
    pairs[i], pairs[i + 1] = pairs[i + 1], pairs[i]
add(pairs)                                                     # adjacent pairs swapped
add(few_wrong(30_000, 1000))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
