# backend/routes/students.py
from flask import Blueprint, request, jsonify
from models.queries import get_total_query

students_bp = Blueprint('students', __name__)

@students_bp.route('/api/total_students', methods=['GET'])
def total_students():
    ids = request.args.getlist('ids', type=int)
    unidad = request.args.get('unidad')
    periodo = request.args.get('periodo')

    if not periodo:
        periodo = '2024A'

    try:
        total = get_total_query(ids, unidad, periodo)
        return jsonify({"estudiantes": total}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
