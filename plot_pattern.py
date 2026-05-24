import subprocess

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap

from golden_ratio_binary_code import to_golden_ratio_binary_iterative

# ── Helpers ──────────────────────────────────────────────────────────────────

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

# ── Data ─────────────────────────────────────────────────────────────────────

FIBS   = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
MAX_N  = 143   # F12 - 1  (last element of block 10)
BITS   = 10    # block 10 → 10-bit strings

# Cell values: 0=empty(white)  1=filled non-prime(black)  2=filled prime(blue)
data = np.zeros((MAX_N, BITS), dtype=np.int8)

for n in range(1, MAX_N + 1):
    bits = to_golden_ratio_binary_iterative(n).zfill(BITS)
    fill = 2 if is_prime(n) else 1
    for col, bit in enumerate(bits):
        if bit == "1":
            data[n - 1, col] = fill

# ── Block metadata ────────────────────────────────────────────────────────────

block_starts_n  = [FIBS[b]     for b in range(1, 11)]   # first N of each block
block_ends_n    = [FIBS[b+1]-1 for b in range(1, 11)]   # last  N of each block
# Row indices (0-based) after which to draw a separator
sep_after_row   = [block_ends_n[b] - 1 for b in range(9)]   # after blocks 1-9

# ── Figure ────────────────────────────────────────────────────────────────────

CELL_W = 0.3   # inches per column
CELL_H = 0.3   # inches per row
FIG_W  = BITS  * CELL_W + 2.2
FIG_H  = MAX_N * CELL_H + 2.2

fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
fig.patch.set_facecolor("#F8F8F8")
ax.set_facecolor("#F8F8F8")

# cmap = ListedColormap(["#FFFFFF", "#1A1A1A", "#2563EB"])
cmap = ListedColormap(["#FFFFFF", "#1A1A1A", "#1A1A1A"])

ax.imshow(
    data,
    cmap=cmap, vmin=0, vmax=2,
    aspect="auto",
    interpolation="none",
    extent=[-0.5, BITS - 0.5, MAX_N - 0.5, -0.5],
)

# ── Cell grid (thin light lines) ──────────────────────────────────────────────

ax.set_xticks(np.arange(-0.5, BITS,   1), minor=True)
ax.set_yticks(np.arange(-0.5, MAX_N,  1), minor=True)
ax.grid(which="minor", color="#CCCCCC", linewidth=0.25, linestyle="-")
ax.tick_params(which="minor", bottom=False, left=False)

# ── Block separator lines (thicker) ───────────────────────────────────────────

for row in sep_after_row:
    ax.axhline(row + 0.5, color="#555555", linewidth=1.4, zorder=3)

# ── Left Y-axis: N at every block start + 143 at the end ─────────────────────

ytick_rows   = [n - 1 for n in block_starts_n] + [MAX_N - 1]
ytick_labels = [str(n) for n in block_starts_n] + [str(MAX_N)]
ax.set_yticks(ytick_rows)
ax.set_yticklabels(ytick_labels, fontsize=8)
ax.set_ylabel("N", fontsize=10, labelpad=6)

# ── Right Y-axis: block label centered in each block ─────────────────────────

ax_r = ax.twinx()
ax_r.set_ylim(ax.get_ylim())

centers = [
    (block_starts_n[i] + block_ends_n[i]) / 2 - 1
    for i in range(10)
]
ax_r.set_yticks(range(MAX_N))
ax_r.set_yticklabels([str(n) for n in range(1, MAX_N + 1)], fontsize=6)
ax_r.tick_params(length=2, pad=2, right=True)

# ── Top X-axis: Fibonacci position labels ────────────────────────────────────

fib_vals = [55, 34, 21, 13, 8, 5, 3, 2, 1, 1]   # F10 → F1

ax.set_xticks(range(BITS))
ax.set_xticklabels(
    [f"F{BITS - i}\n={fib_vals[i]}" for i in range(BITS)],
    fontsize=7.5,
)
ax.xaxis.tick_top()
ax.xaxis.set_label_position("top")

# ── Title ─────────────────────────────────────────────────────────────────────

ax.set_title(
    "Código Binario de Base Áurea   ·   N = 1 … 143   (Bloques 1–10)",
    fontsize=11, pad=18, fontweight="bold",
)

# ── Legend ────────────────────────────────────────────────────────────────────

legend_elements = [
    mpatches.Patch(facecolor="#1A1A1A",                  label="1  (no primo)"),
    mpatches.Patch(facecolor="#2563EB",                  label="1  (primo)"),
    mpatches.Patch(facecolor="white", edgecolor="#AAAAAA", label="0"),
]
ax.legend(
    handles=legend_elements,
    loc="lower center",
    bbox_to_anchor=(0.5, -0.04),
    ncol=3,
    fontsize=9,
    framealpha=0.95,
    edgecolor="#CCCCCC",
)

# ── Save & show ───────────────────────────────────────────────────────────────

plt.tight_layout()
plt.savefig("fractal_pattern.png", dpi=150, bbox_inches="tight")
print("Guardado: fractal_pattern.png")
subprocess.run(["open", "fractal_pattern.png"])  # abre en Preview (macOS)
