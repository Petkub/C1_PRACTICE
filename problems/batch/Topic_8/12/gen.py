# Writes tests/NN.in for this problem. Samples first (01..05), then hidden tests.
import os, random, datetime

random.seed(811)
tests = []
ZONES = [z for z in range(-720, 841) if abs(z) % 60 in (0, 30, 45)]

def zs(z):
    s = "-" if z < 0 else "+"
    return f"{s}{abs(z) // 60:02d}:{abs(z) % 60:02d}"

def fl(y, m, d, hh, mm, z1, dh, dm, z2):
    datetime.date(y, m, d)
    assert 1100 <= y <= 9000 and 0 <= hh <= 23 and 0 <= mm <= 59
    assert -720 <= z1 <= 840 and -720 <= z2 <= 840 and abs(z1) % 60 in (0, 30, 45) and abs(z2) % 60 in (0, 30, 45)
    assert 0 <= dh <= 999 and 0 <= dm <= 59
    return f"{y:04d}-{m:02d}-{d:02d} {hh:02d}:{mm:02d} {zs(z1)} {dh}:{dm:02d} {zs(z2)}"

def add(fs):
    assert 1 <= len(fs) <= 10000
    tests.append(f"{len(fs)}\n" + "\n".join(fs) + "\n")

def rdate(y1, y2):
    while True:
        y, m, d = random.randint(y1, y2), random.randint(1, 12), random.randint(1, 31)
        try:
            datetime.date(y, m, d)
            return y, m, d
        except ValueError:
            pass

def rz():
    return random.choice(ZONES)

def rnd(y1, y2, hmax):
    return fl(*rdate(y1, y2), random.randint(0, 23), random.randint(0, 59), rz(),
              random.randint(0, hmax), random.randint(0, 59), rz())

# samples
add([fl(2026, 12, 31, 22, 0, 420, 11, 30, 60)])
add([fl(2024, 3, 1, 0, 10, 840, 0, 45, -630)])
add([fl(2100, 2, 28, 23, 15, -330, 2, 0, 345)])
add([fl(1999, 12, 31, 23, 59, 0, 0, 1, 0)])
add([fl(2000, 2, 28, 23, 15, -330, 2, 0, 345), fl(2026, 6, 15, 8, 0, 420, 999, 59, -720)])
# hidden
add([fl(1100, 1, 1, 0, 0, 840, 0, 0, -720)])                       # goes back two days, into year 1099
add([fl(9000, 12, 31, 23, 59, -720, 999, 59, 840)])                 # latest possible
add([fl(y, 3, 1, 0, 0, 840, 0, 0, -720) for y in (1600, 1700, 1900, 2000, 2004, 2023, 2100, 2400)])
add([fl(y, 2, 28, 12, 0, 0, 24, 0, 0) for y in (1600, 1700, 1900, 2000, 2004, 2023, 2100, 2400)])
add([fl(2025, 1, 1, 0, 0, 60, 0, 0, 0), fl(2026, 6, 15, 8, 0, -105, 0, 0, -105), fl(2024, 1, 1, 0, 30, -570, 0, 0, 0), fl(2024, 1, 1, 0, 30, 570, 0, 0, 0), fl(2024, 12, 31, 23, 30, -45, 0, 0, 0)])
add([rnd(1100, 9000, 999) for _ in range(10000)])
add([rnd(1100, 9000, 30) for _ in range(10000)])
add([rnd(1890, 2110, 5) for _ in range(3000)])
add([fl(*rdate(1100, 9000), random.randint(0, 3), random.randint(0, 59), random.choice([780, 840, 825]),
        0, random.randint(0, 59), random.choice([-720, -660, -570])) for _ in range(2000)])
add([rnd(2000, 2030, 99) for _ in range(20)])

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
