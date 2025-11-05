from controllers.pool import conectar

def insert_torneo(nombreTorneo, sede, fechaDeInicio, fechaDeFin):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO torneo (nombreTorneo, sede, fechaDeInicio, fechaDeFin)
        VALUES (?, ?, ?, ?)
    """, (nombreTorneo, sede, fechaDeInicio, fechaDeFin))
    conn.commit()
    conn.close()

def get_torneos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombreTorneo, sede, fechaDeInicio, fechaDeFin FROM torneo")
    torneos = cursor.fetchall()
    conn.close()
    return torneos

