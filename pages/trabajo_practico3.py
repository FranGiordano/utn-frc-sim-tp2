import dash
import dash_bootstrap_components as dbc
from dash import html

dash.register_page(__name__,
                   path="/tp3/",
                   title="Trabajo Práctico 3",
                   name="Trabajo Práctico 3")

# Estructura de la página
layout = dbc.Container([
    html.H1('Trabajo Práctico Nº3: Simulación de Monte Carlo'),
])