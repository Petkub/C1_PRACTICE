# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(906)
MAXV = 10**9
tests = []

def add(sets):
    assert 1 <= len(sets) <= 50000
    assert sum(len(s) for s in sets) <= 100000
    for s in sets:
        assert len(set(s)) == len(s)
        for x in s:
            assert -MAXV <= x <= MAXV
    lines = [str(len(sets))] + [" ".join(map(str, [len(s)] + list(s))) for s in sets]
    tests.append("\n".join(lines) + "\n")

def rand_set(k, lo, hi):
    s = set()
    while len(s) < k:
        s.add(random.randint(lo, hi))
    s = list(s)
    random.shuffle(s)
    return s

# samples
add([[1, 2, 3], [2, 3, 4], [3, 5]])
add([[7, -1], [-1, 7]])
add([[]])
add([[1], [1], [1], [2]])
add([[5, 3, 9], [], [9, 10]])
add([[4, -2, 0]])
# hidden
add([[MAXV, -MAXV]])
add([[0]] * 50000)                                    # even count -> empty
add([[7]] * 9999)                                     # odd count -> {7}
big = rand_set(50000, -10**6, 10**6)
add([big] + [[x] for x in random.sample(big, 49999)])  # slow for the pairwise linear method
add([rand_set(80, -50, 50) for _ in range(500)])       # heavy overlaps
add([rand_set(random.randint(0, 5), -10, 10) for _ in range(30)])
add([rand_set(random.randint(0, 20), -30, 30) for _ in range(200)])
add([rand_set(2, -MAXV, MAXV) for _ in range(5000)] + [rand_set(2, -100, 100) for _ in range(5000)])
half = rand_set(15000, -MAXV, MAXV)
add([half, list(reversed(half))])                     # identical sets -> empty
add([list(range(1, 20001)), list(range(10001, 30001)), list(range(20001, 40001))])
add([rand_set(50, -1000, 1000) for _ in range(1000)])
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
