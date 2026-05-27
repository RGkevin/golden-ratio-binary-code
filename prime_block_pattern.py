def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def build_prime_block_pattern(num_blocks: int) -> tuple[list[list[int]], list[list[int]]]:
    """
    Returns two parallel lists of blocks.

    numbers[b]   — natural numbers in block b, ordered right-to-left (descending).
    primality[b] — 1 if the corresponding number is 1 or prime, 0 if composite.

    Block sizes follow the Fibonacci sequence: 1, 1, 2, 3, 5, 8, 13, ...
    """
    fibs: list[int] = [1, 1]
    while len(fibs) < num_blocks:
        fibs.append(fibs[-1] + fibs[-2])

    numbers: list[list[int]] = []
    primality: list[list[int]] = []
    current = 1

    for b in range(num_blocks):
        size = fibs[b]
        block_nums = list(reversed(range(current, current + size)))
        numbers.append(block_nums)
        primality.append([1 if (n == 1 or _is_prime(n)) else 0 for n in block_nums])
        current += size

    return numbers, primality


_FIBS_SET: set[int] = {0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987}
_LUCAS_SET: set[int] = {2, 1, 3, 4, 7, 11, 18, 29, 47, 76, 123, 199, 322, 521, 843}


def analyze_prime_gaps(num_blocks: int) -> list[dict]:
    """
    For each block, returns a dict with:
      block      — block number (1-based)
      full_gaps  — [head, *internal_gaps, tail]
      head       — composites before first prime
      internal   — gaps between consecutive primes
      tail       — composites after last prime
      breaks     — gaps that are not Fibonacci
      lucas      — which breaks are Lucas numbers
      non_lucas  — which breaks are neither Fibonacci nor Lucas
    """
    nums, prim = build_prime_block_pattern(num_blocks)
    results = []

    for b, ps in enumerate(prim, start=1):
        prime_pos = [i for i, p in enumerate(ps) if p == 1]
        if not prime_pos:
            results.append({"block": b, "full_gaps": [], "head": None,
                            "internal": [], "tail": None, "breaks": [], "lucas": [], "non_lucas": []})
            continue

        head     = prime_pos[0]
        tail     = len(ps) - 1 - prime_pos[-1]
        internal = [prime_pos[i] - prime_pos[i - 1] - 1 for i in range(1, len(prime_pos))]
        full     = [head] + internal + [tail]
        breaks   = [g for g in full if g not in _FIBS_SET]

        results.append({
            "block":     b,
            "full_gaps": full,
            "head":      head,
            "internal":  internal,
            "tail":      tail,
            "breaks":    breaks,
            "lucas":     [g for g in breaks if g in _LUCAS_SET],
            "non_lucas": [g for g in breaks if g not in _LUCAS_SET],
        })

    return results


if __name__ == "__main__":
    rows = analyze_prime_gaps(12)
    print("{:>7} | {:<42} | {:>6} | {:>6} | {:<18} | {:<16} | {}".format(
        "Bloque", "Gaps completos", "Head", "Tail", "Rompe", "Lucas", "No-Lucas"))
    print("-" * 120)
    for r in rows:
        def fmt(n):
            return str(n) + ("*" if n not in _FIBS_SET else "")
        full_str = "[" + ", ".join(fmt(g) for g in r["full_gaps"]) + "]"
        print("{:>7} | {:<42} | {:>6} | {:>6} | {:<18} | {:<16} | {}".format(
            r["block"], full_str, fmt(r["head"]) if r["head"] is not None else "--",
            fmt(r["tail"]) if r["tail"] is not None else "--",
            str(r["breaks"]) if r["breaks"] else "--",
            str(r["lucas"])  if r["lucas"]  else "--",
            str(r["non_lucas"]) if r["non_lucas"] else "--",
        ))
