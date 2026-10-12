# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random, string

random.seed(716)
tests = []
AL = string.ascii_lowercase
MAXN = 1_000_000

def add(s):
    assert 1 <= len(s) <= MAXN and all(c in AL for c in s)
    tests.append(s + "\n")

def rnd(n, pool=AL):
    return "".join(random.choice(pool) for _ in range(n))

def skewed(n, pool, rare):
    # mostly common letters, the rare letters appear only a few times
    s = [random.choice(pool) for _ in range(n)]
    for c in rare:
        for _ in range(random.randint(1, 3)):
            s[random.randrange(n)] = c
    return "".join(s)

# samples
add("aabbcbbaacb")
add("zzzz")
add("abc")
add("posncamp")
add("abacabadabacaba")
# hidden
add("q")
add("ab")
add("abba")
add(AL)
add(AL[::-1] + AL)
add(rnd(30, "abc"))
add(skewed(1000, "ab", "cd"))
add(skewed(20000, "abcdefgh", "xyz"))
add(rnd(30000))
add("a" * 299_999 + "b" + "a" * 300_000)
add(skewed(MAXN, AL[:20], "xyz"))
add("".join(AL[i % 26] for i in range(500_000)))
add(rnd(400_000, "ab") + "c")
add(rnd(150_000))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
