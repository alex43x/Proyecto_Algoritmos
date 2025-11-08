from .pool import conectar
    # Inserta un nuevo registro en la tabla 'grupos'
def insert_grupo(nombreGrupo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO grupos (nombreGrupo)
        VALUES (?)
    """, (nombreGrupo,))
    conn.commit()
    conn.close()
    # Recupera todos los registros de la tabla 'grupos'     
def get_grupo():
    conn= conectar()
    cursor=conn.cursor()
    cursor.execute("SELECT idGrupo, nombreGrupo FROM grupos")
    grupos=cursor.fetchall()
    conn.close()
    return grupos
