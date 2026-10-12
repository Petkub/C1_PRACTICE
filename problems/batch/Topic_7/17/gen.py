# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
# Generates a plaintext M, encodes it, and writes K and C.
import os, random, string

random.seed(707)
tests = []
ALNUM = string.ascii_lowercase + string.digits
MAXN = 1_000_000

def encode(m, k):
    rows = [[] for _ in range(min(k, len(m)))]
    r, d = 0, 1
    for ch in m:
        rows[r].append(ch)
        if k > 1:
            if not (0 <= r + d < len(rows)):
                d = -d
            r += d
    return "".join("".join(x) for x in rows)

def add(k, m):
    assert 1 <= k <= 10**9 and 1 <= len(m) <= MAXN and all(ch in ALNUM for ch in m)
    tests.append(f"{k}\n{encode(m, k)}\n")

def rnd(n, alpha=ALNUM):
    return "".join(random.choice(alpha) for _ in range(n))

assert encode("posncamp2026", 3) == "pc2onap06sm2"
# samples
add(3, "posncamp2026")
add(2, "helloworld")
add(1, "abc")
add(4, "thequickbrownfox")
add(100, "toi21")
# hidden
add(1, "z")
add(10**9, "z")
add(2, "ab")
add(5, "abcde")
add(5, "abcdefghi")
for k in [2, 7, 50]:
    add(k, rnd(random.randint(100, 3000)))
add(999, rnd(2000))
add(1000, rnd(1001))
add(1000, rnd(999))
# big
add(10**9, rnd(400000))
add(2, rnd(400000))
add(1000, rnd(MAXN))
add(MAXN - 1, rnd(MAXN))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
