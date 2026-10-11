# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(803)
tests = []

def add(G, Y, R, ts):
    assert 1 <= G <= 10**9 and 0 <= Y <= 10**9 and 1 <= R <= 10**9
    assert 1 <= len(ts) <= 10**5
    for t in ts:
        assert 0 <= t <= 10**18
    tests.append(f"{G} {Y} {R}\n{len(ts)}\n" + "".join(f"{t}\n" for t in ts))

# samples
add(5, 2, 3, [0, 4, 6, 7, 12])
add(3, 0, 2, [2, 3, 5])
add(1, 1, 1, [0, 1, 2, 3])
add(30, 5, 25, [59, 60, 61, 1000])
add(10, 3, 7, [10**18])
# hidden (brute walks phases, so small t / P for these)
add(1, 0, 1, list(range(0, 30)))
add(4, 0, 6, [random.randint(0, 2000) for _ in range(500)])
add(7, 3, 2, [random.randint(0, 10**6) for _ in range(200)])
add(1, 10**9, 1, [0, 1, 10**9, 10**9 + 1, 10**9 + 2, 2 * 10**9 + 1])
add(10**9, 10**9, 10**9, [0, 10**9 - 1, 10**9, 2 * 10**9, 3 * 10**9 - 1, 3 * 10**9, 10**12])
add(10**9, 0, 10**9, [10**18, 10**18 - 1, 999999999999999999, 2 * 10**9 * 499999999])
# big

add(999999999, 2, 999999998, [random.randint(0, 10**18) for _ in range(40000)])
add(13, 7, 11, [random.randint(0, 10**18) for _ in range(40000)])
add(123456789, 0, 987654321, [random.randint(0, 10**18) for _ in range(40000)])
add(3, 5, 8, [10**18 - i for i in range(1000)])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
