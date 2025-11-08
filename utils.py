from controllers.pool import conectar
def tabla_posiciones_general():
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
        WHERE p.jornada IN (1, 2, 3)
        GROUP BY e.identificador, e.pais, e.idGrupo
        ORDER BY e.idGrupo, puntos_totales DESC;
    """)

    tabla = cursor.fetchall()
    conn.close()

    tabla = list(tabla)

    # Aplicar desempates dentro de cada grupo
    for i in range(len(tabla) - 1):
        eq1 = tabla[i]
        eq2 = tabla[i + 1]

        if eq1[2] == eq2[2] and eq1[3] == eq2[3]:
            conn = conectar()
            cursor= conn.cursor()
            cursor.execute("""
                SELECT 
                    SUM(CASE WHEN identificadorEquipoUno = ? THEN puntosEquipoUno 
                             WHEN identificadorEquipoDos = ? THEN puntosEquipoDos ELSE 0 END),
                    SUM(CASE WHEN identificadorEquipoUno = ? THEN golesEquipoUno - golesEquipoDos
                             WHEN identificadorEquipoDos = ? THEN golesEquipoDos - golesEquipoUno ELSE 0 END),
                    SUM(CASE WHEN identificadorEquipoUno = ? THEN golesEquipoUno
                             WHEN identificadorEquipoDos = ? THEN golesEquipoDos ELSE 0 END)
                FROM partido
                WHERE ((identificadorEquipoUno = ? AND identificadorEquipoDos = ?)
                   OR (identificadorEquipoUno = ? AND identificadorEquipoDos = ?))
                  AND jornada IN (1, 2, 3);
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
            c4 = eq1[3] - eq2[3]
            c5 = eq1[4] - eq2[4]
            c6 = eq1[5] - eq2[5]
            c7 = eq2[6] - eq1[6]
            c8 = eq2[7] - eq1[7]

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

    print("\nTABLA DE POSICIONES POR GRUPO (Jornadas 1-3)")
    print("-" * 45)
    for idGrupo in grupos: 
        print(f"\nGRUPO {idGrupo}")
        print(f"{'Identificador':<15}{'Pais':<15}{'Pts':<10}")
        print("-" * 40)
        for fila in grupos[idGrupo]:
            print(f"{fila[0]:<15}{fila[1]:<15}{fila[3]:<10}")

    tabla_final = [(fila[0], fila[1], fila[3]) for fila in tabla]
    return tabla_final
def clasificados_eliminatoria(tabla_pos):
    def ordenar_terceros(lista):
        #me fui a la segura con bubble
        n = len(lista)
        for i in range(n - 1):
            for j in range(n - i - 1):
                if lista[j][2] < lista[j + 1][2]:
                    lista[j], lista[j + 1] = lista[j + 1], lista[j]
        return lista
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
        primero = grupos[grupo][0]
        segundo = grupos[grupo][1]
        equipos_clasificados.append(primero)
        equipos_clasificados.append(segundo)
        tercero = grupos[grupo][2]  # Índice 2 = tercer puesto
        terceros.append(tercero)
    terceros=ordenar_terceros(terceros)
    for p in range(4):
        clasificado_tercero = terceros[p]
        equipos_clasificados.append(clasificado_tercero)
    return equipos_clasificados
def definir_enfrentamientos_octavos(equipos_clasificados):
    # Los últimos 4 son los mejores terceros (ya ordenados)
    terceros = equipos_clasificados[-4:]
    # Obtener combinación alfabética (ej: "ABCD")
    combinacion = "".join(sorted([t[0][0] for t in terceros]))
    # Combinaciones válidas con sus contrarios
    combinaciones_validas = [
        ("ABCD", "3C", "3D", "3A"),
        ("ABCE", "3C", "3A", "3B"),
        ("ABCF", "3C", "3A", "3B"),
        ("ABDE", "3D", "3A", "3B"),
        ("ABDF", "3D", "3A", "3B"),
        ("ABEF", "3E", "3A", "3B"),
        ("ACDE", "3E", "3D", "3A"),
        ("ACDF", "3C", "3D", "3A"),
        ("ACEF", "3C", "3A", "3F"),
        ("ADEF", "3D", "3A", "3F"),
        ("BCDE", "3C", "3D", "3B"),
        ("BCDF", "3C", "3D", "3B"),
        ("BCEF", "3E", "3C", "3B"),
        ("BDEF", "3E", "3D", "3B"),
        ("CDEF", "3C", "3D", "3F")
    ]
    contrario_1D = ""
    contrario_1B = ""
    contrario_1A = ""
    for comb in combinaciones_validas:
        if combinacion == comb[0]:
            contrario_1D = comb[1]
            contrario_1B = comb[2]
            contrario_1A = comb[3]
    #para que retorne el identificador (tipo A1) y no la combinacion 1A
    def buscar_equipo(alias):
        if alias == "":
            return ("", "")
        grupo = alias[1]
        pos = int(alias[0])
        contador = 0
        for eq in equipos_clasificados:
            if eq[0][0] == grupo:
                contador += 1
                if contador == pos:
                    return (eq[0], eq[1])
        return ("", "")
    enfrentamientos_alias = [
        (1, "2A", "2C"),
        (2, "1D", contrario_1D),
        (3, "1B", contrario_1B),
        (4, "1F", "2E"),
        (5, "1E", "2D"),
        (6, "1C", contrario_1A),
        (7, "2B", "2F"),
        (8, "1A", contrario_1A)
    ]

    resultado = []
    for id_partido, alias1, alias2 in enfrentamientos_alias:
        id1, pais1 = buscar_equipo(alias1)
        id2, pais2 = buscar_equipo(alias2)
        if id2 != "":
            resultado.append((id_partido, id1, pais1, id2, pais2))
    return resultado