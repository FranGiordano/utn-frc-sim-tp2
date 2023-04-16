from dash import Dash, dcc, html, Input, Output, no_update, State
import dash_bootstrap_components as dbc
import soporte.simulacion as sim
from dash.exceptions import PreventUpdate

app = Dash(__name__, suppress_callback_exceptions=True,
           external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server
tipo_distribucion = dcc.RadioItems(options=['uniforme', 'normal', 'exponencial', 'poisson'],
                                   value='',
                                   id='controls-dist')

btn_generar_grafico = dbc.Col(dbc.Button("Generar distribución",
                                         id="btn_cargar_grafico",
                                         color="primary"),
                              class_name="col-auto align-self-end")

txt_box_cantidad = dbc.Col([
    dbc.FormFloating([
        dbc.Input(id="in_cantidad_muestras", placeholder="Cantidad de muestras", type="number", max=50000,
                  min=0, step=1, value=10000, required=True),
        dbc.Label("Cantidad de muestras"),
    ])])

txt_box_limite_inferior = dbc.Col([
    dbc.FormFloating([
        dbc.Input(id="in_limite_inferior", placeholder="Límite inferior", type="number",
                  value=-10, required=True, step=0.0001),
        dbc.Label("Límite inferior"),
    ])])

txt_box_limite_superior = dbc.Col([
    dbc.FormFloating([
        dbc.Input(id="in_limite_superior", placeholder="Límite superior", type="number",
                  value=10, required=True, step=0.0001),
        dbc.Label("Límite superior"),
    ])])

txt_box_cantidad_intervalos = dbc.Col(id='form-intervalos',
                                      children=[
                                          dbc.FormFloating([
                                              dbc.Input(id="in_intervalos",
                                                        placeholder="Cantidad de intervalos",
                                                        type="number", min=1, step=1,
                                                        value=15, required=True, max=225),
                                              dbc.Label("Cantidad de intervalos"),
                                          ])])

txt_box_media = dbc.Col(id='form-media', style={"display": "block"},
                        children=[
                            dbc.FormFloating([
                                dbc.Input(id="in_media", placeholder="Media", type="number",
                                          value=0, required=True, step=0.0001),
                                dbc.Label("Media"),
                            ])])

txt_box_desviacion = dbc.Col([
    dbc.FormFloating([
        dbc.Input(id="in_desviacion", placeholder="Desviación Estándar", type="number",
                  value=1, required=True, step=0.0001),
        dbc.Label("Desviación Estándar"),
    ])])

txt_box_lambda = dbc.Col([
    dbc.FormFloating([
        dbc.Input(id="in_lambda", placeholder="Lambda", type="number",
                  value=0, required=True, step=0.0001),
        dbc.Label("Lambda"),
    ])])

parametros = [txt_box_cantidad, txt_box_cantidad_intervalos]
parametros_uniforme = parametros + [txt_box_limite_inferior, txt_box_limite_superior, btn_generar_grafico]
parametros_normal = parametros + [txt_box_media, txt_box_desviacion, btn_generar_grafico]

parametros_exponencial_poisson = parametros + [txt_box_lambda, btn_generar_grafico]

app.layout = dbc.Container([
    html.H1('Trabajo Práctico Número 2'),
    tipo_distribucion,
    dbc.Col(dbc.Button("Seleccionar Distribucion",
                                         id="btn_cargar_param",
                                         color="primary"),
                              class_name="col-auto align-self-end"),
    html.H2(id="titulo-distribucion"),
    html.Div(id="parametros"),
    dcc.Graph(id="histograma", figure={})
])


@app.callback(
    Output('parametros', 'children'),
    Input('btn_cargar_param', 'n_clicks'),
    State('controls-dist', 'value')
)
def mostrar_parametros(n_clicks, p_value, ):
    if n_clicks == None:
        raise PreventUpdate
    res = parametros
    if p_value == 'uniforme':
        res = parametros_uniforme
    elif p_value == 'normal':
        res = parametros_normal
    elif p_value in ('exponencial', 'poisson'):
        res = parametros_exponencial_poisson
    return res


@app.callback(
    Output('titulo-distribucion', 'children'),
    Input('btn_cargar_param', 'n_clicks'),
    State('controls-dist', 'value')
)
def funcionalidad_generar(n_clicks, distribucion):
    if n_clicks == None:
        raise PreventUpdate
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
        def generar_grafico(n_clicks, n, li, ls, intervalos):
            print('Click U: ')
            print(n_clicks)

            if None in [n, li, ls, intervalos, n_clicks]:
                raise PreventUpdate

            if float(li) > float(ls):
                return {}

            serie = sim.generar_lista_uniforme(int(n), float(li), float(ls))
            histograma = sim.generar_histograma(serie, intervalos)

            print(histograma)
            print(serie)

            return histograma

        return 'Distribución Uniforme'

    elif distribucion == 'normal':
        @app.callback(
            Output('histograma', 'figure'),
            Input("btn_cargar_grafico", "n_clicks"),
            State("in_cantidad_muestras", "value"),
            State("in_media", "value"),
            State("in_desviacion", "value"),
            State("in_intervalos", "value"),
            prevent_initial_call=True

        )
        def generar_grafico(n_clicks, n, media, desv, intervalos):
            print('Click N: ')
            print(n_clicks)
            if distribucion != 'normal':
                return no_update

            if None in [n, media, desv, intervalos, n_clicks]:
                raise PreventUpdate

            serie = sim.generar_lista_normal(int(n), float(desv), float(media))
            histograma = sim.generar_histograma(serie, intervalos)
            print(serie)
            print(histograma)

            return histograma

        return 'Distribución Normal'
    elif distribucion == 'exponencial':
        # FALTA EL CALLBACK Y LA FUNCIONALIDAD DE LA DISTRIBUCION exponencial

        return 'Distribución Exponencial'
    elif distribucion == 'poisson':
        return 'Distribución Poisson'


if __name__ == '__main__':
    app.run_server(debug=True)
