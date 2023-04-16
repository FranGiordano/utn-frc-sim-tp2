from dash import Dash, html, Input, Output, State
import soporte.simulacion as sim
from soporte.componentes import *
from dash.exceptions import PreventUpdate

# Se crea la app y el servidor
app = Dash(__name__, suppress_callback_exceptions=True,
           external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

# Defino todos los parametros a meter en la app
parametros_todos = [txt_box_cantidad, txt_box_cantidad_intervalos,
                    txt_box_limite_inferior, txt_box_limite_superior,
                    txt_box_media, txt_box_desviacion,
                    txt_box_lambda, btn_generar_grafico]

# Esta es la estructura de la pagina web
app.layout = dbc.Container([
    html.H1('Trabajo Práctico Número 2'),
    tipo_distribucion,
    html.H2(id="titulo-distribucion"),
    html.Div(id="parametros", children=parametros_todos),
    dcc.Graph(id="histograma", figure={})
])


# Este callback oculta y muestra (cambiando el css style del display ) los parametros segun la distribucion
# seleccionada en los radiobuttons. Tambien cambia el titulo h2 de la distribucion
@app.callback(

    Output('form-limite-inferior', 'style'),
    Output('form-limite-superior', 'style'),
    Output('form-media', 'style'),
    Output('form-desv', 'style'),
    Output('form-lambda', 'style'),
    Output('titulo-distribucion', 'children'),
    Input('controls-dist', 'value')
)
def mostrar_parametros(p_value):
    visible = {"display": "block"}
    oculto = {"display": "none"}
    titulo = 'Distribucion ' + p_value.capitalize()
    if p_value == 'uniforme':
        return visible, visible, oculto, oculto, oculto, titulo
    elif p_value == 'normal':
        return oculto, oculto, visible, visible, oculto, titulo
    elif p_value in ('exponencial', 'poisson'):
        return oculto, oculto, oculto, oculto, visible, titulo
    return oculto, oculto, oculto, oculto, oculto, titulo


# Este callback se activa cuando cambia la cantidad de clicks realizados en el btn-generar-grafico.
# segun la distribucion seleccionada, alterna la funcion que crea la serie de numeros que usa en el histograma
@app.callback(
    Output('histograma', 'figure'),
    Input("btn_cargar_grafico", "n_clicks"),
    State('controls-dist', 'value'),
    State("in_cantidad_muestras", "value"),
    State("in_limite_inferior", "value"),
    State("in_limite_superior", "value"),
    State("in_media", "value"),
    State("in_desviacion", "value"),
    State("in_lambda", "value"),
    State("in_intervalos", "value"),
    prevent_initial_call=True

)
def generar_grafico(n_clicks, distribucion, n, li, ls, media, desv, lam, intervalos):
    print('Click U: ')
    print(n_clicks)
    serie = []

    if distribucion == 'uniforme':
        if None in [n, li, ls, intervalos, n_clicks]:
            raise PreventUpdate

        if float(li) > float(ls):
            raise PreventUpdate

        serie = sim.generar_lista_uniforme(int(n), float(li), float(ls))
    elif distribucion == 'normal':
        serie = sim.generar_lista_normal(int(n), float(desv), float(media))
    elif distribucion == 'exponencial':
        serie = sim.generar_lista_exponencial_negativa(int(n), float(lam))
    elif distribucion == 'poisson':
        serie = sim.generar_lista_poisson(int(n), float(lam))

    print(serie)
    histograma = sim.generar_histograma(serie, intervalos)

    return histograma


# Corre el Servidor
if __name__ == '__main__':
    app.run_server(debug=True)
