# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random, string

random.seed(713)
tests = []
AL = string.ascii_lowercase

def fb(x, g):
    L = len(x)
    f = ["-"] * L
    cnt = {}
    for i in range(L):
        if g[i] == x[i]:
            f[i] = "G"
        else:
            cnt[x[i]] = cnt.get(x[i], 0) + 1
    for i in range(L):
        if f[i] != "G" and cnt.get(g[i], 0) > 0:
            f[i] = "Y"
            cnt[g[i]] -= 1
    return "".join(f)

def add(words, recs):
    m, k = len(words), len(recs)
    assert 1 <= m <= 10_000 and 1 <= k <= 20
    L = len(words[0])
    assert 1 <= L <= 10 and len(set(words)) == m
    for w in words:
        assert len(w) == L and all(c in AL for c in w)
    for g, f in recs:
        assert len(g) == L and len(f) == L and all(c in AL for c in g) and all(c in "GY-" for c in f)
    tests.append(f"{m} {k}\n" + "".join(w + "\n" for w in words) + "".join(f"{g} {f}\n" for g, f in recs))

def rnd(L, pool):
    return "".join(random.choice(pool) for _ in range(L))

def dictionary(m, L, pool):
    s = set()
    while len(s) < m:
        s.add(rnd(L, pool))
    s = sorted(s)                   # a set of strings iterates in hash order, which changes per run
    random.shuffle(s)
    return s

def game(m, L, pool, k, honest=True):
    words = dictionary(m, L, pool)
    secret = random.choice(words)
    recs = []
    for _ in range(k):
        g = random.choice(words) if random.random() < 0.5 else rnd(L, pool)
        recs.append((g, fb(secret, g)))
    if not honest:
        g, f = recs[-1]
        i = random.randrange(L)
        f = f[:i] + random.choice([c for c in "GY-" if c != f[i]]) + f[i + 1:]
        recs[-1] = (g, f)
    add(words, recs)

# samples
add(["apple", "maple", "plead", "pleat"], [("lemon", "YY---"), ("eagle", "YY-Y-")])
add(["apple", "ample", "lapel"], [("llama", "Y-Y--")])
add(["cat", "dog"], [("cow", "GG-")])
add(["a", "b", "c"], [("a", "-")])
add(["sleep", "spree", "geese", "speed"], [("eerie", "YY---")])
# hidden
add(["z"], [("z", "G")])
add(["ab", "ba", "aa", "bb"], [("ab", "YY")])
add(["aab", "aba", "baa", "abb", "bab", "bba"], [("aaa", "-G-"), ("bbb", "G-G")])
game(50, 4, "abc", 3)
game(200, 5, "abcde", 5)
game(1000, 5, "aeiolnrst", 2)
game(3000, 6, "abcd", 3)
game(1000, 10, "ab", 4)
game(10_000, 10, AL, 20)
game(10_000, 5, AL, 2)
game(10_000, 7, "abcdef", 4, honest=False)
game(5000, 3, AL, 1)
w = dictionary(6000, 8, "abc")
add(w, [("aaaaaaaa", "--------")] * 20)

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
