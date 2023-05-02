import dash_bootstrap_components as dbc


def crear_parametros_montecarlo_simulacion():

    parametros_simulacion = dbc.Row([
        dbc.Col(id="form-cantidad-simulaciones", children=[
            dbc.FormFloating([
                dbc.Input(id="in_cantidad_simulaciones", placeholder="Cantidad de simulaciones", type="number",
                          min=1, value=100000, required=True, step=1),
                dbc.Label("Cantidad de simulaciones"),
            ])]),

        dbc.Col(id="form-semana-particular", children=[
            dbc.FormFloating([
                dbc.Input(id="in_semana_particular", placeholder="Semana inicial a mostrar en tabla", type="number",
                          min=1, value=1, required=True, step=1),
                dbc.Label("Semana inicial a mostrar en tabla"),
            ])]),

        dbc.Col(id="form-semilla", children=[
            dbc.FormFloating([
                dbc.Input(id="in_semilla", placeholder="Semilla de random (-1 para aleatorio)", type="number",
                          min=-1, value=-1, required=True, step=1),
                dbc.Label("Semilla de random (-1 para aleatorio)"),
            ])]),

        dbc.Col(dbc.Button("Generar simulación",
                           id="btn_generar_simulacion",
                           color="primary"),
                class_name="col-auto align-self-end")
    ], className="mt-3")

    return parametros_simulacion
