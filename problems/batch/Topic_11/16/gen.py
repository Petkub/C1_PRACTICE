# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(1116)
V = 10**9
INT64 = 2**63 - 1
tests = []

def add(x):
    n = len(x)
    assert 2 <= n <= 100_000
    assert all(0 <= v <= V for v in x)
    s = sorted(x)
    total = sum(v * (2 * j - n + 1) for j, v in enumerate(s))
    assert 0 <= total <= INT64
    tests.append(f"{n}\n" + " ".join(map(str, x)) + "\n")

# samples
add([1, 5, 3])
add([7, 7, 2, 7])
add([0, V])
add([10, 0, 40, 20, 30])
add([3, 3, 3, 3, 3, 3])
# hidden (small)
add([5, 5])
add([V, 0, V, 0, V])
add([random.randint(0, 20) for _ in range(30)])
add([random.randint(0, V) for _ in range(1000)])
add([random.randint(V - 100, V) for _ in range(3000)])
# large: the largest possible answer (half at each end, 2.5e18)
half = [0] * 50_000 + [V] * 50_000
random.shuffle(half)
add(half)
add([random.randint(0, V) for _ in range(100_000)])
add([random.randint(0, 1000) for _ in range(60_000)])
add([V - i * 10_000 for i in range(30_000)])                  # strictly decreasing
add([0] * 99_999 + [V])                                       # one far house
add([V] * 20_000)                                             # all at one spot
add([random.choice((0, 1, V - 1, V)) for _ in range(40_000)])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
