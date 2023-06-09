import dash
import dash_bootstrap_components as dbc
from dash import html, State, Input, Output, callback, no_update, dcc
from soporte.sistema_colas import SistemaColas
from components.tp4.tab_parametros import crear_tab_parametros
from components.tp4.resultados_sistema_colas import crear_resultados_simulacion

dash.register_page(__name__,
                   path="/tp4/",
                   title="Trabajo Práctico 4",
                   name="Trabajo Práctico 4")

# Estructura de la página
layout = html.Div([
    dbc.Container([

        html.Center(html.H1('Trabajo Práctico Nº4: Modelos de Simulación Dinámicos (Trenes)'), className="mb-3"),

        crear_tab_parametros(),

        dbc.Toast("Los datos ingresados no son válidos, revíselos nuevamente.", icon="danger", dismissable=True,
                  id="toast_tp4", is_open=False, header="Simulación no generada.", duration=8000,
                  style={"position": "fixed", "top": 66, "right": 10, "width": 350}),
    ]),
    html.Div({}, id="div_resultados_tp4")
])


# Callback que hace cargar el botón hasta que termine la simulación
@callback(
    Output("btn_simular", "children", allow_duplicate=True),
    Output("btn_simular", "disabled", allow_duplicate=True),
    Output("div_resultados_tp4", "children", allow_duplicate=True),
    Input("btn_simular", "n_clicks"),
    prevent_initial_call=True
)
def cargar_boton(n_clicks):
    contenido_boton = [dbc.Spinner(size="sm"), " Cargando..."]
    return contenido_boton, True, {}


# Callback para el proceso de simulación y generación de resultados
@callback(
    Output("div_resultados_tp4", "children"),
    Output("toast_tp4", "is_open"),
    Output("btn_simular", "children"),
    Output("btn_simular", "disabled"),
    Input("btn_simular", "n_clicks"),
    State("in_cantidad_iteraciones", "value"),
    State("in_iteracion_a_grabar", "value"),
    State("in_semilla_simulacion", "value"),
    State("in_a_lleg_pasaj_mod", "value"),
    State("in_b_lleg_pasaj_mod", "value"),
    State("in_media_lleg_pasaj_crit", "value"),
    State("in_lambda_cercania", "value"),
    State("in_lambda_interprovincial", "value"),
    State("in_lambda_anticipada", "value"),
    State("in_lambda_maquina", "value"),
    State("in_cte_impaciente", "value"),
    State("in_inicio_auxiliar", "value"),
    prevent_initial_call=True
)
def ejecutar_simulacion(n_clicks, ctd_iter, iter_a_grabar, semilla, a_lleg_mod, b_lleg_mod, media_lleg_pasaj, lam_cerc,
                        lam_inter, lam_antic, lam_maq, cte_impac, inicio_auxiliar):

    # Validación de datos
    if None in [ctd_iter, iter_a_grabar, a_lleg_mod, b_lleg_mod, media_lleg_pasaj, lam_cerc, lam_inter, lam_antic,
                lam_maq, cte_impac, inicio_auxiliar]:
        return {}, True, "Generar simulación", False

    # Ejecución de simulación
    simulacion = SistemaColas(semilla)
    simulacion.generar_parametros(a_lleg_mod, b_lleg_mod, media_lleg_pasaj, lam_cerc, lam_inter, lam_maq, lam_antic,
                                  cte_impac, inicio_auxiliar)
    filas = simulacion.simular(ctd_iter, iter_a_grabar)

    # Generación de tabla
    resultado = crear_resultados_simulacion(filas)

    return resultado, False, "Generar simulación", False
