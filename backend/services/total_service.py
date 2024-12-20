from flask import Blueprint, jsonify, Response
import json
from utils.data_loader import load_data
from utils.data_processor import get_total_students
from utils.data_processor import get_gender_distribution
from utils.data_processor import get_mode_distribution
from utils.data_processor import get_status_distribution
from utils.data_processor import get_unidad_distribution
from utils.data_processor import get_procedencia_distribution
from utils.data_processor import get_carrera_distribution

# Aquí están todos los endpoinds que sirven la información, implementando la 
# recuperción de errores
total_service = Blueprint("total_service", __name__)
@total_service.route("/total", methods=["GET"])
def total_students():
    try:
        result = {"total_students": get_total_students(load_data("data/matricula_2024B.csv"))}
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
       
gender_service = Blueprint("gender_service", __name__)
@gender_service.route("/gender", methods=["GET"])
def gender_distribution():
    try:
        result = {"gender_distribution": get_gender_distribution(load_data("data/matricula_2024B.csv"))}
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
mode_service = Blueprint("mode_service", __name__)
@mode_service.route("/mode", methods=["GET"])
def mode_distribution():
    try:
        result = {"mode_distribution": get_mode_distribution(load_data("data/matricula_2024B.csv"))}
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
status_service = Blueprint("status_service", __name__)
@status_service.route("/status", methods=["GET"])
def status_distribution():
    try:
        result = {"status_distribution": get_status_distribution(load_data("data/matricula_2024B.csv"))}
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
unidad_service = Blueprint("unidad_service", __name__)
@unidad_service.route("/unidad", methods=["GET"])
def unidad_distribution():
    try:
        result = {"unidad_distribution": get_unidad_distribution(load_data("data/matricula_2024B.csv"))}
        return Response(
                    json.dumps(result, ensure_ascii=False),
                    content_type="application/json",
                    status=200
                )  
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
procedencia_service = Blueprint("procedencia_service", __name__)
@procedencia_service.route("/procedencia", methods=["GET"])
def procedencia_distribution():
    try:
        result = {"procedencia_distribution": get_procedencia_distribution(load_data("data/matricula_2024B.csv"))}
        return Response(
            json.dumps(result, ensure_ascii=False),
            content_type="application/json",
            status=200
        )    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
carrera_service = Blueprint("carrera_service", __name__)
@carrera_service.route("/carrera", methods=["GET"])
def carrera_distribution():
    try:
        result = {"carrera_distribution": get_carrera_distribution(load_data("data/matricula_2024B.csv"))}
        return jsonify(result), 200
   
    except Exception as e:
        return jsonify({"error": str(e)}), 500