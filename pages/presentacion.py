import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__,
                   path="",
                   title="Simulación",
                   update_title="Simulación",
                   name="Simulación")

layout = dbc.Container([
    html.H1("Integrantes: "),
    html.H3("pepe")
])
