import numpy as np
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go

from kev_fractal import build_kev_fractal

# ── Load fractal data through block 12 (F14-1 = 376) ─────────────────────────
MAX_BLOCKS_LIMIT = 12
fractal = build_kev_fractal(376)

blocks_data: dict[int, list] = {}
for e in fractal:
    if e.block <= MAX_BLOCKS_LIMIT:
        blocks_data.setdefault(e.block, []).append(e)

# Fibonacci sequence (index = F_n, 1-based: FIBS[1]=1, FIBS[2]=1, FIBS[12]=144…)
FIBS = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377]

EMPTY_C      = "white"
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

N_LAT  = 6
N_LON  = 8
RADIUS = 0.5


# ── Geometry: sphere ──────────────────────────────────────────────────────────

def uv_sphere(cx, cy, cz):
    verts = [(cx, cy, cz + RADIUS)]
    for i in range(1, N_LAT):
        phi    = np.pi * i / N_LAT
        ring_r = RADIUS * np.sin(phi)
        z      = cz + RADIUS * np.cos(phi)
        for j in range(N_LON):
            theta = 2 * np.pi * j / N_LON
            verts.append((cx + ring_r * np.cos(theta),
                           cy + ring_r * np.sin(theta), z))
    verts.append((cx, cy, cz - RADIUS))
    faces = []
    for j in range(N_LON):
        faces.append((0, 1 + j, 1 + (j + 1) % N_LON))
    for i in range(N_LAT - 2):
        rs = 1 + i * N_LON
        for j in range(N_LON):
            a, b = rs + j, rs + (j + 1) % N_LON
            c, d = a + N_LON, b + N_LON
            faces.append((a, b, d)); faces.append((a, d, c))
    sp  = len(verts) - 1
    lrs = 1 + (N_LAT - 2) * N_LON
    for j in range(N_LON):
        faces.append((sp, lrs + (j + 1) % N_LON, lrs + j))
    return verts, faces


def build_sphere_mesh(cell_list):
    xs, ys, zs, ii, jj, kk = [], [], [], [], [], []
    vtx_colors, vtx_texts   = [], []
    offset = 0
    for col, yp, row, color, hover in cell_list:
        verts, faces = uv_sphere(col + 0.5, yp + 0.5, row + 0.5)
        for vx, vy, vz in verts:
            xs.append(vx); ys.append(vy); zs.append(vz)
            vtx_colors.append(color); vtx_texts.append(hover)
        for fi, fj, fk in faces:
            ii.append(fi + offset); jj.append(fj + offset); kk.append(fk + offset)
        offset += len(verts)
    return go.Mesh3d(
        x=xs, y=ys, z=zs, i=ii, j=jj, k=kk,
        vertexcolor=vtx_colors, text=vtx_texts,
        hoverinfo="text", showscale=False,
        lighting=dict(ambient=0.5, diffuse=0.9, specular=0.4, roughness=0.3, fresnel=0.3),
        lightposition=dict(x=2, y=-1, z=5),
    )


# ── Geometry: cube ────────────────────────────────────────────────────────────

def unit_cube(x0, y0, z0):
    x1, y1, z1 = x0+1, y0+1, z0+1
    verts = [
        (x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),
        (x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1),
    ]
    faces = [
        (0,2,1),(0,3,2),(4,5,6),(4,6,7),
        (0,1,5),(0,5,4),(2,3,7),(2,7,6),
        (0,4,7),(0,7,3),(1,2,6),(1,6,5),
    ]
    return verts, faces


def build_cube_mesh(cell_list):
    xs, ys, zs, ii, jj, kk = [], [], [], [], [], []
    face_colors, vtx_texts  = [], []
    offset = 0
    for col, yp, row, color, hover in cell_list:
        verts, faces = unit_cube(col, yp, row)
        for vx, vy, vz in verts:
            xs.append(vx); ys.append(vy); zs.append(vz)
            vtx_texts.append(hover)
        for fi, fj, fk in faces:
            ii.append(fi + offset); jj.append(fj + offset); kk.append(fk + offset)
            face_colors.append(color)
        offset += 8
    return go.Mesh3d(
        x=xs, y=ys, z=zs, i=ii, j=jj, k=kk,
        facecolor=face_colors, text=vtx_texts,
        hoverinfo="text", flatshading=True, showscale=False,
        lighting=dict(ambient=0.6, diffuse=0.8, specular=0.3, roughness=0.5, fresnel=0.2),
        lightposition=dict(x=2, y=-1, z=5),
    )


def build_cube_wireframe(cell_list):
    xs, ys, zs = [], [], []
    for col, yp, row, *_ in cell_list:
        x0, y0, z0 = float(col), float(yp), float(row)
        x1, y1, z1 = x0+1, y0+1, z0+1
        edges = [
            (x0,y0,z0),(x1,y0,z0),(x1,y0,z0),(x1,y1,z0),
            (x1,y1,z0),(x0,y1,z0),(x0,y1,z0),(x0,y0,z0),
            (x0,y0,z1),(x1,y0,z1),(x1,y0,z1),(x1,y1,z1),
            (x1,y1,z1),(x0,y1,z1),(x0,y1,z1),(x0,y0,z1),
            (x0,y0,z0),(x0,y0,z1),(x1,y0,z0),(x1,y0,z1),
            (x1,y1,z0),(x1,y1,z1),(x0,y1,z0),(x0,y1,z1),
        ]
        for i in range(0, len(edges), 2):
            ax, ay, az = edges[i];  bx, by, bz = edges[i+1]
            xs += [ax, bx, None];  ys += [ay, by, None];  zs += [az, bz, None]
    return go.Scatter3d(
        x=xs, y=ys, z=zs, mode="lines",
        line=dict(color="white", width=1), hoverinfo="skip",
    )


# ── Core builder: scene data + figures for a given block count ────────────────

def build_figures(num_blocks: int) -> tuple[dict, dict]:
    max_bits    = num_blocks
    cell_list   = []
    label_xs, label_ys, label_zs, label_texts = [], [], [], []
    prime_xs, prime_ys, prime_zs              = [], [], []

    for block_num in range(1, num_blocks + 1):
        entries        = blocks_data[block_num]
        y_pos          = block_num - 1
        start_col      = max_bits - block_num
        prev_entries   = blocks_data.get(block_num - 1, [])
        prev_start_col = max_bits - (block_num - 1)

        for row_idx, e in enumerate(entries):
            bits_padded = e.bits.zfill(max_bits)
            prime_str   = "primo" if e.is_prime else "compuesto"
            hover = (
                f"N = {e.n}  ({prime_str})<br>"
                f"Bloque {e.block}<br>"
                f"Bits: {e.bits}"
            )
            block_color = BLOCK_SHADES[block_num - 1]
            label_col   = None
            for col_idx in range(start_col, max_bits):
                if block_num > 1 and col_idx >= prev_start_col and row_idx < len(prev_entries):
                    continue
                bit   = bits_padded[col_idx]
                color = block_color if bit == "1" else EMPTY_C
                cell_list.append((col_idx, y_pos, row_idx, color, hover))
                if bit == "1":
                    label_col = col_idx
            if label_col is not None:
                lx, ly, lz = label_col + 0.5, y_pos + 0.5, row_idx + 0.5
                label_xs.append(lx); label_ys.append(ly); label_zs.append(lz)
                label_texts.append(str(e.n))
                if e.is_prime:
                    prime_xs.append(lx); prime_ys.append(ly); prime_zs.append(lz)

    # Prime lines from N=1 (rightmost col of block 1)
    origin      = (max_bits - 0.5, 0.5, 0.5)
    line_xs, line_ys, line_zs = [], [], []
    for x, y, z in zip(prime_xs, prime_ys, prime_zs):
        line_xs += [origin[0], x, None]
        line_ys += [origin[1], y, None]
        line_zs += [origin[2], z, None]

    prime_lines = go.Scatter3d(
        x=line_xs, y=line_ys, z=line_zs, mode="lines",
        line=dict(color="black", width=1), opacity=0.5, hoverinfo="skip",
    )
    labels = go.Scatter3d(
        x=label_xs, y=label_ys, z=label_zs,
        mode="text", text=label_texts,
        textfont=dict(size=7, color="white"), hoverinfo="skip",
    )

    # X-axis: F(max_bits) … F1 labels
    fib_labels = [f"F{max_bits - i}={FIBS[max_bits - i]}" for i in range(max_bits)]
    # Z aspect = F(num_blocks) / num_blocks keeps cubes square
    z_ratio = max(FIBS[num_blocks] / num_blocks, 0.5)

    scene = dict(
        xaxis=dict(
            title="Bit de Fibonacci",
            tickvals=[i + 0.5 for i in range(max_bits)],
            ticktext=fib_labels,
            tickfont=dict(size=8),
            autorange="reversed",
        ),
        yaxis=dict(
            title="Bloque",
            tickvals=[b - 0.5 for b in range(1, num_blocks + 1)],
            ticktext=[f"B{b}" for b in range(1, num_blocks + 1)],
            tickfont=dict(size=8),
        ),
        zaxis=dict(title="Posición en bloque", tickfont=dict(size=8)),
        camera=dict(
            eye=dict(x=0.0625, y=-7.3321, z=-0.1558),
            up=dict(x=-0.0026, y=-0.0213, z=0.9998),
            center=dict(x=0, y=0, z=0),
        ),
        bgcolor="#F0F0F0",
        aspectmode="manual",
        aspectratio=dict(x=1, y=1, z=z_ratio),
    )
    layout = dict(
        autosize=True, margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="#1A1A1A", scene=scene,
    )

    def make(traces):
        fig = go.Figure(traces + [prime_lines, labels])
        fig.update_layout(**layout)
        return fig.to_dict()

    return (
        make([build_sphere_mesh(cell_list)]),
        make([build_cube_mesh(cell_list), build_cube_wireframe(cell_list)]),
    )


# Pre-compute default (block 10); others built on first request
_fig_cache: dict[int, tuple] = {}
_fig_cache[10] = build_figures(10)


def get_figures(num_blocks: int) -> tuple[dict, dict]:
    if num_blocks not in _fig_cache:
        _fig_cache[num_blocks] = build_figures(num_blocks)
    return _fig_cache[num_blocks]


# ── Dash app ──────────────────────────────────────────────────────────────────

app = dash.Dash(__name__)

BUTTON_STYLE = {
    "position": "fixed",
    "bottom": "16px",
    "left": "16px",
    "zIndex": 1000,
    "padding": "8px 20px",
    "background": "#333",
    "color": "#eee",
    "border": "1px solid #666",
    "borderRadius": "6px",
    "cursor": "pointer",
    "fontSize": "13px",
    "fontFamily": "monospace",
    "letterSpacing": "0.05em",
}

PANEL_STYLE = {
    "position": "fixed",
    "bottom": "56px",
    "left": "16px",
    "zIndex": 1000,
    "background": "#222",
    "border": "1px solid #555",
    "borderRadius": "6px",
    "padding": "10px 14px",
    "fontFamily": "monospace",
    "fontSize": "11px",
    "color": "#ccc",
    "whiteSpace": "pre",
    "minWidth": "260px",
    "display": "none",
}

SLIDER_PANEL_STYLE = {
    "position": "fixed",
    "bottom": "60px",
    "left": "16px",
    "width": "360px",
    "zIndex": 1000,
    "background": "#222",
    "border": "1px solid #555",
    "borderRadius": "6px",
    "padding": "8px 20px 14px",
}

app.layout = html.Div([
    dcc.Store(id="camera-store"),
    dcc.Loading(
        dcc.Graph(
            id="graph",
            figure=_fig_cache[10][0],
            style={"height": "100vh", "width": "100vw"},
            config={"scrollZoom": True},
        ),
        type="circle",
        color="#eee",
    ),
    # ── Slider ────────────────────────────────────────────────────────────────
    html.Div([
        html.Span(id="slider-label",
                  children="Bloques: 10",
                  style={"color": "#aaa", "fontSize": "11px",
                         "fontFamily": "monospace", "display": "block",
                         "marginBottom": "4px"}),
        dcc.Slider(
            id="block-slider",
            min=1, max=12, step=1, value=10,
            marks={i: {"label": str(i), "style": {"color": "#aaa", "fontSize": "10px"}}
                   for i in range(1, 13)},
            included=True,
            tooltip={"always_visible": False},
        ),
    ], style=SLIDER_PANEL_STYLE),
    # ── Buttons ───────────────────────────────────────────────────────────────
    html.Button("⬡  Switch to Cubes", id="toggle-btn",
                n_clicks=0, style=BUTTON_STYLE),
    html.Button("📷  Camera", id="camera-btn",
                n_clicks=0, style={**BUTTON_STYLE, "left": "172px"}),
    html.Pre(id="camera-panel", style=PANEL_STYLE),
], style={"margin": 0, "padding": 0, "overflow": "hidden"})


@app.callback(
    Output("graph",        "figure"),
    Output("toggle-btn",   "children"),
    Output("slider-label", "children"),
    Input("toggle-btn",    "n_clicks"),
    Input("block-slider",  "value"),
)
def update_view(n_clicks, num_blocks):
    sphere_dict, cube_dict = get_figures(num_blocks)
    label = f"Bloques: {num_blocks}"
    if n_clicks % 2 == 0:
        return sphere_dict, "⬡  Switch to Cubes", label
    else:
        return cube_dict,   "⬜  Switch to Spheres", label


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
def update_camera_panel(n_clicks, camera):
    if not n_clicks or n_clicks % 2 == 0:
        return "", {**PANEL_STYLE, "display": "none"}
    if not camera:
        text = "# rotate the scene first"
    else:
        def fmt(d):
            return "dict({})".format(", ".join(f"{k}={round(v,4)}" for k, v in d.items()))
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
