# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(1313)
V = 10**9
tests = []

def add(a):
    n = len(a)
    assert 1 <= n <= 100_000
    assert all(-V <= x <= V for x in a)
    tests.append(f"{n}\n" + " ".join(map(str, a)) + "\n")

# samples
add([70, 85, 70, 60, 85])
add([-3, 7, -10, -3])
add([0])
add([5, 5, 5, 5, 5, 5])
add([9, 8, 7, 6, 5, 4])
add([3, 1, 4, 1, 5, 9, 2])
# hidden: small (brute is O(N^2))
add([-V])
add([V, -V])
add([random.randint(-5, 5) for _ in range(50)])
add([random.randint(-V, V) for _ in range(3000)])
add([random.choice([-V, -1, 0, 1, V]) for _ in range(3000)])
# max
add([random.randint(-V, V) for _ in range(100_000)])
add(random.sample(range(-50_000, 50_000), 100_000))          # all distinct: levels up to 100000
add([7] * 100_000)
add([random.randint(-20, 20) * 50_000_000 for _ in range(30_000)])
add(sorted([random.randint(-V, V) for _ in range(20_000)], reverse=True))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
