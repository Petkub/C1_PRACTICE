# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(515)
A = 100_000
tests = []

def add(s, a):
    n = len(a)
    assert 1 <= n <= 100_000 and 1 <= s <= 10**10
    assert all(1 <= x <= A for x in a)
    tests.append(f"{n} {s}\n" + " ".join(map(str, a)) + "\n")

def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]

# samples
add(15, [2, 7, 3, 1, 6, 9, 1, 4])
add(100, [10, 20, 30, 30])
add(5, [1, 5, 2, 5, 1])
add(6, [2, 2, 2])
add(10, [4, 6, 1, 9, 5, 5])
add(1, [1])
# hidden
add(2, [1])
add(10**10, [A])
add(3, [1, 1, 1])
add(50, rnd(10, 1, 20))
add(120, rnd(40, 1, 20))
a = rnd(300, 1, 1000)
add(sum(a) - 5, a)
a = rnd(2000, 1, 100)
add(sum(a) + 1, a)                       # no segment
# max
a = [A] * 100_000
add(10**10, a)                           # whole array, sum = 10^10
a = rnd(100_000, 1, A)
add(sum(a) - random.randint(0, 50), a)   # long answer, sums above 2^31
a = rnd(100_000, 1, 10)
add(3_000, a)
a = rnd(100_000, 90_000, A)
add(4_000_000_000, a)                    # S above 2^31
a = rnd(100_000, 1, A)
add(sum(a) + 1, a)                       # no segment at max size
a = [1] * 100_000
a[77_777] = A
add(A, a)

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
