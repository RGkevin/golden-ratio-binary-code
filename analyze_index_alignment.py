"""
Analyzes prime index alignment between consecutive Fibonacci blocks.

For each pair (B_b, B_{b+1}), finds all prime pairs (p at index i in B_b,
q at index j in B_{b+1}) where |i - j| <= 1 (same or adjacent index).

Reports:
  - How many aligned pairs exist per block transition
  - Whether any transition has ZERO aligned pairs (the pattern "breaks")
  - The min/max diff for aligned pairs (should be F_{b+1} ± 1)
"""

from prime_block_pattern import build_prime_block_pattern

MAX_BLOCKS = 20

nums, prim = build_prime_block_pattern(MAX_BLOCKS)

FIBS = [1, 1]
while len(FIBS) < MAX_BLOCKS + 2:
    FIBS.append(FIBS[-1] + FIBS[-2])

print(f"{'Transición':<12} {'F_b+1':>8} {'Pares':>6} {'Mismo idx':>10} {'Adj idx':>8} {'Min diff':>9} {'Max diff':>9}  Estado")
print("-" * 80)

all_aligned = True

for b in range(1, MAX_BLOCKS):  # b = 1..19, transition b → b+1
    primes_b  = [(i, nums[b-1][i]) for i, p in enumerate(prim[b-1]) if p]
    primes_b1 = [(i, nums[b][i])   for i, p in enumerate(prim[b])   if p]

    idx_b  = {i: v for i, v in primes_b}
    idx_b1 = {i: v for i, v in primes_b1}

    same_idx  = []
    adj_idx   = []

    for i, p in primes_b:
        for j, q in primes_b1:
            delta = abs(i - j)
            if delta == 0:
                same_idx.append((i, j, p, q, q - p))
            elif delta == 1:
                adj_idx.append((i, j, p, q, q - p))

    total_pairs = len(same_idx) + len(adj_idx)
    all_diffs   = [d for *_, d in same_idx + adj_idx]
    min_diff    = min(all_diffs) if all_diffs else None
    max_diff    = max(all_diffs) if all_diffs else None
    fib_next    = FIBS[b]   # F_{b+1} (0-indexed fibs: FIBS[0]=1,FIBS[1]=1,...)

    status = "OK" if total_pairs > 0 else "*** ROMPE ***"
    if total_pairs == 0:
        all_aligned = False

    min_str = str(min_diff) if min_diff is not None else "--"
    max_str = str(max_diff) if max_diff is not None else "--"

    print(f"B{b:2d}→B{b+1:<2d}     {fib_next:>8,} {total_pairs:>6}  {len(same_idx):>10}  {len(adj_idx):>7}  {min_str:>9}  {max_str:>9}  {status}")

print("-" * 80)
if all_aligned:
    print("\nResultado: NUNCA se rompe. Cada transicion tiene al menos un par alineado (mismo o indice adyacente).")
else:
    print("\nResultado: Hay transiciones donde NO hay ningun par alineado.")

# Detail for interesting transitions
print("\n--- Detalle de las primeras 5 transiciones ---")
for b in range(1, min(6, MAX_BLOCKS)):
    primes_b  = [(i, nums[b-1][i]) for i, p in enumerate(prim[b-1]) if p]
    primes_b1 = [(i, nums[b][i])   for i, p in enumerate(prim[b])   if p]

    same_idx = []
    adj_idx  = []
    for i, p in primes_b:
        for j, q in primes_b1:
            delta = abs(i - j)
            if delta == 0:
                same_idx.append((i, j, p, q))
            elif delta == 1:
                adj_idx.append((i, j, p, q))

    print(f"\nB{b}→B{b+1}:")
    print(f"  Primos B{b}:   " + "  ".join(f"[{i}]={v}" for i, v in primes_b))
    print(f"  Primos B{b+1}: " + "  ".join(f"[{i}]={v}" for i, v in primes_b1))
    for i, j, p, q in same_idx:
        print(f"    Mismo  [{i}]→[{j}]: {p} y {q} (diff={q-p})")
    for i, j, p, q in adj_idx:
        print(f"    Adyac  [{i}]→[{j}]: {p} y {q} (diff={q-p})")
