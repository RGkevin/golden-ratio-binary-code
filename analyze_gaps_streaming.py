"""
Streaming gap analysis up to block 37.
Processes one block at a time — O(F_b) memory per block.
Uses a segmented sieve for fast primality, saving results to CSV.
"""

import csv
import time
import math

MAX_BLOCK   = 44
OUTPUT_FILE = "gap_analysis.csv"

FIBS_SET  = {0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987}
LUCAS_SET = {1, 2, 3, 4, 7, 11, 18, 29, 47, 76, 123, 199, 322, 521, 843}


# ── Fibonacci sequence ────────────────────────────────────────────────────────

def _build_fibs(n: int) -> list[int]:
    fibs = [1, 1]
    while len(fibs) < n:
        fibs.append(fibs[-1] + fibs[-2])
    return fibs


# ── Segmented sieve ───────────────────────────────────────────────────────────

def _small_primes(limit: int) -> list[int]:
    sieve = bytearray([1]) * (limit + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(limit ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i :: i] = b"\x00" * len(sieve[i * i :: i])
    return [i for i in range(2, limit + 1) if sieve[i]]


def _block_primality(low: int, high: int, small_primes: list[int]) -> bytearray:
    """
    Returns bytearray of length (high-low+1) where byte[i]=1 iff (low+i) is prime.
    Special-cases 1 as non-prime (the block pattern treats it as 1, handled above).
    """
    size = high - low + 1
    arr  = bytearray([1]) * size

    if low == 0:
        arr[0] = 0
    if low <= 1 <= high:
        arr[1 - low] = 0

    for p in small_primes:
        if p * p > high:
            break
        start = max(p * p, ((low + p - 1) // p) * p)
        arr[start - low :: p] = b"\x00" * len(arr[start - low :: p])

    return arr


# ── Gap analysis for one block ────────────────────────────────────────────────

def _gaps_from_primality(prim: bytearray, low: int) -> dict:
    """
    prim[i] = 1 if (low + i) is prime (ascending order, low..high).
    The block is displayed descending, but gaps are symmetric so it doesn't matter.
    Number 1 is treated as '1' (included), handled before calling this.
    """
    prime_pos = [i for i, p in enumerate(prim) if p]
    if not prime_pos:
        return {"head": None, "internal": [], "tail": None,
                "full_gaps": [], "breaks": [], "lucas": [], "non_lucas": []}

    head     = prime_pos[0]
    tail     = len(prim) - 1 - prime_pos[-1]
    internal = [prime_pos[i] - prime_pos[i - 1] - 1 for i in range(1, len(prime_pos))]
    full     = [head] + internal + [tail]
    breaks   = [g for g in full if g not in FIBS_SET]

    return {
        "head":      head,
        "internal":  internal,
        "tail":      tail,
        "full_gaps": full,
        "breaks":    breaks,
        "lucas":     [g for g in breaks if g in LUCAS_SET],
        "non_lucas": [g for g in breaks if g not in LUCAS_SET],
    }


# ── Main ──────────────────────────────────────────────────────────────────────

def run():
    fibs = _build_fibs(MAX_BLOCK + 2)

    # Largest number we'll check: last element of block MAX_BLOCK
    # Block b (1-indexed) occupies [sum(fibs[:b-1])+1 .. sum(fibs[:b])]
    # The largest number in block MAX_BLOCK = sum(fibs[:MAX_BLOCK])
    # That equals fibs[MAX_BLOCK+1] - 1  (Fibonacci identity)
    max_num = fibs[MAX_BLOCK + 1] - 1
    sieve_limit = int(math.isqrt(max_num)) + 1
    print(f"Pre-computing primes up to {sieve_limit:,}...")
    small_primes = _small_primes(sieve_limit)
    print(f"  {len(small_primes):,} small primes ready.\n")

    fieldnames = [
        "bloque", "size", "low", "high",
        "head", "head_fib", "head_lucas",
        "tail", "tail_fib", "tail_lucas",
        "num_breaks", "breaks",
        "num_lucas_breaks", "lucas_breaks",
        "num_non_lucas_breaks", "non_lucas_breaks",
        "contains_18", "max_gap", "num_primes",
        "time_s",
    ]

    total_start = time.time()
    current     = 1  # next number to assign

    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for b in range(1, MAX_BLOCK + 1):
            size = fibs[b - 1]
            low  = current
            high = current + size - 1

            t0 = time.time()

            # Build primality array (ascending order: low..high)
            prim = _block_primality(low, high, small_primes)

            # Block 1 contains number 1, which we treat as prime-like (value=1)
            if low == 1:
                prim[0] = 1  # number 1 → treated as 1

            r = _gaps_from_primality(prim, low)
            elapsed = time.time() - t0

            head = r["head"]
            tail = r["tail"]
            row  = {
                "bloque":              b,
                "size":                size,
                "low":                 low,
                "high":                high,
                "head":                head,
                "head_fib":            int(head in FIBS_SET) if head is not None else "",
                "head_lucas":          int(head in LUCAS_SET) if head is not None else "",
                "tail":                tail,
                "tail_fib":            int(tail in FIBS_SET) if tail is not None else "",
                "tail_lucas":          int(tail in LUCAS_SET) if tail is not None else "",
                "num_breaks":          len(r["breaks"]),
                "breaks":              str(r["breaks"]),
                "num_lucas_breaks":    len(r["lucas"]),
                "lucas_breaks":        str(r["lucas"]),
                "num_non_lucas_breaks":len(r["non_lucas"]),
                "non_lucas_breaks":    str(r["non_lucas"]),
                "contains_18":         int(18 in r["breaks"]),
                "max_gap":             max(r["full_gaps"]) if r["full_gaps"] else 0,
                "num_primes":          sum(prim),
                "time_s":              round(elapsed, 3),
            }
            writer.writerow(row)
            f.flush()

            total_elapsed = time.time() - total_start
            print(f"B{b:2d} | size={size:>12,} | primes={sum(prim):>8,} | "
                  f"breaks={len(r['breaks']):>5} | 18={'YES' if row['contains_18'] else ' no'} | "
                  f"{elapsed:>7.2f}s | total={total_elapsed:>7.1f}s")

            current += size

    print(f"\nDone. Results saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    run()
