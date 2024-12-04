from dash import html
import dash_bootstrap_components as dbc

def gender_card(data):
    male = data.get("M", 0)
    female = data.get("F", 0)

    return dbc.Card(
        dbc.CardBody(
            [
                html.H5("Distribución por Género", className="card-title"),
                html.P(f"Hombres: {male}", className="card-text"),
                html.P(f"Mujeres: {female}", className="card-text"),
            ]
        )
    )
