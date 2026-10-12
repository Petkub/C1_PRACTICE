# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(505)
V = 10**9
tests = []

def add(a):
    n = len(a)
    assert 1 <= n <= 100_000
    assert all(-V <= x <= V for x in a)
    tests.append(f"{n}\n" + " ".join(map(str, a)) + "\n")

def blocks(n, maxb, base, step):
    # increasing blocks, each block shuffled: pivots appear at blocks of size 1
    a, v = [], base
    while len(a) < n:
        b = min(n - len(a), random.randint(1, maxb))
        part = [v + step * k for k in range(b)]
        random.shuffle(part)
        a += part
        v += step * b
    return a

# samples
add([2, 1, 4, 7, 5, 9])
add([3, 3])
add([-8])
add([5, 4, 3, 2, 1])
add([1, 2, 3, 4])
add([6, 1, 2, 3, 10, 7, 8, 12])
# hidden
add([1, 1, 1, 2])
add([2, 3, 3, 4])
add([V, -V])
add([-V, V])
add(blocks(20, 3, -10, 1))
add(blocks(300, 4, -V, 3))
add([random.randint(-5, 5) for _ in range(40)])
add(blocks(2000, 2, 0, 1))
add(list(range(1, 100_001)))                       # every position
add([7] * 100_000)                                  # none (equal values)
add(blocks(100_000, 3, 0, 1))
a = list(range(1, 100_001))
a[0], a[-1] = a[-1], a[0]
add(a)                                              # none
a = blocks(100_000, 2, -50_000, 1)
add(a)
a = [-V] + [random.randint(-V + 1, V - 1) for _ in range(30_000)] + [V]
add(a)                                              # exactly the two ends

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
