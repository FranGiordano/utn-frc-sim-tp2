import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd
from dash.dash_table import DataTable


def crear_resultados_simulacion(filas_guardadas):

    datos_tabla = {
        "Semana": [f"{fila[0]:,.0f}" for fila in filas_guardadas],
        "Random 1": [f"{fila[1]:.2f}" for fila in filas_guardadas],
        "Consumo semanal (m²)": [f"{fila[2]:,.0f}" for fila in filas_guardadas],
        "Random 2": [f"{fila[3]:.2f}" for fila in filas_guardadas],
        "Tamaño de pedido (m²)": [f"{fila[4]:,.0f}" for fila in filas_guardadas],
        "Stock": [f"{fila[5]:,.0f}" for fila in filas_guardadas],
        "Costo de pedido": [f"${fila[6]:,.0f}" for fila in filas_guardadas],
        "Costo de mantenimiento": [f"${fila[7]:,.0f}" for fila in filas_guardadas],
        "Costo de sobrepaso": [f"${fila[8]:,.0f}" for fila in filas_guardadas],
        "Costo total": [f"${fila[9]:,.0f}" for fila in filas_guardadas],
        "Costo total acumulado": [f"${fila[10]:,.0f}" for fila in filas_guardadas],
        "Promedio de costo total": [f"${fila[11]:,.0f}" for fila in filas_guardadas],
        "Diferencia de stock (actual-anterior)": [f"{fila[12]:,.0f}" for fila in filas_guardadas],
        "Diferencia de stock acumulado": [f"{fila[13]:,.0f}" for fila in filas_guardadas],
        "Promedio de crecimiento semanal de stock": [f"{fila[14]:,.0f}" for fila in filas_guardadas],
        "Cantidad semanas con stock negativo": [f"{fila[15]:,.0f}" for fila in filas_guardadas],
        "Porcentaje semanas con stock negativo": [f"{fila[16]*100:.4f}%" for fila in filas_guardadas],
        "Promedio semanas hasta overflow de inventario": [f"{fila[17]:,.0f}" for fila in filas_guardadas],
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
            "heigth": "300px",
        },
        style_cell={
            "height": "auto",
            'minWidth': '120px',
            'width': 'auto',
            'maxWidth': 'auto',
            'whiteSpace': 'normal'
        },
        style_header={'backgroundColor': 'rgb(230, 230, 230)',
                      'fontWeight': 'bold',
                      "textAlign": "center",
                      "maxHeight": "80px",
                      "minHeight": "80px",
                      "height": "80px"},
        page_action="none",
        fixed_rows={'headers': True},
    )

    # Generación de insights

    promedio_crecimiento_semanal_stock = datos_tabla['Promedio de crecimiento semanal de stock'][-1]
    insight3 = f"3) En promedio, el crecimiento semanal del stock es de {promedio_crecimiento_semanal_stock} m²."
    if int(promedio_crecimiento_semanal_stock) > 0:
        insight3 += f" Esto implica que el inventario disponible ingresado alcanzará su máxima capacidad en " \
                   f"aproximadamente {datos_tabla['Promedio semanas hasta overflow de inventario'][-1]} semanas."

    insights = dbc.Card([
        dbc.CardHeader("Insights de la simulación generada"),
        dbc.CardBody([
            html.H5(f"De {datos_tabla['Semana'][-1]} semanas simuladas se obtuvo que: ", className="card-title"),
            html.P(f"1) El costo promedio total es de {datos_tabla['Promedio de costo total'][-1]}.",
                   className="card-text"),
            html.P(f"2) El stock final es de {datos_tabla['Stock'][-1]} m², lo que implica "
                   f"{datos_tabla['Costo de mantenimiento'][-1]} en costos de mantenimiento y "
                   f"{datos_tabla['Costo de sobrepaso'][-1]} en costos de sobrepaso.", className="card-text"),
            html.P(insight3, className="card-text"),
            html.P(f"4) Hubo un total de {datos_tabla['Cantidad semanas con stock negativo'][-1]} semanas con stock "
                   f"negativo, las cuales constituyen el {datos_tabla['Porcentaje semanas con stock negativo'][-1]} "
                   f"del total de semanas.")
        ])
    ], color="success", inverse=True, className="mt-3")

    insights_tp = dbc.Card([
        dbc.CardHeader("Insight general (con los parámetros dados en el trabajo práctico)"),
        dbc.CardBody([
            html.P("Para este TP se estableció el siguiente cuestionamiento: ",
                   className="card-text"),
            html.P("¿La capacidad de almacenar (25000) es adecuada o hace falta invertir y agrandar el espacio?",
                   className="card-text"),
            html.P("La respuesta que podemos dar es que no existe capacidad adecuada para este caso, ya que el stock "
                   "que ingresa es superior al stock que se consume, siendo en promedio 41-42 semanas hasta que la "
                   "capacidad de almacenamiento se rebalse. Queda como únicas opciones aumentar el consumo del stock, "
                   "o disminuir el tamaño de los pedidos, de tal forma de apuntar el crecimiento semanal de stock a un "
                   "valor aproximado a 0.",
                   className="card-text")
        ])
    ], color="primary", inverse=True, className="mt-3")

    resultado = html.Div([
        html.Center(html.H2("Resultados"), className="mt-3"),
        html.Div(tabla, className="mt-3",),
        html.Center(html.H2("Conclusiones"), className="mt-3"),
        insights,
        insights_tp
    ])

    return resultado
