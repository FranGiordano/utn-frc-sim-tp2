import dash
import dash_bootstrap_components as dbc
from dash import html, State, Input, Output, callback, no_update, dcc
from soporte.sistema_colas import SistemaColas

dash.register_page(__name__,
                   path="/tp4/",
                   title="Trabajo Práctico 4",
                   name="Trabajo Práctico 4")

# Estructura de la página
layout = dbc.Container([

    html.Center(html.H1('Trabajo Práctico Nº4: Modelos de Simulación Dinámicos (Trenes)')),

])