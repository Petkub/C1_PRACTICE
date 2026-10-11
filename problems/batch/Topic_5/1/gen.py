# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(501)
tests = []

def add(shoes):
    n = len(shoes)
    assert 1 <= n <= 100_000
    for s, c in shoes:
        assert 1 <= s <= 1000 and c in "LR"
    tests.append(f"{n}\n" + "".join(f"{s} {c}\n" for s, c in shoes))

def rnd(n, lo, hi, pl=0.5):
    return [(random.randint(lo, hi), "L" if random.random() < pl else "R") for _ in range(n)]

# samples
add([(40, "L"), (42, "R"), (38, "R"), (40, "L"), (42, "L"), (40, "R")])
add([(7, "L"), (7, "R"), (7, "R"), (7, "L")])
add([(1000, "L")])
add([(5, "R"), (5, "R"), (3, "L"), (5, "L"), (3, "R"), (9, "L")])
add([(2, "L"), (1, "R"), (2, "R"), (1, "L"), (1, "L")])
# hidden
add([(1, "R")])
add([(3, "L"), (3, "L"), (3, "L")])
add([(10, "L"), (11, "R")])
add(rnd(20, 1, 5))
add(rnd(50, 1, 10, 0.7))
add(rnd(200, 1, 30))
# all paired, many sizes
sh = []
for s in range(1, 1001):
    k = random.randint(1, 3)
    sh += [(s, "L")] * k + [(s, "R")] * k
random.shuffle(sh)
add(sh)
add(rnd(100_000, 1, 1000))                     # max N, many leftovers
add([(1000, "L")] * 50_000 + [(1000, "R")] * 50_000)   # max pairs
add([(1, "L")] * 100_000)                      # no pairs
sh = [(s, "L") for s in range(1, 1001)] + [(s, "R") for s in range(1, 1001) if s != 500]
random.shuffle(sh)
add(sh)                                        # exactly one leftover size
add(rnd(5000, 990, 1000, 0.3))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
