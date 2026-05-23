import matplotlib.pyplot as plt
import numpy as np
import sympy
from typing import Dict, List, Tuple, Any


# =========================================================================
# 1. MÓDULO DE PROCESAMIENTO MATEMÁTICO Y EXPORTACIÓN
# =========================================================================

def generar_fibonacci(n: int) -> List[int]:
    """Genera los primeros n números de la sucesión de Fibonacci."""
    fib = [0] * (n + 1)
    if n >= 1: fib[1] = 1
    for i in range(2, n + 1):
        fib[i] = fib[i - 1] + fib[i - 2]
    return fib


def descomponer_subbloques(tamano_bloque: int) -> Tuple[int, int]:
    """
    Descompone el tamaño de un bloque en sus dos proporciones de Fibonacci previas (F_{n-2} y F_{n-1}).
    Si el tamaño no es un número exacto de Fibonacci puro, aproxima por proporción áurea.
    """
    if tamano_bloque <= 1:
        return 0, tamano_bloque

    # Encontrar los números de Fibonacci más cercanos que sumen el tamaño actual
    a, b = 1, 1
    while a + b != tamano_bloque:
        a, b = b, a + b
        if b > tamano_bloque:
            # Caso de salvaguarda por redondeo: división áurea estándar
            izq = int(tamano_bloque * 0.381966)
            return izq, tamano_bloque - izq
    return a, b


def calcular_ruta_recursiva(numero: int, inicio: int, tamano_izq: int, tamano_der: int,
                            ruta_acumulada: str = "") -> str:
    """
    Calcula de forma recursiva la ruta binaria exacta de un número natural
    dentro de su correspondiente bloque espacial de Fibonacci.
    '0' = Izquierda (subgrupo menor), '1' = Derecha (subgrupo mayor).
    """
    # Condición de parada: hemos alcanzado el nivel mínimo de subdivisión espacial
    if tamano_izq + tamano_der <= 1:
        return ruta_acumulada

    punto_corte = inicio + tamano_izq

    if numero < punto_corte:
        # El número habita en el sector izquierdo
        nuevo_izq, nuevo_der = descomponer_subbloques(tamano_izq)
        return calcular_ruta_recursiva(numero, inicio, nuevo_izq, nuevo_der, ruta_acumulada + "0")
    else:
        # El número habita en el sector derecho
        nuevo_izq, nuevo_der = descomponer_subbloques(tamano_der)
        return calcular_ruta_recursiva(numero, punto_corte, nuevo_izq, nuevo_der, ruta_acumulada + "1")


def exportar_datos_fractal(bloques_totales: int) -> Dict[int, List[Dict[str, Any]]]:
    """
    Procesa un rango de bloques definido y exporta un diccionario estructurado
    con el Número, su Primalidad y su Código de Ruta Binario.
    """
    fib = generar_fibonacci(bloques_totales)
    datos_estructurados = {}
    inicio_bloque = 1

    for b in range(1, bloques_totales + 1):
        f_n = fib[b]
        fin_bloque = inicio_bloque + f_n - 1

        # Omitimos bloques iniciales sin capacidad de ramificación real (F_n <= 1)
        if f_n > 1:
            tamano_izq = fib[b - 2]
            tamano_der = fib[b - 1]

            datos_bloque = []
            for num in range(inicio_bloque, fin_bloque + 1):
                ruta = calcular_ruta_recursiva(num, inicio_bloque, tamano_izq, tamano_der)
                es_primo = sympy.isprime(num)

                datos_bloque.append({
                    "numero": num,
                    "ruta": ruta,
                    "es_primo": es_primo
                })
            datos_estructurados[b] = datos_bloque

        inicio_bloque = fin_bloque + 1

    return datos_estructurados


# =========================================================================
# 2. MÓDULO DE GRAFICACIÓN HORIZONTAL
# =========================================================================

def graficar_matriz_horizontal(datos: Dict[int, List[Dict[str, Any]]], archivo_salida: str = "matriz_horizontal.png"):
    """
    Grafica el patrón binario de forma estrictamente horizontal.
    Cada fila representa un bloque de Fibonacci completo, permitiendo comparar
    la densidad posicional de los números primos.
    """
    bloques_validos = list(datos.keys())
    num_filas = len(bloques_validos)
    ancho_maximo = max(len(datos[b]) for b in bloques_validos)

    # Creamos una matriz rellena de NaN para el fondo vacío
    matriz_puntos = np.full((num_filas, ancho_maximo), np.nan)

    for idx_fila, b in enumerate(bloques_validos):
        for idx_col, info in enumerate(datos[b]):
            # Asignamos 1 para Números Primos y 0 para Números Compuestos
            matriz_puntos[idx_fila, idx_col] = 1 if info["es_primo"] else 0

    fig, ax = plt.subplots(figsize=(14, 7))
    # Usamos matshow para mapear la matriz horizontalmente
    cax = ax.matshow(matriz_puntos, cmap="RdYlBu_r", origin="lower", aspect="auto")

    # Formateo de ejes y etiquetas
    ax.set_yticks(range(num_filas))
    ax.set_yticklabels([f"Bloque {b} (F_{b})" for b in bloques_validos])
    ax.set_xlabel("Índice Posicional Secuencial Dentro del Bloque (Eje Horizontal X)")
    ax.set_ylabel("Bloques de Fibonacci (Eje Vertical Y)")
    ax.set_title("Visualización Horizontal: Distribución de Primos (Rojo) vs Compuestos (Azul)", pad=20, weight="bold")

    # Líneas divisorias de cuadrícula para aislar las celdas limpiamente
    ax.grid(color="white", linestyle="-", linewidth=1)

    plt.tight_layout()
    plt.savefig(archivo_salida, dpi=300)
    plt.close()
    print(f"-> Matriz horizontal guardada con éxito en: {archivo_salida}")


def graficar_arbol_horizontal(datos: Dict[int, List[Dict[str, Any]]], archivo_salida: str = "arbol_horizontal.png"):
    """
    Grafica las trayectorias de las rutas binarias simulando un Árbol Binario Horizontal.
    La raíz inicia a la izquierda (X=0) y se expande en ramificaciones hacia la derecha (X++).
    Resalta los caminos que concluyen en números primos para evidenciar la Simetría Fractal Inversa.
    """
    plt.figure(figsize=(16, 9))

    for b, elementos in datos.items():
        for info in elementos:
            ruta = info["ruta"]
            es_primo = info["es_primo"]

            # Coordenadas iniciales (Cada bloque parte desde su base entera en el eje Y)
            x = [0]
            y = [b]

            y_actual = b
            # Construcción paso a paso del camino de izquierda a derecha
            for nivel, bit in enumerate(ruta):
                x.append(nivel + 1)

                # Factor de desvío geométrico decreciente según la profundidad del nivel
                desvio = 0.2 / (nivel + 1)
                if bit == '1':
                    y_actual += desvio  # Giro a la Derecha mapea hacia arriba en el sub-árbol
                else:
                    y_actual -= desvio  # Giro a la Izquierda mapea hacia abajo en el sub-árbol
                y.append(y_actual)

            # Estilizado dinámico basado en Primalidad (Destacar pasillos cuánticos de Primos)
            if es_primo:
                color_linea = "#ff3333"  # Rojo Intenso
                alpha_linea = 0.85
                grosor_linea = 1.3
            else:
                color_linea = "#4a6984"  # Gris/Azul tenue para atenuar compuestos
                alpha_linea = 0.15
                grosor_linea = 0.5

            plt.plot(x, y, color=color_linea, alpha=alpha_linea, linewidth=grosor_linea)

            # Si el nodo terminal es primo, dibujamos el punto de anclaje final
            if es_primo:
                plt.scatter(x[-1], y[-1], color="#cc0000", s=12, zorder=5)

    plt.title("Estructura de Árbol Binario Horizontal Basado en Fibonacci", fontsize=14, weight="bold", pad=15)
    plt.xlabel("Profundidad de la Ruta (Bits evaluados de Izquierda a Derecha)")
    plt.ylabel("Eje Vertical de Bloques Estructurales")
    plt.grid(True, linestyle="--", alpha=0.5, color="#cccccc")

    plt.tight_layout()
    plt.savefig(archivo_salida, dpi=300)
    plt.close()
    print(f"-> Árbol binario horizontal guardado con éxito en: {archivo_salida}")


# =========================================================================
# 3. EJECUCIÓN DEL SISTEMA
# =========================================================================

if __name__ == "__main__":
    # Define cuántos bloques quieres mapear.
    # El bloque 12 o 13 es perfecto para apreciar patrones sin saturar los gráficos.
    BLOQUES_A_INCLUIR = 12

    print(f"======= INICIANDO PROCESAMIENTO MATEMÁTICO (N = {BLOQUES_A_INCLUIR}) =======")

    # Ejecutamos módulo 1: Procesar y estructurar datos binarios y primos
    datos_fractal = exportar_datos_fractal(BLOQUES_A_INCLUIR)
    print(datos_fractal)

    print("\n======= GENERANDO PIEZAS GRÁFICAS HORIZONTALES =======")
    # Ejecutamos módulo 2: Renderizar imágenes
    graficar_matriz_horizontal(datos_fractal, "1_secuencia_matriz_horizontal.png")
    graficar_arbol_horizontal(datos_fractal, "2_arbol_fractal_horizontal.png")

    print("\n[PROCESO TERMINADO] Las imágenes horizontales se han exportado a tu directorio actual.")