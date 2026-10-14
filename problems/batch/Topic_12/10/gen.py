# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random, re

random.seed(1210)
tests = []
NAME = re.compile(r"[a-z0-9]{1,10}$")

def check_path(p):
    assert 1 <= len(p) <= 200
    if p == "/":
        return
    body = p[1:] if p[0] == "/" else p
    for part in body.split("/"):
        assert part in (".", "..") or NAME.match(part), p

def apply(cur, p):
    cur = [] if p[0] == "/" else cur[:]
    for part in p.split("/"):
        if part == "" or part == ".":
            continue
        if part == "..":
            if cur:
                cur.pop()
        else:
            cur.append(part)
    return cur

def canon_len(cur):
    return 1 if not cur else sum(len(s) + 1 for s in cur)

def add(cmds):
    q = len(cmds)
    assert 1 <= q <= 10_000
    assert "pwd" in cmds
    cur = []
    for c in cmds:
        if c == "pwd":
            continue
        assert c.startswith("cd ") and c.count(" ") == 1
        p = c[3:]
        check_path(p)
        cur = apply(cur, p)
        assert canon_len(cur) <= 200
    tests.append(f"{q}\n" + "\n".join(cmds) + "\n")

def lines(s):
    return s.strip().split("\n")

POOL = ["home", "docs", "a", "b", "c", "x1", "2026", "src", "img", "tmp", "lib", "bin",
        "music", "work", "game", "v2", "0", "zz9", "project", "photos2025"]

def rname(pool):
    if pool is None:
        return "".join(random.choice("abcdefghijklmnopqrstuvwxyz0123456789")
                       for _ in range(random.randint(1, 10)))
    return random.choice(pool)

def rpath(k, pool, pdot, pup, pabs):
    parts = []
    for _ in range(k):
        r = random.random()
        if r < pdot:
            parts.append(".")
        elif r < pdot + pup:
            parts.append("..")
        else:
            parts.append(rname(pool))
    p = "/".join(parts)
    if random.random() < pabs:
        p = "/" + p
    return p

def rnd(q, ppwd, kmax, pool, pdot=0.1, pup=0.3, pabs=0.1, proot=0.0):
    cmds, cur = [], []
    while len(cmds) < q:
        if random.random() < ppwd or (len(cmds) == q - 1 and "pwd" not in cmds):
            cmds.append("pwd")
            continue
        while True:
            if random.random() < proot:
                p = "/"
            else:
                p = rpath(random.randint(1, kmax), pool, pdot, pup, pabs)
            if len(p) <= 200:
                nxt = apply(cur, p)
                if canon_len(nxt) <= 200:
                    break
        cur = nxt
        cmds.append("cd " + p)
    return cmds

# samples
add(lines("pwd\ncd home/somchai\npwd\ncd ../somsri/./docs\npwd\ncd /tmp\npwd"))
add(lines("cd ../../x\npwd\ncd ../..\ncd y/./z/..\npwd"))
add(lines("cd /a/../b/.\npwd\ncd /\npwd"))
add(lines("pwd"))
add(lines("cd 2026/t1\ncd ../t2/../../25\npwd"))
# hidden (small, special cases)
add(lines("cd .\npwd\ncd ..\npwd\ncd /\npwd\ncd /..\npwd\ncd ./.././..\npwd"))
add(lines("cd a/a/a\npwd\ncd ../a\npwd\ncd /a/../../a/./a/..\npwd\ncd ..\ncd ..\npwd"))
add(["cd " + "/".join(["abcdefghi"] * 20), "pwd", "cd ..", "pwd",
     "cd " + "/".join([".."] * 66) + "/z", "pwd"])                        # path of length exactly 200
add(rnd(20, 0.4, 4, ["a", "b", "c"]))
add(rnd(60, 0.3, 6, POOL, pabs=0.2, proot=0.05))
add(rnd(300, 0.3, 8, None, pdot=0.15, pup=0.4))
# large
add(rnd(10_000, 0.4, 6, POOL, proot=0.02))
add(rnd(10_000, 0.3, 10, None, pdot=0.1, pup=0.45, pabs=0.05))
add(rnd(4_000, 0.35, 40, POOL, pdot=0.2, pup=0.35, pabs=0.3))
add(rnd(10_000, 0.2, 30, ["a", "b", "0"], pdot=0.25, pup=0.5, pabs=0.02))  # long chains of . and ..
add(rnd(3_000, 0.5, 25, None, pdot=0.05, pup=0.2, pabs=0.5))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
