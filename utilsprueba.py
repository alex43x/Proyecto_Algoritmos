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

from controllers.pool import conectar

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

    # --- Obtener identificador e idGrupo del equipo ---
    cursor.execute("""
        SELECT identificador, idGrupo 
        FROM equipos 
        WHERE pais = ?;
    """, (equipo_nombre,))
    id_equipo, id_grupo = cursor.fetchone()

    # --- Obtener todos los partidos jugados por el equipo ---
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

    # --- Si no tiene partidos, retorno vacío ---
    if not partidos_raw:
        conn.close()
        return (equipo_nombre, fecha, [], "Sin partidos disputados")

    # --- Asignar fase según jornada ---
    fases = {
        1: "Fase de Grupos",
        2: "Fase de Grupos",
        3: "Fase de Grupos",
        4: "Octavos de Final",
        5: "Cuartos de Final",
        6: "Semifinal",
        7: "Tercer Puesto",
        8: "Final"
    }

    lista_partidos = []
    ultima_jornada = 1
    for p in partidos_raw:
        fecha_p, jornada, equipo1, equipo2, goles1, goles2 = p
        fase = fases.get(jornada, "Fase de Grupos")
        lista_partidos.append((fecha_p, fase, equipo1, goles1, equipo2, goles2))
        ultima_jornada = max(ultima_jornada, jornada)

    # --- Determinar estado final según última jornada disputada ---
    estado_final = {
        1: "Eliminado en Fase de Grupos",
        2: "Eliminado en Fase de Grupos",
        3: "Eliminado en Fase de Grupos",
        4: "Eliminado en Octavos de Final",
        5: "Eliminado en Cuartos de Final",
        6: "Eliminado en Semifinal",
        7: "Partido por Tercer Puesto",
        8: "Finalista"
    }.get(ultima_jornada, "Participación desconocida")
    # --- Si jugó la jornada 8, verificamos si ganó o perdió la final ---
    if ultima_jornada == 8:
        ultimo = lista_partidos[-1]
        _, _, eq1, g1, eq2, g2 = ultimo
        ganador = eq1 if g1 > g2 else eq2
        estado_final = "Campeón" if ganador == equipo_nombre else "Subcampeón"

    conn.close()
    return (equipo_nombre, fecha, lista_partidos, estado_final)

def InformeCuatro(equipo_nombre, fecha):
    """
    Informe 4:
    Muestra el próximo partido a disputar por un equipo dado, para una fecha dada.

    Parámetros:
        equipo_nombre (str): Nombre del país (ejemplo: 'Argentina')
        fecha (str): Fecha en formato 'YYYY-MM-DD'

    Retorna:
        Tupla con:
        (fecha_partido, equipo_uno, equipo_dos, hora, jornada, fase)
    """

    conn = conectar()
    cursor = conn.cursor()

    # Obtener el identificador del equipo
    cursor.execute("""
        SELECT identificador 
        FROM equipos 
        WHERE pais = ?;
    """, (equipo_nombre,))
    id_equipo = cursor.fetchone()[0]

    # Buscar el próximo partido posterior a la fecha indicada
    cursor.execute("""
        SELECT 
            p.fecha,
            p.horaDeInicio,
            p.minuto,
            e1.pais AS equipo_uno,
            e2.pais AS equipo_dos,
            p.jornada
        FROM partido p
        JOIN equipos e1 ON e1.identificador = p.identificadorEquipoUno
        JOIN equipos e2 ON e2.identificador = p.identificadorEquipoDos
        WHERE (p.identificadorEquipoUno = ? OR p.identificadorEquipoDos = ?)
          AND p.fecha > ?
        ORDER BY p.fecha ASC, p.horaDeInicio ASC
        LIMIT 1;
    """, (id_equipo, id_equipo, fecha))

    partido = cursor.fetchone()
    conn.close()

    if not partido:
        return None  # No hay próximos partidos

    fecha_partido, hora, minuto, equipo1, equipo2, jornada = partido

    # Determinar fase según jornada
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

    # Retornar tupla para interfaz
    return (
        fecha_partido.strftime("%Y-%m-%d"),
        f"{hora:02d}:{minuto:02d}",
        equipo1,
        equipo2,
        jornada,
        fase
    )

def InformeCinco():
    """
    Informe 5:
    Genera la tabla de posiciones para todos los grupos (fase de grupos).

    Calcula para cada equipo:
        PJ, PG, PE, PP, GF, GC, DG, Pts.
    Retorna una lista de tuplas organizada por grupo.
    """

    conn = conectar()
    cursor = conn.cursor()

    # Obtener todos los grupos existentes
    cursor.execute("SELECT identificador, nombreGrupo FROM grupos;")
    grupos = cursor.fetchall()

    resultados_finales = []

    # Función auxiliar para definir el criterio de ordenamiento
    def criterio_orden(equipo):
        # equipo = (pais, PJ, PG, PE, PP, GF, GC, DG, Pts)
        # Retorna una tupla para ordenar por Pts, DG y GF en orden descendente
        return (equipo[8], equipo[7], equipo[5])

    for id_grupo, nombre_grupo in grupos:
        # Obtener equipos del grupo
        cursor.execute("""
            SELECT identificador, pais
            FROM equipos
            WHERE identificadorGrupo = ?;
        """, (id_grupo,))
        equipos = cursor.fetchall()

        tabla = []

        for id_equipo, pais in equipos:
            # Estadísticas iniciales
            PJ = PG = PE = PP = GF = GC = 0

            # Partidos donde fue equipo uno
            cursor.execute("""
                SELECT golesEquipoUno, golesEquipoDos
                FROM partido
                WHERE identificadorEquipoUno = ? AND jornada IN (1,2,3);
            """, (id_equipo,))
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

            # Partidos donde fue equipo dos
            cursor.execute("""
                SELECT golesEquipoDos, golesEquipoUno
                FROM partido
                WHERE identificadorEquipoDos = ? AND jornada IN (1,2,3);
            """, (id_equipo,))
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
            Pts = PG * 3 + PE * 1

            tabla.append((pais, PJ, PG, PE, PP, GF, GC, DG, Pts))

        # Ordenar la tabla usando la función auxiliar (en reversa)
        tabla.sort(key=criterio_orden, reverse=True)

        resultados_finales.append((nombre_grupo, tabla))

    conn.close()
    return resultados_finales
