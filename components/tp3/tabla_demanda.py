from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc


def crear_tabla_demanda():

    demandas = [{"consumo": 6000, "probabilidad": 0.05},
                {"consumo": 7000, "probabilidad": 0.15},
                {"consumo": 8000, "probabilidad": 0.20},
                {"consumo": 9000, "probabilidad": 0.30},
                {"consumo": 10000, "probabilidad": 0.20},
                {"consumo": 11000, "probabilidad": 0.10}]

    columnas = [{"id": "consumo", "name": "Consumo semanal de acero (m²)"},
                {"id": "probabilidad", "name": "Probabilidad"}]

    tabla = dash_table.DataTable(
        id="tabla_demanda",
        data=demandas,
        columns=columnas,
        row_deletable=True,
        cell_selectable=False,
        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold', "textAlign": "center"})

    return tabla
