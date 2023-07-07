import dash_bootstrap_components as dbc
from dash import html, dcc
from dash import dash_table
from datetime import timedelta


def crear_resultados_simulacion(filas):

    paleta_de_colores = {
        "Llegada de pasajero": "#84B6F4",
        "Llegada de mecánico": "#FDCAE1",
        "Ventanilla inmediata 1 y 2": "#77DD77",
        "Ventanilla anticipada": "#FFDA9E",
        "Ventanilla auxiliar": "#C0A0C3",
        "Máquina": "#FDFD96",
        "Otros eventos": "#B8E4FF",
        "Colas": "#EAFFC2",
        "Contadores": "#9B9B9B",
        "Acumuladores": "#C5D084",
        "Métricas": "#EB9CFF"
    }

    tabla = dash_table.DataTable(

        columns=[
            {"name": "N", "id": "iteracion"},
            {"name": "Reloj", "id": "reloj"},
            {"name": "Evento", "id": "evento"},
            {"name": "Random 1", "id": "random1"},
            {"name": "Tiempo entre llegadas", "id": "tiempo_entre_llegada_pasajero"},
            {"name": "Próxima llegada", "id": "proxima_llegada_pasajero"},
            {"name": "Random 2", "id": "random2"},
            {"name": "Próximo tipo de atención", "id": "proximo_tipo_atencion"},
            {"name": "Tiempo entre llegadas", "id": "tiempo_entre_llegada_mecanico"},
            {"name": "Próxima llegada", "id": "proxima_llegada_mecanico"},
            {"name": "Random 1", "id": "random3"},
            {"name": "Tiempo fin atención", "id": "tiempo_fin_atencion_inmediata"},
            {"name": "Estado 1", "id": "estado_inmediata_1"},
            {"name": "Próximo fin atención 1", "id": "proximo_fin_atencion_inmed_1"},
            {"name": "Cliente siendo atendido 1", "id": "cliente_atendido_inmed_1"},
            {"name": "Estado 2", "id": "estado_inmediata_2"},
            {"name": "Próximo fin atención 2", "id": "proximo_fin_atencion_inmed_2"},
            {"name": "Cliente siendo atendido 2", "id": "cliente_atendido_inmed_2"},
            {"name": "Estado", "id": "estado_anticipada"},
            {"name": "Random", "id": "random4"},
            {"name": "Tiempo fin atención", "id": "tiempo_fin_atencion_anticipada"},
            {"name": "Próximo fin atención", "id": "proximo_fin_atencion_anticipada"},
            {"name": "Cliente siendo atendido", "id": "cliente_atendido_anticipada"},
            {"name": "Estado", "id": "estado_auxiliar"},
            {"name": "Random", "id": "random5"},
            {"name": "Tiempo fin atención", "id": "tiempo_fin_atencion_auxiliar"},
            {"name": "Próximo fin atención", "id": "proximo_fin_atencion_auxiliar"},
            {"name": "Cliente siendo atendido", "id": "cliente_atendido_auxiliar"},
            {"name": "Estado", "id": "estado_maquina"},
            {"name": "Random 1", "id": "random6"},
            {"name": "Tiempo fin atención", "id": "tiempo_fin_atencion_maquina"},
            {"name": "Próximo fin atención", "id": "proximo_fin_atencion_maquina"},
            {"name": "Cliente siendo atendido", "id": "cliente_atendido_maquina"},
            {"name": "Random 2", "id": "random7"},
            {"name": "Random 3", "id": "random8"},
            {"name": "Tiempo fin mantenimiento", "id": "tiempo_fin_mantenimiento"},
            {"name": "Próximo fin mantenimiento", "id": "proximo_fin_mantenimiento"},
            {"name": "Próximo fin impaciencia", "id": "proximo_fin_impaciencia"},
            {"name": "Próximo inicio hora crítica", "id": "proximo_inicio_hora_critica"},
            {"name": "Próximo inicio hora ventanilla auxiliar", "id": "proximo_inicio_hora_auxiliar"},
            {"name": "Próximo inicio hora moderada", "id": "proximo_inicio_hora_moderada"},
            {"name": "Próximo fin hora moderada", "id": "proximo_fin_hora_moderada"},
            {"name": "Cola salida inmediata", "id": "cola_salida_inmediata"},
            {"name": "Cola salida anticipada", "id": "cola_salida_anticipada"},
            {"name": "Cola máquina", "id": "cola_maquina"},
            {"name": "Pasajeros anticipada que entraron a ventanilla", "id": "ctd_antic_ventanilla"},
            {"name": "Pasajeros anticipada que perdieron el tren", "id": "ctd_antic_no_ventanilla"},
            {"name": "Pasajeros atendidos en máquina", "id": "ctd_atendidos_maquina"},
            {"name": "Pasajeros interrumpidos en máquina", "id": "ctd_interrumpidos_maquina"},
            {"name": "Tiempo ventanilla inmediata 1 en estado libre", "id": "acum_inmed1_libre"},
            {"name": "Tiempo ventanilla inmediata 1 en estado ocupado", "id": "acum_inmed1_ocupado"},
            {"name": "Porcentaje ocupación ventanilla inmediata 1", "id": "pct_ocup_inmed1"},
            {"name": "Porcentaje pasajeros anticipada que perdieron el tren", "id": "pct_perdieron_tren"},
            {"name": "Porcentaje pasajeros interrumpidos al usar la máquina", "id": "pct_interrumpidos_maq"},

            # valores agregados para tp5
            {"name": "Cont clientes que llegan", "id": "cont_clientes_llegan"},
            {"name": "RND valor B", "id": "rnd_valor_b"},
            {"name": "Demora proxima llegada", "id": "dem_prox_llegada"},
            {"name": "Tiempo proxima llegada", "id": "tiemp_prox_llegada"},
            {"name": "RND tipo llegada", "id": "RND_tipo_llegada"},
            {"name": "Tipo llegada", "id": "tipo_llegada"},
            {"name": "Tiempo detenido el servicio V1", "id": "tiempo_detenido_v1"},
            {"name": "Tiempo servicio V1 normalidad", "id": "tiempo_normalidad_v1"},
            {"name": "Tiempo remanente cliente interrumpido", "id": "Tiempo_remanente"},
            {"name": "Tiempo detenida la llegada cliente", "id": "tiempo_detenido_cliente"},
            {"name": "Llegada cliente normalidad", "id": "tiempo_normalidad_cliente"},
        ],

        data=[
            {
                "iteracion": f"{i[0]:,.0f}",
                "reloj": str_reloj(i[1]),
                "evento": i[2],
                "random1": f"{i[3]:.2f}" if i[3] is not None else "",
                "tiempo_entre_llegada_pasajero": str_reloj(i[4]),
                "proxima_llegada_pasajero": str_reloj(i[5]),
                "random2": f"{i[6]:.2f}" if i[6] is not None else "",
                "proximo_tipo_atencion": i[7],
                "tiempo_entre_llegada_mecanico": str_reloj(i[8]),
                "proxima_llegada_mecanico": str_reloj(i[9]),
                "random3": f"{i[10]:.2f}" if i[10] is not None else "",
                "tiempo_fin_atencion_inmediata": str_reloj(i[11]),
                "estado_inmediata_1": i[12],
                "proximo_fin_atencion_inmed_1": str_reloj(i[13]),
                "cliente_atendido_inmed_1": i[14],
                "estado_inmediata_2": i[15],
                "proximo_fin_atencion_inmed_2": str_reloj(i[16]),
                "cliente_atendido_inmed_2": i[17],
                "estado_anticipada": i[18],
                "random4": f"{i[19]:.2f}" if i[19] is not None else "",
                "tiempo_fin_atencion_anticipada": str_reloj(i[20]),
                "proximo_fin_atencion_anticipada": str_reloj(i[21]),
                "cliente_atendido_anticipada": i[53],
                "estado_auxiliar": i[22],
                "random5": f"{i[23]:.2f}" if i[23] is not None else "",
                "tiempo_fin_atencion_auxiliar": str_reloj(i[24]),
                "proximo_fin_atencion_auxiliar": str_reloj(i[25]),
                "cliente_atendido_auxiliar": i[52],
                "estado_maquina": i[26],
                "random6": f"{i[27]:.2f}" if i[27] is not None else "",
                "tiempo_fin_atencion_maquina": str_reloj(i[28]),
                "proximo_fin_atencion_maquina": str_reloj(i[29]),
                "cliente_atendido_maquina": i[54],
                "random7": f"{i[30]:.2f}" if i[30] is not None else "",
                "random8": f"{i[31]:.2f}" if i[31] is not None else "",
                "tiempo_fin_mantenimiento": str_reloj(i[32]),
                "proximo_fin_mantenimiento": str_reloj(i[33]),
                "proximo_fin_impaciencia": str_reloj(i[34]),
                "proximo_inicio_hora_critica": str_reloj(i[35]),
                "proximo_inicio_hora_auxiliar": str_reloj(i[36]),
                "proximo_inicio_hora_moderada": str_reloj(i[37]),
                "proximo_fin_hora_moderada": str_reloj(i[38]),
                "cola_salida_inmediata": i[39],
                "cola_salida_anticipada": i[40],
                "cola_maquina": i[41],
                "ctd_antic_ventanilla": i[42],
                "ctd_antic_no_ventanilla": i[43],
                "ctd_atendidos_maquina": i[44],
                "ctd_interrumpidos_maquina": i[45],
                "acum_inmed1_libre": str_reloj(i[46]),
                "acum_inmed1_ocupado": str_reloj(i[47]),
                "pct_ocup_inmed1": f"{i[48] * 100:.2f}%" if i[48] is not None else "",
                "pct_perdieron_tren": f"{i[49] * 100:.2f}%" if i[49] is not None else "",
                "pct_interrumpidos_maq": f"{i[50] * 100:.2f}%" if i[50] is not None else "",


                # valores agregados para tp5
                "cont_clientes_llegan": f"{i[55]}" if i[55] is not None else "0",
                "rnd_valor_b": i[65],
                "dem_prox_llegada": str_reloj(i[56]),
                "tiemp_prox_llegada": str_reloj(i[57]),
                "RND_tipo_llegada": i[58],
                "tipo_llegada": i[59],
                "tiempo_detenido_v1": str_reloj(i[60]),
                "tiempo_normalidad_v1": str_reloj(i[61]),
                "Tiempo_remanente": f"{str_reloj(i[62])}" if i[62] is not None else "",
                "tiempo_detenido_cliente": str_reloj(i[63]),
                "tiempo_normalidad_cliente": str_reloj(i[64]),

            }
            for i in filas
        ],

        style_cell_conditional=[
            {
                "if": {
                    "column_id": ["random1",
                                  "tiempo_entre_llegada_pasajero",
                                  "proxima_llegada_pasajero",
                                  "random2",
                                  "proximo_tipo_atencion"]
                },
                "backgroundColor": paleta_de_colores["Llegada de pasajero"],
            },
            {
                "if": {
                    "column_id": ["tiempo_entre_llegada_mecanico",
                                  "proxima_llegada_mecanico"]
                },
                "backgroundColor": paleta_de_colores["Llegada de mecánico"],
            },
            {
                "if": {
                    "column_id": ["random3",
                                  "tiempo_fin_atencion_inmediata",
                                  "estado_inmediata_1",
                                  "proximo_fin_atencion_inmed_1",
                                  "cliente_atendido_inmed_1",
                                  "estado_inmediata_2",
                                  "proximo_fin_atencion_inmed_2",
                                  "cliente_atendido_inmed_2"]
                },
                "backgroundColor": paleta_de_colores["Ventanilla inmediata 1 y 2"],
            },
            {
                "if": {
                    "column_id": ["estado_anticipada",
                                  "random4",
                                  "tiempo_fin_atencion_anticipada",
                                  "proximo_fin_atencion_anticipada",
                                  "cliente_atendido_anticipada"]
                },
                "backgroundColor": paleta_de_colores["Ventanilla anticipada"],
            },
            {
                "if": {
                    "column_id": ["estado_auxiliar",
                                  "random5",
                                  "tiempo_fin_atencion_auxiliar",
                                  "proximo_fin_atencion_auxiliar",
                                  "cliente_atendido_auxiliar"]
                },
                "backgroundColor": paleta_de_colores["Ventanilla auxiliar"],
            },
            {
                "if": {
                    "column_id": ["estado_maquina",
                                  "random6",
                                  "tiempo_fin_atencion_maquina",
                                  "proximo_fin_atencion_maquina",
                                  "cliente_atendido_maquina",
                                  "random7",
                                  "random8",
                                  "tiempo_fin_mantenimiento",
                                  "proximo_fin_mantenimiento"]
                },
                "backgroundColor": paleta_de_colores["Máquina"],
            },
            {
                "if": {
                    "column_id": ["proximo_fin_impaciencia",
                                  "proximo_inicio_hora_critica",
                                  "proximo_inicio_hora_auxiliar",
                                  "proximo_inicio_hora_moderada",
                                  "proximo_fin_hora_moderada"]
                },
                "backgroundColor": paleta_de_colores["Otros eventos"],
            },
            {
                "if": {
                    "column_id": ["cola_salida_inmediata",
                                  "cola_salida_anticipada",
                                  "cola_maquina"]
                },
                "backgroundColor": paleta_de_colores["Colas"],
            },
            {
                "if": {
                    "column_id": ["ctd_antic_ventanilla",
                                  "ctd_antic_no_ventanilla",
                                  "ctd_atendidos_maquina",
                                  "ctd_interrumpidos_maquina"]
                },
                "backgroundColor": paleta_de_colores["Contadores"],
            },
            {
                "if": {
                    "column_id": ["acum_inmed1_libre",
                                  "acum_inmed1_ocupado"]
                },
                "backgroundColor": paleta_de_colores["Acumuladores"],
            },
            {
                "if": {
                    "column_id": ["pct_ocup_inmed1",
                                  "pct_perdieron_tren",
                                  "pct_interrumpidos_maq"]
                },
                "backgroundColor": paleta_de_colores["Métricas"],
            }
        ],

        merge_duplicate_headers=True,

        page_size=15,

        cell_selectable=True,

        fixed_columns={'headers': True, 'data': 3},
        style_table={
            'minWidth': '100%'
        },

        style_header={
            "text-align": "center",
            "fontWeight": "bold",
            "border": "1px solid black"
        },

        style_cell={
            "textAlign": "left",
            "border": "1px solid black",
            'font-family': 'sans-serif',
            "whiteSpace": "normal",
            'height': "auto",
            #'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
        },
    )

    referencias = []
    nro_col_por_fila = 4
    for i, j in enumerate(paleta_de_colores):
        if i % nro_col_por_fila == 0:
            referencias.append(dbc.Row([]))
        referencias[-1].children.append(
            dbc.Col([
                html.I(className="bi bi-square-fill", style={"color": paleta_de_colores[j]}),
                f" {i+1}. {j}"
            ])
        )

    if len(referencias[-1].children) != nro_col_por_fila:
        n = nro_col_por_fila - len(referencias[-1].children)
        for i in range(n):
            referencias[-1].children.append(dbc.Col())

    resultados = html.Div([
        dbc.Container(
            dbc.Card(dbc.CardBody(
                referencias
            ), className="mt-3")
        ),
        html.Div(tabla, className="mt-3 mx-5")
    ])

    return resultados


def str_reloj(hora):
    if hora is None:
        return ""
    else:
        return str(timedelta(hours=hora) - timedelta(microseconds=timedelta(hours=hora).microseconds))
