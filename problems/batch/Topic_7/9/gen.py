# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random, string

random.seed(705)
tests = []
AL = string.ascii_lowercase

def add(p, words):
    assert 1 <= len(p) <= 26 and len(set(p)) == len(p) and all(c in AL for c in p)
    assert 1 <= len(words) <= 100000
    for w in words:
        assert 1 <= len(w) <= 20 and all(c in p for c in w)
    tests.append(p + "\n" + f"{len(words)}\n" + "".join(w + "\n" for w in words))

def perm():
    l = list(AL)
    random.shuffle(l)
    return "".join(l)

def word(alpha, lo, hi):
    return "".join(random.choice(alpha) for _ in range(random.randint(lo, hi)))

REV = AL[::-1]
# samples
add("zyxsoear", ["xray", "zoo", "yes"])
add("ctbaeg", ["cat", "cabbage", "cab"])
add("abcehlnpry", ["banana", "apple", "cherry", "apple"])
add("qwertyuiop", ["type", "write", "quiet", "query", "pie"])
add("ba", ["a", "ab", "ba", "aa", "b", "bb"])
# hidden
add(perm(), ["z"])
add("ba", [word("ab", 1, 6) for _ in range(300)])
add("k", [word("k", 1, 20) for _ in range(300)])
add("pqrst", [word("tsrqp", 1, 5) for _ in range(1000)])
add(REV, [word("xyz", 1, 4) for _ in range(500)])
p = perm()
add(p, ["a" * k for k in range(20, 0, -1)] + ["b" * k for k in range(1, 21)])
add(perm(), [word(AL, 1, 20) for _ in range(2000)])
q = perm()
add(q, [word(q[:3], 1, 8) for _ in range(2000)])
# prefix chains
p = perm()
base = word(AL, 20, 20)
add(p, [base[:random.randint(1, 20)] + ("" if random.random() < 0.5 else word(AL, 0, 0)) for _ in range(1500)])
# big tests (brute will time out)
add(perm(), [word(AL, 1, 20) for _ in range(100000)])
add("cab", [word("abc", 1, 6) for _ in range(100000)])
add(REV, ["zz", "yyy"] * 50000)
p = perm()
add(p, [base[:random.randint(15, 20)] for _ in range(20000)])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
