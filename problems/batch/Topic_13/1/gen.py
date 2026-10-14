# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random, string

random.seed(1301)
MAXN = 100_000
tests = []


def ok_name(s):
    return 1 <= len(s) <= 20 and all(c in string.ascii_lowercase for c in s)


def add(entries, queries):
    assert 1 <= len(entries) <= MAXN and 1 <= len(queries) <= MAXN
    for name, num in entries:
        assert ok_name(name)
        assert len(num) == 10 and num.isdigit() and num[0] == "0"
    for name in queries:
        assert ok_name(name)
    tests.append(f"{len(entries)}\n" + "".join(f"{a} {b}\n" for a, b in entries)
                 + f"{len(queries)}\n" + "".join(q + "\n" for q in queries))


def phone():
    return "0" + "".join(random.choice("0123456789") for _ in range(9))


def word(lo, hi, letters=string.ascii_lowercase):
    return "".join(random.choice(letters) for _ in range(random.randint(lo, hi)))


# samples
add([("ploy", "0812345678"), ("bank", "0899990000"), ("bank", "0623456789")],
    ["bank", "ploy", "nat"])
add([("tan", "0811111111"), ("tan", "0822222222")], ["ta", "tan", "tann"])
add([("abcdefghijklmnopqrst", "0912345678"), ("abcdefghijklmnopqrsz", "0987654321")],
    ["abcdefghijklmnopqrs", "abcdefghijklmnopqrsz"])
add([("a", "0000000000")], ["b", "a"])
add([("mew", "0811112222"), ("nok", "0811112222"), ("mew", "0899999999")], ["nok", "mew"])
# hidden (small)
add([("z" * 20, "0999999999")], ["z" * 20])
add([(word(1, 3, "ab"), phone()) for _ in range(30)], [word(1, 3, "ab") for _ in range(30)])
add([(word(1, 4, "abc"), phone()) for _ in range(300)], [word(1, 4, "abc") for _ in range(300)])
# long names that share long prefixes, queries include their prefixes
base = "k" * 17
names = [base + word(1, 3, "xyz") for _ in range(2000)]
add([(s, phone()) for s in names], [random.choice(names)[:random.randint(17, 20)] for _ in range(2000)])
# one person changes number again and again
add([("som", phone()) for _ in range(3000)], [random.choice(["som", "so", "somm", "mos"]) for _ in range(3000)])
add([(word(1, 2, "pq"), phone()) for _ in range(1000)], [word(1, 3, "pqr") for _ in range(1000)])
# large: many repeated short names, queries of length 1..3 (only length-2 names exist)
add([(word(2, 2), phone()) for _ in range(MAXN)], [word(1, 3) for _ in range(MAXN)])
# large: distinct names, many queries, half of them absent
names = set()
while len(names) < 20_000:
    names.add(word(4, 6))
names = sorted(names)
random.shuffle(names)
qs = [random.choice(names) if random.random() < 0.5 else word(4, 6) for _ in range(50_000)]
add([(s, phone()) for s in names], qs)
# medium, every name written twice in a row and again later
names = [word(3, 8) for _ in range(4000)]
ent = []
for s in names:
    ent += [(s, phone()), (s, phone())]
for s in random.sample(names, 2000):
    ent.append((s, phone()))
add(ent, [random.choice(names) for _ in range(6000)])

assert sum(len(t) for t in tests) < 2_950_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
