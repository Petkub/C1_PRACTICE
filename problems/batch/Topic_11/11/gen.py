# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(1111)
tests = []

def add(t):
    n = len(t)
    assert 1 <= n <= 100_000
    assert all(1 <= x <= 10_000 for x in t)
    tests.append(f"{n}\n" + " ".join(map(str, t)) + "\n")

# samples
add([5, 2, 3])
add([4, 1, 4, 1])
add([7])
add([3, 3, 3, 3, 3])
add([10, 3, 7, 3, 1, 10])
# hidden: small (brute tries every order)
add([10_000])
add([2, 1])
add([6, 6])
add([random.randint(1, 3) for _ in range(8)])
add([random.randint(1, 10_000) for _ in range(8)])
add([8, 7, 6, 5, 5, 4, 2, 2])
add([1, 1, 1, 1, 1, 1, 1, 1])
# medium
add([random.randint(1, 20) for _ in range(2000)])
add([random.randint(1, 10_000) for _ in range(1500)])
# max
add([10_000] * 100_000)
add([random.randint(1, 10_000) for _ in range(100_000)])
add([random.randint(1, 3) for _ in range(100_000)])
add(sorted([random.randint(1, 10_000) for _ in range(50_000)], reverse=True))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
