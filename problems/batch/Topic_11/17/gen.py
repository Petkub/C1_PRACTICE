# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(1117)
V = 10**9
tests = []

def add(sh):
    n = len(sh)
    assert 1 <= n <= 100_000
    assert all(0 <= s < e <= V for s, e in sh)
    tests.append(f"{n}\n" + "".join(f"{s} {e}\n" for s, e in sh))

def rnd(n, hi, maxlen):
    out = []
    for _ in range(n):
        ln = random.randint(1, maxlen)
        s = random.randint(0, hi - ln)
        out.append((s, s + ln))
    return out

# samples
add([(0, 10), (10, 20), (5, 15), (20, 30)])
add([(0, 100), (10, 20), (30, 40), (50, 60)])
add([(7, 8)])
add([(5, 8), (5, 8), (5, 8)])
add([(1, 3), (2, 5), (4, 7), (3, 4), (6, 9), (8, 10), (9, 11)])
add([(0, 6), (5, 8), (7, 12)])
# hidden (small)
add([(0, V)])
add([(0, 1), (1, 2), (0, 2), (2, 3), (1, 3)])
add([(1, 10), (2, 3), (3, 4), (4, 5), (0, 2), (9, 12), (5, 9)])
add(rnd(15, 40, 10))
add(rnd(200, 1000, 50))
add(rnd(2000, 10**6, 3000))
add(rnd(3000, 200, 30))
# large
add(rnd(100_000, 2 * 10**6, 2000))
chain = [(i * 3, i * 3 + 3) for i in range(30_000)]                 # touching chain: all can be watched
random.shuffle(chain)
add(chain)
long_first = [(0, V)] + [(V - 2 * (i + 1), V - 2 * i - 1) for i in range(15_000)]   # one long show covers the rest
random.shuffle(long_first)
add(long_first)
traps = []                                                          # short show overlapping two touching ones
for i in range(6_000):
    b = i * 100_000
    traps += [(b, b + 60), (b + 50, b + 70), (b + 60, b + 100)]
random.shuffle(traps)
add(traps)
add(rnd(10_000, V, V // 10))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
