import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import requests
import plotly.graph_objs as go

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Dashboard de Estudiantes"

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
                        className="mb-2",
                    ),
                    width=3
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Distribución por Género"),
                            dbc.CardBody(
                                [
                                    dcc.Graph(
                                        id="genero-pie-chart",
                                        config={"displayModeBar": False},
                                    ),
                                ]
                            ),
                        ],
                        className="mb-4",
                    ),
                    width=3,
                    className="offset-md-3",
                )
            ]
        ),
    ],
    fluid=True,
)

# Callback para el total de estudiantes
@app.callback(
    dash.dependencies.Output("total-students", "children"),
    [dash.dependencies.Input("total-students", "id")],  # Dummy input para activar la carga inicial
)
def update_total_students(_):
    try:
        url = "http://localhost:5000/api/matricula/total"
        params = {"periodo": "2024A"}
        response = requests.get(url, params=params)
        data = response.json()
        return f"{data['estudiantes']} estudiantes"
    except Exception as e:
        return f"Error: {str(e)}"


# Callback para el gráfico de género
@app.callback(
    dash.dependencies.Output("genero-pie-chart", "figure"),
    [dash.dependencies.Input("genero-pie-chart", "id")],  # Dummy input para activar la carga inicial
)
def update_genero_pie(_):
    try:
        # Llama a la API
        url = "http://localhost:5000/api/matricula/genero"
        params = {"periodo": "2024A"}
        response = requests.get(url, params=params)
        data = response.json()

        # Extraer datos para la gráfica
        labels = [item["genero"] for item in data]
        values = [item["cantidad"] for item in data]

        # Crear la figura de Pie Chart
        figure = go.Figure(
            data=[
                go.Pie(
                    labels=labels,
                    values=values,
                    hole=0.3,  # Para un gráfico de dona
                )
            ]
        )
        figure.update_layout(title="Distribución por Género")
        return figure
    except Exception as e:
        return go.Figure(
            layout={"title": {"text": f"Error: {str(e)}", "font": {"color": "red"}}}
        )


if __name__ == "__main__":
    app.run_server(debug=True)
