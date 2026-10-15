# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random, string
from collections import deque

random.seed(1213)
MAXQ = 200_000
tests = []


class Room:
    """the waiting room, used to know who is waiting while generating"""
    def __init__(self):
        self.q = {"U": deque(), "N": deque()}
        self.streak = 0
        self.names = set()

    def arrive(self, name, kind):
        assert name not in self.names
        self.names.add(name)
        self.q[kind].append(name)

    def treat(self):
        u, n = self.q["U"], self.q["N"]
        if not u and not n:
            return None
        if not u or (n and self.streak >= 3):
            self.streak = 0
            x = n.popleft()
        else:
            self.streak += 1
            x = u.popleft()
        self.names.discard(x)
        return x


def add(cmds):
    """cmds: list of (name, kind) for ARRIVE, or None for TREAT"""
    assert 1 <= len(cmds) <= MAXQ and any(c is None for c in cmds)
    room = Room()
    lines = []
    for c in cmds:
        if c is None:
            room.treat()
            lines.append("TREAT")
        else:
            name, kind = c
            assert 1 <= len(name) <= 10 and all(ch in string.ascii_lowercase for ch in name) and kind in "UN"
            room.arrive(name, kind)     # asserts the name is not waiting already
            lines.append(f"ARRIVE {name} {kind}")
    tests.append(f"{len(cmds)}\n" + "\n".join(lines) + "\n")


def rnd(q, p_arrive, p_urgent, lmin, lmax, letters=string.ascii_lowercase):
    room = Room()
    cmds = []
    for _ in range(q - 1):
        name = None
        if random.random() < p_arrive:
            for _ in range(20):
                name = "".join(random.choice(letters) for _ in range(random.randint(lmin, lmax)))
                if name not in room.names:
                    break
            if name in room.names:
                name = None
        if name is not None:
            kind = "U" if random.random() < p_urgent else "N"
            room.arrive(name, kind)
            cmds.append((name, kind))
        else:
            room.treat()
            cmds.append(None)
    cmds.append(None)
    return cmds


A = lambda n, k: (n, k)
T = None
# samples
add([A("nok", "N"), A("dam", "U"), A("fon", "U"), A("ton", "U"), A("mai", "U"), T, T, T, T, T])
add([A("ae", "U"), A("bo", "U"), A("cha", "U"), T, T, T, T, A("pim", "U"), A("joy", "N"), T])
add([T])
add([A("max", "N"), A("ink", "U"), T, T])
add([A("bee", "N"), T, A("bee", "U"), T, T])
add([A("a", "U"), A("b", "U"), A("c", "U"), A("d", "N"), A("e", "U"), T, T, T, T, T, A("d", "U"), T])
# hidden (small)
add([A("x", "N"), A("y", "N"), A("z", "N"), A("w", "U"), T, T, T, T, T])
add([A("u" * 10, "U")] + [T] * 3 + [A("abcdefghij", "N"), A("u" * 10, "U"), T, T])
add(rnd(30, 0.6, 0.7, 1, 1, "abc"))
add(rnd(300, 0.55, 0.8, 1, 2, "abcd"))
add(rnd(3000, 0.5, 0.75, 1, 3))
# large
def code(i, first):
    s = string.ascii_lowercase[first + i % 13]
    i //= 13
    for _ in range(3):
        s += string.ascii_lowercase[i % 26]
        i //= 26
    return s

add(rnd(15_000, 0.5, 0.8, 1, 10))
# a long room first: many normal patients, then urgent ones, then treat until the end
cmds = [A(code(i, 0), "N") for i in range(80_000)] + [A(code(i, 13), "U") for i in range(60_000)]
add(cmds + [T] * (MAXQ - len(cmds)))
add(rnd(20_000, 0.5, 0.95, 3, 3))
add(rnd(10_000, 0.7, 0.5, 2, 5))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
