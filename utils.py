from controllers.pool import conectar
import datetime
from controllers.penales import get_penales_por_partido


def tabla_posiciones_general():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT identificador, pais, grupo
        FROM equipos
        ORDER BY grupo, identificador;
    """)
    equipos = cursor.fetchall()
    tabla = []
    for e in equipos:
        tabla.append([e[0], e[1], e[2], 0, 0, 0, 0, 0, 0])

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
        
        i1 = -1
        i2 = -1
        for k in range(len(tabla)):
            if tabla[k][0] == id_1:
                i1 = k
            if tabla[k][0] == id_2:
                i2 = k

        tabla[i1][5] += goles_1
        tabla[i1][6] += goles_2
        tabla[i2][5] += goles_2
        tabla[i2][6] += goles_1
        
        tabla[i1][4] = tabla[i1][5] - tabla[i1][6]
        tabla[i2][4] = tabla[i2][5] - tabla[i2][6]
        
        tabla[i1][7] += amar_1
        tabla[i1][8] += roja_1
        tabla[i2][7] += amar_2
        tabla[i2][8] += roja_2
        
        if goles_1 > goles_2:
            tabla[i1][3] += 3
        elif goles_2 > goles_1:
            tabla[i2][3] += 3
        else:
            tabla[i1][3] += 1
            tabla[i2][3] += 1
    
    grupos = []
    for fila in tabla:
        g = fila[2]
        if g not in grupos:
            grupos.append(g)
    tabla_final = []

    for g in grupos:
        sub = []
        for fila in tabla:
            if fila[2] == g:
                sub.append(fila)

        m = len(sub)
        for a in range(m - 1):
            for b in range(m - 1 - a):
                cambiar = False
                if sub[b][3] < sub[b+1][3]:
                    cambiar = True
                elif sub[b][3] == sub[b+1][3]:
                    if sub[b][4] < sub[b+1][4]:
                        cambiar = True
                    elif sub[b][4] == sub[b+1][4]:
                        if sub[b][5] < sub[b+1][5]:
                            cambiar = True
                if cambiar:
                    sub[b], sub[b+1] = sub[b+1], sub[b]

        for fila in sub:
            tabla_final.append(fila)
    
    tabla = tabla_final
    salida = []
    for fila in tabla:
        salida.append((fila[0], fila[1], fila[3]))
    return salida


def clasificados_eliminatoria(tabla_pos):
    def ordenar_terceros(lista):
        n = len(lista)
        for i in range(n - 1):
            for j in range(n - i - 1):
                if lista[j][2] < lista[j + 1][2]:
                    lista[j], lista[j + 1] = lista[j + 1], lista[j]
        return lista
    
    grupos = {}
    for identificador, pais, puntos in tabla_pos:
        grupo = identificador[0]
        if grupo not in grupos:
            grupos[grupo] = []
        grupos[grupo].append((identificador, pais, puntos))
    
    equipos_clasificados = []
    terceros = []
    
    for grupo in grupos:
        primero = grupos[grupo][0]
        segundo = grupos[grupo][1]
        equipos_clasificados.append(primero)
        equipos_clasificados.append(segundo)
        tercero = grupos[grupo][2]
        terceros.append(tercero)
    
    terceros = ordenar_terceros(terceros)
    for p in range(4):
        clasificado_tercero = terceros[p]
        equipos_clasificados.append(clasificado_tercero)
    
    return equipos_clasificados

def definir_enfrentamientos_octavos(equipos_clasificados):
    terceros = equipos_clasificados[-4:]
    combinacion = "".join(sorted([t[0][0] for t in terceros]))

    # Combinaciones posibles según la FIFA (sin repeticiones)
    combinaciones_validas = [
        ("ABCD", "3C", "3D", "3A", "3B"),
        ("ABCE", "3C", "3A", "3B", "3E"),
        ("ABCF", "3C", "3A", "3B", "3F"),
        ("ABDE", "3D", "3A", "3B", "3E"),
        ("ABDF", "3D", "3A", "3B", "3F"),
        ("ABEF", "3E", "3A", "3B", "3F"),
        ("ACDE", "3E", "3D", "3A", "3C"),
        ("ACDF", "3C", "3D", "3A", "3F"),
        ("ACEF", "3C", "3A", "3F", "3E"),
        ("ADEF", "3D", "3A", "3F", "3E"),
        ("BCDE", "3C", "3D", "3B", "3E"),
        ("BCDF", "3C", "3D", "3B", "3F"),
        ("BCEF", "3E", "3C", "3B", "3F"),
        ("BDEF", "3E", "3D", "3B", "3F"),
        ("CDEF", "3C", "3D", "3F", "3E")
    ]

    contrario_1D = ""
    contrario_1B = ""
    contrario_1A = ""
    contrario_1C = ""

    for comb in combinaciones_validas:
        if combinacion == comb[0]:
            contrario_1D = comb[1]
            contrario_1B = comb[2]
            contrario_1A = comb[3]
            contrario_1C = comb[4]

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
        (6, "1C", contrario_1C),  # ✅ ahora usa su propio contrario
        (7, "2B", "2F"),
        (8, "1A", contrario_1A)
    ]

    resultado = []
    usados = set()

    for id_partido, alias1, alias2 in enfrentamientos_alias:
        id1, pais1 = buscar_equipo(alias1)
        id2, pais2 = buscar_equipo(alias2)
        if id1 not in usados and id2 not in usados and id1 != "" and id2 != "":
            usados.add(id1)
            usados.add(id2)
            resultado.append((id_partido, id1, pais1, id2, pais2))

    return resultado

def ultima_fecha_jornada():
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='estado_torneo'
    """)
    tabla_existe = cursor.fetchone()
    
    if not tabla_existe:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS estado_torneo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                jornada_actual INTEGER NOT NULL DEFAULT 1,
                ultima_jornada_completada INTEGER NOT NULL DEFAULT 0,
                fecha_ultima_actualizacion TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("INSERT INTO estado_torneo (jornada_actual, ultima_jornada_completada) VALUES (1, 0)")
        conn.commit()
        conn.close()
        return 1
    
    cursor.execute("SELECT jornada_actual FROM estado_torneo WHERE id = 1")
    resultado = cursor.fetchone()
    conn.close()
    
    return resultado[0] if resultado else 1


# 🔧 CORREGIDO: ahora usa asignar funciones con penales y flujo actualizado
def cerrar_jornada():
    from tkinter import messagebox
    import traceback
    
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT jornada_actual FROM estado_torneo WHERE id = 1")
    result = cursor.fetchone()
    if not result:
        messagebox.showerror("Error", "No se pudo obtener la jornada actual")
        conn.close()
        return 1
    
    jornada_actual = result[0]
    nueva_jornada = jornada_actual + 1

    cursor.execute("""
        UPDATE estado_torneo 
        SET jornada_actual = ?, 
            ultima_jornada_completada = ?,
            fecha_ultima_actualizacion = CURRENT_TIMESTAMP
        WHERE id = 1
    """, (nueva_jornada, jornada_actual))
    conn.commit()
    conn.close()

    try:
        if jornada_actual == 3:
            messagebox.showinfo("Info", "Generando octavos de final...")
            tabla_pos = tabla_posiciones_general()
            equipos_clasificados = clasificados_eliminatoria(tabla_pos)
            enfrentamientos_octavos = definir_enfrentamientos_octavos(equipos_clasificados)
            asignar_equipos_octavos(enfrentamientos_octavos)
            messagebox.showinfo("Éxito", "✅ Octavos de final asignados correctamente")

        elif jornada_actual == 4:
            messagebox.showinfo("Info", "Generando cuartos de final...")
            asignar_equipos_cuartos()  # 🔧 CORREGIDO: nombre de función
            messagebox.showinfo("Éxito", "✅ Cuartos de final asignados correctamente (con penales)")

        elif jornada_actual == 5:
            messagebox.showinfo("Info", "Generando semifinales...")
            asignar_equipos_semifinales()  # 🔧 CORREGIDO: nombre de función
            messagebox.showinfo("Éxito", "✅ Semifinales asignadas correctamente (con penales)")

        elif jornada_actual == 6:
            messagebox.showinfo("Info", "Generando final y tercer puesto...")
            asignar_equipos_tercer_puesto()  # 🔧 CORREGIDO: nombre de función
            asignar_equipos_final()  # 🔧 CORREGIDO: nombre de función
            messagebox.showinfo("Éxito", "✅ Final y tercer puesto asignados correctamente (con penales)")

    except Exception as e:
        error_msg = f"Error al cerrar jornada {jornada_actual}: {str(e)}\n\n{traceback.format_exc()}"
        messagebox.showerror("Error", error_msg)
    
    return nueva_jornada


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
        if fecha is None or fecha == "":
            datos_validos = False
        if hora is None or hora == "":
            datos_validos = False
        if not datos_validos:
            return False
    return True


def obtener_ids_partidos_jornada(jornada):
    if jornada == 1:
        return list(range(1, 13))
    elif jornada == 2:
        return list(range(13, 25))
    elif jornada == 3:
        return list(range(25, 37))
    elif jornada == 4:
        return list(range(37, 45))
    elif jornada == 5:
        return list(range(45, 49))
    elif jornada == 6:
        return list(range(49, 51))
    elif jornada == 7:
        return [51]
    elif jornada == 8:
        return [52]
    return []


def asignar_equipos_octavos(enfrentamientos):
    from tkinter import messagebox
    conn = conectar()
    cursor = conn.cursor()
    ids_partidos = obtener_ids_partidos_jornada(4)
    info_asignacion = "Asignando equipos a octavos:\n\n"
    for i, (id_partido, id_equipo1, pais1, id_equipo2, pais2) in enumerate(enfrentamientos):
        if i < len(ids_partidos):
            id_partido_real = ids_partidos[i]
            info_asignacion += f"Partido {id_partido_real}: {id_equipo1} vs {id_equipo2}\n"
            cursor.execute("""
                UPDATE partido 
                SET identificadorEquipoUno = ?, identificadorEquipoDos = ?
                WHERE idPartido = ?
            """, (id_equipo1, id_equipo2, id_partido_real))
    conn.commit()
    conn.close()
    messagebox.showinfo("Asignación Completada", info_asignacion)


def obtener_ganadores_jornada(jornada):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT idPartido, identificadorEquipoUno, identificadorEquipoDos, 
               golesEquipoUno, golesEquipoDos
        FROM partido 
        WHERE jornada = ?
    """, (jornada,))
    partidos = cursor.fetchall()
    ganadores = []
    for partido in partidos:
        id_partido, equipo1, equipo2, goles1, goles2 = partido
        if goles1 > goles2:
            ganadores.append(equipo1)
        elif goles2 > goles1:
            ganadores.append(equipo2)
        else:
            # 🔧 AGREGADO: Verificación de penales para octavos
            penales = get_penales_por_partido(id_partido)
            if penales:
                p1, p2 = penales
                ganador = equipo1 if p1 > p2 else equipo2
                ganadores.append(ganador)
            else:
                # Si no hay penales, se asume el primer equipo como ganador (esto podría mejorarse)
                ganadores.append(equipo1)
    conn.close()
    return ganadores


def obtener_ganadores_y_perdedores_jornada(jornada):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT idPartido, identificadorEquipoUno, identificadorEquipoDos, 
               golesEquipoUno, golesEquipoDos
        FROM partido 
        WHERE jornada = ?
    """, (jornada,))
    partidos = cursor.fetchall()
    ganadores, perdedores = [], []
    for partido in partidos:
        id_partido, equipo1, equipo2, goles1, goles2 = partido
        if goles1 > goles2:
            ganadores.append(equipo1)
            perdedores.append(equipo2)
        elif goles2 > goles1:
            ganadores.append(equipo2)
            perdedores.append(equipo1)
        else:
            # 🔧 AGREGADO: Verificación de penales para octavos
            penales = get_penales_por_partido(id_partido)
            if penales:
                p1, p2 = penales
                if p1 > p2:
                    ganadores.append(equipo1)
                    perdedores.append(equipo2)
                else:
                    ganadores.append(equipo2)
                    perdedores.append(equipo1)
            else:
                # Si no hay penales, se asume el primer equipo como ganador
                ganadores.append(equipo1)
                perdedores.append(equipo2)
    conn.close()
    return ganadores, perdedores


def generar_enfrentamientos_cuartos(ganadores_octavos):
    enfrentamientos = [
        (1, ganadores_octavos[0], ganadores_octavos[1]),
        (2, ganadores_octavos[2], ganadores_octavos[3]),
        (3, ganadores_octavos[4], ganadores_octavos[5]),
        (4, ganadores_octavos[6], ganadores_octavos[7])
    ]
    return enfrentamientos


def generar_enfrentamientos_semifinales(ganadores_cuartos):
    enfrentamientos = [
        (1, ganadores_cuartos[0], ganadores_cuartos[1]),
        (2, ganadores_cuartos[2], ganadores_cuartos[3])
    ]
    return enfrentamientos


def generar_enfrentamiento_final(ganadores_semifinales):
    return [(1, ganadores_semifinales[0], ganadores_semifinales[1])]


def generar_enfrentamiento_tercer_puesto(perdedores_semifinales):
    return [(1, perdedores_semifinales[0], perdedores_semifinales[1])]


# 🔧 CORREGIDO: Funciones con nombres correctos y con verificación de penales

def asignar_equipos_cuartos():
    from tkinter import messagebox
    conn = conectar()
    cursor = conn.cursor()
    
    # Obtener ganadores de octavos con verificación de penales
    ganadores_octavos = obtener_ganadores_jornada(4)
    
    if len(ganadores_octavos) != 8:
        messagebox.showerror("Error", f"No hay suficientes ganadores en octavos: {len(ganadores_octavos)}")
        conn.close()
        return
    
    enfrentamientos = generar_enfrentamientos_cuartos(ganadores_octavos)
    ids_partidos = obtener_ids_partidos_jornada(5)
    
    info_asignacion = "Asignando equipos a cuartos:\n\n"
    for i, (_, equipo1, equipo2) in enumerate(enfrentamientos):
        if i < len(ids_partidos):
            id_partido_real = ids_partidos[i]
            info_asignacion += f"Partido {id_partido_real}: {equipo1} vs {equipo2}\n"
            cursor.execute("""
                UPDATE partido 
                SET identificadorEquipoUno = ?, identificadorEquipoDos = ?
                WHERE idPartido = ?
            """, (equipo1, equipo2, id_partido_real))
    
    conn.commit()
    conn.close()
    messagebox.showinfo("Asignación Completada", info_asignacion)


def asignar_equipos_semifinales():
    from tkinter import messagebox
    conn = conectar()
    cursor = conn.cursor()
    
    # Obtener ganadores de cuartos con verificación de penales
    ganadores_cuartos = obtener_ganadores_jornada(5)
    
    if len(ganadores_cuartos) != 4:
        messagebox.showerror("Error", f"No hay suficientes ganadores en cuartos: {len(ganadores_cuartos)}")
        conn.close()
        return
    
    enfrentamientos = generar_enfrentamientos_semifinales(ganadores_cuartos)
    ids_partidos = obtener_ids_partidos_jornada(6)
    
    info_asignacion = "Asignando equipos a semifinales:\n\n"
    for i, (_, equipo1, equipo2) in enumerate(enfrentamientos):
        if i < len(ids_partidos):
            id_partido_real = ids_partidos[i]
            info_asignacion += f"Partido {id_partido_real}: {equipo1} vs {equipo2}\n"
            cursor.execute("""
                UPDATE partido 
                SET identificadorEquipoUno = ?, identificadorEquipoDos = ?
                WHERE idPartido = ?
            """, (equipo1, equipo2, id_partido_real))
    
    conn.commit()
    conn.close()
    messagebox.showinfo("Asignación Completada", info_asignacion)


def asignar_equipos_final():
    from tkinter import messagebox
    conn = conectar()
    cursor = conn.cursor()
    
    # Obtener ganadores de semifinales con verificación de penales
    ganadores_semifinales = obtener_ganadores_jornada(6)
    
    if len(ganadores_semifinales) != 2:
        messagebox.showerror("Error", f"No hay suficientes ganadores en semifinales: {len(ganadores_semifinales)}")
        conn.close()
        return
    
    enfrentamientos = generar_enfrentamiento_final(ganadores_semifinales)
    ids_partidos = obtener_ids_partidos_jornada(8)  # Jornada 8 para la final
    
    info_asignacion = "Asignando equipos a la final:\n\n"
    for i, (_, equipo1, equipo2) in enumerate(enfrentamientos):
        if i < len(ids_partidos):
            id_partido_real = ids_partidos[i]
            info_asignacion += f"Partido {id_partido_real}: {equipo1} vs {equipo2}\n"
            cursor.execute("""
                UPDATE partido 
                SET identificadorEquipoUno = ?, identificadorEquipoDos = ?
                WHERE idPartido = ?
            """, (equipo1, equipo2, id_partido_real))
    
    conn.commit()
    conn.close()
    messagebox.showinfo("Asignación Completada", info_asignacion)


def asignar_equipos_tercer_puesto():
    from tkinter import messagebox
    conn = conectar()
    cursor = conn.cursor()
    
    # Obtener perdedores de semifinales
    _, perdedores_semifinales = obtener_ganadores_y_perdedores_jornada(6)
    
    if len(perdedores_semifinales) != 2:
        messagebox.showerror("Error", f"No hay suficientes perdedores en semifinales: {len(perdedores_semifinales)}")
        conn.close()
        return
    
    enfrentamientos = generar_enfrentamiento_tercer_puesto(perdedores_semifinales)
    ids_partidos = obtener_ids_partidos_jornada(7)  # Jornada 7 para tercer puesto
    
    info_asignacion = "Asignando equipos al partido por tercer puesto:\n\n"
    for i, (_, equipo1, equipo2) in enumerate(enfrentamientos):
        if i < len(ids_partidos):
            id_partido_real = ids_partidos[i]
            info_asignacion += f"Partido {id_partido_real}: {equipo1} vs {equipo2}\n"
            cursor.execute("""
                UPDATE partido 
                SET identificadorEquipoUno = ?, identificadorEquipoDos = ?
                WHERE idPartido = ?
            """, (equipo1, equipo2, id_partido_real))
    
    conn.commit()
    conn.close()
    messagebox.showinfo("Asignación Completada", info_asignacion)