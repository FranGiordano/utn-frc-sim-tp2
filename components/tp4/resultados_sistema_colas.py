import dash_bootstrap_components as dbc
from dash import html, dcc
from dash import dash_table


def crear_resultados_simulacion(filas):

    tabla = dash_table.DataTable(

        columns=[
            {"name": ["", "Iteración"], "id": "iteracion"},
            {"name": ["", "Reloj"], "id": "reloj"},
            {"name": ["", "Evento"], "id": "evento"},
            {"name": ["Llegada pasajero", "Random 1"], "id": "random1"},
            {"name": ["Llegada pasajero", "Tiempo entre llegadas"], "id": "tiempo_entre_llegada_pasajero"},
            {"name": ["Llegada pasajero", "Próxima llegada"], "id": "proxima_llegada_pasajero"},
            {"name": ["Llegada pasajero", "Random 2"], "id": "random2"},
            {"name": ["Llegada pasajero", "Próximo tipo de atención"], "id": "proximo_tipo_atencion"},
            {"name": ["Llegada mecánico", "Tiempo entre llegadas"], "id": "tiempo_entre_llegada_mecanico"},
            {"name": ["Llegada mecánico", "Próxima llegada"], "id": "proxima_llegada_mecanico"},
            {"name": ["Ventanilla salida inmediata 1 y 2", "Random 1"], "id": "random3"},
            {"name": ["Ventanilla salida inmediata 1 y 2", "Tiempo fin atención"],
             "id": "tiempo_fin_atencion_inmediata"},
            {"name": ["Ventanilla salida inmediata 1 y 2", "Estado 1"], "id": "estado_inmediata_1"},
            {"name": ["Ventanilla salida inmediata 1 y 2", "Próximo fin atención 1"],
             "id": "proximo_fin_atencion_inmed_1"},
            {"name": ["Ventanilla salida inmediata 1 y 2", "Cliente siendo atendido 1"],
             "id": "cliente_atendido_inmed_1"},
            {"name": ["Ventanilla salida inmediata 1 y 2", "Estado 2"], "id": "estado_inmediata_2"},
            {"name": ["Ventanilla salida inmediata 1 y 2", "Próximo fin atención 2"],
             "id": "proximo_fin_atencion_inmed_2"},
            {"name": ["Ventanilla salida inmediata 1 y 2", "Cliente siendo atendido 2"],
             "id": "cliente_atendido_inmed_2"},
            {"name": ["Ventanilla salida anticipada", "Estado"], "id": "estado_anticipada"},
            {"name": ["Ventanilla salida anticipada", "Random"], "id": "random4"},
            {"name": ["Ventanilla salida anticipada", "Tiempo fin atención"], "id": "tiempo_fin_atencion_anticipada"},
            {"name": ["Ventanilla salida anticipada", "Próximo fin atención"], "id": "proximo_fin_atencion_anticipada"},
            {"name": ["Ventanilla salida anticipada", "Cliente siendo atendido"], "id": "cliente_atendido_anticipada"},
            {"name": ["Ventanilla auxiliar", "Estado"], "id": "estado_auxiliar"},
            {"name": ["Ventanilla auxiliar", "Random"], "id": "random5"},
            {"name": ["Ventanilla auxiliar", "Tiempo fin atención"], "id": "tiempo_fin_atencion_auxiliar"},
            {"name": ["Ventanilla auxiliar", "Próximo fin atención"], "id": "proximo_fin_atencion_auxiliar"},
            {"name": ["Ventanilla auxiliar", "Cliente siendo atendido"], "id": "cliente_atendido_auxiliar"},
            {"name": ["Máquina", "Estado"], "id": "estado_maquina"},
            {"name": ["Máquina", "Random 1"], "id": "random6"},
            {"name": ["Máquina", "Tiempo fin atención"], "id": "tiempo_fin_atencion_maquina"},
            {"name": ["Máquina", "Próximo fin atención"], "id": "proximo_fin_atencion_maquina"},
            {"name": ["Máquina", "Cliente siendo atendido"], "id": "cliente_atendido_maquina"},
            {"name": ["Máquina", "Random 2"], "id": "random7"},
            {"name": ["Máquina", "Random 3"], "id": "random8"},
            {"name": ["Máquina", "Tiempo fin mantenimiento"], "id": "tiempo_fin_mantenimiento"},
            {"name": ["Máquina", "Próximo fin mantenimiento"], "id": "proximo_fin_mantenimiento"},
            {"name": ["Otros eventos", "Próximo fin impaciencia"], "id": "proximo_fin_impaciencia"},
            {"name": ["Otros eventos", "Próximo inicio hora crítica"], "id": "proximo_inicio_hora_critica"},
            {"name": ["Otros eventos", "Próximo inicio hora ventanilla auxiliar"],
             "id": "proximo_inicio_hora_auxiliar"},
            {"name": ["Otros eventos", "Próximo inicio hora moderada"], "id": "proximo_inicio_hora_moderada"},
            {"name": ["Otros eventos", "Próximo fin hora moderada"], "id": "proximo_fin_hora_moderada"},
            {"name": ["Colas", "Cola salida inmediata"], "id": "cola_salida_inmediata"},
            {"name": ["Colas", "Cola salida anticipada"], "id": "cola_salida_anticipada"},
            {"name": ["Colas", "Cola máquina"], "id": "cola_maquina"},
            {"name": ["Contadores", "Pasajeros anticipada que entraron a ventanilla"], "id": "ctd_antic_ventanilla"},
            {"name": ["Contadores", "Pasajeros anticipada que no entraron a ventanilla"],
             "id": "ctd_antic_no_ventanilla"},
            {"name": ["Contadores", "Pasajeros atendidos en máquina"], "id": "ctd_atendidos_maquina"},
            {"name": ["Contadores", "Pasajeros interrumpidos en máquina"], "id": "ctd_interrumpidos_maquina"},
            {"name": ["Acumuladores", "Tiempo ventanilla inmediata 1 en estado libre"], "id": "acum_inmed1_libre"},
            {"name": ["Acumuladores", "Tiempo ventanilla inmediata 1 en estado ocupado"], "id": "acum_inmed1_ocupado"},
            {"name": ["Métricas", "Porcentaje ocupación ventanilla inmediata 1"], "id": "pct_ocup_inmed1"},
            {"name": ["Métricas", "Porcentaje pasajeros anticipada que perdieron el tren"], "id": "pct_perdieron_tren"},
            {"name": ["Métricas", "Porcentaje pasajeros interrumpidos al usar la máquina"],
             "id": "pct_interrumpidos_maq"},
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
                "pct_ocup_inmed1": f"{i[48] * 100:.4f}%" if i[48] is not None else "",
                "pct_perdieron_tren": f"{i[49] * 100:.2f}%" if i[49] is not None else "",
                "pct_interrumpidos_maq": f"{i[50] * 100:.2f}%" if i[50] is not None else ""
            }
            for i in filas
        ],

        merge_duplicate_headers=True,

        page_size=15,

        # fixed_columns={'headers': True, 'data': 1},
        style_table={
            'minWidth': '100%',
            "overflowX": "auto"
        },

        style_header={
            "text-align": "center",

        },

        style_cell={
            "textAlign": "left"
        },

        style_data={
        }


    )

    return tabla


