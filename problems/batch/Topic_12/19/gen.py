# Writes tests/NN.in for this problem. Samples first (01..06), then hidden tests.
import os, random, sys

random.seed(1219)
sys.setrecursionlimit(20000)
B = 10**18
MAXLEN = 100_000
MAXDEPTH = 1000
tests = []


def check(s):
    """Evaluate s with precedence and left-to-right rules, asserting every constraint."""
    assert 1 <= len(s) <= MAXLEN
    assert set(s) <= set("0123456789+-*()")
    depth = 0
    for c in s:
        depth += (c == "(") - (c == ")")
        assert 0 <= depth <= MAXDEPTH
    assert depth == 0
    vals, ops = [], []

    def apply():
        op = ops.pop()
        b = vals.pop()
        a = vals.pop()
        r = a + b if op == "+" else a - b if op == "-" else a * b
        assert abs(r) <= B
        vals.append(r)

    prec = {"+": 1, "-": 1, "*": 2}
    i, expect_operand = 0, True
    while i < len(s):
        c = s[i]
        if c.isdigit():
            assert expect_operand
            j = i
            while j < len(s) and s[j].isdigit():
                j += 1
            tok = s[i:j]
            assert tok == "0" or tok[0] != "0"
            assert int(tok) <= 10**9
            vals.append(int(tok))
            i, expect_operand = j, False
            continue
        if c == "(":
            assert expect_operand
            ops.append(c)
        elif c == ")":
            assert not expect_operand
            while ops[-1] != "(":
                apply()
            ops.pop()
        else:
            assert not expect_operand
            while ops and ops[-1] != "(" and prec[ops[-1]] >= prec[c]:
                apply()
            ops.append(c)
            expect_operand = True
        i += 1
    assert not expect_operand
    while ops:
        apply()
    assert len(vals) == 1
    return vals[0]


def add(s):
    if isinstance(s, tuple):            # (string, value) from gen_expr
        s, v = s
        assert check(s) == v
    check(s)
    tests.append(s + "\n")


def number(big):
    r = random.random()
    if r < 0.05:
        return 0
    if r < 0.6 or not big:
        return random.randint(1, 9)
    if r < 0.85:
        return random.randint(10, 99_999)
    return random.randint(10**8, 10**9)


def gen_factor(budget, depth, pparen, big):
    if budget >= 5 and depth < MAXDEPTH and random.random() < pparen:
        s, v = gen_expr(random.randint(3, budget - 2), depth + 1, pparen, big)
        return "(" + s + ")", v
    x = number(big)
    return str(x), x


def gen_expr(budget, depth, pparen, big, pmul=0.4):
    """Random valid expression of about `budget` characters; keeps every partial result within B."""
    s, v = gen_factor(budget, depth, pparen, big)
    parts, total, sign, prod = [s], 0, 1, v   # value so far = total + sign * prod
    used = len(s)
    while used + 2 <= budget:
        s, v = gen_factor(budget - used - 1, depth, pparen, big)
        if random.random() < pmul and abs(prod * v) <= B and abs(total + sign * prod * v) <= B:
            parts.append("*" + s)
            prod *= v
        else:
            total += sign * prod
            op = random.choice("+-")
            if abs(total + v if op == "+" else total - v) > B:
                op = "-" if op == "+" else "+"
            sign = 1 if op == "+" else -1
            parts.append(op + s)
            prod = v
        used += len(s) + 1
    return "".join(parts), total + sign * prod


def nested(depth, inner_first):
    """depth levels of parentheses, e.g. ((1+2)*3-4) or 1-(2-(3-...))."""
    if inner_first:
        e, val = "1", 1
        for _ in range(depth):
            x = random.randint(1, 9)
            op = random.choice("+-*") if abs(val) < 10**12 else random.choice("+-")
            e = "(" + e + op + str(x) + ")"
            val = val + x if op == "+" else val - x if op == "-" else val * x
        return e
    parts = [str(random.randint(0, 9)) + random.choice("+-") + "(" for _ in range(depth)]
    return "".join(parts) + "7" + ")" * depth


# samples
add("5+2*3-1")
add("100-30-20-10")
add("(1+2)*(3+4)-5")
add("999999999*999999999")
add("2*3-4*5-(6-7)")
add("((7))")
# hidden (small)
add("0")
add("1-2-3-4-5")
add("8-(2-3)*4")
add("2*3*4-24")
add("0-1000000000*1000000000")
add("1000000000*1000000000-999999999*1000000000-1000000000+7")
add(gen_expr(40, 0, 0.25, False))
add(gen_expr(200, 0, 0.2, True))
# large
add(nested(MAXDEPTH, True))
add(nested(MAXDEPTH, False))
add(gen_expr(MAXLEN - 12, 0, 0.0, True, pmul=0.0))       # long chain of + and -
add(gen_expr(MAXLEN - 12, 0, 0.0, True, pmul=0.6))       # no parentheses
add(gen_expr(MAXLEN - 12, 0, 0.15, True))
add(gen_expr(MAXLEN - 12, 0, 0.3, False, pmul=0.5))

os.makedirs("tests", exist_ok=True)
for i, t in enumerate(tests, 1):
    with open(f"tests/{i:02d}.in", "w") as f:
        f.write(t)
