# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(1202)
L = 100_000
LET = "abcdefghijklmnopqrstuvwxyz"
tests = []

def add(a, b):
    for s in (a, b):
        assert 1 <= len(s) <= L
        assert all(c == "#" or "a" <= c <= "z" for c in s)
    tests.append(a + "\n" + b + "\n")

def rnd(n, phash, alpha=LET):
    return "".join("#" if random.random() < phash else random.choice(alpha) for _ in range(n))

def keys_for(target, noise, maxlen, alpha=LET):
    # keystrokes whose final text is target: random detours that are deleted again
    out = []
    if random.random() < 0.5:
        out.append("#" * random.randint(1, 3))
    for c in target:
        if random.random() < noise:
            k = random.randint(1, 3)
            out.append("".join(random.choice(alpha) for _ in range(k)) + "#" * k)
        out.append(c)
    s = "".join(out)
    assert len(s) <= maxlen
    return s

# samples
add("pas#sz#", "pass#")
add("#a#b", "a#")
add("abc", "acb")
add("a##", "###b#")
add("ab#cd##e", "ae")
add("zz#z", "zzz#z")
# hidden
add("#", "a")
add("q", "q")
add("x#", "#")
add("ab", "ab#")
add(rnd(40, 0.4, "ab"), rnd(40, 0.4, "ab"))
t = "".join(random.choice(LET) for _ in range(300))
add(keys_for(t, 0.5, L), keys_for(t, 0.5, L))
t = "".join(random.choice("xy") for _ in range(800))
add(keys_for(t, 0.3, L, "xy"), keys_for(t[:-1] + ("x" if t[-1] == "y" else "y"), 0.3, L, "xy"))
add(rnd(2000, 0.45), rnd(1999, 0.45))
# max size
add("a" * 50_000 + "#" * 50_000, "#" * 50_000 + "b" * 50_000)
add("#" * L, "z" * L)
t = "".join(random.choice(LET) for _ in range(25_000))
a, b = keys_for(t, 0.6, L), keys_for(t, 0.6, L)
add(a, b)
t = "".join(random.choice("ab") for _ in range(35_000))
a = keys_for(t, 0.4, L, "ab")
b = keys_for(t[:17_000] + ("b" if t[17_000] == "a" else "a") + t[17_001:], 0.4, L, "ab")
add(a, b)
add(rnd(L, 0.49, "ab"), rnd(L, 0.3))
add("k" * L, "k" * (L - 1) + "#")

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
