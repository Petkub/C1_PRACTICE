# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(405)
MAXL = 200_000
W = [7, 3, 1]
tests = []

def S(c):
    return sum(W[i % 3] * int(x) for i, x in enumerate(c))

def add(c):
    assert 2 <= len(c) <= MAXL and all(ch in "0123456789" for ch in c)
    tests.append(c + "\n")

def rnd(n, alphabet="0123456789"):
    return ''.join(random.choice(alphabet) for _ in range(n))

def make_valid(n):
    c = list(rnd(n))
    # fix the last digit so that S % 10 == 0 (last weight is 7, 3 or 1, all invertible mod 10)
    c[-1] = '0'
    s = S(c)
    w = W[(n - 1) % 3]
    for d in range(10):
        if (s + w * d) % 10 == 0:
            c[-1] = str(d)
    assert S(c) % 10 == 0
    return ''.join(c)

def swapped(c, i):
    c = list(c)
    c[i], c[i + 1] = c[i + 1], c[i]
    return ''.join(c)

# samples
add("2026051")
add("2620051")
add("4852391")
add("1112223")
add("55")
add("31415926535")
# hidden, small
add("00")
add("10")
add("9999999")
add(swapped(make_valid(12), 0))
add(swapped(make_valid(30), 28))
for n in (5, 40, 200, 2000):
    add(rnd(n))
# big
add(rnd(MAXL))
add(make_valid(MAXL))
add(swapped(make_valid(MAXL), 77_777))
add(rnd(MAXL, "09"))
add("1" + "0" * (MAXL - 1))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
