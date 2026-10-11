# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(306)
MAXN = 1_000_000
tests = []

def add(qs):
    assert 1 <= len(qs) <= 100_000
    assert all(1 <= n <= MAXN for n in qs)
    tests.append(f"{len(qs)}\n" + "".join(f"{n}\n" for n in qs))

# samples
add([1, 4, 5])
add([6])
add([2, 3, 10])
add([100, 1])
add([1000000])
# hidden
add([1])
add([2])
add([7, 8, 9, 11, 12, 13, 97, 128])
add(list(range(1, 501)))
add([random.randint(1, 3000) for _ in range(1000)])
add([3000, 2999, 2310, 2048, 1])
add([random.randint(1, 3000) for _ in range(100_000)])
add([MAXN] * 1000 + [999_983, 999_999, 1])
add([random.randint(1, MAXN) for _ in range(100_000)])
add([random.randint(MAXN - 1000, MAXN) for _ in range(100_000)])
add([random.choice([1, 2, MAXN]) for _ in range(50_000)])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
