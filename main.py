from golden_ratio_binary_code import to_golden_ratio_binary


def main():
    print("=== Código Binario de Base Áurea ===\n")

    # Tabla con todos los ejemplos del documento (N = 1 al 12)
    header = f"{'N':>4} | {'bits':>6} | {'Representación':>15}"
    print(header)
    print("-" * len(header))

    for n in range(1, 13):
        result = to_golden_ratio_binary(n)
        print(f"{n:>4} | {len(result):>6} | {result:>15}")

    # Ejemplo específico del enunciado
    print()
    n = 5
    result = to_golden_ratio_binary(n)
    print(f"to_golden_ratio_binary({n}) = {result}")

    # Verificación adicional con valores más grandes
    print("\n=== Valores adicionales ===")
    for n in [13, 20, 21, 34, 55]:
        result = to_golden_ratio_binary(n)
        print(f"to_golden_ratio_binary({n:>3}) = {result}")


if __name__ == "__main__":
    main()
