import asyncio
import aiohttp
from dash import Dash, html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

HEADER_LOGO_PATH = "/assets/tsj.png"
FOOTER_LOGO_EDU = "/assets/educacion.svg" 
FOOTER_LOGO_TEC = "/assets/tecnologico.svg" 
FOOTER_LOGO_INN = "/assets/innovacion.svg" 
FOOTER_LOGO_JAL = "/assets/jalisco.svg" 

# Inicializar la app
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
app.title = "Dashboard TSJ"


# Función asíncrona para obtener datos del backend
async def fetch_data(session, endpoint):
    try:
        async with session.get(f"http://127.0.0.1:5010/{endpoint}") as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Error fetching {endpoint}: HTTP {response.status}")
                return None
    except aiohttp.ClientConnectorError as e:
        print(f"Connection error while fetching {endpoint}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error in fetch_data for {endpoint}: {e}")
        return None

# Función para realizar todas las solicitudes simultáneamente
async def fetch_all_data():
    async with aiohttp.ClientSession() as session:
        endpoints = ["data/total", "data/gender", "data/mode", "data/status", "data/unidad", "data/carrera"]
        tasks = [fetch_data(session, endpoint) for endpoint in endpoints]
        return await asyncio.gather(*tasks)
    


# Layout de la aplicación
app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.Div(
                            html.Img(src=HEADER_LOGO_PATH, height="60px"),
                            className="d-flex align-items-center",
                            style={"flex": "1", "justify-content": "flex-start"},
                        ),
                        html.H1(
                            "Dashboard de Matrícula 2024",
                            className="text-primary text-center mb-0",
                            style={"flex": "3"},
                        ),
                    ],
                    className="d-flex align-items-center justify-content-between",
                ),                
                width=12,
            ),
            className="bg-light p-3 shadow-sm mb-4",
        ),
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
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4("Carrera", className="card-title"),
                            html.H2("Cargando...", id="carrera-stu", className="text-center"),
                        ]
                    )
                ),
                width=12,
            )
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.Div(
                            [
                                html.Img(src=FOOTER_LOGO_EDU, height="50px", className="mx-2"),
                                html.Img(src=FOOTER_LOGO_TEC, height="50px", className="mx-2"),
                                html.Img(src=FOOTER_LOGO_INN, height="50px", className="mx-2"),
                                html.Img(src=FOOTER_LOGO_JAL, height="50px", className="mx-2"),
                            ],
                            className="d-flex align-items-center justify-content-center",
                        ),
                        html.P(
                            "Institución Tecnológico Superior de Jalisco 2024",
                            className="text-muted text-center mt-3 mb-0",
                        ),
                    ]
                ),
                className="bg-light p-3 shadow-sm",
            )
        ),
        dbc.Row(
            dbc.Col(html.Div(id="update-status", className="mt-3")),
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
        Output("carrera-stu", "children"),
        Output("update-status", "children"),
    ],
    [Input("total-students", "id")],  # Callback se activa al cargar el layout
)

def update_dashboard(_):
    # Usamos asyncio para realizar las solicitudes concurrentes
    data = asyncio.run(fetch_all_data())
    students_data, gender_data, mode_data, status_data, unidad_data, carrera_data = data

    if students_data and gender_data and mode_data and status_data and unidad_data and carrera_data:
        # Total de estudiantes
        total_students_data = students_data.get("total_students", 0)
        total_students = "{:,}".format(total_students_data)
        # Distribución por género
        gender_distribution = gender_data.get("gender_distribution", {})
        gender_df = pd.DataFrame(
            [{"Género": k, "Cantidad": v} for k, v in gender_distribution.items()]
        )
        gender_chart = px.pie(
            gender_df,
            names="Género",
            values="Cantidad",
            height=300
        )

        # Modalidad
        modalidad_distribution = mode_data.get("mode_distribution", {})
        mode_rows = [{"Tipo": key, "Cantidad": value} for key, value in modalidad_distribution.items()]
        mode_table = dash_table.DataTable(
            columns=[{"name": col, "id": col} for col in ["Tipo", "Cantidad"]],
            data=mode_rows,
            style_table={
                "overflowX": "auto",  
                "border": "1px solid #dee2e6",  
                "height":"300px"
            },
            style_cell={
                "textAlign": "left",  
                "fontSize": "12px",  
                "fontFamily": "Arial, sans-serif",  
                "padding": "4px 8px",  
                "border": "1px solid #dee2e6",
            },
            style_header={
                "backgroundColor": "#f8f9fa",
                "fontWeight": "bold",
                "fontSize": "13px",
                "textAlign": "center",
                "border": "1px solid #dee2e6",
            },
        )

        # Estatus
        status_distribution = status_data.get("status_distribution", {})
        status_rows = [{"Tipo": key, "Cantidad": value} for key, value in status_distribution.items()]
        status_table = dash_table.DataTable(
            columns=[{"name": col, "id": col} for col in ["Tipo", "Cantidad"]],
            data=status_rows,
            style_table={
                "overflowX": "auto",
                "border": "1px solid #dee2e6",
                "height":"300px"
            },
            style_cell={
                "textAlign": "left",
                "fontSize": "12px",
                "fontFamily": "Arial, sans-serif",
                "padding": "4px 8px",
                "border": "1px solid #dee2e6",
            },
            style_header={
                "backgroundColor": "#f8f9fa",
                "fontWeight": "bold",
                "fontSize": "13px",
                "textAlign": "center",
                "border": "1px solid #dee2e6",
            },
        )

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

        # carrera
        carrera_distribution = carrera_data.get("carrera_distribution", [])
        carrera_rows = [
            {"Unidad": item["nombreUReal"], "Carrera": item["carrera"], "Modalidad": item["modalidad"], "Estudiantes": item["estudiantes"]}
            for item in carrera_distribution
        ]

        carrera_table = dash_table.DataTable(
            columns=[{"name": col, "id": col} for col in ["Unidad", "Carrera", "Modalidad", "Estudiantes"]],
            data=carrera_rows,
            style_table={
                "overflowX": "auto",
                "border": "1px solid #dee2e6",
                "height": "300px"
            },
            style_cell={
                "textAlign": "left",
                "fontSize": "12px",
                "fontFamily": "Arial, sans-serif",
                "padding": "4px 8px",
                "border": "1px solid #dee2e6",
            },
            style_header={
                "backgroundColor": "#f8f9fa",
                "fontWeight": "bold",
                "fontSize": "13px",
                "textAlign": "center",
                "border": "1px solid #dee2e6",
            },
        )

        return (
            total_students,
            gender_chart,
            mode_table,
            status_table,
            unidad_chart,
            carrera_table,            
            "Datos cargados automáticamente.",
        )
    else:
        return "Error", {}, "Error", "Error", {}, "Error al obtener datos del backend."

if __name__ == "__main__":
    app.run_server(debug=True, port=5002)
