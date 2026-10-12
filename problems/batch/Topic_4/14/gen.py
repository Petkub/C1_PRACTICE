# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(414)
MAXN, MAXA = 100_000, 10**9
tests = []

def add(a):
    assert 2 <= len(a) <= MAXN and all(0 <= x <= MAXA for x in a)
    tests.append(f"{len(a)}\n" + " ".join(map(str, a)) + "\n")

# samples
add([1, 2, 3])
add([12, 10, 6])
add([5, 5])
add([0, 1, 2, 3, 4, 5, 6, 7])
add([7, 7, 7, 7])
add([1000000000, 0, 0, 1])
# hidden, small (brute checks)
add([0, 0])
add([0, MAXA])
add([random.randint(0, 15) for _ in range(50)])
add([random.randint(0, MAXA) for _ in range(2000)])
add([random.choice([0, MAXA, 2**29, 2**30 - 1 - 2**29]) for _ in range(3000)])
# hidden, big
add([random.randint(0, MAXA) for _ in range(MAXN)])
add([2**29 - 1] * (MAXN // 2) + [2**29] * (MAXN // 2))           # largest answer
add([random.choice([0, 1]) for _ in range(MAXN)])
add([MAXA] * 10000)
add([random.randint(0, 1023) for _ in range(MAXN)])
add([random.randint(0, MAXA) for _ in range(10000)])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
