# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random, re

random.seed(712)
tests = []

def ok(s):
    return re.fullmatch(r"0|-?[1-9][0-9]{0,99}", s) is not None

def add(nums):
    assert 1 <= len(nums) <= 20_000
    for s in nums:
        assert ok(s), s
    tests.append(f"{len(nums)}\n" + "".join(s + "\n" for s in nums))

def num(maxd, pneg=0.5):
    d = random.randint(1, maxd)
    s = str(random.randint(1, 9)) + "".join(random.choice("0123456789") for _ in range(d - 1))
    if random.random() < pneg:
        s = "-" + s
    return s

def near(s):
    # a number with the same length and many equal leading digits
    neg = s.startswith("-")
    d = list(s.lstrip("-"))
    i = random.randrange(len(d))
    d[i] = random.choice("123456789" if i == 0 else "0123456789")
    return ("-" if neg else "") + "".join(d)

# samples
add(["10", "-3", "9", "0", "-12"])
add(["-1", "-10", "-2", "100", "20", "3"])
add(["0"])
add(["7", "-7", "7"])
add(["123456789012345678901234567890", "-99999999999999999999", "123456789012345678901234567891", "5"])
# hidden
add(["-" + "9" * 100, "9" * 100, "0", "1" + "0" * 99, "-1" + "0" * 99, "-1", "1"])
add(["0"] * 10 + ["-1"] * 5 + ["1"] * 5)
add([str(x) for x in range(-50, 51)][::-1])
add([str(random.randint(-10**18, 10**18)) for _ in range(1000)] + ["9223372036854775807", "-9223372036854775808", "9223372036854775808", "-9223372036854775809", "18446744073709551616"])
add([num(3) for _ in range(500)])
base = [num(60) for _ in range(50)]
add([near(random.choice(base)) for _ in range(2000)] + base)
add([num(100) for _ in range(20_000)])
add([num(20, 0.3) for _ in range(20_000)])
b = num(100, 0)
add([near(b) for _ in range(3000)] + ["-" + near(b) for _ in range(3000)])
add([str(random.choice([-1, 1]) * random.randint(1, 10**9)) for _ in range(5000)])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
