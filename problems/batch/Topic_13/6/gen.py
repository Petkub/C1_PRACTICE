# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random, string

random.seed(1306)
MAXQ = 100_000
LOW = string.ascii_lowercase
CODE = string.ascii_uppercase + string.digits
tests = []


def ok_name(s):
    return 1 <= len(s) <= 20 and all(c in LOW for c in s)


def ok_book(s):
    return 1 <= len(s) <= 10 and all(c in CODE for c in s)


def add(cmds):
    assert 1 <= len(cmds) <= MAXQ
    lines = []
    for c in cmds:
        if c[0] == "BORROW":
            assert len(c) == 3 and ok_name(c[1]) and ok_book(c[2])
        elif c[0] in ("RETURN", "WHO"):
            assert len(c) == 2 and ok_book(c[1])
        else:
            assert c[0] == "COUNT" and len(c) == 2 and ok_name(c[1])
        lines.append(" ".join(c))
    tests.append(f"{len(cmds)}\n" + "\n".join(lines) + "\n")


def words(k, alphabet, lmin, lmax):
    out = set()
    while len(out) < k:
        out.add("".join(random.choice(alphabet) for _ in range(random.randint(lmin, lmax))))
    return sorted(out)


def rnd(q, names, books, w, prefill=0):
    """w = weights of (BORROW, RETURN, WHO, COUNT); prefill = BORROWs of distinct books first"""
    loans = {}
    cmds = []
    for b in random.sample(books, prefill):
        n = random.choice(names)
        loans[b] = n
        cmds.append(("BORROW", n, b))
    while len(cmds) < q:
        t = random.choices(["BORROW", "RETURN", "WHO", "COUNT"], weights=w)[0]
        on_loan = list(loans) if loans and random.random() < 0.7 else None
        if t == "BORROW":
            if on_loan and random.random() < 0.4:
                b = random.choice(on_loan)
            else:
                b = random.choice(books)
            n = random.choice(names)
            if b not in loans:
                loans[b] = n
            cmds.append((t, n, b))
        elif t == "RETURN":
            b = random.choice(on_loan) if on_loan else random.choice(books)
            loans.pop(b, None)
            cmds.append((t, b))
        elif t == "WHO":
            b = random.choice(on_loan) if on_loan else random.choice(books)
            cmds.append((t, b))
        else:
            cmds.append((t, random.choice(names)))
    return cmds


B = lambda n, b: ("BORROW", n, b)
R = lambda b: ("RETURN", b)
W = lambda b: ("WHO", b)
C = lambda n: ("COUNT", n)
# samples
add([B("nok", "A12"), B("fon", "B7"), B("fon", "A12"), C("nok"),
     R("A12"), B("fon", "A12"), C("fon")])
add([R("X1"), B("pim", "X1"), B("pim", "X1"), R("X1"), W("X1"), R("X1")])
add([B("dam", "K1"), B("dam", "K2"), R("K1"), C("dam"), W("K1")])
add([C("a")])
add([B("bee", "Z9"), W("Z90"), W("Z9")])
# hidden (small)
add([W("A")])
add([B("a" * 20, "ABCDEFGHIJ"), B("b" * 20, "ABCDEFGHIJ"), C("a" * 20), C("b" * 20),
     R("ABCDEFGHIJ"), R("ABCDEFGHIJ"), C("a" * 20), B("b" * 20, "ABCDEFGHIJ"), W("ABCDEFGHIJ")])
add(rnd(40, ["ann", "ben", "cat"], ["B1", "B2", "B3", "B4"], [4, 3, 2, 2]))
add(rnd(300, words(10, "abc", 1, 3), words(30, "AB12", 1, 3), [4, 3, 2, 2]))
add(rnd(3000, words(200, LOW, 1, 20), words(500, CODE, 1, 10), [5, 3, 2, 2]))
add(rnd(5000, words(5, "ab", 1, 2), words(2000, CODE, 1, 4), [6, 1, 2, 3]))
# large
add(rnd(MAXQ, words(15000, LOW, 1, 3), words(60000, CODE, 4, 4), [3, 2, 3, 2], prefill=45000))
add(rnd(25_000, words(3000, LOW, 5, 20), words(30000, CODE, 6, 10), [3, 1, 3, 2], prefill=12000))
add(rnd(40_000, ["x"], words(25000, CODE, 3, 3), [2, 1, 2, 1], prefill=20000))

for t in tests:
    assert t.endswith("\n") and "  " not in t and " \n" not in t
assert sum(len(t) for t in tests) < 3_000_000
print("total bytes", sum(len(t) for t in tests))
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
