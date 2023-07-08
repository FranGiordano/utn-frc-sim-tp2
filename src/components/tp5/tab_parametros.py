from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc


def crear_tab_parametros():

    tab = dbc.Tabs([

        # Simulación
        dbc.Tab(dbc.Card(dbc.CardBody([

            dbc.Row([

                dbc.Col(dbc.FormFloating([
                    dbc.Input(id="in_cantidad_iteraciones_5", placeholder="Cantidad de iteraciones", type="number", min=1,
                              value=10000, required=True, max=1000000, step=1),
                    dbc.Label("Cantidad de simulaciones")
                ])),

                dbc.Col(dbc.FormFloating([
                    dbc.Input(id="in_iteracion_a_mostrar_5", placeholder="Iteración inicial a mostrar en tabla",
                              type="number", min=1, value=1000, required=True, max=1000000, step=1),
                    dbc.Label("Cantidad iteraciones a mostrar en tabla")
                ])),

                dbc.Col(dbc.FormFloating([
                    dbc.Input(id="in_iteracion_a_grabar_5", placeholder="Iteración inicial a mostrar en tabla",
                              type="number", min=1, value=1, required=True, max=1000000, step=1),
                    dbc.Label("Iteración inicial a mostrar en tabla")
                ])),

                dbc.Col(dbc.FormFloating([
                    dbc.Input(id="in_semilla_simulacion_5", placeholder="Semilla de simulación",
                              type="number", min=0, value=1, required=False, step=1),
                    dbc.Label("Semilla de simulación")
                ])),

                dbc.Col(
                    dbc.Button("Generar simulación", id="btn_simular_5", color="primary"),
                    class_name="col-auto align-self-end")
            ])

        ]), className="mt-3"), label="Simulación"),

        # Llegada de pasajeros
        dbc.Tab(dbc.Card(dbc.CardBody([

            dbc.Row([

                dbc.Col(dbc.FormFloating([
                    dbc.Input(id="in_a_lleg_pasaj_mod_5", placeholder="Límite inferior llegada pasajero moderada",
                              type="number", required=True, value=0.0063, step=0.00001),
                    dbc.Label("Límite inferior llegada pasajero moderada")
                ])),

                dbc.Col(dbc.FormFloating([
                    dbc.Input(id="in_b_lleg_pasaj_mod_5", placeholder="Límite superior llegada pasajero moderada",
                              type="number", required=True, value=0.0292, step=0.00001),
                    dbc.Label("Límite superior llegada pasajero moderada")
                ])),

                dbc.Col(dbc.FormFloating([
                    dbc.Input(id="in_media_lleg_pasaj_crit_5", placeholder="Media llegada pasajero crítica",
                              type="number", required=True, value=0.0106, step=0.00001),
                    dbc.Label("Media llegada pasajero crítica")
                ]))
            ])

        ]), className="mt-3"), label="Llegada de pasajeros"),

        # Tiempos de atención
        dbc.Tab(dbc.Card(dbc.CardBody([

            dbc.Row([

                dbc.Col(dbc.FormFloating([
                    dbc.Input(id="in_lambda_cercania_5", placeholder="Lambda atención cercanía",
                              type="number", required=True, value=80, step=0.00001),
                    dbc.Label("Lambda atención cercanía")
                ])),

                dbc.Col(dbc.FormFloating([
                    dbc.Input(id="in_lambda_interprovincial_5", placeholder="Lambda atención interprovincial",
                              type="number", required=True, value=40, step=0.00001),
                    dbc.Label("Lambda atención interprovincial")
                ])),

                dbc.Col(dbc.FormFloating([
                    dbc.Input(id="in_lambda_anticipada_5", placeholder="Lambda atención anticipada",
                              type="number", required=True, value=25, step=0.00001),
                    dbc.Label("Lambda atención anticipada")
                ])),

                dbc.Col(dbc.FormFloating([
                    dbc.Input(id="in_lambda_maquina_5", placeholder="Lambda atención máquina",
                              type="number", required=True, value=30, step=0.00001),
                    dbc.Label("Lambda atención máquina")
                ]))
            ])

        ]), className="mt-3"), label="Tiempos de atención"),

        # Otros parámetros
        dbc.Tab(dbc.Card(dbc.CardBody([

            dbc.Row([

                dbc.Col(dbc.FormFloating([
                    dbc.Input(id="in_cte_impaciente_5", placeholder="Constante tiempo impaciencia",
                              type="number", required=True, value=0.33, step=0.00001),
                    dbc.Label("Constante tiempo impaciencia")
                ])),

                dbc.Col(dbc.FormFloating([
                    dbc.Input(id="in_inicio_auxiliar_5", placeholder="Hora inicio ventanilla auxiliar",
                              type="number", required=True, min=6.00001, max=14.9999, value=12, step=0.00001),
                    dbc.Label("Hora inicio ventanilla auxiliar")
                ]))

            ])

        ]), className="mt-3"), label="Otros parámetros"),

    ])

    return tab
