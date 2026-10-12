# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(819)
tests = []

def tight(p):
    return all("#" in row for row in p) and all(any(row[j] == "#" for row in p) for j in range(len(p[0])))

def add(W, H, pieces):
    assert 1 <= W <= 30 and 1 <= H <= 1000 and 1 <= len(pieces) <= 10000
    lines = [f"{W} {H} {len(pieces)}"]
    for pat, x in pieces:
        r, c = len(pat), len(pat[0])
        assert 1 <= r <= 4 and 1 <= c <= 4 and all(len(row) == c for row in pat)
        assert set("".join(pat)) <= set("#.") and tight(pat)
        assert 1 <= x and x + c - 1 <= W
        lines.append(f"{r} {c} {x} " + " ".join(pat))
    tests.append("\n".join(lines) + "\n")

SHAPES = [["#"], ["##"], ["###"], ["####"], ["#", "#"], ["#", "#", "#"], ["#", "#", "#", "#"],
          ["##", "##"], ["#.", "##"], [".#", "##"], ["##", "#."], ["##", ".#"], ["###", ".#."],
          [".#.", "###"], ["#..", "###"], ["..#", "###"], ["##.", ".##"], [".##", "##."],
          ["#.", "#.", "##"], ["##", "#.", "#."], ["#.#", "###"], ["###", "#.#"]]

TETRO = [["####"], ["#", "#", "#", "#"], ["##", "##"], ["###", ".#."], [".#.", "###"], ["#.", "##", "#."],
         [".#", "##", ".#"], [".##", "##."], ["#.", "##", ".#"], ["##.", ".##"], [".#", "##", "#."],
         ["#.", "#.", "##"], ["###", "#.."], ["##", ".#", ".#"], ["..#", "###"], [".#", ".#", "##"],
         ["#..", "###"], ["##", "#.", "#."], ["###", "..#"]]

def rpat():
    while True:
        r, c = random.randint(1, 4), random.randint(1, 4)
        p = ["".join(random.choice("#.") for _ in range(c)) for _ in range(r)]
        if tight(p):
            return p

def rnd(W, H, n, shapes=True, flat=False):
    out = []
    for _ in range(n):
        if flat:
            c = random.randint(1, min(4, W))
            p = ["#" * c]
        elif shapes:
            p = random.choice([s for s in SHAPES if len(s[0]) <= W])
        else:
            p = rpat()
            while len(p[0]) > W:
                p = rpat()
        out.append((p, random.randint(1, W - len(p[0]) + 1)))
    return out

def greedy(W, n, shapes):
    """pieces placed where the stack stays lowest, so rows get cleared and the game lasts"""
    rows, out = [], []
    full = (1 << W) - 1
    def top(j):
        for k in range(len(rows) - 1, -1, -1):
            if rows[k] >> j & 1:
                return k + 1
        return 0
    def place(p, x):
        r, c = len(p), len(p[0])
        base = 1
        for j in range(c):
            low = 0
            while p[r - 1 - low][j] != "#":
                low += 1
            base = max(base, top(x - 1 + j) - low + 1)
        nr = rows + [0] * max(0, base + r - 1 - len(rows))
        for i in range(r):
            for j in range(c):
                if p[i][j] == "#":
                    nr[base - 1 + r - 1 - i] |= 1 << (x - 1 + j)
        nr = [m for m in nr if m != full]
        holes, seen = 0, 0
        for m in reversed(nr):
            holes += bin(seen & ~m).count("1")
            seen |= m
        hs = [0] * W
        for k, m in enumerate(nr):
            for j in range(W):
                if m >> j & 1:
                    hs[j] = k + 1
        bump = sum(abs(hs[j] - hs[j + 1]) for j in range(W - 1))
        return nr, sum(hs) + 4 * holes + bump
    for _ in range(n):
        p = random.choice([q for q in shapes if len(q[0]) <= W])
        best = None
        for x in range(1, W - len(p[0]) + 2):
            nr, holes = place(p, x)
            key = (holes, random.random())
            if best is None or key < best[0]:
                best = (key, x, nr)
        rows = best[2]
        out.append((p, best[1]))
    return out

def bands(W, n, junk=0.0):
    """2-row bands tiled exactly by squares, vertical dominoes and pairs of stacked bars"""
    out = []
    while len(out) < n:
        segs, col = [], 1
        while col <= W:
            kind = random.choice("SVB") if col < W else random.choice("VB")
            if kind == "S" and col + 1 <= W:
                segs.append([(["##", "##"], col)]); col += 2
            elif kind == "V":
                segs.append([(["#", "#"], col)]); col += 1
            else:
                w = random.randint(1, min(4, W - col + 1))
                segs.append([(["#" * w], col), (["#" * w], col)]); col += w
        pending = [list(sg) for sg in segs]
        while pending:
            sg = random.choice(pending)
            out.append(sg.pop(0))
            if not sg:
                pending.remove(sg)
            if random.random() < junk:
                p = random.choice(TETRO)
                out.append((p, random.randint(1, W - len(p[0]) + 1)))
    return out[:n]

# samples
add(4, 5, [(["###"], 1), (["#", "#"], 4), (["##"], 2)])
add(3, 3, [(["##.", ".##"], 1), (["#", "#", "#"], 1), (["#.#", "###"], 1)])
add(5, 4, [(["#.#", "###"], 1), (["#"], 2), (["##", "##"], 4)])
add(2, 3, [(["#"], 1), (["#", "#"], 1), (["##"], 1)])
add(4, 6, [(["###", "#.#"], 1), (["#"], 2), (["#", "#"], 4)])
# hidden
add(1, 1, [(["#"], 1)] * 5)
add(1, 1, [(["#", "#"], 1)])
add(30, 1000, rnd(30, 1000, 10000))
add(4, 1000, rnd(4, 1000, 10000, flat=True))
add(6, 1000, rnd(6, 1000, 10000))
add(10, 1000, rnd(10, 1000, 10000, shapes=False))
add(30, 1000, ([(["####"], x) for x in range(1, 26, 4)] + [(["##"], 29)]) * 1250)           # a row cleared every 8 pieces
add(30, 1000, ([(["####"] * 4, x) for x in range(1, 26, 4)] + [(["##"] * 4, 29)]) * 1250)    # four rows at once
add(8, 20, rnd(8, 20, 300))
add(5, 10, rnd(5, 10, 60, shapes=False))
add(4, 8, rnd(4, 8, 30))
add(3, 6, rnd(3, 6, 25, flat=True))
add(30, 1000, [(["#" * 4] * 4, x) for x in (1, 5, 9, 13, 17, 21, 25)] * 1400 + [(["#" * 2] * 4, 29)] * 200)   # game over
add(7, 50, rnd(7, 50, 2000, shapes=False))
add(10, 1000, bands(10, 10000))
add(6, 40, greedy(6, 500, TETRO))
add(30, 1000, bands(30, 10000, 0.002))
add(8, 100, bands(8, 3000, 0.01))
add(5, 12, bands(5, 40))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
