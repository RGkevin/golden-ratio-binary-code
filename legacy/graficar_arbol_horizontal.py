import matplotlib.pyplot as plt


def graficar_arbol_horizontal(datos_fractal: dict, nombre_archivo: str = "2_arbol_binario_horizontal.png") -> None:
    plt.figure(figsize=(16, 10))

    for b, filas in datos_fractal.items():
        for info in filas:
            ruta = info["ruta"]
            es_primo = info["es_primo"]

            x = [0]
            y = [b]
            y_actual = b

            for idx, bit in enumerate(ruta):
                x.append(idx + 1)
                desvío = 0.15 / (idx + 1)
                if bit == '1':
                    y_actual += desvío
                else:
                    y_actual -= desvío
                y.append(y_actual)

            color_rama = '#ff4d4d' if es_primo else '#b0c4de'
            alpha_rama = 0.8 if es_primo else 0.2
            linewidth_rama = 1.5 if es_primo else 0.6

            plt.plot(x, y, color=color_rama, alpha=alpha_rama, linewidth=linewidth_rama)

            if es_primo:
                plt.scatter(x[-1], y[-1], color='red', s=15, zorder=5)

    plt.xlabel("Profundidad de la Ruta Fractal (Bits de izquierda a derecha)")
    plt.ylabel("Eje de Bloques")
    plt.title("Estructura de Árbol Binario Horizontal (Ramas Rojas = Caminos a Números Primos)", pad=15)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.savefig(nombre_archivo, dpi=300)
    plt.close()
    print(f"Imagen del árbol horizontal guardada como: {nombre_archivo}")
