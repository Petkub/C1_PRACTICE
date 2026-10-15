# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(1203)
L = 200_000
LET = "abcdefghijklmnopqrstuvwxyz"
tests = []

def add(s):
    assert 1 <= len(s) <= L
    assert all("a" <= c <= "z" for c in s)
    tests.append(s + "\n")

def rnd(n, alpha):
    return "".join(random.choice(alpha) for _ in range(n))

def reduced(n, alpha):
    # a random string with no two equal neighbours
    out = [random.choice(alpha)]
    while len(out) < n:
        c = random.choice(alpha)
        if c != out[-1]:
            out.append(c)
    return "".join(out)

def vanish(n, alpha):
    # iterative version: build by pushing letters and matching them with a stack
    st, out = [], []
    while len(out) + len(st) < n:
        if st and (random.random() < 0.5 or len(out) + len(st) + 2 > n):
            out.append(st.pop())
        else:
            c = random.choice(alpha)
            st.append(c)
            out.append(c)
    while st:
        out.append(st.pop())
    return "".join(out)

def mix(core, n, alpha):
    # core letters with vanishing blocks inserted between them
    out = []
    left = n - len(core)
    for c in core:
        out.append(c)
        if left >= 2 and random.random() < 0.5:
            k = 2 * random.randint(1, max(1, min(left // 2, 20)))
            out.append(vanish(k, alpha))
            left -= k
    return "".join(out)

# samples
add("abbaca")
add("aabccbdd")
add("abc")
add("aaa")
add("z")
add("abccbaab")
# hidden
add("qq")
add("abab")
add(rnd(30, "ab"))
add(mix(reduced(20, "abc"), 120, "abc"))
add(rnd(2000, "abc"))
add(vanish(2000, LET))
add(rnd(1999, LET))
# max size
s = "".join(LET[i % 26] for i in range(L // 2))
add(s + s[::-1])                                           # nested, EMPTY
add("a" * L)
add("a" * (L - 1))
add(reduced(L, "ab"))                                      # nothing to delete
add(rnd(L, "ab"))
add(mix(reduced(1000, LET), L, "xyz"))
add(vanish(L, "ab"))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
