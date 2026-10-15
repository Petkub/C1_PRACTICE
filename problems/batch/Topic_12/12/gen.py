# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random
from collections import deque

random.seed(1212)
MAXID = 10**6
tests = []


class Line:
    """the canteen line, used to know who is in the line while generating"""
    def __init__(self, groups):
        self.grp = {}
        for g, mem in enumerate(groups, 1):
            for x in mem:
                self.grp[x] = g
        self.blocks = deque()
        self.members = {}
        self.inside = set()

    def come(self, x):
        assert x not in self.inside
        self.inside.add(x)
        g = self.grp.get(x, -x)
        if g not in self.members or not self.members[g]:
            self.members[g] = deque()
            self.blocks.append(g)
        self.members[g].append(x)

    def serve(self):
        if not self.blocks:
            return None
        g = self.blocks[0]
        x = self.members[g].popleft()
        if not self.members[g]:
            self.blocks.popleft()
        self.inside.discard(x)
        return x


def add(groups, cmds):
    t = len(groups)
    assert 1 <= t <= 1000 and all(len(g) >= 1 for g in groups)
    ids = [x for g in groups for x in g]
    assert len(ids) <= 50_000 and len(set(ids)) == len(ids) and all(1 <= x <= MAXID for x in ids)
    assert 1 <= len(cmds) <= 200_000 and any(c is None for c in cmds)
    line = Line(groups)
    out = []
    for c in cmds:
        if c is None:
            line.serve()
            out.append("OUT")
        else:
            assert 1 <= c <= MAXID
            line.come(c)          # asserts c is not in the line
            out.append(f"IN {c}")
    s = f"{t}\n" + "".join(f"{len(g)} " + " ".join(map(str, g)) + "\n" for g in groups)
    s += f"{len(cmds)}\n" + "\n".join(out) + "\n"
    tests.append(s)


def make_groups(t, total, idmax):
    ids = random.sample(range(1, idmax + 1), total)
    cuts = sorted(random.sample(range(1, total), t - 1))
    return [ids[a:b] for a, b in zip([0] + cuts, cuts + [total])]


def rnd_cmds(groups, extra, q, p_in):
    """random commands; persons = all group members + `extra` unlisted persons"""
    listed = set(x for g in groups for x in g)
    pool = [x for g in groups for x in g]
    taken = set(pool)
    while len(pool) < len(listed) + extra:
        x = random.randint(1, max(2 * (len(listed) + extra), 50))
        if x not in taken:
            taken.add(x)
            pool.append(x)
    line = Line(groups)
    waiting = pool[:]          # persons not in the line
    cmds = []
    for _ in range(q - 1):
        if waiting and random.random() < p_in:
            i = random.randrange(len(waiting))
            x = waiting[i]
            waiting[i] = waiting[-1]
            waiting.pop()
            line.come(x)
            cmds.append(x)
        else:
            x = line.serve()
            if x is not None:
                waiting.append(x)
            cmds.append(None)
    cmds.append(None)
    return cmds


# samples
add([[1, 2]], [1, 3, None, 2, None, None])
add([[7, 8]], [7, 9, 8, None, None, None])
add([[5]], [None, 5, None])
add([[9, 3]], [9, None, None])
add([[2, 6]], [6, 4, 2, None, None])
# hidden (small)
add([[1]], [None, None, 1, None, 1, None])
add([[1000000, 999999], [1]], [2, 999999, 1, 1000000, None, None, None, None, None])
g = make_groups(3, 10, 20)
add(g, rnd_cmds(g, 5, 40, 0.6))
g = make_groups(10, 60, 200)
add(g, rnd_cmds(g, 30, 400, 0.55))
g = make_groups(50, 1000, MAXID)
add(g, rnd_cmds(g, 500, 3000, 0.5))
g = make_groups(1, 1000, 5000)
add(g, rnd_cmds(g, 1000, 5000, 0.6))
# large
g = make_groups(1000, 20_000, MAXID)
add(g, rnd_cmds(g, 20_000, 40_000, 0.52))
g = make_groups(1000, 50_000, 60_000)
add(g, rnd_cmds(g, 0, 50_000, 0.7))
# a long line where every newcomer has to stand near the front, then everyone is served
g = make_groups(1000, 50_000, 99_999)
first = [grp[0] for grp in g]
rest = [x for grp in g for x in grp[1:]]
random.shuffle(rest)
listed = set(x for grp in g for x in grp)
lone = [x for x in range(1, 100_000) if x not in listed][:49_000]
random.shuffle(lone)
add(g, first + lone + rest + [None] * (200_000 - len(first) - len(lone) - len(rest)))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
