from math_core import exportar_datos_bloques
from graficar_matriz_horizontal import graficar_matriz_horizontal

CANTIDAD_DE_BLOQUES = 12

if __name__ == "__main__":
    print(f"Procesando {CANTIDAD_DE_BLOQUES} bloques...")
    datos = exportar_datos_bloques(CANTIDAD_DE_BLOQUES)

    graficar_matriz_horizontal(datos, "1_matriz_patron_horizontal.png")

    print("¡Proceso completado!")
