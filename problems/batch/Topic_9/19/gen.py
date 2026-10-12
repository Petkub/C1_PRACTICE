# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
# Every test file holds several functions; a file passes only if every answer in it is right.
import os, random

random.seed(919)
MAXT = 10000
MAXSUM = 1 << 21
tests = []

def add(cases):
    assert 1 <= len(cases) <= MAXT
    assert sum(1 << n for n, t in cases) <= MAXSUM
    lines = [str(len(cases))]
    for n, t in cases:
        assert 1 <= n <= 20 and len(t) == 1 << n and set(t) <= {"0", "1"}
        lines += [str(n), t]
    tests.append("\n".join(lines) + "\n")

def table(n, f):
    # f gets the list x[0..n-1] = (x_1, ..., x_n)
    out = []
    for i in range(1 << n):
        x = [(i >> (n - 1 - k)) & 1 for k in range(n)]
        out.append("1" if f(x) else "0")
    return "".join(out)

def table_mask(n, f):
    # faster: f gets the row index i (bit n-1-k is x_{k+1})
    return "".join("1" if f(i) else "0" for i in range(1 << n))

def rand_monotone(n, terms, maxlen):
    ts = [random.sample(range(n), random.randint(1, min(maxlen, n))) for _ in range(terms)]
    return table(n, lambda x: any(all(x[k] for k in term) for term in ts))

def rand_self_dual(n):
    t = ["0"] * (1 << n)
    full = (1 << n) - 1
    for i in range(1 << n):
        if i < (full ^ i):
            v = random.choice("01")
            t[i] = v
            t[full ^ i] = "1" if v == "0" else "0"
    return "".join(t)

def maj(*a):
    return sum(a) * 2 > len(a)

def rand_mono_dual(n):
    # majority of an odd number of variables or nested majorities: monotone and self-dual
    k = random.choice([v for v in (1, 3, 5, 7) if v <= n])
    vs = random.sample(range(n), k)
    if k >= 5 and random.random() < 0.5:
        return table(n, lambda x: maj(x[vs[0]], x[vs[1]], maj(*[x[v] for v in vs[2:]])))
    return table(n, lambda x: maj(*[x[v] for v in vs]))

def flip(t, i):
    return t[:i] + ("1" if t[i] == "0" else "0") + t[i + 1:]

def flip_dual_pair(t, i):
    # flipping a row and its complement row keeps self-duality
    n = len(t).bit_length() - 1
    return flip(flip(t, i), ((1 << n) - 1) ^ i)

def rand_case(n):
    kind = random.randrange(7)
    if kind == 0:
        return rand_monotone(n, random.randint(1, 2 * n), 3)
    if kind == 1:
        return rand_self_dual(n)
    if kind == 2:
        return rand_mono_dual(n)
    if kind == 3:          # monotone, one row broken
        return flip(rand_monotone(n, random.randint(1, 2 * n), 3), random.randrange(1 << n))
    if kind == 4:          # monotone and self-dual, a complementary pair of rows broken: self-dual only (usually)
        return flip_dual_pair(rand_mono_dual(n), random.randrange(1 << n))
    if kind == 5:          # monotone and self-dual with one row broken: usually neither
        return flip(rand_mono_dual(n), random.randrange(1 << n))
    return "".join(random.choice("01") for _ in range(1 << n))

# samples
add([(2, "0001"), (2, "0110")])
add([(3, "00010111"), (1, "10")])
add([(1, "01"), (3, "00000000"), (1, "11")])
add([(3, "01101001"), (2, "0011")])
add([(2, "1000"), (4, table(4, lambda x: x[0] and maj(x[1], x[2], x[3])))])
# hidden
add([(1, t) for t in ("00", "01", "10", "11")] +
    [(2, format(m, "04b")) for m in range(16)])                       # every function of 1 and 2 variables
add([(3, format(m, "08b")) for m in range(256)])                       # every function of 3 variables
add([(n, rand_case(n)) for n in [random.randint(4, 8) for _ in range(300)]])
add([(n, rand_case(n)) for n in [random.randint(9, 10) for _ in range(40)]])
add([(n, rand_case(n)) for n in [11, 12, 11, 12, 11, 12, 11, 12]])
# big tests: one huge function plus small ones of every kind
small = [(4, table(4, lambda x: maj(x[0], x[1], x[3]))), (5, table(5, lambda x: (x[0] ^ x[2] ^ x[4]) == 1)),
         (2, "1000"), (3, "00010110")]
add([(20, table_mask(20, lambda i: (i & 0b00000010100100010100) != 0))] + small)   # x_7 or x_9 or x_12 or x_16 or x_18
add(small[::-1] + [(20, table_mask(20, lambda i: (i & 0b10001000100010000001) == 0b10001000100010000001))])  # x_1 x_5 x_9 x_13 x_20 all 1
big = table_mask(17, lambda i: bin(i).count("1") >= 9)                 # majority of 17 variables
add([(17, big), (16, flip(table_mask(16, lambda i: bin(i >> 1).count("1") >= 8), (1 << 16) - 1 - (1 << 5))),
     (17, flip_dual_pair(big, 0b00000000111111111))])
add([(16, table_mask(16, lambda i: ((i >> 3) ^ (i >> 8) ^ (i >> 15)) & 1)),
     (16, table_mask(16, lambda i: not maj(*[(i >> b) & 1 for b in range(5)]))),
     (16, flip(rand_monotone(16, 30, 4), random.randrange(1 << 16)))])
add([(10, rand_case(10)) for _ in range(60)])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
