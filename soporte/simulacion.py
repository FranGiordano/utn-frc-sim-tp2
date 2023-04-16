import random as rd
import math
import plotly.graph_objs as go
import numpy as np


def generar_lista_uniforme(n, a, b):
    if a > b:
        a, b = b, a
    serie = []
    for i in range(n):
        x = a + (b - a) * rd.random()
        serie.append(x)
    return serie

def generar_numeros_aleatorios_normal(cantidad, media, desviacion):
    numeros_aleatorios = []
    for i in range(cantidad):
        r1 = rd.random()
        r2 = rd.random()
        z = math.sqrt(-2.0 * math.log(r1)) * math.cos(2 * math.pi * r2)
        numeros_aleatorios.append(media + desviacion * z)
    return numeros_aleatorios
def generar_lista_exponencial_negativa(n, lam):
    serie = []
    for i in range(n):
        x = -(1 / lam) * math.log(1 - rd.random())
        serie.append(x)
    return serie


def generar_lista_normal(n, desv_est, media):
    serie = []
    i = 0
    while i < n:
        rd1 = rd.random()
        rd2 = rd.random()
        n1 = math.sqrt(-2 * math.log(rd1)) * math.cos(2 * math.pi * rd2) * desv_est + media
        n2 = math.sqrt(-2 * math.log(rd1)) * math.sin(2 * math.pi * rd2) * desv_est + media
        serie.append(n1)
        serie.append(n2)
        i += 2
    if n % 2 == 1:
        serie.pop()
    return serie


def generar_lista_poisson(n, lam):
    serie = []
    for i in range(n):
        p = 1
        x = -1
        a = math.e ** (-lam)
        while p >= a:
            u = rd.random()
            p *= u
            x = x + 1
        serie.append(x)
    return serie


def generar_histograma(muestras, n_barras):

    # Constantes

    maximo = max(muestras)
    minimo = min(muestras)
    rango = (maximo - minimo) / n_barras

    # Creación de histograma

    fig = go.Figure(
        data=go.Histogram(
            x=muestras,
            xbins=dict(
                start=minimo,
                size=rango,
                end=maximo
            ),
            marker_line=dict(width=1, color="black")
        ),
        layout=go.Layout(
            xaxis=dict(title="Valores"),
            yaxis=dict(title="Cantidad"),
            title={
                "text": "Histograma",
                }
        )
    )

    return fig