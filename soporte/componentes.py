from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd


def generar_barra_navegacion():
    barra_navegacion = dbc.Navbar(
        dbc.Container([

            dbc.NavItem(
                dbc.Row(
                    [
                        dbc.Col(
                            html.Img(src="/assets/icons/simulation.png", height="30px")),
                        dbc.Col(dbc.NavbarBrand("UTN FRC - Simulación",
                                className="ms-2", href="/")),
                    ],
                    align="center",
                    className="g-0",
                )),

            dbc.NavItem(
                dbc.NavLink("Inicio", href="/", style={"color": "white"}),
                class_name="ms-auto px-1"),

            dbc.NavItem(
                dbc.NavLink("TP2", href="/tp2/", style={"color": "white"}),
                class_name="px-3"),

            html.A(
                html.Img(src="/assets/icons/github-mark-white.svg",
                         height="30px"),
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
                dbc.Input(id="in_cantidad_muestras", placeholder="Cantidad de muestras", type="number",
                          min=0, step=1, value=10000, required=True),
                dbc.Label("Cantidad de muestras"),
            ])]),

        dbc.Col(id='form-intervalos',
                children=[
                    dbc.FormFloating([
                        dbc.Input(id="in_intervalos",
                                  placeholder="Cantidad de intervalos",
                                  type="number", min=1, step=1,
                                  value=15, required=True),
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
                          value=5, required=True, step=0.0001, min=0.0001),
                dbc.Label("Lambda"),
            ])], style={"display": "none"}),

        dbc.Col(dbc.Button("Generar distribución",
                           id="btn_cargar_grafico",
                           color="primary"),
                class_name="col-auto align-self-end")
    ])

    return parametros


def generar_visualizacion(histograma, datos_frecuencias, datos_chi2, datos_ks=None):

    visualizacion = html.Div([

        # Sección 1: Histograma

        dcc.Graph(figure=histograma),

        dbc.Row([

            # Sección 2: Tabla de frecuencias

            crear_columna_frecuencias(datos_frecuencias),

            # Sección 3: Pruebas de bondad

            dbc.Col([

                html.Center(html.H3("Pruebas de bondad de ajuste")),
                html.Br(),

                dbc.Row([

                    # Sección 3a: Chi2

                    crear_columna_chi2(datos_chi2),

                    # Sección 3b: K-S

                    crear_columna_ks(datos_ks) if datos_ks is not None else dbc.Col(
                        class_name="d-none"),
                ])
            ])
        ])
    ])

    return visualizacion


def crear_columna_frecuencias(datos_frecuencias):

    tabla = pd.DataFrame(datos_frecuencias)
    tabla = tabla.set_index("#")
    tabla = tabla.round(4).astype(str)

    columna_frecuencia = dbc.Col([
        html.Center(html.H3("Tabla de frecuencias")),
        html.Br(),
        dbc.Table.from_dataframe(tabla, class_name="w-auto mx-auto", striped=True, bordered=True, responsive=True,
                                 index=True)
    ])

    return columna_frecuencia


def crear_columna_chi2(datos_chi2):

    tabla = pd.DataFrame({
        "Parámetro": datos_chi2.keys(),
        "Valor": datos_chi2.values()
    })

    tabla = tabla.round(4).astype(str)

    if datos_chi2["Grados de libertad"] <= 0:
        alerta = dbc.Alert("La cantidad de muestras no es suficiente para conseguir el χ2 tabulado ó se presentó un "
                           "error de cálculo", color="danger")
    elif datos_chi2["χ2 calculado"] <= datos_chi2["χ2 tabulado"]:
        alerta = dbc.Alert(
            "El test de χ2 no rechaza la hipótesis nula", color="success")
    else:
        alerta = dbc.Alert(
            "El test de χ2 rechaza la hipótesis nula", color="danger")

    columna_chi2 = dbc.Col([
        html.Center(html.H4("Chi-cuadrado")),
        dbc.Table.from_dataframe(
            tabla, class_name="w-auto mx-auto", striped=True, bordered=True),
        alerta
    ])

    return columna_chi2


def crear_columna_ks(datos_ks):

    tabla = pd.DataFrame({
        "Parámetro": datos_ks.keys(),
        "Valor": datos_ks.values()
    })

    tabla = tabla.round(4).astype(str)

    if datos_ks["K-S calculado"] <= datos_ks["K-S tabulado"]:
        alerta = dbc.Alert(
            "El test de K-S no rechaza la hipótesis nula", color="success")
    else:
        alerta = dbc.Alert(
            "El test de K-S rechaza la hipótesis nula", color="danger")

    columna_ks = dbc.Col([
        html.Center(html.H4("Kolmogorov-Smirnov")),
        dbc.Table.from_dataframe(
            tabla, class_name="w-auto mx-auto", striped=True, bordered=True),
        alerta
    ])

    return columna_ks
