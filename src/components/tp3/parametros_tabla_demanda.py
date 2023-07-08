from dash import html
import dash_bootstrap_components as dbc


def crear_parametros_tabla_demanda():

    parametros = html.Div([
        dbc.Alert("Probabilidad acumulada: 1", id="alerta_demanda", color="success", className="ms-1"),

        dbc.Row([
            dbc.Col(
                dbc.Input(id="in_demanda_consumo", placeholder="Consumo", type="number", min=1, step=1)
            ),
            dbc.Col(
                dbc.Input(id="in_demanda_probabilidad", placeholder="Probabilidad", type="number", min=0.01, step=0.01,
                          max=1)
            ),
            dbc.Col(
                dbc.Button("Añadir fila", id="btn_crear_fila_demanda"), class_name="col-auto align-self-end"
            )
        ]),
    ])

    return parametros

