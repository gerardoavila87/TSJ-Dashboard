from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from components.gender_card import gender_card
from components.total_card import total_card
import requests
import pandas as pd
import plotly.express as px

# Inicializar la app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Dashboard TSJ"

# Función para obtener datos del backend
def fetch_data(endpoint):
    try:
        response = requests.get(f"http://127.0.0.1:5000/{endpoint}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

# Layout de la aplicación
# Layout con contenedores para los IDs requeridos
app.layout = dbc.Container(
    [
        dbc.Row(dbc.Col(html.H1("Dashboard TSJ", className="text-center mb-4"))),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Total Estudiantes", className="card-title"),
                                html.H2("Cargando...", id="total-students", className="text-center"),
                            ]
                        )
                    ),
                    width=4,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Distribución por Género", className="card-title"),
                                dcc.Graph(id="gender-chart"),
                            ]
                        )
                    ),
                    width=8,
                ),
            ]
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button(
                    "Actualizar Datos",
                    id="update-data",
                    color="primary",
                    className="mt-4",
                )
            )
        ),
        dbc.Row(
            dbc.Col(html.Div(id="update-status", className="mt-3")),
        ),
    ],
    fluid=True,
)

# Callback para actualizar los datos
@app.callback(
    [
        Output("total-students", "children"),
        Output("gender-chart", "figure"),
        Output("update-status", "children"),
    ],
    [Input("update-data", "n_clicks")],
)
def update_dashboard(n_clicks):
    if n_clicks:
        students_data = fetch_data("data/total")  # Endpoint: {"total_students": 1000}
        gender_data = fetch_data("data/gender")  # Endpoint: {"gender_distribution": {"M": 5306, "F": 3184}}

        if students_data and gender_data:
            # Obtener el total de estudiantes
            total_students = students_data.get("total_students", 0)

            # Obtener la distribución por género
            gender_distribution = gender_data.get("gender_distribution", {})
            gender_df = pd.DataFrame(
                [{"Género": k, "Cantidad": v} for k, v in gender_distribution.items()]
            )
            
            # Crear la gráfica
            gender_chart = px.pie(
                gender_df, 
                names="Género", 
                values="Cantidad", 
                title="Distribución por Género"
            )

            return total_students, gender_chart, "Datos actualizados correctamente."
        else:
            return "Error", {}, "Error al obtener datos del backend."
    return "", {}, ""


if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
