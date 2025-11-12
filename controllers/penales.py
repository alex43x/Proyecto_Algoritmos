from controllers.pool import conectar

# Registrar penales para un partido (inserta o actualiza)
def registrar_penales(id_partido, goles_equipo_uno, goles_equipo_dos):
    try:
        conn = conectar()
        cursor = conn.cursor()

        # Verificar si ya existen penales para este partido
        cursor.execute("SELECT id FROM penales WHERE idPartido = ?;", (id_partido,))
        existe = cursor.fetchone()

        if existe:
            # Actualizar si ya existía
            cursor.execute("""
                UPDATE penales
                SET golesEquipoUno = ?, golesEquipoDos = ?
                WHERE idPartido = ?;
            """, (goles_equipo_uno, goles_equipo_dos, id_partido))
        else:
            # Insertar nuevo registro
            cursor.execute("""
                INSERT INTO penales (idPartido, golesEquipoUno, golesEquipoDos)
                VALUES (?, ?, ?);
            """, (id_partido, goles_equipo_uno, goles_equipo_dos))

        conn.commit()
        print(f"✅ Penales registrados para partido {id_partido}: {goles_equipo_uno}-{goles_equipo_dos}")
    except Exception as e:
        print(f"❌ Error al registrar penales: {e}")
    finally:
        conn.close()


# Obtener penales de un partido
def get_penales_por_partido(id_partido):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT golesEquipoUno, golesEquipoDos
            FROM penales
            WHERE idPartido = ?;
        """, (id_partido,))
        resultado = cursor.fetchone()
        return resultado if resultado else None
    except Exception as e:
        print(f"❌ Error al obtener penales: {e}")
        return None
    finally:
        conn.close()


# Eliminar penales de un partido (por si se necesita reingresar)
def eliminar_penales(id_partido):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM penales WHERE idPartido = ?;", (id_partido,))
        conn.commit()
        print(f"🗑️ Penales eliminados para partido {id_partido}")
    except Exception as e:
        print(f"❌ Error al eliminar penales: {e}")
    finally:
        conn.close()


# Listar todos los penales registrados (para informes o control interno)
def get_todos_los_penales():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id, p.idPartido, e1.pais AS equipo1, e2.pais AS equipo2,
                   p.golesEquipoUno, p.golesEquipoDos
            FROM penales AS p
            JOIN partido AS pa ON p.idPartido = pa.idPartido
            JOIN equipos AS e1 ON pa.identificadorEquipoUno = e1.identificador
            JOIN equipos AS e2 ON pa.identificadorEquipoDos = e2.identificador
            ORDER BY p.id ASC;
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"❌ Error al obtener la lista de penales: {e}")
        return []
    finally:
        conn.close()
