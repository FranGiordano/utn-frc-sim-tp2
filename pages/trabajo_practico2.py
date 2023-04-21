import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, no_update, callback, html
import soporte.simulacion as sim
from soporte.componentes import select_distribucion, generar_parametros, generar_histograma, generar_visualizacion

dash.register_page(__name__,
                   path="/tp2/",
                   title="Trabajo Práctico 2",
                   name="Trabajo Práctico 2")

# Esta es la estructura de la pagina
layout = dbc.Container([
    html.H1('Trabajo Práctico Nº2: Variables Aleatorias'),
    select_distribucion(),
    html.Br(),
    generar_parametros(),
    html.Br(),
    dbc.Alert("Distribución no generada. Revise nuevamente los datos.", color="danger", dismissable=True,
              id="alerta", is_open=False),
    dbc.Spinner(id="sp_resultados", children={}, color="primary", show_initially=False),
    html.Br()
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
    """
    Muestra u oculta los forms de parámetros dependiendo el tipo de distribución seleccionado.

    :param p_value: El tipo de distribución seleccionado.
    :return: La propiedad de visible o invisible para cada uno de los forms.
    """

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
    """
    Lee los parámetros de los forms y el tipo de distribución, y genera y muestra los resultados en base a dichos
    parámetros.

    :param n_clicks: Cantidad de clicks del botón "btn-cargar-gráfico" (NO SE USA)
    :param distribucion: Tipo de distribución.
    :param n: Cantidad de muestras.
    :param li: Límite inferior (aplicado en distribución uniforme).
    :param ls: Límite superior (aplicado en distribución uniforme).
    :param media: Media (aplicado en distribución normal).
    :param desv: Desviación estándar (aplicado en distribución exponencial negativa).
    :param lam: Lambda (aplicado en distribución exponencial negativa y de Poisson).
    :param intervalos: Cantidad de intervalos
    :return: Una alerta si hubo un error o las visualizaciones correspondientes si la función se procesó con éxito.
    """

    # Chequeo de formularios y generación de muestras por distribución

    match distribucion:

        case "U":

            if None in [n, li, ls, intervalos]:
                return True, no_update

            if float(li) > float(ls):
                return True, no_update

            serie = sim.generar_serie_uniforme(n, float(li), float(ls))

        case "N":

            if None in [n, media, desv, intervalos]:
                return True, no_update

            serie = sim.generar_serie_normal(int(n), float(desv), float(media))

        case "EN":

            if None in [n, lam, intervalos]:
                return True, no_update

            serie = sim.generar_serie_exponencial_negativa(int(n), float(lam))

        case "P":

            if None in [n, lam]:
                return True, no_update

            serie = sim.generar_serie_poisson(int(n), float(lam))

        case _:
            return True, no_update

    # Cálculo de parámetros

    cant_muestras, media, varianza, desv_est = sim.calcular_parametros(serie)

    # Generación y cálculo de frecuencias observadas y esperadas

    match distribucion:

        case "N":
            lista_li, lista_ls, lista_marca, lista_fo = sim.generar_intervalos_dist_continua(serie, intervalos)
            lista_fe = sim.calcular_frecuencia_esperada_normal(lista_li, lista_ls, lista_marca, cant_muestras, media,
                                                               desv_est)

        case "U":
            lista_li, lista_ls, lista_marca, lista_fo = sim.generar_intervalos_dist_continua(serie, intervalos)
            lista_fe = sim.calcular_frecuencia_esperada_uniforme(cant_muestras, intervalos)

        case "EN":
            lista_li, lista_ls, lista_marca, lista_fo = sim.generar_intervalos_dist_continua(serie, intervalos)
            lista_fe = sim.calcular_frecuencia_esperada_exp_neg(lista_li, lista_ls, cant_muestras, media)

        case "P":
            lista_marca, lista_fo = sim.generar_intervalos_dist_discreta(serie)
            lista_fe = sim.calcular_frecuencia_esperada_poisson(lista_marca, media, cant_muestras)

        case _:
            return True, no_update

    if distribucion in ("N", "EN", "U"):
        datos_frecuencia = {
            "#": range(intervalos),
            "Desde": [round(i, 4) for i in lista_li],
            "Hasta": [round(i, 4) for i in lista_ls],
            "Marca de clase": [round(i, 4) for i in lista_marca],
            "Frecuencia observada": lista_fo,
            "Frecuencia esperada": [round(i, 0) for i in lista_fe]
        }
    else:
        datos_frecuencia = {
            "#": [i for i in range(len(lista_fo))],
            "Marca de clase": lista_marca,
            "Frecuencia observada": lista_fo,
            "Frecuencia esperada": lista_fe
        }

    # Cálculo de chi2

    chi2_calculado, chi2_tabulado, nivel_de_confianza, grados_libertad = sim.calcular_chi2(lista_fo, lista_fe,
                                                                                           distribucion)
    datos_chi2 = {
        "Nivel de confianza": nivel_de_confianza,
        "Grados de libertad": grados_libertad,
        "χ2 calculado": round(chi2_calculado, 4),
        "χ2 tabulado": round(chi2_tabulado, 4),
    }

    # Cálculo de ks si aplica

    if distribucion in ("N", "EN", "U"):
        ks_calculado, ks_tabulado, nivel_de_confianza = sim.calcular_ks(lista_fo, lista_fe)
        datos_ks = {
            "Nivel de confianza": nivel_de_confianza,
            "Cantidad de muestras": n,
            "K-S calculado": round(ks_calculado, 4),
            "K-S tabulado": round(ks_tabulado, 4)
        }
    else:
        datos_ks = None

    # Generación de visualizacion
    histograma = generar_histograma(lista_marca, lista_fo, lista_fe)
    visualizacion = generar_visualizacion(histograma, serie, datos_frecuencia, datos_chi2, datos_ks)

    return False, visualizacion
