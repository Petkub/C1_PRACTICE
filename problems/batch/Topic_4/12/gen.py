# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(412)
F = [0, 1, 2]
while len(F) < 90:
    F.append(F[-1] + F[-2])
tests = []

def value(s):
    return sum(F[i + 1] for i, c in enumerate(reversed(s)) if c == "1")

def add(strs):
    assert 1 <= len(strs) <= 1000
    for s in strs:
        assert 1 <= len(s) <= 80 and set(s) <= {"0", "1"} and "1" in s
    tests.append(f"{len(strs)}\n" + "".join(s + "\n" for s in strs))

def rnd(n, p=0.5):
    s = "".join("1" if random.random() < p else "0" for _ in range(n))
    return s if "1" in s else s[:-1] + "1"

# samples
add(["111", "1001", "11"])
add(["0110", "1111", "10100"])
add(["1"])
add(["0001", "11111111", "00100"])
add(["110110", "101010", "011"])
add(["1" * 20])
# hidden, small values (brute checks)
add([bin(i)[2:] for i in range(1, 301)])
add([rnd(random.randint(1, 12)) for _ in range(200)])
add(["0" * random.randint(0, 60) + bin(random.randint(1, 255))[2:] for _ in range(100)])
add(["1" * k for k in range(1, 18)] + ["10" * k for k in range(1, 9)])
# hidden, big
add(["1" * 80, "1" + "0" * 79, "10" * 40, "01" * 40, "1" * 79 + "0", "0" * 79 + "1"])
add([rnd(80) for _ in range(1000)])
add([rnd(80, 0.9) for _ in range(1000)])
add([rnd(random.randint(1, 80), random.random()) for _ in range(1000)])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
