# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random, itertools, string

random.seed(1320)
LOW = string.ascii_lowercase
tests = []

def add(words, queries):
    n, q = len(words), len(queries)
    assert 1 <= n <= 100_000 and 1 <= q <= 100_000
    assert len(set(words)) == n
    for w in words + queries:
        assert 1 <= len(w) <= 10 and all(c in LOW for c in w)
    tests.append(f"{n} {q}\n" + "\n".join(words) + "\n" + "\n".join(queries) + "\n")

def word(lo, hi, alpha=LOW):
    return "".join(random.choice(alpha) for _ in range(random.randint(lo, hi)))

def dictionary(n, lo, hi, alpha=LOW):
    got = set()
    while len(got) < n:
        got.add(word(lo, hi, alpha))
    res = sorted(got)
    random.shuffle(res)
    return res

def queries(words, q, alpha=LOW, pmiss=0.25):
    """mostly prefixes of dictionary words (sometimes a whole word), some random strings"""
    res = []
    for _ in range(q):
        if random.random() < pmiss:
            res.append(word(1, 10, alpha))
        else:
            w = random.choice(words)
            res.append(w[:random.randint(1, len(w))])
    return res

# samples
add(["card", "car", "care", "cat", "cart"], ["car", "ca", "x"])
add(["apple", "app", "apply"], ["a", "appl", "apples"])
add(["z"], ["z", "zz"])
add(["ba", "b", "bz", "bba"], ["b", "bb"])
add(["aaa", "aba", "abb"], ["a", "ab", "aac"])
add(["aaa", "aab", "aba", "abb", "baa"], ["a", "ab", "b", "aac", "abbb"])
add(["card", "car", "care", "cat", "dog", "cart"], ["car", "ca", "d", "x"])
# hidden (small)
add(["abz", "abzz", "abzzz", "ab", "aby", "ac", "abzzzzzzzz"], ["ab", "abz", "abzz", "aby", "abzzzzzzzz", "a", "zz"])
add(["zzzzzzzzzz", "zzzzz", "z"], ["z", "zzzzzz", "zzzzzzzzzz", "zy"])
w = dictionary(40, 1, 4, "abc")
add(w, queries(w, 60, "abc"))
w = ["".join(t) for k in range(1, 11) for t in itertools.product("ab", repeat=k)]
random.shuffle(w)
add(w, list(w))                                        # every a/b word, every a/b query
w = dictionary(3000, 1, 10)
add(w, queries(w, 3000))
w = dictionary(2000, 6, 10, "xyz")
add(w, queries(w, 2000, "xyz", 0.1))
# large
w = dictionary(100_000, 3, 8)
add(w, queries(w, 100_000))
w = dictionary(50_000, 5, 10, "abc")
add(w, queries(w, 50_000, "abc", 0.1))
w = dictionary(40_000, 1, 10, "mno")
add(w, ["m"] * 10_000 + ["n"] * 10_000 + queries(w, 30_000, "mno", 0.05))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
