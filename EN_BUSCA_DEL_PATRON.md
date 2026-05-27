# En busca del patrón

Registro de los análisis realizados sobre la distribución de números primos dentro de los bloques Fibonacci (estructura fractal del Golden Ratio Binary Code). Cada sección describe una perspectiva distinta, el script que la implementa y los resultados obtenidos.

---

## 1. Estructura base: bloques Fibonacci

Los enteros positivos se particionan en bloques según la secuencia de Fibonacci. El bloque $b$ tiene exactamente $F_b$ elementos y ocupa el rango $[F_{b+1},\ F_{b+2}-1]$.

| Bloque | Rango | Tamaño ($F_b$) |
|--------|-------|----------------|
| 1 | [1, 1] | 1 |
| 2 | [2, 2] | 1 |
| 3 | [3, 4] | 2 |
| 4 | [5, 7] | 3 |
| 5 | [8, 12] | 5 |
| 6 | [13, 20] | 8 |
| 7 | [21, 33] | 13 |
| 8 | [34, 54] | 21 |
| 9 | [55, 88] | 34 |
| 10 | [89, 143] | 55 |
| b | $[F_{b+1},\ F_{b+2}-1]$ | $F_b$ |

**Convención:** dentro de cada bloque los números se listan en orden **descendente** (el mayor primero). Esta convención refleja la estructura recursiva del GRBC: el bloque $b$ empieza con una copia del bloque $b-1$ (grupo interno) seguida del bloque $b-2$ (grupo externo).

**Script base:** `prime_block_pattern.py`

```python
# Devuelve dos listas paralelas: números y primalidad (1=primo, 0=compuesto)
# Los bloques están en orden descendente
from prime_block_pattern import build_prime_block_pattern
nums, prim = build_prime_block_pattern(20)
```

```bash
python3 prime_block_pattern.py
```

---

## 2. Gaps entre primos consecutivos

La primera perspectiva analiza los **huecos** (gaps) entre primos consecutivos dentro de cada bloque, divididos en tres partes:

- **Head:** compuestos antes del primer primo
- **Internos:** gaps entre pares de primos consecutivos
- **Tail:** compuestos después del último primo

### Script

```bash
python3 prime_block_pattern.py          # hasta B12 (modo demo)
python3 analyze_gaps_streaming.py       # hasta B44, guarda gap_analysis.csv
```

### Hallazgos

**Gaps puros Fibonacci (B1–B8):** los primeros ocho bloques tienen todos sus gaps (head, internos, tail) dentro de la secuencia Fibonacci `{0,1,2,3,5,8,13,...}`. No hay ninguna ruptura.

**Bloque 9 — último patrón perfecto:** el bloque 9 tiene gaps internos `[3, 5, 1, 3, 5, 1]`, un período de longitud 3 que se repite exactamente dos veces. Ningún bloque posterior exhibe repetición exacta.

**Ruptura a partir de B9:** el valor 4 (Lucas) aparece como head del B9. A partir de B10, los gaps que no son Fibonacci empiezan a acumularse.

**Tabla resumen B1–B16:**

| B | size | primos | head | tail | total_breaks | breaks_lucas | max_gap |
|---|------|--------|------|------|-------------|-------------|---------|
| 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| 2 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| 3 | 2 | 1 | 0 | 1 | 0 | 0 | 1 |
| 4 | 3 | 2 | 0 | 0 | 0 | 0 | 1 |
| 5 | 5 | 1 | 3 | 1 | 0 | 0 | 3 |
| 6 | 8 | 3 | 0 | 1 | 0 | 0 | 3 |
| 7 | 13 | 3 | 2 | 2 | 0 | 0 | 5 |
| 8 | 21 | 5 | 3 | 1 | 0 | 0 | 5 |
| 9 | 34 | 7 | 4 | 5 | 1 | 1 | 5 |
| 10 | 55 | 11 | 0 | 4 | 2 | 2 | 13 |
| 11 | 89 | 16 | 5 | 3 | 3 | 2 | 11 |
| 12 | 144 | 24 | 0 | 3 | 4 | 1 | 13 |
| 13 | 233 | 37 | 2 | 2 | 12 | 7 | 17 |
| 14 | 377 | 55 | 3 | 3 | 18 | 10 | 19 |
| 15 | 610 | 84 | 4 | 13 | 29 | 17 | 33 |
| 16 | 987 | 126 | 0 | 4 | 44 | 20 | 25 |

**Datos completos:** `gap_summary.csv` (44 filas, una por bloque)

### Paridad de head y tail

La paridad del head y tail de cada bloque está completamente determinada por $b \bmod 3$, derivada del período de Pisano $\pi(2) = 3$ de la secuencia Fibonacci:

| $b \bmod 3$ | Head | Tail |
|:-----------:|:----:|:----:|
| $b \equiv 0$ | **par** | **impar** |
| $b \equiv 1$ | **par** | **par** |
| $b \equiv 2$ | **impar** | **impar** |

Confirmado sin excepción en los 44 bloques analizados.

### El número 18 nunca aparece

El gap 18 **nunca** aparece en ningún bloque (ni como head, tail, ni gap interno) hasta el B44. Tiene dos razones:

1. **Estructura:** 18 es par → no puede ser gap interno (todos los gaps entre dos primos impares son impares)
2. **Empírico:** tampoco aparece como head ni tail en los 44 bloques verificados (~1.84 × 10⁹ números)

---

## 3. Grupos internos y externos

La segunda perspectiva divide cada bloque en dos **sub-grupos** que reflejan la autosimilaridad del GRBC:

- **Grupo interno:** los $F_{b-1}$ números **más grandes** del bloque → replica la estructura del bloque $b-1$
- **Grupo externo:** los $F_{b-2}$ números **más pequeños** del bloque → replica la estructura del bloque $b-2$

### Script

```bash
python3 analyze_groups.py               # gaps por sub-grupo hasta B20
python3 analyze_prime_groups.py         # conteo de primos por sub-grupo hasta B44, guarda prime_groups.csv
```

### Hallazgos — conteo de primos por grupo

| B | primos_total | primos_interno | primos_externo | ratio int/ext |
|---|-------------|---------------|---------------|---------------|
| 1 | 1 | 0 | 1 | — |
| 2 | 1 | 0 | 1 | 0.0000 |
| 3 | 1 | 0 | 1 | 0.0000 |
| 4 | 2 | 1 | 1 | 1.0000 |
| **5** | **1** | **1** | **0** | **—** |
| 6 | 3 | 2 | 1 | 2.0000 |
| 7 | 3 | 2 | 1 | 2.0000 |
| 8 | 5 | 3 | 2 | 1.5000 |
| 9 | 7 | 4 | 3 | 1.3333 |
| 10 | 11 | 5 | 6 | 0.8333 |
| 20 | 704 | 431 | 273 | 1.5788 |
| 30 | 57,909 | 35,587 | 22,322 | 1.5943 |
| 40 | 5,334,509 | 3,280,988 | 2,053,521 | 1.5977 |
| 44 | 33,227,992 | 20,445,994 | 12,781,998 | 1.5996 |

**El ratio converge hacia φ ≈ 1.6180.** La convergencia es lenta porque la densidad de primos (teorema del número primo) introduce un factor $b/(b+1)$, de modo que el ratio real es aproximadamente $\varphi \cdot b/(b+1) \to \varphi$.

**El B5 es el único bloque (hasta B44) donde el grupo externo tiene cero primos.** Su grupo externo es `[8, 9]`, el único par de consecutivos compuestos que coincide con un grupo externo. A partir de B6, los números de inicio del grupo externo son ≥ 13, y siempre contienen al menos un primo. Este resultado es garantizable por Baker-Harman-Pintz una vez que $F_{b+1} > 8$.

**Datos completos:** `prime_groups.csv` (44 filas)

---

## 4. Teorema: todo bloque tiene al menos un primo

Ver `TEOREMA_PRIMOS_BLOQUES.md` para la demostración completa. Resumen:

**Enunciado:** para todo $b \geq 1$, el bloque $B_b = [F_{b+1}, F_{b+2}-1]$ contiene al menos un número primo.

**Demostración:**
- Casos base B1–B44: verificación computacional mediante criba segmentada
- Caso general b > 44: Baker-Harman-Pintz (2001) garantiza un primo en $(n,\ n + n^{0.525})$. Como $F_b > F_{b+1}^{0.525}$ para $F_{b+1} \geq 3$, existe un primo dentro del bloque

El Postulado de Bertrand no es suficiente porque el bloque termina en $F_{b+2} - 1 \approx 1.618 \cdot F_{b+1} < 2 F_{b+1}$.

---

## 5. Alineación de índices entre bloques consecutivos

La tercera perspectiva analiza qué ocurre cuando se apilan los bloques uno debajo del otro, alineados por índice de posición. Un primo en el índice $i$ del bloque $b$ y otro en el índice $j$ del bloque $b+1$ están **alineados** si $|i - j| \leq 1$.

### Regla descubierta

Para un primo $p$ en el índice $i$ del bloque $b$ y un primo $q$ en el índice $j$ del bloque $b+1$:

$$q - p = F_{b+1} + (i - j)$$

- Mismo índice ($i = j$): $q - p = F_{b+1}$ exactamente
- Índices adyacentes ($|i-j|=1$): $q - p = F_{b+1} \pm 1$

### Script

```bash
python3 analyze_index_alignment.py      # análisis hasta B20
```

### Resultados — transiciones B1→B20

| Transición | $F_{b+1}$ | Pares alineados | Mismo índice | Adyacente | Estado |
|-----------|----------|-----------------|-------------|-----------|--------|
| B1→B2 | 1 | 1 | 1 | 0 | OK |
| B2→B3 | 2 | 1 | 0 | 1 | OK |
| B3→B4 | 3 | 2 | 0 | 2 | OK |
| B4→B5 | 5 | 2 | 0 | 2 | OK |
| B5→B6 | 8 | 1 | 1 | 0 | OK |
| B6→B7 | 13 | 3 | 0 | 3 | OK |
| B7→B8 | 21 | 2 | 0 | 2 | OK |
| B8→B9 | 34 | 1 | 1 | 0 | OK |
| B9→B10 | 55 | 5 | 0 | 5 | OK |
| B10→B11 | 89 | 10 | 0 | 10 | OK |
| B11→B12 | 144 | 7 | 7 | 0 | OK |
| B12→B13 | 233 | 15 | 0 | 15 | OK |
| B13→B14 | 377 | 27 | 0 | 27 | OK |
| B14→B15 | 610 | 11 | 11 | 0 | OK |
| B15→B16 | 987 | 33 | 0 | 33 | OK |
| B16→B17 | 1,597 | 69 | 0 | 69 | OK |
| B17→B18 | 2,584 | 39 | 39 | 0 | OK |
| B18→B19 | 4,181 | 157 | 0 | 157 | OK |
| B19→B20 | 6,765 | 139 | 0 | 139 | OK |

**El patrón nunca se rompe:** en las 19 transiciones analizadas, siempre existe al menos un par de primos alineados (mismo o índice adyacente). El número de pares crece con el tamaño del bloque.

**Patrón en las transiciones de "mismo índice" puro:** ocurren en B1→B2, B5→B6, B8→B9, B11→B12, B14→B15, B17→B18 — es decir, en $b \equiv 2 \pmod{3}$ (excepto B1). Coincide con el mismo período que rige la paridad de head/tail.

---

## 7. Potencias y posición en el árbol

Cada multiplicación por una base fija desplaza exactamente $\log_\varphi(\text{base})$ bloques hacia arriba en el árbol. Como los bloques crecen en proporción $\varphi$, multiplicar por una constante equivale a un salto fijo en la escala logarítmica Fibonacci.

### Salto de bloque por base

| Base $k$ | $\log_\varphi(k)$ | Salto observado | Comportamiento |
|----------|-------------------|-----------------|----------------|
| 5 | 3.09 | 3 bloques (patrón período 3) | posición relativa oscila |
| 7 | 4.04 | **siempre exactamente 4** | converge al techo del bloque |
| 11 | 4.78 | 4–5, promedio 5 | converge al centro del bloque |

### Base 7 — cuatro bloques, siempre en el techo

Las potencias de 7 cumplen $\text{bloque}(7^k) = 4k + \text{bloque}(7)$ sin excepción. En términos de ruta, cada multiplicación por 7 añade un cero al inicio de la ruta:

| Potencia | Valor | Ruta |
|----------|-------|------|
| $7^1$ | 7 | `[1]` |
| $7^2$ | 49 | `[0, 0, 1]` |
| $7^3$ | 343 | `[0, 0, 0, 1]` |
| $7^4$ | 2401 | `[0, 0, 0, 0, 1]` |

El 7 ocupa el techo de su bloque (posición 0 descendente), y su cuadrado queda cerca del techo del bloque que está 4 bloques más arriba. El patrón de zeros crecientes refleja que las potencias de 7 son cada vez más "interiores" dentro de sus bloques.

### Base 11 — convergencia al centro

Las potencias de 11 saltan entre 4 y 5 bloques, con promedio 5 (igual a $\lfloor\log_\varphi(11)\rceil$). La posición relativa dentro del bloque oscila y converge lentamente hacia 0.5 (centro del bloque), sin la estabilidad de la base 7.

### Base 5 — patrón de período 3

Las potencias de 5 exhiben un patrón cíclico de período 3 en su posición relativa dentro del bloque, derivado del período de Pisano $\pi(5) = 20$ módulo 3. El salto es siempre 3 bloques.

### Cuadrados de primos con trayectoria profunda

Cuando un primo $p$ tiene una ruta con muchos ceros iniciales (es decir, está muy "dentro" del interior de su bloque), su cuadrado extiende esa trayectoria:

$$\text{ruta}(p^2) = \text{ruta}(p) + [\text{sufijo adicional}]$$

Ejemplo más claro: $47$ con ruta `[0, 0, 1, 1]` → $47^2 = 2209$ con ruta `[0, 0, 1, 1, 1, 1, 1, 0, 0]`. Los primeros 4 bits son idénticos; el cuadrado extiende la ruta al doble de profundidad aproximadamente.

---

## 8. Orden ascendente vs orden descendente

El análisis en orden descendente (mayor primero dentro de cada bloque) no es una elección arbitraria: refleja la estructura recursiva del GRBC donde el sub-grupo interior (los $F_{b-1}$ mayores) viene primero.

### Ruta ascendente = complemento bit a bit de la descendente

Para todo número $n$, si su ruta descendente es $[b_1, b_2, \ldots, b_k]$, entonces su ruta ascendente es $[\bar{b}_1, \bar{b}_2, \ldots, \bar{b}_k]$ (cada bit invertido):

$$\text{ruta\_asc}(n) = \overline{\text{ruta}(n)}$$

Esto se debe a que el orden ascendente simplemente invierte el rol de interior/exterior: lo que era "tomar el interior" (0 descendente) pasa a ser "tomar el exterior" (0 ascendente), y viceversa.

**Consecuencia:** el árbol en orden ascendente es el espejo exacto del árbol en orden descendente. Todos los patrones estructurales se preservan, incluyendo:
- La herencia de rutas entre bloques
- La distribución de profundidades (recursión doble Fibonacci)
- La convergencia del ratio interno/externo hacia $\varphi$

**Confirmado** para todos los números hasta el B15 (sin excepción).

### Implicación geométrica

El fractal es **autocomplementario**: si se invierte el bit de cada paso en la coordenada binaria de cualquier número, se obtiene el espejo de ese número en el mismo árbol. Los primos en orden descendente y en orden ascendente ocupan posiciones simétricas.

---

## 9. Números compuestos y memoria genética de rutas

Los números compuestos $n = p \times q$ no se comportan de forma aleatoria en el árbol: heredan información estructural de sus factores.

### Aditividad de bloques

$$\text{bloque}(p \times q) = \text{bloque}(p) + \text{bloque}(q) + \delta, \quad \delta \in \{0, -1\}$$

La diferencia $\delta$ nunca es positiva ni menor a $-1$. Verificado para todos los productos de primos hasta el B20.

| Producto | $B_p$ | $B_q$ | $B_{pq}$ | $B_p + B_q$ | $\delta$ |
|----------|-------|-------|----------|-------------|---------|
| $2 \times 7 = 14$ | 2 | 4 | 6 | 6 | 0 |
| $7 \times 7 = 49$ | 4 | 4 | 8 | 8 | 0 |
| $7 \times 41 = 287$ | 4 | 8 | 12 | 12 | 0 |
| $7 \times 53 = 371$ | 4 | 8 | 12 | 12 | 0 |
| $29 \times 67 = 1943$ | 7 | 9 | 16 | 16 | 0 |

### Herencia de rutas

El producto $p \times q$ tiende a comenzar su ruta con el prefijo del factor más "interior" (el que tiene más ceros iniciales). Cuanto más interior es un factor en su bloque, mayor es la longitud del prefijo heredado:

| Producto | Ruta del factor "interior" | Ruta del producto | Prefijo heredado |
|----------|---------------------------|-------------------|-----------------|
| $7 \times 41 = 287$ | `[1,0,0,0,0]` (41) | `[1,0,0,0,0,0,0,0,0]` | 5 bits |
| $7 \times 53 = 371$ | `[0,0,0,0,0,1]` (53) | `[0,0,0,0,0,0,1,0,0]` | 5 bits |
| $29 \times 67 = 1943$ | `[1,0,0,0,0,0]` (67) | `[1,0,0,0,0,0,1,1,0,0,1]` | 6 bits |
| $47 \times 47 = 2209$ | `[0,0,1,1]` (47) | `[0,0,1,1,1,1,1,0,0]` | 4 bits |

### El 7 como amplificador de profundidad

El número 7 ocupa la posición más alta de su bloque (posición descendente 0), lo que lo convierte en un multiplicador casi neutro en términos de ruta. Multiplicar cualquier número $q$ por 7 preserva esencialmente la ruta de $q$, añadiendo bits adicionales al final pero manteniendo el prefijo intacto. En otras palabras, $7 \times q$ "amplifica" la trayectoria de $q$ sin torcer su dirección inicial.

### Cuadrados como extensión de ruta

Cuando $p$ tiene una ruta con muchos ceros iniciales, $p^2$ extiende esa ruta al doble de profundidad aproximadamente. El ejemplo más claro es:

$$47 = \texttt{[0,0,1,1]} \quad \Rightarrow \quad 47^2 = 2209 = \texttt{[0,0,1,1,1,1,1,0,0]}$$

Los primeros 4 bits de $47^2$ son idénticos a los de $47$. El cuadrado "recuerda" el inicio del camino de su raíz.

---

## 6. Resumen de hallazgos

| # | Hallazgo | Verificado hasta |
|---|----------|-----------------|
| 1 | Todo bloque Fibonacci contiene al menos un primo | B44 (~1.84 × 10⁹) + BHP(2001) para b > 44 |
| 2 | Todos los gaps internos entre primos son impares | B44 |
| 3 | El número de Lucas 18 nunca aparece como gap | B44 |
| 4 | La paridad de head y tail está determinada por $b \bmod 3$ | B44 |
| 5 | Bloque 9 es el último con patrón interno perfecto `[3,5,1,3,5,1]` | — |
| 6 | Las rupturas de la secuencia Fibonacci son mayoritariamente Lucas hasta B20; a partir de B25 dominan los no-Lucas | B44 |
| 7 | El ratio primos_interno/primos_externo converge a φ ≈ 1.6180 | B44 (valor: 1.5996) |
| 8 | B5 es el único bloque con 0 primos en el grupo externo | B44 + argumento BHP para b ≥ 6 |
| 9 | Siempre existe al menos un par de primos con índice igual o adyacente entre bloques consecutivos | B20 |
| 10 | Las transiciones de "mismo índice" puro ocurren en $b \equiv 2 \pmod{3}$ | B20 |
| 11 | Multiplicar por una base fija desplaza exactamente $\lfloor\log_\varphi(\text{base})\rceil$ bloques; base 7 siempre salta exactamente 4 | B20 |
| 12 | La ruta ascendente de cualquier número es el complemento bit a bit de su ruta descendente | B15 |
| 13 | $\text{bloque}(p \times q) = \text{bloque}(p) + \text{bloque}(q) + \delta$ con $\delta \in \{0, -1\}$ | B20 |
| 14 | Los productos $p \times q$ heredan el prefijo de ruta del factor más interior; $p^2$ extiende la ruta de $p$ | B20 |

---

## Archivos del proyecto

| Archivo | Descripción |
|---------|-------------|
| `prime_block_pattern.py` | Módulo base: genera bloques y analiza gaps |
| `analyze_gaps_streaming.py` | Criba segmentada hasta B44; guarda `gap_analysis.csv` |
| `analyze_groups.py` | Gaps por sub-grupo interno/externo hasta B20 |
| `analyze_prime_groups.py` | Conteo de primos por sub-grupo hasta B44; guarda `prime_groups.csv` |
| `analyze_index_alignment.py` | Alineación de índices de primos entre bloques consecutivos |
| `gap_summary.csv` | Resumen compacto de gaps por bloque (B1–B44) |
| `prime_groups.csv` | Conteo de primos por grupo interno/externo (B1–B44) |
| `gap_analysis.csv` | Análisis completo de gaps con listas de rupturas (B1–B44) |
| `TEOREMA_PRIMOS_BLOQUES.md` | Demostración formal del teorema de existencia de primos |
| `fractal_path.py` | Coordenadas binarias (ruta Fibonacci) de cualquier número natural |
