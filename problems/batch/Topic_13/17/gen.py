# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random, itertools, string

random.seed(1317)
LOW = string.ascii_lowercase
tests = []

def add(L, words):
    n = len(words)
    assert 1 <= n <= 50_000 and 1 <= L <= 10
    assert len(set(words)) == n
    for w in words:
        assert len(w) == L and all(c in LOW for c in w)
    tests.append(f"{n} {L}\n" + "\n".join(words) + "\n")

def rand_word(L, alpha=LOW):
    return "".join(random.choice(alpha) for _ in range(L))

def clustered(n, L, bases, alpha=LOW, maxchg=2):
    """words near a few base words: many pairs at distance 1, some at distance 2+"""
    bs = [rand_word(L, alpha) for _ in range(bases)]
    got = set()
    while len(got) < n:
        w = list(random.choice(bs))
        for _ in range(random.randint(0, maxchg)):
            w[random.randrange(L)] = random.choice(alpha)
        got.add("".join(w))
    res = sorted(got)
    random.shuffle(res)
    return res

def all_words(L, alpha):
    return ["".join(t) for t in itertools.product(alpha, repeat=L)]

# samples
add(3, ["cat", "cot", "cog", "dog", "dot"])
add(3, ["act", "cat", "tac", "tca"])
add(1, ["a", "b", "z"])
add(4, ["abcd"])
add(2, ["aa", "ab", "ba", "bb", "ca", "zz"])
add(4, ["rose", "rise", "rile", "ride", "hide", "hire", "rope"])
# hidden (small)
add(1, list(LOW))
add(2, ["ab", "ba"])
add(10, clustered(60, 10, 3))
add(5, clustered(800, 5, 20, "abcde", 3))
add(2, all_words(2, LOW))
# large
w = all_words(3, LOW)
random.shuffle(w)
add(3, w)                                          # every 3-letter word
w = all_words(4, LOW[:15])
add(4, random.sample(w, 50_000))                   # dense 4-letter words
add(10, clustered(50_000, 10, 1500, LOW, 2))
add(10, sorted({rand_word(10) for _ in range(50_000)}))
w = ["".join(t) for t in itertools.product("abc", "wxyz", repeat=4)]
random.shuffle(w)
add(8, w)                                          # small alphabet per position, 20736 words
add(6, clustered(50_000, 6, 400, "abcdefgh", 3))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
