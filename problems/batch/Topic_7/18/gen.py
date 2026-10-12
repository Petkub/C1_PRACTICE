# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random, string

random.seed(708)
tests = []
AL = string.ascii_lowercase
V = "aeiou"
C = "".join(c for c in AL if c not in V)
MAXN = 1_000_000

def add(s):
    assert 1 <= len(s) <= MAXN and all(c in AL for c in s)
    tests.append(s + "\n")

def rnd(n, pv):
    return "".join(random.choice(V) if random.random() < pv else random.choice(C) for _ in range(n))

# samples
add("banana")
add("rhythm")
add("a")
add("posncamp")
add("aeioubcdfg")
# hidden
add("z")
add("ab")
add("aa")
add(rnd(20, 0.5))
add(rnd(1000, 0.5))
add(rnd(5000, 0.3))
add(rnd(20000, 0.5))
add("ab" * 10000)
# big
add("ba" * (MAXN // 2))                 # answer ~ n^2/4
add("e" * 250000)                      # answer 0
add(rnd(MAXN, 0.5))
add("a" * 125000 + "b" * 125000)
add(rnd(249999, 0.4))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
