# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random, string

random.seed(703)
tests = []
PRINT = [chr(c) for c in range(32, 127)]
NONLET = [c for c in PRINT if not c.isalpha()]

def add(lines):
    assert 1 <= len(lines) <= 100
    for l in lines:
        assert 1 <= len(l) <= 1000
        assert all(32 <= ord(c) <= 126 for c in l)
        assert l[0] != " " and l[-1] != " "
        assert any(c.isalpha() for c in l)
    tests.append(f"{len(lines)}\n" + "".join(l + "\n" for l in lines))

def is_pal(l):
    s = [c.lower() for c in l if c.isalpha()]
    return s == s[::-1]

def decorate(letters, junk=0.3):
    # random case, insert non-letters between letters
    out = []
    for ch in letters:
        while random.random() < junk:
            out.append(random.choice(NONLET))
        out.append(ch.upper() if random.random() < 0.5 else ch)
    while random.random() < junk:
        out.append(random.choice(NONLET))
    s = "".join(out).strip(" ")
    return s

def pal_letters(n, alpha=string.ascii_lowercase):
    h = [random.choice(alpha) for _ in range(n // 2)]
    m = [random.choice(alpha)] if n % 2 else []
    return "".join(h + m + h[::-1])

def fit(s):
    return s[:1000].strip(" ") if len(s) > 1000 else s

# samples
add(["A man, a plan, a canal: Panama!", "Hello, olleh", "abc ab"])
add(["a1b", "A 2 B"])
add(["Was it a car or a cat I saw?"])
add(["x", "Xx", "No lemon, no melon", "Step on no pets!", "Top spot? No."])
add(["Madam, I'm Adam.", "Race car", "Race cars", "12321 a"])
# hidden
add(["a", "Z", "aB", "Ab", "ab", "1a1", "a 1 2 3 b", "?A", "A?"])
lines = []
for _ in range(100):
    n = random.randint(1, 40)
    p = pal_letters(n, "ab")
    if random.random() < 0.5 and n >= 2:
        i = random.randrange(n)
        p = p[:i] + ("a" if p[i] == "b" else "b") + p[i + 1:]
    lines.append(decorate(p))
add(lines)
for junk in (0.0, 0.5, 0.8):
    lines = []
    for _ in range(100):
        n = random.randint(1, 300)
        p = pal_letters(n, random.choice(["ab", "abc", string.ascii_lowercase]))
        if random.random() < 0.5 and n >= 2:
            i = random.randrange(n // 2)          # break near the middle or edge
            if random.random() < 0.5:
                i = n // 2 - 1
            j = n - 1 - i
            if i != j:
                p = p[:i] + ("z" if p[i] != "z" else "y") + p[i + 1:]
        lines.append(fit(decorate(p, junk)))
    add(lines)
# max length lines
lines = []
for k in range(100):
    n = random.choice([999, 1000, 500, 1])
    p = pal_letters(n, "ab")
    if k % 2:
        p = p[:-1] + ("a" if p[-1] == "b" else "b")
    lines.append(fit(decorate(p, 0.0)))
add(lines)
# long line mostly junk
lines = []
for k in range(100):
    core = random.choice(["ab", "aa", "a", "aba", "abA"])
    s = "".join(random.choice(NONLET) for _ in range(400)).strip(" ") or "."
    s = s + core + s[::-1]
    s = s.strip(" ")
    lines.append(fit(s))
add(lines)
# letters near spaces and case only differences
add(["AbBa", "AbbA", "a b B A", "Ab ba X", "aaa aaA AAA", "zZ zZ z", "q W e R t y T r E w Q"])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
