# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(1208)
N_MAX = 200_000
tests = []

def add(h):
    n = len(h)
    assert 1 <= n <= N_MAX
    assert all(1 <= x <= 10**9 for x in h)
    tests.append(f"{n}\n" + " ".join(map(str, h)) + "\n")

def rnd(n, vmax):
    return [random.randint(1, vmax) for _ in range(n)]

# samples
add([3, 1, 4, 1, 5, 9, 2])
add([2, 2, 1, 2, 3])
add([10])
add([5, 4, 3, 2, 1])
add([1, 2, 3, 4, 5])
add([6, 2, 8, 3, 3, 7, 1, 9, 4, 9])
# hidden (small)
add([10**9, 10**9])
add([1, 10**9])
add(rnd(20, 5))
add(rnd(300, 10**9))
add(rnd(2000, 50))
add([random.choice([5, 4, 3]) for _ in range(1000)] + [6])
# large: a long run without a taller building makes a pair-by-pair search slow
add([9 - i * 9 // N_MAX for i in range(N_MAX)])                 # non-increasing 9..1, many equal
add([7] * (N_MAX - 1) + [8])                                    # equal heights, the last one is taller
add([N_MAX - i if i % 2 == 0 else 1 for i in range(N_MAX)])       # tall ones decreasing, ones in between
add(rnd(30_000, 10**9))
add(sorted(rnd(20_000, 10**9), reverse=True))
h = []                                                          # saw teeth: short rising runs, falling peaks
while len(h) < 50_000:
    top = 100_000 - len(h)
    h += [top - 5, top - 3, top]
add(h[:50_000])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
