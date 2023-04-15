from dash import Dash, dcc, html, Input, Output, no_update, State
import dash_bootstrap_components as dbc
import soporte.simulacion as sim

app = Dash(__name__, suppress_callback_exceptions=True,
           external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server
tipo_distribucion = dcc.RadioItems(options=['uniforme', 'normal', 'exponencial'], value='uniforme', id='controls-dist')
btn_generar_grafico = dbc.Col(dbc.Button("Generar distribución", id="btn_cargar_grafico", color="primary"),
                              class_name="col-auto align-self-end")

parametros_uniforme = dbc.Row([

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
    btn_generar_grafico

])

parametros_normal = dbc.Row([

    dbc.Col([
        dbc.FormFloating([
            dbc.Input(id="in_cantidad_muestras", placeholder="Cantidad de muestras", type="number", max=50000,
                      min=0, step=1, value=10000, required=True),
            dbc.Label("Cantidad de muestras"),
        ])]),

    dbc.Col([
        dbc.FormFloating([
            dbc.Input(id="in_media", placeholder="Media", type="number",
                      value=0, required=True, step=0.0001),
            dbc.Label("Media"),
        ])]),

    dbc.Col([
        dbc.FormFloating([
            dbc.Input(id="in_desviacion", placeholder="Desviación Estándar", type="number",
                      value=1, required=True, step=0.0001),
            dbc.Label("Desviación Estándar"),
        ])]),

    dbc.Col([
        dbc.FormFloating([
            dbc.Input(id="in_intervalos", placeholder="Cantidad de intervalos", type="number", min=1, step=1,
                      value=15, required=True, max=225),
            dbc.Label("Cantidad de intervalos"),
        ])]),
    btn_generar_grafico

])

app.layout = dbc.Container([
    html.H1('Trabajo Práctico Número 2'),
    tipo_distribucion,
    html.H2(id="titulo-distribucion"),
    html.Div(id="parametros"),
    dcc.Graph(id="histograma", figure={})
])


@app.callback(
    Output('parametros', 'children'),
    Input('controls-dist', 'value')
)
def mostrar_parametros(p_value):

    if p_value == 'uniforme':
        return parametros_uniforme
    elif p_value == 'normal':
        return parametros_normal
    # Faltan definir los parametros de exponencial Y agregar la Poisson
    else:
        return None


@app.callback(
    Output('titulo-distribucion', 'children'),
    Input('controls-dist', 'value')
)
def funcionalidad_generar(distribucion):
    if distribucion == 'uniforme':
        @app.callback(
            Output('histograma', 'figure'),
            Input("btn_cargar_grafico", "n_clicks"),
            State("in_cantidad_muestras", "value"),
            State("in_limite_inferior", "value"),
            State("in_limite_superior", "value"),
            State("in_intervalos", "value"),
            prevent_initial_call=True

        )
        def generar_grafico_uniforme(n_clicks, n, li, ls, intervalos):
            print('Click: ')
            print(n_clicks)

            if None in [n, li, ls, intervalos, n_clicks]:
                return {}

            if float(li) > float(ls):
                return {}

            serie = sim.generar_lista_uniforme(int(n), float(li), float(ls))
            histograma = sim.generar_histograma(serie, intervalos)

            print(histograma)
            return histograma
        return 'Distribución Uniforme'

    elif distribucion == 'normal':
        # FALTA EL CALLBACK Y LA FUNCIONALIDAD DE LA DISTRIBUCION NORMAL

        return 'Distribución Normal'
    elif distribucion == 'exponencial':
        # FALTA EL CALLBACK Y LA FUNCIONALIDAD DE LA DISTRIBUCION exponencial

        return 'Distribución Exponencial'


if __name__ == '__main__':
    app.run_server(debug=True)
