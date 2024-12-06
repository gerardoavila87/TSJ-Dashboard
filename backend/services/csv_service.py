from flask import Blueprint, jsonify, request
from sqlalchemy import create_engine, text
import pandas as pd
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

csv_service = Blueprint("csv_service", __name__)

# Configuración de la base de datos desde las variables de entorno
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DATA_DB_NAME = os.getenv("DATA_DB_NAME")

# Construcción del URL para la conexión a la base de datos
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DATA_DB_NAME}"
engine = create_engine(DATABASE_URL)

@csv_service.route("/generate", methods=["POST"])
def generate_csv():
    try:
        data = request.json
        periodo = data.get("periodo")
        if not periodo:
            return jsonify({"error": "El campo 'periodo' es requerido."}), 400

        # Consulta SQL
        query = text("""
            SELECT de.nocontrol, de.curp, de.lugarNacimiento, de.nombre, de.primerApellido,
                   de.segundoApellido, de.seguro, de.genero, de.celular, de.correo, 
                   de.indigena, dc.clave AS carrera, dm.nombre AS modalidad, 
                   de2.nombre AS estudios, dp.estado AS entidad, dp.municipio, 
                   du.nombre AS nombreUReal, du2.nombre AS nombreUOficial, 
                   dd.nombre AS discapacidad, fm.semestre, fm.estatus AS status
              FROM FactMatricula fm 
              JOIN DimEstudiante de ON de.idEstudiante = fm.idEstudiante
              JOIN DimCarreras dc ON dc.idCarrera = fm.idCarrera 
              JOIN DimModalidades dm ON dm.idModalidad = fm.idModalidad 
         LEFT JOIN DimEstudios de2 ON de2.idEstudio = fm.idEstudio 
         LEFT JOIN DimProcedencia dp ON dp.idProcedencia = fm.idProcedencia 
              JOIN DimUnidades du ON du.idUnidad = fm.idUnidadReal 
              JOIN DimUnidades du2 ON du2.idUnidad = fm.idUnidadOficial 
         LEFT JOIN DimDiscapacidades dd ON dd.IdDiscapacidad = fm.idDiscapacidad 
              JOIN DimFecha df ON df.idFecha = fm.idFechaInicio 
         LEFT JOIN DimFecha df2 ON df2.idFecha = fm.idFechaTermino
             WHERE ISNULL(fm.idFechaTermino)
               AND df.periodo = :periodo
        """)
        with engine.connect() as conn:
            result = conn.execute(query, {"periodo": periodo})
            rows = result.fetchall()

        # Crear un DataFrame
        columns = result.keys()
        df = pd.DataFrame(rows, columns=columns)

        # Crear el directorio "data" si no existe
        output_dir = "data"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Guardar el archivo CSV
        output_path = os.path.join(output_dir, f"matricula_{periodo}.csv")
        df.to_csv(output_path, index=False, encoding="utf-8")

        return jsonify({"message": "CSV generado con éxito.", "path": output_path}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
