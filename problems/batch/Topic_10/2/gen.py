import os, random

random.seed(1002)
tests = []

def add(s):
    n = len(s)
    assert 1 <= n <= 100000 and set(s) <= set(".x")
    tests.append(f"{n}\n{s}\n")

def rnd(n, p):
    return "".join("x" if random.random() < p else "." for _ in range(n))

# samples
add(".x..")
add(".xxx.")
add("...")
add("x")
add("." * 10)
add("." * 40)
# hidden
add(".")
add("..")
add("xx.")
add("x.x.x.x.x.x.")
add("..x" * 8)
add(".xx" * 9 + ".")
add(rnd(30, 0.2))
add(rnd(35, 0.1)[:-1] + "x")
add(".xx." * 7)
add("." * 100000)
add(rnd(100000, 0.1))
add(rnd(99999, 0.3)[:-1] + "x")
add("." * 50000 + "xxx" + "." * 49997)
add(rnd(100000, 0.05))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
