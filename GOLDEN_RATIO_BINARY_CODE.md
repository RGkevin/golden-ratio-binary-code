# Código Binario de Base Áurea

El Código Binario de Base Áurea es un sistema de numeración posicional
no estándar que mapea los números naturales en un mapa de bits de ceros(0) y unos (1).
Que utiliza valores de fibonacci como base en lugar de $2^n$.

| $n$   | 0 | 1 | 2 | 3 | 4  |
|-------|---|---|---|---|----|
| $2^n$ | 1 | 2 | 4 | 8 | 16 |
| $F_n$ | 0 | 1 | 1 | 2 | 3  |

---

## Sucesión de Fibonacci

La sucesión de Fibonacci $\{F_n\}$ se define por la siguiente recurrencia:

$$F_n = \begin{cases} 0 & \text{si } n = 0 \\ 1 & \text{si } n = 1 \\ F_{n-1} + F_{n-2} & \text{si } n \geq 2 \end{cases}$$

Generando la secuencia: $0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, \ldots$

### Fórmula Cerrada (Fórmula de Binet)

$$F_n = \frac{\phi^n - \psi^n}{\sqrt{5}}$$

donde $\phi = \dfrac{1 + \sqrt{5}}{2} \approx 1.6180\ldots$ (la proporción áurea) y $\psi = \dfrac{1 - \sqrt{5}}{2} \approx -0.6180\ldots$

### Propiedad Límite

$$\lim_{n \to \infty} \frac{F_{n+1}}{F_n} = \phi$$

---

Ejemplos de números naturales $N$ en base áurea (Fibonacci):

| 5 | 4 | 3 | 2 | 1 | n     |
|---|---|---|---|---|-------|
| 5 | 3 | 2 | 1 | 1 | $F_n$ |
|   |   |   |   |   | $N$   |
|   |   |   |   | 1 | 1     |
|   |   |   | 1 | 1 | 2     |
|   |   | 1 | 0 | 1 | 3     |
|   |   | 1 | 1 | 1 | 4     |
|   | 1 | 0 | 1 | 1 | 5     |
|   | 1 | 1 | 0 | 1 | 6     |
|   | 1 | 1 | 1 | 1 | 7     |
| 1 | 0 | 1 | 0 | 1 | 8     |
| 1 | 0 | 1 | 1 | 1 | 9     |
| 1 | 1 | 0 | 1 | 1 | 10    |
| 1 | 1 | 1 | 0 | 1 | 11    |
| 1 | 1 | 1 | 1 | 1 | 12    |

Nota como cada bloque de Fibonacci se representa como la union de las dos matrices anteriores.

Ejemplo:

**Bloque 3**

| 1 | 0 | 1 |
|---|---|---|
| 1 | 1 | 1 |

**Bloque 4**

| 1 | 0 | 1 | 1 |
|---|---|---|---|
| 1 | 1 | 0 | 1 |
| 1 | 1 | 1 | 1 |


**Bloque 5**

| 1 | 0 | 1 | 0 | 1 |
|---|---|---|---|---|
| 1 | 0 | 1 | 1 | 1 |
| 1 | 1 | 0 | 1 | 1 |
| 1 | 1 | 1 | 0 | 1 |
| 1 | 1 | 1 | 1 | 1 |

Nota como el bloque 5 se compone del bloque 3 y el bloque 4, uno sobre el otro.
Con la diferencia que, para el bloque 3 se le agrega `10` y para el bloque 4 se le agrega un `1` a la izquierda.

## Encontrando el bloque para un número natural $N_n$

La longitud de la cadena de bits se expande cada vez que se salta a un nuevo bloque, distribuyéndose de la siguiente forma:
* Bloque 1 (Tamaño $F_1 = 1$): Contiene al 1
* Bloque 2 (Tamaño $F_2 = 1$): Contiene al 2
* Bloque 3 (Tamaño $F_3 = 2$): Contiene al 3 y 4
* Bloque 4 (Tamaño $F_4 = 3$): Contiene al 5, 6 y 7
* Bloque 5 (Tamaño $F_5 = 5$): Contiene del 8 al 12
* Bloque 6 (Tamaño $F_6 = 8$): Contiene del 13 al 20

#### Núcleo Algorítmico ($O(1)$)

Para determinar instantáneamente en qué bloque o escalón de Fibonacci ($x$) se encuentra cualquier número natural ($b$) sin necesidad de iterar ni generar la secuencia, se utiliza la inversa matemática del crecimiento áureo mediante logaritmos y la constante de Binet:Función de Localización de Bloque$$x = \lfloor \log_{\phi}((b + 1) \cdot \sqrt{5}) \rfloor - 1$$

Implementación de Referencia (JavaScript)
```js
/**
 * Calcula el argumento de Fibonacci (escalón del fractal) para un número dado.
 * @param {number} b - El número natural a evaluar.
 * @returns {number} El índice x de Fibonacci correspondiente al bloque.
 */
function obtenerBloqueKav(b) {
    if (b <= 0) return 0;
    if (b === 1) return 1; 
    if (b === 2) return 2; 
    
    const PHI = (1 + Math.sqrt(5)) / 2;
    const argumento = (b + 1) * Math.sqrt(5);
    
    // Mapeo directo en tiempo constante utilizando logaritmo de base áurea
    const x = Math.floor(Math.log(argumento) / Math.log(PHI)) - 1;
    
    return x;
}
```

### Obteniendo la forma binaria en base áurea de un número natural

El algoritmo se apoya directamente en la estructura recursiva de bloques descrita anteriormente.

#### Paso 1 — Localizar el bloque

Dado $N$, encontrar el bloque $b$ tal que $F_{b+1} \leq N \leq F_{b+2} - 1$.

Con la fórmula de localización del núcleo algorítmico ($O(1)$):

$$b = \left\lfloor \log_{\phi}\left((N + 1) \cdot \sqrt{5}\right) \right\rfloor - 1$$

El resultado $b$ es el bloque y además indica la longitud en bits de la representación.

#### Paso 2 — Calcular la posición dentro del bloque

$$\text{pos} = N - F_{b+1}$$

`pos` es el índice base-0 del elemento dentro del bloque $b$.

#### Paso 3 — Codificación recursiva

La cadena de bits se construye navegando la estructura fractal del bloque:

$$\text{codificar}(b,\, \text{pos}) = \begin{cases}
\texttt{"1"} & \text{si } b = 1 \\
\texttt{"11"} & \text{si } b = 2 \\
\texttt{"10"} + \text{codificar}(b-2,\; \text{pos}) & \text{si } b \geq 3 \text{ y } \text{pos} < F_{b-2} \\
\texttt{"1"} + \text{codificar}(b-1,\; \text{pos} - F_{b-2}) & \text{si } b \geq 3 \text{ y } \text{pos} \geq F_{b-2}
\end{cases}$$

Los primeros $F_{b-2}$ elementos del bloque $b$ provienen del bloque $b-2$ con `10` a la izquierda.  
Los siguientes $F_{b-1}$ elementos provienen del bloque $b-1$ con `1` a la izquierda.  
Esto refleja la identidad $F_b = F_{b-2} + F_{b-1}$.

#### Ejemplo: $N = 5$

1. **Bloque:** $b = \lfloor \log_{\phi}(6\sqrt{5}) \rfloor - 1 = 4$
2. **Posición:** $\text{pos} = 5 - F_5 = 5 - 5 = 0$
3. **Codificación:**
   - $\text{codificar}(4,\; 0)$: como $\text{pos}=0 < F_2=1$ → $\texttt{"10"} + \text{codificar}(2,\; 0)$
   - $\text{codificar}(2,\; 0) = \texttt{"11"}$
   - Resultado: $\texttt{"10"} + \texttt{"11"} = \texttt{"1011"}$

$$5 = F_4 + F_2 + F_1 = 3 + 1 + 1 \checkmark$$

#### Implementación de referencia (Python)

```python
import math

PHI = (1 + math.sqrt(5)) / 2
SQRT5 = math.sqrt(5)


def _generate_fibs(n):
    fibs = [1, 1]
    while fibs[-1] <= n:
        fibs.append(fibs[-1] + fibs[-2])
    return fibs


def find_block(n, fibs):
    if n == 1:
        return 1
    b = int(math.log((n + 1) * SQRT5) / math.log(PHI)) - 1
    while b > 1 and fibs[b] > n:
        b -= 1
    while b + 1 < len(fibs) and fibs[b + 1] <= n:
        b += 1
    return b


def _encode_block(b, pos, fibs):
    if b == 1:
        return "1"
    if b == 2:
        return "11"
    f_b_minus_2 = fibs[b - 3]
    if pos < f_b_minus_2:
        return "10" + _encode_block(b - 2, pos, fibs)
    return "1" + _encode_block(b - 1, pos - f_b_minus_2, fibs)


def to_golden_ratio_binary(n):
    fibs = _generate_fibs(n)
    b = find_block(n, fibs)
    pos = n - fibs[b]
    return _encode_block(b, pos, fibs)
```

#### Tabla completa (N = 1 … 12)

| $N$ | Bloque | bits | Representación |
|-----|--------|------|----------------|
| 1   | 1      | 1    | `1`            |
| 2   | 2      | 2    | `11`           |
| 3   | 3      | 3    | `101`          |
| 4   | 3      | 3    | `111`          |
| 5   | 4      | 4    | `1011`         |
| 6   | 4      | 4    | `1101`         |
| 7   | 4      | 4    | `1111`         |
| 8   | 5      | 5    | `10101`        |
| 9   | 5      | 5    | `10111`        |
| 10  | 5      | 5    | `11011`        |
| 11  | 5      | 5    | `11101`        |
| 12  | 5      | 5    | `11111`        |
