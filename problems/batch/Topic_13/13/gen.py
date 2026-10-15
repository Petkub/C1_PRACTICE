# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(1313)
MAXQ, MAXX = 200_000, 10**9
tests = []


def add(cmds):
    """cmds: list of strings "PUT x" / "TAKE x" / "COUNT x" / "MAX" / "MIN" """
    assert 1 <= len(cmds) <= MAXQ
    asks = 0
    for c in cmds:
        w = c.split()
        if w[0] in ("PUT", "TAKE", "COUNT"):
            assert len(w) == 2 and 1 <= int(w[1]) <= MAXX and str(int(w[1])) == w[1]
        else:
            assert w[0] in ("MAX", "MIN") and len(w) == 1
        asks += w[0] in ("MAX", "MIN", "COUNT")
    assert asks >= 1
    tests.append(f"{len(cmds)}\n" + "\n".join(cmds) + "\n")


def rnd(q, lo, hi, w_put, w_take, w_ask, first_puts=0):
    """random commands; TAKE / COUNT hit a size in the freezer most of the time"""
    inside = []           # sizes in the freezer (with repeats), only used to pick likely hits
    cmds = []
    for _ in range(first_puts):
        x = random.randint(lo, hi)
        inside.append(x)
        cmds.append(f"PUT {x}")
    while len(cmds) < q:
        r = random.random() * (w_put + w_take + w_ask)
        if r < w_put:
            x = random.randint(lo, hi)
            inside.append(x)
            cmds.append(f"PUT {x}")
        else:
            if inside and random.random() < 0.8:
                j = random.randrange(len(inside))
                x = inside[j]
            else:
                j, x = -1, random.randint(lo, hi)
            if r < w_put + w_take:
                cmds.append(f"TAKE {x}")
                if j >= 0:
                    inside[j] = inside[-1]
                    inside.pop()
                elif x in inside:
                    inside.remove(x)
            else:
                cmds.append(random.choice(["MAX", "MIN", f"COUNT {x}"]))
    if not any(c.split()[0] in ("MAX", "MIN", "COUNT") for c in cmds):
        cmds[-1] = "MAX"
    return cmds


# samples
add(["PUT 5", "PUT 3", "PUT 5", "MAX", "TAKE 5", "COUNT 5", "TAKE 5", "MAX"])
add(["MIN", "PUT 7", "TAKE 2", "COUNT 2", "MIN", "TAKE 7", "MAX"])
add(["PUT 1000000000", "PUT 1", "MAX", "MIN", "COUNT 1000000000"])
add(["PUT 4", "PUT 9", "PUT 4", "COUNT 4", "TAKE 4", "TAKE 4", "MIN"])
add(["COUNT 3"])
# hidden (small)
add(["PUT 5", "COUNT 100", "MAX", "COUNT 1", "MIN", "TAKE 100", "TAKE 1", "MAX", "MIN"])
add(["PUT 5", "PUT 5", "TAKE 5", "TAKE 5", "TAKE 5", "MAX", "MIN", "COUNT 5", "PUT 6", "MIN", "MAX"])
add(rnd(60, 1, 10, 4, 3, 3))
add(rnd(400, 1, 30, 3, 3, 4))
add(rnd(2000, 1, 1000, 4, 2, 4))
add(rnd(5000, 1, MAXX, 3, 3, 4))
add(rnd(3000, MAXX - 5, MAXX, 3, 3, 4))
# large
cmds = [f"PUT {x}" for x in range(100_000, 0, -1)]            # many cups (each one the new smallest), then questions
for i in range(100_000):
    cmds.append(random.choice(["MAX", "MIN"]) if i % 50 else f"COUNT {random.randint(1, 100_000)}")
add(cmds)
add(rnd(30_000, 1, MAXX, 4, 3, 3))
add(rnd(40_000, 1, 50, 3, 3, 4))                               # few sizes, many repeats
cmds = [f"PUT {x}" for x in range(1, 20_001)]                  # sizes taken away from both ends
for i in range(10_000):
    cmds += [f"TAKE {i + 1}", "MIN", f"TAKE {20_000 - i}", "MAX"]
add(cmds + ["MAX", "MIN", "COUNT 1"])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
