import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import requests

# Inicializa la aplicación con un tema Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Dashboard de Estudiantes"

# Layout principal de la aplicación
app.layout = dbc.Container(
    [
        html.H1("Dashboard de Control Escolar", className="text-center my-4"),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Total de Estudiantes"),
                            dbc.CardBody(
                                [
                                    html.H4(
                                        id="total-students",
                                        className="card-title text-center",
                                    ),
                                    html.P(
                                        "Cantidad total de estudiantes activos en el periodo.",
                                        className="card-text text-center",
                                    ),
                                ]
                            ),
                        ],
                        className="mb-4",
                    ),
                    width=6,
                    className="offset-md-3",
                )
            ]
        ),
    ],
    fluid=True,
)

# Callback para obtener el total de estudiantes desde la API
@app.callback(
    dash.dependencies.Output("total-students", "children"),
    [dash.dependencies.Input("total-students", "id")],  # Dummy input para activar la carga inicial
)
def update_total_students(_):
    try:
        # Llama a la API
        url = "http://localhost:5000/api/total_students"
        params = {"periodo": "2024A"}  # Parámetros de ejemplo
        response = requests.get(url, params=params)
        data = response.json()

        # Devuelve el total
        return f"{data['estudiantes']} estudiantes"
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    app.run_server(debug=True)
