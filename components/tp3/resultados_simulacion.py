import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd
from dash.dash_table import DataTable


def crear_resultados_simulacion(filas_guardadas):

    datos_tabla = {
        "Semana": [fila[0] for fila in filas_guardadas],
        "Random 1": [round(fila[1], 2) for fila in filas_guardadas],
        "Consumo semanal (m²)": ["{:,.0f}".format(fila[2]) for fila in filas_guardadas],
        "Random 2": [round(fila[3], 2) for fila in filas_guardadas],
        "Tamaño de pedido (m²)": ["{:,.0f}".format(fila[4]) for fila in filas_guardadas],
        "Stock": ["{:,.0f}".format(fila[5]) for fila in filas_guardadas],
        "Costo de pedido": ["${:,.0f}".format(fila[6]) for fila in filas_guardadas],
        "Costo de mantenimiento": ["${:,.0f}".format(fila[7]) for fila in filas_guardadas],
        "Costo de sobrepaso": ["${:,.0f}".format(fila[8]) for fila in filas_guardadas],
        "Costo total": ["${:,.0f}".format(fila[9]) for fila in filas_guardadas],
        "Costo total acumulado": ["${:,.0f}".format(fila[10]) for fila in filas_guardadas],
        "Promedio de costo total": ["${:,.0f}".format(fila[11]) for fila in filas_guardadas],
        "Diferencia de stock (actual-anterior)": ["{:,.0f}".format(fila[12]) for fila in filas_guardadas],
        "Diferencia de stock acumulado": ["{:,.0f}".format(fila[13]) for fila in filas_guardadas],
        "Promedio de crecimiento semanal de stock": ["{:,.0f}".format(fila[14]) for fila in filas_guardadas],
        "Cantidad semanas en stock-out": ["{:,.0f}".format(fila[15]) for fila in filas_guardadas],
        "Porcentaje semanas en stock-out": ["{:.2f}%".format(fila[16] * 100) for fila in filas_guardadas],
        "Promedio semanas hasta overflow de inventario": ["{:,.0f}".format(fila[17]) for fila in filas_guardadas],
    }

    df = pd.DataFrame(datos_tabla)

    tabla = DataTable(
        id="tabla_resultados_simulacion",
        data=df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df.columns],
        cell_selectable=False,
        style_table={"overflowX": "auto"},
        style_cell={
            "height": "auto",
            'minWidth': '180px',
            'width': '180px',
            'maxWidth': '180px',
            'whiteSpace': 'normal'
        },
        style_header={'backgroundColor': 'rgb(230, 230, 230)',
                      'fontWeight': 'bold',
                      "textAlign": "center"},
        page_action="none",
        fixed_rows={'headers': True},
    )

    resultado = html.Div([
        html.Center(html.H2("Resultados")),
        html.Div(tabla, className="mt-3")
    ], className="mt-3")

    return resultado
