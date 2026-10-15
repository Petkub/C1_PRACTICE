# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(1215)
MAXQ, MAXW = 300_000, 10**9
tests = []


def add(cmds):
    """cmds: list of ints (PUSH w), "P" (POP) or "M" (MIN)"""
    assert 1 <= len(cmds) <= MAXQ and "M" in cmds
    lines = []
    for c in cmds:
        if c == "P":
            lines.append("POP")
        elif c == "M":
            lines.append("MIN")
        else:
            assert 1 <= c <= MAXW
            lines.append(f"PUSH {c}")
    tests.append(f"{len(cmds)}\n" + "\n".join(lines) + "\n")


def rnd(q, pp, ppop, lo, hi):
    cmds = []
    for _ in range(q - 1):
        r = random.random()
        if r < pp:
            cmds.append(random.randint(lo, hi))
        elif r < pp + ppop:
            cmds.append("P")
        else:
            cmds.append("M")
    return cmds + ["M"]


P, M = "P", "M"
# samples
add([5, 3, M, 7, M, P, P, M])
add([M, P, 4, 4, P, M])
add([10**9, M])
add([2, 1, 3, P, P, M, P, M])
add([8, P, P, 9, M])
# hidden (small)
add([M])
add([1, 1, 1, P, M, P, M, P, M])
add([3, 2, 1, 1, 2, 3, M, P, M, P, M, P, M, P, M, P, M, P, M])
add(rnd(50, 0.45, 0.25, 1, 5))
add(rnd(2000, 0.4, 0.3, 1, 30))
add(rnd(5000, 0.5, 0.2, 1, MAXW))
# large
# a tall pile first, then only MIN
add([random.randint(1, 9) for _ in range(100_000)] + [M] * 200_000)
add(rnd(70_000, 0.4, 0.25, 1, MAXW))
# sawtooth: lighter boxes on top, removed again
cmds = []
while len(cmds) < 40_000:
    k = random.randint(1, 40)
    cmds += [random.randint(1, 99) for _ in range(k)] + [M]
    cmds += [P] * random.randint(0, k) + [M]
add(cmds[:40_000] + [M])
cmds = []
w = 99_999
while len(cmds) < 30_000:
    cmds += [w, M]
    w -= random.randint(0, 3)
add(cmds + [P, M] * 10_000)

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
