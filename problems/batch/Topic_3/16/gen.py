# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(3116)
MAXN = 3_000_000
tests = []

def add(ns):
    assert 1 <= len(ns) <= 100_000
    assert all(1 <= n <= MAXN for n in ns)
    tests.append(f"{len(ns)}\n" + "".join(f"{n}\n" for n in ns))

def primes_upto(n):
    s = bytearray([1]) * (n + 1)
    s[0] = s[1] = 0
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i in range(n + 1) if s[i]]

P = primes_upto(MAXN)

# samples
add([4, 6, 1])
add([29, 30])
add([7, 8, 9, 10])
add([28, 31, 32, 40])
add([MAXN])
# hidden
add([1])
add(list(range(1, 101)))
add([2**21, 2**21 - 1, 3**13, 3**13 - 1, 1361**2, 1361**2 - 1])   # prime powers and their predecessors
add([P[-1], P[-1] - 1, MAXN - 1])
add([random.randint(1, 200) for _ in range(300)])
add([random.randint(1, 3000) for _ in range(50)])
add([random.randint(1, 20000) for _ in range(5)])
add([MAXN] * 100_000)                                 # one pass over all primes per query is too slow
add([random.randint(MAXN // 2, MAXN) for _ in range(100_000)])
add([random.randint(1, MAXN) for _ in range(60_000)])
add([random.choice(P[-2000:]) for _ in range(30_000)] + [p - 1 for p in random.sample(P[-60000:], 30_000)])
add([60_000, 65_536, 65_537, 59_049])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
