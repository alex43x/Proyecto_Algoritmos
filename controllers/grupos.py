from controllers.pool import conectar

def insert_grupo(nombreGrupo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO grupos (nombreGrupo)
        VALUES (?)
    """, (nombreGrupo,))
    conn.commit()
    conn.close()
def get_grupo():
    conn= conectar()
    cursor=conn.cursor()
    cursor.execute("SELECT nombreGrupo FROM grupos")
    grupos=cursor.fetchall()
    conn.close()
    return grupos
