# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random

random.seed(812)
tests = []
M = 10**6

def add(ops):
    assert 1 <= len(ops) <= 50000
    for t, q, x in ops:
        assert t in ("BUY", "SELL") and 1 <= q <= M and 1 <= x <= M
    tests.append(f"{len(ops)}\n" + "".join(f"{t} {q} {x}\n" for t, q, x in ops))

def rnd(n, qmax, cmax, pbuy, sell_scale=1.0):
    ops = []
    for _ in range(n):
        if random.random() < pbuy:
            ops.append(("BUY", random.randint(1, qmax), random.randint(1, cmax)))
        else:
            ops.append(("SELL", random.randint(1, max(1, int(qmax * sell_scale))), random.randint(1, cmax)))
    return ops

# samples
add([("BUY", 3, 10), ("BUY", 4, 20), ("SELL", 4, 25), ("SELL", 2, 15)])
add([("BUY", 2, 7), ("BUY", 3, 7), ("SELL", 6, 9), ("SELL", 5, 8)])
add([("SELL", 1, 100), ("BUY", 1, 100), ("SELL", 1, 100)])
add([("BUY", 5, 3), ("SELL", 1, 4), ("BUY", 2, 1), ("SELL", 5, 2), ("BUY", 1, 9), ("SELL", 3, 5)])
add([("BUY", 10, 6), ("BUY", 1, 1), ("SELL", 11, 2)])
# hidden
add([("BUY", 1, 1)])
add([("BUY", M, M)] * 30000)                                     # remaining value 3e16
add([("BUY", M, 1)] * 10000 + [("SELL", M, M)] * 10000)          # many big sales
add([("BUY", 1, random.randint(1, 9)) for _ in range(49999)] + [("SELL", 49999, 1)])   # one sale eats every lot
add([("BUY", M, M), ("SELL", M, 1)] * 10000)                     # big losses
add(rnd(15000, M, M, 0.5))
add(rnd(15000, M, M, 0.35, 0.3))
add(rnd(30000, 1000, 50, 0.5, 2.0))                              # many rejects
add(rnd(2000, 20, 30, 0.5))
add(rnd(50, 6, 10, 0.5))
add(rnd(300, 10, 100, 0.4, 0.5))
add([("SELL", 5, 5)] * 3 + [("BUY", 5, 5)] + [("SELL", 6, 5), ("SELL", 5, 5), ("SELL", 1, 1)])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
