import math
import random as rd
import plotly.graph_objs as go
from scipy.special import factorial
from scipy.stats import kstwo, chi2


def generar_serie_uniforme(n, a, b):
    if a > b:
        a, b = b, a
    return [rd.random() * (b - a) + a for _ in range(n)]


def generar_serie_normal(cantidad, desviacion, media):
    numeros_aleatorios = []
    for i in range(cantidad):
        r1 = rd.random()
        r2 = rd.random()
        while r1 == 0:
            r1 = rd.random()
        z = math.sqrt(-2.0 * math.log(r1)) * math.cos(2 * math.pi * r2)
        numeros_aleatorios.append(media + desviacion * z)
    return numeros_aleatorios


def generar_serie_exponencial_negativa(n, lam):
    return [-(1 / lam) * math.log(1 - rd.random()) for _ in range(n)]


def generar_serie_poisson(n, lam):
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

    eje_x = [i for i in range(minimo, maximo+1)]
    frecuencias = [muestras.count(i) for i in eje_x]

    # Creación de histograma

    fig = go.Figure(
        data=go.Bar(
            x=eje_x,
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
    # Constantes

    n = len(muestras)
    maximo = max(muestras)
    minimo = min(muestras)
    rango = (maximo - minimo) / n_barras

    # Se establecen límites inferiores y superiores y se cuentan las frecuencias observadas

    li = [minimo]
    ls = [minimo + rango]

    for i in range(1, n_barras):
        li.append(ls[i - 1])
        ls.append(ls[i - 1] + rango)

    fo = [0] * n_barras

    for i in muestras:
        for j in range(n_barras):
            if li[j] <= i < ls[j]:
                fo[j] += 1
                break

    # Como el loop anterior no tiene en cuenta al valor máximo, se lo añade en la siguiente línea

    fo[-1] += muestras.count(maximo)

    # Cálculo de frecuencia esperada de acuerdo a tipo de distribución

    match distribucion:

        case "U":
            fe = [n / n_barras] * n_barras

        case "N":
            media = sum(muestras) / n
            desv_est = math.sqrt(sum([(i - media) ** 2 for i in muestras]) / (n - 1))
            marca = [(li[i] + ls[i]) / 2 for i in range(n_barras)]
            fe = []
            for i in range(n_barras):
                prob = (1 / (desv_est * math.sqrt(2 * math.pi))) * math.exp(
                    -(1 / 2) * ((marca[i] - media) / desv_est) ** 2) * (ls[i] - li[i])
                fe.append(prob * n)

        case "EN":
            media = sum(muestras) / n
            lam = 1 / media
            fe = []
            for i in range(n_barras):
                prob = -math.exp(-lam * ls[i]) + math.exp(-lam * li[i])
                fe.append(prob * n)

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

    # Constantes

    maximo = max(muestras)
    minimo = min(muestras)
    n = len(muestras)
    lam = sum(muestras) / n

    # Vectores

    x = [i for i in range(minimo, maximo+1)]
    fo = [muestras.count(i) for i in x]
    fe = []
    for i in x:
        prob = lam ** i * math.exp(-lam) / factorial(i)
        fe.append(int(round(prob * n, 0)))

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

    fo = nuevo_fo
    fe = nuevo_fe

    # Chi-Cuadrado calculado:

    chi2_calculado = 0
    for i in range(len(fo)):
        chi2_calculado += (fo[i] - fe[i]) ** 2 / fe[i]

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

    # K-S calculado:

    ks_calculado = po_acum = pe_acum = 0
    for i in range(len(fo)):
        po_acum += fo[i] / n
        pe_acum += fe[i] / n
        dif = abs(po_acum - pe_acum)
        if dif > ks_calculado:
            ks_calculado = dif

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
