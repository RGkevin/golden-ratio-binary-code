import math


def encontrar_bloque_fibonacci(n):
    phi = (1 + math.sqrt(5)) / 2
    argumento = (n + 1) * math.sqrt(5)
    x = math.floor(math.log(argumento) / math.log(phi)) - 1

    return x