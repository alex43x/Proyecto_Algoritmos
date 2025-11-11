from controllers.pool import conectar
from datetime import datetime
def InformeUno(fecha):
    """
    Devuelve una lista de tuplas con los partidos a disputarse en una fecha dada.
    Cada tupla incluye:
    (idPartido, equipo1, equipo2, jornada, fase, hora)
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            p.idPartido,
            e1.pais AS equipo1,
            e2.pais AS equipo2,
            p.jornada,
            p.hora
        FROM partido p
        JOIN equipos e1 ON p.identificadorEquipoUno = e1.identificador
        JOIN equipos e2 ON p.identificadorEquipoDos = e2.identificador
        WHERE p.fecha = ?
        ORDER BY p.hora
    """, (fecha,))

    resultados = []
    for idPartido, equipo1, equipo2, jornada, hora in cursor.fetchall():
        if jornada in (1, 2, 3):
            fase = "Fase de grupos"
        elif jornada == 4:
            fase = "Octavos de final"
        elif jornada == 5:
            fase = "Cuartos de final"
        elif jornada == 6:
            fase = "Semifinal"
        elif jornada == 7:
            fase = "Tercer puesto"
        elif jornada == 8:
            fase = "Final"
        resultados.append((idPartido, equipo1, equipo2, jornada, fase, hora))

    conn.close()
    return resultados

def InformeTres(equipo_nombre, fecha):
    """
    Informe 3:
    Cuadro de resultados para un equipo dado, incluyendo todos sus partidos
    y su posición final (fase alcanzada) a la conclusión del torneo.

    Retorna:
        (equipo_nombre, fecha, lista_partidos, estado_final)

        lista_partidos = [
            (fecha_partido, fase, equipo1, goles1, equipo2, goles2)
            ...
        ]
    """

    conn = conectar()
    cursor = conn.cursor()

    # Obtener identificador e idGrupo del equipo 
    cursor.execute("""
        SELECT identificador, idGrupo 
        FROM equipos 
        WHERE pais = ?;
    """, (equipo_nombre,))
    id_equipo, grupo = cursor.fetchone()

    # Obtener todos los partidos jugados por el equipo 
    cursor.execute("""
        SELECT 
            p.fecha,
            p.jornada,
            e1.pais AS equipo_uno,
            e2.pais AS equipo_dos,
            p.golesEquipoUno,
            p.golesEquipoDos
        FROM partido p
        JOIN equipos e1 ON e1.identificador = p.identificadorEquipoUno
        JOIN equipos e2 ON e2.identificador = p.identificadorEquipoDos
        WHERE (p.identificadorEquipoUno = ? OR p.identificadorEquipoDos = ?)
        AND p.fecha <= ?
        ORDER BY p.jornada ASC, p.fecha ASC;
    """, (id_equipo, id_equipo, fecha))

    partidos_raw = cursor.fetchall()

    # Si no tiene partidos, retorno vacío 
    if not partidos_raw:
        conn.close()
        return (equipo_nombre, fecha, [], "Sin partidos disputados")

    lista_partidos = []
    ultima_jornada = 1

    # Asignar fase según jornada (sin diccionario) 
    for p in partidos_raw:
        fecha_p, jornada, equipo1, equipo2, goles1, goles2 = p

        if jornada in (1, 2, 3):
            fase = "Fase de Grupos"
        elif jornada == 4:
            fase = "Octavos de Final"
        elif jornada == 5:
            fase = "Cuartos de Final"
        elif jornada == 6:
            fase = "Semifinal"
        elif jornada == 7:
            fase = "Tercer Puesto"
        elif jornada == 8:
            fase = "Final"

        lista_partidos.append((fecha_p, fase, equipo1, goles1, equipo2, goles2))
        ultima_jornada = max(ultima_jornada, jornada)

    # Determinar estado final según última jornada disputada 
    if ultima_jornada <= 3:
        estado_final = "Eliminado en Fase de Grupos"
    elif ultima_jornada == 4:
        estado_final = "Eliminado en Octavos de Final"
    elif ultima_jornada == 5:
        estado_final = "Eliminado en Cuartos de Final"
    elif ultima_jornada == 6:
        estado_final = "Eliminado en Semifinal"
    elif ultima_jornada == 7:
        estado_final = "Partido por Tercer Puesto"
    elif ultima_jornada == 8:
        # Si jugó la jornada 8, verificamos si ganó o perdió la final
        ultimo = lista_partidos[-1]
        _, _, eq1, g1, eq2, g2 = ultimo
        ganador = eq1 if g1 > g2 else eq2
        estado_final = "Campeón" if ganador == equipo_nombre else "Subcampeón"
    else:
        estado_final = "Participación desconocida"

    conn.close()
    return (equipo_nombre, fecha, lista_partidos, estado_final)

def InformeCuatro(grupo_nombre, fecha):
    """
    Informe 4:
    Devuelve todos los partidos jugados por los equipos de un grupo dado
    hasta una fecha determinada.

    Retorna una tupla:
        (grupo_nombre, fecha, lista_partidos)

        lista_partidos = [
            (fecha, hora, equipo1, goles1, equipo2, goles2, jornada, fase)
            ...
        ]
    """

    conn = conectar()
    cursor = conn.cursor()

    # Obtener el ID del grupo
    cursor.execute("""
        SELECT idGrupo
        FROM grupos
        WHERE nombreGrupo = ?;
    """, (grupo_nombre,))
    fila = cursor.fetchone()
    if not fila:
        conn.close()
        return (grupo_nombre, fecha, [])

    id_grupo = fila[0]

    # Obtener todos los equipos de ese grupo
    cursor.execute("""
        SELECT identificador
        FROM equipos
        WHERE grupo = ?;
    """, (id_grupo,))
    equipos = [r[0] for r in cursor.fetchall()]

    if not equipos:
        conn.close()
        return (grupo_nombre, fecha, [])

    # Obtener los partidos donde ambos equipos pertenecen al grupo
    cursor.execute(f"""
        SELECT
            p.fecha,
            p.hora,
            e1.pais AS equipo1,
            e2.pais AS equipo2,
            p.golesEquipoUno,
            p.golesEquipoDos,
            p.jornada
        FROM partido p
        JOIN equipos e1 ON e1.identificador = p.identificadorEquipoUno
        JOIN equipos e2 ON e2.identificador = p.identificadorEquipoDos
        WHERE p.fecha <= ?
        AND p.identificadorEquipoUno IN ({','.join('?' * len(equipos))})
        AND p.identificadorEquipoDos IN ({','.join('?' * len(equipos))})
        ORDER BY p.jornada, p.fecha, p.hora;
    """, (fecha, *equipos, *equipos))

    partidos = cursor.fetchall()

    lista_partidos = []

    # Asignar fase según jornada (como en Informe 1)
    for fecha_p, hora, equipo1, equipo2, g1, g2, jornada in partidos:
        if jornada in (1, 2, 3):
            fase = "Fase de grupos"
        elif jornada == 4:
            fase = "Octavos de final"
        elif jornada == 5:
            fase = "Cuartos de final"
        elif jornada == 6:
            fase = "Semifinal"
        elif jornada == 7:
            fase = "Tercer puesto"
        elif jornada == 8:
            fase = "Final"
        else:
            fase = "Desconocida"

        lista_partidos.append((fecha_p, hora, equipo1, g1, equipo2, g2, jornada, fase))

    conn.close()
    return (grupo_nombre, fecha, lista_partidos)


def InformeCinco(fecha):
    """
    Informe 5:
    Genera la tabla de posiciones para todos los grupos (fase de grupos),
    considerando solo los partidos jugados hasta la fecha indicada.

    Calcula para cada equipo:
        PJ, PG, PE, PP, GF, GC, DG, Pts.
    Retorna una tupla con:
        ("Informe 5 - Tabla de posiciones hasta <fecha>", lista_por_grupos)
    """

    conn = conectar()
    cursor = conn.cursor()

    # Obtener grupos A-F en orden fijo
    cursor.execute("""
        SELECT identificador, nombreGrupo 
        FROM grupos 
        WHERE nombreGrupo IN ('A','B','C','D','E','F')
        ORDER BY nombreGrupo ASC;
    """)
    grupos = cursor.fetchall()

    resultados_finales = []

    # Función auxiliar para ordenar 
    def criterio_orden(equipo):
        # equipo = (pais, PJ, PG, PE, PP, GF, GC, DG, Pts)
        # Retorna una tupla usada como clave de ordenamiento (Pts, DG, GF)
        return (equipo[8], equipo[7], equipo[5])

    for id_grupo, nombre_grupo in grupos:
        # Equipos del grupo
        cursor.execute("""
            SELECT identificador, pais
            FROM equipos
            WHERE identificadorGrupo = ?
            ORDER BY pais ASC;
        """, (id_grupo,))
        equipos = cursor.fetchall()

        tabla = []

        for id_equipo, pais in equipos:
            PJ = PG = PE = PP = GF = GC = 0

            # Partidos como equipo uno
            cursor.execute("""
                SELECT golesEquipoUno, golesEquipoDos
                FROM partido
                WHERE identificadorEquipoUno = ?
                  AND jornada IN (1,2,3)
                  AND fecha <= ?;
            """, (id_equipo, fecha))
            partidos_uno = cursor.fetchall()

            for gf, gc in partidos_uno:
                PJ += 1
                GF += gf
                GC += gc
                if gf > gc:
                    PG += 1
                elif gf == gc:
                    PE += 1
                else:
                    PP += 1

            # Partidos como equipo dos
            cursor.execute("""
                SELECT golesEquipoDos, golesEquipoUno
                FROM partido
                WHERE identificadorEquipoDos = ?
                  AND jornada IN (1,2,3)
                  AND fecha <= ?;
            """, (id_equipo, fecha))
            partidos_dos = cursor.fetchall()

            for gf, gc in partidos_dos:
                PJ += 1
                GF += gf
                GC += gc
                if gf > gc:
                    PG += 1
                elif gf == gc:
                    PE += 1
                else:
                    PP += 1

            DG = GF - GC
            Pts = PG * 3 + PE

            tabla.append((pais, PJ, PG, PE, PP, GF, GC, DG, Pts))

        # Ordenar tabla usando la función auxiliar
        tabla.sort(key=criterio_orden, reverse=True)

        resultados_finales.append((fecha, nombre_grupo, tabla))

    conn.close()

    return (resultados_finales)


