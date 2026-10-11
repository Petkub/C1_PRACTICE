# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(502)
V = 10**9
tests = []

def add(a):
    n = len(a)
    assert 1 <= n <= 100_000
    assert all(-V <= x <= V for x in a)
    tests.append(f"{n}\n" + " ".join(map(str, a)) + "\n")

def pieces(n, maxlen, dmax, vmax):
    a = [random.randint(-vmax, vmax)]
    while len(a) < n:
        d = random.randint(-dmax, dmax)
        for _ in range(random.randint(1, maxlen)):
            if len(a) == n:
                break
            nx = a[-1] + d
            if abs(nx) > vmax:
                d = -d
                nx = a[-1] + d
            a.append(nx)
    return a

# samples
add([4, 3, 5, 7, 9, 8, 4])
add([5, 5, 5, 1, 2, 3])
add([42])
add([10, -3])
add([1, 2, 4, 8, 16])
add([9, 6, 3, 0, 1, 5, 9, 13, 17])
# hidden
add([-V, V, -V])                      # differences 2e9 and -2e9 (overflow in int)
add([-V, V, -V, V, -V])
add([V, 0, -V, 1, 2])                 # -1e9 twice, then diffs 1e9+1, 1
add([7] * 1000)
add(list(range(-50_000, 50_000)))     # max N, whole array
add(pieces(30, 5, 3, 20))
add(pieces(200, 8, 2, 50))
add(pieces(2000, 30, 5, 1000))
add(pieces(100_000, 40, 10**6, V))
add([random.choice([-V, V]) for _ in range(40_000)])
a = [random.randint(-V, V) for _ in range(50_000)]
add(a)                                # random: answer usually 2 at l = 1
b = pieces(100_000, 3, 5, 100)
b[70_000:70_100] = [5 * i - 200 for i in range(100)]
add(b)                                # one long run late in the array

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
