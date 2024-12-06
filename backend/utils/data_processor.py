
# Para el analisis de los datos se utilizan funciones puras
def get_total_students(data):
    return len(data)

def get_gender_distribution(data):
    return data["genero"].value_counts().to_dict()

def get_mode_distribution(data):
    return data["modalidad"].value_counts().to_dict()

def get_status_distribution(data):
    return data["status"].value_counts().to_dict()

def get_unidad_distribution(data):
    return data["nombreUReal"].value_counts().to_dict()

def get_procedencia_distribution(data):
    return data["municipio"].value_counts().to_dict()

def get_carrera_distribution(data):
    distribution = data.groupby(["carrera", "modalidad", "nombreUReal"]).size().reset_index(name="estudiantes")
    distribution_list = distribution.to_dict(orient="records")
    return distribution_list
