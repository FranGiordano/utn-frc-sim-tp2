from dash import dcc
import dash_bootstrap_components as dbc

tipo_distribucion = dcc.RadioItems(options=['uniforme', 'normal', 'exponencial', 'poisson'],
                                   value='uniforme',
                                   id='controls-dist')

btn_generar_grafico = dbc.Col(dbc.Button("Generar distribución",
                                         id="btn_cargar_grafico",
                                         color="primary"),
                                         class_name="col-auto align-self-end")

txt_box_cantidad = dbc.Col(id="form-cantidad", children=[
    dbc.FormFloating([
        dbc.Input(id="in_cantidad_muestras", placeholder="Cantidad de muestras", type="number", max=1000000,
                  min=0, step=1, value=10000, required=True),
        dbc.Label("Cantidad de muestras"),
    ])])

txt_box_limite_inferior = dbc.Col(id="form-limite-inferior", children=[
    dbc.FormFloating([
        dbc.Input(id="in_limite_inferior", placeholder="Límite inferior", type="number",
                  value=-10, required=True, step=0.0001),
        dbc.Label("Límite inferior"),
    ])])

txt_box_limite_superior = dbc.Col(id="form-limite-superior", children=[
    dbc.FormFloating([
        dbc.Input(id="in_limite_superior", placeholder="Límite superior", type="number",
                  value=10, required=True, step=0.0001),
        dbc.Label("Límite superior"),
    ])])

txt_box_cantidad_intervalos = dbc.Col(id='form-intervalos',
                                      children=[
                                          dbc.FormFloating([
                                              dbc.Input(id="in_intervalos",
                                                        placeholder="Cantidad de intervalos",
                                                        type="number", min=1, step=1,
                                                        value=15, required=True, max=225),
                                              dbc.Label("Cantidad de intervalos"),
                                          ])])


txt_box_media = dbc.Col(id='form-media',
                        children=[
                            dbc.FormFloating([
                                dbc.Input(id="in_media", placeholder="Media", type="number",
                                          value=0, required=True, step=0.0001),
                                dbc.Label("Media"),
                            ])])

txt_box_desviacion = dbc.Col(id="form-desv", children=[
    dbc.FormFloating([
        dbc.Input(id="in_desviacion", placeholder="Desviación Estándar", type="number",
                  value=1, required=True, step=0.0001),
        dbc.Label("Desviación Estándar"),
    ])])

txt_box_lambda = dbc.Col(id="form-lambda", children=[
    dbc.FormFloating([
        dbc.Input(id="in_lambda", placeholder="Lambda", type="number",
                  value=5, required=True, step=0.0001),
        dbc.Label("Lambda"),
    ])])