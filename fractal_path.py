"""
Coordenadas binarias dentro del fractal Fibonacci.

Cada bloque se divide recursivamente en:
  interior (0) — los F_{b-1} elementos más grandes
  exterior (1) — los F_{b-2} elementos más pequeños

La ruta de n es la representación de Zeckendorf (Fibonacci binario)
de su posición descendente dentro del bloque — no base 2 clásica,
pero sí cada dígito es 0 ó 1.

Algoritmo O(log n): idéntico a Zeckendorf greedy sobre la posición p.
"""


def _build_fibs(limit: int) -> list[int]:
    fibs = [1, 1]
    while fibs[-1] < limit:
        fibs.append(fibs[-1] + fibs[-2])
    return fibs


def fractal_path(n: int) -> list[int]:
    """
    Ruta binaria de n en el árbol fractal Fibonacci.

      0 → interior  (mitad más grande, F_{b-1} elementos)
      1 → exterior  (mitad más pequeña, F_{b-2} elementos)

    La ruta es equivalente a la representación de Zeckendorf de la
    posición descendente p = F_{b+2} - 1 - n dentro del bloque b,
    usando los Fibonacci F_{b-1}, F_{b-2}, ..., F_1.
    """
    fibs = _build_fibs(n + 2)

    # Encontrar bloque b: fibs[b] <= n <= fibs[b+1] - 1
    b = next(
        i for i in range(1, len(fibs) - 1)
        if fibs[i] <= n <= fibs[i + 1] - 1
    )

    # Posición desde el mayor (0 = elemento más grande del bloque)
    p = fibs[b + 1] - 1 - n

    # Descomposición greedy de p en Fibonacci: misma lógica que Zeckendorf
    #   bit 0 → p cabe en el interior  (F_{cur-1} elementos)
    #   bit 1 → p va al exterior       (restar el tamaño interior)
    path = []
    cur = b - 1  # fibs[cur] = tamaño del bloque actual

    while cur > 1:              # parar cuando tamaño = 1
        if p < fibs[cur - 1]:  # cabe en el interior
            path.append(0)
            cur -= 1
        else:                   # va al exterior
            path.append(1)
            p -= fibs[cur - 1]
            cur -= 2

    return path


def fractal_path_info(n: int) -> dict:
    """Devuelve ruta, bloque y posición descendente de n."""
    fibs = _build_fibs(n + 2)
    b = next(
        i for i in range(1, len(fibs) - 1)
        if fibs[i] <= n <= fibs[i + 1] - 1
    )
    p = fibs[b + 1] - 1 - n
    return {
        "n":      n,
        "bloque": b,               # bloque 1-indexado
        "rango":  (fibs[b], fibs[b + 1] - 1),
        "pos_desc": p,             # posición desde el mayor (0 = mayor)
        "ruta":   fractal_path(n),
    }


# ── Demo ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Verificar los ejemplos del bloque 4
    print("Bloque 4  [5, 6, 7]")
    for n in [7, 6, 5]:
        print(f"  {n} → {fractal_path(n)}")

    print("\nBloque 5  [8..12]")
    for n in [12, 11, 10, 9, 8]:
        print(f"  {n} → {fractal_path(n)}")

    print("\nBloque 6  [13..20]")
    for n in range(20, 12, -1):
        print(f"  {n} → {fractal_path(n)}")

    print("\nPor qué es Zeckendorf:")
    print("  p = posición descendente dentro del bloque")
    print("  bit 1 ↔ 'este Fibonacci está en la suma de p'")
    print("  bit 0 ↔ 'no está, bajar al siguiente Fibonacci'")
    print("  → la ruta es exactamente la representación de Zeckendorf de p")
