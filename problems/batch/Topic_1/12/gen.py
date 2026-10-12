# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(1012)
E = 10**18
G = 10**9
OPS = ["<", "<=", ">", ">="]
tests = []

def add(sets):
    assert 1 <= len(sets) and sum(len(ineq) for _, _, ineq in sets) <= 100_000
    out = [f"{len(sets)}"]
    for l, r, ineq in sets:
        assert -E <= l <= r <= E and len(ineq) >= 1
        out.append(f"{len(ineq)} {l} {r}")
        for a, op, c in ineq:
            assert -G <= a <= G and -G <= c <= G and op in OPS
            out.append(f"{a} {op} {c}")
    tests.append("\n".join(out) + "\n")

def ineq(am, cm):
    a = random.randint(-am, am)
    if random.random() < 0.1:
        a = 0
    return (a, random.choice(OPS), random.randint(-cm, cm))

def through(x, am):
    # an inequality that x satisfies with equality or nearly, to keep answers non-empty and tight
    a = random.randint(1, am) * random.choice([-1, 1])
    op = random.choice(OPS)
    c = a * x + {"<": 1, "<=": 0, ">": -1, ">=": 0}[op] + random.randint(-1, 1)
    c = max(-G, min(G, c))
    return (a, op, c)

def small_set(am, cm, rm):
    l = random.randint(-rm, rm)
    r = random.randint(l, rm)
    n = random.randint(1, 5)
    x = random.randint(l, r)
    return (l, r, [ineq(am, cm) if random.random() < 0.5 else through(x + random.randint(-3, 3), am) for _ in range(n)])

def holds(x, am, slack):
    # an inequality that x satisfies (|a x| stays within the limits)
    am = max(1, min(am, (G - slack - 1) // max(1, abs(x))))
    a = random.randint(1, am) * random.choice([-1, 1])
    op = random.choice(OPS)
    s = random.randint(0, slack)
    c = a * x + {"<": 1 + s, "<=": s, ">": -1 - s, ">=": -s}[op]
    assert -G <= c <= G
    return (a, op, c)

def big_set(n):
    l = random.choice([-E, random.randint(-E, E)])
    r = random.choice([E, random.randint(l, E)])
    w = G - 10**6 - 2
    x = random.choice([random.randint(-w, w), random.randint(-1000, 1000), random.randint(-10**6, 10**6)])
    if not l <= x <= r:
        l, r = min(l, x), max(r, x)
    return (l, r, [holds(x, random.choice([1, 10, 1000, G]), random.choice([0, 1, 100, 10**6]))
                   if random.random() < (0.9 if n <= 10 else 1.0) else ineq(G, G) for _ in range(n)])

# samples
add([(-10, 10, [(2, "<=", 7), (-3, "<", 6)]), (1, 5, [(4, ">", 20)])])
add([(-20, 20, [(-2, "<=", 9), (3, "<", 10), (-4, ">", -15)])])
add([(-100, 100, [(0, "<", 1), (5, ">=", -12), (-7, ">=", -30)]), (-100, 100, [(0, ">=", 1)])])
add([(-5, 5, [(-3, "<=", -7)]), (-5, 5, [(0, ">=", 0)]), (3, 3, [(1, ">", 2)])])
add([(-1000000, 1000000, [(1, ">=", -1000)]), (0, 9, [(3, ">", 3), (3, "<", 3)])])
# hidden, small (checked by the brute)
add([small_set(5, 20, 30) for _ in range(3000)])
add([small_set(30, 1000, 300) for _ in range(1000)])
add([(l, l + 200, [(a, op, c)]) for l in (-100,) for a in range(-6, 7) for op in OPS for c in range(-13, 14)])
add([small_set(G, G, 1000) for _ in range(500)])
add([(-50, 50, [holds(x, 9, random.choice([0, 0, 1, 3])) for _ in range(20)]) for x in (random.randint(-50, 50) for _ in range(300))])
# hidden, big
add([(-E, E, [(1, ">=", -G)]), (-E, E, [(0, "<=", 0)]), (-E, E, [(-1, "<", -G)]), (-E, -E, [(1, "<", 0)]),
     (E, E, [(1, ">", G)]), (-E, E, [(G, ">=", G), (G, "<=", G)]), (-E, E, [(G, ">", G), (G, "<=", G)]),
     (-E, E, [(-G, ">", -G)]), (-E, E, [(-G, "<", G)]), (-E, E, [(7, "<=", -G), (-7, "<=", -G)]),
     (-E, E, [(3, ">", -G), (3, "<", G)]), (0, E, [(-2, "<=", -G)]), (-E, 0, [(-2, ">=", -G)])])
add([big_set(5) for _ in range(4_000)])
add([big_set(1000) for _ in range(30)])
add([big_set(30_000)])
add([big_set(1) for _ in range(5_000)])
add([(random.randint(-E, 0), random.randint(0, E), [ineq(G, G)]) for _ in range(6_000)])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
