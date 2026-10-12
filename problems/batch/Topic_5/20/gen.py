# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(520)
V = 10_000
tests = []

def add(g, c):
    n = len(g)
    assert 1 <= n <= 100_000 and len(c) == n
    assert all(0 <= x <= V for x in g) and all(0 <= x <= V for x in c)
    tests.append(f"{n}\n" + " ".join(map(str, g)) + "\n" + " ".join(map(str, c)) + "\n")

def balanced(n, hi, extra):
    # random pumps whose total fuel is the total cost plus `extra` (extra may be negative)
    g = [random.randint(0, hi) for _ in range(n)]
    c = [random.randint(0, hi) for _ in range(n)]
    diff = sum(g) - sum(c) - extra       # make sum(g) - sum(c) == extra
    i = 0
    while diff != 0:
        j = i % n
        if diff > 0:
            step = min(diff, V - c[j])
            c[j] += step
            diff -= step
        else:
            step = min(-diff, V - g[j])
            g[j] += step
            diff += step
        i += 1
    return g, c

# samples
add([1, 2, 3, 4], [3, 4, 1, 1])
add([1, 1, 1], [2, 2, 2])
add([3, 0, 2, 0, 2], [1, 1, 1, 1, 1])
add([5], [5])
add([2, 2, 2, 2], [1, 3, 1, 3])
add([0, 0], [0, 0])
# hidden
add([4], [5])
add([0, 7], [7, 0])
add(*balanced(8, 5, 0))
add(*balanced(12, 4, 2))
add(*balanced(50, 6, 3))
add(*balanced(300, 20, -1))
add(*balanced(2000, 3, 5))
# max
add([0] * 100_000, [0] * 100_000)                 # every pump works
add(*balanced(100_000, 3, 4))
add(*balanced(100_000, 10, 0))
add(*balanced(50_000, V, 50_000))
g = [2, 0] * 50_000
g[0] = 3
add(g, [1, 1] * 50_000)                           # half of the pumps work, total 1
add(*balanced(100_000, 5, -1))                    # total one litre short
g = [1] * 100_000
c = [1] * 100_000
c[99_999] = 3
g[0] = 3
add(g, c)

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
