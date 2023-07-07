import dash
import dash_bootstrap_components as dbc
from dash import html, State, Input, Output, callback, no_update, dcc, dash_table
from soporte.sistema_colas_5 import SistemaColas
from components.tp5.tab_parametros import crear_tab_parametros
from components.tp5.resultados_sistema_colas import crear_resultados_simulacion
import components.tp5.resultado_runge_kutta as trk
import soporte.runge_kutta as rk

dash.register_page(__name__,
                   path="/tp5/",
                   title="Trabajo Práctico 5",
                   name="Trabajo Práctico 5")

# Estructura de la página
layout = html.Div([
    dbc.Container([

        html.Center(html.H1('Trabajo Práctico Nº5: Modelo Combinado (Virus Informatico)'), className="mb-3"),

        crear_tab_parametros(),

        dbc.Toast("Los datos ingresados no son válidos, revíselos nuevamente.", icon="danger", dismissable=True,
                  id="toast_tp5", is_open=False, header="Simulación no generada.", duration=8000,
                  style={"position": "fixed", "top": 66, "right": 10, "width": 350}),
    ]),

    dbc.Container([

        dbc.InputGroup([
            dbc.Select(
                id="ddm_runge",
                value=""
            ),
            dbc.InputGroupText("Mostrar tabla Runge-Kutta")
        ], id="ig_runge", style={"display": "none"}),

        html.Div({}, id="div_seleccion_runge")

    ], className="mt-3 mb-3"),

    html.Div({}, id="div_resultados_tp5")
])


# Callback que hace cargar el botón hasta que termine la simulación
@callback(
    Output("btn_simular_5", "children", allow_duplicate=True),
    Output("btn_simular_5", "disabled", allow_duplicate=True),
    Output("div_resultados_tp5", "children", allow_duplicate=True),
    Output("div_seleccion_runge", "children", allow_duplicate=True),
    Output("ig_runge", "style", allow_duplicate=True),
    Input("btn_simular_5", "n_clicks"),
    prevent_initial_call=True
)
def cargar_boton(n_clicks):
    contenido_boton = [dbc.Spinner(size="sm"), " Cargando..."]
    return contenido_boton, True, {}, {}, {"display": "none"}


# Callback para el proceso de simulación y generación de resultados
@callback(
    Output("div_resultados_tp5", "children"),
    Output("toast_tp5", "is_open"),
    Output("btn_simular_5", "children"),
    Output("btn_simular_5", "disabled"),
    Output("ddm_runge", "options"),
    Output("ig_runge", "style"),
    Input("btn_simular_5", "n_clicks"),
    State("in_cantidad_iteraciones_5", "value"),
    State("in_iteracion_a_grabar_5", "value"),
    State("in_semilla_simulacion_5", "value"),
    State("in_a_lleg_pasaj_mod_5", "value"),
    State("in_b_lleg_pasaj_mod_5", "value"),
    State("in_media_lleg_pasaj_crit_5", "value"),
    State("in_lambda_cercania_5", "value"),
    State("in_lambda_interprovincial_5", "value"),
    State("in_lambda_anticipada_5", "value"),
    State("in_lambda_maquina_5", "value"),
    State("in_cte_impaciente_5", "value"),
    State("in_inicio_auxiliar_5", "value"),
    State("in_iteracion_a_mostrar_5", "value"),
    prevent_initial_call=True
)
def ejecutar_simulacion(n_clicks, ctd_iter, iter_a_grabar, semilla, a_lleg_mod, b_lleg_mod, media_lleg_pasaj, lam_cerc,
                        lam_inter, lam_antic, lam_maq, cte_impac, inicio_auxiliar, total_iter):

    # Validación de datos
    if None in [ctd_iter, iter_a_grabar, a_lleg_mod, b_lleg_mod, media_lleg_pasaj, lam_cerc, lam_inter, lam_antic,
                lam_maq, cte_impac, inicio_auxiliar]:
        return {}, True, "Generar simulación", False, no_update

    # Ejecución de simulación
    simulacion = SistemaColas(semilla)
    simulacion.generar_parametros(a_lleg_mod, b_lleg_mod, media_lleg_pasaj, lam_cerc, lam_inter, lam_maq, lam_antic,
                                  cte_impac, inicio_auxiliar, total_iter)
    filas = simulacion.simular(ctd_iter, iter_a_grabar)

    # Generación de tabla
    resultado = crear_resultados_simulacion(filas)

    lista = []
    for i in filas:
        if i[65] is not None and i[56] is not None:
            lista.append({"label": f"{i[0]} - Llegada Virus", "value": [i[0], 'Llegada Virus', i[1], i[65], 0.1]})
        if i[60] is not None and i[58] is not None:
            lista.append({"label": f"{i[0]} - Detencion Servicio", "value": [i[0], 'Detencion Servicio', i[1], 0.1]})
        if i[58] is not None and i[63] is not None:
            lista.append({"label": f"{i[0]} - Detencion Cliente", "value": [i[0], 'Detencion Cliente', i[1], 0.1]})

    return resultado, False, "Generar simulación", False, lista, {"display": "flex"}

@callback(
    Output("div_seleccion_runge", "children"),
    Input("ddm_runge", "value"),
    prevent_initial_call=True
)
def mostrar_tabla_runge(palabra):

    fila = palabra.split(",")

    if fila[1] == "Llegada Virus":
        filas_rk = rk.cuando_detiene(float(fila[2]), float(fila[3]), float(fila[4]))
        resultado = trk.crear_resultados_simulacion(filas_rk, 'A')
        return resultado
    if fila[1] == "Detencion Servicio":
        filas_rk = rk.detencion_servidor(float(fila[2]), float(fila[3]))
        resultado = trk.crear_resultados_simulacion(filas_rk, 'L')
        return resultado
    if fila[1] == "Detencion Cliente":
        filas_rk = rk.detencion_cliente(float(fila[2]), float(fila[3]))
        resultado = trk.crear_resultados_simulacion(filas_rk, 'S')
        return resultado
