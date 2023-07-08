import dash_bootstrap_components as dbc


def crear_alerta_ks(ks_calculado, ks_tabulado):

    # Se crea una alerta en base al resultado de la prueba

    if ks_calculado <= ks_tabulado:
        alerta = dbc.Alert(
            "El test de K-S no rechaza la hipótesis nula", color="success")
    else:
        alerta = dbc.Alert(
            "El test de K-S rechaza la hipótesis nula", color="danger")

    return alerta
