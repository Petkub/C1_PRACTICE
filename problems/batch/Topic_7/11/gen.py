# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random, string

random.seed(711)
tests = []
AL = string.ascii_lowercase
MAXN = 1_000_000

def add(s, k):
    assert 1 <= k <= len(s) <= MAXN and all(c in AL for c in s)
    tests.append(f"{s}\n{k}\n")

def rnd(n, pool=AL):
    return "".join(random.choice(pool) for _ in range(n))

def noisy(n, k, pool, p):
    base = rnd(k, pool)
    return "".join(base[i % k] if random.random() > p else random.choice(pool) for i in range(n))

# samples
add("abcxbcabd", 3)
add("abba", 2)
add("z", 1)
add("mississippi", 4)
add("aaaa", 4)
# hidden
add("ab", 1)
add("ba", 1)
add("zyxwvutsrqponmlkjihgfedcba", 13)
add(rnd(30, "ab"), 7)
add(noisy(100, 10, "xyz", 0.3), 10)
add(noisy(1000, 37, AL, 0.5), 37)
add(rnd(5000, "zy"), 2)
add(noisy(500_000, 1000, AL, 0.4), 1000)
add(rnd(MAXN), MAXN - 3)
add(rnd(300_000), 1)
add(rnd(300_000, "yz"), 2)
add(noisy(300_000, 3, "abc", 0.6), 3)
add(rnd(299_993, "pq"), 149_999)

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
