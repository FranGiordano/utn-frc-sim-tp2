import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__,
                   path="/",
                   title="Simulación",
                   update_title="Simulación",
                   name="Simulación")

layout = dbc.Container([
    html.Center(html.H1("Simulación 2023 - Grupo Nº3")),

    html.H2("Integrantes"),
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
    ], class_name="w-auto", striped=True, bordered=True),

    html.Br(),
    html.H2("Trabajos realizados"),
    html.Br(),

    dbc.Card(
        [
            dbc.CardImg(src="/assets/cards/tp2.png", top=True),
            dbc.CardBody(
                [
                    html.H4("TP2: Variables Aleatorias", className="card-title"),
                    html.P(
                        "Generación de variables aleatorias para distribuciones normales, exponenciales, uniformes y de"
                        " Poisson, junto a sus respectivos histogramas y pruebas de bondad de ajuste.",
                        className="card-text",
                    ),
                    dbc.Button("Ir al proyecto", color="primary", href="/tp2/"),
                ]
            ),
        ],
        style={"width": "20rem"},
    ),
])
    
    
