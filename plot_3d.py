import dash
from dash import Input, Output
import plotly.graph_objects as go

from kev_fractal import build_kev_fractal
from geometry import build_sphere_mesh, build_cube_mesh, build_cube_wireframe
from ui_layout import create_layout, PANEL_STYLE

# ── Constants ─────────────────────────────────────────────────────────────────

MAX_BLOCKS_LIMIT = 12
FIBS = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377]

EMPTY_C = "white"
BLOCK_SHADES = [
    "#E63946",  # B1  — red
    "#F4A261",  # B2  — orange
    "#E9C46A",  # B3  — yellow
    "#8AC926",  # B4  — lime
    "#06D6A0",  # B5  — teal
    "#118AB2",  # B6  — blue
    "#5E60CE",  # B7  — indigo
    "#9B5DE5",  # B8  — purple
    "#F72585",  # B9  — pink
    "#3A0CA3",  # B10 — deep purple
    "#00B4D8",  # B11 — sky blue
    "#2DC653",  # B12 — green
]

DEFAULT_CAMERA = dict(
    eye=dict(x=4.6557, y=-3.16, z=4.6444),
    up=dict(x=-0.33, y=-0.9008, z=-0.2821),
    center=dict(x=-0.0, y=0.0, z=-0.0),
)

# ── Load fractal data ─────────────────────────────────────────────────────────

fractal = build_kev_fractal(377)
blocks_data: dict[int, list] = {}
for e in fractal:
    if e.block <= MAX_BLOCKS_LIMIT:
        blocks_data.setdefault(e.block, []).append(e)


# ── Block alignment ───────────────────────────────────────────────────────────

def block_start_col(block_num: int, max_bits: int) -> int:
    """Column where block_num's bits begin. Change this to adjust alignment."""
    return max_bits - block_num  # right-aligned (pyramid shape)


# ── Scene builders ────────────────────────────────────────────────────────────

def build_cell_list(num_blocks: int):
    """Compute (col, y, z, color, hover) for every visible bit cell."""
    max_bits  = num_blocks
    cell_list = []
    label_pts = []  # [(x, y, z), label_str]
    prime_pts = []  # [(x, y, z)]

    for block_num in range(1, num_blocks + 1):
        entries     = blocks_data[block_num]
        y_pos       = block_num - 1
        start_col   = block_start_col(block_num, max_bits)
        block_color = BLOCK_SHADES[block_num - 1]

        z_offset = -(len(entries) - 1)
        for row_idx, e in enumerate(entries):
            z_pos   = row_idx + z_offset
            bits    = e.bits.zfill(max_bits)
            hover   = (f"N = {e.n}  ({'primo' if e.is_prime else 'compuesto'})<br>"
                       f"Bloque {e.block}<br>Bits: {e.bits}")
            label_col = None

            for col_idx in range(start_col, max_bits):
                color = block_color if bits[col_idx] == "1" else EMPTY_C
                cell_list.append((col_idx, y_pos, z_pos, color, hover))
                if bits[col_idx] == "1":
                    label_col = col_idx

            if label_col is not None:
                pt = (label_col + 0.5, y_pos + 0.5, z_pos + 0.5)
                label_pts.append((pt, str(e.n)))
                if e.is_prime:
                    prime_pts.append(pt)

    return cell_list, label_pts, prime_pts


def build_overlay_traces(num_blocks: int, label_pts, prime_pts):
    """Black lines from N=1 to all primes, plus number labels."""
    origin = (num_blocks - 0.5, 0.5, 0.5)  # position of N=1

    line_xs, line_ys, line_zs = [], [], []
    for x, y, z in prime_pts:
        line_xs += [origin[0], x, None]
        line_ys += [origin[1], y, None]
        line_zs += [origin[2], z, None]

    prime_lines = go.Scatter3d(
        x=line_xs, y=line_ys, z=line_zs, mode="lines",
        line=dict(color="black", width=1), opacity=0.5, hoverinfo="skip",
    )

    if label_pts:
        lxs, lys, lzs, ltexts = zip(*[(p[0], p[1], p[2], t) for p, t in label_pts])
    else:
        lxs, lys, lzs, ltexts = [], [], [], []

    labels = go.Scatter3d(
        x=lxs, y=lys, z=lzs, mode="text", text=ltexts,
        textfont=dict(size=7, color="white"), hoverinfo="skip",
    )
    return prime_lines, labels


def build_scene_layout(num_blocks: int) -> dict:
    max_bits   = num_blocks
    fib_labels = [f"F{max_bits - i}={FIBS[max_bits - i]}" for i in range(max_bits)]
    z_ratio    = max(FIBS[num_blocks] / num_blocks, 0.5)
    return dict(
        autosize=True,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="#1A1A1A",
        scene=dict(
            xaxis=dict(
                title="X — Bit de Fibonacci",
                tickvals=[i + 0.5 for i in range(max_bits)],
                ticktext=fib_labels,
                tickfont=dict(size=8),
                autorange="reversed",
            ),
            yaxis=dict(
                title="Y — Bloque",
                tickvals=[b - 0.5 for b in range(1, num_blocks + 1)],
                ticktext=[f"B{b}" for b in range(1, num_blocks + 1)],
                tickfont=dict(size=8),
            ),
            zaxis=dict(title="Z — Posición en bloque", tickfont=dict(size=8), autorange="reversed"),
            camera=DEFAULT_CAMERA,
            bgcolor="#F0F0F0",
            aspectmode="manual",
            aspectratio=dict(x=1, y=1, z=z_ratio),
        ),
    )


def build_figures(num_blocks: int) -> tuple[dict, dict]:
    cell_list, label_pts, prime_pts = build_cell_list(num_blocks)
    prime_lines, labels = build_overlay_traces(num_blocks, label_pts, prime_pts)
    layout = build_scene_layout(num_blocks)

    def make(geometry_traces):
        fig = go.Figure(geometry_traces + [prime_lines, labels])
        fig.update_layout(**layout)
        return fig.to_dict()

    return (
        make([build_sphere_mesh(cell_list)]),
        make([build_cube_mesh(cell_list), build_cube_wireframe(cell_list)]),
    )


# ── Figure cache ──────────────────────────────────────────────────────────────

_fig_cache: dict[int, tuple] = {}
_fig_cache[5] = build_figures(5)


def get_figures(num_blocks: int) -> tuple[dict, dict]:
    if num_blocks not in _fig_cache:
        _fig_cache[num_blocks] = build_figures(num_blocks)
    return _fig_cache[num_blocks]


# ── Dash app + callbacks ──────────────────────────────────────────────────────

app = dash.Dash(__name__)
app.layout = create_layout(_fig_cache[5][0])


@app.callback(
    Output("graph",        "figure"),
    Output("toggle-btn",   "children"),
    Output("slider-label", "children"),
    Input("toggle-btn",    "n_clicks"),
    Input("block-slider",  "value"),
)
def update_view(n_clicks, num_blocks):
    sphere_fig, cube_fig = get_figures(num_blocks)
    if n_clicks % 2 == 0:
        return sphere_fig, "⬡  Switch to Cubes",   f"Bloques: {num_blocks}"
    return     cube_fig,  "⬜  Switch to Spheres",  f"Bloques: {num_blocks}"


@app.callback(
    Output("camera-store", "data"),
    Input("graph", "relayoutData"),
)
def store_camera(relayout):
    if relayout and "scene.camera" in relayout:
        return relayout["scene.camera"]
    return dash.no_update


@app.callback(
    Output("camera-panel", "children"),
    Output("camera-panel", "style"),
    Input("camera-btn",    "n_clicks"),
    Input("camera-store",  "data"),
)
def show_camera_panel(n_clicks, camera):
    if not n_clicks or n_clicks % 2 == 0:
        return "", {**PANEL_STYLE, "display": "none"}
    if not camera:
        return "# rotate the scene first", {**PANEL_STYLE, "display": "block"}

    def fmt(d):
        return "dict({})".format(", ".join(f"{k}={round(v, 4)}" for k, v in d.items()))

    text = (
        "camera=dict(\n"
        f"    eye={fmt(camera.get('eye', {}))},\n"
        f"    up={fmt(camera.get('up', {}))},\n"
        f"    center={fmt(camera.get('center', {}))},\n"
        ")"
    )
    return text, {**PANEL_STYLE, "display": "block"}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
