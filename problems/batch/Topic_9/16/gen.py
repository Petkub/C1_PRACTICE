# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(916)
LET = "abcdefghijkl"
tests = []

def add(sets):
    assert 2 <= len(sets) <= 100000
    for s in sets:
        assert s == "-" or (1 <= len(s) <= 12 and len(set(s)) == len(s) and all(c in LET for c in s))
    tests.append(f"{len(sets)}\n" + "\n".join(sets) + "\n")

def rand_set(p):
    s = [c for c in LET if random.random() < p]
    random.shuffle(s)
    return "".join(s) if s else "-"

def from_pool(pool, n):
    out = []
    for _ in range(n):
        s = list(random.choice(pool))
        random.shuffle(s)
        out.append("".join(s) if s and s != ["-"] else "-")
    return out

# samples
add(["ab", "a", "abc"])
add(["ba", "ab", "-"])
add(["a", "b"])
add(["-", "-", "l", "kl"])
add(["abcdefghijkl", "lkj", "jk", "abc", "c"])
# hidden
add(["-", "-"])
add(["abcdefghijkl", "lkjihgfedcba"])
add(["-"] * 100000)                                            # 99999 * 100000
add([rand_set(0.5) for _ in range(100000)])
add([rand_set(0.15) for _ in range(100000)])
add(from_pool(["a", "b", "ab", "c", "-", "abcdefghijkl"], 60000))
add([rand_set(random.random()) for _ in range(20000)])
add([rand_set(0.5) for _ in range(10)])
add([rand_set(0.3) for _ in range(300)])
add([rand_set(0.7) for _ in range(2000)])
add(from_pool(["ace", "bdf", "abcdef", "ghijkl"], 50))
singles = list(LET)
add([random.choice(singles) for _ in range(5000)])             # only equal pairs count

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
