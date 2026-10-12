# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random, string

random.seed(704)
tests = []
AL = string.ascii_lowercase

def add(msgs):
    assert 1 <= len(msgs) <= 100
    for m in msgs:
        assert 1 <= len(m) <= 1000
        assert all(c == " " or c in AL for c in m)
        assert m[0] != " " and m[-1] != " "
    tests.append(f"{len(msgs)}\n" + "".join(m + "\n" for m in msgs))

def rnd(length, pool, pspace=0.15):
    s = [" " if random.random() < pspace else random.choice(pool) for _ in range(length)]
    s[0] = random.choice(pool)
    s[-1] = random.choice(pool)
    return "".join(s)

# samples
add(["hi", "hello world"])
add(["see  you"])
add(["abc", "z"])
add(["posn camp", "mom", "pqrs"])
add(["call me", "ok"])
# hidden
add(["a"])
add([c for c in AL])
add(["a" + " " * 998 + "b", "o" * 1000])
add(["ab" * 500, "s" * 1000, "wxyz" * 250])
add(["this is a test", "aaa bbb ccc", "mn on no", "j k l", "tutu vuvu"])
for _ in range(3):
    add([rnd(random.randint(1, 60), AL) for _ in range(random.randint(20, 100))])
add([rnd(1000, AL) for _ in range(100)])
add([rnd(1000, "abcpqrstuvmno", 0.3) for _ in range(100)])
add([rnd(random.randint(1, 1000), "ghi", 0.4) for _ in range(100)])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
