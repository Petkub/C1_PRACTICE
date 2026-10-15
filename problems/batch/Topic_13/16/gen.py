# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random, string

random.seed(1316)
ALPHA = string.ascii_lowercase + string.digits
tests = []

def add(names):
    assert 1 <= len(names) <= 100_000
    for s in names:
        assert 1 <= len(s) <= 15 and all(c in ALPHA for c in s)
    tests.append(f"{len(names)}\n" + "\n".join(names) + "\n")

def word(lo, hi, alpha=ALPHA):
    return "".join(random.choice(alpha) for _ in range(random.randint(lo, hi)))

def pool_mix(n, bases, pnum, kmax):
    """requests drawn from bases and from base+number names that collide with generated ones"""
    res = []
    for _ in range(n):
        b = random.choice(bases)
        if random.random() < pnum:
            b = (b + str(random.randint(1, kmax)))[:15]
        res.append(b)
    return res

# samples
add(["nok", "ploy", "nok", "ploy", "nok"])
add(["a", "a", "a1", "a1"])
add(["tom1", "tom", "tom", "tom", "tom1"])
add(["z", "z1", "z", "z1", "z11"])
add(["x"])
add(["007", "007", "0071", "00", "00", "0"])
# hidden (small)
add([word(15, 15)])
add(["b"] * 12 + ["b1"] * 3 + ["b11"] * 2 + ["b"] * 3)
add(["q" + str(i) for i in range(1, 25)] + ["q"] * 30 + ["q2"] * 5)
add(pool_mix(300, ["a", "b", "ab", "a1", "1", "11"], 0.3, 12))
add(pool_mix(3000, [word(1, 3, "abc") for _ in range(30)], 0.35, 40))
# large
add(["a"] * 100_000)
first = ["a" + str(i) for i in range(1, 50_001)]
random.shuffle(first)
add(first + ["a"] * 50_000)
add(pool_mix(100_000, sorted({word(1, 4) for _ in range(3000)}), 0.3, 60))
add(pool_mix(100_000, [word(1, 2, "ab1") for _ in range(10)], 0.4, 300))
names = set()
while len(names) < 40_000:
    names.add(word(1, 15))
names = sorted(names)
add(names + random.sample(names, 10_000))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
