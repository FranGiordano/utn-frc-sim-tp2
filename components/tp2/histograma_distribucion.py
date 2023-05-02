from plotly import graph_objs as go


def crear_histograma(lista_marca, lista_frec_observada, lista_frec_esperada) -> go.Figure:
    """
    Genera un histograma para una distribución.

    :param lista_frec_observada: 1ra lista de valores a representar en el eje y.
    :type lista_frec_observada: list[int]
    :param lista_frec_esperada: 2da lista de valores a representar en el eje y.
    :type lista_frec_esperada: list[float]
    :param lista_marca: Valores a representar en el eje x.
    :type lista_marca: list[float]
    :return: Figura con el histograma generado.
    :rtype: go.Figure
    """

    # Creación de histograma

    fig = go.Figure(
        layout=go.Layout(
            xaxis={"title": "Marca de clase"},
            yaxis={"title": "Frecuencia"},
            title={
                "text": "Histograma",
                "xanchor": "center",
                "x": 0.5,
                "font": {
                    "family": "Rubik",
                    "color": "Black",
                    "size": 30,
                }
            },
        )
    )

    fig.add_trace(
        go.Bar(
            x=lista_marca,
            y=lista_frec_observada,
            name="Frecuencia observada",
            marker_line={"width": 1, "color": "black"}
        )
    )

    fig.add_trace(
        go.Bar(
            x=lista_marca,
            y=lista_frec_esperada,
            name="Frecuencia esperada",
            marker_line={"width": 1, "color": "black"}
        )
    )

    return fig
