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
            tarjetasRojasEquipoUno, tarjetasRojasEquipoDos,
            jornada, estadio
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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

# ACTUALIZAR FECHA, HORA Y ESTADIO DE UN PARTIDO
def update_partido_fecha(idPartido, fecha, hora, estadio):
    """
    Actualiza la fecha, hora y estadio de un partido.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE partido
        SET fecha = ?, hora = ?, estadio = ?
        WHERE idPartido = ?
    """, (fecha, hora, estadio, idPartido))
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
            p.jornada,
            COALESCE(p.estadio, '') AS estadio
        FROM partido p
        LEFT JOIN equipos e1 ON p.identificadorEquipoUno = e1.identificador
        LEFT JOIN equipos e2 ON p.identificadorEquipoDos = e2.identificador
        ORDER BY p.jornada, p.idPartido;
    """)
    partidos = cursor.fetchall()
    conn.close()
    return partidos