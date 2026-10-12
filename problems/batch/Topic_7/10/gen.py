# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random, string

random.seed(706)
tests = []
AL = string.ascii_lowercase
MAXN = 1_000_000

def add(s):
    assert 1 <= len(s) <= MAXN and all(c in AL for c in s)
    tests.append(s + "\n")

def rnd(n, alpha):
    return "".join(random.choice(alpha) for _ in range(n))

# samples
add("baacb")
add("abcdcc")
add("z")
add("dcba")
add("racecar")
# hidden (small: brute checks them)
add("ab")
add("aa")
add("zyzyz")
add("abcdefgh")
add("aabbccddeeffgg")
add(rnd(12, "ab"))
add(rnd(13, "abc"))
add(rnd(14, "xyz"))
add(rnd(10, AL))
add("qqqwwweee")
# big
add(rnd(MAXN, AL))
add("y" * (MAXN - 1) + "a")
add((AL * 20000)[:300000])
add(rnd(200001, "mn"))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
