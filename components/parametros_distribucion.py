import dash_bootstrap_components as dbc


def crear_parametros_distribucion() -> dbc.Row:
    """
    Genera una fila con los forms de parámetros y el botón de generar gráfico.

    :return: La fila con los forms de parámetros y el botón de generar gráfico.
    :rtype: dbc.Row
    """
    parametros = dbc.Row([

        dbc.Col(id="form-cantidad", children=[
            dbc.FormFloating([
                dbc.Input(id="in_cantidad_muestras", placeholder="Cantidad de muestras", type="number",
                          min=0, step=1, value=10000, required=True),
                dbc.Label("Cantidad de muestras"),
            ])]),

        dbc.Col(id='form-intervalos',
                children=[
                    dbc.FormFloating([
                        dbc.Input(id="in_intervalos",
                                  placeholder="Cantidad de intervalos",
                                  type="number", min=1, step=1,
                                  value=15, required=True),
                        dbc.Label("Cantidad de intervalos"),
                    ])]),

        dbc.Col(id="form-limite-inferior", children=[
            dbc.FormFloating([
                dbc.Input(id="in_limite_inferior", placeholder="Límite inferior", type="number",
                          value=-10, required=True, step=0.0001),
                dbc.Label("Límite inferior"),
            ])], style={"display": "none"}),

        dbc.Col(id="form-limite-superior", children=[
            dbc.FormFloating([
                dbc.Input(id="in_limite_superior", placeholder="Límite superior", type="number",
                          value=10, required=True, step=0.0001),
                dbc.Label("Límite superior"),
            ])], style={"display": "none"}),

        dbc.Col(id='form-media',
                children=[
                    dbc.FormFloating([
                        dbc.Input(id="in_media", placeholder="Media", type="number",
                                  value=0, required=True, step=0.0001),
                        dbc.Label("Media"),
                    ])], style={"display": "none"}),

        dbc.Col(id="form-desv", children=[
            dbc.FormFloating([
                dbc.Input(id="in_desviacion", placeholder="Desviación Estándar", type="number", min=0.0001,
                          value=1, required=True, step=0.0001),
                dbc.Label("Desviación Estándar"),
            ])], style={"display": "none"}),

        dbc.Col(id="form-lambda", children=[
            dbc.FormFloating([
                dbc.Input(id="in_lambda", placeholder="Lambda", type="number",
                          value=5, required=True, step=0.0001, min=0.0001),
                dbc.Label("Lambda"),
            ])], style={"display": "none"}),

        dbc.Col(dbc.Button("Generar distribución",
                           id="btn_cargar_grafico",
                           color="primary"),
                class_name="col-auto align-self-end")
    ])

    return parametros
