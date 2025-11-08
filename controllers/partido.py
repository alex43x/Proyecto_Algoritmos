from .pool import conectar

# INSERTAR NUEVO PARTIDO
def insert_partido(datos):
    """
    Inserta un nuevo partido en la base de datos.
    datos debe ser una tupla con este orden:
    (fecha, hora, idEquipo1, idEquipo2,
     goles1, goles2,
     amarillas1, amarillas2,
     rojas1, rojas2,
     puntos1, puntos2,
     jornada)
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO partido (
            fecha, hora,
            identificadorEquipoUno, identificadorEquipoDos,
            golesEquipoUno, golesEquipoDos,
            tarjetasAmarillasEquipoUno, tarjetasAmarillasEquipoDos,
            tarjetasRojasEquipoUno, tarjetasRojasEquipoDos,
            puntosEquipoUno, puntosEquipoDos, jornada
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, datos)
    conn.commit()
    conn.close()


# ACTUALIZAR PARTIDO COMPLETO (GOLES, TARJETAS, PUNTOS)
def update_partido(datos):
    """
    Actualiza los datos de un partido existente (goles, tarjetas, puntos).
    datos debe ser una tupla con este orden:
    (goles1, goles2, amarillas1, amarillas2, rojas1, rojas2, puntos1, puntos2, idPartido)
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE partido
        SET golesEquipoUno = ?,
            golesEquipoDos = ?,
            tarjetasAmarillasEquipoUno = ?,
            tarjetasAmarillasEquipoDos = ?,
            tarjetasRojasEquipoUno = ?,
            tarjetasRojasEquipoDos = ?,
            puntosEquipoUno = ?,
            puntosEquipoDos = ?
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


# OBTENER PUNTOS DE PARTIDOS
def get_puntos_partido():
    """Devuelve los puntos asignados por partido."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT idPartido, fecha, puntosEquipoUno, puntosEquipoDos
        FROM partido
    """)
    partidos = cursor.fetchall()
    conn.close()
    return partidos

# LISTA CON TODOS LOS PARTIDOS Y SUS DATOS PRINCIPALES
def get_partidos():
    """
    Devuelve una lista de tuplas (idPartido, equipo1, equipo2, jornada, fecha, hora)
    desde la tabla 'partido', uniendo con 'equipos' para mostrar los nombres.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            p.idPartido,
            e1.pais AS equipo1,
            e2.pais AS equipo2,
            p.jornada,
            COALESCE(p.fecha, '') AS fecha,
            COALESCE(p.hora, '') AS hora
        FROM partido p
        JOIN equipos e1 ON p.identificadorEquipoUno = e1.identificador
        JOIN equipos e2 ON p.identificadorEquipoDos = e2.identificador
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