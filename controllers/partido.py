from .pool import conectar

def insert_partido(datos):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO partido (
            idPartido, anio, mes, dia, horaDeInicio, minuto, fecha,
            identificadorEquipoUno, identificadorEquipoDos,
            golesEquipoUno, golesEquipoDos,
            tarjetasAmarillasEquipoUno, tarjetasAmarillasEquipoDos,
            tarjetasRojasEquipoUno, tarjetasRojasEquipoDos,
            puntosEquipoUno, puntosEquipoDos, jornada
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, datos)
    conn.commit()
    conn.close()
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
            tarjetasRojasEquipoDos = ?,
            puntosEquipoUno = ?,
            puntosEquipoDos = ?,
        WHERE idPartido = ?
    """, datos)
    conn.commit()
    conn.close()
def get_partido_sin_jugar():
    conn=conectar()
    cursor =conn.cursor()
    cursor.execute("SELECT idPartido, fecha, identificadorEquipoUno, identificadorEquipoDos FROM partido")
    partido=cursor.fetchall()
    conn.close()
    return partido
    #se separa los detalles del partido, primero se carga el evento y su fecha y luego sus detalles
def get_puntos_partido():
    conn=conectar()
    cursor =conn.cursor()
    cursor.execute("SELECT idPartido, fecha, puntosEquipoUno, puntosEquipoDos FROM partido")
    partido=cursor.fetchall()
    conn.close()
    return partido