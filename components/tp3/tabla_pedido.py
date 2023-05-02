from dash import html, dcc, dash_table
from dash.dash_table.Format import Format, Scheme, Sign, Symbol
import dash_bootstrap_components as dbc


def crear_tabla_pedido():

    pedidos = [{"pedido": 8000, "probabilidad": 0.55},
               {"pedido": 11000, "probabilidad": 0.45}]

    columnas = [
        {"id": "pedido", "name": "Tamaño de pedido (m²)", "type": "numeric"},
        {"id": "probabilidad", "name": "Probabilidad", "type": "numeric"}]

    tabla = dash_table.DataTable(
        id="tabla_pedido",
        data=pedidos,
        columns=columnas,
        row_deletable=True,
        cell_selectable=False,
        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold', "textAlign": "center"})

    return tabla
