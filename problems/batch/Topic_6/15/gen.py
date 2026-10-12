# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(615)
tests = []

def add(n, m, folds, punch):
    assert 1 <= n <= 300 and 1 <= m <= 300 and 0 <= len(folds) <= 600
    h, w = n, m
    for t, k in folds:
        assert t in "LRUD" and k >= 1
        if t in "LR":
            assert 2 * k <= w
            w -= k
        else:
            assert 2 * k <= h
            h -= k
    assert len(punch) == h and all(len(r) == w and set(r) <= set("o.") for r in punch)
    tests.append(f"{n} {m} {len(folds)}\n" + "".join(f"{t} {k}\n" for t, k in folds)
                 + "".join(r + "\n" for r in punch))

def rfolds(n, m, cnt, small=False):
    h, w, res = n, m, []
    for _ in range(cnt):
        opts = [t for t in "LRUD" if (w >= 2 if t in "LR" else h >= 2)]
        if not opts:
            break
        t = random.choice(opts)
        lim = (w if t in "LR" else h) // 2
        k = random.randint(1, min(lim, 3)) if small else random.randint(1, lim)
        res.append((t, k))
        if t in "LR":
            w -= k
        else:
            h -= k
    return res, h, w

def rpunch(h, w, q):
    return ["".join("o" if random.random() < q else "." for _ in range(w)) for _ in range(h)]

def rand_test(n, m, cnt, q, small=False):
    folds, h, w = rfolds(n, m, cnt, small)
    add(n, m, folds, rpunch(h, w, q))

# samples
add(3, 6, [("L", 2), ("R", 1)], ["o..", "...", ".o."])
add(4, 3, [("U", 1), ("D", 1)], ["...", "o.o"])
add(2, 2, [], ["o.", ".o"])
add(2, 2, [("L", 1), ("U", 1)], ["o"])
add(2, 5, [("R", 2)], ["o..", "..o"])
# hidden
add(4, 4, [("L", 2), ("U", 2), ("R", 1), ("D", 1)], ["o"])
add(5, 4, [("D", 2), ("L", 1), ("U", 1)], ["o..", "..o"])
add(1, 1, [], ["."])
add(1, 1, [], ["o"])
add(1, 300, [("L", 150), ("R", 75), ("L", 37), ("R", 19)], ["o" + "." * 17 + "o"])
add(300, 1, [("U", 1)] * 299, ["o"])
rand_test(300, 300, 8, 0.05)
rand_test(300, 300, 40, 0.3, small=True)
rand_test(299, 297, 600, 0.5, small=True)
rand_test(8, 9, 4, 0.3)
rand_test(10, 7, 6, 0.3, small=True)
rand_test(20, 20, 10, 0.2)
rand_test(50, 80, 15, 0.1)
add(256, 256, [("L", 128), ("U", 128), ("R", 64), ("D", 64), ("L", 32), ("U", 32)], rpunch(32, 32, 0.1))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
