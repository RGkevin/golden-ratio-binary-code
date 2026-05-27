"""
Counts total primes, internal-group primes, and external-group primes
for every Fibonacci block from 1 to 44.

Internal group: the largest F_{b-1} numbers in the block (descending positions 0..F_{b-1}-1)
External group: the smallest F_{b-2} numbers in the block (descending positions F_{b-1}..F_b-1)

Uses a segmented sieve — only one block lives in memory at a time.
"""

import csv
import math
import time

MAX_BLOCK   = 44
OUTPUT_FILE = "prime_groups.csv"

FIBS_SET  = {0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987,
             1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368, 75025}
LUCAS_SET = {1, 2, 3, 4, 7, 11, 18, 29, 47, 76, 123, 199, 322, 521, 843}


def _build_fibs(n):
    fibs = [1, 1]
    while len(fibs) < n:
        fibs.append(fibs[-1] + fibs[-2])
    return fibs


def _small_primes(limit):
    sieve = bytearray([1]) * (limit + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(limit ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i :: i] = b"\x00" * len(sieve[i * i :: i])
    return [i for i in range(2, limit + 1) if sieve[i]]


def _block_primality(low, high, small_primes):
    size = high - low + 1
    arr  = bytearray([1]) * size
    if low <= 1 <= high:
        arr[1 - low] = 0
    for p in small_primes:
        if p * p > high:
            break
        start = max(p * p, ((low + p - 1) // p) * p)
        arr[start - low :: p] = b"\x00" * len(arr[start - low :: p])
    return arr


def _tag(n):
    if n in FIBS_SET:  return "fib"
    if n in LUCAS_SET: return "lucas"
    return ""


def run():
    fibs    = _build_fibs(MAX_BLOCK + 3)
    max_num = fibs[MAX_BLOCK + 1] - 1
    print(f"Pre-computing small primes up to {int(math.isqrt(max_num)) + 1:,}...")
    small_primes = _small_primes(int(math.isqrt(max_num)) + 1)
    print(f"  {len(small_primes):,} primes ready.\n")

    fieldnames = [
        "bloque", "size_bloque", "low", "high",
        "size_interno", "size_externo",
        "total_primos", "primos_interno", "primos_externo",
        "ratio_int_ext",
        "total_es", "interno_es", "externo_es",
        "time_s",
    ]

    current = 1
    total_start = time.time()

    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for b in range(1, MAX_BLOCK + 1):
            size_b   = fibs[b - 1]                      # F_b
            size_int = fibs[b - 2] if b >= 2 else 0     # F_{b-1}
            size_ext = fibs[b - 3] if b >= 3 else size_b  # F_{b-2}

            low  = current
            high = current + size_b - 1

            t0   = time.time()
            prim = _block_primality(low, high, small_primes)

            # Number 1 treated as prime-like
            if low == 1:
                prim[0] = 1

            # In ascending order:
            #   external group = prim[:size_ext]  (smallest F_{b-2} numbers)
            #   internal group = prim[size_ext:]  (largest F_{b-1} numbers)
            p_ext   = sum(prim[:size_ext])
            p_int   = sum(prim[size_ext:])
            p_total = p_int + p_ext
            elapsed = time.time() - t0

            ratio = round(p_int / p_ext, 4) if p_ext > 0 else None

            row = {
                "bloque":        b,
                "size_bloque":   size_b,
                "low":           low,
                "high":          high,
                "size_interno":  size_int,
                "size_externo":  size_ext,
                "total_primos":  p_total,
                "primos_interno":p_int,
                "primos_externo":p_ext,
                "ratio_int_ext": ratio if ratio is not None else "",
                "total_es":      _tag(p_total),
                "interno_es":    _tag(p_int),
                "externo_es":    _tag(p_ext),
                "time_s":        round(elapsed, 3),
            }
            writer.writerow(row)
            f.flush()

            total_elapsed = time.time() - total_start
            ratio_str = f"{ratio:.4f}" if ratio is not None else "  --  "
            print(f"B{b:2d} | primos={p_total:>8,} | int={p_int:>7,} | ext={p_ext:>7,} | "
                  f"ratio={ratio_str} | {_tag(p_total):5} | {elapsed:.2f}s | tot={total_elapsed:.1f}s")

            current += size_b

    print(f"\nGuardado en {OUTPUT_FILE}")


if __name__ == "__main__":
    run()
