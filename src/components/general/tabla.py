from dash import html
import dash_bootstrap_components as dbc

def crear_tabla(diccionario) -> dbc.Table:
    """
    Genera una tabla en base a los datos de un diccionario.

    :param diccionario: Un diccionario con keys de tipo str y values de tipo list[float] o float
    :type diccionario: Union[dict[str,list[float]], dict[str, float]]
    :return: La tabla con los valores correspondientes.
    :rtype: dbc.Table
    """

    # Se crea el encabezado de la tabla

    table_header = [html.Thead(html.Tr([html.Th(i) for i in diccionario.keys()]))]

    # Se crea el cuerpo de la tabla

    rows = []
    lista_body = list(diccionario.values())

    # Para la creación de las filas se itera sobre las listas contenidas en cada value del diccionario. En caso de que
    # el value esté dado por un escalar y no por una lista, se convierte este escalar a lista:

    try:
        n = len(lista_body[0])
    except TypeError:
        lista_body = [[escalar] for escalar in lista_body]
        n = 1

    for i in range(n):
        row = html.Tr([html.Td(lista[i]) for lista in lista_body])
        rows.append(row)

    table_body = [html.Tbody(rows)]

    # Creación de la tabla

    table = dbc.Table(table_header + table_body, class_name="w-auto mx-auto mt-3", striped=True, bordered=True,
                      responsive=True)

    return table
