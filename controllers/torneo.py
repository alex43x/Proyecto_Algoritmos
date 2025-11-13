from .pool import conectar
    # Inserta un nuevo torneo en la base de datos 
def insert_torneo(nombreTorneo, sede, fechaDeInicio, fechaDeFin):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO torneo (nombreTorneo, sede, fechaDeInicio, fechaDeFin)
        VALUES (?, ?, ?, ?)
    """, (nombreTorneo, sede, fechaDeInicio, fechaDeFin))
    conn.commit()
    conn.close()
    # Obtiene todos los torneos registrados en la base de datos
def get_torneos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombreTorneo, sede, fechaDeInicio, fechaDeFin FROM torneo")
    torneos = cursor.fetchall()
    conn.close()
    return torneos
