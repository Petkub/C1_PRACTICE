# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(815)
tests = []

def add(S, C, P, ps):
    N = len(ps)
    assert 2 <= S <= 100 and 1 <= C <= 100 and 1 <= P <= 100 and 1 <= N <= 100000
    for t, s, e in ps:
        assert 0 <= t <= 10**6 and 1 <= s <= S and 1 <= e <= S and s != e
    assert all(ps[i][0] <= ps[i + 1][0] for i in range(N - 1))
    tests.append(f"{S} {C} {P} {N}\n" + "".join(f"{t} {s} {e}\n" for t, s, e in ps))

def trip(S, s=None):
    s = s or random.randint(1, S)
    e = random.randint(1, S - 1)
    return s, e + (e >= s)

def rnd(S, N, tmax, hot=None):
    ps = []
    for _ in range(N):
        s = hot if hot and random.random() < 0.5 else None
        ps.append((random.randint(0, tmax), *trip(S, s)))
    ps.sort(key=lambda x: x[0])
    return ps

# samples
add(4, 2, 2, [(0, 1, 3), (0, 1, 2), (0, 1, 4), (1, 2, 1), (2, 3, 1)])
add(3, 1, 1, [(0, 1, 3), (0, 1, 2), (3, 1, 2)])
add(5, 3, 3, [(0, 2, 1), (2, 2, 3), (6, 3, 5), (7, 3, 4)])
add(2, 1, 2, [(0, 1, 2)] * 3)
add(4, 2, 3, [(0, 3, 1), (1, 1, 2), (1, 1, 3), (1, 1, 4)])
# hidden
add(4, 2, 3, [(0, 3, 1), (1, 1, 2), (1, 1, 3), (1, 1, 4), (2, 4, 3), (5, 2, 1), (5, 2, 4)])
add(2, 1, 1, [(0, 2, 1)])
add(100, 100, 100, [(10**6, 100, 99)])                                  # latest arrival, longest ride
add(100, 1, 100, [(0, 1, 100)] * 100000)                                # one per lap, 100 laps of patience
add(100, 3, 100, sorted((random.randint(0, 50), *trip(100, random.choice([1, 2, 3]))) for _ in range(50000)))
add(7, 2, 5, rnd(7, 60000, 10**6, hot=3))
add(20, 3, 2, rnd(20, 60000, 200000, hot=7))
add(10, 1, 3, rnd(10, 3000, 15000, hot=4))
add(5, 2, 2, rnd(5, 40, 30, hot=1))
add(3, 1, 4, rnd(3, 25, 20, hot=2))
add(6, 3, 1, rnd(6, 60, 25, hot=5))
add(2, 2, 3, rnd(2, 30, 10))
add(8, 4, 2, [(t, s, e) for t in range(0, 40, 8) for s, e in [(1, 8), (1, 5), (2, 1), (5, 6), (1, 2), (1, 3)]])
add(4, 1, 100, [(0, 1, 4)] * 60 + [(500, 3, 2)])                       # long queue, then a quiet gap

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
