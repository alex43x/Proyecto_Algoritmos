from .pool import conectar

def insert_partido(datos):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO partido (
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
