import dash
from dash import Dash, html
import dash_bootstrap_components as dbc
from components.barra_navegacion import crear_barra_navegacion

# Se crea la app y el servidor
app = Dash(__name__,
           title="Simulación",
           meta_tags=[{"name": "viewport", "content": "width=device-width"}],
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           use_pages=True)

app._favicon = "/assets/icons/favicon.ico"

server = app.server

# Esta es la estructura de la pagina web
app.layout = html.Div([
    # Barra de navegación
    crear_barra_navegacion(),
    html.Br(),
    # Contenido de cada página
    dash.page_container
])

# Corre el Servidor
if __name__ == '__main__':
    app.run_server(debug=True)
