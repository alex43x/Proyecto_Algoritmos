from .pool import conectar

def insert_grupo(nombreGrupo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO grupos (nombreGrupo)
        VALUES (?)
    """, (nombreGrupo,))
    conn.commit()
    conn.close()
