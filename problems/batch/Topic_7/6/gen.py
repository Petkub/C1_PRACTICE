# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random, string

random.seed(705)
tests = []
AL = string.ascii_lowercase

def add(t, words):
    assert 1 <= len(t) <= 10_000 and all(c in AL for c in t)
    assert 1 <= len(words) <= 1000
    for w in words:
        assert 1 <= len(w) <= 100 and all(c in AL for c in w)
    tests.append(f"{t}\n{len(words)}\n" + "".join(w + "\n" for w in words))

def rnd(n, pool=AL):
    return "".join(random.choice(pool) for _ in range(n))

def sub(t, m):
    # a random subsequence of t of length m
    idx = sorted(random.sample(range(len(t)), m))
    return "".join(t[i] for i in idx)

# samples
add("programming", ["pgm", "gap", "rig"])
add("banana", ["ana", "nab", "a", "bananas"])
add("x", ["x", "xx", "y"])
add("posncamp", ["pos", "camp", "pn", "sop"])
add("abcabcabc", ["cba", "ccc", "aaaa", "abcabcabc"])
# hidden
add("a", ["a"])
add("z" * 10000, ["z", "z" * 100, "zy", "y"])
add("ab" * 5000, ["b" * 100, "ba" * 50, "a" * 100, "c"])
t = rnd(200, "abc")
add(t, [sub(t, random.randint(1, 20)) for _ in range(100)] + [rnd(random.randint(1, 20), "abc") for _ in range(100)])
t = rnd(1000, "ab")
add(t, [rnd(random.randint(1, 100), "ab") for _ in range(300)])
t = rnd(2000)
add(t, [sub(t, random.randint(1, 100)) for _ in range(150)] + [rnd(random.randint(1, 5)) for _ in range(150)])
t = rnd(10000)
add(t, [sub(t, random.randint(1, 100)) for _ in range(500)] + [rnd(random.randint(1, 100)) for _ in range(500)])
t = "".join(AL[i % 26] for i in range(10000))
add(t, ["".join(AL[(i * 7) % 26] for i in range(100)), "zyx", AL * 3 + "zzzzzz", "a" * 100] + [rnd(100) for _ in range(996)])
t = rnd(10000, "xyz")
add(t, [rnd(100, "xyz") for _ in range(990)] + ["xyz" * 33, t[-50:], t[:100], "w"] + [sub(t, 100) for _ in range(6)])
add("a" * 9999 + "b", ["a" * 99 + "c" for _ in range(500)] + ["a" * random.randint(1, 99) + "b" for _ in range(500)])

os.makedirs("tests", exist_ok=True)
for i, tt in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(tt)
