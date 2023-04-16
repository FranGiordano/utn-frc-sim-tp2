from dash import Dash, dcc, html, Input, Output, no_update, State
import dash_bootstrap_components as dbc
import soporte.simulacion as sim
from dash.exceptions import PreventUpdate

app = Dash(__name__, suppress_callback_exceptions=True,
           external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server
tipo_distribucion = dcc.RadioItems(options=['uniforme', 'normal', 'exponencial', 'poisson'],
                                   value='uniforme',
                                   id='controls-dist')

btn_generar_grafico = dbc.Col(dbc.Button("Generar distribución",
                                         id="btn_cargar_grafico",
                                         color="primary"),
                              class_name="col-auto align-self-end")

txt_box_cantidad = dbc.Col(id="form-cantidad", children=[
    dbc.FormFloating([
        dbc.Input(id="in_cantidad_muestras", placeholder="Cantidad de muestras", type="number", max=50000,
                  min=0, step=1, value=10000, required=True),
        dbc.Label("Cantidad de muestras"),
    ])])

txt_box_limite_inferior = dbc.Col(id="form-limite-inferior", children=[
    dbc.FormFloating([
        dbc.Input(id="in_limite_inferior", placeholder="Límite inferior", type="number",
                  value=-10, required=True, step=0.0001),
        dbc.Label("Límite inferior"),
    ])])

txt_box_limite_superior = dbc.Col(id="form-limite-superior", children=[
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


txt_box_media = dbc.Col(id='form-media',
                        children=[
                            dbc.FormFloating([
                                dbc.Input(id="in_media", placeholder="Media", type="number",
                                          value=0, required=True, step=0.0001),
                                dbc.Label("Media"),
                            ])])

txt_box_desviacion = dbc.Col(id="form-desv", children=[
    dbc.FormFloating([
        dbc.Input(id="in_desviacion", placeholder="Desviación Estándar", type="number",
                  value=1, required=True, step=0.0001),
        dbc.Label("Desviación Estándar"),
    ])])

txt_box_lambda = dbc.Col(id="form-lambda", children=[
    dbc.FormFloating([
        dbc.Input(id="in_lambda", placeholder="Lambda", type="number",
                  value=0.5, required=True, step=0.0001),
        dbc.Label("Lambda"),
    ])])

parametros = [txt_box_cantidad, txt_box_cantidad_intervalos]
parametros_uniforme = parametros + [txt_box_limite_inferior, txt_box_limite_superior, btn_generar_grafico]
parametros_normal = parametros + [txt_box_media, txt_box_desviacion, btn_generar_grafico]

parametros_exponencial_poisson = parametros + [txt_box_lambda, btn_generar_grafico]
parametros_todos = parametros + [txt_box_limite_inferior, txt_box_limite_superior,
                                 txt_box_media, txt_box_desviacion,
                                 txt_box_lambda, btn_generar_grafico]

app.layout = dbc.Container([
    html.H1('Trabajo Práctico Número 2'),
    tipo_distribucion,
    # dbc.Col(dbc.Button("Seleccionar Distribucion",
    #                                      id="btn_cargar_param",
    #                                      color="primary"),
    #                           class_name="col-auto align-self-end"),
    html.H2(id="titulo-distribucion"),
    html.Div(id="parametros", children=parametros_todos),
    dcc.Graph(id="histograma", figure={})
])


@app.callback(

    Output('form-limite-inferior', 'style'),
    Output('form-limite-superior', 'style'),
    Output('form-media', 'style'),
    Output('form-desv', 'style'),
    Output('form-lambda', 'style'),
    Output('titulo-distribucion', 'children'),
    #Input('btn_cargar_param', 'n_clicks'),
    Input('controls-dist', 'value')
)
def mostrar_parametros(p_value):
    # if n_clicks == None:
    #     raise PreventUpdate
    visible = {"display": "block"}
    oculto = {"display": "none"}
    if p_value == 'uniforme':
        return visible, visible, oculto, oculto, oculto, 'Distribucion Uniforme'
    elif p_value == 'normal':
        return oculto, oculto, visible, visible, oculto, 'Distribucion Normal'
    elif p_value in ('exponencial', 'poisson'):
        return oculto, oculto, oculto, oculto, visible, 'Distribucion ' + p_value.capitalize()
    return oculto, oculto, oculto, oculto, oculto


@app.callback(
    Output('histograma', 'figure'),
    Input("btn_cargar_grafico", "n_clicks"),
    State('controls-dist', 'value'),
    State("in_cantidad_muestras", "value"),
    State("in_limite_inferior", "value"),
    State("in_limite_superior", "value"),
    State("in_media", "value"),
    State("in-desviacion", "value"),
    State("in-lambda", "value"),
    State("in_intervalos", "value"),

    prevent_initial_call=True

)
def generar_grafico(n_clicks,distribucion, n, li, ls, media, desv, lam, intervalos):
    print('Click U: ')
    print(n_clicks)
    serie = []

    if distribucion == 'uniforme':
        if None in [n, li, ls, intervalos, n_clicks]:
            raise PreventUpdate

        if float(li) > float(ls):
            return {}

        serie = sim.generar_lista_uniforme(int(n), float(li), float(ls))
    elif distribucion == 'normal':
        serie = sim.generar_lista_normal(int(n), float(desv), float(media))
    elif distribucion == 'expoenencial':
        serie = sim.generar_lista_exponencial_negativa(int(n), float(lam))
    elif distribucion == 'poisson':
        serie = sim.generar_lista_poisson(int(n), float(lam))

    histograma = sim.generar_histograma(serie, intervalos)

    print(serie)

    return histograma




if __name__ == '__main__':
    app.run_server(debug=True)
