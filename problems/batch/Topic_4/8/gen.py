# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(404)
MAXL = 100_000
tests = []

def add(s):
    assert 1 <= len(s) <= MAXL and s.isdigit() and s[0] != '0'
    tests.append(s + "\n")

# samples
add("2026")
add("4321")
add("115")
add("7")
add("1090")
add("12443322")
# hidden (small, brute checks fully)
add("10")
add("1000")
add("99")
add("102")
add("1099")
add("531")
add("199999")
add("989898")
# big
digs = ''.join(random.choice("0123456789") for _ in range(MAXL - 1))
add(random.choice("123456789") + digs)                     # random: pivot near the end
add("9" * MAXL)                                          # all equal -> -1
add("1" + "9" * (MAXL - 2) + "0")                        # pivot is the first digit, answer starts with 9
add(''.join(sorted("123456789" * 10000 + "0" * 10000, reverse=True)))   # descending -> -1
add("2" + "".join(sorted(digs, reverse=True)))            # pivot is the first digit

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
