# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(1103)
V = 10**9
tests = []

def add(a):
    n = len(a)
    assert 1 <= n <= 100_000
    assert all(1 <= x <= V for x in a)
    tests.append(f"{n}\n" + " ".join(map(str, a)) + "\n")

def ri(lo, hi, n):
    return [random.randint(lo, hi) for _ in range(n)]

# samples
add([19, 4, 31, 100, 22, 13])
add([7, 70, 7, 16, 25])
add([1000000000])
add([9, 10, 99, 100])
add([5, 50, 41, 999999999, 123, 321, 8])
# hidden
add([1, 1])
add([999999999, 899999999, 1000000000, 1, 10, 100000000, 999999998])
add(ri(1, 100, 50))
add(ri(1, 10**4, 300))
add(ri(1, V, 2000))
add(ri(1, 1000, 3000))
# all with the same digit sum (permutations of digits), many ties broken by value
pool = [int("".join(random.sample("1234567", 7))) for _ in range(2000)]
add(pool)
add(ri(1, V, 100_000))
add(ri(1, 1000, 100_000))
add([7] * 100_000)
# numbers with digit sum 1 or 2 only: powers of ten and their sums
small = [10**i for i in range(10)] + [10**i + 10**j for i in range(9) for j in range(9)] + [2 * 10**i for i in range(9)]
add([random.choice(small) for _ in range(60_000)])
add(sorted(ri(1, V, 30_000)))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
