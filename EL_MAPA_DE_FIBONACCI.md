# El mapa de Fibonacci

Sistema de coordenadas binarias para ubicar cualquier número natural dentro del fractal Fibonacci (Golden Ratio Binary Code).

---

## Definición

Cada bloque Fibonacci se divide recursivamente en dos sub-grupos:

- **Interior (0):** los $F_{b-1}$ elementos más grandes del bloque
- **Exterior (1):** los $F_{b-2}$ elementos más pequeños del bloque

Cada sub-grupo es a su vez un bloque Fibonacci anterior, y puede dividirse de la misma manera. La **ruta** de un número $n$ es la secuencia de bits que describe el camino desde la raíz del árbol hasta $n$:

$$\text{ruta}(n) = [b_1,\ b_2,\ b_3,\ \ldots]$$

donde $b_i = 0$ significa "tomar el interior" y $b_i = 1$ significa "tomar el exterior" en cada nivel de la división.

### Ejemplo — Bloque 4: [5, 6, 7]

```
Bloque 4  (tamaño 3)
├── Interior [0]  → {7, 6}
│   ├── Interior [0,0]  → {7}
│   └── Exterior [0,1]  → {6}
└── Exterior [1]  → {5}
```

| Número | Ruta |
|--------|------|
| 7 | `[0, 0]` |
| 6 | `[0, 1]` |
| 5 | `[1]` |

### Ejemplo — Bloque 5: [8..12]

| Número | Ruta |
|--------|------|
| 12 | `[0, 0, 0]` |
| 11 | `[0, 0, 1]` |
| 10 | `[0, 1]` |
| 9 | `[1, 0]` |
| 8 | `[1, 1]` |

---

## Algoritmo de cálculo

```python
def fractal_path(n: int) -> list[int]:
    fibs = _build_fibs(n + 2)

    # Encontrar bloque b: fibs[b] <= n <= fibs[b+1] - 1
    b = next(i for i in range(1, len(fibs) - 1) if fibs[i] <= n <= fibs[i+1] - 1)

    # Posición descendente dentro del bloque (0 = mayor)
    p = fibs[b + 1] - 1 - n

    path = []
    cur = b - 1  # fibs[cur] = tamaño del bloque actual

    while cur > 1:
        if p < fibs[cur - 1]:  # cabe en el interior
            path.append(0)
            cur -= 1
        else:                   # va al exterior
            path.append(1)
            p -= fibs[cur - 1]
            cur -= 2

    return path
```

**Complejidad:** $O(\log n)$ — tan rápido como es posible.

### Conexión con Zeckendorf

La ruta de $n$ es equivalente a la **representación de Zeckendorf** (Fibonacci binario) de su posición descendente dentro del bloque:

$$p = F_{b+2} - 1 - n$$

Cada bit $1$ indica que el Fibonacci correspondiente está en la descomposición de $p$; cada bit $0$ indica que no está. No es base 2 clásica — es base Fibonacci, donde cada posición vale un número de Fibonacci en lugar de una potencia de 2.

---

## Patrones descubiertos

### 1. Herencia de rutas

Toda ruta se construye sobre rutas de bloques anteriores. Para cualquier $n$ en el bloque $b$:

$$\text{ruta}(n) = [\text{bit}] + \text{ruta}(n - F_b)$$

donde el primer bit indica interior (0) o exterior (1), y el resto de la ruta es exactamente la ruta de $n - F_b$ en el bloque correspondiente. La diferencia $F_b$ es el desplazamiento entre el inicio del sub-grupo y el inicio del bloque anterior equivalente.

Confirmado sin excepción hasta el bloque 15.

### 2. Composición del conjunto de rutas

$$\text{paths}(B_b) = \{[0]+p \mid p \in \text{paths}(B_{b-1})\} \cup \{[1]+p \mid p \in \text{paths}(B_{b-2})\}$$

El conjunto de rutas del bloque $b$ se construye exactamente prefijando con `0` las rutas de $B_{b-1}$ y con `1` las rutas de $B_{b-2}$. La cantidad de rutas únicas por bloque sigue la secuencia Fibonacci: 1, 1, 2, 3, 5, 8, 13, 21, ...

### 3. Los dos más profundos

Los dos números con ruta más larga en el bloque $b$ son siempre $F_{b+2}-2$ y $F_{b+2}-1$ (los dos mayores del bloque), con longitud máxima $b-2$:

$$\text{ruta}(F_{b+2}-1) = [0, 0, \ldots, 0] \quad (b-2 \text{ ceros})$$
$$\text{ruta}(F_{b+2}-2) = [0, 0, \ldots, 0, 1] \quad (b-3 \text{ ceros y un 1 al final})$$

### 4. Los números Fibonacci son siempre todo-exterior

Todo número Fibonacci $F_k$ tiene ruta compuesta únicamente de $1$s. Son los números de **mínima profundidad** en su bloque. Además, dos Fibonacci consecutivos comparten la misma longitud de ruta:

| Fibonacci | Ruta | Longitud |
|-----------|------|----------|
| $F_3 = 3$, $F_4 = 5$ | `[1]` | 1 |
| $F_5 = 8$, $F_6 = 13$ | `[1, 1]` | 2 |
| $F_7 = 21$, $F_8 = 34$ | `[1, 1, 1]` | 3 |
| $F_9 = 55$, $F_{10} = 89$ | `[1, 1, 1, 1]` | 4 |
| $F_{2k-1},\ F_{2k}$ | $k-1$ unos | $k-1$ |

Los Fibonacci son las "entradas" más directas al fractal — llegan a su posición tomando siempre el exterior, sin ningún giro interior.

### 5. Distribución de profundidades — recursión doble Fibonacci

La cantidad de números con longitud de ruta $\ell$ en el bloque $b$ sigue:

$$\text{count}(b,\ \ell) = \text{count}(b-1,\ \ell-1) + \text{count}(b-2,\ \ell-1)$$

La misma regla que define la secuencia Fibonacci, pero aplicada en dos dimensiones: bloque y profundidad. En cada bloque, la distribución de profundidades es la suma de las distribuciones desplazadas de los dos bloques anteriores.

### 6. Profundidad mínima y máxima

Para el bloque $b$:

| | Fórmula | Descripción |
|--|---------|-------------|
| **Máxima profundidad** | $b - 2$ | Siempre 2 números (interior total) |
| **Mínima profundidad** | $\lceil (b-2)/2 \rceil$ | Exterior total, tomando el camino más corto |

En bloques pares, exactamente **1 número** tiene profundidad mínima: el inicio del bloque ($F_{b+1}$, un número Fibonacci).  
En bloques impares, hay **varios** números con profundidad mínima, pero el Fibonacci de inicio siempre es uno de ellos.

---

## Intuición geométrica

El mapa puede visualizarse como un árbol binario donde:

- La **raíz** no existe como número — es la división primordial
- Cada **nodo interno** es una bifurcación: rama izquierda (0 = interior, los más grandes) y rama derecha (1 = exterior, los más pequeños)
- Cada **hoja** es un número natural
- La **profundidad** de una hoja es la longitud de su ruta
- Los **números Fibonacci** son siempre hojas de mínima profundidad — la "orilla" del árbol

El árbol crece según la secuencia Fibonacci: cada nivel nuevo hereda la estructura completa de los dos niveles anteriores, prefijada con un bit.

---

## Archivo de implementación

`fractal_path.py` — función `fractal_path(n)` y `fractal_path_info(n)`

```bash
python3 fractal_path.py
```
