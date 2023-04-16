import dash
from dash import Input, Output, State, no_update, callback, html
import dash_bootstrap_components as dbc
import soporte.simulacion as sim
from soporte.componentes import generar_tipos_distribuciones, generar_parametros, generar_visualizacion

dash.register_page(__name__,
                   path="/tp2/",
                   title="Trabajo Práctico 2",
                   name="Trabajo Práctico 2")

# Esta es la estructura de la pagina
layout = dbc.Container([
    html.H1('Trabajo Práctico Nº2: Variables Aleatorias'),
    generar_tipos_distribuciones(),
    html.Br(),
    generar_parametros(),
    html.Br(),
    dbc.Alert("Distribución no generada. Revise nuevamente los datos.", color="danger", dismissable=True,
              id="alerta", is_open=False),
    dbc.Spinner(id="sp_resultados", children={}, color="primary", show_initially=False)
])


# Este callback oculta y muestra (cambiando el css style del display ) los parametros segun la distribucion
# seleccionada en los radiobuttons. Tambien cambia el titulo h2 de la distribucion
@callback(
    Output('form-limite-inferior', 'style'),
    Output('form-limite-superior', 'style'),
    Output('form-media', 'style'),
    Output('form-desv', 'style'),
    Output('form-lambda', 'style'),
    Output('form-intervalos', 'style'),
    Input('controls-dist', 'value')
)
def mostrar_parametros(p_value):
    visible = {"display": "block"}
    oculto = {"display": "none"}
    match p_value:
        case "U":
            return visible, visible, oculto, oculto, oculto, visible
        case "N":
            return oculto, oculto, visible, visible, oculto, visible
        case "EN":
            return oculto, oculto, oculto, oculto, visible, visible
        case "P":
            return oculto, oculto, oculto, oculto, visible, oculto
        case _:
            return oculto, oculto, oculto, oculto, oculto, oculto


# Este callback se activa cuando cambia la cantidad de clicks realizados en el btn-generar-grafico.
# segun la distribucion seleccionada, alterna la funcion que crea la serie de numeros que usa en el histograma
@callback(
    Output("alerta", "is_open"),
    Output('sp_resultados', 'children'),
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
    # Chequeo de formularios y generación de muestras por distribución
    match distribucion:

        case "U":

            if None in [n, li, ls, intervalos]:
                return True, no_update

            if float(li) > float(ls):
                return True, no_update

            serie = sim.generar_lista_uniforme(int(n), float(li), float(ls))

        case "N":

            if None in [n, media, desv, intervalos]:
                return True, no_update

            serie = sim.generar_numeros_aleatorios_normal(int(n), float(desv), float(media))

        case "EN":

            if None in [n, lam, intervalos]:
                return True, no_update

            serie = sim.generar_lista_exponencial_negativa(int(n), float(lam))

        case "P":

            if None in [n, lam]:
                return True, no_update

            serie = sim.generar_lista_poisson(int(n), float(lam))

        case _:
            return True, no_update

    # Generación de histograma y datos de acuerdo a distribución
    match distribucion:

        case "N" | "U" | "EN":

            histograma = sim.generar_histograma_continua(serie, intervalos)
            datos_frecuencia = sim.calcular_frecuencias_continua(serie, intervalos, distribucion)
            datos_chi2 = sim.calcular_chi2(datos_frecuencia["Frecuencia observada"],
                                           datos_frecuencia["Frecuencia esperada"], distribucion)
            datos_ks = sim.calcular_ks(datos_frecuencia["Frecuencia observada"],
                                       datos_frecuencia["Frecuencia esperada"])

        case "P":

            histograma = sim.generar_histograma_poisson(serie)
            datos_frecuencia = sim.calcular_frecuencias_poisson(serie)
            datos_chi2 = sim.calcular_chi2(datos_frecuencia["Frecuencia observada"],
                                           datos_frecuencia["Frecuencia esperada"], distribucion)
            datos_ks = None

        case _:
            return True, no_update

    # Generación de visualizacion
    visualizacion = generar_visualizacion(histograma, datos_frecuencia, datos_chi2, datos_ks)

    return False, visualizacion
