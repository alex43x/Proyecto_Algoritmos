from .pool import conectar
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

# Obtener los registros y mostrarlos en un único print
torneos = get_torneos()
print("TORNEOS REGISTRADOS:\n" + "\n".join([
    f"ID: {t[0]} | Nombre: {t[1]} | Sede: {t[2]} | Inicio: {t[3]} | Fin: {t[4]}"
    for t in torneos
]))
