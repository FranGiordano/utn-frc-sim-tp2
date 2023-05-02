from dash import html
import dash_bootstrap_components as dbc


def crear_parametros_tabla_pedido():

    parametros = html.Div([
        dbc.Alert("Probabilidad acumulada: 1", id="alerta_pedido", color="success"),

        dbc.Row([
            dbc.Col(
                dbc.Input(id="in_pedido_tamanio", placeholder="Tamaño", type="number", min=1, step=1)
            ),
            dbc.Col(
                dbc.Input(id="in_pedido_probabilidad", placeholder="Probabilidad", type="number", min=0.01, step=0.01,
                          max=1)
            ),
            dbc.Col(
                dbc.Button("Añadir fila", id="btn_crear_fila_pedido"), class_name="col-auto align-self-end"
            )
        ])
    ])

    return parametros
