import sympy


def generar_numeros_fibonacci(cantidad: int) -> list[int]:
    fib = [0] * (cantidad + 1)
    if cantidad >= 1:
        fib[1] = 1
    for i in range(2, cantidad + 1):
        fib[i] = fib[i - 1] + fib[i - 2]
    return fib


def descomponer_fibonacci(n: int) -> tuple[int, int]:
    if n <= 1:
        return 0, 1
    a, b = 1, 1
    while a + b != n:
        a, b = b, a + b
        if b > n:
            return n // 2, n - (n // 2)
    return a, b


def calcular_ruta_fractal(
    numero: int,
    inicio: int,
    tamano_izq: int,
    tamano_der: int,
    ruta_actual: str = "",
) -> str:
    if tamano_izq + tamano_der == 1:
        return ruta_actual
    punto_corte = inicio + tamano_izq
    if numero < punto_corte:
        nuevo_izq, nuevo_der = descomponer_fibonacci(tamano_izq)
        return calcular_ruta_fractal(numero, inicio, nuevo_izq, nuevo_der, ruta_actual + "0")
    else:
        nuevo_izq, nuevo_der = descomponer_fibonacci(tamano_der)
        return calcular_ruta_fractal(numero, punto_corte, nuevo_izq, nuevo_der, ruta_actual + "1")


def exportar_datos_bloques(cantidad_bloques: int) -> dict:
    fib = generar_numeros_fibonacci(cantidad_bloques)
    datos_fractal = {}
    inicio_bloque = 1

    for b in range(1, cantidad_bloques + 1):
        f_n = fib[b]
        fin_bloque = inicio_bloque + f_n - 1

        if f_n > 1:
            tamano_izq = fib[b - 2]
            tamano_der = fib[b - 1]

            datos_bloque = []
            for num in range(inicio_bloque, fin_bloque + 1):
                ruta = calcular_ruta_fractal(num, inicio_bloque, tamano_izq, tamano_der)
                es_primo = sympy.isprime(num)
                datos_bloque.append({
                    "numero": num,
                    "ruta": ruta,
                    "es_primo": es_primo,
                })
            datos_fractal[b] = datos_bloque

        inicio_bloque = fin_bloque + 1

    return datos_fractal
