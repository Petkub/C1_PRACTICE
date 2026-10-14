# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random, string

random.seed(1310)
MAXN = 100_000
LOW = string.ascii_lowercase
tests = []


def add(ws):
    n = len(ws)
    assert 1 <= n <= MAXN
    assert all(1 <= len(w) <= 10 and all(c in LOW for c in w) for w in ws)
    tests.append(f"{n}\n" + " ".join(ws) + "\n")


def word(lmin, lmax, letters=LOW):
    return "".join(random.choice(letters) for _ in range(random.randint(lmin, lmax)))


def perm(w):
    a = list(w)
    random.shuffle(a)
    return "".join(a)


def from_bases(n, bases):
    return [perm(random.choice(bases)) for _ in range(n)]


# samples
add("listen silent enlist tinsel google cat act".split())
add("evil rat vile tar live art".split())
add("aa a aa".split())
add("abc cab ba ab".split())
add(["zoo"])
add("dog cat bird".split())
# hidden (small)
add(["a"])
add(["abcdefghij"] * 5)
add("cab bad dab abc ad da".split())        # sizes 2,2,2: smallest words abc, ad, bad
add([word(1, 2, "abc") for _ in range(50)])
add(from_bases(300, [word(2, 4, "abcde") for _ in range(20)]))
add([word(1, 3, "abcd") for _ in range(3000)])
# large
add([word(5, 10) for _ in range(MAXN)])                                  # almost all alone
add(from_bases(MAXN, [word(3, 6) for _ in range(2000)]))                 # about 50 words per group
big = [perm("aabbccddee") for _ in range(30_000)]
rest = from_bases(20_000, [word(1, 10) for _ in range(5000)])
ws = big + rest
random.shuffle(ws)
add(ws)                                                                  # one huge group
add([word(1, 2) for _ in range(MAXN)])                                   # groups of up to 2 letters
add(from_bases(50_000, ["ab", "ba", "ac", "bc", "aab"]))
alone = {}
while len(alone) < 30_000:
    w = word(8, 10)
    alone.setdefault("".join(sorted(w)), w)
add(list(alone.values()))                                                # every group alone

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
assert sum(len(t) for t in tests) < 3_000_000
print("total bytes", sum(len(t) for t in tests))
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
