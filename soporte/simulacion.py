import random as rd
import math
import plotly.graph_objs as go
import numpy as np
from scipy.special import factorial
from scipy.stats import kstwo, chi2


def generar_lista_uniforme(n, a, b):
    if a > b:
        a, b = b, a
    serie = []
    for i in range(n):
        x = a + (b - a) * rd.random()
        serie.append(x)
    return serie


def generar_numeros_aleatorios_normal(cantidad, desviacion, media):
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


def generar_histograma_continua(muestras, n_barras):

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
            xaxis=dict(title="Valor"),
            yaxis=dict(title="Frecuencia"),
            title={
                "text": "Histograma",
                "xanchor": "center",
                "x": 0.5,
                "font": {
                    "family": "Rubik",
                    "color": "Black",
                    "size": 30,
                }
            }
        )
    )

    return fig


def generar_histograma_poisson(muestras):

    # Constantes

    minimo = min(muestras)
    maximo = max(muestras)

    # Vectores

    x = np.arange(minimo, maximo+1)
    frecuencias = [muestras.count(i) for i in x]

    # Creación de histograma

    fig = go.Figure(
        data=go.Bar(
            x=x,
            y=frecuencias,
            marker_line=dict(width=1, color="black")
        ),
        layout=go.Layout(
            xaxis=dict(title="Valor"),
            yaxis=dict(title="Frecuencia"),
            title={
                "text": "Histograma",
                "xanchor": "center",
                "x": 0.5,
                "font": {
                    "family": "Rubik",
                    "color": "Black",
                    "size": 30,
                }
            }
        )
    )

    return fig


def calcular_frecuencias_continua(muestras, n_barras, distribucion):

    # Conversión de lista a numpy array

    muestras = np.array(muestras)

    # Constantes

    n = len(muestras)

    # Vectores

    fo, limites = np.histogram(muestras, n_barras)
    li = limites[:-1]
    ls = limites[1:]

    # Cálculo de frecuencia esperada de acuerdo a tipo de distribución

    match distribucion:

        case "U":
            fe = [n / n_barras] * n_barras

        case "N":
            media = sum(muestras) / n
            desv_est = np.sqrt(sum((muestras-media)**2) / (n-1))
            marca = (ls + li) / 2
            prob = (1/(desv_est * np.sqrt(2*np.pi))) * np.exp(-(1/2)*((marca-media)/desv_est)**2) * (ls-li)
            fe = prob * n

        case "EN":
            media = sum(muestras) / n
            lam = 1 / media
            prob = -np.exp(-lam * ls) + np.exp(-lam * li)
            fe = prob * n

        case _:
            raise Exception

    # Asignación de vectores en una tabla única

    diccionario = {
        "#": range(1, n_barras + 1),
        "Desde": li,
        "Hasta": ls,
        "Frecuencia observada": fo,
        "Frecuencia esperada": fe
    }

    return diccionario


def calcular_frecuencias_poisson(muestras):

    # Conversión de lista a numpy array

    muestras = np.array(muestras)

    # Constantes

    maximo = max(muestras)
    minimo = min(muestras)
    n = len(muestras)
    lam = sum(muestras) / n

    # Vectores

    x = np.arange(minimo, maximo+1)
    fo = [(muestras == i).sum() for i in x]
    prob = lam ** x * np.exp(-lam) / factorial(x)
    fe = np.round(prob * n, 0).astype(int)

    # Asignación de vectores en un diccionario

    diccionario = {
        "#": x,
        "Valor": x,
        "Frecuencia observada": fo,
        "Frecuencia esperada": fe
    }

    return diccionario


def calcular_chi2(fo, fe, distribucion):

    # Agrupamiento de frecuencias de forma que cada valor de frecuencias esperadas sea >= 5:

    nuevo_fo = []
    nuevo_fe = []

    acum_fe = 0
    acum_fo = 0

    for i in range(len(fe)):

        acum_fe += fe[i]
        acum_fo += fo[i]

        if acum_fe >= 5:
            nuevo_fe.append(acum_fe)
            nuevo_fo.append(acum_fo)
            acum_fe = 0
            acum_fo = 0

    if not nuevo_fe:
        nuevo_fe.append(acum_fe)
        nuevo_fo.append(acum_fo)
    elif acum_fo > 0 or acum_fe > 0:
        nuevo_fe[-1] += acum_fe
        nuevo_fo[-1] += acum_fo

    fo = np.array(nuevo_fo)
    fe = np.array(nuevo_fe)

    # Chi-Cuadrado calculado:

    c = (fo - fe) ** 2 / fe
    chi2_calculado = sum(c)

    # Chi-Cuadrado tabulado:

    m = {"U": 0, "EN": 1, "N": 2, "P": 1}
    k = len(fo)
    grados_libertad = k - 1 - m[distribucion]
    nivel_de_confianza = 0.95
    chi2_tabulado = chi2.ppf(nivel_de_confianza, grados_libertad)

    # Asignación de datos en un diccionario

    diccionario = {
        "Nivel de confianza": nivel_de_confianza,
        "Grados de libertad": grados_libertad,
        "χ2 calculado": chi2_calculado,
        "χ2 tabulado": chi2_tabulado
    }

    return diccionario


def calcular_ks(fo, fe):

    # Constantes

    n = sum(fo)

    # Conversión de listas a numpy arrays

    fo = np.array(fo)
    fe = np.array(fe)

    # K-S calculado:

    po = fo / n
    pe = fe / n
    po_ac = np.cumsum(po)
    pe_ac = np.cumsum(pe)
    dif = abs(po_ac - pe_ac)
    ks_calculado = max(dif)

    # K-S tabulado:

    nivel_de_confianza = 0.95
    ks_tabulado = kstwo.ppf(nivel_de_confianza, n)

    # Asignación de datos en un diccionario

    diccionario = {
        "Nivel de confianza": nivel_de_confianza,
        "Cantidad de muestras": n,
        "K-S calculado": ks_calculado,
        "K-S tabulado": ks_tabulado
    }

    return diccionario
