# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(508)
tests = []

def add(L, segs):
    m = len(segs)
    assert 1 <= L <= 1_000_000 and 1 <= m <= 100_000
    assert all(1 <= l <= r <= L for l, r in segs)
    tests.append(f"{L} {m}\n" + "".join(f"{l} {r}\n" for l, r in segs))

def rseg(L, maxlen):
    ln = random.randint(1, min(L, maxlen))
    l = random.randint(1, L - ln + 1)
    return (l, l + ln - 1)

# samples
add(10, [(1, 4), (3, 6), (5, 10)])
add(5, [(2, 4)])
add(8, [(1, 8), (2, 3), (6, 7)])
add(12, [(1, 3), (5, 6), (9, 12)])
add(9, [(1, 5), (4, 9), (2, 7), (8, 9)])
# hidden
add(1, [(1, 1), (1, 1)])
add(1_000_000, [(1, 1_000_000)])
add(20, [(1, 10), (11, 20), (5, 15)])            # middle one fully covered
add(20, [(1, 2), (3, 20), (5, 15)])
add(15, [(1, 2), (4, 10), (4, 10), (12, 15)])     # duplicates: firing one loses nothing
add(30, [rseg(30, 8) for _ in range(6)])
add(100, [rseg(100, 30) for _ in range(20)])
add(500, [rseg(500, 50) for _ in range(60)])
add(3000, [rseg(3000, 400) for _ in range(300)])
# max L, max M: short segments, firing someone always loses something
segs = [(10 * i + 1, 10 * i + 10) for i in range(100_000)]
random.shuffle(segs)
segs[12_345] = (999_991, 1_000_000)
add(1_000_000, segs)
# max: random long segments
add(1_000_000, [rseg(1_000_000, 300_000) for _ in range(50_000)])
# max: the shortest segment is not the right choice
segs = []
for i in range(15_000):
    segs.append((30 * i + 1, 30 * i + 3))
    segs.append((30 * i + 4, 30 * i + 30))
segs.append((30 * 9_000 + 4, 30 * 9_000 + 30))  # one duplicate long segment
random.shuffle(segs)
add(450_000, segs)
add(1_000_000, [rseg(1_000_000, 50) for _ in range(20_000)])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
