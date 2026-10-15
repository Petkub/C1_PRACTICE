# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(1309)
MAXN = 200_000
V = 10**9
tests = []


def add(a):
    assert 1 <= len(a) <= MAXN
    assert all(1 <= x <= V for x in a)
    tests.append(f"{len(a)}\n" + " ".join(map(str, a)) + "\n")


def distinct(n, lo=1, hi=V):
    s = set()
    while len(s) < n:
        s.add(random.randint(lo, hi))
    s = list(s)
    random.shuffle(s)
    return s


def rnd(n, kinds):
    return [random.choice(kinds) for _ in range(n)]


def shuffled(a):
    a = list(a)
    random.shuffle(a)
    return a


# samples
add([5, 2, 9, 2, 7, 5, 1, 9])
add([4, 8, 8, 4, 6])
add([7, 7, 7, 7])
add([V])
add([1, 2, 3, 4, 5])
add([3, V, 3, 5, V, 5, 6])
# hidden (small)
add([1, 2])
add([2, 2])
add(list(range(1, 37)) * 3)                                  # many longest, the first wins
add([1, 2, 3, 4, 2, 1] * 5 + [7, 8, 9, 10])
add(rnd(50, [1, 2, 3]))
add(rnd(300, distinct(40)))
add([x for k in range(1, 40) for x in shuffled(range(1, k + 1))])   # the longest is near the end
add(rnd(2000, distinct(200)))
# large
add(shuffled(range(1, 80_001)))                              # no repeat at all
add([random.randint(1, V) for _ in range(40_000)])           # big codes, a few repeats by chance
add(rnd(MAXN, [1, 2]))
add([V] * 5000 + [1])
p = distinct(1000, 1, 9999)
s = [x for _ in range(60) for x in shuffled(p)]
add(s + distinct(1500, 10_000, 99_999))                      # the longest only at the very end
add(rnd(100_000, list(range(1, 20_001))))
a = []
nxt = 100
while len(a) < 70_000:                                       # a code whose last time is already left of the block
    m = random.randint(1, 3000)
    a += [1, 2, 2, 1] + list(range(nxt, nxt + m))
    nxt += m
add(a[:70_000])

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
assert sum(len(t) for t in tests) < 3_000_000
print("total bytes", sum(len(t) for t in tests))
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
