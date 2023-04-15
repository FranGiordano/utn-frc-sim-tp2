from dash import Dash, dcc, html, Input, Output, no_update, State
import dash_bootstrap_components as dbc
import soporte.simulacion as sim

app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

app.layout = dbc.Container([
    html.H1('Trabajo Práctico Número 2'),

    dbc.Row([

            dbc.Col([
                dbc.FormFloating([
                    dbc.Input(id="in_cantidad_muestras", placeholder="Cantidad de muestras", type="number", max=50000,
                              min=0, step=1, value=10000, required=True),
                    dbc.Label("Cantidad de muestras"),
                ])]),

            dbc.Col([
                dbc.FormFloating([
                    dbc.Input(id="in_limite_inferior", placeholder="Límite inferior", type="number",
                              value=-10, required=True, step=0.0001),
                    dbc.Label("Límite inferior"),
                ])]),

            dbc.Col([
                dbc.FormFloating([
                    dbc.Input(id="in_limite_superior", placeholder="Límite superior", type="number",
                              value=10, required=True, step=0.0001),
                    dbc.Label("Límite superior"),
                ])]),

            dbc.Col([
                dbc.FormFloating([
                    dbc.Input(id="in_intervalos", placeholder="Cantidad de intervalos", type="number", min=1, step=1,
                              value=15, required=True, max=225),
                    dbc.Label("Cantidad de intervalos"),
                ])]),

            dbc.Col(dbc.Button("Generar distribución", id="btn_cargar_grafico", color="primary"),
                    class_name="col-auto align-self-end")

    ]),

    dcc.Graph(id="histograma", figure={})
])


@app.callback(
    Output('histograma', 'figure'),
    State("in_cantidad_muestras", "value"),
    State("in_limite_inferior", "value"),
    State("in_limite_superior", "value"),
    State("in_intervalos", "value"),
    Input("btn_cargar_grafico", "n_clicks"),
    prevent_initial_call=True
)
def generar_grafico(n, li, ls, intervalos, n_clicks):

    if None in [n, li, ls, intervalos]:
        return True, no_update

    if float(li) > float(ls):
        return True, no_update

    serie = sim.generar_lista_uniforme(int(n), float(li), float(ls))

    histograma = sim.generar_histograma(serie, intervalos)

    return histograma


if __name__ == '__main__':
    app.run_server(debug=True)
