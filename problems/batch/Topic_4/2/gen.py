# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(402)
MAXV = 10**9
tests = []

def add(t, a):
    assert 1 <= len(a) <= 100_000
    assert 0 <= t <= MAXV and all(0 <= x <= MAXV for x in a)
    tests.append(f"{len(a)} {t}\n{' '.join(map(str, a))}\n")

# samples
add(5, [12, 6, 3])
add(9, [1, 9, 8])
add(0, [7, 1024, 8, 5])
add(1, [0])
add(1000000000, [1, 999999999])
add(15, [16, 31, 0, 14])
# hidden
add(0, [0])
add(MAXV, [MAXV])
add(MAXV, [0, 1, 2])
add(7, [8, 6, 5, 3])                 # tie: 3 5 6 all distance 1 -> 3
# big random
add(random.randint(0, MAXV), [random.randint(0, MAXV) for _ in range(100_000)])
add(random.randint(0, MAXV), [random.randint(0, MAXV) for _ in range(100_000)])
# big, many ties, best placed last and not first
t = 0b1010101010101010101010101010
a = [t ^ (1 << random.randint(0, 29)) ^ (1 << random.randint(0, 29)) ^ (1 << random.randint(0, 29)) for _ in range(99_998)]
a = [x for x in a if x <= MAXV][:99_990]
a += [t ^ (1 << 29), t ^ (1 << 3), t ^ (1 << 1)]
random.shuffle(a)
add(t, a)
# small powers of two vs T (different lengths)
add(1 << 29, [(1 << k) for k in range(30)][::-1])
add(536870911, [random.randint(0, 2000) for _ in range(50)])
for _ in range(3):
    add(random.randint(0, 100), [random.randint(0, 100) for _ in range(random.randint(1, 10))])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
