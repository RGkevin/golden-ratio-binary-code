import numpy as np
import plotly.graph_objects as go

N_LAT  = 6
N_LON  = 8
RADIUS = 0.5


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


def unit_cube(x0, y0, z0):
    x1, y1, z1 = x0 + 1, y0 + 1, z0 + 1
    verts = [
        (x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
        (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1),
    ]
    faces = [
        (0, 2, 1), (0, 3, 2), (4, 5, 6), (4, 6, 7),
        (0, 1, 5), (0, 5, 4), (2, 3, 7), (2, 7, 6),
        (0, 4, 7), (0, 7, 3), (1, 2, 6), (1, 6, 5),
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
            ax, ay, az = edges[i]; bx, by, bz = edges[i + 1]
            xs += [ax, bx, None]; ys += [ay, by, None]; zs += [az, bz, None]
    return go.Scatter3d(
        x=xs, y=ys, z=zs, mode="lines",
        line=dict(color="white", width=1), hoverinfo="skip",
    )
