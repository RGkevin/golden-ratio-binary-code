from typing import List


def generar_fibonacci(n: int) -> List[int]:
    """Genera los primeros n números de la sucesión de Fibonacci."""
    fib = [0] * (n + 1)
    if n >= 1: fib[1] = 1
    for i in range(2, n + 1):
        fib[i] = fib[i - 1] + fib[i - 2]
    return fib