# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(1004)
E = 10**18
tests = []

def seat(k, r, c):
    return (r - 1) * k + (c if r % 2 == 1 else k + 1 - c)

def add(k, qs):
    assert 1 <= k <= E and 1 <= len(qs) <= 100_000
    lines = []
    for q in qs:
        if q[0] == 1:
            assert len(q) == 2 and 1 <= q[1] <= E
        else:
            assert len(q) == 3 and q[1] >= 1 and 1 <= q[2] <= k and seat(k, q[1], q[2]) <= E
        lines.append(" ".join(map(str, q)))
    tests.append(f"{k} {len(qs)}\n" + "\n".join(lines) + "\n")

def rand_queries(k, cnt, maxn):
    qs = []
    for _ in range(cnt):
        n = random.randint(1, maxn)
        if random.random() < 0.5:
            qs.append((1, n))
        else:
            r = (n - 1) // k + 1
            c = random.randint(1, k)
            while seat(k, r, c) > maxn:
                c = random.randint(1, k)
            qs.append((2, r, c))
    return qs

# samples
add(4, [(1, 6), (1, 4), (1, 9), (2, 2, 1), (2, 3, 4)])
add(3, [(1, 6), (1, 7), (2, 2, 3)])
add(1, [(1, 5), (2, 6, 1)])
add(5, [(1, 10), (1, 11), (2, 4, 1)])
add(10**9, [(1, 2 * 10**9), (2, 3, 1)])
# hidden, small (checked by the brute)
add(2, [(1, n) for n in range(1, 21)] + [(2, r, c) for r in range(1, 11) for c in (1, 2)])
add(7, [(1, n) for n in range(1, 50)] + [(2, r, c) for r in range(1, 8) for c in range(1, 8)])
add(1, rand_queries(1, 500, 2000))
add(10, rand_queries(10, 2000, 5000))
add(97, rand_queries(97, 2000, 5000))
add(1000, rand_queries(1000, 1000, 5000))
# hidden, big
add(E, [(1, E), (1, 1), (2, 1, E), (2, 1, 1)])
h = E // 2
add(h, [(1, E), (1, h), (1, h + 1), (2, 2, 1), (2, 2, h), (2, 1, h), (1, 1)])
add(3, [(1, E), (1, E - 1), (1, E - 2), (1, E - 3), (2, 333333333333333333, 1),
        (2, 333333333333333333, 3), (2, 333333333333333334, 3)])
add(2, [(1, E), (1, E - 1), (2, E // 2, 1), (2, E // 2, 2), (2, 1, 2)])
add(10**9, rand_queries(10**9, 25_000, E))
add(999_999_999_989, rand_queries(999_999_999_989, 25_000, E))
kr = random.randint(E // 3, E)
add(kr, rand_queries(kr, 20_000, E))
add(1, rand_queries(1, 20_000, E))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
