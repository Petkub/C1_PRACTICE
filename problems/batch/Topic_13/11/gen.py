# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random
from bisect import bisect_right

random.seed(1311)
MAXR, MAXQ = 10**9, 100_000
tests = []


class Hotel:
    """free rooms as sorted disjoint ranges; also a list of occupied rooms to pick OUT from"""
    def __init__(self, R):
        self.R = R
        self.st, self.en = [1], [R]
        self.occ, self.pos = [], {}

    def take(self, r):
        i = bisect_right(self.st, r) - 1
        if i >= 0 and self.en[i] >= r:
            s, e = self.st[i], self.en[i]
            room = r
        else:
            i += 1
            if i == len(self.st):
                return None
            s, e = self.st[i], self.en[i]
            room = s
        del self.st[i], self.en[i]
        if room < e:
            self.st.insert(i, room + 1); self.en.insert(i, e)
        if s < room:
            self.st.insert(i, s); self.en.insert(i, room - 1)
        self.pos[room] = len(self.occ)
        self.occ.append(room)
        return room

    def free(self, x):
        assert x in self.pos
        j = self.pos.pop(x)
        last = self.occ.pop()
        if last != x:
            self.occ[j] = last
            self.pos[last] = j
        i = bisect_right(self.st, x)          # first range starting after x
        l, r = x, x
        if i < len(self.st) and self.st[i] == x + 1:
            r = self.en[i]
            del self.st[i], self.en[i]
        if i > 0 and self.en[i - 1] == x - 1:
            l = self.st[i - 1]
            del self.st[i - 1], self.en[i - 1]
            i -= 1
        self.st.insert(i, l); self.en.insert(i, r)


def add(R, cmds):
    """cmds: list of ("IN", r) / ("OUT", x); checked by simulation"""
    assert 1 <= R <= MAXR and 1 <= len(cmds) <= MAXQ
    assert any(c == "IN" for c, _ in cmds)
    h = Hotel(R)
    for c, v in cmds:
        assert 1 <= v <= R
        if c == "IN":
            h.take(v)
        else:
            assert c == "OUT"
            h.free(v)       # asserts the room is occupied
    tests.append(f"{R} {len(cmds)}\n" + "".join(f"{c} {v}\n" for c, v in cmds))


def rnd(R, q, p_in, rlo=1, rhi=None):
    """random IN r (r in [rlo, rhi]) / OUT of a random occupied room"""
    rhi = R if rhi is None else rhi
    h = Hotel(R)
    cmds = []
    for _ in range(q):
        if h.occ and random.random() >= p_in:
            x = random.choice(h.occ)
            h.free(x)
            cmds.append(("OUT", x))
        else:
            r = random.randint(rlo, rhi)
            h.take(r)
            cmds.append(("IN", r))
    return cmds


def I(*rs):
    return [("IN", r) for r in rs]


def O(*xs):
    return [("OUT", x) for x in xs]


# samples
add(3, I(2, 2, 2, 1) + O(2) + I(2))
add(MAXR, I(999_999_999, 999_999_999, 999_999_999) + O(MAXR) + I(999_999_999))
add(1, I(1, 1) + O(1) + I(1))
add(6, I(1, 1, 1) + O(2) + I(1, 1))
add(10, I(7, 3, 7) + O(7) + I(6))
# hidden (small)
add(1, I(1))
add(2, I(2, 2, 1, 1) + O(2) + I(1) + O(1) + I(1, 2))
add(10, rnd(10, 50, 0.65))
add(50, rnd(50, 300, 0.6, 1, 10))
add(1000, rnd(1000, 5000, 0.55, 1, 300))
add(100, rnd(100, 2000, 0.8))                      # many FULL
add(MAXR, rnd(MAXR, 3000, 0.6, MAXR - 2000, MAXR))  # near the last room, some FULL
# large
add(MAXR, I(*([1] * MAXQ)))                        # one long run of occupied rooms
cmds = I(*([1] * 50_000))                         # rooms 1..50000 occupied
for _ in range(25_000):                            # free a room, the next guest (IN 1) takes it back
    cmds += O(random.randint(20_000, 50_000)) + I(1)
add(MAXR, cmds)
add(MAXR, rnd(MAXR, 20_000, 0.7, MAXR - 12_000, MAXR))
add(100_000, rnd(100_000, 40_000, 0.6, 1, 100_000))
add(30_000, rnd(30_000, 60_000, 0.6, 1, 3_000))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
