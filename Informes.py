from controllers.pool import conectar
from datetime import datetime
from controllers.penales import get_penales_por_partido

def InformeUno(fecha):
    """
    Devuelve una lista de tuplas con los partidos a disputarse en una fecha dada.
    Cada tupla incluye:
    (idPartido, fecha, equipo1, equipo2, jornada, fase, hora, estadio)
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
            p.hora,
            p.estadio
        FROM partido p
        JOIN equipos e1 ON p.identificadorEquipoUno = e1.identificador
        JOIN equipos e2 ON p.identificadorEquipoDos = e2.identificador
        WHERE p.fecha = ?
        ORDER BY p.hora
    """, (fecha,))

    resultados = []
    for idPartido, fecha_p, equipo1, equipo2, jornada, hora, estadio in cursor.fetchall():

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

        resultados.append((idPartido, fecha_p, equipo1, equipo2, jornada, fase, hora, estadio))

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
    
    # Ordenar tabla
    def criterio_orden(fila):
        pais, PJ, PG, PE, PP, GF, GC, DG, Pts = fila
        return (Pts, DG, GF)

    tabla.sort(key=criterio_orden, reverse=True)
    
    # 🔧 MANTENER ESTRUCTURA ORIGINAL para compatibilidad
    return (grupo_nombre, fecha_limite, tabla)

def InformeTres(equipo_nombre, fecha):
    """
    Informe 3:
    Cuadro de resultados para un equipo dado hasta una fecha dada,
    e indica su estado final si el torneo concluyó.

    Retorna:
        (equipo_nombre, fecha, lista_partidos, estado_final)
    """
    conn = conectar()
    cursor = conn.cursor()

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

    cursor.execute("""
        SELECT 
            p.idPartido,
            p.fecha,
            p.jornada,
            e1.pais AS equipo_uno,
            e2.pais AS equipo_dos,
            p.golesEquipoUno,
            p.golesEquipoDos,
            p.estadio
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

    for id_partido, fecha_p, jornada, eq1, eq2, g1, g2, estadio in partidos_raw:

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

        # 🔧 AGREGADO: Obtener información de penales
        info_penales = ""
        penales1 = penales2 = 0
        
        if jornada >= 4:  # Solo en fase eliminatoria
            penales = get_penales_por_partido(id_partido)
            if penales:
                penales1, penales2 = penales
                if g1 == g2:  # Solo mostrar penales si hubo empate
                    info_penales = f" ({penales1}-{penales2} penales)"

        # 🔧 MODIFICADO: Mantener estructura original de 7 elementos para compatibilidad
        estadio_con_penales = estadio
        if info_penales:
            estadio_con_penales = f"{estadio}{info_penales}"

        lista_partidos.append((fecha_p, fase, eq1, g1, eq2, g2, estadio_con_penales))

        if jornada > ultima_jornada:
            ultima_jornada = jornada

    # Determinar estado final
    estado_final = determinar_estado_final(conn, id_equipo, equipo_nombre, ultima_jornada, partidos_raw)

    conn.close()
    # 🔧 MANTENER ESTRUCTURA ORIGINAL
    return (equipo_nombre, fecha, lista_partidos, estado_final)

def determinar_estado_final(conn, id_equipo, equipo_nombre, ultima_jornada, partidos_raw):
    """
    Determina el estado final del equipo
    """
    cursor = conn.cursor()
    
    if ultima_jornada <= 3:
        return "En Fase de Grupos"
    elif ultima_jornada == 4:
        return "Eliminado en Octavos de Final" if esta_eliminado(conn, id_equipo, 4) else "En Octavos de Final"
    elif ultima_jornada == 5:
        return "Eliminado en Cuartos de Final" if esta_eliminado(conn, id_equipo, 5) else "En Cuartos de Final"
    elif ultima_jornada == 6:
        return "Eliminado en Semifinal" if esta_eliminado(conn, id_equipo, 6) else "En Semifinal"
    elif ultima_jornada == 7:
        # Para tercer puesto
        ultimo_partido = partidos_raw[-1] if partidos_raw else None
        if ultimo_partido:
            id_partido, fecha_p, jornada, eq1, eq2, g1, g2, estadio = ultimo_partido
            if determinar_ganador_partido(id_partido, eq1, g1, eq2, g2) == equipo_nombre:
                return "Tercer Lugar"
            else:
                return "Cuarto Lugar"
        return "En Tercer Puesto"
    elif ultima_jornada == 8:
        # Para la final
        ultimo_partido = partidos_raw[-1] if partidos_raw else None
        if ultimo_partido:
            id_partido, fecha_p, jornada, eq1, eq2, g1, g2, estadio = ultimo_partido
            if determinar_ganador_partido(id_partido, eq1, g1, eq2, g2) == equipo_nombre:
                return "Campeón"
            else:
                return "Subcampeón"
    return "Participación desconocida"

def esta_eliminado(conn, id_equipo, jornada_eliminacion):
    """Determina si un equipo fue eliminado en una jornada específica"""
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT idPartido, identificadorEquipoUno, identificadorEquipoDos, 
               golesEquipoUno, golesEquipoDos
        FROM partido 
        WHERE (identificadorEquipoUno = ? OR identificadorEquipoDos = ?)
          AND jornada = ?
        ORDER BY fecha DESC 
        LIMIT 1
    """, (id_equipo, id_equipo, jornada_eliminacion))
    
    partido = cursor.fetchone()
    if not partido:
        return True
    
    id_partido, eq1, eq2, g1, g2 = partido
    ganador = determinar_ganador_partido(id_partido, eq1, g1, eq2, g2)
    return ganador != id_equipo

def determinar_ganador_partido(id_partido, eq1, g1, eq2, g2):
    """Determina el ganador de un partido considerando penales"""
    if g1 > g2:
        return eq1
    elif g2 > g1:
        return eq2
    else:
        penales = get_penales_por_partido(id_partido)
        if penales:
            p1, p2 = penales
            return eq1 if p1 > p2 else eq2
        else:
            return eq1

def InformeCuatro(equipo_nombre, fecha_limite):
    """
    Informe 4:
    Devuelve el PRÓXIMO partido que debe disputar un equipo dado
    después de una fecha dada.

    Retorna:
        (equipo_nombre, fecha_limite, partido)
    """
    conn = conectar()
    cursor = conn.cursor()

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

    cursor.execute("""
        SELECT
            p.fecha,
            p.hora,
            e1.pais AS equipo1,
            e2.pais AS equipo2,
            p.jornada,
            p.estadio
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

    fecha_p, hora, eq1, eq2, jornada, estadio = partido

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

    # 🔧 MANTENER ESTRUCTURA ORIGINAL
    return (equipo_nombre, fecha_limite,
            (fecha_p, hora, eq1, eq2, jornada, fase, estadio))

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

    # 🔧 MANTENER ESTRUCTURA ORIGINAL
    return resultados_finales

# 🔧 FUNCIONES ADICIONALES PARA FORMATEO (opcionales)
def formatear_informe_dos(grupo_nombre, fecha_limite):
    """
    Función opcional para obtener el informe 2 formateado como texto
    """
    grupo, fecha, tabla = InformeDos(grupo_nombre, fecha_limite)
    
    if not tabla:
        return f"❌ No hay datos para el Grupo {grupo_nombre} hasta {fecha_limite}"
    
    return _formatear_tabla_grupo(grupo, fecha, tabla)

def formatear_informe_cinco(fecha):
    """
    Función opcional para obtener el informe 5 formateado como texto
    """
    resultados = InformeCinco(fecha)
    
    if not resultados:
        return f"❌ No hay datos de grupos hasta la fecha {fecha}"
    
    tablas_formateadas = []
    tablas_formateadas.append(f"🏆 TABLA DE POSICIONES - TODOS LOS GRUPOS")
    tablas_formateadas.append(f"📅 Actualizado al {fecha}")
    tablas_formateadas.append("")
    
    for fecha_grupo, grupo_nombre, tabla in resultados:
        if tabla:
            tabla_grupo = _formatear_tabla_grupo(grupo_nombre, fecha_grupo, tabla)
            tablas_formateadas.append(tabla_grupo)
            tablas_formateadas.append("")
    
    return "\n".join(tablas_formateadas)

def _formatear_tabla_grupo(grupo_nombre, fecha_limite, tabla):
    """
    Función interna para formatear tablas de grupos
    """
    encabezados = ["Pos", "Equipo", "PJ", "PG", "PE", "PP", "GF", "GC", "DG", "Pts"]
    anchos = [4, 20, 3, 3, 3, 3, 3, 3, 4, 4]
    
    linea_encabezado = " | ".join(encabezados[i].center(anchos[i]) for i in range(len(encabezados)))
    separador = "-" * len(linea_encabezado)
    
    resultado = []
    resultado.append(f"🏆 GRUPO {grupo_nombre} - Hasta {fecha_limite}")
    resultado.append(separador)
    resultado.append(linea_encabezado)
    resultado.append(separador)
    
    for pos, (pais, PJ, PG, PE, PP, GF, GC, DG, Pts) in enumerate(tabla, 1):
        fila = [
            str(pos).rjust(anchos[0]),
            pais.ljust(anchos[1]),
            str(PJ).center(anchos[2]),
            str(PG).center(anchos[3]),
            str(PE).center(anchos[4]),
            str(PP).center(anchos[5]),
            str(GF).center(anchos[6]),
            str(GC).center(anchos[7]),
            str(DG).rjust(anchos[8]),
            str(Pts).center(anchos[9])
        ]
        resultado.append(" | ".join(fila))
    
    resultado.append(separador)
    return "\n".join(resultado)