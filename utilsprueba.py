from controllers.pool import conectar
from datetime import datetime

from controllers.pool import conectar

def tabla_posiciones_por_fecha(fecha):
    """
    Genera la tabla de posiciones considerando partidos jugados hasta una fecha dada.
    Mantiene el formato del Informe 5 y calcula:
    PJ, PG, PE, PP, GF, GC, DG, Pts.
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            e.identificador,
            e.pais,
            e.idGrupo,
            -- Partidos jugados
            COUNT(p.idPartido) AS partidos_jugados,
            -- Partidos ganados
            SUM(
                CASE 
                    WHEN (p.identificadorEquipoUno = e.identificador AND p.golesEquipoUno > p.golesEquipoDos)
                      OR (p.identificadorEquipoDos = e.identificador AND p.golesEquipoDos > p.golesEquipoUno)
                    THEN 1 ELSE 0 END
            ) AS ganados,
            -- Partidos empatados
            SUM(
                CASE WHEN p.golesEquipoUno = p.golesEquipoDos THEN 1 ELSE 0 END
            ) AS empatados,
            -- Partidos perdidos
            SUM(
                CASE 
                    WHEN (p.identificadorEquipoUno = e.identificador AND p.golesEquipoUno < p.golesEquipoDos)
                      OR (p.identificadorEquipoDos = e.identificador AND p.golesEquipoDos < p.golesEquipoUno)
                    THEN 1 ELSE 0 END
            ) AS perdidos,
            -- Goles a favor
            SUM(
                CASE 
                    WHEN p.identificadorEquipoUno = e.identificador THEN p.golesEquipoUno
                    WHEN p.identificadorEquipoDos = e.identificador THEN p.golesEquipoDos
                    ELSE 0 END
            ) AS goles_favor,
            -- Goles en contra
            SUM(
                CASE 
                    WHEN p.identificadorEquipoUno = e.identificador THEN p.golesEquipoDos
                    WHEN p.identificadorEquipoDos = e.identificador THEN p.golesEquipoUno
                    ELSE 0 END
            ) AS goles_contra,
            -- Diferencia de goles
            SUM(
                CASE 
                    WHEN p.identificadorEquipoUno = e.identificador THEN p.golesEquipoUno - p.golesEquipoDos
                    WHEN p.identificadorEquipoDos = e.identificador THEN p.golesEquipoDos - p.golesEquipoUno
                    ELSE 0 END
            ) AS diferencia_goles,
            -- Puntos
            SUM(
                CASE 
                    WHEN (p.identificadorEquipoUno = e.identificador AND p.golesEquipoUno > p.golesEquipoDos)
                      OR (p.identificadorEquipoDos = e.identificador AND p.golesEquipoDos > p.golesEquipoUno)
                    THEN 3
                    WHEN p.golesEquipoUno = p.golesEquipoDos THEN 1
                    ELSE 0 END
            ) AS puntos
        FROM equipos e
        LEFT JOIN partido p
            ON (e.identificador = p.identificadorEquipoUno OR e.identificador = p.identificadorEquipoDos)
            AND p.fecha <= ?
        GROUP BY e.identificador, e.pais, e.idGrupo
        ORDER BY e.idGrupo, puntos DESC, diferencia_goles DESC, goles_favor DESC;
    """, (fecha,))

    tabla = cursor.fetchall()
    conn.close()

    # Agrupar equipos por grupo (igual que en el código original)
    grupos = {}
    for fila in tabla:
        idGrupo = fila[2]
        if idGrupo not in grupos:
            grupos[idGrupo] = []
        grupos[idGrupo].append(fila)

    # --- Mostrar tabla en consola agrupada por grupo ---
    print(f"\nTABLA DE POSICIONES HASTA LA FECHA {fecha}")
    print("-" * 90)
    for idGrupo in grupos:
        print(f"\nGRUPO {idGrupo}")
        print(f"{'Identificador':<15}{'Pais':<15}{'PJ':<5}{'PG':<5}{'PE':<5}{'PP':<5}{'GF':<5}{'GC':<5}{'DG':<5}{'Pts':<5}")
        print("-" * 85)
        for fila in grupos[idGrupo]:
            print(f"{fila[0]:<15}{fila[1]:<15}{fila[3]:<5}{fila[4]:<5}{fila[5]:<5}{fila[6]:<5}{fila[7]:<5}{fila[8]:<5}{fila[9]:<5}{fila[10]:<5}")

    # Retornar lista de tuplas con todos los datos
    return tabla


def informe_partidos_por_fecha(fecha):
    """
    Informe 1:
    Devuelve todos los partidos a disputarse en una fecha dada,
    mostrando equipos, horario, estadio y fase.
    
    Parámetro:
        fecha (str): en formato 'YYYY-MM-DD'
    
    Retorna:
        Lista de tuplas con:
        (equipo_uno, equipo_dos, hora, fase, estadio)
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            e1.pais AS equipo_uno,
            e2.pais AS equipo_dos,
            p.hora,
            p.fase,
            p.estadio
        FROM partido p
        INNER JOIN equipos e1 ON e1.identificador = p.identificadorEquipoUno
        INNER JOIN equipos e2 ON e2.identificador = p.identificadorEquipoDos
        WHERE p.fecha = ?
        ORDER BY p.hora ASC;
    """, (fecha,))

    partidos = cursor.fetchall()
    conn.close()

    # --- Mostrar por consola (solo para depuración o texto simple) ---
    print(f"\nINFORME 1 - PARTIDOS DEL {fecha}")
    print("-" * 70)
    if not partidos:
        print("No hay partidos programados para esa fecha.")
    else:
        for p in partidos:
            print(f"{p[0]} vs {p[1]} - {p[2]} - {p[3]} - {p[4]}")

    return partidos


def informe_equipo(equipo_nombre, fecha):
    """
    Informe 3:
    Muestra todos los partidos jugados por un equipo dado hasta una fecha dada
    y determina si está clasificado a la siguiente fase.
    """

    conn = conectar()
    cursor = conn.cursor()

    # Obtener identificador y grupo del equipo
    cursor.execute("""
        SELECT identificador, idGrupo 
        FROM equipos 
        WHERE pais = ?;
    """, (equipo_nombre,))
    id_equipo, id_grupo = cursor.fetchone()

    # Obtener los partidos del equipo hasta la fecha dada
    cursor.execute("""
        SELECT 
            p.fecha,
            e1.pais AS equipo_uno,
            e2.pais AS equipo_dos,
            p.golesEquipoUno,
            p.golesEquipoDos
        FROM partido p
        JOIN equipos e1 ON e1.identificador = p.identificadorEquipoUno
        JOIN equipos e2 ON e2.identificador = p.identificadorEquipoDos
        WHERE (p.identificadorEquipoUno = ? OR p.identificadorEquipoDos = ?)
        AND p.fecha <= ?
        ORDER BY p.fecha ASC;
    """, (id_equipo, id_equipo, fecha))

    partidos = cursor.fetchall()

    # Encabezado del informe
    print(f"\nInforme 3")
    print(f"Equipo: {equipo_nombre}")
    print(f"Fecha de emisión del informe: {fecha}\n")

    # Mostrar los partidos jugados
    for p in partidos:
        fecha_partido, equipo1, equipo2, goles1, goles2 = p
        fecha_str = fecha_partido.strftime("%d/%m/%Y")
        fase = "Fase de Grupos"  # fijo por ahora, se puede adaptar luego

        if equipo1 == equipo_nombre:
            print(f"{fecha_str} - {fase} - {equipo1} {goles1} : {equipo2} {goles2}")
        else:
            print(f"{fecha_str} - {fase} - {equipo2} {goles2} : {equipo1} {goles1}")

    # Calcular tabla de posiciones del grupo hasta la fecha
    cursor.execute("""
        SELECT 
            e.identificador,
            e.pais,
            COALESCE(SUM(
                CASE 
                    WHEN (p.identificadorEquipoUno = e.identificador AND p.golesEquipoUno > p.golesEquipoDos)
                      OR (p.identificadorEquipoDos = e.identificador AND p.golesEquipoDos > p.golesEquipoUno)
                    THEN 3
                    WHEN p.golesEquipoUno = p.golesEquipoDos THEN 1
                    ELSE 0 END
            ), 0) AS puntos
        FROM equipos e
        LEFT JOIN partido p
            ON (e.identificador = p.identificadorEquipoUno OR e.identificador = p.identificadorEquipoDos)
            AND p.fecha <= ?
        WHERE e.idGrupo = ?
        GROUP BY e.identificador, e.pais
        ORDER BY puntos DESC;
    """, (fecha, id_grupo))

    tabla_grupo = cursor.fetchall()
    conn.close()

    # Determinar clasificación (2 primeros del grupo)
    clasificados = tabla_grupo[:2]
    clasificado = any(eq[0] == id_equipo for eq in clasificados)

    if clasificado:
        print("\nClasificado a Octavos de Final")
    else:
        print("\nNo clasificado")

    # Retorno para uso interno / interfaz gráfica
    return (
        equipo_nombre,
        fecha,
        partidos,
        "Clasificado a Octavos de Final" if clasificado else "No clasificado"
    )


def informe_proximo_partido(equipo_nombre, fecha):
    """
    Informe 4:
    Muestra el próximo partido a disputar por un equipo dado, para una fecha dada.
    """

    conn = conectar()
    cursor = conn.cursor()

    # Obtener identificador del equipo
    cursor.execute("""
        SELECT identificador FROM equipos WHERE pais = ?;
    """, (equipo_nombre,))
    id_equipo = cursor.fetchone()[0]

    # Buscar el próximo partido después de la fecha indicada
    cursor.execute("""
        SELECT 
            p.fecha,
            p.hora,
            e1.pais AS equipo_uno,
            e2.pais AS equipo_dos,
            p.fase,
            p.estadio
        FROM partido p
        JOIN equipos e1 ON e1.identificador = p.identificadorEquipoUno
        JOIN equipos e2 ON e2.identificador = p.identificadorEquipoDos
        WHERE (p.identificadorEquipoUno = ? OR p.identificadorEquipoDos = ?)
        AND p.fecha > ?
        ORDER BY p.fecha ASC, p.hora ASC
        LIMIT 1;
    """, (id_equipo, id_equipo, fecha))

    partido = cursor.fetchone()
    conn.close()

    fecha_partido, hora, equipo1, equipo2, fase, estadio = partido
    fecha_str = fecha_partido.strftime("%d/%m/%Y")

    # Encabezado
    print(f"\nInforme 4")
    print(f"Equipo: {equipo_nombre}")
    print(f"Fecha : {fecha}\n")

    # Detalle del próximo partido
    print("Copa Mundial Sub-20 de la FIFA Chile 2025™")
    print(f"{fase} · {estadio} · {fecha_str}")
    print()
    if equipo1 == equipo_nombre:
        print(f"{equipo1[:3].upper()}  vs  {equipo2[:3].upper()}   {hora}")
    else:
        print(f"{equipo2[:3].upper()}  vs  {equipo1[:3].upper()}   {hora}")

    # Retorno tipo tupla para informes posteriores
    return (equipo_nombre, fecha, fecha_partido, hora, equipo1, equipo2, fase, estadio)


