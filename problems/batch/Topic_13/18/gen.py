# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(1318)
MAXT = 10**9
tests = []

def add(cmds):
    n = len(cmds)
    assert 1 <= n <= 100_000
    books = 0
    lines = [str(n)]
    for c in cmds:
        if c[0] == "BOOK":
            s, e = c[1], c[2]
            assert 0 <= s < e <= MAXT
            books += 1
            lines.append(f"BOOK {s} {e}")
        else:
            assert c[0] == "CANCEL" and 1 <= c[1] <= books
            lines.append(f"CANCEL {c[1]}")
    assert books >= 1
    tests.append("\n".join(lines) + "\n")

def B(s, e):
    return ("BOOK", s, e)

def C(k):
    return ("CANCEL", k)

def rnd(n, tmax, maxlen, pcancel, recent=None):
    """random commands; cancels pick any earlier booking, or one of the last `recent` ones"""
    cmds, books = [], 0
    for _ in range(n):
        if books > 0 and random.random() < pcancel:
            lo = 1 if recent is None else max(1, books - recent)
            cmds.append(C(random.randint(lo, books)))
        else:
            s = random.randint(0, tmax - 1)
            e = min(tmax, s + random.randint(1, maxlen))
            cmds.append(B(s, e))
            books += 1
    return cmds

# samples
add([B(1, 3), B(3, 5), B(2, 4), C(1), B(2, 3), B(0, 2)])
add([B(10, 20), B(10, 20), C(2), B(15, 16), C(1), B(15, 16)])
add([B(0, MAXT), C(1), B(5, 6), C(1), B(0, 10)])
add([B(0, 1)])
add([B(5, 10), B(1, 20), B(6, 7), B(10, 11), B(4, 5), B(4, 6)])
add([B(0, 5), B(10, 15), B(5, 10), C(3), B(4, 11), B(6, 9)])
# hidden (small)
add([B(MAXT - 1, MAXT), B(0, MAXT), C(1), C(1), B(0, MAXT), B(0, 1), C(4), B(0, 1)])
add(rnd(40, 20, 4, 0.3))
# few distinct ranges: rejected bookings with the same range as an accepted one get cancelled
cmds, books = [], 0
for _ in range(400):
    if books and random.random() < 0.4:
        cmds.append(C(random.randint(1, books)))
    else:
        s = random.randint(0, 6)
        cmds.append(B(s, s + random.randint(1, 3)))
        books += 1
add(cmds)
add(rnd(2000, 3000, 40, 0.25, recent=60))
add(rnd(3000, MAXT, 10**7, 0.3))
# large
slots = list(range(60_000))
random.shuffle(slots)
cmds = [B(t, t + 1) for t in slots]                     # every unit slot is booked
books = len(cmds)
for _ in range(40_000):
    if random.random() < 0.5:
        cmds.append(C(random.randint(1, books)))
    else:
        t = random.randint(0, 60_000)
        cmds.append(B(t, t + random.randint(1, 2)))
        books += 1
add(cmds)
add(rnd(30_000, MAXT, 2 * 10**5, 0.35, recent=5000))
add(rnd(15_000, 50_000, 30, 0.45, recent=200))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
