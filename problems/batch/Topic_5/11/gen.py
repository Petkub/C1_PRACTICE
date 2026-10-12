# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(511)
M = 10**9
tests = []

def add(a):
    n = len(a)
    assert 1 <= n <= 100_000
    assert all(-M <= x <= M for x in a)
    tests.append(f"{n}\n" + " ".join(map(str, a)) + "\n")

def rnd(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(n)]

# samples
add([4, 6, 2, 6, 4, 4, 9])
add([5, -1, 5, -1, 3, 3])
add([8])
add([10, 9, 8, 7, 6])
add([1, 2, 2, 3, 3, 3, 2, 1])
# hidden
add([-M, M, -M])
add([0] * 10)
add([3, -3, 3, -3, 2])
add(rnd(10, -3, 3))
add(rnd(50, -10, 10))
add(rnd(300, 1, 40))
add(rnd(1000, -M, M))
# frequency 1, 2, ..., k of values given in a shuffled order
a = []
for v in range(1, 300):
    a += [1000 - 7 * v] * v
random.shuffle(a)
add(a[:40_000])
# max N
add(rnd(100_000, -50, 50))
add(rnd(100_000, -M, M))
b = rnd(50_000, -M, M)
b += random.sample(b, 30_000)          # many values with frequency 2
random.shuffle(b)
add(b)
add([7] * 100_000)
c = [random.choice([-1, 0, 1, 2, 3]) for _ in range(100_000)]
add(c)

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
