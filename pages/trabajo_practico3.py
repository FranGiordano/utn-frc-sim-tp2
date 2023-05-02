import dash
import dash_bootstrap_components as dbc
from dash import html, State, Input, Output, callback, no_update
from components.tp3.parametros_montecarlo_negocio import crear_parametros_montecarlo_negocio
from components.tp3.parametros_montecarlo_simulacion import crear_parametros_montecarlo_simulacion
from components.tp3.tabla_demanda import crear_tabla_demanda
from components.tp3.tabla_pedido import crear_tabla_pedido
from components.tp3.parametros_tabla_pedido import crear_parametros_tabla_pedido
from components.tp3.parametros_tabla_demanda import crear_parametros_tabla_demanda
from components.general.tabla import crear_tabla
from soporte.montecarlo import MonteCarloLavarropa

dash.register_page(__name__,
                   path="/tp3/",
                   title="Trabajo Práctico 3",
                   name="Trabajo Práctico 3")

# Estructura de la página
layout = dbc.Container([
    html.Center(html.H1('Trabajo Práctico Nº3: Simulación de Montecarlo (Lavarropas)')),

    dbc.Tabs([

        dbc.Tab(dbc.Card(dbc.CardBody([
            crear_parametros_montecarlo_negocio(),
            crear_parametros_montecarlo_simulacion(),
        ]), className="mt-3"), label="Parámetros"),

        dbc.Tab(dbc.Card(dbc.CardBody([
            dbc.Row([
                dbc.Col(crear_tabla_demanda()),
                dbc.Col(crear_tabla_pedido()),
            ]),
            dbc.Row([
                dbc.Col(crear_parametros_tabla_demanda()),
                dbc.Col(crear_parametros_tabla_pedido()),
            ], className="mt-3"),
        ]), className="mt-3"), label="Tablas de probabilidad"),

    ], className="mt-3"),

    dbc.Toast("Los datos ingresados no son válidos, revíselos nuevamente.", icon="danger", dismissable=True,
              id="toast_tp3", is_open=False, header="Simulación no generada.", duration=8000,
              style={"position": "fixed", "top": 66, "right": 10, "width": 350},),

    dbc.Spinner(id="sp_resultados_tp3", children={}, color="primary", show_initially=False, spinnerClassName="mt-3"),

])


# Callback para añadir una fila a la tabla demanda y actualizar alertas correspondientes
@callback(
    Output("tabla_demanda", "data", allow_duplicate=True),
    Output("alerta_demanda", "children", allow_duplicate=True),
    Output("alerta_demanda", "color", allow_duplicate=True),
    Input("btn_crear_fila_demanda", "n_clicks"),
    State("in_demanda_consumo", "value"),
    State("in_demanda_probabilidad", "value"),
    State("tabla_demanda", "data"),
    prevent_initial_call=True
)
def crear_fila_tabla_demanda(n_clicks, consumo, probabilidad, filas):

    suma_probabilidades = round(sum([fila["probabilidad"] for fila in filas]), 2)

    if None in [consumo, probabilidad]:
        return no_update, no_update, no_update

    fila = {"consumo": consumo, "probabilidad": probabilidad}

    suma_probabilidades = round(suma_probabilidades + probabilidad, 2)

    bandera_repetido = False
    for fila in filas:
        if fila["consumo"] == consumo:
            fila["probabilidad"] = round(fila["probabilidad"] + probabilidad, 2)
            bandera_repetido = True

    if not bandera_repetido:
        filas.append(fila)

    if suma_probabilidades == 1:
        return filas, f"Probabilidad acumulada: {suma_probabilidades}", "success"
    else:
        return filas, f"Probabilidad acumulada: {suma_probabilidades}", "warning"


# Callback para actualizar alertas correspondientes al eliminar fila de tabla demanda
@callback(
    Output("tabla_demanda", "data", allow_duplicate=True),
    Output("alerta_demanda", "children", allow_duplicate=True),
    Output("alerta_demanda", "color", allow_duplicate=True),
    Input("tabla_demanda", "data"),
    prevent_initial_call=True
)
def actualizar_alertas_tabla_demanda(filas):

    suma_probabilidades = round(sum([fila["probabilidad"] for fila in filas]), 2)

    if suma_probabilidades == 1:
        return filas, f"Probabilidad acumulada: {suma_probabilidades}", "success"
    else:
        return filas, f"Probabilidad acumulada: {suma_probabilidades}", "warning"


# Callback para añadir una fila a la tabla pedido y actualizar alertas correspondientes
@callback(
    Output("tabla_pedido", "data", allow_duplicate=True),
    Output("alerta_pedido", "children", allow_duplicate=True),
    Output("alerta_pedido", "color", allow_duplicate=True),
    Input("btn_crear_fila_pedido", "n_clicks"),
    State("in_pedido_tamanio", "value"),
    State("in_pedido_probabilidad", "value"),
    State("tabla_pedido", "data"),
    prevent_initial_call=True
)
def crear_fila_tabla_pedido(n_clicks, tamanio, probabilidad, filas):

    suma_probabilidades = round(sum([fila["probabilidad"] for fila in filas]), 2)

    if None in [tamanio, probabilidad]:
        return no_update, no_update, no_update

    fila = {"pedido": tamanio, "probabilidad": probabilidad}

    suma_probabilidades = round(suma_probabilidades + probabilidad, 2)

    bandera_repetido = False
    for fila in filas:
        if fila["pedido"] == tamanio:
            fila["probabilidad"] = round(fila["probabilidad"] + probabilidad, 2)
            bandera_repetido = True

    if not bandera_repetido:
        filas.append(fila)

    if suma_probabilidades == 1:
        return filas, f"Probabilidad acumulada: {suma_probabilidades}", "success"
    else:
        return filas, f"Probabilidad acumulada: {suma_probabilidades}", "warning"


# Callback para actualizar alertas correspondientes al eliminar fila de tabla pedido
@callback(
    Output("tabla_pedido", "data", allow_duplicate=True),
    Output("alerta_pedido", "children", allow_duplicate=True),
    Output("alerta_pedido", "color", allow_duplicate=True),
    Input("tabla_pedido", "data"),
    prevent_initial_call=True
)
def actualizar_alertas_tabla_pedido(filas):

    suma_probabilidades = round(sum([fila["probabilidad"] for fila in filas]), 2)

    if suma_probabilidades == 1:
        return filas, f"Probabilidad acumulada: {suma_probabilidades}", "success"
    else:
        return filas, f"Probabilidad acumulada: {suma_probabilidades}", "warning"


# Callback para el proceso de simulación y generación de resultados
@callback(
    Output("toast_tp3", "is_open"),
    Output('sp_resultados_tp3', 'children'),
    Input("btn_generar_simulacion", "n_clicks"),
    State("in_inventario", "value"),
    State("in_stock_inicial", "value"),
    State("in_costo_sobrepaso", "value"),
    State("in_costo_mantenimiento", "value"),
    State("in_costo_pedido", "value"),
    State("tabla_demanda", "data"),
    State("tabla_pedido", "data"),
    State("in_cantidad_simulaciones", "value"),
    State("in_semana_particular", "value"),
    State("in_semilla", "value"),
    prevent_initial_call=True
)
def arrancar_la_simulacion(n_clicks, inventario, stock, c_sobrepaso, c_mantenimiento, c_pedido, filas_demanda,
                           filas_pedido, simulaciones, semana, semilla):

    # Validación de datos

    if None in [inventario, stock, c_sobrepaso, c_mantenimiento, c_pedido, simulaciones, semana]:
        return True, no_update

    suma_probabilidades_demanda = round(sum([fila["probabilidad"] for fila in filas_demanda]), 2)
    if suma_probabilidades_demanda != 1:
        return True, no_update

    suma_probabilidades_pedido = round(sum([fila["probabilidad"] for fila in filas_pedido]), 2)
    if suma_probabilidades_pedido != 1:
        return True, no_update

    # Procesamiento de entradas

    consumos_demanda = [fila["consumo"] for fila in filas_demanda]
    probabilidades_demanda = [fila["probabilidad"] for fila in filas_demanda]
    tamanios_pedido = [fila["pedido"] for fila in filas_pedido]
    probabilidades_pedido = [fila["probabilidad"] for fila in filas_pedido]

    # Cálculo y generación de resultados

    simulador = MonteCarloLavarropa(semilla)
    simulador.establecer_tabla_demanda(consumos_demanda, probabilidades_demanda)
    simulador.establecer_tabla_pedido(tamanios_pedido, probabilidades_pedido)
    simulador.establecer_parametros_negocio(c_pedido, c_mantenimiento, c_sobrepaso, stock, inventario)
    filas_guardadas, fila_actual, fila_anterior = simulador.simular(simulaciones, semana)

    datos_filas_guardadas = {
        "Semana": [fila[0] for fila in filas_guardadas],
        "Random 1": [round(fila[1], 2) for fila in filas_guardadas],
        "Consumo semanal (m²)": ["{:,.0f}".format(fila[2]) for fila in filas_guardadas],
        "Random 2": [round(fila[3], 2) for fila in filas_guardadas],
        "Tamaño de pedido (m²)": ["{:,.0f}".format(fila[4]) for fila in filas_guardadas],
        "Stock": ["{:,.0f}".format(fila[5]) for fila in filas_guardadas],
        "Costo de pedido": ["${:,.0f}".format(fila[6]) for fila in filas_guardadas],
        "Costo de mantenimiento": ["${:,.0f}".format(fila[7]) for fila in filas_guardadas],
        "Costo de sobrepaso": ["${:,.0f}".format(fila[8]) for fila in filas_guardadas],
        "Costo total": ["${:,.0f}".format(fila[9]) for fila in filas_guardadas],
        "Costo total acumulado": ["${:,.0f}".format(fila[10]) for fila in filas_guardadas],
    }

    tabla_filas = crear_tabla(datos_filas_guardadas)

    return False, tabla_filas
