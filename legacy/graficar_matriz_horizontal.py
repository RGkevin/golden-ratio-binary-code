import matplotlib.pyplot as plt
import numpy as np


def graficar_matriz_horizontal(datos_fractal: dict, nombre_archivo: str = "1_matriz_patron_horizontal.png") -> None:
    bloques_validos = list(datos_fractal.keys())
    num_bloques = len(bloques_validos)
    ancho_maximo = max(len(datos_fractal[b]) for b in bloques_validos)

    matriz_visual = np.full((num_bloques, ancho_maximo), np.nan)

    for idx_fila, b in enumerate(bloques_validos):
        for idx_col, info in enumerate(datos_fractal[b]):
            matriz_visual[idx_fila, idx_col] = 1 if info["es_primo"] else 0

    plt.figure(figsize=(14, 6))
    plt.matshow(matriz_visual, cmap="Set3", fignum=1, origin='lower')
    plt.yticks(range(num_bloques), [f"Bloque {b}" for b in bloques_validos])
    plt.xlabel("Índice posicional dentro del Bloque (Eje Horizontal)")
    plt.ylabel("Bloques de Fibonacci")
    plt.title("Matriz Horizontal: Distribución de Primos (Zonas coloreadas de forma distinta)", pad=20)
    plt.grid(color='white', linestyle='-', linewidth=0.5)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(nombre_archivo, dpi=300)
    plt.close()
    print(f"Imagen de matriz horizontal guardada como: {nombre_archivo}")
