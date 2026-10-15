# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(1305)
MAXN = 100_000
V = 10**9
tests = []


def add(s, a):
    assert 2 <= len(a) <= MAXN
    assert all(-V <= x <= V for x in a)
    assert -2 * V <= s <= 2 * V
    tests.append(f"{len(a)} {s}\n" + " ".join(map(str, a)) + "\n")


# samples
add(10, [3, 7, 5, 5, 7])
add(0, [-2, 2, 0, 0, 9])
add(2, [1, 3])
add(0, [0, 0, 0, 0, 0, 0])
add(-2 * V, [-V, -V, -V])
# hidden (small)
add(2, [1, 1])
add(5, [1, 2, 3, 4, 5, 0, -1, 6])
add(4, [2, 2, 2, 2, 2, 2, 2, 1, 3])
add(random.randint(-10, 10), [random.randint(-6, 6) for _ in range(40)])
add(2 * V, [V] * 50 + [V - 1, 1, -V])
# S far from most amounts
add(2 * V, [-V, V, 0] * 300 + [V, 7, V])
add(-2 * V + 1, [-V, -V + 1, V, -V + 1] * 100)
add(random.randint(-100, 100), [random.randint(-100, 100) for _ in range(3000)])
a = [random.randint(-V, V) for _ in range(3000)]
add(a[5] + a[2000], a)
# large
add(14, [7] * MAXN)                       # every pair works
add(1, [random.randint(-3, 4) for _ in range(MAXN)])
a = [random.randint(-V, V) for _ in range(50_000)]
for _ in range(2000):                     # plant some pairs
    i, j = random.sample(range(len(a)), 2)
    if abs(123_456_789 - a[i]) <= V:
        a[j] = 123_456_789 - a[i]
add(123_456_789, a)
a = [random.randint(-V, V) for _ in range(80_000)]
add(0, a + [-x for x in random.sample(a, 20_000)])

assert sum(len(t) for t in tests) < 2_950_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
