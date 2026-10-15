# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(1307)
MAXN = 200_000
STEP = {"U": (0, 1), "D": (0, -1), "L": (-1, 0), "R": (1, 0)}
tests = []


def add(s):
    assert 1 <= len(s) <= MAXN
    assert all(c in "UDLR" for c in s)
    tests.append(f"{len(s)}\n{s}\n")


def walk(n, weights=(1, 1, 1, 1)):
    return "".join(random.choices("UDLR", weights=weights, k=n))


def spiral(n):
    """square spiral R1 U1 L2 D2 R3 U3 ... cut to n steps: never repeats a cell"""
    out, k = [], 1
    while len(out) < n:
        for d in ("RU" if k % 2 else "LD"):
            out += [d] * k
        k += 1
    return "".join(out[:n])


def snake(n):
    """right runs and up/down runs in turn: x never decreases, so no cell repeats"""
    out = []
    while len(out) < n:
        out += ["R"] * random.randint(1, 3)
        out += [random.choice("UD")] * random.randint(1, 25)
    return "".join(out[:n])


def into_old(s):
    """one more step onto an already visited cell that is not the previous one (if possible)"""
    x = y = 0
    seen = {(0, 0)}
    prev = None
    for d in s:
        prev = (x, y)
        x, y = x + STEP[d][0], y + STEP[d][1]
        seen.add((x, y))
    good = [d for d in "UDLR" if (x + STEP[d][0], y + STEP[d][1]) in seen
            and (x + STEP[d][0], y + STEP[d][1]) != prev]
    return s + (good[0] if good else {"U": "D", "D": "U", "L": "R", "R": "L"}[s[-1]])


# samples
add("RRUULDDD")
add("RRDLLLUUU")
add("UD")
add("L")
add("UURDDLLU")
# hidden (small)
add("D")
add("RL")
add("URDL" * 3)
add(walk(60))
add(into_old(spiral(300)))                           # repeat only at the last step
add(snake(2000))                                     # long, no repeat
add(snake(1500) + "L" * 500)                         # turns back and crosses its own path
add(walk(3000, (1, 1, 1, 3)))
# large
add("R" * MAXN)                                      # straight line, no repeat
add("L" * 100_000 + "D" * 100_000)                   # negative coordinates only
add(spiral(MAXN))                                    # long spiral, no repeat
add(into_old(spiral(MAXN - 1)))                      # spiral, repeat at step N
h = (MAXN - 2) // 2
add("R" + "U" * h + "L" + "D" * h)                   # two columns, back to the start at step N
add("R" + "U" * h + "L" + "D" * (h - 1))             # same but stops one cell short
add("R" + "U" * 100_000 + "L")                       # (1, 0) and (0, 100000)
add("R" * 10_737 + "U" * 156_559)                    # far corner, no repeat
add("R" * 4_295 + "D" * 32_704)                      # far corner, no repeat
add(walk(MAXN))
add(walk(MAXN, (1, 1, 1, 6)))
add("U" * 50_000 + walk(MAXN - 50_000))              # first steps straight, then random

for t in tests:
    assert t.endswith("\n") and " " not in t
assert sum(len(t) for t in tests) < 3_000_000
print("total bytes", sum(len(t) for t in tests))
os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
