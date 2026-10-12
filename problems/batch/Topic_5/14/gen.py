# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(514)
tests = []

def add(c):
    n = len(c)
    assert 1 <= n <= 200_000
    assert all(x in (0, 1) for x in c)
    tests.append(f"{n}\n" + " ".join(map(str, c)) + "\n")

def rnd(n, p1=0.5):
    return [1 if random.random() < p1 else 0 for _ in range(n)]

# samples
add([1, 0, 1, 0, 0])
add([0, 1, 0, 1, 0, 1])
add([1, 1, 1, 1])
add([0])
add([1, 0, 0, 1, 1, 0, 0, 1])
add([0, 0, 1, 1, 1, 0, 0])
# hidden
add([1])
add([1, 0])
add([0, 1, 1, 0])
add(rnd(12))
add(rnd(16, 0.3))
add(rnd(16, 0.6))
add(rnd(300))
add(rnd(2000, 0.1))
# max
add([1] * 100_000 + [0] * 100_000)                 # already grouped
add([0, 1] * 100_000)                              # answer about 5 * 10^9
add([0] * 50_000 + [1] * 100_000 + [0] * 50_000)   # answer 10^10 / 2
add(rnd(200_000))
add(rnd(200_000, 0.02))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
