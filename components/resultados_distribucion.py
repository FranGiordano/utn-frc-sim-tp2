import dash_bootstrap_components as dbc
from dash import html, dcc


def crear_resultados_distribucion(histograma, muestras, tabla_frecuencia, tabla_chi2, alerta_chi2, tabla_ks, alerta_ks):

    visualizacion = html.Div([

        # Histograma

        dcc.Graph(figure=histograma),

        dbc.Accordion([

            # Frecuencias observadas y esperadas

            dbc.AccordionItem(html.Div(tabla_frecuencia, className="table-container"),
                              title="Frecuencias observadas y esperadas"),

            # Pruebas de ajuste

            dbc.AccordionItem([
                dbc.Row([
                    dbc.Col([
                        html.Center(html.H4("Chi-cuadrado")),
                        tabla_chi2,
                        alerta_chi2,
                    ]),
                    dbc.Col([
                        html.Center(html.H4("Kolmogorov-Smirnov")),
                        tabla_ks,
                        alerta_ks,
                    ]),
                ])
            ], title="Pruebas de bondad de ajuste"),

            # Números generados

            dbc.AccordionItem([
                html.Div([
                    html.Ul([html.Li(str(round(n, 2))) for n in muestras[:1000]], className="columnas")
                ], className="table-container"),
            ], title="Lista de 1000 primeros números generados"),

        ], start_collapsed=True, always_open=True),
    ])

    return visualizacion
