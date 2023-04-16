from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd


def generar_barra_navegacion():

    barra_navegacion = dbc.Navbar(
        dbc.Container([
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="/assets/simulation.png", height="30px")),
                        dbc.Col(dbc.NavbarBrand("Simulación", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="/",
                style={"textDecoration": "none"},
            ),
            dbc.NavItem(
                dbc.NavLink("Trabajo Práctico Nº2", href="/tp2/", style={"color": "white"}),
                class_name="ms-auto px-2"),
            html.A(
                html.Img(src="/assets/github-mark-white.svg", height="30px"),
                href="https://github.com/FranGiordano/utn-frc-sim-tp2",
                style={"textDecoration": "none"},
                target="_blank"
            ),
        ]),
        color="primary",
        dark=True
    )

    return barra_navegacion


def generar_tipos_distribuciones():

    tipo_distribucion = dbc.InputGroup([
        dbc.Select(
            id="controls-dist",
            options=[
                {"label": "Exponencial Negativa", "value": "EN"},
                {"label": "Normal", "value": "N"},
                {"label": "Poisson", "value": "P"},
                {"label": "Uniforme", "value": "U"},
            ],
            value="U"
        ),
        dbc.InputGroupText("Distribución")
    ])

    return tipo_distribucion


def generar_parametros():
    parametros = dbc.Row([

        dbc.Col(id="form-cantidad", children=[
            dbc.FormFloating([
                dbc.Input(id="in_cantidad_muestras", placeholder="Cantidad de muestras", type="number", max=1000000,
                          min=0, step=1, value=10000, required=True),
                dbc.Label("Cantidad de muestras"),
            ])]),

        dbc.Col(id='form-intervalos',
                children=[
                    dbc.FormFloating([
                        dbc.Input(id="in_intervalos",
                                  placeholder="Cantidad de intervalos",
                                  type="number", min=1, step=1,
                                  value=15, required=True, max=225),
                        dbc.Label("Cantidad de intervalos"),
                    ])]),

        dbc.Col(id="form-limite-inferior", children=[
            dbc.FormFloating([
                dbc.Input(id="in_limite_inferior", placeholder="Límite inferior", type="number",
                          value=-10, required=True, step=0.0001),
                dbc.Label("Límite inferior"),
            ])], style={"display": "none"}),

        dbc.Col(id="form-limite-superior", children=[
            dbc.FormFloating([
                dbc.Input(id="in_limite_superior", placeholder="Límite superior", type="number",
                          value=10, required=True, step=0.0001),
                dbc.Label("Límite superior"),
            ])], style={"display": "none"}),

        dbc.Col(id='form-media',
                children=[
                    dbc.FormFloating([
                        dbc.Input(id="in_media", placeholder="Media", type="number",
                                  value=0, required=True, step=0.0001),
                        dbc.Label("Media"),
                    ])], style={"display": "none"}),

        dbc.Col(id="form-desv", children=[
            dbc.FormFloating([
                dbc.Input(id="in_desviacion", placeholder="Desviación Estándar", type="number", min=0.0001,
                          value=1, required=True, step=0.0001),
                dbc.Label("Desviación Estándar"),
            ])], style={"display": "none"}),

        dbc.Col(id="form-lambda", children=[
            dbc.FormFloating([
                dbc.Input(id="in_lambda", placeholder="Lambda", type="number",
                          value=5, required=True, step=0.0001),
                dbc.Label("Lambda"),
            ])], style={"display": "none"}),

        dbc.Col(dbc.Button("Generar distribución",
                           id="btn_cargar_grafico",
                           color="primary"),
                class_name="col-auto align-self-end")
    ])

    return parametros


def generar_visualizacion(histograma):
    visualizacion = html.Div([
        # Histograma
        dcc.Graph(figure=histograma),
    ])

    return visualizacion
