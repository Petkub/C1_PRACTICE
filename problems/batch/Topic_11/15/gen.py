# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(1515)
V = 10**9
tests = []

def add(g):
    n = len(g)
    assert 1 <= n <= 100_000
    assert all(1 <= a < b <= V for a, b in g)
    tests.append(f"{n}\n" + "".join(f"{a} {b}\n" for a, b in g))

def rg(n, lo, hi, maxlen):
    out = []
    for _ in range(n):
        a = random.randint(lo, hi - 1)
        b = random.randint(a + 1, min(hi, a + maxlen))
        out.append((a, b))
    return out

# samples
add([(1, 4), (2, 5), (4, 6)])
add([(1, 3), (3, 5), (3, 4)])
add([(V - 1, V)])
add([(7, 10)] * 4)
add([(10, 12), (11, 13), (1, 3), (2, 4)])
add([(1, V), (500, 501), (500, 600), (2, 3)])
# hidden: small day ranges (brute counts every night)
add([(1, 2)])
add([(i, i + 1) for i in range(1, 300)])                 # chain: check-out day = next check-in day
add([(i, i + 2) for i in range(200, 0, -1)])             # every night after the first has 2
add([(1, 100)] + [(j, j + 1) for j in range(99, 0, -1)])
add(rg(50, 1, 30, 10))
add(rg(1000, 1, 500, 50))
add(rg(2000, 1, 2000, 2000))
# max N with small day numbers (keeps the files small), then big day numbers
add(rg(100_000, 1, 99_999, 99_999))
add([(i, 100_001 - i) for i in range(1, 50_001)])       # nested: peak 50000 on the night of day 50000
add(rg(20_000, 1, V, V))
add(rg(10_000, 1, V, 1000))
add([(V - 1 - i, V) if i % 2 else (1, 2 + i) for i in range(10_000)])
add([(i, i + 1) for i in range(V - 10_000, V)])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
