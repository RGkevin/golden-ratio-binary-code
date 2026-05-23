import matplotlib.pyplot as plt
import numpy as np


def graficar_simetria_espejo():
    # El Bloque 8 va desde el número 34 al 54 (Tiene 21 elementos)
    # Posición indexada en la matriz (de 0 a 20)
    # Número 37 -> Ruta 0100 -> Está en la posición índice 3 dentro del bloque
    # Número 43 -> Ruta 1001 -> Está en la posición índice 9 dentro del bloque

    ancho_bloque = 21
    # Creamos una fila vacía (rellena de ceros)
    fila_bloque_8 = np.zeros(ancho_bloque)

    # Marcamos con valores diferentes cada camino para que tengan colores distintos
    fila_bloque_8[3] = 1  # Camino del 37 (Izquierda-Derecha-Izquierda-Izquierda)
    fila_bloque_8[9] = 2  # Camino del 43 (Derecha-Izquierda-Izquierda-Derecha)

    # Convertimos en una matriz 2D para que matshow pueda dibujarla como una barra
    matriz_visual = np.array([fila_bloque_8])

    plt.figure(figsize=(12, 3))

    # Graficamos la matriz
    cax = plt.imshow(matriz_visual, cmap="Pastel1", aspect="auto")

    # Configurar el eje X para mostrar los números reales del Bloque 8 (34 al 54)
    numeros_bloque = list(range(34, 55))
    plt.xticks(range(ancho_bloque), numeros_bloque)
    plt.yticks([])  # Ocultamos el eje Y ya que es una sola fila

    # Añadir etiquetas de texto sobre las celdas exactas para ver las rutas
    plt.text(3, 0, "37\n(0100)", ha="center", va="center", color="black", weight="bold")
    plt.text(9, 0, "43\n(1001)", ha="center", va="center", color="black", weight="bold")

    plt.title("Simetría Fractal Inversa: Posición de los Caminos 37 y 43 en el Bloque 8", pad=15)
    plt.xlabel("Números Naturales dentro del Bloque")

    # Cuadrícula para delimitar los casilleros
    plt.grid(color='white', linestyle='-', linewidth=2, which='major')

    plt.tight_layout()
    nombre_archivo = "simetria_37_43_bloque8.png"
    plt.savefig(nombre_archivo, dpi=300)
    plt.close()
    print(f"Gráfica de simetría guardada como: {nombre_archivo}")


if __name__ == "__main__":
    graficar_simetria_espejo()