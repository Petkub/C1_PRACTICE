# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random, string

random.seed(714)
tests = []
AL = string.ascii_lowercase

def add(neck):
    assert 1 <= len(neck) <= 2000
    for s in neck:
        assert 1 <= len(s) <= 100 and all(c in AL for c in s)
    tests.append(f"{len(neck)}\n" + "".join(s + "\n" for s in neck))

def rnd(L, pool):
    return "".join(random.choice(pool) for _ in range(L))

def variant(s):
    i = random.randrange(len(s))
    t = s[i:] + s[:i]
    return t[::-1] if random.random() < 0.5 else t

def mixed(count, nbase, lens, pool):
    bases = [rnd(random.choice(lens), pool) for _ in range(nbase)]
    return [variant(random.choice(bases)) for _ in range(count)]

# samples
add(["abcd", "cdab", "dcba", "acbd", "bdac"])
add(["abc", "acb", "aabb", "abab"])
add(["z"])
add(["ab", "ba", "a", "b", "aa"])
add(["posn", "nsop", "snop", "opsn", "npos", "psno"])
# hidden
add(["q"] * 7)
add(["abc", "abc", "abcd", "ab", "a"])
add(["aab", "aba", "baa", "abb", "bab", "bba", "aaa", "bbb"])
add(["abcabd", "dbacba", "abdabc", "acbadb"])
add(mixed(100, 10, [4, 5, 6], "ab"))
add(mixed(500, 300, [3, 4, 5, 6, 7, 8], "abc"))
add([rnd(random.randint(1, 8), "ab") for _ in range(2000)])
add(mixed(2000, 2000, [100], AL))
add(mixed(2000, 3, [100], "ab"))
add(mixed(2000, 600, list(range(90, 101)), "abc"))
s = "a" * 99 + "b"
add([s[i:] + s[:i] for i in range(100)] * 20)
add(["ab" * 50] * 1000 + ["ba" * 50] * 1000)
add(mixed(2000, 1000, [100], "xy"))
def sparse(L, k):
    t = ["a"] * L
    for i in random.sample(range(L), k):
        t[i] = "b"
    return "".join(t)
add([sparse(100, random.choice([3, 4])) for _ in range(2000)])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
