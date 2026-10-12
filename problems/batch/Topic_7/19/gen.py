# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random, string

random.seed(719)
tests = []
AL = string.ascii_lowercase
MAXN = 1_000_000

def add(s, k):
    assert 1 <= len(s) <= MAXN and all(c in AL for c in s)
    assert 0 <= k < len(s)
    tests.append(f"{s}\n{k}\n")

def rnd(n, pool=AL):
    return "".join(random.choice(pool) for _ in range(n))

# samples
add("banana", 2)
add("abcd", 2)
add("zyx", 0)
add("cbacdcbc", 3)
add("posncamp", 4)
# hidden
add("q", 0)
add("ba", 1)
add("ab", 1)
add("aaaa", 3)
add(rnd(12, "abc"), 5)
add(rnd(200, "ab"), 100)
add(rnd(2000), 1000)
add(rnd(3000, "xyz"), 2999)
add("".join(sorted(rnd(5000))), 2500)
add(AL[::-1] * 100, 1300)
add(rnd(500_000), 250_000)
t = list("".join(sorted(rnd(600_000))))
for _ in range(100):
    t[random.randrange(len(t))] = random.choice(AL)
add("".join(t), 300_000)
add("".join(sorted(rnd(300_000)))[::-1], 150_000)
add("z" * 199_999 + "a" * 100_000, 199_999)
add(rnd(400_000, "ab"), 1000)
add(rnd(200_000, "pq"), 199_000)

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
