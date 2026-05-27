from prime_block_pattern import build_prime_block_pattern

FIBS = [1, 1]
while len(FIBS) < 25:
    FIBS.append(FIBS[-1] + FIBS[-2])

FIBS_SET  = {0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233}
LUCAS_SET = {1, 2, 3, 4, 7, 11, 18, 29, 47, 76, 123}

def tag(n):
    if n in FIBS_SET:  return str(n)
    if n in LUCAS_SET: return str(n) + "L"
    return str(n) + "*"

def gaps_from_prim(prim_list):
    pos = [i for i, p in enumerate(prim_list) if p]
    if not pos:
        return None, [], None
    head     = pos[0]
    tail     = len(prim_list) - 1 - pos[-1]
    internal = [pos[i] - pos[i-1] - 1 for i in range(1, len(pos))]
    return head, internal, tail

nums, prim = build_prime_block_pattern(20)

sep = "-" * 80

for b in range(1, 21):
    size_b  = FIBS[b - 1]
    size_b1 = FIBS[b - 2] if b >= 2 else 0   # size of previous block = F_{b-1}
    size_b2 = size_b - size_b1                # F_{b-2}

    ps = prim[b - 1]   # descending primality

    interno = ps[:size_b1]
    externo = ps[size_b1:]

    hi, gi, ti = gaps_from_prim(interno)
    he, ge, te = gaps_from_prim(externo)

    def fmt_gaps(h, g, t, size):
        if h is None:
            return "(sin primos)"
        gi_str = "[" + ", ".join(tag(x) for x in g) + "]"
        return "head={} | interno={} | tail={}".format(tag(h), gi_str, tag(t))

    print(sep)
    print("Bloque {:2d}  |  total={:4d}  |  interno={:4d}  |  externo={:4d}".format(
        b, size_b, size_b1, size_b2))
    print("  INTERNO : {}".format(fmt_gaps(hi, gi, ti, size_b1)))
    print("  EXTERNO : {}".format(fmt_gaps(he, ge, te, size_b2)))

print(sep)
