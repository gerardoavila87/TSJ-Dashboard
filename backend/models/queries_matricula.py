# backend/models/queries.py
from sqlalchemy.sql import text
from app import db

def get_total_query(ids, unidad, periodo):
    # Construcción de la consulta SQL
    query = """
        SELECT COUNT(fm.idMatricula) AS estudiantes
        FROM FactMatricula fm
        JOIN DimFecha df ON df.idFecha = fm.idFechaInicio
    """
    params = {"periodo": periodo}

    if unidad:
        query += "JOIN DimUnidades du ON du.idUnidad = fm.idUnidadReal\n"
        params["unidad"] = unidad

    if ids:
        query += """
            WHERE fm.idFechaInicio IN :ids
            AND (fm.idFechaTermino IS NULL 
                 OR fm.idFechaTermino > (
                     SELECT MAX(idFecha)
                     FROM DimFecha 
                     WHERE idFecha IN :ids
                 ))
        """
        params["ids"] = tuple(ids)
    else:
        query += "WHERE fm.idFechaTermino IS NULL\n"

    query += "AND df.periodo = :periodo\n"

    if unidad:
        query += "AND du.nombre = :unidad\n"

    # Ejecutar la consulta
    result = db.session.execute(text(query), params)
    return result.fetchone()[0]  # Devuelve el número total de estudiantes

