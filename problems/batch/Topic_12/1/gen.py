# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(1201)
V = 10**9
tests = []

def add(cmds):
    q = len(cmds)
    assert 1 <= q <= 100_000
    for c in cmds:
        p = c.split()
        assert p[0] in ("PUSH", "POP", "TOP")
        if p[0] == "PUSH":
            assert len(p) == 2 and 1 <= int(p[1]) <= V and str(int(p[1])) == p[1]
        else:
            assert len(p) == 1
    tests.append(f"{q}\n" + "".join(c + "\n" for c in cmds))

def rnd(q, ppush, ptop, lo, hi):
    cmds = []
    for _ in range(q):
        r = random.random()
        if r < ppush:
            cmds.append(f"PUSH {random.randint(lo, hi)}")
        elif r < ppush + ptop:
            cmds.append("TOP")
        else:
            cmds.append("POP")
    return cmds

# samples
add(["PUSH 5", "PUSH 8", "TOP", "PUSH 3", "POP", "PUSH 1", "TOP"])
add(["POP", "PUSH 4", "POP", "POP", "TOP"])
add(["PUSH 1000000000", "PUSH 7", "PUSH 7"])
add(["TOP"])
add(["PUSH 2", "POP", "PUSH 6", "PUSH 2", "TOP", "POP", "PUSH 9"])
# hidden
add(["POP"])
add(["PUSH 1"])
add(["PUSH 3", "PUSH 3", "POP", "POP", "POP", "PUSH 3", "TOP"])
add(rnd(30, 0.5, 0.2, 1, 9))
add(rnd(500, 0.4, 0.2, 1, 50))           # often empty
add(rnd(2000, 0.6, 0.2, 1, V))
add(rnd(2000, 0.34, 0.33, 1, 3))
# pushes then pops past the bottom, then a few more
add([f"PUSH {i}" for i in range(1, 1001)] + ["POP"] * 1003 + ["TOP", "PUSH 77"])
# max size
add(rnd(100_000, 0.6, 0.15, 1, V))
add([f"PUSH {random.randint(1, 9)}" for _ in range(99_999)] + ["TOP"])
cmds = [f"PUSH {random.randint(1, 9)}" for _ in range(50_000)] + ["POP"] * 50_000
add(cmds)
cmds = []
for _ in range(20_000):
    cmds += ["POP", "TOP", f"PUSH {random.randint(1, 999)}", "TOP"]
add(cmds)

assert sum(len(t) for t in tests) < 2_900_000
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
