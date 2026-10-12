# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(813)
tests = []

def add(s):
    assert 1 <= len(s) <= 10**6 and set(s) <= set(".LR")
    tests.append(f"{len(s)}\n{s}\n")

def rnd(n, p):
    return "".join(random.choice("LR") if random.random() < p else "." for _ in range(n))

# samples
add(".R....L..R.")
add("R...L")
add("..R....")
add("L..R")
add("....")
add(".L.R..L..R.")
# hidden
add(".")
add("R")
add("R" + "." * 999999)                       # longest chain to the right
add("." * 999999 + "L")
add("R" + "." * 499998 + "L")
add("R" + "." * 500 + "L" + "." * 500 + "R")
add(rnd(10**5, 0.001))
add(rnd(10**5, 0.5))
add(rnd(2000, 0.01))
add(rnd(300, 0.05))
add(rnd(50, 0.2))
add("L.R" * 1000)
add("R.L" * 1000 + "R..L" * 500)

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
