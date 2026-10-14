# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random

random.seed(1102)
tests = []

def add(ts):
    n = len(ts)
    assert 2 <= n <= 100_000
    for s in ts:
        assert len(s) == 5 and s[2] == ":" and s[:2].isdigit() and s[3:].isdigit()
        assert 0 <= int(s[:2]) <= 23 and 0 <= int(s[3:]) <= 59
    tests.append(f"{n}\n" + " ".join(ts) + "\n")

def fmt(m):
    assert 0 <= m < 1440
    return f"{m // 60:02d}:{m % 60:02d}"

def addm(ms):
    add([fmt(m) for m in ms])

# samples
add("08:30 07:45 09:10 08:00 08:15".split())
add("12:00 06:30 12:00 18:45 12:00".split())
add("23:50 00:05".split())
add("11:00 10:00 23:59 11:00 10:00 11:00".split())
add("00:00 12:00 23:59".split())
add("05:02 05:00 05:01".split())
# hidden
addm([0, 1439])
addm([777, 777])
ms = list(range(1440)); random.shuffle(ms); addm(ms)                      # D = 1, 1439 pairs
ms = list(range(0, 1440, 2)); random.shuffle(ms); addm(ms)                # D = 2, 719 pairs
ms = list(range(0, 1440, 7)) + [3]; random.shuffle(ms); addm(ms)          # D = 3 once
addm(random.sample(range(1440), 40))
addm(random.sample(range(0, 1440, 5), 60))
addm([random.randint(600, 620) for _ in range(30)])
addm([random.randint(0, 1439) for _ in range(2000)])
addm([1000] * 100_000)                                                    # 4 999 950 000 pairs
ms = [5] * 50_000 + [1430] * 50_000; random.shuffle(ms); addm(ms)
addm([random.randint(0, 1439) for _ in range(100_000)])
ms = random.sample(range(0, 1440, 3), 400); random.shuffle(ms); addm(ms)
ms = list(range(0, 1440, 4)) * 250; random.shuffle(ms); addm(ms[:100_000])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
