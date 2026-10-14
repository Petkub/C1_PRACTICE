# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random, string

random.seed(1314)
MAXN, MAXC, MAXLEN = 50_000, 10_000, 40
tests = []


def add(rows):
    """rows: list of (c, domain)"""
    assert 1 <= len(rows) <= MAXN
    for c, d in rows:
        assert 1 <= c <= MAXC
        assert 1 <= len(d) <= MAXLEN
        parts = d.split(".")
        assert 1 <= len(parts) <= 4
        assert all(p and all(ch in string.ascii_lowercase for ch in p) for p in parts)
    tests.append(f"{len(rows)}\n" + "".join(f"{c} {d}\n" for c, d in rows))


def rpart(lo, hi, alpha=string.ascii_lowercase):
    return "".join(random.choice(alpha) for _ in range(random.randint(lo, hi)))


def rdomain(kmax, lo, hi, alpha=string.ascii_lowercase, tops=None):
    k = random.randint(1, kmax)
    parts = [rpart(lo, hi, alpha) for _ in range(k)]
    if tops and random.random() < 0.7:
        parts[-1] = random.choice(tops)
    return ".".join(parts)


def rnd(n, cmax, kmax, lo, hi, alpha=string.ascii_lowercase, tops=None, reuse=0.0):
    rows = []
    for _ in range(n):
        if rows and random.random() < reuse:
            d = random.choice(rows)[1]
        else:
            d = rdomain(kmax, lo, hi, alpha, tops)
        rows.append((random.randint(1, cmax), d))
    return rows


TOPS = ["com", "net", "org", "th", "co", "io", "ac"]

# samples
add([(5, "mail.google.com"), (2, "google.com"), (4, "www.go.th")])
add([(1, "a.b"), (1, "ab"), (2, "b")])
add([(2, "x.co"), (2, "co.th")])
add([(4, "a.b.c.d"), (1, "a.b.c.d"), (3, "c.d")])
add([(10000, "th")])
# hidden (small)
add([(1, "a")])
add([(3, "b.a"), (3, "ba"), (3, "b"), (3, "a.a"), (3, "aa"), (2, "a"), (1, "b.b")])
add(rnd(30, 3, 4, 1, 2, "ab", reuse=0.2))
add(rnd(300, 5, 4, 1, 3, "abc", reuse=0.2))
add(rnd(2000, 100, 4, 1, 6, tops=TOPS, reuse=0.3))
add([(random.randint(1, MAXC), ".".join(rpart(9, 10) for _ in range(4))[:MAXLEN]) for _ in range(300)]
    + [(MAXC, "z" * 40), (MAXC, "y" * 19 + "." + "z" * 20)])
# large
add(rnd(MAXN, MAXC, 4, 1, 4))                                       # many different domains
add(rnd(MAXN, 20, 4, 1, 2, "abcd", reuse=0.1))                      # many ties
add(rnd(10_000, MAXC, 4, 7, 9, tops=TOPS, reuse=0.2))              # long domains
add([(MAXC, "a.b.c.d")] * 20_000)                                   # one domain, big totals
add(rnd(30_000, MAXC, 4, 2, 5, tops=TOPS, reuse=0.5))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
