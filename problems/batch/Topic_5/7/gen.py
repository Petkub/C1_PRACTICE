# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(507)
M = 10**9
tests = []

def add(a):
    n = len(a)
    assert 1 <= n <= 100_000
    assert all(-M <= x <= M for x in a)
    tests.append(f"{n}\n" + " ".join(map(str, a)) + "\n")

def sorted_rand(n, lo, hi):
    return sorted(random.randint(lo, hi) for _ in range(n))

def one_swap(a):
    # swap two positions holding different values
    a = a[:]
    while True:
        i, j = random.sample(range(len(a)), 2)
        if a[i] != a[j]:
            a[i], a[j] = a[j], a[i]
            return a

def two_swaps(a):
    return one_swap(one_swap(a))

# samples
add([1, 5, 3, 4, 2])
add([3, 1, 2, 4])
add([1, 2, 2])
add([5, 3])
add([2, 2, 1, 1])
add([1, 3, 2, 2, 4])
# hidden
add([42])
add([7, 7, 7, 7])
add([M, -M])
add([1, 2, 3, 5, 4])                              # adjacent swap at the end
add([2, 3, 1])                                    # 3-cycle
add([1, 1, 3, 2, 2, 2, 4])                        # duplicates: swap 3 and 6
add(one_swap(sorted_rand(12, 1, 4)))
add(one_swap(sorted_rand(200, -50, 50)))
add(two_swaps(sorted_rand(200, -1000, 1000)))
# max
add(sorted_rand(100_000, -M, M))
add(one_swap(sorted_rand(100_000, 1, 3)))
add(two_swaps(sorted_rand(100_000, 1, 1000)))
a = list(range(1, 100_001))
a[0], a[-1] = a[-1], a[0]
add(a)
b = list(range(1, 100_001))
b[50_000], b[50_001], b[50_002] = b[50_001], b[50_002], b[50_000]   # 3-cycle: NO
add(b)

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
