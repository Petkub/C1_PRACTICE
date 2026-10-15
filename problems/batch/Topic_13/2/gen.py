# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(1302)
MAXN = 200_000
V = 10**9
tests = []


def add(a):
    assert 1 <= len(a) <= MAXN
    assert all(1 <= x <= V for x in a)
    tests.append(f"{len(a)}\n" + " ".join(map(str, a)) + "\n")


def distinct(n, lo, hi):
    s = set()
    while len(s) < n:
        s.add(random.randint(lo, hi))
    s = list(s)
    random.shuffle(s)
    return s


# samples
add([5, 3, 7, 3, 5, 9])
add([10, 20, 30, 40])
add([V, V - 1, V])
add([7])
add([9, 8, 7, 6, 5, 4, 3, 9])
# hidden (small)
add([1, 2, 1, 2])
add([4, 1, 2, 2, 4])                       # a later number started first
add(distinct(30, 1, 40) + [random.randint(1, 40) for _ in range(10)])
add([random.randint(1, 1000) for _ in range(60)])
add(distinct(2000, 1, V))                  # no repeat, large values
a = distinct(3000, 1, V)
add(a + [a[0]])                            # repeat only at the very end
a = distinct(5000, V - 10_000, V)
a[4000] = a[17]
a[4500] = a[100]
add(a)
# large
a = list(range(1, MAXN + 1))
random.shuffle(a)
add(a)                                     # max N, no repeat
a = list(range(1, 130_000))
random.shuffle(a)
add(a + [a[60_000], a[3]])                 # first repeat near the end
a = distinct(15_000, 1, V)
add(a + [a[-1]])                           # large values, repeat at the end
a = distinct(10_000, 1, V)
a[7_000] = a[6_999]
add(a)

assert sum(len(t) for t in tests) < 2_950_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
