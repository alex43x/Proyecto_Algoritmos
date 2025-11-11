from .pool import conectar

# INSERTAR NUEVO PARTIDO
def insert_partido(datos):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO partido (
            fecha, hora,
            identificadorEquipoUno, identificadorEquipoDos,
            golesEquipoUno, golesEquipoDos,
            tarjetasAmarillasEquipoUno, tarjetasAmarillasEquipoDos,
            tarjetasRojasEquipoUno, tarjetasRojasEquipoDos, jornada
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, datos)
    conn.commit()
    conn.close()
# ACTUALIZAR PARTIDO COMPLETO (GOLES, TARJETAS)
def update_partido(datos):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE partido
        SET golesEquipoUno = ?,
            golesEquipoDos = ?,
            tarjetasAmarillasEquipoUno = ?,
            tarjetasAmarillasEquipoDos = ?,
            tarjetasRojasEquipoUno = ?,
            tarjetasRojasEquipoDos = ?
        WHERE idPartido = ?
    """, datos)
    conn.commit()
    conn.close()
# OBTENER PARTIDOS SIN JUGAR
def get_partido_sin_jugar():
    """Devuelve los partidos (id, fecha, equipos) que aún no se han jugado."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT idPartido, fecha, identificadorEquipoUno, identificadorEquipoDos
        FROM partido
        WHERE golesEquipoUno = 0 AND golesEquipoDos = 0
    """)
    partidos = cursor.fetchall()
    conn.close()
    return partidos
# LISTA CON TODOS LOS PARTIDOS Y SUS DATOS PRINCIPALES
def get_partidos():
    """
    Devuelve una lista de tuplas con todos los campos de la tabla 'partido',
    uniendo con 'equipos' para mostrar los nombres de los equipos.
    Si aún no hay equipos asignados, muestra 'Sin asignar'.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            p.idPartido,
            COALESCE(p.fecha, '') AS fecha,
            COALESCE(p.hora, '') AS hora,
            COALESCE(e1.pais, 'Sin asignar') AS equipo1_nombre,
            COALESCE(e2.pais, 'Sin asignar') AS equipo2_nombre,
            p.identificadorEquipoUno,
            p.identificadorEquipoDos,
            p.golesEquipoUno,
            p.golesEquipoDos,
            p.tarjetasAmarillasEquipoUno,
            p.tarjetasAmarillasEquipoDos,
            p.tarjetasRojasEquipoUno,
            p.tarjetasRojasEquipoDos,
            p.jornada
        FROM partido p
        LEFT JOIN equipos e1 ON p.identificadorEquipoUno = e1.identificador
        LEFT JOIN equipos e2 ON p.identificadorEquipoDos = e2.identificador
        ORDER BY p.jornada, p.idPartido
    """)
    datos = cursor.fetchall()
    conn.close()
    return datos


# ACTUALIZA FECHA Y HORA DE UN PARTIDO
def update_partido_fecha(idPartido, fecha, hora):
    """
    Actualiza la fecha y hora (TEXT) de un partido específico.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE partido 
        SET fecha = ?, hora = ?
        WHERE idPartido = ?
    """, (fecha, hora, idPartido))
    conn.commit()
    conn.close()