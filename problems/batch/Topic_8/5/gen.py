# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(805)
tests = []

def add(F, P, sl, dice):
    M, K = len(sl), len(dice)
    assert 10 <= F <= 1000 and 2 <= P <= 10 and 1 <= K <= 10**5 and 0 <= M <= F // 2
    xs = [x for x, _ in sl]
    assert len(set(xs)) == M
    for x, y in sl:
        assert 2 <= x <= F - 1 and 1 <= y <= F and x != y and y not in xs
    assert all(1 <= d <= 6 for d in dice)
    lines = [f"{F} {P} {M} {K}"] + [f"{x} {y}" for x, y in sl] + [" ".join(map(str, dice))]
    tests.append("\n".join(lines) + "\n")

def board(F, M):
    cells = list(range(2, F))
    random.shuffle(cells)
    xs = cells[:M]
    rest = [c for c in range(1, F + 1) if c not in set(xs)]
    return [(x, random.choice([c for c in random.sample(rest, 5) if c != x] or [1])) for x in xs]

def dice(K):
    return [random.randint(1, 6) for _ in range(K)]

# samples
add(10, 2, [(3, 7), (9, 2)], [3, 4, 4, 6, 3])
add(12, 3, [(5, 11)], [5, 2, 6, 3])
add(10, 2, [(4, 10)], [1, 3, 3])                       # ladder to the last cell
add(15, 2, [(12, 1), (3, 14)], [3, 6, 4, 6, 1])        # bounce onto a snake
add(10, 3, [], [6, 5, 4, 4, 5, 6, 1, 1])
# hidden
add(10, 2, [], [1])
add(10, 10, [], [6] * 10)
add(1000, 2, [], [1] * 10**5)                           # slow game, many rolls
add(1000, 10, [(999, 1), (998, 1), (997, 1), (996, 1), (995, 1), (994, 1)], [6] * 10**5)
add(1000, 4, board(1000, 500), dice(10**5))
add(100, 3, board(100, 30), dice(10**5))
add(30, 5, board(30, 15), dice(200))
add(20, 2, [(19, 3), (18, 3), (17, 3), (16, 3)], [6, 6, 6, 6, 4, 4, 1, 2, 3, 4, 5, 6, 6, 6])
add(10, 2, [(5, 10)], [5])                              # win on the first roll
add(50, 6, board(50, 25), dice(40))
add(10, 2, [(9, 1), (8, 1)], [6, 6, 3, 2, 6, 6, 6, 6, 1, 1])
add(500, 7, board(500, 250), dice(3000))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
