# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(1104)
V = 10**9
tests = []

def add(k, s):
    n = len(s)
    assert 1 <= k <= n <= 100_000
    assert all(0 <= x <= V for x in s)
    tests.append(f"{n} {k}\n" + " ".join(map(str, s)) + "\n")

def ri(lo, hi, n):
    return [random.randint(lo, hi) for _ in range(n)]

# samples
add(2, [70, 90, 85, 90, 70, 70])
add(4, [50, 80, 50, 80, 60])
add(4, [0, 100, 0, 55, 100, 0, 20])
add(1, [0])
add(1, [1000000000, 1000000000, 3, 1000000000])
add(3, [5, 5, 5])
# hidden
add(2, [7, 7])
add(2, [3, 9])
s = ri(0, 10, 40); add(len(set(s)), s)                          # smallest distinct value
s = ri(0, 10, 40); add(len(set(s)) + 1, s)                      # one too many
add(5, ri(0, 20, 60))
add(17, ri(0, 30, 200))
add(250, ri(0, 1000, 2000))
add(1, ri(0, V, 30_000))
s = random.sample(range(10**6), 100_000); add(100_000, s)        # all distinct, K = N
s = random.sample(range(100_000), 99_999); s.append(s[0]); random.shuffle(s); add(100_000, s)  # one duplicate -> '-'
add(2, [V] * 20_000)
add(1, [0] * 100_000)
s = ri(0, 100, 100_000); add(random.randint(50, 101), s)
s = ri(V - 5000, V, 40_000); add(3000, s)

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
