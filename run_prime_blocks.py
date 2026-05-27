from prime_block_pattern import build_prime_block_pattern

nums, prim = build_prime_block_pattern(10)

for b, (ns, ps) in enumerate(zip(nums, prim), start=1):
    print(f"Bloque {b:2d} | números:   {ns}")
    print(f"         | primality: {ps}")
    print()
