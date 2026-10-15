# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(1107)
V = 10**9
tests = []

def add(t):
    n = len(t)
    assert 1 <= n <= 100_000
    assert all(1 <= x <= V for x in t)
    tests.append(f"{n}\n" + " ".join(map(str, t)) + "\n")

def blocks(spec, dup_prob=0.0):
    """spec = list of (start, length); returns a shuffled list, some numbers repeated"""
    t = []
    for s, l in spec:
        for x in range(s, s + l):
            t.append(x)
            while random.random() < dup_prob:
                t.append(x)
    random.shuffle(t)
    return t

# samples
add([5, 3, 4, 10, 11, 12, 4, 20])
add([7, 7, 7, 8, 8])
add([1000000000])
add([9, 1, 5, 3, 7, 11])
add([100, 101, 52, 102, 103, 50, 51, 52, 51])
add([1000000000, 999999999, 999999998, 1])
# hidden: small (checked by brute force)
add([random.randint(1, 30) for _ in range(40)])
add([random.randint(1, 12) for _ in range(25)])
add([20, 21, 22, 22, 22, 22, 22, 22, 5, 6, 7, 8])      # repeats must not lengthen 20..22
add([1, 2, 3, 3, 4, 5, 6, 40, 41, 42, 43, 44, 45])     # repeat inside the longest run, tie: start 1
add([1, 3, 5, 7, 9, 11, 13, 15, 2])                    # gaps of exactly 2
add(blocks([(900, 6), (300, 6), (600, 5), (10, 6)], 0.3))
add([random.randint(1, 600) for _ in range(300)])
# hidden: large
add([random.randint(1, V) for _ in range(50_000)])                        # random, mostly isolated numbers
add(blocks([(1, 60_000)]) + [random.randint(1, 60_000) for _ in range(40_000)])
lens = [random.randint(1, 40) for _ in range(2000)]
lens[700] = 41
spec = []
s = 1000
for l in lens:
    spec.append((s, l))
    s += l + random.randint(2, 50_000)
spec.append((V - 40, 41))                                                  # ties with the earlier 41
add(blocks(spec, 0.15))
add(blocks([(V - 49_999, 50_000), (1, 49_999)]))                           # longest run ends at 10^9
t = blocks([(10, 30_000), (40_011, 30_000), (80_000, 29_999)])
t += [random.choice(t) for _ in range(100_000 - len(t))]
random.shuffle(t)
add(t)                                                                     # tie 10.. and 40011.., repeats

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
