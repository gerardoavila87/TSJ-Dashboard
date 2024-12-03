from flask import Blueprint, request, jsonify
from models.queries_matricula import get_total_query
from models.queries_estudiantes import get_estudiantes_query

students_bp = Blueprint('students', __name__)

@students_bp.route('/api/matricula/total', methods=['GET'])
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

@students_bp.route('/api/matricula/genero', methods=['GET'])
def matricula_genero():
    ids = request.args.getlist('ids', type=int)
    unidad = request.args.get('unidad')
    periodo = request.args.get('periodo', '2024A')
    carreras = request.args.get('carreras')
    tipo = 'genero'

    try:
        results = get_estudiantes_query(tipo, unidad, ids, carreras, periodo)
        
        data = [{"genero": row[0], "cantidad": row[1]} for row in results]
        
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
