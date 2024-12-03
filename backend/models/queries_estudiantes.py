from sqlalchemy.sql import text
from app import db

def get_estudiantes_query(tipo=None, unidad=None, ids=None, carreras=None, periodo=None):
    # Construcción de la consulta base
    query = "SELECT "

    if unidad:
        query += "du.nombre, "
    if carreras:
        query += "dc.clave, dc.abreviacion, dc.nombre, "

    # Agregar las columnas según el tipo
    if tipo == "genero":
        query += "de.genero, "
    elif tipo == "lugar":
        query += "de.lugarNacimiento, "
    elif tipo == "indigena":
        query += "de.indigena, "

    # Agregar el conteo
    query += "COUNT(fm.idMatricula) as cantidad FROM FactMatricula fm "

    # Unir con otras tablas según sea necesario
    query += """
        JOIN DimEstudiante de ON de.idEstudiante = fm.idEstudiante
        JOIN DimFecha df ON df.idFecha = fm.idFechaInicio
    """
    if unidad or carreras:
        query += "JOIN DimUnidades du ON du.idUnidad = fm.idUnidadReal "
    if carreras:
        query += "JOIN DimCarreras dc ON dc.idCarrera = fm.idCarrera "

    # Condicionales en la cláusula WHERE
    params = {}
    if ids and len(ids) > 0:
        query += """
            WHERE fm.idFechaInicio IN :ids
            AND (fm.idFechaTermino IS NULL OR fm.idFechaTermino > (
                SELECT MAX(idFecha) FROM DimFecha WHERE idFecha IN :ids
            ))
        """
        params["ids"] = tuple(ids)
    else:
        query += "WHERE fm.idFechaTermino IS NULL "

    # Filtrar por periodo
    if periodo:
        query += "AND df.periodo = :periodo "
        params["periodo"] = periodo

    # Filtrar por unidad y carreras
    if unidad and unidad != "unidad":
        query += "AND du.nombre = :unidad "
        params["unidad"] = unidad
    if carreras:
        query += "AND dc.nombre = :carreras "
        params["carreras"] = carreras

    # Agregar agrupamiento según el tipo
    if tipo:
        query += "GROUP BY "
        if tipo == "genero":
            query += "de.genero"
        elif tipo == "lugar":
            query += "de.lugarNacimiento"
        elif tipo == "indigena":
            query += "de.indigena"

        if carreras:
            query += ", dc.idCarrera"
        if unidad:
            query += ", du.idUnidad"

    # Agregar ordenamiento
    query += " ORDER BY "
    if carreras:
        query += "dc.idCarrera, "
    if unidad:
        query += "du.nombre, "

    if tipo:
        if tipo == "genero":
            query += "de.genero"
        elif tipo == "lugar":
            query += "de.lugarNacimiento"
        elif tipo == "indigena":
            query += "de.indigena"

    result = db.session.execute(text(query), params)
    return result.fetchall()