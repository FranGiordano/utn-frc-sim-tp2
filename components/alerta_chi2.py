import dash_bootstrap_components as dbc


def crear_alerta_chi2(grados_de_libertad, chi2_calculado, chi2_tabulado):

    # Se crea una alerta en base al resultado de la prueba

    if grados_de_libertad <= 0:
        alerta = dbc.Alert("La cantidad de muestras no es suficiente para conseguir el χ2 tabulado ó se presentó un "
                           "error de cálculo", color="danger")
    elif chi2_calculado <= chi2_tabulado:
        alerta = dbc.Alert(
            "El test de χ2 no rechaza la hipótesis nula", color="success")
    else:
        alerta = dbc.Alert(
            "El test de χ2 rechaza la hipótesis nula", color="danger")

    return alerta
