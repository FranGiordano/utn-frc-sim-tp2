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
from soporte.simulacion import generar_simulacion

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


# Callback para añadir una fila a la tabla demanda
@callback(
    Output("tabla_demanda", "data"),
    Input("btn_crear_fila_demanda", "n_clicks"),
    State("in_demanda_consumo", "value"),
    State("in_demanda_probabilidad", "value"),
    State("tabla_demanda", "data"),
    prevent_initial_call=True
)
def crear_fila_tabla_demanda(n_clicks, consumo, probabilidad, filas):

    if None in [consumo, probabilidad]:
        return no_update

    # Busca si el consumo ya se encuentra en la tabla y suma la probabilidad, en caso contrario crea una fila
    for fila in filas:
        if fila["consumo"] == consumo:
            fila["probabilidad"] = round(fila["probabilidad"] + probabilidad, 2)
            break
    else:
        filas.append({"consumo": consumo, "probabilidad": probabilidad})

    return filas


# Callback para actualizar alertas correspondientes al eliminar o añadir fila de tabla demanda
# Tener en cuenta que este callback se ejecuta siempre que se ejecute la función crear_fila_tabla_demanda
@callback(
    Output("alerta_demanda", "children"),
    Output("alerta_demanda", "color"),
    Input("tabla_demanda", "data"),
    prevent_initial_call=True
)
def actualizar_alertas_tabla_demanda(filas):
    suma_probabilidades = round(sum([fila["probabilidad"] for fila in filas]), 2)
    color = "success" if suma_probabilidades == 1 else "warning"
    return f"Probabilidad acumulada: {suma_probabilidades}", color


# Callback para añadir una fila a la tabla pedido
@callback(
    Output("tabla_pedido", "data"),
    Input("btn_crear_fila_pedido", "n_clicks"),
    State("in_pedido_tamanio", "value"),
    State("in_pedido_probabilidad", "value"),
    State("tabla_pedido", "data"),
    prevent_initial_call=True
)
def crear_fila_tabla_pedido(n_clicks, tamanio, probabilidad, filas):

    if None in [tamanio, probabilidad]:
        return no_update

    # Busca si el pedido ya se encuentra en la tabla y suma la probabilidad, en caso contrario crea una fila
    for fila in filas:
        if fila["pedido"] == tamanio:
            fila["probabilidad"] = round(fila["probabilidad"] + probabilidad, 2)
            break
    else:
        filas.append({"pedido": tamanio, "probabilidad": probabilidad})

    return filas


# Callback para actualizar alertas correspondientes al eliminar o añadir fila de tabla pedido
# Tener en cuenta que este callback se ejecuta siempre que se ejecute la función crear_fila_tabla_pedido
@callback(
    Output("alerta_pedido", "children"),
    Output("alerta_pedido", "color"),
    Input("tabla_pedido", "data"),
    prevent_initial_call=True
)
def actualizar_alertas_tabla_pedido(filas):
    suma_probabilidades = round(sum([fila["probabilidad"] for fila in filas]), 2)
    color = "success" if suma_probabilidades == 1 else "warning"
    return f"Probabilidad acumulada: {suma_probabilidades}", color


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

    filas_guardadas = generar_simulacion(simulaciones, semana, semilla, c_pedido, c_mantenimiento, c_sobrepaso, stock,
                                         inventario, consumos_demanda, probabilidades_demanda, tamanios_pedido,
                                         probabilidades_pedido)

    datos_tabla = {
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
        "Promedio de costo total": ["${:,.0f}".format(fila[11]) for fila in filas_guardadas],
        "Diferencia de stock": ["{:,.0f}".format(fila[12]) for fila in filas_guardadas],
        "Diferencia de stock acumulado": ["{:,.0f}".format(fila[13]) for fila in filas_guardadas],
        "Promedio de crecimiento semanal de stock": ["{:,.0f}".format(fila[14]) for fila in filas_guardadas],
        "Cantidad de semanas que debemos pedidos": ["{:,.0f}".format(fila[15]) for fila in filas_guardadas],
        "Porcentaje de semanas que debemos pedidos": ["{:.0f}%".format(fila[16]*100) for fila in filas_guardadas],
        "Semana donde el stock supera la cap. máx.": ["{:,.0f}".format(fila[17]) for fila in filas_guardadas],
    }

    tabla = crear_tabla(datos_tabla)

    return False, tabla
