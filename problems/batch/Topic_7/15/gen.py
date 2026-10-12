# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random, base64

random.seed(715)
tests = []
PRINT = [chr(c) for c in range(32, 127)]

def enc(m):
    # Base64 exactly as described in the statement
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    bits = "".join(format(ord(c), "08b") for c in m)
    bits += "0" * (-len(bits) % 6)
    out = "".join(alpha[int(bits[i:i + 6], 2)] for i in range(0, len(bits), 6))
    out += "=" * (-len(out) % 4)
    assert out == base64.b64encode(m.encode()).decode()
    return out

def add(texts):
    assert 1 <= len(texts) <= 100
    for m in texts:
        assert 1 <= len(m) <= 3000
        assert all(32 <= ord(c) <= 126 for c in m) and m[0] != " " and m[-1] != " "
    tests.append(f"{len(texts)}\n" + "".join(enc(m) + "\n" for m in texts))

def rnd(n, pool=PRINT):
    s = [random.choice(pool) for _ in range(n)]
    while s[0] == " ":
        s[0] = random.choice(pool)
    while s[-1] == " ":
        s[-1] = random.choice(pool)
    return "".join(s)

# samples
add(["Hi!", "Hi"])
add(["POSN Camp 1"])
add(["a"])
add(["Man", "Ma", "M"])
add(["2 + 3 = 5?", "~/home/user"])
# hidden
add(["~", "}", "!", "0"])
add(["ab", "abc", "abcd", "abcde", "abcdef"])
add(["Hello, World!", "The quick brown fox jumps over the lazy dog.", "C++ is fun; Python too :)"])
add(["".join(PRINT[1:])] + ["~" * k for k in range(1, 10)] + ["?" * k for k in range(1, 10)])
add([rnd(random.randint(1, 20)) for _ in range(100)])
add([rnd(random.randint(1, 300)) for _ in range(100)])
add([rnd(3000) for _ in range(30)])
add([rnd(2999) for _ in range(30)])
add([rnd(2998, "~?>") for _ in range(30)])
add([rnd(random.randint(2990, 3000), "abc ") for _ in range(30)])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
