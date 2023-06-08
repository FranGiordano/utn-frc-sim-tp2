import dash_bootstrap_components as dbc
from dash import html, dcc
from dash import dash_table


def crear_resultados_simulacion(filas):

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
            {"name": "Pasajeros anticipada que no entraron a ventanilla", "id": "ctd_antic_no_ventanilla"},
            {"name": "Pasajeros atendidos en máquina", "id": "ctd_atendidos_maquina"},
            {"name": "Pasajeros interrumpidos en máquina", "id": "ctd_interrumpidos_maquina"},
            {"name": "Tiempo ventanilla inmediata 1 en estado libre", "id": "acum_inmed1_libre"},
            {"name": "Tiempo ventanilla inmediata 1 en estado ocupado", "id": "acum_inmed1_ocupado"},
            {"name": "Porcentaje ocupación ventanilla inmediata 1", "id": "pct_ocup_inmed1"},
            {"name": "Porcentaje pasajeros anticipada que perdieron el tren", "id": "pct_perdieron_tren"},
            {"name": "Porcentaje pasajeros interrumpidos al usar la máquina", "id": "pct_interrumpidos_maq"}
        ],

        data=[
            {
                "iteracion": f"{i[0]:,.0f}",
                "reloj": f"{i[1]:.4f}" if i[1] is not None else "",
                "evento": i[2],
                "random1": f"{i[3]:.2f}" if i[3] is not None else "",
                "tiempo_entre_llegada_pasajero": f"{i[4]:.4f}" if i[4] is not None else "",
                "proxima_llegada_pasajero": f"{i[5]:.4f}" if i[5] is not None else "",
                "random2": f"{i[6]:.2f}" if i[6] is not None else "",
                "proximo_tipo_atencion": i[7],
                "tiempo_entre_llegada_mecanico": f"{i[8]:.4f}" if i[8] is not None else "",
                "proxima_llegada_mecanico": f"{i[9]:.4f}" if i[9] is not None else "",
                "random3": f"{i[10]:.2f}" if i[10] is not None else "",
                "tiempo_fin_atencion_inmediata": f"{i[11]:.4f}" if i[11] is not None else "",
                "estado_inmediata_1": i[12],
                "proximo_fin_atencion_inmed_1": f"{i[13]:.4f}" if i[13] is not None else "",
                "cliente_atendido_inmed_1": i[14],
                "estado_inmediata_2": i[15],
                "proximo_fin_atencion_inmed_2": f"{i[16]:.4f}" if i[16] is not None else "",
                "cliente_atendido_inmed_2": i[17],
                "estado_anticipada": i[18],
                "random4": f"{i[19]:.2f}" if i[19] is not None else "",
                "tiempo_fin_atencion_anticipada": f"{i[20]:.4f}" if i[20] is not None else "",
                "proximo_fin_atencion_anticipada": f"{i[21]:.4f}" if i[21] is not None else "",
                "cliente_atendido_anticipada": i[53],
                "estado_auxiliar": i[22],
                "random5": f"{i[23]:.2f}" if i[23] is not None else "",
                "tiempo_fin_atencion_auxiliar": f"{i[24]:.4f}" if i[24] is not None else "",
                "proximo_fin_atencion_auxiliar": f"{i[25]:.4f}" if i[25] is not None else "",
                "cliente_atendido_auxiliar": i[52],
                "estado_maquina": i[26],
                "random6": f"{i[27]:.2f}" if i[27] is not None else "",
                "tiempo_fin_atencion_maquina": f"{i[28]:.4f}" if i[28] is not None else "",
                "proximo_fin_atencion_maquina": f"{i[29]:.4f}" if i[29] is not None else "",
                "cliente_atendido_maquina": i[54],
                "random7": f"{i[30]:.2f}" if i[30] is not None else "",
                "random8": f"{i[31]:.2f}" if i[31] is not None else "",
                "tiempo_fin_mantenimiento": f"{i[32]:.4f}" if i[32] is not None else "",
                "proximo_fin_mantenimiento": f"{i[33]:.4f}" if i[33] is not None else "",
                "proximo_fin_impaciencia": f"{i[34]:.4f}" if i[34] is not None else "",
                "proximo_inicio_hora_critica": f"{i[35]:.4f}" if i[35] is not None else "",
                "proximo_inicio_hora_auxiliar": f"{i[36]:.4f}" if i[36] is not None else "",
                "proximo_inicio_hora_moderada": f"{i[37]:.4f}" if i[37] is not None else "",
                "proximo_fin_hora_moderada": f"{i[38]:.4f}" if i[38] is not None else "",
                "cola_salida_inmediata": i[39],
                "cola_salida_anticipada": i[40],
                "cola_maquina": i[41],
                "ctd_antic_ventanilla": i[42],
                "ctd_antic_no_ventanilla": i[43],
                "ctd_atendidos_maquina": i[44],
                "ctd_interrumpidos_maquina": i[45],
                "acum_inmed1_libre": f"{i[46]:.4f}" if i[46] is not None else "",
                "acum_inmed1_ocupado": f"{i[47]:.4f}" if i[47] is not None else "",
                "pct_ocup_inmed1": f"{i[48] * 100:.2f}%" if i[48] is not None else "",
                "pct_perdieron_tren": f"{i[49] * 100:.2f}%" if i[49] is not None else "",
                "pct_interrumpidos_maq": f"{i[50] * 100:.2f}%" if i[50] is not None else ""
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
                "backgroundColor": "#84B6F4",
            },
            {
                "if": {
                    "column_id": ["tiempo_entre_llegada_mecanico",
                                  "proxima_llegada_mecanico"]
                },
                "backgroundColor": "#FDCAE1",
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
                "backgroundColor": "#77DD77",
            },
            {
                "if": {
                    "column_id": ["estado_anticipada",
                                  "random4",
                                  "tiempo_fin_atencion_anticipada",
                                  "proximo_fin_atencion_anticipada",
                                  "cliente_atendido_anticipada"]
                },
                "backgroundColor": "#FFDA9E",
            },
            {
                "if": {
                    "column_id": ["estado_auxiliar",
                                  "random5",
                                  "tiempo_fin_atencion_auxiliar",
                                  "proximo_fin_atencion_auxiliar",
                                  "cliente_atendido_auxiliar"]
                },
                "backgroundColor": "#C0A0C3",
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
                "backgroundColor": "#FDFD96",
            },
            {
                "if": {
                    "column_id": ["proximo_fin_impaciencia",
                                  "proximo_inicio_hora_critica",
                                  "proximo_inicio_hora_auxiliar",
                                  "proximo_inicio_hora_moderada",
                                  "proximo_fin_hora_moderada"]
                },
                "backgroundColor": "#B8E4FF",
            },
            {
                "if": {
                    "column_id": ["cola_salida_inmediata",
                                  "cola_salida_anticipada",
                                  "cola_maquina"]
                },
                "backgroundColor": "#EAFFC2",
            },
            {
                "if": {
                    "column_id": ["ctd_antic_ventanilla",
                                  "ctd_antic_no_ventanilla",
                                  "ctd_atendidos_maquina",
                                  "ctd_interrumpidos_maquina"]
                },
                "backgroundColor": "#9B9B9B",
            },
            {
                "if": {
                    "column_id": ["acum_inmed1_libre",
                                  "acum_inmed1_ocupado"]
                },
                "backgroundColor": "#C5D084",
            },
            {
                "if": {
                    "column_id": ["pct_ocup_inmed1",
                                  "pct_perdieron_tren",
                                  "pct_interrumpidos_maq"]
                },
                "backgroundColor": "#EB9CFF",
            }
        ],

        merge_duplicate_headers=True,

        page_size=15,

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

    resultados = html.Div([
        dbc.Container(
            dbc.Card(dbc.CardBody(
                "Añadir referencias de colores acá"
            ), className="mt-3")
        ),
        html.Div(tabla, className="mt-3 mx-5")
    ])

    return resultados


