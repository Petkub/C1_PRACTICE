# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(1013)
LM = 2 * 10**9
WM = 10**9
tests = []

def add(qs):
    assert 1 <= len(qs) <= 100_000
    for l, w in qs:
        assert 3 <= l <= LM and 1 <= w <= WM
    tests.append(f"{len(qs)}\n" + "".join(f"{l} {w}\n" for l, w in qs))

def near_kink(lmax):
    # W close to the value where the wall limit starts to matter (around L/2)
    l = random.randint(3, lmax)
    w = max(1, min(WM, l // 2 + random.randint(-3, 3)))
    return (l, w)

# samples
add([(12, 100), (12, 4)])
add([(7, 10), (3, 1)])
add([(100, 30), (100, 50), (100, 49), (101, 51)])
add([(2000000000, 5), (1000000001, 1000000)])
add([(4, 1), (5, 1), (6, 1), (10, 3), (11, 5)])
# hidden, small (checked by the brute)
add([(l, w) for l in range(3, 201) for w in range(1, 201)])
add([(random.randint(3, 20000), random.randint(1, 20000)) for _ in range(300)])
add([near_kink(30000) for _ in range(300)])
add([(l, w) for l in range(9990, 10011) for w in range(4980, 5021)])
# hidden, big
add([(LM, WM), (LM, 1), (LM, WM - 1), (LM - 1, WM), (LM - 1, WM - 1), (LM - 2, WM), (3, WM), (4, WM), (LM, WM // 2),
     (LM, 3), (1_999_999_999, 999_999_999), (1_999_999_997, 1), (LM, 2), (LM - 3, WM)])
add([(random.randint(3, LM), random.randint(1, WM)) for _ in range(40_000)])
add([near_kink(LM) for _ in range(40_000)])
add([(random.randint(3, LM), random.randint(1, 1000)) for _ in range(20_000)])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
