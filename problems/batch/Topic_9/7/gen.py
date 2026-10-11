# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random
from math import gcd

random.seed(907)
MAXN = 100_000
tests = []

def answer(f):
    n = len(f)
    if sorted(f) != list(range(1, n + 1)):
        return -1
    seen = [False] * (n + 1)
    l = 1
    for i in range(1, n + 1):
        if not seen[i]:
            c, x = 0, i
            while not seen[x]:
                seen[x] = True; x = f[x - 1]; c += 1
            l = l // gcd(l, c) * c
    return l

def add(f):
    n = len(f)
    assert 1 <= n <= MAXN and all(1 <= v <= n for v in f)
    assert answer(f) <= 10**18
    tests.append(f"{n}\n" + " ".join(map(str, f)) + "\n")

def from_cycles(lengths, n=None, shuffle=True):
    total = sum(lengths)
    if n is None:
        n = total
    lengths = lengths + [1] * (n - total)
    labels = list(range(1, n + 1))
    if shuffle:
        random.shuffle(labels)
    f = [0] * n
    p = 0
    for L in lengths:
        cyc = labels[p:p + L]
        for j in range(L):
            f[cyc[j] - 1] = cyc[(j + 1) % L]
        p += L
    return f

# samples
add([2, 3, 1])
add([2, 2])
add([1, 2, 3, 4])
add([2, 1, 4, 5, 3])
add([3, 1, 2, 3])
add([2, 3, 4, 1, 6, 7, 8, 9, 10, 5])
# hidden
add([1])
add(list(range(1, MAXN + 1)))                       # identity
add([i % MAXN + 1 for i in range(1, MAXN + 1)])      # one big cycle
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
add(from_cycles(primes, 20_000))                       # lcm = 47# ~ 6.1e17
add(from_cycles([2] * 15_000))                        # product of lengths overflows, lcm = 2
add(from_cycles([6, 10, 15] * 500, 20_000))          # lcm 30
add(from_cycles([64, 27, 25, 49, 11, 13, 17, 19, 23, 29, 31, 37], 20_000))
f = from_cycles(primes, 20_000); f[-1] = f[0]             # not a bijection, found only at the end
add(f)
f = list(range(1, MAXN + 1)); f[0] = 2                  # 1 -> 2 -> 2
add(f)
add(from_cycles([3, 4, 5]))
add(from_cycles([7, 9, 4, 5]))
add(from_cycles([random.randint(1, 6) for _ in range(5)]))
add([random.randint(1, 8) for _ in range(8)])
add(from_cycles([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
