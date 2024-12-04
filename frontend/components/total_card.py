from dash import html
import dash_bootstrap_components as dbc

def total_card(total):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H5("Total de Estudiantes", className="card-title"),
                html.P(f"{total}", className="card-text"),
            ]
        )
    )
