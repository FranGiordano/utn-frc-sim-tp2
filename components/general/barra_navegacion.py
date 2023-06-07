import dash_bootstrap_components as dbc
from dash import html


def crear_barra_navegacion() -> dbc.Navbar:
    """
    Genera una barra de navegación para la página web.
    :return: La barra de navegación.
    :rtype: dbc.Navbar
    """
    barra_navegacion = dbc.Navbar(
        dbc.Container([
            dbc.NavItem(
                dbc.Row(
                    [
                        dbc.Col(
                            html.Img(src="/assets/icons/simulation.png", height="30px")),
                        dbc.Col(dbc.NavbarBrand("UTN FRC - Simulación",
                                                className="ms-2", href="/")),
                    ],
                    align="center",
                    className="g-0",
                )),
            dbc.NavItem(
                dbc.NavLink("Inicio", href="/", style={"color": "white"}),
                class_name="ms-auto px-3"),
            dbc.NavItem(
                dbc.NavLink("TP2", href="/tp2/", style={"color": "white"}),
                class_name="px-3"),
            dbc.NavItem(
                dbc.NavLink("TP3", href="/tp3/", style={"color": "white"}),
                class_name="px-3"),
            dbc.NavItem(
                dbc.NavLink("TP4", href="/tp4/", style={"color": "white"}),
                class_name="px-3"),
            html.A(
                html.Img(src="/assets/icons/github-mark-white.svg",
                         height="30px"),
                href="https://github.com/FranGiordano/utn-frc-sim-tp2",
                style={"textDecoration": "none"},
                target="_blank"
            ),
        ]),
        color="primary",
        dark=True
    )
    return barra_navegacion
