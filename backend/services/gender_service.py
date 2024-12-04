from flask import Blueprint, jsonify
from utils.data_loader import load_data
from utils.data_processor import get_gender_distribution

gender_service = Blueprint("gender_service", __name__)

@gender_service.route("/gender", methods=["GET"])
def gender_distribution():
    """
    Ruta para obtener la distribución de género.
    """
    try:
        # Cargar y procesar los datos
        data = load_data("data/matricula_2024B.csv")
        filtered_data = data  # Aquí puedes aplicar filtros basados en el periodo si es necesario
        result = {"gender_distribution": get_gender_distribution(filtered_data)}
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
