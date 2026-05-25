from dash import dcc, html

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


def create_layout(initial_figure):
    return html.Div([
        dcc.Store(id="camera-store"),
        dcc.Store(id="lines-store", data=True),

        dcc.Loading(
            dcc.Graph(
                id="graph",
                figure=initial_figure,
                style={"height": "100vh", "width": "100vw"},
                config={"scrollZoom": True},
            ),
            type="circle",
            color="#eee",
        ),

        html.Div([
            html.Span(
                id="slider-label",
                children="Bloques: 5",
                style={"color": "#aaa", "fontSize": "11px",
                       "fontFamily": "monospace", "display": "block",
                       "marginBottom": "4px"},
            ),
            dcc.Slider(
                id="block-slider",
                min=1, max=12, step=1, value=5,
                marks={i: {"label": str(i), "style": {"color": "#aaa", "fontSize": "10px"}}
                       for i in range(1, 13)},
                included=True,
                tooltip={"always_visible": False},
            ),
        ], style=SLIDER_PANEL_STYLE),

        html.Button("⬡  Switch to Cubes", id="toggle-btn",
                    n_clicks=0, style=BUTTON_STYLE),
        html.Button("📷  Camera", id="camera-btn",
                    n_clicks=0, style={**BUTTON_STYLE, "left": "172px"}),
        html.Button("╱  Ocultar líneas", id="lines-btn",
                    n_clicks=0, style={**BUTTON_STYLE, "left": "280px"}),
        html.Pre(id="camera-panel", style=PANEL_STYLE),

    ], style={"margin": 0, "padding": 0, "overflow": "hidden"})
