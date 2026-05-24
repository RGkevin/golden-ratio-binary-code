import numpy as np
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go

from kev_fractal import build_kev_fractal

fractal = build_kev_fractal()

# ── Group entries by block ─────────────────────────────────────────────────────
blocks_data: dict[int, list] = {}
for e in fractal:
    blocks_data.setdefault(e.block, []).append(e)

MAX_BITS    = 10
NUM_BLOCKS  = 10
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
]

N_LAT  = 6
N_LON  = 8
RADIUS = 0.5


# ── Geometry: sphere ──────────────────────────────────────────────────────────

def uv_sphere(cx: float, cy: float, cz: float):
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
            faces.append((a, b, d))
            faces.append((a, d, c))
    sp  = len(verts) - 1
    lrs = 1 + (N_LAT - 2) * N_LON
    for j in range(N_LON):
        faces.append((sp, lrs + (j + 1) % N_LON, lrs + j))
    return verts, faces


def build_sphere_mesh(cell_list: list[tuple]) -> go.Mesh3d:
    xs, ys, zs, ii, jj, kk = [], [], [], [], [], []
    vtx_colors, vtx_texts   = [], []
    offset = 0
    for col, yp, row, color, hover in cell_list:
        cx, cy, cz = col + 0.5, yp + 0.5, row + 0.5
        verts, faces = uv_sphere(cx, cy, cz)
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

def unit_cube(x0: float, y0: float, z0: float):
    x1, y1, z1 = x0 + 1, y0 + 1, z0 + 1
    verts = [
        (x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),
        (x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1),
    ]
    faces = [
        (0,2,1),(0,3,2), (4,5,6),(4,6,7),
        (0,1,5),(0,5,4), (2,3,7),(2,7,6),
        (0,4,7),(0,7,3), (1,2,6),(1,6,5),
    ]
    return verts, faces


def build_cube_wireframe(cell_list: list[tuple]) -> go.Scatter3d:
    xs, ys, zs = [], [], []
    for col, yp, row, *_ in cell_list:
        x0, y0, z0 = float(col), float(yp), float(row)
        x1, y1, z1 = x0 + 1, y0 + 1, z0 + 1
        edges = [
            (x0,y0,z0),(x1,y0,z0), (x1,y0,z0),(x1,y1,z0),
            (x1,y1,z0),(x0,y1,z0), (x0,y1,z0),(x0,y0,z0),
            (x0,y0,z1),(x1,y0,z1), (x1,y0,z1),(x1,y1,z1),
            (x1,y1,z1),(x0,y1,z1), (x0,y1,z1),(x0,y0,z1),
            (x0,y0,z0),(x0,y0,z1), (x1,y0,z0),(x1,y0,z1),
            (x1,y1,z0),(x1,y1,z1), (x0,y1,z0),(x0,y1,z1),
        ]
        for i in range(0, len(edges), 2):
            ax, ay, az = edges[i]
            bx, by, bz = edges[i + 1]
            xs += [ax, bx, None]
            ys += [ay, by, None]
            zs += [az, bz, None]
    return go.Scatter3d(
        x=xs, y=ys, z=zs,
        mode="lines",
        line=dict(color="white", width=1),
        hoverinfo="skip",
    )


def build_cube_mesh(cell_list: list[tuple]) -> go.Mesh3d:
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


# ── Build cell list (shared by both modes) ────────────────────────────────────

cell_list: list[tuple] = []
label_xs, label_ys, label_zs, label_texts = [], [], [], []

for block_num in range(1, NUM_BLOCKS + 1):
    entries        = blocks_data[block_num]
    y_pos          = block_num - 1
    start_col      = MAX_BITS - block_num
    prev_entries   = blocks_data.get(block_num - 1, [])
    prev_start_col = MAX_BITS - (block_num - 1)

    for row_idx, e in enumerate(entries):
        bits_padded = e.bits.zfill(MAX_BITS)
        prime_str   = "primo" if e.is_prime else "compuesto"
        hover = (
            f"N = {e.n}  ({prime_str})<br>"
            f"Bloque {e.block}<br>"
            f"Bits: {e.bits}"
        )
        block_color = BLOCK_SHADES[block_num - 1]
        label_col   = None
        for col_idx in range(start_col, MAX_BITS):
            if block_num > 1 and col_idx >= prev_start_col and row_idx < len(prev_entries):
                continue
            bit   = bits_padded[col_idx]
            color = block_color if bit == "1" else EMPTY_C
            cell_list.append((col_idx, y_pos, row_idx, color, hover))
            if bit == "1":
                label_col = col_idx
        if label_col is not None:
            label_xs.append(label_col + 0.5)
            label_ys.append(y_pos    + 0.5)
            label_zs.append(row_idx  + 0.5)
            label_texts.append(str(e.n))

labels_trace = go.Scatter3d(
    x=label_xs, y=label_ys, z=label_zs,
    mode="text", text=label_texts,
    textfont=dict(size=7, color="white"),
    hoverinfo="skip",
)


# ── Pre-build both figures ─────────────────────────────────────────────────────

SCENE = dict(
    xaxis=dict(
        title="Bit de Fibonacci",
        tickvals=[i + 0.5 for i in range(MAX_BITS)],
        ticktext=["F10","F9","F8","F7","F6","F5","F4","F3","F2","F1"],
        tickfont=dict(size=8),
        autorange="reversed",
    ),
    yaxis=dict(
        title="Bloque",
        tickvals=[b - 0.5 for b in range(1, NUM_BLOCKS + 1)],
        ticktext=[f"B{b}" for b in range(1, NUM_BLOCKS + 1)],
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
    aspectratio=dict(x=1, y=1, z=5.5),
)

LAYOUT = dict(
    autosize=True,
    margin=dict(l=0, r=0, t=0, b=0),
    paper_bgcolor="#1A1A1A",
    scene=SCENE,
)


def make_fig(traces: list):
    fig = go.Figure(traces + [labels_trace])
    fig.update_layout(**LAYOUT)
    return fig


fig_spheres = make_fig([build_sphere_mesh(cell_list)])
fig_cubes   = make_fig([build_cube_mesh(cell_list), build_cube_wireframe(cell_list)])

# Pre-serialise for fast callback response
data_spheres = fig_spheres.to_dict()
data_cubes   = fig_cubes.to_dict()

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

app.layout = html.Div([
    dcc.Store(id="camera-store"),
    dcc.Graph(
        id="graph",
        figure=fig_spheres,
        style={"height": "100vh", "width": "100vw"},
        config={"scrollZoom": True},
    ),
    html.Button(
        "⬡  Switch to Cubes",
        id="toggle-btn",
        n_clicks=0,
        style=BUTTON_STYLE,
    ),
    html.Button(
        "📷  Camera",
        id="camera-btn",
        n_clicks=0,
        style={**BUTTON_STYLE, "left": "172px"},
    ),
    html.Pre(id="camera-panel", style=PANEL_STYLE),
], style={"margin": 0, "padding": 0, "overflow": "hidden"})


@app.callback(
    Output("graph",      "figure"),
    Output("toggle-btn", "children"),
    Input("toggle-btn",  "n_clicks"),
)
def toggle_mode(n_clicks):
    if n_clicks % 2 == 0:
        return data_spheres, "⬡  Switch to Cubes"
    else:
        return data_cubes,   "⬜  Switch to Spheres"


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
            return "dict({})".format(
                ", ".join(f"{k}={round(v, 4)}" for k, v in d.items())
            )
        text = (
            "camera=dict(\n"
            f"    eye={fmt(camera.get('eye',    {}))},\n"
            f"    up={fmt(camera.get('up',      {}))},\n"
            f"    center={fmt(camera.get('center', {}))},\n"
            ")"
        )
    return text, {**PANEL_STYLE, "display": "block"}


if __name__ == "__main__":
    app.run(debug=True)
