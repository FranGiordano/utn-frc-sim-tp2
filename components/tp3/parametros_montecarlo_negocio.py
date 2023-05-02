import dash_bootstrap_components as dbc


def crear_parametros_montecarlo_negocio():

    parametros_negocio = dbc.Row([
        dbc.Col(id="form-inventario", children=[
            dbc.FormFloating([
                dbc.Input(id="in_inventario", placeholder="Inventario", type="number",
                          min=1, step=1, value=25000, required=True),
                dbc.Label("Inventario disponible"),
            ])]),

        dbc.Col(id='form-stock-inicial',
                children=[
                    dbc.FormFloating([
                        dbc.Input(id="in_stock_inicial",
                                  placeholder="Stock inicial",
                                  type="number", min=0, step=1,
                                  value=0, required=True),
                        dbc.Label("Stock inicial"),
                    ])]),

        dbc.Col(id='form-costo-sobrepaso',
                children=[
                    dbc.FormFloating([
                        dbc.Input(id="in_costo_sobrepaso",
                                  placeholder="Costo por sobrepaso",
                                  type="number", min=0, step=1,
                                  value=15000, required=True),
                        dbc.Label("Costo por sobrepaso"),
                    ])]),

        dbc.Col(id="form-costo-mantenimiento", children=[
            dbc.FormFloating([
                dbc.Input(id="in_costo_mantenimiento",
                          placeholder="Costo por mantenimiento", type="number", min=0,
                          value=6000, required=True, step=1),
                dbc.Label("Costo por mantenimiento"),
            ])]),

        dbc.Col(id="form-costo-pedido", children=[
            dbc.FormFloating([
                dbc.Input(id="in_costo_pedido", placeholder="Costo por pedido", type="number", min=0,
                          value=550000, required=True, step=1),
                dbc.Label("Costo por pedido"),
            ])]),
    ])

    return parametros_negocio