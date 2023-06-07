import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__,
                   path="/",
                   title="Simulación",
                   update_title="Simulación",
                   name="Simulación")

layout = dbc.Container([
    html.Center(html.B(html.H1("Simulación 2023 - 4K2 - Grupo Nº3"))),
    html.Br(),

    html.Center(html.U(html.H2("Integrantes"))),
    html.Br(),

    dbc.Table([
        html.Thead(html.Tr([html.Th("Legajo"), html.Th("Apellido y Nombres")])),
        html.Tbody([
            html.Tr([html.Td("72905"), html.Td("Flores, Jorge Martin")]),
            html.Tr([html.Td("81757"), html.Td("Giordano, Franco Omar")]),
            html.Tr([html.Td("86120"), html.Td("Grande, Tamara Araceli")]),
            html.Tr([html.Td("86425"), html.Td("Gutierrez, Ezequiel")]),
            html.Tr([html.Td("85461"), html.Td("Molina, Juan Ignacio")])
        ])
    ], class_name="w-auto", striped=True, bordered=True, style={"margin": "auto"}),

    html.Br(),
    html.Center(html.U(html.H2("Trabajos Prácticos"))),
    html.Br(),

    dbc.Row([
        dbc.Col([
            dbc.Card(
                [
                    dbc.CardImg(src="/assets/cards/tp2.png", top=True),
                    dbc.CardBody(
                        [
                            html.H4("TP2: Generador de Variables Aleatorias", className="card-title"),
                            html.P(
                                "Generación de variables aleatorias para distribuciones normales, exponenciales, "
                                "uniformes y de Poisson, con histogramas y pruebas de bondad de "
                                "ajuste.",
                                className="card-text", style={"text-align": "justify"}
                            ),
                            dbc.Button("Ir al proyecto", color="primary", href="/tp2/"),
                        ]
                    ),
                ],
                style={"width": "18rem"},
                className="mx-auto"
            ),
        ]),

        dbc.Col([
            dbc.Card(
                [
                    dbc.CardImg(src="/assets/cards/tp3.png", top=True),
                    dbc.CardBody(
                        [
                            html.H4("TP3: Simulación de Monte Carlo", className="card-title"),
                            html.P(
                                "Ejecución de una simulación de Monte Carlo para la producción de una empresa "
                                "fabricante de lavadoras industriales en el país, aplicando un Vector de Estado.",
                                className="card-text", style={"text-align": "justify"}
                            ),
                            dbc.Button("Ir al proyecto", color="primary", href="/tp3/"),
                        ]
                    ),
                ],
                style={"width": "18rem"},
                className="mx-auto"
            ),
        ]),

        dbc.Col([
            dbc.Card(
                [
                    dbc.CardImg(src="/assets/cards/tp4.jpg", top=True),
                    dbc.CardBody(
                        [
                            html.H4("TP4: Modelos de Simulación Dinámicos", className="card-title"),
                            html.P(
                                "Ejecución de una simulación de líneas de espera (colas) para la simulación del sistema"
                                " de atención de pasajeros de la estación de tren de Córdoba.",
                                className="card-text", style={"text-align": "justify"}
                            ),
                            dbc.Button("Ir al proyecto", color="primary", href="/tp4/"),
                        ]
                    ),
                ],
                style={"width": "18rem"},
                className="mx-auto"
            ),
        ])

    ])
])
    


