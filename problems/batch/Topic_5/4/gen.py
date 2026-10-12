# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(504)
MAXA = 10**9
tests = []

def add(a):
    n = len(a)
    assert 1 <= n <= 100_000
    assert all(0 <= x <= MAXA for x in a)
    tests.append(f"{n}\n" + " ".join(map(str, a)) + "\n")

def divisible(n, hi):
    # random list whose sum is divisible by n
    a = [random.randint(0, hi) for _ in range(n)]
    r = sum(a) % n
    i = 0
    while r:
        take = min(r, a[i])
        a[i] -= take
        r -= take
        i += 1
    return a

# samples
add([5, 1, 4, 6])
add([1, 2, 4])
add([7])
add([3, 3, 3, 3, 3])
add([0, 0, 0, 0, 0, 12])
add([0, 1_000_000_000])
# hidden
add([0])
add([0, 1])
add([2, 0, 1])
add(divisible(8, 20))
add([random.randint(0, 9) for _ in range(9)])
add(divisible(50, 100))
add(divisible(1000, 1000))
# max: half zero, half 10^9 (answer 2.5 * 10^13)
add([0] * 50_000 + [MAXA] * 50_000)
# max: one rich child
add([0] * 99_999 + [99_999 * 10_000])
add([7] * 100_000)
# max: sum not divisible
a = [random.randint(0, MAXA) for _ in range(100_000)]
if sum(a) % len(a) == 0:
    a[0] += 1 if a[0] < MAXA else -1
add(a)
add(divisible(99_991, 1000))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
