from controllers.pool import conectar
def tabla_posiciones():
    """
    Genera la tabla de posiciones considerando desempates por grupo
    según los criterios especificados (1 a 9),
    y muestra la tabla jerarquizada por grupo.
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            e.identificador,
            e.pais,
            e.idGrupo,
            COALESCE(SUM(
                CASE WHEN p.identificadorEquipoUno = e.identificador THEN p.puntosEquipoUno ELSE 0 END
            ), 0)
            +
            COALESCE(SUM(
                CASE WHEN p.identificadorEquipoDos = e.identificador THEN p.puntosEquipoDos ELSE 0 END
            ), 0)
            AS puntos_totales,
            COALESCE(SUM(
                CASE WHEN p.identificadorEquipoUno = e.identificador THEN p.golesEquipoUno - p.golesEquipoDos
                     WHEN p.identificadorEquipoDos = e.identificador THEN p.golesEquipoDos - p.golesEquipoUno
                     ELSE 0 END
            ), 0) AS diferencia_goles,
            COALESCE(SUM(
                CASE WHEN p.identificadorEquipoUno = e.identificador THEN p.golesEquipoUno
                     WHEN p.identificadorEquipoDos = e.identificador THEN p.golesEquipoDos
                     ELSE 0 END
            ), 0) AS goles_favor,
            COALESCE(SUM(
                CASE WHEN p.identificadorEquipoUno = e.identificador THEN p.tarjetasAmarillasEquipoUno
                     WHEN p.identificadorEquipoDos = e.identificador THEN p.tarjetasAmarillasEquipoDos
                     ELSE 0 END
            ), 0) AS amarillas,
            COALESCE(SUM(
                CASE WHEN p.identificadorEquipoUno = e.identificador THEN p.tarjetasRojasEquipoUno
                     WHEN p.identificadorEquipoDos = e.identificador THEN p.tarjetasRojasEquipoDos
                     ELSE 0 END
            ), 0) AS rojas
        FROM equipos e
        LEFT JOIN partido p
        ON e.identificador = p.identificadorEquipoUno
        OR e.identificador = p.identificadorEquipoDos
        GROUP BY e.identificador, e.pais, e.idGrupo
        ORDER BY e.idGrupo, puntos_totales DESC;
    """)

    tabla = cursor.fetchall()
    conn.close()

    # Convertir a lista mutable
    tabla = list(tabla)

    # Aplicar desempates dentro de cada grupo (como ya tenías)
    for i in range(len(tabla) - 1):
        eq1 = tabla[i]
        eq2 = tabla[i + 1]

        # Solo desempatar si pertenecen al mismo grupo y están empatados en puntos
        if eq1[2] == eq2[2] and eq1[3] == eq2[3]:
            conn = conectar()
            c = conn.cursor()

            # Enfrentamiento directo entre ambos
            c.execute("""
                SELECT 
                    SUM(CASE WHEN identificadorEquipoUno = ? THEN puntosEquipoUno 
                             WHEN identificadorEquipoDos = ? THEN puntosEquipoDos ELSE 0 END),
                    SUM(CASE WHEN identificadorEquipoUno = ? THEN golesEquipoUno - golesEquipoDos
                             WHEN identificadorEquipoDos = ? THEN golesEquipoDos - golesEquipoUno ELSE 0 END),
                    SUM(CASE WHEN identificadorEquipoUno = ? THEN golesEquipoUno
                             WHEN identificadorEquipoDos = ? THEN golesEquipoDos ELSE 0 END)
                FROM partido
                WHERE (identificadorEquipoUno = ? AND identificadorEquipoDos = ?)
                   OR (identificadorEquipoUno = ? AND identificadorEquipoDos = ?);
            """, (
                eq1[0], eq1[0],
                eq1[0], eq1[0],
                eq1[0], eq1[0],
                eq1[0], eq2[0],
                eq2[0], eq1[0]
            ))

            enfrentamiento = c.fetchone()
            conn.close()

            c1 = enfrentamiento[0] or 0
            c2 = enfrentamiento[1] or 0
            c3 = enfrentamiento[2] or 0

            # Diferencias generales
            c4 = eq1[3] - eq2[3]  # puntos totales
            c5 = eq1[4] - eq2[4]  # dif goles general
            c6 = eq1[5] - eq2[5]  # goles a favor general
            c7 = eq2[6] - eq1[6]  # menos amarillas mejor
            c8 = eq2[7] - eq1[7]  # menos rojas mejor

            criterios = [c1, c2, c3, c4, c5, c6, c7, c8]
            for c in criterios:
                if c > 0:
                    break
                elif c < 0:
                    tabla[i], tabla[i + 1] = tabla[i + 1], tabla[i]
                    break

    # Agrupar equipos por grupo
    grupos = {}
    for fila in tabla:
        idGrupo = fila[2]
        if idGrupo not in grupos:
            grupos[idGrupo] = []
        grupos[idGrupo].append(fila)

    # --- Mostrar tabla en consola agrupada por grupo ---
    print("\nTABLA DE POSICIONES POR GRUPO")
    print("-" * 45)
    for idGrupo in grupos: 
        print(f"\nGRUPO {idGrupo}")
        print(f"{'Identificador':<15}{'Pais':<15}{'Pts':<10}")
        print("-" * 40)
        for fila in grupos[idGrupo]:
            print(f"{fila[0]:<15}{fila[1]:<15}{fila[3]:<10}")

    # --- Retornar solo identificador, país y puntos ---
    tabla_final = [(fila[0], fila[1], fila[3]) for fila in tabla]
    return tabla_final
def ordenar_terceros(lista):
    #me fui a la segura con bubble
    n = len(lista)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if lista[j][2] < lista[j + 1][2]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    return lista

def clasificados_eliminatoria(tabla_pos):
    grupos = {}
    for identificador, pais, puntos in tabla_pos:
        grupo = identificador[0]  # Primera letra
        if grupo not in grupos:
            grupos[grupo] = []
        grupos[grupo].append((identificador, pais, puntos))
    equipos_clasificados=[]
    terceros=[] #para verificar mejores terceros despues
    for grupo in grupos:
        #agrego ya el 1° y 2°, cargo aparte los 3° para compararlos despues
        primero=grupos[grupo][0]
        primero.append(equipos_clasificados)
        segundo=grupos[grupo][1]
        segundo.append(equipos_clasificados)
        tercero = grupos[grupo][2]  # Índice 2 = tercer puesto
        terceros.append(tercero)
    terceros=ordenar_terceros(terceros)
    for p in range (4):
        clasificado_tercero= grupos[grupo][p]
        clasificado_tercero.append(equipos_clasificados)