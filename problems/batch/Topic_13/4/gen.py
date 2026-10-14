# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random, string

random.seed(1304)
LOW = string.ascii_lowercase
MAXQ = 100_000
MAXSUM = 200_000
tests = []


def add(pairs):
    assert 1 <= len(pairs) <= MAXQ
    assert sum(len(a) for a, b in pairs) <= MAXSUM
    for a, b in pairs:
        assert 1 <= len(a) == len(b)
        assert all(c in LOW for c in a + b)
    tests.append(f"{len(pairs)}\n" + "".join(f"{a} {b}\n" for a, b in pairs))


def word(n, letters=LOW):
    return "".join(random.choice(letters) for _ in range(n))


def coded(a):
    """B is a code of A: apply a random one-to-one rule"""
    p = list(LOW)
    random.shuffle(p)
    rule = dict(zip(LOW, p))
    return "".join(rule[c] for c in a)


def merged(a):
    """two different letters of A become the same letter (A->B is a function, but not one-to-one)"""
    used = sorted(set(a))
    if len(used) < 2:
        return None
    x, y = random.sample(used, 2)
    b = list(coded(a))
    tx = b[a.index(x)]
    for i, c in enumerate(a):
        if c == y:
            b[i] = tx
    return "".join(b)


def split(a):
    """one occurrence of a repeated letter of A becomes a letter not used anywhere else in B"""
    b = list(coded(a))
    rep = [c for c in sorted(set(a)) if a.count(c) >= 2]
    free = [c for c in LOW if c not in b]
    if not rep or not free:
        return None
    x = random.choice(rep)
    pos = [i for i, c in enumerate(a) if c == x]
    b[random.choice(pos)] = random.choice(free)
    return "".join(b)


def mix(q, lo, hi, letters, kinds="cms"):
    out = []
    while len(out) < q:
        a = word(random.randint(lo, hi), letters)
        k = random.choice(kinds)
        b = coded(a) if k == "c" else merged(a) if k == "m" else split(a) if k == "s" else word(len(a), letters)
        if b is not None:
            out.append((a, b))
    return out


# samples
add([("abca", "xyzx"), ("ab", "cc"), ("aa", "bc"), ("paper", "title")])
add([("abc", "abc"), ("aba", "aab"), ("abc", "bca")])
add([("z", "a")])
add([("moon", "noon"), ("aab", "abb"), ("xyz", "zyx")])
add([("abcdefghijklm", "nopqrstuvwxyz"), ("abcdefghijkla", "nopqrstuvwxyz")])
# hidden (small)
add([("a", "a"), ("ab", "ba"), ("ab", "aa"), ("ba", "aa"), ("aa", "ab"), ("aa", "zz")])
add(mix(50, 1, 4, "ab"))
add(mix(300, 1, 8, "abc"))
add(mix(500, 5, 30, LOW, "cmsr"))
add(mix(200, 30, 80, "abcdefgh", "m"))       # only "merge" NO cases (and none YES)
add(mix(200, 30, 80, "abcdefgh", "sc"))      # "split" NO cases and YES cases
# large
a = word(100_000)
b = coded(a)
c = word(100_000, "ab")
d = list(coded(c))
d[-1] = d[0] if c[-1] != c[0] else ("b" if d[0] == "a" else "a")   # spoil only the last letter
add([(a, b), (c, "".join(d))])
add(mix(MAXQ, 2, 2, "abc", "cmsr"))
add(mix(2000, 80, 120, LOW, "cms"))
a = word(100_000, "pq")
add([(a, a.replace("p", "x").replace("q", "p").replace("x", "q")), (a, a.replace("q", "p"))])
add(mix(20_000, 1, 15, "abcd", "cms"))

assert sum(len(t) for t in tests) < 2_950_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
