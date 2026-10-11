# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(804)
tests = []

def is_leap(y, A, B):
    return y % A == 0 and y % B != 0

def mlen(L, A, B, mo, y):
    return L[mo - 1] + (1 if mo == len(L) and is_leap(y, A, B) else 0)

def key(dt):
    d, m, y = dt
    return (y, m, d)

def add(L, A, B, qs):
    M = len(L)
    assert 1 <= M <= 100 and all(1 <= l <= 100 for l in L)
    assert 1 <= A <= B <= 10**9 and B % A == 0
    assert 1 <= len(qs) <= 10**4
    lines = [f"{M} {A} {B}", " ".join(map(str, L)), str(len(qs))]
    for a, b in qs:
        for d, m, y in (a, b):
            assert 1 <= y <= 10**9 and 1 <= m <= M and 1 <= d <= mlen(L, A, B, m, y)
        assert key(a) <= key(b)
        lines.append(" ".join(map(str, a + b)))
    tests.append("\n".join(lines) + "\n")

def rdate(L, A, B, ylo, yhi):
    y = random.randint(ylo, yhi)
    m = random.randint(1, len(L))
    d = random.randint(1, mlen(L, A, B, m, y))
    return (d, m, y)

def rq(L, A, B, ylo, yhi, gap):
    a = rdate(L, A, B, ylo, yhi)
    b = rdate(L, A, B, a[2], min(10**9, a[2] + gap))
    if key(b) < key(a):
        a, b = b, a
    return (a, b)

def leapday(L, A, B, y):     # last day of a leap year y
    return (L[-1] + 1, len(L), y)

# samples
add([10, 20, 30], 4, 100, [((30, 3, 4), (1, 1, 5)), ((1, 1, 1), (1, 1, 2)), ((5, 2, 7), (5, 2, 7))])
add([7], 3, 6, [((1, 1, 1), (1, 1, 11)), ((7, 1, 3), (8, 1, 3)), ((8, 1, 9), (1, 1, 10))])
add([5, 5], 2, 2, [((5, 2, 1), (1, 1, 2)), ((1, 1, 1), (5, 2, 10))])
add([31, 28], 4, 100, [((28, 2, 1900), (1, 1, 1901)), ((28, 2, 1904), (1, 1, 1905))])
add([100], 1, 10**9, [((1, 1, 999999998), (101, 1, 999999999)), ((1, 1, 1), (100, 1, 10**9))])
add([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31], 4, 100,
    [((1, 1, 2000), (1, 1, 2001)), ((1, 1, 2100), (1, 1, 2101)), ((25, 12, 1999), (2, 1, 2000))])
# hidden: brute walks month by month, so these keep dates close
Lg = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
add(Lg, 4, 100, [rq(Lg, 4, 100, 1, 3000, 20) for _ in range(300)])
add([1], 1, 2, [rq([1], 1, 2, 1, 10**9, 1000) for _ in range(300)])
L3 = [random.randint(1, 100) for _ in range(100)]
add(L3, 7, 49, [rq(L3, 7, 49, 10**9 - 5000, 10**9, 30) for _ in range(300)])
add(L3, 7, 49, [(leapday(L3, 7, 49, 7 * k), (1, 1, 7 * k + 1)) for k in range(1, 200) if (7 * k) % 49] [:150])
add([1, 1], 10**9, 10**9, [((1, 1, 1), (1, 2, 10**9)), ((1, 2, 10**9), (1, 2, 10**9))])
add([2, 3], 1, 10**9, [((1, 1, 999999999), (3, 2, 10**9)), ((4, 2, 999999999), (1, 1, 10**9))])
# big (brute too slow)
L4 = [100] * 100
add(L4, 1, 10**9, [((1, 1, 1), (100, 100, 10**9))] + [rq(L4, 1, 10**9, 1, 10**9, 10**9) for _ in range(9999)])
L5 = [random.randint(1, 100) for _ in range(37)]
add(L5, 3, 300, [rq(L5, 3, 300, 1, 10**9, 10**9) for _ in range(10**4)])
add(Lg, 4, 100, [rq(Lg, 4, 100, 1, 10**9, 10**6) for _ in range(10**4)])
add([13], 5, 5000, [((1, 1, 1), rdate([13], 5, 5000, 1, 10**9)) for _ in range(10**4)])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
