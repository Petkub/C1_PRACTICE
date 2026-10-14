# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random, string

random.seed(1303)
MAXN = 100_000
tests = []


def add(rec):
    assert 1 <= len(rec) <= MAXN
    for name, sc in rec:
        assert 1 <= len(name) <= 20 and all(c in string.ascii_lowercase for c in name)
        assert 0 <= sc <= 100
    tests.append(f"{len(rec)}\n" + "".join(f"{a} {b}\n" for a, b in rec))


def word(lo, hi, letters=string.ascii_lowercase):
    return "".join(random.choice(letters) for _ in range(random.randint(lo, hi)))


def rnd(n, pool, lo=0, hi=100):
    return [(random.choice(pool), random.randint(lo, hi)) for _ in range(n)]


# samples
add([("ploy", 70), ("an", 55), ("ploy", 85), ("ann", 90), ("ploy", 60)])
add([("bo", 0), ("bo", 0), ("ant", 100), ("b", 30)])
add([("zz", 100)])
add([("mint", 40), ("min", 95), ("mint", 100), ("mi", 0), ("mint", 100)])
add([("tonkla", 0), ("aom", 73), ("tonkla", 99), ("tonkla", 12)])
# hidden (small)
add([("a", 0)])
add([("b", 5), ("a", 5), ("ab", 5), ("ba", 5), ("aa", 5), ("a", 6), ("b", 4)])
add(rnd(30, ["a", "aa", "aaa", "ab", "b"]))
add(rnd(200, [word(1, 3, "abc") for _ in range(40)]))
add(rnd(500, ["x" * k for k in range(1, 21)]))                # names that are prefixes of each other
add(rnd(2000, [word(1, 20) for _ in range(300)], 0, 3))
add([("zero", 0)] * 1000 + [("zeros", 0)] * 3)
# large
add(rnd(MAXN, [word(1, 4) for _ in range(60_000)]))           # many students
pool = ["k" * 15 + word(1, 5, "ab") for _ in range(40)]
add(rnd(50_000, pool))                                       # few students with long names
names = sorted({word(5, 5) for _ in range(30_000)}, reverse=True)
add([(s, random.randint(0, 100)) for s in names] + rnd(20_000, names))

assert sum(len(t) for t in tests) < 2_950_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
