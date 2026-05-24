from golden_ratio_binary_code import (
    to_golden_ratio_binary,
    to_golden_ratio_binary_iterative,
    _generate_fibs,
    find_block,
)


def main():
    print("=== Código Binario de Base Áurea — Bloques 1 al 4 (N = 1…7) ===\n")

    # Bloques 1-4 corresponden a N=1..7
    header = f"{'N':>3} | {'Bloque':>6} | {'Recursivo':>12} | {'Iterativo':>12} | {'Igual':>5}"
    sep = "-" * len(header)
    print(header)
    print(sep)

    for n in range(1, 13):
        fibs = _generate_fibs(n)
        bloque = find_block(n, fibs)
        rec = to_golden_ratio_binary(n)
        ite = to_golden_ratio_binary_iterative(n)
        igual = "✓" if rec == ite else "✗"
        print(f"{n:>3} | {bloque:>6} | {rec:>12} | {ite:>12} | {igual:>5}")

    # Ejemplo específico del enunciado
    n = 5
    print(f"to_golden_ratio_binary({n})            = {to_golden_ratio_binary(n)}")
    print(f"to_golden_ratio_binary_iterative({n})  = {to_golden_ratio_binary_iterative(n)}")


if __name__ == "__main__":
    main()
