# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(3012)
MAXV = 1_000_000
tests = []

def add(a):
    assert 2 <= len(a) <= 100_000
    assert all(1 <= v <= MAXV for v in a)
    tests.append(f"{len(a)}\n" + " ".join(map(str, a)) + "\n")

def primes_upto(n):
    s = bytearray([1]) * (n + 1)
    s[0] = s[1] = 0
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i in range(n + 1) if s[i]]

P = primes_upto(MAXV)

# samples
add([8, 12, 20, 9, 7])
add([5, 5, 5, 1])
add([1, 1])
add([7, 11, 13, 17, 19, 23])
add([1000000, 500000, 999999, 333333, 2])
add([6, 10, 15])
# hidden
add([1, 1000000])
add([1000000, 1000000])
add([MAXV] * 100_000)                       # 4999950000 pairs
add([1] * 100_000)
add(random.sample(P[-30000:], 30000) + [1] * 20000)   # every pair has gcd 1
add([random.randint(1, 50) for _ in range(2000)])
add([random.randint(1, 3000) for _ in range(3000)])
add([random.randint(1, MAXV) for _ in range(2500)])
add([random.randint(1, MAXV) for _ in range(100_000)])
add([p for p in P if p > 500_000][:40000] + [999_983])    # distinct large primes plus 999983 twice
add([2 * p for p in random.sample(P[1000:40000], 2000)] + [3, 9])             # answer 3, not 2
add([999_983, 499_979 * 2, 499_979])
add([random.randint(1, 1000) * 997 for _ in range(1000)])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
