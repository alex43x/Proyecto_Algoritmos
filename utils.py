from controllers.pool import conectar
import datetime
def tabla_posiciones_general():
    conn = conectar()
    cursor = conn.cursor()
    # 1. Cargar todos los equipos: (id, pais, grupo)
    cursor.execute("""
        SELECT identificador, pais, grupo
        FROM equipos
        ORDER BY grupo, identificador;
    """)
    equipos = cursor.fetchall()
    # tabla[fila] = [id, pais, grupo, pts, dg, gf, gc, amarillas, rojas]
    tabla = []
    for e in equipos:
        tabla.append([e[0], e[1], e[2], 0, 0, 0, 0, 0, 0])

    # 2. Cargar todos los partidos de fase de grupos
    cursor.execute("""
        SELECT identificadorEquipoUno, identificadorEquipoDos,
               golesEquipoUno, golesEquipoDos,
               tarjetasAmarillasEquipoUno, tarjetasAmarillasEquipoDos,
               tarjetasRojasEquipoUno, tarjetasRojasEquipoDos
        FROM partido
        WHERE jornada IN (1, 2, 3);
    """)
    partidos = cursor.fetchall()
    conn.close()
    for p in partidos:
        id_1 = p[0]
        id_2 = p[1]

        goles_1 = p[2]
        goles_2 = p[3]

        amar_1 = p[4]
        amar_2 = p[5]

        roja_1 = p[6]
        roja_2 = p[7]
        # Buscar índices en tabla
        i1 = -1
        i2 = -1
        for k in range(len(tabla)):
            if tabla[k][0] == id_1:
                i1 = k
            if tabla[k][0] == id_2:
                i2 = k
        # Goles a favor y en contra
        tabla[i1][5] += goles_1   # GF
        tabla[i1][6] += goles_2   # GC
        tabla[i2][5] += goles_2
        tabla[i2][6] += goles_1
        # Diferencia de goles
        tabla[i1][4] = tabla[i1][5] - tabla[i1][6]
        tabla[i2][4] = tabla[i2][5] - tabla[i2][6]
        # Tarjetas
        tabla[i1][7] += amar_1
        tabla[i1][8] += roja_1
        tabla[i2][7] += amar_2
        tabla[i2][8] += roja_2
        # Puntos acumulados (regla 3-1-0)
        if goles_1 > goles_2:
            tabla[i1][3] += 3
        elif goles_2 > goles_1:
            tabla[i2][3] += 3
        else:
            tabla[i1][3] += 1
            tabla[i2][3] += 1
    # 4. ORDENAR POR GRUPO (bubble limpio por cada grupo)
    # Obtener lista de grupos únicos
    grupos = []
    for fila in tabla:
        g = fila[2]
        if g not in grupos:
            grupos.append(g)
    tabla_final = []

    # Ordenar cada grupo por separado
    for g in grupos:
        # Extraer equipos del grupo g
        sub = []
        for fila in tabla:
            if fila[2] == g:
                sub.append(fila)

        # Bubble sort por puntos, DG y GF
        m = len(sub)
        for a in range(m - 1):
            for b in range(m - 1 - a):

                cambiar = False

                # 1. Puntos
                if sub[b][3] < sub[b+1][3]:
                    cambiar = True

                elif sub[b][3] == sub[b+1][3]:

                    # 2. DG
                    if sub[b][4] < sub[b+1][4]:
                        cambiar = True

                    elif sub[b][4] == sub[b+1][4]:

                        # 3. GF
                        if sub[b][5] < sub[b+1][5]:
                            cambiar = True

                if cambiar:
                    sub[b], sub[b+1] = sub[b+1], sub[b]

        # Añadir grupo ordenado
        for fila in sub:
            tabla_final.append(fila)
    tabla = tabla_final
    print("\nTABLA DE POSICIONES POR GRUPO (Jornadas 1-3)")
    print("------------------------------------------------")
    grupo_actual = None
    for fila in tabla:
        id_eq  = fila[0]
        pais   = fila[1]
        grupo  = fila[2]
        pts    = fila[3]
        dg     = fila[4]
        gf     = fila[5]
        gc     = fila[6]
        if grupo != grupo_actual:
            grupo_actual = grupo
            print(f"\nGRUPO {grupo_actual}")
            print(f"{'ID':<10}{'Pais':<15}{'Pts':<6}{'DG':<6}{'GF':<6}{'GC':<6}")
            print("----------------------------------------")
        print(f"{id_eq:<10}{pais:<15}{pts:<6}{dg:<6}{gf:<6}{gc:<6}")
    salida = []
    for fila in tabla:
        salida.append((fila[0], fila[1], fila[3]))
    return salida
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
#funcion para evaluar si la jornada esta totalmente cargada
#para ver hasta que jornada se completo
#devuelve 0 si la jornada 1 no se cargo por completo, luego entrega el ultimo cargado
#por j1 completa y j2 no, devuelve j1 
def ultima_fecha_jornada():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT jornada, fecha
        FROM partido
        ORDER BY jornada ASC;
    """)
    registros = cursor.fetchall()
    conn.close()
    if len(registros) == 0:
        return 0
    ultima_completa = 0
    jornada_actual = 1
    while jornada_actual <= 7:
        todos_con_fecha = True
        # Revisar partidos de esta jornada
        for fila in registros:
            jornada_fila = fila[0]
            fecha_fila = fila[1]
            if jornada_fila == jornada_actual:
                if fecha_fila == "" or fecha_fila is None:
                    todos_con_fecha = False
                    break
        if todos_con_fecha:
            ultima_completa = jornada_actual
        else:
            break
        jornada_actual = jornada_actual + 1
    return ultima_completa
def carga_completa_fechas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT fecha, hora
        FROM partido
        ORDER BY jornada, idPartido;
    """)
    registros = cursor.fetchall()
    conn.close()
    for fila in registros:
        fecha = fila[0]
        hora  = fila[1]
        datos_validos = True
        if fecha is None:
            datos_validos = False
        elif fecha == "":
            datos_validos = False

        if hora is None:
            datos_validos = False
        elif hora == "":
            datos_validos = False
        if datos_validos == False:
            return False
    return True