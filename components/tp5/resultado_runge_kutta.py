import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd
from dash.dash_table import DataTable


def crear_resultados_simulacion(filas_guardadas, y):
    datos_tabla = {
        "t": [f"{fila[0]:,.4f}" for fila in filas_guardadas],
        f"{y}": [f"{fila[1]:,.4f}" for fila in filas_guardadas],
        "K1": [f"{fila[2]:,.4f}" for fila in filas_guardadas],
        "K2": [f"{fila[3]:,.4f}" for fila in filas_guardadas],
        "K3": [f"{fila[4]:,.4f}" for fila in filas_guardadas],
        "K4": [f"{fila[5]:,.4f}" for fila in filas_guardadas],
        "t(i+1)": [f"{fila[6]:,.4f}" for fila in filas_guardadas],
        f"{y}(i+1)": [f"{fila[7]:,.4f}" for fila in filas_guardadas],
    }

    # Generación de tabla

    df = pd.DataFrame(datos_tabla)

    tabla = DataTable(
        id="tabla_resultados_simulacion",
        data=df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df.columns],
        cell_selectable=False,
        style_table={
            "overflowX": "auto",
            "heigth": "auto",
            "width": "1000px"
        },
        style_cell={
            "height": "auto",
            'minWidth': '100px',
            'width': 'auto',
            'maxWidth': '200px',
            'whiteSpace': 'normal'
        },
        style_header={'backgroundColor': 'rgb(230, 230, 230)',
                      'fontWeight': 'bold',
                      "textAlign": "center",
                      "maxHeight": "50px",
                      "minHeight": "50px",
                      "height": "50px"},
        page_action="none",
        fixed_rows={'headers': True},
    )

    resultado = html.Div([
        html.Center(html.H2("Runge Kutta"), className="mt-3"),
        html.Center(html.Div(tabla, className="mt-3",))
    ])

    return resultado
