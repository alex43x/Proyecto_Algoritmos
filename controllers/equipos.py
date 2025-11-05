from pool import conectar

def insert_equipo(identificador, pais, abreviatura, confederacion, grupo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO equipos (identificador, pais, abreviatura, confederacion, grupo)
        VALUES (?, ?, ?, ?, ?)
    """, (identificador, pais, abreviatura, confederacion, grupo))
    conn.commit()
    conn.close()
def get_equipo():
    conn=conectar()
    cursor=conn.cursor()
    cursor.execute("SELECT identificador, pais, abreviatura, confederacion, grupo FROM equipos")
    equipos=cursor.fetchall()
    conn.close()
    return equipos
    # Insertar equipos de prueba
insert_equipo("A1", "Argentina", "ARG", "CONMEBOL", 1)
insert_equipo("B2", "Francia", "FRA", "UEFA", 2)
insert_equipo("C3", "Japón", "JPN", "AFC", 3)

# Obtener y mostrar en un solo print
equipos = get_equipo()
print("EQUIPOS REGISTRADOS:\n" + "\n".join([
    f" | Identificador: {e[0]} | País: {e[1]} | Abrev: {e[2]} | Confed: {e[3]} | Grupo: {e[4]}"
    for e in equipos
]))