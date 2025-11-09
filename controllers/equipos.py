from .pool import conectar

def insert_equipo(identificador, pais, abreviatura, confederacion, grupo):
    # Inserta o reemplaza un registro en la tabla 'equipos'
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO equipos (identificador, pais, abreviatura, confederacion, grupo)
        VALUES (?, ?, ?, ?, ?)
    """, (identificador, pais, abreviatura, confederacion, grupo))
    conn.commit()
    conn.close()
def get_equipo():
    # Devuelve todos los registros de la tabla 'equipos'
    conn=conectar()
    cursor=conn.cursor()
    cursor.execute("SELECT identificador, pais, abreviatura, confederacion, grupo FROM equipos")
    equipos=cursor.fetchall()
    conn.close()
    return equipos
    # Insertar equipos de prueba
def get_equipos_por_grupo(idGrupo):
    # Devuelve los equipos pertenecientes a un grupo especifico
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM equipos WHERE grupo = ?", (idGrupo,))
    equipos = cursor.fetchall()
    conn.close()
    return equipos
