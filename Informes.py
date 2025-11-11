from controllers.pool import conectar
from datetime import datetime

def InformeUno(fecha):
    """
    Devuelve una lista de tuplas con los partidos a disputarse en una fecha dada.
    Cada tupla incluye:
    (idPartido, fecha, equipo1, equipo2, jornada, fase, hora)
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            p.idPartido,
            p.fecha,
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
    for idPartido, fecha_p, equipo1, equipo2, jornada, hora in cursor.fetchall():

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

        resultados.append((idPartido, fecha_p, equipo1, equipo2, jornada, fase, hora))

    conn.close()
    return resultados

def InformeDos(grupo_nombre, fecha_limite):
    """
    Informe 2:
    Devuelve la tabla de posiciones para un grupo dado (A-F),
    considerando solo partidos de fase de grupos (jornadas 1–3)
    jugados hasta una fecha límite.

    Retorna:
        (grupo_nombre, fecha_limite, tabla)

    tabla = [
        (pais, PJ, PG, PE, PP, GF, GC, DG, Pts)
    ]
    """

    conn = conectar()
    cursor = conn.cursor()

    # Obtener ID del grupo
    cursor.execute("""
        SELECT idGrupo
        FROM grupos
        WHERE nombreGrupo = ?;
    """, (grupo_nombre,))
    fila = cursor.fetchone()

    if not fila:
        conn.close()
        return (grupo_nombre, fecha_limite, [])

    id_grupo = fila[0]

    # Obtener equipos del grupo
    cursor.execute("""
        SELECT identificador, pais
        FROM equipos
        WHERE grupo = ?
        ORDER BY pais ASC;
    """, (id_grupo,))
    equipos = cursor.fetchall()

    if not equipos:
        conn.close()
        return (grupo_nombre, fecha_limite, [])

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
        """, (id_equipo, fecha_limite))
        partidos1 = cursor.fetchall()

        for gf, gc in partidos1:
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
        """, (id_equipo, fecha_limite))
        partidos2 = cursor.fetchall()

        for gf, gc in partidos2:
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

    conn.close()
    # tabla = [(pais, PJ, PG, PE, PP, GF, GC, DG, Pts)]
    # Orden requerido: Pts → DG → GF
    def criterio_orden(fila):
        pais, PJ, PG, PE, PP, GF, GC, DG, Pts = fila
        return (Pts, DG, GF)

    tabla.sort(key=criterio_orden, reverse=True)

    return (grupo_nombre, fecha_limite, tabla)
def InformeTres(equipo_nombre, fecha):
    """
    Informe 3:
    Cuadro de resultados para un equipo dado hasta una fecha dada,
    e indica su estado final si el torneo concluyó.

    Retorna:
        (equipo_nombre, fecha, lista_partidos, estado_final)

        lista_partidos = [
            (fecha_partido, fase, equipo1, goles1, equipo2, goles2)
        ]
    """

    conn = conectar()
    cursor = conn.cursor()

    # Obtener identificador del equipo
    cursor.execute("""
        SELECT identificador, grupo 
        FROM equipos 
        WHERE pais = ?;
    """, (equipo_nombre,))
    fila = cursor.fetchone()

    if not fila:
        conn.close()
        return (equipo_nombre, fecha, [], "Equipo no encontrado")

    id_equipo = fila[0]

    # PARTIDOS HASTA LA FECHA DADA
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

    if not partidos_raw:
        conn.close()
        return (equipo_nombre, fecha, [], "Sin partidos disputados hasta esa fecha")

    lista_partidos = []
    ultima_jornada = 1

    # RECORRER PARTIDOS, ASIGNAR FASE, ARMAR LISTA
    for fecha_p, jornada, eq1, eq2, g1, g2 in partidos_raw:

        # Fase según jornada
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
        else:
            fase = "Desconocida"

        lista_partidos.append((fecha_p, fase, eq1, g1, eq2, g2))

        if jornada > ultima_jornada:
            ultima_jornada = jornada

    # ESTADO FINAL DEL EQUIPO SEGÚN ÚLTIMA JORNADA JUGADA HASTA ESA FECHA
    if ultima_jornada <= 3:
        estado_final = "En Fase de Grupos"
    elif ultima_jornada == 4:
        estado_final = "En Octavos de Final"
    elif ultima_jornada == 5:
        estado_final = "En Cuartos de Final"
    elif ultima_jornada == 6:
        estado_final = "En Semifinal"
    elif ultima_jornada == 7:
        estado_final = "En Tercer Puesto"
    elif ultima_jornada == 8:
        # Si ya jugó la final antes de esa fecha, evaluar ganador
        ult = lista_partidos[-1]
        _, _, eq1f, g1f, eq2f, g2f = ult
        ganador = eq1f if g1f > g2f else eq2f
        estado_final = "Campeón" if ganador == equipo_nombre else "Subcampeón"
    else:
        estado_final = "Participación desconocida"

    conn.close()

    return (equipo_nombre, fecha, lista_partidos, estado_final)

def InformeCuatro(equipo_nombre, fecha_limite):
    """
    Informe 4:
    Devuelve el PRÓXIMO partido que debe disputar un equipo dado
    después de una fecha dada.

    Retorna:
        (equipo_nombre, fecha_limite, partido)

    donde partido =
        (fecha, hora, equipo1, equipo2, jornada, fase)
    """

    conn = conectar()
    cursor = conn.cursor()

    # Obtener identificador del equipo
    cursor.execute("""
        SELECT identificador
        FROM equipos
        WHERE pais = ?;
    """, (equipo_nombre,))
    fila = cursor.fetchone()

    if not fila:
        conn.close()
        return (equipo_nombre, fecha_limite, None)

    id_equipo = fila[0]

    # Buscar el PRÓXIMO partido luego de la fecha dada
    cursor.execute("""
        SELECT
            p.fecha,
            p.hora,
            e1.pais AS equipo1,
            e2.pais AS equipo2,
            p.jornada
        FROM partido p
        JOIN equipos e1 ON e1.identificador = p.identificadorEquipoUno
        JOIN equipos e2 ON e2.identificador = p.identificadorEquipoDos
        WHERE (p.identificadorEquipoUno = ?
               OR p.identificadorEquipoDos = ?)
          AND p.fecha > ?
        ORDER BY p.fecha ASC, p.hora ASC
        LIMIT 1;
    """, (id_equipo, id_equipo, fecha_limite))

    partido = cursor.fetchone()
    conn.close()

    if not partido:
        return (equipo_nombre, fecha_limite, None)

    fecha_p, hora, eq1, eq2, jornada = partido

    # Determinar fase según jornada
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

    return (equipo_nombre, fecha_limite,
            (fecha_p, hora, eq1, eq2, jornada, fase))


def InformeCinco(fecha):
    """
    Informe 5:
    Genera la tabla de posiciones para todos los grupos (A-F),
    considerando solo los partidos hasta la fecha dada.

    Retorna:
        ( [(fecha, grupo, [(pais, PJ, PG, PE, PP, GF, GC, DG, Pts), ... ]), ... ] )
    """

    conn = conectar()
    cursor = conn.cursor()

    # Obtener grupos A–F
    cursor.execute("""
        SELECT idGrupo, nombreGrupo
        FROM grupos
        WHERE nombreGrupo IN ('A','B','C','D','E','F')
        ORDER BY nombreGrupo ASC;
    """)
    grupos = cursor.fetchall()

    resultados_finales = []

    # Clave de ordenamiento
    def criterio_orden(e):
        # e = (pais, PJ, PG, PE, PP, GF, GC, DG, Pts)
        return (e[8], e[7], e[5])  # Pts, DG, GF

    for id_grupo, nombre_grupo in grupos:

        # Obtener equipos de este grupo
        cursor.execute("""
            SELECT identificador, pais
            FROM equipos
            WHERE grupo = ?
            ORDER BY pais ASC;
        """, (id_grupo,))
        equipos = cursor.fetchall()

        tabla = []

        for id_equipo, pais in equipos:

            PJ = PG = PE = PP = GF = GC = 0

            # Como equipo uno
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

            # Como equipo dos
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

        # Orden final
        tabla.sort(key=criterio_orden, reverse=True)

        resultados_finales.append((fecha, nombre_grupo, tabla))

    conn.close()

    return resultados_finales

