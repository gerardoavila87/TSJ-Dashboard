import asyncio
import aiohttp
from dash import Dash, html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Inicializar la app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Dashboard TSJ"

# Función asíncrona para obtener datos del backend
async def fetch_data(session, endpoint):
    try:
        async with session.get(f"http://127.0.0.1:5001/{endpoint}") as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Error fetching {endpoint}: {response.status}")
                return None
    except Exception as e:
        print(f"Exception in fetch_data for {endpoint}: {e}")
        return None

# Función para realizar todas las solicitudes simultáneamente
async def fetch_all_data():
    async with aiohttp.ClientSession() as session:
        endpoints = ["data/total", "data/gender", "data/mode", "data/status", "data/unidad"]
        tasks = [fetch_data(session, endpoint) for endpoint in endpoints]
        return await asyncio.gather(*tasks)

# Layout de la aplicación
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
                    width=3,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Género", className="card-title"),
                                dcc.Graph(id="gender-chart"),
                            ]
                        )
                    ),
                    width=3,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Modalidad", className="card-title"),
                                html.H2("Cargando...", id="modalidad-stu", className="text-center"),
                            ]
                        )
                    ),
                    width=3,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Estatus", className="card-title"),
                                html.H2("Cargando...", id="status-stu", className="text-center"),
                            ]
                        )
                    ),
                    width=3,
                ),
            ]
        ),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4("Estudiantes por Unidad", className="card-title"),
                            dcc.Graph(id="unidad-chart"),
                        ]
                    )
                ),
                width=12,
            )
        ),
        dbc.Row(
            dbc.Col(html.Div(id="update-status", className="mt-3")),
        ),
        dcc.Interval(
            id="interval-component",  # Componente para disparar la carga inicial
            interval=1,  # Se ejecuta una sola vez al inicio (en ms)
            n_intervals=0,
        ),
    ],
    fluid=True,
)

# Callback para actualizar el dashboard
@app.callback(
    [
        Output("total-students", "children"),
        Output("gender-chart", "figure"),
        Output("modalidad-stu", "children"),
        Output("status-stu", "children"),
        Output("unidad-chart", "figure"),
        Output("update-status", "children"),
    ],
    [Input("interval-component", "n_intervals")],
)
def update_dashboard(n_intervals):
    # Usamos asyncio para realizar las solicitudes concurrentes
    data = asyncio.run(fetch_all_data())
    students_data, gender_data, mode_data, status_data, unidad_data = data

    if students_data and gender_data and mode_data and status_data and unidad_data:
        # Total de estudiantes
        total_students = students_data.get("total_students", 0)

        # Distribución por género
        gender_distribution = gender_data.get("gender_distribution", {})
        gender_df = pd.DataFrame(
            [{"Género": k, "Cantidad": v} for k, v in gender_distribution.items()]
        )
        gender_chart = px.pie(
            gender_df,
            names="Género",
            values="Cantidad",
            title="Distribución por Género",
        )

        # Modalidad
        modalidad_distribution = mode_data.get("mode_distribution", {})
        modalidad_total = sum(modalidad_distribution.values())

        # Estatus
        status_distribution = status_data.get("status_distribution", {})
        status_total = sum(status_distribution.values())

        # Estudiantes por Unidad
        unidad_distribution = unidad_data.get("unidad_distribution", {})
        unidad_df = pd.DataFrame(
            [{"Unidad": k, "Estudiantes": v} for k, v in unidad_distribution.items()]
        )
        unidad_chart = px.bar(
            unidad_df,
            x="Unidad",
            y="Estudiantes",
            title="Estudiantes por Unidad Académica",
            labels={"Estudiantes": "Número de Estudiantes", "Unidad": "Unidad Académica"},
        )

        return (
            total_students,
            gender_chart,
            modalidad_total,
            status_total,
            unidad_chart,
            "Datos cargados automáticamente.",
        )
    else:
        return "Error", {}, "Error", "Error", {}, "Error al obtener datos del backend."

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
