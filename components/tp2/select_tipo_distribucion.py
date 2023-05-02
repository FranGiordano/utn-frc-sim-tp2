import dash_bootstrap_components as dbc


def crear_select_tipo_distribucion() -> dbc.InputGroup:
    """
    Genera un dropdown para la selección del tipo de distribución.

    :return: El dropdown de distribuciones.
    :rtype: dbc.InputGroup
    """

    tipo_distribucion = dbc.InputGroup([
        dbc.Select(
            id="controls-dist",
            options=[
                {"label": "Exponencial Negativa", "value": "EN"},
                {"label": "Normal", "value": "N"},
                {"label": "Poisson", "value": "P"},
                {"label": "Uniforme", "value": "U"},
            ],
            value="U"
        ),
        dbc.InputGroupText("Distribución")
    ])

    return tipo_distribucion
