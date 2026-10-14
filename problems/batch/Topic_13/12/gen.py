# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random, string

random.seed(1312)
MAXQ, MAXP, MAXK, MAXSUMK = 100_000, 10_000, 100_000, 200_000
tests = []


def add(cmds):
    """cmds: list of (name, p) for ADD or int k for TOP"""
    assert 2 <= len(cmds) <= MAXQ
    assert isinstance(cmds[0], tuple)
    tops = [c for c in cmds if not isinstance(c, tuple)]
    assert tops and sum(tops) <= MAXSUMK and all(1 <= k <= MAXK for k in tops)
    lines = []
    for c in cmds:
        if isinstance(c, tuple):
            s, p = c
            assert 1 <= len(s) <= 10 and all(ch in string.ascii_lowercase for ch in s)
            assert 1 <= p <= MAXP
            lines.append(f"ADD {s} {p}")
        else:
            lines.append(f"TOP {c}")
    tests.append(f"{len(cmds)}\n" + "\n".join(lines) + "\n")


def rname(lo, hi, alpha=string.ascii_lowercase):
    return "".join(random.choice(alpha) for _ in range(random.randint(lo, hi)))


def rnd(q, names, p_top, pmax, kmax, sumk=MAXSUMK, plo=1):
    """random commands; names: pool of player names; TOP k with k in [1, kmax] while the budget lasts"""
    cmds = [(random.choice(names), random.randint(plo, pmax))]
    left = sumk
    for _ in range(q - 2):
        if random.random() < p_top and left > kmax:
            k = random.randint(1, kmax)
            left -= k
            cmds.append(k)
        else:
            cmds.append((random.choice(names), random.randint(plo, pmax)))
    cmds.append(min(left, MAXK))
    return cmds


def pool(n, lo, hi, alpha=string.ascii_lowercase):
    s = set()
    while len(s) < n:
        s.add(rname(lo, hi, alpha))
    return sorted(s)


# samples
add([("bo", 5), ("ann", 3), ("cat", 5), 2, ("ann", 4), 5])
add([("anna", 2), ("ann", 2), ("b", 1), 1, 3])
add([("z", 10000), ("z", 10000), 100])
add([("ka", 3), ("ja", 4), ("ka", 1), 3, ("ab", 4), 2])
add([("mo", 7), ("tom", 7), ("al", 1), 1, 4])
# hidden (small)
add([("a", 1), MAXK])
add([("b", 1), ("a", 1), ("ab", 1), ("aa", 1), ("ba", 1), ("a", 1), 6, ("b", 1), 2, ("aaa", 2), 3])
add(rnd(40, pool(6, 1, 3, "ab"), 0.3, 3, 8))
add(rnd(300, pool(30, 1, 4, "abc"), 0.3, 5, 40))
add(rnd(3000, pool(500, 1, 10), 0.4, MAXP, 600))
add(rnd(2000, pool(100, 1, 3, "vwxyz"), 0.5, 2, 200))
# large
add(rnd(MAXQ, pool(30_000, 2, 4), 0.5, MAXP, 7))
add(rnd(40_000, pool(20_000, 1, 4, "abcdefghijklmnopqrst"), 0.5, 1, 7))   # every gain is 1: many ties
add(rnd(30_000, pool(40, 1, 10), 0.5, MAXP, 8))                          # few players, big scores
cmds = [("k", MAXP)] * 30_000 + [("q", 1), 3]                              # one big score
add(cmds)
names = pool(45_000, 3, 4)
add([(s, random.randint(1, 9)) for s in names] + [MAXK, 50_000, 50_000])  # long TOP lines

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
