# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(415)
MAXL, MAXM = 200_000, 10**9
tests = []

def add(s, m):
    assert 1 <= len(s) <= MAXL and set(s) <= set("0123456789") and s[0] != "0"
    assert 1 <= m <= MAXM
    tests.append(f"{s}\n{m}\n")

def rnd(n, alpha="0123456789"):
    return random.choice("123456789") + "".join(random.choice(alpha) for _ in range(n - 1))

# samples
add("1234", 2)
add("100", 10)
add("142857", 7)
add("5", 3)
add("1111", 11)
add("20262026", 1013)
# hidden, small (brute checks)
add("7", 7)
add("98", 1)
add("1000000", 1000000)
add(rnd(30), 3)
add(rnd(500, "0123"), 4)
add("12" * 1000, 12)
add(rnd(3000), 37)
add("9" * 4995, 999_999_999)
# hidden, big
add(rnd(MAXL), 7)
add(rnd(MAXL), 999_999_937)
add("1" + "0" * (MAXL - 1), 2**20)
add("142857" * (MAXL // 6), 7)
add(rnd(MAXL, "05"), 25)

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
