# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(1211)
MAXN, MAXS = 100_000, 10**9
tests = []

def add(s, d):
    n = len(s)
    assert 1 <= n <= MAXN and len(d) == n
    assert all(1 <= x <= MAXS for x in s) and set(d) <= set("LR")
    tests.append(f"{n}\n" + " ".join(map(str, s)) + f"\n{d}\n")

def rnd(n, lo, hi, pr=0.5):
    return [random.randint(lo, hi) for _ in range(n)], "".join("R" if random.random() < pr else "L" for _ in range(n))

# samples
add([4, 7, 5, 6, 2], "RRLLR")
add([5, 2, 5], "RRL")
add([3, 1, 1, 3], "LLRR")
add([9], "L")
add([8, 1, 2, 3, 9, 4], "RRRRLL")
add([3, 3, 2, 6, 1, 6, 4], "RLRRLLL")
# hidden (small)
add([5, 5], "RL")
add([1, 2], "RL")
add([2, 1], "RL")
add([7, 7, 7, 7, 7, 7], "RLRLRL")
add([1, 2, 3, 4, 5, 6], "LRLRLR")
add(*rnd(12, 1, 3))
add(*rnd(300, 1, 5))
add(*rnd(2000, 1, 100, 0.6))
# large
add(*rnd(MAXN, 1, MAXS))
add(*rnd(MAXN, 1, 30, 0.55))
# a tall run of R that one big L eats from right to left, then the rest
n = MAXN
add([random.randint(1, 9) for _ in range(n - 1)] + [10], "R" * (n - 1) + "L")
# equal sizes everywhere: pairs cancel, the unmatched remain
add([7] * n, "".join(random.choice("RRL") for _ in range(n)))
# small L meteors bounce off a few giant R meteors
s, d = [], ""
for i in range(n):
    if i % 1000 == 0:
        s.append(100); d += "R"
    else:
        s.append(random.randint(1, 99)); d += "L"
add(s, d)

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
